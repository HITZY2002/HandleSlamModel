"""D435i one-hand spatial marker cage V2. mm; CadQuery 2.7+ / NumPy.
Camera rear face Y=0, forward -Y, bottom Z=0. Edit stations in MARKERS.
"""
from pathlib import Path
import cadquery as cq, numpy as np, json, math, itertools
OUT=Path(__file__).resolve().parent
for d in ['STL','STEP']: (OUT/d).mkdir(exist_ok=True)
PAD_T=5.5; PAD_MAIN_D=30.; PAD_EAR_X=17.; M3_CLEAR=3.4; M4_CLEAR=4.5
# ID, adhesive face center, outward normal; actual ball center = face + standoff * normal.
AX,AZ=-60.,65.; BX,BZ=50.,105.; CY,CZ=0.,94.; DY,DZ=90.,55.; EY,EZ=62.,119.
MARKERS=[('A',(AX,12-PAD_T,AZ),(0,-1,0)),('B',(BX,20+PAD_T,BZ),(0,1,0)),('C',(-5-PAD_T,CY,CZ),(-1,0,0)),('D',(5+PAD_T,DY,DZ),(1,0,0)),('E',(-5-PAD_T,EY,EZ),(-1,0,0))]
def box(x,y,z,c):return cq.Workplane('XY').box(x,y,z).translate(c).val()
def cyl(r,p,d,h):return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*d))
def cy(r,y0,h,x=0,z=0):return cyl(r,(x,y0,z),(0,1,0),h)
def bar(a,b,r=6,y0=12,h=8):
 ax,az=a;bx,bz=b;L=math.hypot(bx-ax,bz-az);nx=-(bz-az)/L*r;nz=(bx-ax)/L*r
 w=cq.Wire.makePolygon([cq.Vector(ax+nx,y0,az+nz),cq.Vector(bx+nx,y0,bz+nz),cq.Vector(bx-nx,y0,bz-nz),cq.Vector(ax-nx,y0,az-nz),cq.Vector(ax+nx,y0,az+nz)])
 return cq.Solid.extrudeLinear(w,[],cq.Vector(0,h,0)).fuse(cy(r,y0,h,ax,az),cy(r,y0,h,bx,bz))
def landing(x,z,y0=12,h=8):return cy(PAD_MAIN_D/2,y0,h,x,z).fuse(box(34,h,8,(x,y0+h/2,z)),cy(5.2,y0,h,x-17,z),cy(5.2,y0,h,x+17,z))
def clear(s,pts,d,axis=(0,1,0),length=180):
 for p in pts:s=s.cut(cyl(d/2,p,axis,length))
 return s.clean()
