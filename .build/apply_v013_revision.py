"""One-time v0.13 source edit from the fixed v0.12 baseline."""
from pathlib import Path
import ast,json,re
B=Path('.build');base=B/'revision_0_13_baseline'
p=B/'build_selfcontained.py';s=(base/p).read_text()
old_order=ast.literal_eval(re.search(r'^order=(.+)$',s,re.M)[1])
removed={'claude_method','claude_results','rpent','rpent_results'}
order=[k for k in old_order if k not in removed];order.insert(order.index('robolab_results')+1,'report_heatmap')
old_minutes=ast.literal_eval(re.search(r'^minutes=(.+)$',s,re.M)[1]);times=dict(zip(old_order,old_minutes));times['report_heatmap']=1.5
minutes=[times[k] for k in order]
mapping={i+1:order.index(k)+1 for i,k in enumerate(old_order) if k in order}
(B/'v0_13_page_map.json').write_text(json.dumps({'old_to_new':mapping,'new_order':order,'minutes':minutes,'total_minutes':sum(minutes)},indent=2)+'\n')
for fn in ['claude_method','claude_results','rpent']:
 s=re.sub(r'^def '+fn+r'\(\):\n.*?(?=^def |^from )','',s,flags=re.M|re.S)
for key in ['claude_method','claude_results','rpent']:
 s=re.sub(r"^ '"+key+r"':\([^\n]+\n",'',s,flags=re.M)
s=s.replace("['S09','RPENT','WAM']","['ROBOCURVE','ASIM','ANON','WAM']").replace("['HIROBOT_DISCUSSION','S09','ASIM'","['HIROBOT_DISCUSSION','ASIM'")
new_functions='''from report_figures_v013 import load_report_figures
report_captures=load_report_figures(ROOT)
REPORT_URL='https://anonymous-report-421.github.io/public-website/?lang=en&view=1'

def report_dojo_results():
 els=page('RoboDojo: Overall Results',1)
 for name,x in [('panel-score-ranking.png',64),('panel-sr-ranking.png',656)]:
  els += [figure(report_captures[name],'Original report RoboDojo '+name,x,145,560,455,REPORT_URL)]
 els += [text('Hybrid 24/50  ·  Direct 13/50',64,608,1152,32,25,'#1d7d76',True),
         text('Public baselines are reweighted references, not paired reruns.',64,646,1152,27,18,'#646464')]
 return els

def report_lab_results():
 els=page('RoboLab: Overall Results',1)
 els += [figure(report_captures['robolab-success-ranking.png'],'Original report RoboLab success-rate result',84,145,1112,415,REPORT_URL),
         text('Direct 49/50  ·  Hybrid 46/50',84,582,1112,35,27,'#1d7d76',True),
         text('Selected final slots + retries / historical baselines; not fresh paired trials.',84,629,1112,29,19,'#646464')]
 return els

def report_task_heatmap():
 els=page('RoboDojo: Task-Level Patterns',1)
 els += [figure(report_captures['task-score-table-complete.png'],'Original report per-task Score heatmap; overflow expanded, data and colors unchanged',64,139,1152,512,REPORT_URL)]
 return els

'''
s=s.replace('summaries={',new_functions+'summaries={',1)
s=s.replace('summaries.update(result_slides)','''summaries.update(result_slides)
summaries.update({
 'robodojo_results':('RoboDojo: Overall Results',report_dojo_results(),['ANON']),
 'robolab_results':('RoboLab: Overall Results',report_lab_results(),['ANON']),
 'report_heatmap':('RoboDojo: Task-Level Patterns',report_task_heatmap(),['ANON']),
})''')
s=re.sub(r'^order=.+$',f'order={order!r}',s,flags=re.M).replace('assert len(order)==38','assert len(order)==35')
s=re.sub(r'^minutes=.+$',f'minutes={minutes!r}',s,flags=re.M).replace('assert len(minutes)==38 and sum(minutes)==60','assert len(minutes)==35 and sum(minutes)==55')
s=s.replace("n<=19 else '2", "n<=16 else '2").replace("n<=27 else '3", "n<=24 else '3").replace("n<=36 else 'Closing'", "n<=33 else 'Closing'")
s=s.replace(" 'robodojo_results':'Anonymous report · case counts recalculated from 100 public records; task subset and scored-episode denominator retained',"," 'robodojo_results':'Original report screenshots · 10 selected tasks · Direct Score n=48, Hybrid n=50; success denominator 50 each',")
s=s.replace(" 'robolab_results':'Anonymous report · selected final-slot outcomes + historical first-five baselines; descriptive, not matched fresh attempts',"," 'robolab_results':'Original report screenshot · selected final slots + historical first-five baselines; initial states/budgets not fully paired',\n 'report_heatmap':'Original report Score heatmap · all 10 tasks and 7 methods · public references are not matched reruns; click to enlarge',")
for key in ['robodojo_results','robolab_results']:
 s=re.sub(r"^ '"+key+r"':'Bold:[^\n]+\n",'',s,flags=re.M)
