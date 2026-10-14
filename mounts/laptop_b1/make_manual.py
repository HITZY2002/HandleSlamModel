from pathlib import Path
import json,re
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import HexColor
P=Path(__file__).resolve().parent;q=json.loads((P/'QA.json').read_text());p=q['params']
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'));c=Canvas(str(P/'B1_D435i双夹支架_详细设计与试装说明.pdf'),pagesize=(841.89,595.28));W,H=841.89,595.28
c.setTitle('B1 D435i双夹支架详细设计与试装说明');c.setAuthor('dot');pg=0
COL='#183e4a';GREY='#526b75';ORANGE='#ae541d'
def clean(s):return s.replace('Ø','直径').replace('mm²','平方毫米').replace('N·m','N m').replace('−','-').replace('–','-')
def txt(x,y,s,fs=11,col=COL):c.setFillColor(HexColor(col));c.setFont('STSong-Light',fs);c.drawString(x,y,clean(s))
def para(x,y,s,width=365,fs=11,lead=17):
 line=''
 for ch in re.findall(r'[A-Za-z0-9.,%×/+=<>\-]+|.',clean(s)):
  if pdfmetrics.stringWidth(line+ch,'STSong-Light',fs)>width:
   txt(x,y,line,fs);y-=lead;line=ch
  else:line+=ch
 if line:txt(x,y,line,fs);y-=lead
 return y

def page(title,sub=''):
 global pg
 if pg:c.showPage()
 pg+=1;txt(31,557,title,22)
 if sub:txt(32,531,sub,11,GREY)
 txt(32,20,'B1 | 2026-10-11 | 实测前工程样件，单位 mm',8.5,GREY);txt(775,20,f'{pg} / 8',8.5,GREY)
def pic(name,x,y,w,h=None):
 from PIL import Image
 f=P/name
 if h is None:
  a=Image.open(f);h=w*a.height/a.width
 c.drawImage(str(f),x,y,width=w,height=h,mask='auto')
def head(x,y,s):txt(x,y,s,14);return y-24
def link(x,y,label,url,fs=9):
 txt(x,y,label,fs,GREY);c.linkURL(url,(x,y-2,x+pdfmetrics.stringWidth(label,'STSong-Light',fs),y+fs+2),relative=0)
page('B1 双夹支架详细设计','面向 HUAWEI MateBook 13s 2023 EMF-16 与 D435i；先做夹口试片，再确定实配位置。')
pic('renders/02_working_position.png',28,167,440)
y=head(494,495,'本版结构')
for s in ['一体主体 + 两个活动压脚，共3个打印件。金属M5螺杆配捕获六角螺母，压脚隔开螺杆与电脑底壳。','5个粘贴圆座与相机承架同体。贴面中心跨度99×87×44mm，保持真实非共面；没有独立贴座装配螺丝。','相机在机身侧边外，光轴朝屏幕后方环境。屏幕朝操作者，双手始终托住电脑。']:
 y=para(494,y,s,316,11,17)-9
y=head(494,y-6,'关键设计数值')
for s in ['主件：153.5×173×134mm','夹距：72mm；示意夹点Y=88 / 160','名义夹厚范围：8–22mm','每块接触软垫：18×24×2mm','机身侧边外最大伸出：约133.5mm']:
 txt(495,y,s,11);y-=23
