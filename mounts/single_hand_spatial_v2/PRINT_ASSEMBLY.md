# Print and assembly / 打印与装配

## 切片 / Slicing

原 PLA 原型起点：0.4 mm 喷嘴、0.2 mm 层高、5–6 道墙、上下至少6层、40–50% 填充；接头/孔位/握柄法兰附近可局部实心。尚未验证具体打印机、材料或强度。

STL 已落到 Z=0。主框架背面朝床，相机桥两侧检查局部支撑；握柄、叉架、点座平放；U 件底部朝床，开口朝上。180 mm 平台也须加上裙边/黏附边重新检查范围。

**U 件是 44 × 32 × 40 mm。两组 Ø4.5 mm 通道轴线互相垂直，但分层错开，不相交。** 不能沿一组孔清通另一组。横向孔桥接或支撑要在切片预览中检查可拆性；不要把整个 U 槽填满难取支撑。先用同工艺局部试验，拆不出时停下改切片或结构。

The two perpendicular Ø4.5 mm hole families are separate passages. One does not provide access to clear the other. Inspect support accessibility before printing and never force or hammer hardware through trapped support.

## 装配 / Assembly

1. 去毛刺并用散装机器螺钉轻试通孔；Ø3.4/Ø4.5 是间隙孔，不是打印螺纹。
2. 握柄贴合主框架，用4颗名义 M4×30 连接。所有垫圈/螺母按实际厚度检查。
3. U 件贴主框架后侧，用4颗轴向 M4 连接；长度须按 BOM 复核。
4. 10 mm 叉架插入名义10.4 mm槽并坐到底部台阶；两侧对称用硬薄片消隙，不垫高台阶。对孔后装4颗横向 M4，检查完整啮合和突出净空。
5. 安装5个点座，粘贴面保持平整清洁。按粘胶厂商规定固化球形 marker。
6. 相机最后安装。M3×10 穿过名义7 mm打印路径和约1 mm硬垫后，实测接触凸台外突出1.8–2.2 mm且严格小于3 mm。不靠拧到底探深。
7. 交替轻紧，出现开裂、发白、层间变形就停。给USB留自然弯曲，用扎带卸力；低位空载和轻缓握持检查。

Assemble the grip, axial U joint, seated/shimmed depth fork, and pads, then the camera. Do not pull misaligned parts together with screws. Check each fastener stack-up, camera screw protrusion and cable path before loading.

## 动捕与使用 / Tracking and use

贴面中心坐标与法向见 `QA.json`；实际球心 = 贴面中心 + 实测底座到球心距离 × 朝外法向。理论点位不能直接替代刚体标定。工作姿态至少要可靠识别3个不共线点；系统要求更高时以系统为准。朝向分散不等于360°可见。

检查快速转动、俯仰时的遮挡/误匹配、相机主动红外与动捕系统干扰、热变形及线缆扯动。相机或点座拆装、重新粘球后复核外参。

Measure ball centers and validate visibility, thermal behavior, interference and calibration on the real system. No load, fatigue, drop or tracking certification is claimed.
