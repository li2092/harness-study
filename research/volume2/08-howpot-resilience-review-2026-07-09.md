> 快照自 /Users/jimi/ClaudeCode/Howpot/howpot-chat/docs/resilience-review-2026-07-09.md · 2026-07-17 拷贝，供第二卷 §一 引用；原文件为准。

# 韧性建设复审与修复记录（2026-07-09）

本文记录 `docs/resilience-audit-2026-07-09.md` 四阶段方案落地后的复审结果与后续修复。审计报告回答"要建什么"，本文回答"建得对不对、又修了什么"。全部工作在分支 `fix/resilience-stage-0`。

## 一、复审方法

四阶段落地（12 个功能 commit，S0-S3）后，对分支 diff（+1665 行，35 个文件）做了 7 维并行审查：并发竞态、持久化正确性、UI 生命周期、错误路径、Tauri 壳导航安全、测试质量、范围与简洁性。每条 finding 由独立验证 agent 以"默认是误报"的立场对抗核实——读完整代码上下文、必要时写探针测试复现，才允许进入确认清单。同批对 H-Relay 做了 4 路摸底（另见 `H-Relay/docs/resilience-hardening-2026-07-09.md`）。

结果：34 条确认，4 条误报剔除。确认项分三批修复，每批 verify 全绿后提交。

## 二、确认问题与修复映射

### 第一批（ba6749d3）——低成本高收益

| 问题 | 失败场景 | 修法 |
|---|---|---|
| threadKey 挂在包裹整个 shell 的 SessionRuntimeProvider 上（本分支 S1-1 引入的回归） | 后台任务完成触发自动刷新时，Sidebar 正在编辑的重命名、未保存的 agent.md 内容被连带卸载丢弃 | keyed provider 收窄到只包 Thread（已确认 Thread 是唯一 assistant-ui context 消费者） |
| restore 后 reopen 失败使 SessionStore 单例僵尸化 | 还原了损坏备份 → catch 只返回 500，模块级 store 仍指向已关闭实例，`if (!store)` 守卫永不重建 → 全部路由连锁 500 直到重启 | 自动回滚到 pre-restore 快照并重开；连回滚都失败才提示重启并 `resetSessionStore()` 置空单例 |
| audit.db 还原无 close→restore→reopen 保护 | 活跃 WAL 连接下直接覆盖文件 + 抽掉边车 → 下次审计写入抛异常且未包 try/catch | 与 sessions.db 对称处理；`_resetAuditStore` 改 try/finally 保证半死连接不残留 |
| 指示灯不查 `response.ok` | auth token 轮换后每次轮询稳定收 401，指示灯却常绿 | 非 2xx 计入失败计数 |
| readWithTimeout 超时不释放连接 | 半死连接累积占满浏览器每 origin 6 个连接槽 → 应用整体失联 | 超时路径 `reader.cancel()` |

**修复过程中挖出的新地雷**：回滚调用 restoreBackup 时默认会先给当前（已损坏的）库拍 pre-restore 快照；时间戳精确到毫秒，同毫秒内文件名相同——好快照先被坏内容覆盖、再被拷回去。测试跑得快正好复现。回滚路径改为 `snapshot: false`。

### 第二批（46280702）——并发与覆盖面

| 问题 | 失败场景 | 修法 |
|---|---|---|
| tryStart 同会话并发抢占 TOCTOU | 双标签页同会话 / 快速双击发送：两个并发抢占都通过同会话 recheck，后到者静默 abort 先到者刚建的新 run，整轮跳过持久化，占位行永久卡"生成中" | tryStart 按 sessionId 串行化（promise 链互斥）；新增并发测试锁行为 |
| 10s 抢占等待兜底放行后占位行卡死 | 旧 run 卡超 10s（如 block 类工具中）→ 放行后旧 run 落库被 isCurrentRun 拦截，占位行到重启才被扫掉 | 新 run preinsert 前按会话收敛遗留 running 行（reconcileOrphanRunningMessages 加 sessionId 参数）；flush 定时器加 isCurrentRun 所有权检查防复活 |
| 外链拦截只覆盖 Thread 一处 | FilePreview / AskUserCard / BtwTabContent 里点链接仍原地跳转丢 SPA | 拦截抽 `src/ui/lib/markdown-link.tsx`，四处渲染面统一挂载 |
| Rust opener 兜底绕过 scope 校验 | agent 输出里注入 `file://` 或自定义协议链接，点击即触发本地协议处理器 | on_navigation 兜底只放行 http/https/mailto |
| kill_node 同步阻塞主线程最长 ~15s | 窗口"未响应"诱发强杀 / OS 关机宽限（~5s）内必被强制终止，恰好截断落盘 | 托盘退出：先藏窗口，后台线程优雅关闭；Destroyed 路径缩短到 OS 宽限内（`kill_node(wait_polls)` 参数化） |
| BTW 侧问两处断线（用户报告） | ①按钮路径监听 `btw-response` 但 server 发 `btw-delta`，答案从不渲染；②无历史请求兜底读 modelView（仅 run 收尾写入），运行中侧问拿到旧视图 | ①事件名对齐；②兜底改读持久化消息表——S0-3 之后它是含运行中快照的实时 SSOT。e2e 实测通过 |

### P2/P3 收尾（619eeb5f）