def clear_y(s,pts,d):return clear(s,[(x,-60,z) for x,z in pts],d)
# Main lateral fork, camera carrier, and grip interface.
frame=box(36,8,58,(0,16,-8)).fuse(box(36,13,17,(0,13.5,12.5)),box(62,6,17,(0,4,12.5)),box(44,8,50,(0,16,41)))
for x in [-22.5,22.5]:frame=frame.fuse(cy(4,0,1,x,12.5))
frame=frame.fuse(bar((-14,55),(AX,AZ),7),bar((14,58),(BX,BZ),7),landing(AX,AZ),landing(BX,BZ))
frame=clear_y(frame,[(-22.5,12.5),(22.5,12.5)],M3_CLEAR)
grip_holes=[(x,z) for x in [-10,10] for z in [-8,-27]]
mount_holes=[(x,z) for x in [-14,14] for z in [32,60]]
frame=clear_y(frame,grip_holes+mount_holes,M4_CLEAR)
frame=clear_y(frame,[(AX-17,AZ),(AX+17,AZ),(BX-17,BZ),(BX+17,BZ)],M3_CLEAR)
# Grip is unchanged from v1; constant-thickness profile, printed on flat side.
grip=cq.Workplane('XY').box(32,28,112).edges('|Y').fillet(5).val().translate(cq.Vector(0,34,-81))
grip=grip.fuse(cq.Workplane('XY').box(40,28,37).edges('|Y').fillet(3).val().translate(cq.Vector(0,34,-18.5)))
grip=clear_y(grip,grip_holes,M4_CLEAR)
for x,z in grip_holes:grip=grip.cut(cy(4.3,33,16,x,z))
for z in [-52,-68,-84,-100,-116]:grip=grip.cut(cyl(2,(-20,48,z),(1,0,0),40))
grip=clear_y(grip,[(0,-128)],5.2)
for x in [-15,15]:grip=grip.cut(box(3,35,6,(x,34,-18)))
grip=grip.clean()
# Separate U connector: upper slot 10.4 wide receives 10 mm depth fork.
hub=box(44,32,40,(0,36,46)).cut(box(10.4,34,34,(0,36,51)))
hub=clear_y(hub,mount_holes,M4_CLEAR)
joint_holes=[(y,z) for y in [28,44] for z in [43,53]]
hub=clear(hub,[(-40,y,z) for y,z in joint_holes],M4_CLEAR,(1,0,0))
# Depth fork designed as a flat XZ profile then rotated into YZ.
# local u becomes global Y; local extrusion becomes -X.
fork=box(32,10,32,(36,0,50))
for a,b in [((36,60),(CY,CZ)),((36,55),(DY,DZ)),((36,55),(EY,EZ)),((CY,CZ),(EY,EZ)),((DY,DZ),(EY,EZ))]:fork=fork.fuse(bar(a,b,6,-5,10))
for y,z in [(CY,CZ),(DY,DZ),(EY,EZ)]:fork=fork.fuse(landing(y,z,-5,10))
fork=clear_y(fork,joint_holes,M4_CLEAR)
fork=clear_y(fork,[(y+o,z) for y,z in [(CY,CZ),(DY,DZ),(EY,EZ)] for o in [-17,17]],M3_CLEAR)
fork=fork.rotate((0,0,0),(0,0,1),90).clean()
# Reusable pad has a clear central adhesive area of 27.6 mm diameter.
pad=landing(0,0,0,PAD_T);pad=clear_y(pad,[(-17,0),(17,0)],M3_CLEAR)
for x in [-17,17]:pad=pad.cut(cy(3.2,2.3,4,x,0))
pad=pad.clean()
def placed_pad(id):
 _,pos,n=next(m for m in MARKERS if m[0]==id)
 shape=pad
 if n==(0,-1,0):shape=shape.rotate((0,0,0),(1,0,0),180)
 elif n==(-1,0,0):shape=shape.rotate((0,0,0),(0,0,1),90)
 elif n==(1,0,0):shape=shape.rotate((0,0,0),(0,0,1),-90)
 base=np.array(pos)-PAD_T*np.array(n)
 return shape.translate(cq.Vector(*base))
parts={'01_lateral_frame_x1':frame,'02_grip_x1':grip,'03_u_connector_x1':hub,'04_depth_fork_x1':fork,'05_adhesive_pad_x5':pad}
installed=[('frame',frame),('grip',grip),('hub',hub),('depth_fork',fork)]+[(f'pad_{i}',placed_pad(i)) for i,_,_ in MARKERS]
camera=box(90.15,25.15,25.15,(0,-12.575,12.575))
qa={'version':'v2 supersedes v1','units':'mm','parts':{},'installed_collisions':[],'not_verified':['physical fit','load and fatigue','thermal behavior','real cable geometry','real ball geometry and optical visibility','calibration accuracy']}
def print_pose(name,s):
 if name.startswith('01'):s=s.rotate((0,0,0),(1,0,0),-90)
 elif name.startswith(('02','05')):s=s.rotate((0,0,0),(1,0,0),90)
 elif name.startswith('04'):s=s.rotate((0,0,0),(0,1,0),90)
 bb=s.BoundingBox();return s.translate(cq.Vector(-bb.xmin,-bb.ymin,-bb.zmin))
for name,s in parts.items():
 assert s.isValid() and len(s.Solids())==1,name
 q=print_pose(name,s);bb=q.BoundingBox()
 qa['parts'][name]={'valid':s.isValid(),'solids':len(s.Solids()),'volume_cm3':round(s.Volume()/1000,3),'print_bounds_mm':[round(bb.xlen,3),round(bb.ylen,3),round(bb.zlen,3)]}
 cq.exporters.export(q,str(OUT/'STL'/f'{name}.stl'),tolerance=.05,angularTolerance=.1);cq.exporters.export(s,str(OUT/'STEP'/f'{name}.step'))
