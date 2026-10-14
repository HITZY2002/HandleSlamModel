# Validation status / 验证状态

## 发布检查 / Release checks

`scripts/verify_release.py` reads the actual 14 STL files and 14 corresponding independent STEP solids. Results are written to `validation/release_geometry.json`, with file hashes and the actual runtime timestamp.

Checks: finite coordinates; closed/manifold edges after 0.00001 mm coordinate welding; consistent edge directions; no zero-area triangles by the stated numerical threshold; positive signed volume; STL lower face within 0.01 mm of Z=0 (CAD export tolerance); valid single-solid STEP; mesh/STEP bounding dimensions and volume agreement within explicit tolerances.

发布检查不等于严格三角面自交证明、完整装配碰撞证明、螺母有效啮合/拧紧验证或机械强度分析。未运行的物理试验不会因几何通过而变成通过。

## 原设计记录 / Historical design records

- Dual-hand v1: `source/cad_validation.json`, `source/mesh_validation.json`. Six custom CAD/STL types. These do not validate excluded upstream geometry or a physical assembled rig.
- Single-hand v2: `QA.json`, `STL_validation.json`. Five types, nominal assembled-volume intersections, smooth bolt-shaft paths and a simplified USB envelope. No actual thread, head/tool-access or hardware-tolerance certification.
- B1: `QA.json`, `STL_validation.json`, `STEP_validation.json`. Three printable types and original nominal reference-assembly checks. The reference laptop is illustrative and cannot establish actual contact pressure, friction, port clearance or fit.

这些文件保留原交付记录。记录中出现的参考总装不表示相应文件一定打包，也不表示实物验收。

## 尚未完成 / Not performed

| Design / 设计 | Physical acceptance / 实物状态 | Still needed / 待验证 |
| --- | --- | --- |
| Dual-hand v1 | Prior build exists, exact revision unknown / 旧装配版本未匹配 | bottom camera bolt engagement, vents, laptop fit, all structural hardware, load/creep/heat |
| Single-hand v2 | No version-matched acceptance / 没有本版验收 | M4 joint stack-up, support removal, actual camera and grip fit, optical visibility/calibration |
| Laptop B1 | Never physically accepted / 从未实装验收 | measured laptop contact/keep-outs, coupon fit, safe clamp pressure, slip/heat/finish, FOV |

All designs require real cable and marker geometry checks, controlled low-height trials and appropriate engineering judgment. No rated load, fatigue life, drop resistance or tracking accuracy is claimed.

## 重建 / Source reproducibility

The CAD scripts are preserved from the original deliveries. Run only in a copied directory to avoid replacing the curated exports and historical records. Successful regeneration and matching geometry are useful software checks, but do not close the physical tests above. See any separate source-rebuild report under `validation/` for the actual checks performed.
