"""B1 detail prototype for D435i and laptop base. CadQuery 2.7+, NumPy. Units mm.
NOT a dimensionally verified EMF-16 fit. Only jaw thickness is mechanically adjustable.
Clamp pitch/location and contact footprint are changed in params.json BEFORE printing.
STL meshes are exported through a welded degenerate-face filter, then independently checked.
"""
from pathlib import Path
import cadquery as cq,numpy as np,json,math,itertools,struct,collections,hashlib
P=Path(__file__).resolve().parent
for d in ['STL_PROTOTYPE','STEP','renders']:(P/d).mkdir(exist_ok=True)
D={'reference_laptop_width':297.2,'reference_laptop_depth':218.4,'reference_base_thickness':12.,'reference_opening_angle_deg':110.,'clamp_rear_y':88.,'clamp_pitch':72.,'clamp_width':26.,'jaw_intrusion':20.,'jaw_outer_x':14.,'side_wall_inner_x':4.,'upper_jaw_bottom_z':2.,'upper_jaw_thickness':6.,'lower_jaw_top_z':-30.,'lower_jaw_thickness':8.,'pad_thickness':2.,'contact_center_x':-10.,'contact_width_x':18.,'contact_length_y':24.,'shoe_thickness':5.,'shoe_socket_d':5.8,'shoe_socket_depth':2.,'M5_clearance_d':5.6,'nut_pocket_af':8.5,'nut_pocket_depth':4.3,'nut_af_nominal':8.,'nut_thickness_nominal':4.,'M5_under_knob_length':30.,'main_spine_width':10.,'main_spine_height':12.,'mast_y':64.,'camera_center_x':70.,'camera_rear_y':0.,'camera_hole_z':36.,'camera_envelope_center_z':36.075,'camera_hole_spacing':45.,'camera_boss_thickness':1.,'camera_plate_thickness':6.,'camera_clearance_d':3.4,'marker_seat_d':25.,'marker_seat_thickness':3.,'markers':[[22,24,56],[121,19,69],[27,106,79],[117,102,50],[72,64,94]],'marker_reference_radius':7.,'marker_reference_center_offset':9.,'reference_body_thickness_range':[8.,22.],'note':'ALL laptop geometry is illustrative. Base thickness 12 mm is not a measured EMF-16 dimension. Clamp station/contact footprints, lid angle, vents and ports require photos and measurements.'}
f=P/'params.json'
if not f.exists():f.write_text(json.dumps(D,ensure_ascii=False,indent=2))
p=json.loads(f.read_text());T=p['reference_base_thickness'];CX=p['camera_center_x'];CY=p['camera_rear_y'];CZ=p['camera_hole_z'];ys=[p['clamp_rear_y'],p['clamp_rear_y']+p['clamp_pitch']];X=p['contact_center_x'];JTOP=p['lower_jaw_top_z'];JBOTTOM=JTOP-p['lower_jaw_thickness'];W=p['clamp_width'];PAD=p['pad_thickness'];SH=p['shoe_thickness'];MARK=np.array(p['markers'],float)
def box(a,b,c,at):return cq.Workplane('XY').box(a,b,c).translate(at).val()
def cyl(r,at,d,h):return cq.Solid.makeCylinder(r,h,cq.Vector(*at),cq.Vector(*d))
def rod(a,b,r):
 a=np.array(a,float);b=np.array(b,float);v=b-a;L=np.linalg.norm(v)
 return cyl(r,a,v/L,L).fuse(cq.Solid.makeSphere(r,cq.Vector(*a)),cq.Solid.makeSphere(r,cq.Vector(*b)))
def union(ss):
 s=ss[0]
 for a in ss[1:]:s=s.fuse(a)
 return s.clean()
def hex_af(af,z,h,x,y):return cq.Workplane('XY').polygon(6,2*af/math.sqrt(3)).extrude(h).translate((x,y,z)).val()
def jaw(y):
 xmin=-p['jaw_intrusion'];xmax=p['jaw_outer_x'];lx=xmax-xmin;xc=(xmax+xmin)/2
 up=cq.Workplane('XY').box(lx,W,p['upper_jaw_thickness']).edges('|Y').fillet(.8).val().translate(cq.Vector(xc,y,p['upper_jaw_bottom_z']+p['upper_jaw_thickness']/2))
 low=cq.Workplane('XY').box(lx,W,p['lower_jaw_thickness']).edges('|Y').fillet(.8).val().translate(cq.Vector(xc,y,(JTOP+JBOTTOM)/2))
 top=p['upper_jaw_bottom_z']+p['upper_jaw_thickness'];wi=xmax-p['side_wall_inner_x'];wall=box(wi,W,top-JBOTTOM,((xmax+p['side_wall_inner_x'])/2,y,(top+JBOTTOM)/2))
 s=union([up,low,wall])
 s=s.cut(cyl(p['M5_clearance_d']/2,(X,y,JBOTTOM-1),(0,0,1),p['lower_jaw_thickness']+2))
 # TOP-LOADED captured nut. Downward screw reaction is supported by the 3.7 mm floor.
 s=s.cut(hex_af(p['nut_pocket_af'],JTOP-p['nut_pocket_depth'],p['nut_pocket_depth']+1,X,y))
 return s.clean()