s=s.replace('Anonymous technical report · GPT 6 Astra as an Embodied Policy (accessed 14 Sep 2026)','Technical report · GPT 6 Astra as an Embodied Policy (result images captured 15 Sep 2026)')
p.write_text(s)
# Narration is keyed by the old slide IDs only for this controlled migration.
s=(base/B/'script_revised.md').read_text();parts=re.split(r'^## (\d{2})\. (.+)\n',s,flags=re.M)
sections={int(parts[i]):[parts[i+1],parts[i+2].strip()] for i in range(1,len(parts),3)}
sections[3][1]=sections[3][1].replace('旧接口实验与 Astra 的新表现','Astra 的实机、接口与 Direct/Hybrid 证据')
sections[5][1]=sections[5][1].replace('Claude 和 Astra 的实验','Astra 的实验')
sections[6][1]=sections[6][1].replace('后面的证据沿这条问题走。先看旧模型为什么依赖motor prior，再看RPent怎样组织执行能力，最后看Astra哪些表现支持职责上移、哪些结果又提醒我们不能把执行层削得过头。','下面直接看Astra。先看没有独立VLA的实机控制，再看同一模型的不同action interfaces，最后用Direct/Hybrid报告检验什么时候仍需要learned motor prior。关键不是提前选边，而是让任务和实验决定分工。')
sections[16]=['RoboDojo: Overall Results','''> 读图提示：两张都是报告原始结果图，左边Score，右边success rate；可以点击放大。两图沿用同一Score排序，不要按右图行次误读为success-rate排名。

先只看三条彩色柱。Hybrid是24/50，success rate 48%；Direct是13/50，也就是26%。对应的mean Score是62.60与37.81。橙色π0.5是公开参考，不是用我们的五组种子重新跑出来的baseline。

灰色柱同样来自公开RoboDojo统计，作者重算了这十个选定任务以及standard/randomized场景的权重，因此不能拿它当整个benchmark的最新排行榜，也不能声称这些模型与Astra做了同种子配对比较。

Direct有两个episode缺少可用native Score，所以37.81基于48个scored episodes，Hybrid基于50个；两组success rate的分母都保持50。Learned prior、action interface和执行段长一起变化，结果支持整体Hybrid配置的价值，不能把提升归因于单个组件。

下一页换到RoboLab，排序会反过来。我们要看任务与prior的适配，而不是从一个汇总图宣布一种架构普遍最好。''']
sections[17]=['RoboLab: Overall Results','''> 读图提示：这是报告原始整体结果图。先说明selected final slots的口径，再看Direct与Hybrid的位置；可点击放大。

Direct最终49/50，Hybrid46/50；π0.5与Cosmos3-Nano-Policy各18/50，DreamZero为17/50。报告认为，选定的semantic pick-and-place任务，以及student prior未针对这些任务适配，可能解释与RoboDojo不同的排序。这是解释假设，不是隔离因素后的因果结论。

特别要保留选择规则：Astra组使用retained final slots，包含历史结果和authorized retries，initial states没有严格配对。Direct最后两次BlocksInBin retry把decision budget从180提高到500。三个baseline来自June cohort，每任务按顺序取前五次，包括失败。

所以这些数字是已发布记录的描述性汇总，不是fresh、统一预算、每条件只跑一次的配对试验。相同task名称和slot数量也不能证明task version、control settings或起点一致。不要和RoboDojo合成一个总成功率。

随后回到RoboDojo的逐任务热力图，检查整体均值背后的任务差异。''']
sections[19][1]=sections[19][1].replace('类似地，Claude 的 Cursor tool 实验从6%到32%，支持 spatial aids 的价值，不意味着所有失败都只是定位问题。','Asim在同一个Astra上更换观测和action interface，也出现明显差异，但预算并不匹配，不能据此分离单一原因。')
heatmap='''> 读图提示：先看右侧Hybrid与Direct两列，再横向比较对应任务。颜色越深Score越高；这是partial-completion Score，不是success rate。可点击放大原图。

总体数会掩盖分工差异。Classify objects中Direct的Score是100，Hybrid是71；但Fold clothes中Hybrid是100，Direct是40，Build tower则是64与12。Hybrid不是逐任务都赢，Direct也不是所有操作都能替代动作先验。

把这张图连回开头的问题：更强System 2确实可以承担更多语义、空间和动作决策，但System 1需要多强、多通用，仍然取决于任务和prior是否适配。热力图提供任务层面的线索，不是“语义”和“物理”两种能力被严格分离的测量。

前五列是公开参考值，后两列是报告的实验。它们不是同种子重跑；Direct缺失Score的分母限制仍然适用。图中保留原报告全部十个任务、Overall和七种方法，没有重新挑选最有利的任务。

最后核对视频容易掩盖的另一个问题：这些系统具体输出什么，模型多久才返回一次？'''
header=parts[0].replace('0.12','0.13').replace('60 分钟','55 分钟')
header=header.replace('从 generalist VLA / WAM 承担泛化，到更强 Agent 配合较窄 action primitives。','从 generalist VLA / WAM 承担泛化，直接进入 Astra 的能力、接口与 Direct/Hybrid 证据。')
header=header.replace('RoboLab 加粗只表示 retained slots 的行最大值，','RoboDojo/RoboLab使用原报告结果图，RoboLab仍是retained slots口径，')
chunks=[header.rstrip()]
for i,k in enumerate(order,1):
 if k=='report_heatmap':title,body='RoboDojo: Task-Level Patterns',heatmap
 else:title,body=sections[old_order.index(k)+1]
 chunks.append(f'## {i:02}. {title}\n\n{body}')
(B/'script_revised.md').write_text('\n\n\n'.join(chunks)+'\n')
print('New slides',len(order),'minutes',sum(minutes),'mapping',mapping)
