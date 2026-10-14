from pathlib import Path
import struct, numpy as np, collections,json,hashlib
P=Path(__file__).resolve().parent
results={}
for p in (P/'STL').glob('*.stl'):
 b=p.read_bytes(); n=struct.unpack_from('<I',b,80)[0]
 if len(b)==84+50*n:
  tris=np.array([struct.unpack_from('<12fH',b,84+i*50)[3:12] for i in range(n)]).reshape(-1,3,3)
 else:
  text=b.decode();pts=[list(map(float,l.strip().split()[1:])) for l in text.splitlines() if l.strip().startswith('vertex ')];tris=np.array(pts).reshape(-1,3,3)
 ed=collections.Counter();orient=collections.Counter()
 for t in tris:
  pts=[tuple(np.round(v,5)) for v in t]
  for a,c in zip(pts,pts[1:]+pts[:1]):ed[tuple(sorted((a,c)))]+=1;orient[(a,c)]+=1
 bad=sum(v!=2 for v in ed.values());deg=int((np.linalg.norm(np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]),axis=1)<1e-9).sum());wrong=sum(orient[(a,c)]!=1 or orient[(c,a)]!=1 for a,c in ed)
 vol=float(np.einsum('ij,ij->i',tris[:,0],np.cross(tris[:,1],tris[:,2])).sum()/6)
 r={'triangles':len(tris),'boundary_or_nonmanifold_edges':bad,'degenerate_triangles':deg,'inconsistent_edges':wrong,'signed_volume_mm3':vol,'bounds_mm':(tris.max((0,1))-tris.min((0,1))).tolist(),'sha256':hashlib.sha256(b).hexdigest()};results[p.name]=r
 assert bad==deg==wrong==0 and vol>0,(p,r)
(P/'STL_validation.json').write_text(json.dumps(results,indent=2));print('PASS',len(results),'actual STL files')
