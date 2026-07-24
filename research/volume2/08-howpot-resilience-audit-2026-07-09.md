> 快照自 /Users/jimi/ClaudeCode/Howpot/howpot-chat/docs/resilience-audit-2026-07-09.md · 2026-07-17 拷贝，供第二卷 §一 引用；原文件为准。

# Howpot Chat 韧性摸底报告与工程化建设方案

日期: 2026-07-09
方法: 9 路专项审计（7 路主线 + 2 路查漏补审），P0/P1 发现逐条独立对抗验证，全部结论有 file:line 实证。
状态: 摸底完成，建设方案待用户审批。**本报告未修改任何代码。**

## 一、总体诊断

系统的结构性缺陷可以归结为一句话：**运行中的对话没有真相源（SSOT）**。一轮 run 的过程态只存在于两个易失载体里——一条一次性 HTTP 流和 server 内存。消息要等 run 彻底结束才由 `persistRunMessages()` 一次性写入 SQLite。于是任何一环断掉（前端卸载、webview 导航、进程退出、同会话抢占），用户都会看到内容消失，其中两条路径造成真实的永久丢失。

用户报告的两个 bug 都不是单点问题，而是这个结构缺陷与其他机制交叉的产物。良好的一面：run 生命周期加固（fix/run-lifecycle-hardening）留下的 finishPromise / isCurrentRun / safeWrite 等机制质量不错，多数修复可以复用它们，不需要推倒重来。

## 二、两个已报 Bug 的根因链

### Bug 1: 切走再切回运行中会话，UI 空白

因果链（每环均已实证 + 独立验证 CONFIRMED）：

1. run 进行中，这一轮对话在 SQLite 里不存在。`persistRunMessages()`（chat.ts:2418-2544）是浏览器问答链路唯一落库点，只在 run 收尾的 finally/catch 调用（chat.ts:2166/2227）。
2. 切换会话时前端 runtime 整体销毁重建。App.tsx:626 `key={currentSessionId}-${threadKey}`，注释自述 "ensures the runtime is fully recreated on session switch"。fetch 被 abort（ChatAdapter.ts:193, 429-432）。
3. server 端是故意不杀 run 的。chat.ts:1642-1644 注释："We no longer auto-abort runs on SSE disconnect... the server run should continue in the background"；safeWrite（chat.ts:1854-1861）让流死掉后 agent 继续跑完。**设计只做了一半：断开是安全的，但没有做"接回来"。**
4. 切回时新 runtime 只 GET `/api/sessions/:id/messages`（SQLite 直读，sessions.ts:372-380）。因为第 1 条，读到的是 run 开始前的状态——新会话第一轮就是空数组，Thread 渲染欢迎屏（Thread.tsx:1031-1046），观感即"空白"。
5. 切回后唯一的"临场感"是一次性 GET `/api/runtime-state/:id` 快照（App.tsx:395-398），只含 phase/tokens 不含消息正文，且不再更新。run 后台完成落库后，界面也没有任何机制自动重拉——必须再切走一次再切回。
6. 叠加丢失路径：用户若在切回后的"空白"会话里继续发消息，`RunManager.start()`（run-manager.ts:43-49）立即抢占旧 run，旧 handler 的 `isCurrentRun` 判假后跳过持久化——旧一轮（含用户消息）永久丢失。

### Bug 2: 点链接原地跳走，返回后"对话记录全没了"

三个独立缺口叠加：

1. **外链无兜底（触发器）**：Thread.tsx:50 只渲染 `<a target="_blank">`；两套 Tauri 壳都没有 plugin-shell/opener，main.rs 无 on_navigation，capabilities 只有 core:default。Tauri 默认行为下 `_blank` 不开新窗口，主 webview 原地导航，SPA 整体被替换，且窗口无浏览器工具栏，只能右键"后退"。无 beforeunload 守卫。
2. **返回后"看起来丢了"**：SPA 重载，project/session 恢复逻辑（localStorage + DB）本身可用，但若被打断那轮 run 未跑完，读库读不到最后一轮 → 显示缺一轮甚至空会话。此时数据并未真丢（run 在后台跑完会落库）。
3. **然后真丢了（Bug2 的实质）**：用户误判对话丢失，在同一会话重新提问。`tryStart→start()` 抢占语义不等旧 run 落盘（run-manager.ts:44-49 abort 后立即 `runs.set` 覆盖），旧 handler `isCurrentRun` 判假（chat.ts:2219-2220），整轮跳过 `persistRunMessages` ——被打断那轮连同用户消息从未写库。此路径有单测验证其"替换"行为，但没人测过它对持久化的副作用。

