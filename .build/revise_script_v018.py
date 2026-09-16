from pathlib import Path
import re
p=Path('.build/script_revised.md');s=p.read_text();parts=re.split(r'^## (\d{2})\. (.+)\n',s,flags=re.M)
old={int(parts[i]):(parts[i+1],parts[i+2].strip()) for i in range(1,len(parts),3)}
new={i:old[i] for i in range(1,22)}
new[22]=('Agent Improves Policy', '''> 读图提示：沿 Task + API、Agent、真实 rollout、Verifier + logs 走一圈。先问改进留下了什么。

第三章的问题是：一次实验的反馈，怎样成为下次仍能使用的能力？Control 关心这一步怎么动，这里关心下一版 policy 怎样变好。Agent 可以修改 policy code、training recipe，或训练 neural policy，让后续 trial 使用新的版本。

ENPIRE 的切入点是，软件实验可以自动重跑，机器人实验却常常需要人收拾现场、判断成功、调代码。只要这些环节还依赖人工，autonomous research 就无法真正持续。

因此它先建立可重复、可验证的环境，再让 Agent 提出假设、组织实验和保留有效修改。章末我们再把这件事接到 RSI，也就是本 talk 所说的 Recursive Self-Improvement：能否连“如何改进”的经验也留下来，让以后做研究更有效？''')
new[23]=old[23]
new[24]=('ENPIRE: Reset and Verification', '''> 播放提示：左边为完整 pin reset，压缩到 8×；右边为完整 zip-tie detector 视频，1×。两段来自不同任务，不是同一 rollout 的同步画面。

Automatic reset 解决下一次试验从哪里开始。Agent 组合 SAM3 的物体检测、pose tracking、cuRobo motion planning 和 gripper torque 检查，把现场恢复到指定起点。部分任务直接从最难的 subphase 开始，不能解释成从任意初态解决完整任务。

Verification 解决结果到底有没有变好。右边展示 top/right 两个视角的检测框；完整判定还包括 segmentation 和几何测试，避免一个视角看起来穿过、实际上没有穿过的 false positive。Pin insertion 则结合视觉对齐、插入深度与力矩信号。

环境构造仍需要 human feedback，也需要成功和失败样例。之后进入 policy improvement，reset、verifier、安全约束和评测规则固定，不能为了得高分而修改成功定义。有了稳定的实验接口，才谈得上自动改进。''')
new[25]=('ENPIRE: Two Ways to Improve Policy', '''> 读图提示：两张官网原图分别对应 Push-T 和 Pin insertion。对比下方 f(o) 与 πθ(a | o)，不要把 coding Agent 和部署 policy 混成同一个模型。

ENPIRE 没有规定必须使用某一个 RL 算法。左边 Push-T 的改进对象可以直接是 heuristic code：根据 observation 算接触位置、推的方向和反馈修正，写成可执行函数 f。

右边 Pin insertion 则会训练 neural policy。Agent 可以选择 BC、iterative BC / data aggregation、offline RL、online RL，或带 BC regularization 的组合。它修改学习目标、数据混合和训练程序，再用实机结果判断这一版值不值得保留。

训练栈把 robot deployment、learner 和 actor 分开。Rollout buffer 保存 observation、action 来源和视频；online transitions 与 demonstrations 分开进入 buffer，再按训练配方混合。这里更新的 θ 是机器人 policy 的参数，不是 coding foundation model 的权重。

原论文的 robot policy 以 30 Hz 运行，底层 joint controller 为 100 Hz；这也不是 coding Agent 的推理频率。Agent 在更慢的研究循环中组织改进，训练出的 policy 在执行循环中产生动作。下面看它实际提出过什么修改。''')
new[26]=old[25]
new[26]=(new[26][0],new[26][1].replace('接下来用正式 learning curve 和 scaling 实验看总体表现。','接下来用正式的模型对照和 fleet scaling 看总体表现。'))
new[27]=old[27]
new[27]=(new[27][0],new[27][1].replace('下一页换到RoboCasa，观察autoresearch如何改善工具和VLA的组合，注意评测协议也会改变。','下一页先看扩大并行实验，能否更早找到高性能策略。'))
new[28]=('ENPIRE: Parallel Physical Research', '''> 播放提示：左边是完整的官方 pin fleet 视频，8×。右边原曲线保留 axes 和 legend，可以点击放大。

每个 station 有自己的 robot、compute 和 coding Agent。不同 Agent 异步探索训练思路，通过 Git 分支共享代码、读取其他分支的结果，把有用的修改继续试下去。这不仅是把一个固定策略复制到八台机器上评估，而是并行寻找更好的策略。

Pin insertion 从一个 agent–robot pair 扩到八个，达到接近完美表现的 research time，从超过一个半小时缩短到大约四十分钟。横轴是研究时间，不是 action inference latency。

这里的物理 rollout 允许最多八次 conditional retries，后一次尝试能利用前面失败的信息。因此不是 one-shot precision，也不是相互独立的 best-of-eight，不能由此反推 pass@1。Fleet 视频展示并行执行的形态，不给视频里的动作自行统计新成功率。

这组证据支持更多资源缩短 time-to-target，但更快不等于更省。后面会回到成本，现在先看同一套 autoresearch 思路在 RoboCasa 中怎样使用。''')
new[29]=old[28]
new[30]=('ENPIRE: Learned Manipulation Demos', '''> 播放提示：依次看 Pin insertion、Tie zip-tie、Cut zip-tie，均为官网下载原文件完整内容，统一转为 8×。可单独全屏观察接触与恢复，不必三段同时解说。

这页只看 ENPIRE 自己的任务 demo，不再放 CAD + RL 开发预览或另一个 physical ICL 项目。关注点不只是最后有没有做成，也包括接触失败后如何继续尝试、调整，再走向完成。

官网把这些任务的结果描述为高 pass@8，其中 retry 不是八个互相独立的随机样本，而是同一长程 rollout 内利用失败信息恢复。这里没有把片段裁到只剩成功动作，也不从几个展示视频额外推算成功率。

这些是作者展示的已得到的行为。它们不能单独证明训练算法更强，也不自动证明跨物体、跨任务的泛化。更接近自进化的问题是：在一个任务里学会如何做实验，能不能帮助下一个任务？''')
new[31]=('ENPIRE: Experience Across Tasks', '''> 读图提示：沿 Pin autoresearch、Written recipes、GPU autoresearch 看传递的是什么。下方 GPU insertion 为官网完整原片转 8×，它展示目标任务，不是迁移消融视频。

ENPIRE §3.4 给了一个很有意思的桥梁。完成 Pin insertion 的 autoresearch 后，Agent 被要求总结和反思有效的 training recipes，再把这份经验加入 GPU insertion 新任务的 instructions。作者报告这些经验可以转移到相似的新 dexterous task。

Appendix B.1 进一步说明，传过去的是明确的 Markdown summary，旧任务的 raw trajectories、hidden logs 和 checkpoints 都没有直接带过去。所以这不是把旧 policy 换个名字部署，也不是 foundation model 的 weights 更新，而是把研究经验放进下次能够读到的外部记忆。

这已经比“只让下一版 policy 更好”更接近 self-improving Agent：过去的实验能影响以后怎样提出和选择方法。不过，当前证据还不能说明改进者的能力会不断增强，更没有证明递归加速。要支持更强的 RSI 结论，还需要 held-out tasks 上有无记忆的比较、相同预算以及重复验证。''')
new[32]=('ENPIRE: Cost of Physical Research',old[30][1].split('本章可以收束为：')[0].strip()+'\n\n因此，把经验保存下来并减少重复探索，可能不仅是能力问题，也是成本问题。最后用一张框图把 ENPIRE 已经做到的部分和 RSI 的下一步分开。')
new[33]=('Toward Recursive Self-Improvement', '''> 读图提示：先看上面已运行的 policy improvement 循环，再看下方从 retained recipes / memory 指向 Better future research 的问号。问号不能省掉。

本章已经看到，Agent 能把实机反馈转成下一版 policy 或训练程序，在固定接口内持续搜索。ENPIRE 还把一个任务的经验整理成 recipes，影响下一项研究。两部分合在一起，确实开始接近 self-improving Agent 的方向。

这里把 RSI 展开为 Recursive Self-Improvement，强调的不只是产物变好，而是改进后的系统是否更擅长做下一轮改进。改进对象不一定是 LLM weights，也可能是 memory、tools、workflow 或研究代码。不能因为基础模型 frozen 就排除所有 RSI，也不能因为有循环就宣布 RSI 已成立。

最近的 RoboRSI 报告也讨论把交互沉淀成可复用 skill 和 policy；更早的 Darwin Gödel Machine 则在 coding 任务中修改 Agent 自身代码。它们帮助说明这个概念，但这里不展开另一套结果，更不把 coding benchmark 当成机器人实证。

我想留下的 open question 是：积累的经验，能否在 held-out tasks 和相同研究预算下，让 Agent 更快找到更好的策略，同时不损害旧能力？ENPIRE 提供了可运行的物理反馈循环，也给出经验复用的起点；开放世界、持续可验证的 recursive improvement 仍需要下一步实验。''')
new[34]=old[31];new[35]=old[32]
head=parts[0].replace('0.17（','0.18（').replace('建议 51 分钟','建议 57 分钟')
p.write_text(head.rstrip()+'\n\n'+''.join(f'## {i:02}. {new[i][0]}\n\n{new[i][1]}\n\n' for i in range(1,36)))
