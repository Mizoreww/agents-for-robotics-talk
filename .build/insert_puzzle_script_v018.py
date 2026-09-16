from pathlib import Path
import re
p=Path('.build/script_revised.md');s=p.read_text().replace('建议 57 分钟','建议 59 分钟')
assert '## 09. One Model' in s
s=re.sub(r'^## (\d{2})\.',lambda m:f'## {int(m[1])+1:02}.' if int(m[1])>=9 else m[0],s,flags=re.M)
insert='''## 09. Robot Puzzle Demos in Simulation

> 播放提示：左边是作者发布的完整 Rubik’s Cube 视频，未额外加速；右边是作者网站导出视频中的完整 Claw 段。两边分别播放，先看动作，再区分验证条件。

前一页是真机 demo，这一页补两个更复杂的 simulation puzzle。左边 Yanjie Ze 展示 Astra 用 robot hands 操作 Rubik’s Cube。Awesome-Astra 将它描述为 zero-shot manipulation，但本次可核验的原帖只明确写了解魔方，没有公开完整 trial denominator 和 action API。这里不把 zero-shot 当成经过独立验证的评测结论，也不猜测它是直接 joint q、IK goal 或 atomic skill。

右边 Unlocking the Claw 展示双臂如何绕开相互锁住的几何约束，把两部分分离、放到支架、松手和撤离。它从已有 object-space reference path 出发，实现局部路径修正、grasp 选择、full-robot IK 和 motion planning。起始时物体已经抓住，使用 ideal rigid grasps，记录的是 kinematic joint motion。

所以这两个例子展示了很强的空间任务表现，但不是相同证据。尤其 Claw 验证的是特定路径的几何可行性，不是接触动力学、frictional force closure，也不是能从任意新初态在线解题的 policy。下面继续看同一个基础模型使用不同 action interface，表现会怎样改变。

'''
s=s.replace('## 10. One Model',insert+'## 10. One Model');p.write_text(s)