## 三、发现清单（去重合并后）

同一根因被多路独立发现的已合并，标注印证路数。

### P0 — 已报 bug 根因 / 必然的数据丢失（5 条）

| # | 缺口 | 关键证据 | 印证 |
|---|---|---|---|
| P0-1 | run 进行中零落库：用户消息与流式内容都要等 run 结束才写库，形成查询盲区，且放大一切"中途死掉"场景 | chat.ts:2418-2544, 2166/2227; sessions.ts:372-380 | 3 路独立 |
| P0-2 | RunManager.start() 同会话抢占静默丢弃前一轮（含用户消息），不等待旧 run 落盘 | run-manager.ts:43-49; chat.ts:2219-2220 | 3 路独立 |
| P0-3 | 外链在主 webview 原地跳转：无 opener/shell 插件、无 on_navigation、无 beforeunload | Thread.tsx:50; src-tauri/Cargo.toml; capabilities/default.json | 2 路 |
| P0-4 | 应用退出（托盘退出/窗口 Destroyed）不检测不等待运行中 run，整轮丢失无标记：kill_node() 先 POST /api/shutdown 再 sleep 2s 强杀，shutdown 路由不检查 RunManager | main.rs:224-227, 258-260, 404-429; index.ts:103-127 | 2 路独立 |
| P0-5 | 运行时还原备份直接覆盖被活跃 SessionStore 持有连接的 db 文件，不走 close/checkpoint/reopen | backup 路由 + session-store.ts（查漏补审实证） | 1 路+验证 |

### P1 — 特定交叉场景下的状态损坏/卡死/丢失

**流与恢复:**
- 无"重新挂接进行中 run"机制：切回/重载后界面停在快照，run 完成后视图也不自动重拉（3 路独立发现）
- 后台 run 完成零用户感知（用户 2026-07-09 补报）：chat.ts run 收尾路径不触发任何通知；通知基础设施齐全但未接线——/api/notifications 轮询通道 + Web Notification 权限（App.tsx:354-373）目前只服务 cron 提醒，Tauri set_focus（main.rs:54）只用在托盘点击。与"SSE 断开不杀 run"的半途设计同源：后台跑完做了，跑完让用户知道没做
- SSE 出错分支不发 [DONE]，ChatAdapter 无 error 事件分支：非 agent-loop 异常导致流静默死亡，UI 永远"生成中"
- ErrorBoundary 包住整个 shell：一处消息渲染崩溃全屏爆炸；Retry 仅清 state，坏数据死循环；叠加 localStorage 自动恢复上次会话 → **重启客户端也可能立即复现崩溃，无逃生通道**（验证员认为有理由升 P0）

**持久化:**
- SQLite 写入失败（磁盘满/锁）在两处落盘路径被静默吞掉（chat.ts:2166-2169 catch 仅 console.error），用户看到"已完成"实际没写库
- 工具的文件修改（file_snapshots）实时落盘，但进程终止时归属消息随之丢失——聊天记录看不到"崩溃前改了什么"

**并发与中止:**
- tool-confirm 挂起无超时：刷新/切走后全局 run 锁被无限期占用
- ask_user 的 execute() 不接收 abortSignal：Stop 与删除会话都解除不了等待
- Stop 是假停止：shell_exec/write_file/git 执行期间本地显示已停，服务端子进程继续跑 5-10 分钟，应用退出也不回收

**壳与进程:**
- server 子进程启动后崩溃：壳不重启、UI 检测不到（连接指示灯只在挂载时检查一次）
- 启动失败/超时诊断页是死胡同：无重试按钮，"关闭窗口"已被改造成隐藏而非退出

**运维通道（查漏补审新发现）:**
- 热更新×4：dist 既是替换目标又是静态资源实时读盘来源（替换窗口刷新可白屏）；更新后无强制重启（"已更新"实跑旧代码，漂移窗口无限期）；无 active-run 门槛（RunManager 有现成接口但更新完全不感知）；回滚失败无自愈路径（dist 损坏可能彻底起不来）
- autoBackup 只拷主 db 文件，不 checkpoint 不带 -wal/-shm：非正常关闭后的备份静默缺失最近写入；还原路由不检查活跃 run

### P2 — 体验/可观测性（择要）

