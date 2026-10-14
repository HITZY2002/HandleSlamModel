# Print and assembly / 打印与装配

## 打印起点 / Slicer starting point

原设计建议 PETG 或 ASA；0.2 mm 层高、5–6 道墙、5–6 层顶底、35–45% 填充。不是强度保证。主 STL 已侧放并落在 Z=0；不要重新整体缩放。检查横孔/槽的桥接与局部支撑可拆性，先打印四孔试片。

The suggested material and settings are unvalidated starting points. Preserve the provided orientation, inspect every support path and dry-fit the coupon first. Keep mating surfaces and slots free of support residue.

## 装配 / Assembly

1. 拆除旧雷达、电池、相机组件，暂卸上方笔记本托架。确认是正确上游版本。
2. 试片检查四孔。名义孔距 66.004046 × 54 mm；新增孔 Ø3.6 mm。错位时停下，不拉弯底板。
3. 4 颗 M3 从底板顶部沉孔向下穿入新支架，下方加平垫和防松螺母。头部应齐平或低于底板顶面。先装齐再复装上方托架。
4. 松装两个后挡块。在相机底部孔周围放 2 mm 窄环，确认不盖散热孔。
5. 从下方用核对长度的 1/4-20 螺丝和金属大平垫固定相机。槽尺寸 14.8 × 6.8 mm。头侧垫片只减少伸入量。
6. 后挡块轻靠后壳以防转，不能把机身夹变形。复装笔记本托架及全部承力五金。
7. 留 USB 自然松弛段，固定线缆护套。先桌面低位、再替代负载检查；放电脑后检查实际图像无遮挡。

Sequence: remove old sensor hardware and expose the base; check the coupon; attach the adapter before the laptop carrier; fit the narrow ring and verified camera bolt; set the two stops; reassemble and check at low height before using equipment.

## 相机螺丝 / Camera bolt

理论伸入量 `P = L − 6 − 2 − W − S`（mm），其中 L 是头下长度、W 金属垫厚、S 头侧附加垫厚。实际含打印/零件公差。**允许 P 尚未确定，不能用拧到底探深。** 后部 M3 的深度和扭矩不适用于底部螺孔。

The formula is stack-up arithmetic, not a permitted engagement depth. Establish the camera's allowed engagement independently, then measure the actual assembled protrusion.

## 验收 / Acceptance

窄环接触、散热、相机防转、USB 插拔/弯线、真实笔记本重心与刚性、RGB/深度视野仍需实物检查。出现裂纹、层间发白、松动或变形即停用。无长期蠕变、疲劳、热或跌落验证。
