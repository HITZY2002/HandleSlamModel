# 单手空间动捕架 v2 / Single-hand spatial marker mount

2026-10-10 设计。只承载 D435i；5 个可更换粘贴式球形动捕点座，分布在两组垂直支臂上。**5 种打印件，共 9 件。** v2 替代旧平面 v1，不混装两版结构件。

Five replaceable marker pads on a noncoplanar frame. The actual ball-center coordinates must be measured. Noncoplanarity and distributed directions do not guarantee tracking visibility or accuracy.

[BOM](BOM.md) · [打印与装配 / Print and assembly](PRINT_ASSEMBLY.md) · [已知问题](../../docs/KNOWN_ISSUES.md)

## 重要修订说明 / Important release note

旧 BOM 的两组 M4×50 是原设计名义规格；尤其横向穿过 44 mm U 件时，按 2 mm 垫圈及 3.2 mm 螺母仅余约 0.8 mm。**不得当成已验收采购规格，也未核定一个通用替换长度。** 实测实际夹持厚度、垫圈、螺母完整啮合及周边净空后选型。

The historical M4×50 callout is provisional. The transverse joint has little nominal spare length. Do not assume a longer replacement is automatically safe; check both engagement and protrusion clearance.

## 文件与重建 / Files and rebuild

`STL/` 是打印姿态；`STEP/` 是各独立实体的装配坐标。`build_model.py` 与 `verify_stl.py` 为原交付源码；`QA.json` 与 `STL_validation.json` 为原检查记录。

```sh
python mounts/single_hand_spatial_v2/build_model.py
python mounts/single_hand_spatial_v2/verify_stl.py
```

先复制目录。修改源文件顶部点位参数后须重新核查所有接口、碰撞、支撑、点位和实际光学可见性。源码会另生成自制方盒相机包络总装与渲染网格；这些不是相机制造 CAD 或打印零件。

## 状态 / Status

实物装配版本未匹配；没有本版载荷、疲劳、跌落、温升、手型或全角度动捕验收。数字检查只覆盖几何。本目录采用GPL-2.0-only，见 [许可范围](../../LICENSING.md)。