- RuntimeStore 全局单例不按会话隔离，切换可串台
- messageQueue 纯内存，刷新丢排队消息
- SSE 无心跳、客户端读取无超时
- Sidebar 全文件 6 处空 catch 且 `.then()` 不查 response.ok（验证后由 P1 降级：不造成数据分歧，refreshSessions 会拉回真值）
- 连接指示灯一次性检查（验证后由 P1 降级：StatusBar 另有 rs.lastError 独立错误通道）
- 通知轮询静默吞错，降级不可观测

### 已推翻（REFUTED）

- "IM 渠道绕过 RunManager 与 UI 并发写同一 session"：证据属实（channels 确实不经 RunManager），但触发场景不存在——ChannelChatView 是只读组件，渠道 master session 的 projectPath 是哨兵值 `__channel__`，无法被常规 UI 选中，两个写入者当前不会并存。记为理论缺口。验证员附带发现 MessageMerger 去重 key 存在相邻风险，待后续核。

## 四、工程化建设方案（待审批）

原则：复用既有机制（finishPromise、safeWrite、RunManager 接口、howpot-tip 事件），不推倒重来。每项都有验证方式，按"写一个测一个"推进。

### 阶段 0 · 止血（直接消除两个已报 bug 的根因，改动小收益大）

| 项 | 内容 | 改动量 |
|---|---|---|
| S0-1 | 外链交系统浏览器：引入 plugin-opener，markdown 链接 onClick preventDefault + open()；Rust 端 on_navigation 白名单（仅放行本机源）做第二道闸 | 小 |
| S0-2 | 抢占前先落盘：start() 替换同会话旧 run 前 abort + await waitForFinish（复用 finishPromise，参考 cleanupRuntimeState 既有做法），补一条"抢占后旧轮已落库"的测试 | 小 |
| S0-3 | 增量持久化（SSOT 根基）：run 开始即写入用户消息（pending 态），assistant 内容按事件节流 upsert，run 收尾改为终态更新。persist-run-messages 测试同步扩展 | 中 |

### 阶段 1 · 恢复机制（让"断开"之后能"接回来"）

- S1-1 运行中会话重挂接与完成感知：切回/重载时若该 session 正在 running，短周期轮询消息表（S0-3 后天然可见增量）；globalRunningSessionId 由 running→idle 时自动重拉一次；run 完成事件接入既有 /api/notifications 通道（窗口非前台时发 Web Notification，可选 Tauri request_user_attention 闪动任务栏）
- S1-2 退出保障：/api/shutdown 检查 RunManager，abort + waitForFinish 后再退；壳层等待时间与之匹配
- S1-3 挂起解除：tool-confirm/ask_user 支持 abortSignal + 超时自动拒绝，Stop 与删除会话能解除一切等待；Stop 真停止（工具子进程随 abort 回收）

### 阶段 2 · 纵深防御与可观测

- S2-1 ErrorBoundary 分层：Thread 消息区独立边界，单条消息渲染容错；Retry 附带数据重拉；会话自动恢复加"连续崩溃则回退空会话"的熔断
- S2-2 流协议补全：error 事件 + 出错也发 [DONE] + 心跳；ChatAdapter 处理 error 事件并呈现
- S2-3 落库失败可见化：persistRunMessages 失败走 howpot-tip 告知用户；健康状态改为轮询驱动，server 崩溃可被 UI 感知

### 阶段 3 · 运维通道加固

- S3-1 热更新：加 active-run 门槛（复用 RunManager 接口）；更新成功后强制重启提示；回滚失败给出修复引导
- S3-2 备份：autoBackup 走 SQLite backup API 或 checkpoint 后拷贝；还原前检查活跃 run 并走 close/reopen 流程

### 建议的推进方式

阶段 0 三项互相独立，可并行为三个小 PR，每个都能独立验证（S0-1 有运行时证据要求：真机点链接）。阶段 1 依赖 S0-3。阶段 2/3 可按风险偏好排期。P2 项不专门立项，顺手修。

---

## 收尾状态（2026-07-09 更新）

四阶段方案已全量落地于 `fix/resilience-stage-0`（S0-S3 共 12 个功能 commit）。落地后对分支做了 7 维审查 + 对抗验证（34 条确认 / 4 条误报剔除），确认项分三批修复完毕；同批对 H-Relay 做了 4 路摸底并补强。

- 复审与修复记录（含验收清单、经验沉淀）：`docs/resilience-review-2026-07-09.md`
- H-Relay 摸底与补强（兼运维手册）：`../H-Relay/docs/resilience-hardening-2026-07-09.md`

主项目 verify 1622 全绿（基线 1585 → 1622），H-Relay 226/226。全部待用户验收。
