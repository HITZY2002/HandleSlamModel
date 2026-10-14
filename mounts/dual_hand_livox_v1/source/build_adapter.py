"""Livox handheld to D435i open-bottom mount, 2026-09-30.
Units: millimetres. Source interface measured from upstream all_parts_holder.STL.
Requires CadQuery 2.7.0. This generates new parts only, not original SolidWorks history.
GPL-2.0-only. See LICENSE and README_装配说明.txt.
"""
from pathlib import Path
import json
import cadquery as cq
OUT=Path(__file__).resolve().parents[1]
(OUT/'source'/'assembly_meshes').mkdir(exist_ok=True)
P={
 'geometry_note':'Bracket is generated in canonical -X view, then mirrored across x=57.109207. Final camera faces +X.',
 'mirror_plane_x':57.109207,'final_camera_screw_x':113.318414,'final_camera_glass_x':128.218414,
 'base_hole_x':[24.107184,90.111230], 'base_hole_y':[164.473588,218.473588],
 'mount_top_z':8.0,'mount_thickness':5.0,'mount_clearance_d':3.6,
 'camera_y':191.473588,'camera_front_x':-14.,'camera_depth':25.05,
 'camera_bottom_z':-35.,'camera_height':25.,'camera_width':90.,
 'camera_screw_x_provisional':0.9,'camera_screw_slot_length':14.8,'camera_screw_slot_width':6.8,
 'shelf_bottom_z':-43.,'shelf_top_z':-37.,'air_gap':2.,
 'shelf_x_min':-13.,'shelf_x_max':41.,'width':74.,
 'rear_wall_x_min':35.,'rear_wall_x_max':41.,
 'stop_screw_x':22.,'stop_screw_y_offset':25.,'stop_slot_length':9.4,'stop_slot_width':3.4,
 'pad_outer_d':9.,'pad_inner_d':6.8,'pad_height':2.
}
(OUT/'source'/'parameters.json').write_text(json.dumps(P,indent=2),encoding='utf-8')
CY=P['camera_y']
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0).translate(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))
def cyl(x,y,z0,z1,d):return cq.Workplane('XY').workplane(offset=z0).center(x,y).circle(d/2).extrude(z1-z0)
def slot_z(x,y,z0,z1,l,w):return cq.Workplane('XY').workplane(offset=z0).center(x,y).slot2D(l,w).extrude(z1-z0)
def triangle_xz(points,y0,th):
 return cq.Workplane('XZ').polyline(points).close().extrude(th).translate((0,y0+th,0))
y0,y1=CY-37,CY+37
main=box(18.107184,96.111230,y0,y1,3,8)
main=main.union(box(35,41,y0,y1,-43,8))
main=main.union(box(-13,41,y0,y1,-43,-37))
for y in [y0,y1-4]:
 main=main.union(triangle_xz([(15,-37),(35,-37),(35,-17)],y,4))
 main=main.union(triangle_xz([(41,-17),(41,3),(61,3)],y,4))
# Four matching original base holes. Source base already has D6 x3 counterbores.
for x in P['base_hole_x']:
 for y in P['base_hole_y']:main=main.cut(cyl(x,y,2,9,3.6))
# Camera 1/4-20 screw goes through a clearance slot, never a printed thread.
main=main.cut(slot_z(.9,CY,-44,-36,14.8,6.8))
# Two antirotation stops attach behind camera. Their fore-aft position is adjustable.
for yy in [-25,25]:main=main.cut(cyl(22,CY+yy,-44,-36,3.4))
# Small cable-strain-relief tie slots on rear web; not on the camera or vents.
for yy in [-12,12]:
 cut=cq.Workplane('YZ').workplane(offset=34).center(CY+yy,-12).rect(3.5,10).extrude(8)
 main=main.cut(cut)
main=main.clean().mirror('YZ',(57.109207,0,0))
# Separate adjustable stop: local x=0 is the camera-contact face, local z=0 lies on shelf.
stop=box(0,18,-5,5,0,4).union(box(0,3,-5,5,0,8))
stop=stop.cut(slot_z(10.65,0,-1,5,9.4,3.4)).clean()
# Narrow ring around the tripod land: verify no vent covered on user's camera.
pad=cq.Workplane('XY').circle(P['pad_outer_d']/2).circle(P['pad_inner_d']/2).extrude(2)
spacer1=cq.Workplane('XY').circle(12/2).circle(6.8/2).extrude(1)
spacer2=cq.Workplane('XY').circle(12/2).circle(6.8/2).extrude(2)
# Fit coupon verifies all four base holes before spending filament on full bracket.
coupon=box(18.107184,96.111230,CY-33,CY+33,0,2)
coupon=coupon.cut(box(30.107184,84.111230,CY-21,CY+21,-1,3))
for x in P['base_hole_x']:
 for y in P['base_hole_y']:coupon=coupon.cut(cyl(x,y,-1,3,3.6))
parts={'D435i_adapter':main,'antirotation_stop_print_2':stop,'camera_contact_ring_2mm':pad,'screw_head_spacer_1mm':spacer1,'screw_head_spacer_2mm':spacer2,'base_fit_coupon_optional':coupon}
report={}
for name,part in parts.items():
 shape=part.val();bb=shape.BoundingBox()
 assert shape.isValid(),name+' invalid BRep'
 assert len(shape.Solids())==1,name+' not one solid'
 cq.exporters.export(part,str(OUT/'source'/'assembly_meshes'/(name+'.stl')),tolerance=0.03,angularTolerance=0.12)
 print_part=part
 if name=='D435i_adapter':
  print_part=part.rotate((0,0,0),(1,0,0),90)
  pbb=print_part.val().BoundingBox();print_part=print_part.translate((-pbb.xmin,-pbb.ymin,-pbb.zmin))
 elif name=='base_fit_coupon_optional':
  pbb=part.val().BoundingBox();print_part=part.translate((-pbb.xmin,-pbb.ymin,-pbb.zmin))
 cq.exporters.export(print_part,str(OUT/'stl'/(name+'.stl')),tolerance=0.03,angularTolerance=0.12)
 cq.exporters.export(part,str(OUT/'source'/(name+'.step')))
 report[name]={'valid_brep':shape.isValid(),'solid_count':len(shape.Solids()),'volume_mm3':shape.Volume(),'bounds_mm':[bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax],'dimensions_mm':[bb.xlen,bb.ylen,bb.zlen]}
(OUT/'source'/'cad_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
