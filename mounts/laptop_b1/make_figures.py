from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;q=json.loads((P/'QA.json').read_text());pr=json.loads((P/'projection_points.json').read_text());F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=lambda n:ImageFont.truetype(F,n)
COL='#173d49';GREY='#506d78';ORANGE='#bb5a14'
def paste(im,name,xy,size):
 a=Image.open(P/'renders'/f'{name}.png').convert('RGB');a=a.resize(size);im.paste(a,xy);return lambda key:(xy[0]+pr[name]['points'][key][0]*size[0]/pr[name]['size'][0],xy[1]+pr[name]['points'][key][1]*size[1]/pr[name]['size'][1])
def label(d,xy,text,sz=29,col=COL):
 x,y=xy;bb=d.textbbox((x,y),text,font=f(sz));d.rounded_rectangle((bb[0]-7,bb[1]-5,bb[2]+7,bb[3]+5),radius=5,fill='white');d.text((x,y),text,font=f(sz),fill=col)
def arrow(d,a,b,col=ORANGE,width=4):
 d.line([a,b],fill=col,width=width);v=np.array(a)-np.array(b);v=v/max(np.linalg.norm(v),1);n=np.array([-v[1],v[0]]);bs=np.array(b);d.polygon([tuple(bs),tuple(bs+v*14+n*6),tuple(bs+v*14-n*6)],fill=col)
def dim(d,a,b,text,shift=(0,0),sz=29):
 a=np.array(a);b=np.array(b);aa=a+shift;bb=b+shift;d.line([tuple(a),tuple(aa)],fill=GREY,width=2);d.line([tuple(b),tuple(bb)],fill=GREY,width=2);arrow(d,tuple(aa),tuple(bb),GREY,3);arrow(d,tuple(bb),tuple(aa),GREY,3);m=(aa+bb)/2;label(d,(m[0]-len(text)*sz*.22,m[1]-sz-8),text,sz,GREY)
def lines(d,x,y,texts,sz=29,lead=48):
 for s in texts:d.text((x,y),s,font=f(sz),fill=GREY);y+=lead
# 1 Installation, side view and underside.
im=Image.new('RGB',(2700,2680),'#f5f7f8');d=ImageDraw.Draw(im)
d.text((55,30),'B1 双夹详细设计  |  开屏使用与实际占用',font=f(57),fill=COL)
d.text((58,112),'MateBook 13s 2023 EMF-16 · 底座厚度/接口/键帽位置尚待实测 · 相机朝 -Y 环境方向',font=f(30),fill=GREY)
ps=paste(im,'02_working_position',(45,190),(1430,1152));d.text((70,1280),'屏幕朝操作者；相机放在机身外侧并向后缘外前伸',font=f(30),fill=COL)
ps2=paste(im,'03_rear_structure',(1520,195),(1120,1015));d.text((1550,1200),'主件 + 2个压脚，共3个打印件',font=f(36),fill=COL)
lines(d,1550,1260,['主体：153.5 × 173 × 134 mm','双夹中心：距示意后缘 88 / 160 mm','夹距 72 mm，修改位置后须重新打印'],29,49)
side=paste(im,'02b_laptop_side',(45,1475),(1250,1029));bot=paste(im,'02c_laptop_bottom',(1390,1475),(1250,1029))
d.text((70,1435),'侧面：梁下沉，接口区域仍需逐项对照实物',font=f(30),fill=COL)
d.text((1415,1435),'底面：两块18 × 24 mm软垫接触，不铺满底壳',font=f(30),fill=COL)
dim(d,bot('contact1'),bot('contact2'),'72 mm',(35,60),28)
d.text((65,2570),'先用小夹口试片确认：上垫不压键帽，下垫不落风口/脚垫/斜面。不得直接整件强夹试配。',font=f(31),fill=ORANGE)
im.save(P/'B1_01_整机安装与避让.png')
# 2 exploded view and sequence. Actual CAD meshes are the same as the print candidate.
im=Image.new('RGB',(2500,2440),'#f5f7f8');d=ImageDraw.Draw(im)
d.text((55,28),'B1 爆炸图与装配顺序',font=f(58),fill=COL)
d.text((58,108),'打印件只有主体1件、压脚2件；软垫/紧固件/相机/球形marker另配。',font=f(32),fill=GREY)
px=paste(im,'04_exploded',(50,165),(1810,1559))
for key,num in [('camera','1'),('main','2'),('M3','3'),('nut1','4'),('shoe1','5'),('knob2','6'),('top_pad2','7'),('markers','8')]:
 x,y=px(key);d.ellipse((x-24,y-24,x+24,y+24),fill='white',outline=ORANGE,width=3);d.text((x-10,y-23),num,font=f(30),fill=ORANGE)
lines(d,1850,330,['1  D435i 相机','2  一体双夹主体','3  M3×10 + 每孔总厚1mm垫片','4  M5螺母，从上方放入窝','5  活动压脚，盲孔向螺杆','6  M5×30手拧螺杆','7  上/下2mm软垫','8  5个球形反光点'],26,82)
d.text((1870,1060),'不要反向装螺母',font=f(35),fill=ORANGE)
lines(d,1870,1120,['螺母由下方3.7mm底面承力','不可强压更厚螺母','不可用金属螺杆直接顶底壳'],25,51)
steps=[('1 试片确认接触面','先核硬边、键帽、风口'),('2 装螺母和压脚','上下软垫完整接触后轻紧'),('3 测旋入量后装相机','突出量1.8–2.2mm，且<3mm'),('4 粘点并固定线缆','检查全动作可见性，重新标定')]
for i,(a,b) in enumerate(steps):
 x=35+i*620;y=1730;d.text((x+5,y),a,font=f(31),fill=COL);im.paste(Image.open(P/'renders'/f'assembly_step_{i+1}.png').convert('RGB').resize((600,545)),(x,y+55));d.text((x+5,2375),b,font=f(23),fill=GREY)
