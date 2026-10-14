from pathlib import Path
import struct,json,numpy as np
out=Path(__file__).resolve().parents[1]
report={}
for f in (out/'stl').glob('*.stl'):
 data=f.read_bytes();n=struct.unpack('<I',data[80:84])[0]
 a=np.frombuffer(data,dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]),offset=84)
 t=a['v'].astype(float)
 v,ids=np.unique(np.round(t.reshape(-1,3),5),axis=0,return_inverse=True);face=ids.reshape(-1,3)
 e=np.concatenate([face[:,[0,1]],face[:,[1,2]],face[:,[2,0]]]);sorted_e=np.sort(e,axis=1);ue,counts=np.unique(sorted_e,axis=0,return_counts=True)
 area=np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1)*.5
 # Signed volume should be positive for outward orientated closed solids.
 volume=np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6
 edge_sign=np.where(e[:,0]<e[:,1],1,-1);key=sorted_e[:,0]*len(v)+sorted_e[:,1];order=np.argsort(key);bad_winding=int(np.sum(edge_sign[order].reshape(-1,2).sum(1)!=0)) if np.all(counts==2) else -1
 result={'triangles':n,'vertices_welded':len(v),'boundary_edges':int(np.sum(counts==1)),'nonmanifold_edges':int(np.sum(counts>2)),'degenerate_triangles':int(np.sum(area<1e-8)),'inconsistent_winding_edges':bad_winding,'signed_volume_mm3':float(volume),'dimensions_mm':(v.max(0)-v.min(0)).tolist(),'watertight':bool(np.all(counts==2))}
 assert result['watertight'] and result['degenerate_triangles']==0 and bad_winding==0 and volume>0,(f,result)
 report[f.name]=result
(out/'source'/'mesh_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