- **崩溃熔断限定启动时**：会话恢复 effect 每次项目切换都重跑，60s 内两次无关 UI 崩溃后的正常切换会被误判为崩溃循环、静默丢弃已有会话。改为仅 boot 恢复时判定（`bootRestoreRef`）。
- **checkpoint 可观测**：备份/close 路径改 TRUNCATE（PASSIVE 遇争用直接放弃，拷贝静默缺 WAL 数据）；30s 周期保持 PASSIVE；auto-backup 的 checkpoint 失败落 console.warn。
- **补测试**：shell_exec abort 杀进程树 ×2；抢占端到端集成测试（真实 RunManager + 真实 SQLite 贯穿验证"旧轮先终态化，新 run 才拿到手"）。

### 有意不修

- **pushNotification 四处结构重复**（P3）：纯风格，无失败场景，重构稳定代码无收益。
- **maxSteps commit "夹带"**：审查者标记 c5248614 与审计条目对应不上——实为用户中途插的需求，非问题；将来 cherry-pick 时留意即可。

### 误报剔除（防止重复报告）

- "data: scheme 链接可替换整窗 HTML"——被 react-markdown ≥10 的默认 URL 消毒器在 DOM 之前截断。
- "clearSessionConfirmations 是 S1-3 唯一解挂机制"——实际解挂在 tool-executor 侧，该调用只是补充清理。

## 三、验收清单（用户实测用）

1. 长任务运行中切走再切回：看增量内容；停留看自动刷新——刷新发生时侧边栏若正在重命名，输入不应丢失
2. 后台跑任务最小化窗口，等完成通知
3. 跑 `sleep 60` 点 Stop，确认进程真死
4. 打包后真机点对话里的链接（跳系统浏览器）；ask_user 卡片、文件预览里的链接同样验证
5. 任务运行中退出应用，重启看 [已中断] 记录
6. 杀 server 进程，指示灯两个轮询周期内变红
7. 还原备份：任务运行中应被 409 拒绝；正常还原后不用重启直接可用
8. BTW 按钮：任务运行中侧问当前对话内容，tab 流式出答案且认识上下文；tab 内追问连贯
9. 托盘退出：任务运行中点"退出"，窗口立即消失不白屏
10. （回归）正常的项目切换、双标签页同会话操作不丢消息

## 四、经验沉淀（教程原料候补）

1. **"半途设计"是头号反模式的实证**：本轮修的大部分问题（SSE 断开不杀 run 但没做接回、审计表建好没接线、告警格式化了没发送、降级档位文档化了没实现）同构——机制只接一半的线，比没有机制更危险，因为它制造"已保障"的假象。
2. **修复自身也要过对抗验证**：threadKey 回归是韧性建设自己引入的；毫秒时间戳碰撞藏在"安全快照"逻辑里。改动越接近保障机制，越需要独立复审。
3. **串行化改变时序契约**：tryStart 串行化后 abort 晚一个微任务发生，两个既有测试的隐式时序假设立即失效。给并发原语做互斥时，同步语义变异步语义的涟漪要 grep 全部调用方和测试。
4. **计费/观测代码的作用域陷阱**：把记账变量声明在 try 块内，等于宣布"失败路径不记账"。凡 catch 需要读的状态必须提升到 try 之外。
5. **token 轮换的隐性联动**：本机起 dev server 触发 auth.token 重生成，用户正开着的实例（内存旧 token）与文件失同步——外部新客户端全部 401。这正是指示灯 finding 的真实复现，也是测试环境污染生产态的例证。

## 五、三项抽查追加（同日，commit 4f6b488f）

用户点名抽查三条线，结果与修复：

**1. BTW 链路**——复核通过，无改动。五环闭合：按钮 → openBtw（面板展开）→ 独立 fetch（不打断主对话）→ btw-delta 流式 → markdown 渲染（带外链拦截）→ tab 追问同链路。

**2. 消息数 500 墙**——查实三个 bug 叠加，全部修复：
- 分类器不认 relay 的 `Too many messages (max 500)`，归为不可重试 unknown 且丢弃 response body，用户只看到 `HTTP 400`。修：分类正则补 too many messages → context-too-long 可重试；unknown 兜底保留 body；isContextOverflow 补读 `.classified`。
- 压缩只在回合开始检查（token 85% 或条数 400），单个长 agentic 回合（几百次短工具往返）在轮内冲破 500 无人拦截——工具输出短时条数几乎总是先于 token 撞墙。修：agent 步循环加回合内条数闸。
- L2/L3 都按"回合"折叠，单个巨型回合原样穿过两级压缩。修：compress() 末尾 capMessageCount 回合内截断兜底（保任务头 + 截断标记 + 最近 300 条，工具配对交 ensureToolAlignment）。

**3. Stop 三层语义**——前两层通过，第三层缺失已补：
- 中止链完整：Stop/Esc 双路触发（客户端 cancelRun + 服务端 /chat/abort），signal 一路传到原生 fetch，llmFetch 不吞 AbortError（历史修复保持）。
- 部分内容保留完整：UI 不清已生成内容；落库带 `*[已停止]*` 标记；刷新重进可见。
- 停止提醒缺失：`*[已停止]*` 只在 UI 展示层，持久化给下一轮 LLM 的 modelView 是无标注的截断文本。修：abort 持久化路径对 stopped 停因做 annotateUserStop——浅拷贝后给最后一条 assistant 消息尾附系统备注（getModelView 返回活引用，必须先拷贝再改，否则污染内存态）。

verify 1630 全绿（+8 测试）。
