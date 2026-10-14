# 双手 Livox → D435i v1 / Dual-hand retrofit

2026-09-30 设计。保留 Livox_handheld 主底板、双手柄和笔记本托架，新增 D435i 支架。**本目录仅含 6 种新增件，不含整机原件，也不是完整 11-STL 打印包。**

The custom adapter attaches to the existing Livox base without changing its four-hole pattern. Original frame parts must be obtained separately from [the pinned upstream version](https://github.com/hku-mars/Livox_handheld/tree/31def48c50816932e5c5043d54c80a51fb80a6bf).

## 文件 / Files

- `stl/`: 6 种打印方向 STL。主件约 109.11 × 51 × 74 mm。
- `source/*.step`: 6 种可编辑 CAD 实体，装配坐标。
- `source/build_adapter.py`: 原始 CadQuery 参数化源；`parameters.json` 是导出的记录，不是自动读入的配置。
- `source/cad_validation.json`、`mesh_validation.json`: 原交付数字检查记录，不能当作实物验收。

[BOM](BOM.md) · [打印与装配 / Print and assembly](PRINT_ASSEMBLY.md) · [上游依赖](../../docs/ATTRIBUTION.md)

## 关键限制 / Limits

底部 1/4-20 UNC 相机孔允许伸入量仍需向实物或原厂安装件核对；不能套用后部 M3 的 3 mm。窄接触环与真实散热槽、USB 和笔记本视野都要实测。旧支架的装配经历无法对应到本快照，不能标为本版通过。

Bottom 1/4-20 engagement is unresolved. Check the contact ring against real vents, plus cable and laptop occlusion. No verified load, fatigue, heat or drop rating is available.

## 重建 / Rebuild

在仓库根目录运行；先复制此目录，因为导出会覆盖文件：

```sh
python mounts/dual_hand_livox_v1/source/build_adapter.py
python mounts/dual_hand_livox_v1/source/validate_meshes.py
```

修改几何应编辑源码内参数和对应几何值，不能只改 `parameters.json`。重建只生成新增件；不会生成上游 SolidWorks 零件或完整装配历史。

GPL-2.0-only，见 [LICENSE](LICENSE)。Livox 原设计：Jiarong Lin / HKU MARS；改装未获原作者验证或认可。