def shoe():
 s=cq.Workplane('XY').box(p['contact_width_x'],p['contact_length_y'],SH).edges('|Z').fillet(1.5).val().translate(cq.Vector(0,0,SH/2))
 return s.cut(cyl(p['shoe_socket_d']/2,(0,0,-.1),(0,0,1),p['shoe_socket_depth']+.1)).clean()
# Low connecting rail runs below the base rather than across port height.
rail_end=ys[-1]+W/2;rail_start=p['mast_y']-12.;rail_z=JBOTTOM+p['main_spine_height']/2;rail=box(p['main_spine_width'],rail_end-rail_start,p['main_spine_height'],(9.,(rail_start+rail_end)/2,rail_z))
# Short load path: low rail -> braced mast -> camera back plate and compact marker frame.
mast=p['mast_y'];main_parts=[jaw(y) for y in ys]+[rail,box(10,18,28-JBOTTOM,(9,mast,(28+JBOTTOM)/2))]
main_parts += [rod((9,mast,27),(70,64,35),6),rod((9,mast,4),(CX,CY+9,CZ),6),rod((70,64,35),(CX,CY+7,CZ),6)]
# Front lower gusset reduces bending of the mast, with rail still below the laptop.
main_parts += [rod((9,mast,10),(9,ys[0],rail_z),5.5)]
# Camera bridge: 1 mm contact bosses + 6 mm plate.
plate=box(62,p['camera_plate_thickness'],25,(CX,CY+1+p['camera_plate_thickness']/2,CZ))
for x in [CX-p['camera_hole_spacing']/2,CX+p['camera_hole_spacing']/2]:plate=plate.fuse(cyl(4,(x,CY,CZ),(0,1,0),1))
main_parts += [plate]
anchor=np.array([70,64,35.])
for x,y,z in MARK:
 base=np.array([x,y,35.]);seat=np.array([x,y,z-p['marker_seat_thickness']])
 main_parts += [rod(anchor,base,5),rod(base,seat,5),rod(anchor,base+(seat-base)*.7,4.5),cyl(p['marker_seat_d']/2,(x,y,z-p['marker_seat_thickness']),(0,0,1),p['marker_seat_thickness'])]
main=union(main_parts)
for x in [CX-p['camera_hole_spacing']/2,CX+p['camera_hole_spacing']/2]:
 main=main.cut(cyl(p['camera_clearance_d']/2,(x,CY-1,CZ),(0,1,0),12))
 main=main.cut(cyl(3.6,(x,CY+7,CZ),(0,1,0),4))
# Two cable-tie holes in mast: keep the tether/USB restrained on the bracket, not the screen.
for z in [13,23]:main=main.cut(cyl(2.1,(1,mast,z),(1,0,0),17))
main=main.clean();sho=shoe();coupon=jaw(0)
# The fit coupon is optional, NOT an extra installed assembly piece.
parts={'01_B_main_PROTOTYPE_x1':main,'02_pressure_shoe_x2':sho,'03_optional_fit_coupon_x1':coupon}
cam=box(90.15,25.15,25.15,(CX,CY-12.575,p['camera_envelope_center_z']))
usb=box(16,20,35,(CX,CY-12.575,p['camera_envelope_center_z']+12.575+17.5))
base=box(p['reference_laptop_width'],p['reference_laptop_depth'],T,(-p['reference_laptop_width']/2,p['reference_laptop_depth']/2,-T/2))
refs=[('camera_reference',cam)]
for i,y in enumerate(ys):
 footz=-T-PAD-SH;tipz=footz+p['shoe_socket_depth'];headz=tipz-p['M5_under_knob_length']
 refs += [(f'top_pad_{i}',box(p['contact_width_x'],p['contact_length_y'],PAD,(X,y,PAD/2))),(f'pressure_shoe_{i}',sho.translate(cq.Vector(X,y,footz))),(f'bottom_pad_{i}',box(p['contact_width_x'],p['contact_length_y'],PAD,(X,y,-T-PAD/2))),(f'M5_nut_{i}',hex_af(p['nut_af_nominal'],JTOP-p['nut_pocket_depth']+.1,p['nut_thickness_nominal'],X,y).cut(cyl(2.5,(X,y,JTOP-6),(0,0,1),8))),(f'M5_shank_{i}',cyl(2.5,(X,y,headz),(0,0,1),p['M5_under_knob_length'])),(f'M5_knob_{i}',cyl(10,(X,y,headz-5),(0,0,1),5))]
