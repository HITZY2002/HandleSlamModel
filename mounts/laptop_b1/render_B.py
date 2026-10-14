import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent;p=json.loads((P/'params.json').read_text());D=json.loads((P/'render_meshes.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
mat={}
for n,c in {'main':(.06,.36,.42),'silver':(.64,.68,.72),'dark':(.065,.09,.12),'shoe':(.18,.46,.52),'metal':(.79,.54,.18),'seat':(.98,.67,.20),'ball':(.95,.97,.99),'glass':(.08,.14,.18),'key':(.25,.29,.32),'arrow':(.1,.54,.71)}.items():
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);mat[n]=m
objs={};fixed=[];laptop=[];balls=[]
def mesh(n,v,f,ma):
 m=bpy.data.meshes.new(n);m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new(n,m);bpy.context.collection.objects.link(o);o.data.materials.append(mat[ma]);return o
def cube(n,sz,loc,ma,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=sz;o.rotation_euler[0]=rot;o.data.materials.append(mat[ma]);return o
def cyl(n,r,h,loc,ma,axis=(0,0,1)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();o.data.materials.append(mat[ma]);return o
def arrow(a,b):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();L=(b-a).length
 fixed.append(cyl('Optical_axis',1.2,L-8,(a+b)/2-d*4,'arrow',d));bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=4.3,radius2=0,depth=10,location=b-d*5);o=bpy.context.object;o.name='Axis_head';o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat['arrow']);fixed.append(o)
for r in D['assembly']:
 n=r['name'];ma='main' if n=='main' else 'silver' if n=='camera_reference' else 'dark' if '_pad_' in n else 'shoe' if 'shoe' in n else 'metal';objs[n]=mesh(n,r['v'],r['f'],ma)
CX=p['camera_center_x'];CZ=p['camera_hole_z'];T=p['reference_base_thickness'];W=p['reference_laptop_width'];DEP=p['reference_laptop_depth'];ys=[p['clamp_rear_y'],p['clamp_rear_y']+p['clamp_pitch']]
for x in [CX-33,CX-11,CX+15,CX+33]:fixed.append(cyl('Lens',4,1,(x,-25.7,p['camera_envelope_center_z']),'dark',(0,1,0)))
fixed.append(cube('USB_plug_reference',(12,15,18),(CX,-12.5,CZ+22),'dark'))
for i,(x,y,z) in enumerate(p['markers']):
 fixed.append(cyl('Seat_'+str(i),10.8,.4,(x,y,z+.2),'seat'))
 b=cyl('Stem_'+str(i),2.3,4,(x,y,z+2),'ball');balls.append(b)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=p['marker_reference_radius'],location=(x,y,z+p['marker_reference_center_offset']));o=bpy.context.object;o.name='Ball_'+str(i);o.data.materials.append(mat['ball']);balls.append(o)
arrow((CX,-35,CZ),(CX,-92,CZ))
laptop.append(cube('Laptop_base_reference',(W,DEP,T),(-W/2,DEP/2,-T/2),'silver'))
a=math.radians(p['reference_opening_angle_deg']-90);H=205
laptop.append(cube('Lid_outline',(W,5,H),(-W/2,-math.sin(a)*H/2,math.cos(a)*H/2),'silver',a));laptop.append(cube('Screen_operator_side',(W-12,1,H-15),(-W/2,3.1*math.cos(a)-math.sin(a)*H/2,math.cos(a)*H/2+3.1*math.sin(a)),'glass',a))
laptop.append(cube('Keyboard_illustrative',(W-35,96,.7),(-W/2,76,.5),'key'));laptop.append(cube('Touchpad_illustrative',(104,51,.7),(-W/2,182,.5),'key'))
for row in range(5):
 for col in range(13):laptop.append(cube('Key',(16,13,.7),(-W+32+col*18.3,42+row*17,.9),'silver'))
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.studiolight_rotate_z=.4;scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_specular_highlight=True;scene.display.shading.background_type='WORLD';scene.world.color=(.945,.96,.97);scene.view_settings.view_transform='Standard';scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';scene.camera=cam
meta={}
def render(tag,loc,target,scale,res=(1600,1400),points=None):
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.resolution_x,scene.render.resolution_y=res;scene.render.resolution_percentage=100;bpy.context.view_layer.update();scene.render.filepath=str(P/'renders'/f'{tag}.png');bpy.ops.render.render(write_still=True)
 meta[tag]={'size':res,'points':{}}
 for name,pos in (points or {}).items():
  q=world_to_camera_view(scene,cam,Vector(pos));meta[tag]['points'][name]=[q.x*res[0],(1-q.y)*res[1]]