para(32,138,'这是已完成数字几何核验的原型设计，不是已确认合身的EMF-16成品。示意电脑底座厚12mm、宽297.2mm、深218.4mm、开屏110°均用于表达布局，不能代替你的实机测量。',776,11,18)
para(32,87,'只有夹厚可在装好后用螺杆调节。夹距、沿侧边位置、咬入深度与避让窗口都需要改参数并重新打印。禁止把支架当作提电脑手柄；装着夹具不要合盖。',776,11,18)
page('安装区域与为何前移夹点','灰色机身没有精确键帽、端口、风口和脚垫细节，图中空白不等于实机可夹。')
pic('renders/02b_laptop_side.png',30,198,380);pic('renders/02c_laptop_bottom.png',432,198,380)
txt(35,512,'右侧视图',14);txt(436,512,'底面视图',14)
y=head(33,178,'前移55mm的目的')
y=para(33,y,'两夹点由概念版Y=33/105前移到88/160，夹距仍72。整体深度由约119增至173mm，是沿电脑侧边向掌托方向延长，用来争取后侧接口空间；相机和点架高度没有因此增加。',369,11,17)
y=para(33,y-8,'下沉连接梁截面10×12mm，内侧在X=+4mm，位于电脑外缘外，不是覆盖整个底面的托板。下垫接触侧边1至19mm，两块共864mm²。',369,11,17)
y=head(435,178,'这些部位必须检查')
para(435,y,'上垫必须全部压在平直硬边上，绝不能压键帽、触控板或薄弱装饰边。下垫必须避开进风格栅、脚垫和斜面。立柱约在Y=55至73，夹区为75至101、147至173；这些位置仍可能与真实接口冲突。',375,11,17)
para(435,76,'若实际安全接触区不同，优先改夹点位置与深度；不要用更大夹力或厚软泡棉硬凑。',375,11,17)
page('夹口剖面与机械调节范围','A-A：切过单个M5螺杆轴线；下图由真实CAD零件剖切，螺纹以光杆包络表示。')
pic('renders/05_section_AA.png',20,98,385)
y=head(448,500,'夹口尺寸')
for s in ['上臂厚6；下臂厚8；侧壁厚10。','夹宽26；向机身内咬入20；软垫18×24×2。','压脚18×24×5，底部Ø5.8盲孔深2。','M5通孔Ø5.6，不打印承力内螺纹。','螺母窝对边8.5、深4.3；下方承压底厚3.7。']:
 y=para(448,y,s,361,11,17)-6