im.save(P/'B1_02_爆炸与装配.png')
# 3 Critical true CAD sections.
im=Image.new('RGB',(3000,1820),'#f5f7f8');d=ImageDraw.Draw(im)
d.text((55,30),'B1 三个关键截面  |  mm',font=f(60),fill=COL)
d.text((58,118),'蓝绿=打印件，灰=电脑/相机包络，金色=金属件，黑=软垫；金属螺纹用光杆包络表示。',font=f(31),fill=GREY)
items=[('05_section_AA','A-A  单个夹口'),('06_section_BB','B-B  相机后安装孔'),('07_section_CC','C-C  双夹之间的下沉梁')]
trans=[]
for i,(name,title) in enumerate(items):
 x=30+i*990;d.text((x+20,202),title,font=f(42),fill=COL);fn=paste(im,name,(x,270),(950,[855,823,792][i]));trans.append(fn)
# dimensions are tied to camera-projected design points.
a=trans[0];dim(d,a('T_top'),a('T_bottom'),'T 待量',(-20,0),25);label(d,(65,1190),'8–22 mm 为名义调节目标，不是实测厚度',28,ORANGE)
b=trans[1];dim(d,b('camera_back'),b('plate_back'),'7 mm',(0,-50),27)
tip=np.array(b('hole'))+np.array(b('screw_tip'))-np.array(b('camera_back'));arrow(d,(1840,430),tuple(tip));label(d,(1740,335),'名义旋入 2 mm',29,ORANGE)
c=trans[2];dim(d,c('rail_top'),c('rail_bottom'),'12 mm',(125,0),28);dim(d,c('rail_left'),c('rail_right'),'10 mm',(0,125),28)
lines(d,60,1280,['压脚 18×24×5；盲孔 Ø5.8，深2','上下软垫各2mm；M5螺杆30mm','M5 DIN934：对边8、厚4；窝AF8.5','螺母窝深4.3，承压底厚3.7','仅夹厚机械可调，夹距/位置需改CAD'],29,65)
lines(d,1050,1280,['后孔距45；通孔Ø3.4；接触路径7','M3×10，硬垫片总厚约1mm/孔','10 − 7 − 1 = 名义2mm突出量','装前用卡尺量1.8–2.2mm且严格<3','此剖面不代表相机真实孔底和螺纹'],29,65)
lines(d,2040,1280,['梁截面10×12，最高点Z=-26','机身右边缘X=0，梁内侧X=+4','示意底座T=12，竖向让空14mm','真实插头、接口与风口仍待测','连接柱及两夹区不可落在接口处'],29,65)
d.text((60,1740),'先完成小试片接触验证，再装相机。无笔记本允许夹力数据，不能按相机扭矩去拧塑料夹口。',font=f(33),fill=ORANGE)
im.save(P/'B1_03_关键截面.png')
# 4 non-coplanar coordinate sheet.
pts=np.array(q['params']['markers']);fig,axs=plt.subplots(1,3,figsize=(14,4.5));colors=['#d56823','#1b7bb4','#39945a','#8c57a0','#c9484d']
for ax,(u,v,title) in zip(axs,[(0,1,'TOP / XY'),(0,2,'FRONT / XZ'),(1,2,'SIDE / YZ')]):
 for i,a in enumerate(pts):ax.scatter(a[u],a[v],s=95,color=colors[i]);ax.annotate('ABCDE'[i],(a[u],a[v]),xytext=(6,6),textcoords='offset points',fontsize=14,fontweight='bold')
 ax.set_aspect('equal');ax.grid(alpha=.23);ax.set_xlabel('XYZ'[u]+' / mm');ax.set_ylabel('XYZ'[v]+' / mm');ax.set_title(title,fontsize=15);ax.margins(.23)
fig.tight_layout();fig.savefig(P/'marker_orthographic.png',dpi=180);plt.close(fig)
im=Image.new('RGB',(2700,1720),'#f5f7f8');d=ImageDraw.Draw(im);d.text((55,30),'B1 五点空间坐标与主要尺寸',font=f(58),fill=COL)
d.text((60,116),'坐标：X向机身右侧外；Y从后缘朝掌托/操作者；Z从键盘甲板向上。光轴朝 -Y。',font=f(32),fill=GREY)
im.paste(Image.open(P/'marker_orthographic.png').convert('RGB').resize((2590,833)),(55,200))
lines(d,70,1060,['点位        X          Y          Z     （贴面中心，mm）','A           22         24         56','B          121         19         69','C           27        106         79','D          117        102         50','E           72         64         94'],31,70)
lines(d,1210,1070,['点阵跨度 99 × 87 × 44 mm；五座直径25mm','五种四点组合体积均>0，中心化秩=3','最小点距63.36mm；奇异值比0.362','主件外廓153.5×173×134mm（不含球/螺杆）','电脑侧边外最大伸出约133.5mm','双夹72mm；主梁10×12mm；软垫18×24mm'],31,65)
d.text((65,1560),'图中的球径14mm、球心高出贴面9mm只是参考。实际球心需按真实底座/胶层/粘贴偏心重新标定。',font=f(31),fill=ORANGE)
d.text((65,1620),'这是设计坐标，不是RealSense SDK的光学坐标系。非共面不等于全角度可见，也不代表测量精度。',font=f(31),fill=GREY)
im.save(P/'B1_04_尺寸与动捕坐标.png')