for i,x in enumerate([CX-22.5,CX+22.5]):
 refs += [(f'M3_shank_{i}',cyl(1.5,(x,CY-2,CZ),(0,1,0),10)),(f'M3_washer_{i}',cyl(3.5,(x,CY+7,CZ),(0,1,0),1).cut(cyl(1.6,(x,CY+6,CZ),(0,1,0),4))),(f'M3_head_{i}',cyl(2.75,(x,CY+8,CZ),(0,1,0),3))]
qa={'version':'B1 detailed design prototype','units':'mm','status':'Not an exact EMF-16 fit. Thickness adjustment is mechanical; clamp station/pitch changes require CAD regeneration and reprint.','params':p,'parts':{},'collisions_mm3':{},'stl_export':{},'not_verified':['actual EMF-16 surfaces/ports/vents/keyboard/feet','physical load, vibration, fatigue, creep and finish sensitivity','real plug/cable geometry','real optical FOV and mocap visibility/calibration','printer process and support removability'],'camera_mount':{'nominal_M3':'M3x10','nominal_printed_path':7,'nominal_washer':1,'nominal_protrusion':2,'required_measured_protrusion':[1.8,2.2],'must_be_less_than':3},'clamp':{'pitch_mm':p['clamp_pitch'],'stations_y_mm':ys,'nut_pocket_entry':'TOP','nut_af_nominal_mm':8,'nut_thickness_nominal_mm':4,'nut_pocket_af_mm':p['nut_pocket_af'],'nut_support_floor_mm':p['lower_jaw_thickness']-p['nut_pocket_depth'],'target_body_thickness_range_mm':p['reference_body_thickness_range'],'M5_nominal_under_knob_length_mm':30,'printed_internal_threads':False}}

def export_clean_stl(shape,path):
 bb=shape.BoundingBox();s=shape.translate(cq.Vector(-bb.xmin,-bb.ymin,-bb.zmin));v,f=s.tessellate(.07,.14);verts=np.array([[a.x,a.y,a.z] for a in v]);tri=np.array([[verts[j] for j in ids] for ids in f]);raw=len(tri)
 # Stable float coordinates: duplicates and zero-area tessellation slivers do not alter surface at useful precision.
 tri=np.round(tri,5).astype(np.float32);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);keep=np.linalg.norm(cross,axis=1)>1e-8;tri=tri[keep];cross=cross[keep]
 normals=cross/np.linalg.norm(cross,axis=1)[:,None]
 with path.open('wb') as out:
  out.write(b'B1 prototype mm; welded 1e-5 mm; verify fit before use'.ljust(80,b'\0'));out.write(struct.pack('<I',len(tri)))
  for n,t in zip(normals,tri):out.write(struct.pack('<12fH',*n,*t.ravel(),0))
 return {'raw_triangles':raw,'exported_triangles':len(tri),'removed_zero_area_slivers':raw-len(tri),'coordinate_rounding_mm':1e-5}
for n,s in parts.items():
 assert s.isValid() and len(s.Solids())==1,(n,s.isValid(),len(s.Solids()))
 bb=s.BoundingBox();bounds=[bb.xlen,bb.ylen,bb.zlen]
 qa['parts'][n]={'valid':s.isValid(),'solid_count':len(s.Solids()),'bounds_mm':[round(a,3) for a in bounds],'volume_cm3':round(s.Volume()/1000,3),'centroid_mm':s.Center().toTuple()}
 assert max(bounds)<180,(n,bounds)
 cq.exporters.export(s,str(P/'STEP'/f'{n}.step'))
 qa['stl_export'][n]=export_clean_stl(s,P/'STL_PROTOTYPE'/f'{n}.stl')
qa['collisions_mm3']['main_camera']=main.intersect(cam).Volume();qa['collisions_mm3']['main_USB_assumed']=main.intersect(usb).Volume();qa['collisions_mm3']['main_laptop_reference']=main.intersect(base).Volume()
qa['collisions_mm3']['main_M3_shanks']=sum(main.intersect(s).Volume() for n,s in refs if n.startswith('M3_shank'))
qa['collisions_mm3']['main_M5_shanks']=sum(main.intersect(s).Volume() for n,s in refs if n.startswith('M5_shank'))
qa['collisions_mm3']['main_pressure_shoes']=sum(main.intersect(s).Volume() for n,s in refs if n.startswith('pressure_shoe'))
qa['collisions_mm3']['main_M5_nuts']=sum(main.intersect(s).Volume() for n,s in refs if n.startswith('M5_nut'))
assert all(v<1e-5 for v in qa['collisions_mm3'].values()),qa['collisions_mm3']
# Range calculations use pad nominal thickness; compression and tapered surfaces are not simulated.
qa['clamp']['range_checks']=[]
for t in p['reference_body_thickness_range']:
 footz=-t-PAD-SH;tip=footz+p['shoe_socket_depth'];head=tip-p['M5_under_knob_length'];nut_top=JTOP-p['nut_pocket_depth']+.1+p['nut_thickness_nominal'];qa['clamp']['range_checks'].append({'body_thickness_mm':t,'shoe_above_lower_jaw_mm':footz-JTOP,'screw_beyond_nut_top_mm':tip-nut_top,'head_clearance_below_lower_jaw_mm':JBOTTOM-head})
 assert footz-JTOP>=.9 and tip-nut_top>3 and JBOTTOM-head>1