base_pts={'clamp1':(-10,ys[0],5),'clamp2':(-10,ys[1],5),'rail':(9,124,-30),'camera':(70,-12,36),'mast':(9,64,20),'screw1':(-10,ys[0],-50),'screw2':(-10,ys[1],-50),'usb':(70,-12,62),'contact1':(-10,ys[0],-T-2),'contact2':(-10,ys[1],-T-2)}
for i,pos in enumerate(p['markers']):base_pts['marker_'+str(i)]=tuple(Vector(pos)+Vector((0,0,9)))
render('01_front_overview',(450,-530,330),(38,78,25),300,(1500,1600),base_pts)
render('02_working_position',(510,590,350),(-87,72,78),585,(1800,1450),base_pts)
render('02b_laptop_side',(650,90,75),(20,90,75),375,(1700,1400),base_pts)
render('02c_laptop_bottom',(350,370,-480),(-90,95,-5),525,(1700,1400),base_pts)
for o in laptop:o.hide_render=True
render('03_rear_structure',(460,560,310),(39,78,24),285,(1600,1450),base_pts)
# True-parts exploded assembly; movements are cosmetic separation only.
for n,o in objs.items():
 if n=='camera_reference':o.location.y=-65
 elif n.startswith('M3_shank'):o.location.y=44
 elif n.startswith('M3_head'):o.location.y=44
 elif n.startswith('M3_washer'):o.location.y=27
 elif n.startswith('M5_nut'):o.location.x=-30;o.location.z=10
 elif n.startswith('M5_shank') or n.startswith('M5_knob'):o.location.z=-35
 elif n.startswith('pressure_shoe'):o.location.x=-50;o.location.z=-10
 elif n.startswith('bottom_pad'):o.location.x=-50;o.location.z=8
 elif n.startswith('top_pad'):o.location.z=25
for o in fixed:
 if o.name.startswith('Lens') or o.name.startswith('USB'):o.location.y-=65
 if 'Optical' in o.name or 'Axis_' in o.name:o.hide_render=True
for o in balls:o.location.z+=20
expts={'main':(45,70,30),'camera':(70,-77,36),'M3':(92.5,52,36),'nut1':(-40,ys[0],-22),'knob2':(-10,ys[1],-85),'shoe1':(-60,ys[0],-27),'bottom_pad1':(-60,ys[0],-5),'top_pad2':(-10,ys[1],27),'markers':(72,64,123)}
render('04_exploded',(400,560,310),(20,70,10),390,(1800,1550),expts)
for o in list(objs.values())+fixed+balls+laptop:o.hide_render=True
# Actual CAD section solids. Hardware is cut at the same plane through a viewport clipping workflow.
# Other section silhouettes are generated from exported geometry; 2D dimensions are annotated later.
sections={}
for r in D['sections']:
 n=r['name'];ma='silver' if 'laptop' in n or 'camera_reference' in n else 'dark' if 'pad_' in n else 'shoe' if 'shoe_' in n else 'metal' if 'M3_' in n or 'M5_' in n else 'main';sections[n]=mesh(n,r['v'],r['f'],ma)