y=head(448,y-5,'金属螺杆与螺母')
y=para(448,y,'M5×0.8手拧螺杆，手柄下有效长度30mm，参考手柄直径20mm。螺母用DIN934 M5，对边8mm、厚4mm，从上方放入窝。不要换入4.7mm厚等不同规格而不改槽。',361,11,17)
y=para(448,y-8,'螺杆反力把螺母压向下方承压底面；不能把螺母窝反向做成朝下敞口。压脚盲孔底仍有3mm塑料，螺杆端不能碰电脑。压脚是独立件，松夹时扶住防止掉落。',361,11,17)
y=head(33,115,'8–22mm范围的几何检查')
para(33,y,'按上下各2mm未压缩软垫和M5×30计算：T=8时压脚离下臂15mm、手柄余隙5mm；T=22时压脚离下臂1mm、螺杆越过螺母顶部3.2mm。此范围没有包含软垫压缩、机壳斜面和打印误差，须用试片确认。',778,10.5,16)
page('相机螺钉路径与下沉梁截面','B-B：后M3孔轴线；C-C：两夹点之间。相机仅为外形包络，不代表真实孔底或内部结构。')
pic('renders/06_section_BB.png',75,263,285);pic('renders/07_section_CC.png',480,272,285)
txt(35,512,'B-B  D435i后安装孔',14);txt(438,512,'C-C  下沉梁',14)
y=head(32,242,'M3旋入量必须实测')
y=para(32,y,'后双M3孔距45mm。接触凸台1mm + 主板6mm = 名义7mm路径；M3×10加每孔总厚约1mm硬垫片，名义突出10−7−1=2mm。建议每孔用两片名义0.5mm的M3平垫，实际叠厚要测。',373,11,17)
y=para(32,y-6,'安装前用卡尺量螺钉超出相机接触凸台的长度，目标1.8至2.2mm且严格小于3mm。过长应换螺钉或调整硬垫片，不能靠拧到底判断。0.4N·m是相机资料值，不能当PLA电脑夹的拧紧扭矩。',373,11,17)
link(32,52,'安装数据依据：RealSense数据表 p67 与 p139 [1]', 'https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf',9)
y=head(434,242,'连接梁与USB')
y=para(434,y,'梁截面10×12mm，Z=-38至-26，内侧X=+4。示意T=12mm时，机身底面到梁顶有14mm竖向高度差；这不代表任何实际插头已能通过，柱和夹区仍需逐个避让。',375,11,17)
y=para(434,y-6,'相机顶部按16×20×35mm插头包络检查，无主件体积干涉；尚未包含真实插头外形和线缆弯曲。先留自然松弛弯，沿支臂外侧走线，再在立柱两孔附近做应力释放。扎带不得勒接口或跨过风口、屏幕和键盘。',375,11,17)
para(434,81,'相机外壳近侧边距电脑边缘约24.9mm，镜头前平面前伸25.15mm。实际开盖角与每路相机视野仍需检查，不能只检查外壳不碰撞。',375,10.5,16)
page('爆炸图与采购清单','蓝绿色为打印件，金色为金属紧固件，黑色为软垫；参考相机/球体不打印。')
pic('renders/04_exploded.png',13,93,480)
y=head(500,505,'安装所需')
rows=[('打印主体','1件，01_B_main'),('打印压脚','2件，02_pressure_shoe'),('M5手拧螺杆','2颗，M5×0.8，有效长30'),('M5六角螺母','2个，DIN934，AF8×厚4'),('M3圆柱头螺钉','2颗，M3×10，头Ø5.5×高3'),('M3平垫片','4片起，每孔总厚约1mm'),('接触软垫','4片，18×24×2，薄硅胶/EVA'),('球形反光marker','5个，底座≤25mm，实际核对'),('USB数据线','1条，接头与弯线需量'),('小扎带或软线扣','2条，立柱孔Ø4.2')]
for a,b in rows:txt(500,y,a,10.5);txt(596,y,b,10.5);y-=24
para(500,y-3,'M3垫片参考内径3.2、外径7、厚0.5。螺钉长度、头径、实际垫厚及螺母尺寸到货后核对；不要未经测量换大法兰头或更厚螺母。',305,10.5,16)
para(32,71,'安全绳仅在电脑有可靠、不会妨碍键盘/风口的挂点时选配；没有明确挂点，不应绑屏幕或随意绕线。支架仍只能承载相机。',773,10.5,16)
link(500,97,'DIN934 M5尺寸 [2]', 'https://www.accu.co.uk/hexagon-nuts/766474-NUT203M5-B',8.5)
link(634,97,'M3平垫尺寸 [3]', 'https://www.westfieldfasteners.co.uk/BZP-Washer-M3.html',8.5)
page('五点非共面布局与标定','圆座直径25mm，厚3mm，均朝+Z；粘贴面保持平整，无安装孔或刻字占用。')
pic('marker_orthographic.png',25,260,792)
y=head(35,235,'设计坐标  X / Y / Z')
for i,(x,yy,z) in enumerate(p['markers']):txt(40,y,f"{'ABCDE'[i]}          {x:>3}          {yy:>3}          {z:>3}",12);y-=27
para(35,72,'原点在示意机身右边缘、后缘与键盘甲板的交点。X向外、Y朝操作者、Z向上；相机朝-Y。',354,10.5,16)
y=head(438,235,'数字核验与实际球心')
for s in ['XYZ跨度99×87×44；最小点距63.36mm。','中心化秩3，奇异值95.281 / 82.231 / 34.521mm，最小/最大0.362。五种四点组合体积均为正。','示意球直径14mm、球心高出贴面9mm。真实球径、底座高度、胶层与偏心都会改变球心。','这是设计坐标，不是RealSense SDK光学坐标。用实际球心建立动捕刚体，标定相机外参；拆装和重新粘点后复核。']:
 y=para(438,y,s,367,11,17)-6
page('打印起点与逐步装配','STL单位mm，已落在Z=0；主体1件、压脚2件。另附小试片，可在打印整件前验证。')
steps=[('1 先做试片','assembly_step_1'),('2 装螺母与压脚','assembly_step_2'),('3 装相机','assembly_step_3'),('4 粘点与标定','assembly_step_4')]
for i,(t,n) in enumerate(steps):
 x=26+i*204;txt(x,506,t,13);pic('renders/'+n+'.png',x,304,192)