sv=np.linalg.svd(MARK-MARK.mean(0),compute_uv=False)
qa['marker_geometry']={'face_centers_mm':MARK.tolist(),'face_normals':[[0,0,1]]*5,'axis_spans_mm':np.ptp(MARK,axis=0).tolist(),'rank':int(np.linalg.matrix_rank(MARK-MARK.mean(0))),'svd_mm':sv.tolist(),'smallest_largest_ratio':float(sv[-1]/sv[0]),'minimum_spacing_mm':min(float(np.linalg.norm(a-b)) for a,b in itertools.combinations(MARK,2)),'tetrahedra_mm3':{''.join('ABCDE'[i] for i in ids):round(abs(np.linalg.det(np.stack([MARK[ids[k]]-MARK[ids[0]] for k in [1,2,3]])))/6,3) for ids in itertools.combinations(range(5),4)},'reference_ball_centers_mm':(MARK+np.array([0,0,p['marker_reference_center_offset']])).tolist()}
assert qa['marker_geometry']['rank']==3 and min(qa['marker_geometry']['tetrahedra_mm3'].values())>0
# Independent scalar force illustrations, NOT a laptop permitted load or verified capacity.
qa['load_illustration']={'moment_Nm':.15,'clamp_spacing_m':p['clamp_pitch']/1000,'equal_opposite_reaction_N':.15/(p['clamp_pitch']/1000),'interpretation':'Only moment divided by clamp spacing; excludes local shell strength, friction, preload, dynamics and eccentric lateral torque. Not a rating or tightening force.'}
ass=cq.Assembly(name='B1_trial_assembly');ass.add(main,name='printed_main',color=cq.Color(.09,.37,.43))
for n,s in refs:ass.add(s,name=n,color=cq.Color(.65,.7,.74) if n=='camera_reference' else cq.Color(.10,.12,.14) if 'pad_' in n else cq.Color(.2,.43,.49) if 'shoe' in n else cq.Color(.8,.55,.2))
ass.save(str(P/'STEP'/'B1_assembly_reference.step'))
# Actual solid intersections for engineering section renders; no fabricated construction lines.
sections={
 'section_AA_clamp':jaw(ys[0]).intersect(box(65,.8,82,(-6,ys[0],-15))),
 'section_BB_camera':main.intersect(box(.8,28,44,(CX-22.5,4,CZ))),
 'section_CC_rail':main.intersect(box(35,.8,80,(9,(ys[0]+ys[1])/2,-10)))
}
# Cut real assembly-reference solids with the identical section planes.
cutAA=box(65,.8,82,(-6,ys[0],-15));cutBB=box(.8,52,44,(CX-22.5,-5,CZ));cutCC=box(70,.8,80,(-10,(ys[0]+ys[1])/2,-10))
for n,o in refs:
 if n.endswith('_0') and not n.startswith('M3'):
  cut=o.intersect(cutAA)
  if cut.Volume()>1e-6:sections['section_AA_'+n]=cut
 if n=='camera_reference' or (n.endswith('_0') and n.startswith('M3')):
  cut=o.intersect(cutBB)
  if cut.Volume()>1e-6:sections['section_BB_'+n]=cut
sections['section_AA_laptop_reference']=base.intersect(cutAA)
sections['section_CC_laptop_reference']=base.intersect(cutCC)
render={'assembly':[],'sections':[]}

for n,s in [('main',main)]+refs:
 v,ts=s.tessellate(.15,.18);render['assembly'].append({'name':n,'v':[[a.x,a.y,a.z] for a in v],'f':ts})
for n,s in sections.items():
 if n in ('section_AA_clamp','section_BB_camera','section_CC_rail'):
  cq.exporters.export(s,str(P/'STEP'/f'{n}.step'))
 assert s.Volume()>0,(n,s.Volume());v,ts=s.tessellate(.07,.12);render['sections'].append({'name':n,'v':[[a.x,a.y,a.z] for a in v],'f':ts})
(P/'render_meshes.json').write_text(json.dumps(render));(P/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));print(json.dumps(qa,ensure_ascii=False,indent=2))
