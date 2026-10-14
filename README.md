# HandleSlamModel

[English](README.en.md) · 毫米 / millimetres

三款 D435i 打印支架的设计文件：双手 Livox 改装、单手空间动捕架、笔记本 B1 双夹试装架。这里保留此前交付的零件几何，没有为发布重新设计或宣称升级修复。

**状态：研究原型。数字几何检查不等于实物适配、强度或跟踪性能认证。** 旧支架曾装配，但无法对应到本库的确切版本；单手 v2 与 B1 均不能据此标为“实测通过”。B1 尚未实装验收。

## 选择设计

| 目录 | 用途 | 本库打印文件 | 重要边界 |
| --- | --- | --- | --- |
| [双手 Livox v1](mounts/dual_hand_livox_v1/README.md) | 利用 Livox_handheld 底板、双手柄和笔记本托架，增加 D435i | 6 种新增件，含可选垫片/试片 | 上游 5 种原件不随本库分发；不是完整 11-STL 包 |
| [单手空间 v2](mounts/single_hand_spatial_v2/README.md) | 单手 D435i，5 个空间错位粘贴式动捕点座 | 5 种，共打印 9 件 | M4×50 接头紧固件余量需实测；不混装单手 v1 |
| [笔记本 B1](mounts/laptop_b1/README.md) | D435i 与 5 个一体点座，双夹固定于笔记本底座 | 3 种，正式装配 3 件，另有可选试片 | 以 MateBook EMF-16 为设计背景，尚未精配；严禁提支架搬电脑 |

## 先读再打印

1. 读对应目录的 README、BOM 和装配说明，以及 [已知问题](docs/KNOWN_ISSUES.md)。
2. STL 用 mm、100% 比例导入。STEP 是装配坐标的可编辑中性实体；不要将两者方向差异当成尺寸错误。
3. 先试片、再空载试配，确认孔径、实际五金、接触面和支撑清理路径。相机最后装。
4. 实测相机螺丝伸出量。相机后 M3 孔的 3 mm 上限不能用于底部 1/4-20 孔。
5. 拍摄真实 RGB/红外/深度画面，检查线缆、散热和动捕可见性；重新测量球心并标定外参。

不要敲打装入螺母、用自攻螺钉代替机器螺纹紧固件，或靠强拧拉齐错孔。没有额定载荷；不用于悬吊、防坠或载人。

## 修改与验证

源码使用 CadQuery 2.7.0 与 NumPy。各款 README 有重建命令。建议先复制目录，重建会覆盖导出文件和报告。只查看、编辑 STEP 或切片 STL 不必运行 Python。

```sh
python -m pip install -r requirements.txt
python scripts/verify_release.py
```

[验证状态](docs/VALIDATION.md) 区分历史检查、发布时重新检查、未完成的实物试验。文档改动不会自动更新源文件里的几何和原始 QA。

## 来源与许可

发布准备过程中仅收录自制零件和可追溯源码。Livox 原件、下载的相机 CAD/网格、整机 Blend、含第三方模型的历史渲染、个人照片和无关资料均不在本库。

本库自制代码、CAD与文档统一采用 GPL-2.0-only，经发布者确认。见 [LICENSE](LICENSE) 与 [LICENSING.md](LICENSING.md)。第三方依赖仍遵守其自身许可。

[上游依赖与署名](docs/ATTRIBUTION.md) · [变更记录](CHANGELOG.md) · [文件校验](SHA256SUMS.txt)