for i,(an,a) in enumerate(installed):
 for bn,b in installed[i+1:]+[('camera_reference',camera)]:
  v=a.intersect(b).Volume()
  if v>1e-5:qa['installed_collisions'].append([an,bn,v])
assert not qa['installed_collisions'],qa['installed_collisions']
# Full shafts, excluding threads/heads: check clear paths through all printed solids.
shafts=[]
for x,z in grip_holes:shafts.append(('grip M4',cyl(2,(x,4,z),(0,1,0),30)))
for x,z in mount_holes:shafts.append(('hub mount M4',cyl(2,(x,11,z),(0,1,0),50)))
for y,z in joint_holes:shafts.append(('cross joint M4',cyl(2,(-23,y,z),(1,0,0),50)))
for id,pos,n in MARKERS:
 p=np.array(pos,dtype=float);norm=np.array(n);axis=-norm;seat=p-3.2*norm;offset=np.array([1,0,0]) if id in ['A','B'] else np.array([0,1,0]);L=16 if id in ['A','B'] else 20
 for sign in [-1,1]:shafts.append(('pad '+id+' M3',cyl(1.5,tuple(seat+sign*17*offset),tuple(axis),L)))
qa['shaft_collisions']=[]
for hn,hs in shafts:
 for pn,ps in installed:
  v=hs.intersect(ps).Volume()
  if v>1e-5:qa['shaft_collisions'].append([hn,pn,v])
assert not qa['shaft_collisions'],qa['shaft_collisions']
# Conservative assumed top USB plug envelope, plus frame/camera checks.
usb=box(16,20,35,(0,-12.575,42.65));qa['assumed_usb_plug_mm']=[16,20,35]
qa['usb_collisions']=[n for n,s in installed if s.intersect(usb).Volume()>1e-5];assert not qa['usb_collisions']
p=np.array([pos for _,pos,_ in MARKERS]);sv=np.linalg.svd(p-p.mean(0),compute_uv=False)
vols={''.join(MARKERS[i][0] for i in c):round(abs(np.linalg.det(np.stack([p[c[k]]-p[c[0]] for k in [1,2,3]])))/6,3) for c in itertools.combinations(range(5),4)}
qa['marker_adhesive_faces']=[{'id':id,'xyz_mm':pos,'outward_normal':n} for id,pos,n in MARKERS]
qa['spatial_metrics_on_ADHESIVE_FACE_centers']={'axis_ranges_mm':np.ptp(p,axis=0).tolist(),'centered_singular_values_mm':sv.tolist(),'smallest_largest_ratio':float(sv[-1]/sv[0]),'minimum_pair_distance_mm':min(float(np.linalg.norm(a-b)) for a,b in itertools.combinations(p,2)),'tetrahedra_mm3':vols,'rank':int(np.linalg.matrix_rank(p-p.mean(0)))}
qa['illustrative_ball_centers_for_7mm_offset']= [(p[i]+7*np.array(n)).tolist() for i,(_,_,n) in enumerate(MARKERS)]
compound=cq.Compound.makeCompound([s for _,s in installed]+[camera]);bb=compound.BoundingBox();qa['assembly_bounds_without_balls_mm']=[bb.xlen,bb.ylen,bb.zlen]
assembly=cq.Assembly(name='D435i_spatial_one_hand_v2')
for n,s in installed:assembly.add(s,name=n,color=cq.Color(.15,.4,.48) if n not in ['grip','hub'] and not n.startswith('pad') else cq.Color(.9,.52,.16) if n.startswith('pad') else cq.Color(.2,.23,.26))
assembly.add(camera,name='CAMERA_ENVELOPE_REFERENCE_ONLY',color=cq.Color(.7,.72,.75));assembly.save(str(OUT/'STEP'/'assembly_reference_v2.step'))
render=[]
for n,s in installed+[('camera',camera)]:
 vs,ts=s.tessellate(.1,.15);render.append({'name':n,'v':[[v.x,v.y,v.z] for v in vs],'f':ts})
(OUT/'render_meshes.json').write_text(json.dumps(render));(OUT/'QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