for o in sections.values():o.hide_render=True
sections['section_AA_clamp'].hide_render=False
# The hardware slice has sufficient depth for orthographic viewing; no fake cut-face dimensions.
sA=[o for n,o in sections.items() if n.startswith('section_AA_') and n!='section_AA_clamp']
for o in sA:o.hide_render=False
render('05_section_AA',(-7,-310,-20),(-7,ys[0],-20),91,(1500,1350),{'T_top':(-36,ys[0],0),'T_bottom':(-36,ys[0],-T),'shoe':(-10,ys[0],-16),'nut':(-10,ys[0],-32),'floor':(1,ys[0],-36),'screw':(-10,ys[0],-43),'mouth_top':(25,ys[0],0),'mouth_bottom':(25,ys[0],-30)})
for o in sA:o.hide_render=True
sections['section_AA_clamp'].hide_render=True;sections['section_BB_camera'].hide_render=False
sB=[o for n,o in sections.items() if n.startswith('section_BB_') and n!='section_BB_camera']
for o in sB:
 o.hide_render=False
 if 'M3_' in o.name:o.location.x=.6
 if 'camera_reference' in o.name:o.location.x=-.6
render('06_section_BB',(400,0,37),(CX-22.5,0,37),65,(1500,1300),{'front':(47.5,-25.15,36),'camera_back':(47.5,0,52),'plate_back':(47.5,7,52),'washer_back':(47.5,8,52),'screw_tip':(47.5,-2,52),'head':(47.5,11,36),'hole':(47.5,0,36)})
for o in sB:o.hide_render=True
sections['section_BB_camera'].hide_render=True;sections['section_CC_rail'].hide_render=False
sC=[o for n,o in sections.items() if n.startswith('section_CC_') and n!='section_CC_rail'];mid=sum(ys)/2
for o in sC:o.hide_render=False
render('07_section_CC',(-4,-300,-18),(-4,mid,-18),80,(1500,1250),{'base_bottom':(-10,mid,-T),'rail_top':(9,mid,-26),'rail_bottom':(9,mid,-38),'rail_left':(4,mid,-32),'rail_right':(14,mid,-32),'open_space':(9,mid,-11),'screen_side':(-22,mid,-6)})
for o in sC:o.hide_render=True
sections['section_CC_rail'].hide_render=True
# Four-step assembly, consistent camera and scale.
for n,o in objs.items():o.location=(0,0,0)
for o in fixed:
 if o.name.startswith('Lens') or o.name.startswith('USB'):o.location.y+=65
for o in balls:o.location.z-=20
for step in range(1,5):
 for n,o in objs.items():
  allowed=n=='main' or (step>=2 and not n.startswith('M3') and n!='camera_reference') or step>=3
  o.hide_render=not allowed
 for o in fixed:o.hide_render=step<3 or o.name.startswith('Seat')
 for o in balls:o.hide_render=step<4
 render(f'assembly_step_{step}',(460,560,310),(39,78,24),285,(1100,1000))
# Replace step 1 with the actual optional coupon and actual pressure-foot/hardware meshes.
for o in bpy.data.objects:
 if o.type=='MESH':o.hide_render=True
import struct
raw=(P/'STL_PROTOTYPE'/'03_optional_fit_coupon_x1.stl').read_bytes();count=struct.unpack_from('<I',raw,80)[0];vv=[];ff=[]
for i in range(count):
 vals=struct.unpack_from('<12fH',raw,84+50*i)[3:12];off=len(vv);vv.extend([vals[j:j+3] for j in [0,3,6]]);ff.append((off,off+1,off+2))
co=mesh('actual_fit_coupon',vv,ff,'main')
for n,o in objs.items():
 if n.endswith('_0') and not n.startswith('M3'):
  du=o.copy();du.data=o.data.copy();bpy.context.collection.objects.link(du);du.hide_render=False;du.location=(20,13-ys[0],38)
cube('coupon_gauge_only',(43,24,T),(-1.5,13,38-T/2),'silver')
render('assembly_step_1',(115,-150,105),(10,13,20),105,(1100,1000))
(P/'projection_points.json').write_text(json.dumps(meta,indent=2))