y=head(32,272,'PLA切片起点')
for s in ['0.4mm喷嘴、0.2mm层高，5至6道墙，上下至少6层，40%至50%填充；夹口、螺母窝和立柱节点局部加密。以上只是试制起点，不是强度认证。','主体按STL姿态下臂朝床。空间支臂和上夹臂下方需要支撑；把螺母窝/螺杆孔设为支撑屏蔽，检查支撑能从夹口侧面拆出。压脚盲孔朝下，小孔顶可桥接试打。','主件153.5×173×134。180mm平台添加3mm外沿后名义占179mm深，仍须看有效边界；5mm外沿会超180mm。具体打印机未知，禁止整体缩放配尺寸。']:
 y=para(32,y,s,376,10.5,16)-6
y=head(437,272,'安装顺序')
for s in ['试片+1压脚先检查接触面，确认软垫全部落在硬边，螺母能自然放入、螺杆能顺畅通过。发现键帽受压、底壳局部变形或脚垫干涉就停，改参数。','去支撑和毛刺；M5螺母从上放入窝，螺杆从下穿入；上下软垫各贴一片，压脚盲孔对准螺杆。装机后交替轻紧，不用工具加力。','M3先穿过打印件和硬垫片，测实际突出量，再装相机。粘好marker按胶的规定固化；线缆留松弛并固定。双手托电脑，低幅度测试无滑动后检查画面与动捕。']:
 y=para(437,y,s,372,10.5,16)-6
page('验收边界与最少实测清单','网格可切片不代表夹口已合身；有限几何/受力算例不等于实物承载、振动或热可靠性。')
y=head(32,504,'已经完成的数字检查')
for s in ['主体、压脚和试片都是有效单一CAD实体。三个最终STL重新读取后，封闭流形、边方向一致、无退化三角形、正体积。主体导出时去除了7个零面积细分碎片。','主件与相机包络、假设USB包络、示意电脑、M3/M5光杆、螺母和压脚均无体积干涉。夹厚8/22mm两个端点通过名义几何检查。','D435i官方重量75g±10%，还要计支架、球点、线缆与运动扰动。72mm夹距可形成前后力偶。例如假设0.15N·m俯仰力矩，M/d=2.08N；这只是附加反力算例，绝不是允许夹力或额定承载。它也不能替代对侧向悬臂滚转、摩擦、预紧力、层间强度和动态载荷的验证。']:
 y=para(32,y,s,376,11,17)-8
y=head(32,y-3,'使用中必须停下的情况')
para(32,y,'任何滑移、裂纹、层间发白、电脑壳体变形、明显发热软化、线缆拉扯或标记点晃动，都应立即拆下检查。PLA避高温与暴晒。不能带着夹具合盖；安装后不能直接把电脑平放压在支架/螺杆上；放桌面前应先拆下。',376,11,17)
y=head(438,504,'请量这5项后再冻结实配')
for s in ['1. 左右侧面和底部照片，包含接口、风口、脚垫、键帽；序列号可遮。','2. 两个候选夹点的底座厚度：边缘、向内10mm和20mm分别量，只算底座，不含屏幕。','3. 可承压平直硬边的宽度/长度，以及距后缘的位置；确认上垫18×24mm完全避开按键。','4. 常用及最大开屏角，USB两端插头尺寸/弯线空间，marker底座直径与球心高度。','5. Creality打印机完整型号、有效平台尺寸与喷嘴直径。']:
 y=para(438,y,s,370,11,17)-7
y=head(438,y-4,'仍未验证')
para(438,y,'真实配合、表面压强容限、振动/疲劳/跌落、热蠕变、实际画面全视野和动捕遮挡/精度。至少按你的动捕系统要求验证各采集姿态可见点数；非共面不是360°可见保证。',370,11,17)
link(32,65,'[1] RealSense D400 Series Datasheet, Mar 2026，D435i表3-52 / 图10-9', 'https://www.realsenseai.com/wp-content/uploads/2026/03/RealSense-D400-Series-Datasheet-Mar-2026.pdf',8.5)
link(32,48,'[2] Accu：DIN934 M5 对边8、厚4、螺距0.8', 'https://www.accu.co.uk/hexagon-nuts/766474-NUT203M5-B',8.5)
link(438,48,'[3] Westfield：M3 DIN125 平垫3.2×7×0.5', 'https://www.westfieldfasteners.co.uk/BZP-Washer-M3.html',8.5)
c.save();print('Created 8-page manual')
