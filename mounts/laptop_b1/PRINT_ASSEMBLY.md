# Print and assembly / 打印与装配

完整中文步骤、参数与接触检查见 [原型说明](README_先读.txt) 与 [详细手册文字](docs/B1_原手册完整文字.txt)。

## Before printing / 打印前

1. 量两个候选夹点的底座厚度、顶部硬边宽度和底面平坦宽度；闭盖厚度不能替代。
2. 拍左右侧和底面带标尺照片，核接口、真实插头、风口、脚垫、转轴与开屏角。
3. 先打印单夹试片及一个压脚，用真实垫和五金轻试；手托住电脑。
4. 软垫须整面落在硬边，不压键帽、触控板、缝隙或薄弱悬空处。接触不明时停下改参数。

Measure the actual base at both clamp stations, including hard contact lands and all keep-out areas. Print and test the coupon first. Do not use a soft pad to hide an unsuitable surface.

## Printing / 切片

主体153.5 × 173 × 134 mm。给173 mm边加两侧3 mm黏附边后已到179 mm，须核实际可用打印范围，不可整体缩放。STL已按下夹臂朝床落到Z=0。

空间斜撑和上夹臂需要检查支撑；螺母窝与螺杆孔避免不可拆支撑，切片前看侧向取出路径。压脚盲孔朝下，小孔顶可先试桥接。原设计是PLA试样，没有材料强度或热蠕变保证。

The model's bed fit does not establish reliable printing. Verify all support-removal paths, bridge quality, hole sizes and joint integrity on the actual printer.

## Assembly / 装配

- M5螺母自然落入下夹臂上方六角窝；不要锤敲。压脚盲孔朝螺杆，软垫朝电脑。
- 两夹交替手指轻紧，没有已验证夹力或扭矩，不能用工具加力。压脚松夹会掉落，接住它。
- 相机最后装。后双M3孔距45 mm，名义路径7 mm。M3×10配约1 mm硬垫，安装前实测突出1.8–2.2 mm且严格 <3 mm。不要拧到底探深。
- 0.4 N·m 的厂家相机固定数值不是电脑夹或PLA安全扭矩。
- 给USB自然松弛段，线固定在支架而不是屏幕。插头示意盒16 × 20 × 35 mm不保证实际避让。

## Use boundaries / 使用边界

Always support the laptop with both hands. Never carry or suspend it by this bracket. Do not close the lid while mounted or place the laptop directly on the bracket, knobs or screws; remove the bracket before setting it down normally.

光轴朝 -Y，即屏幕后方环境；以真实开屏角检查RGB、红外、深度画面是否被上盖挡住。出现滑动、开裂、壳体压痕、键帽受压、异常发热、线缆受拉或变形即停用。

The five marker centers in CAD describe adhesive faces, not calibrated ball centers. Measure real markers, validate the capture volume and calibrate extrinsics. Digital collision-free results do not validate laptop shell pressure, friction, fatigue or tracking performance.
