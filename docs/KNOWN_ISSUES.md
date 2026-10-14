# Known issues / 已知问题

## 1. 旧实装版本不明 / Prior build version is unknown

旧支架曾完成装配，也遇到过M3×30偏短、内部支撑难拆和强行加工的问题。无法确认对应本库哪份几何或哪种接头，因此不能据此把任何一款标成“实测通过”，也不能套用同一修复规格。

A prior build's assembly and fastener difficulties have not been linked to an exact source snapshot. They are cautionary observations, not validation of this repository. Hammering or self-tapping modifications are not an approved assembly procedure; inspect altered load-bearing parts and replace damaged ones.

## 2. 单手 v2 横接螺栓余量小 / Limited v2 transverse bolt allowance

U件外廓44 × 32 × 40 mm。原BOM的横向M4×50按44 mm夹持、两片共2 mm垫和3.2 mm普通螺母，仅约0.8 mm名义余量；制造公差、垫圈和螺母标准变化会吃掉余量。轴向连接也须核实实际厚度。

This release does not establish a replacement length. Measure full nut engagement and protrusion clearance with the actual hardware. A geometrically clear nominal shaft path does not prove usable thread engagement, tool access or tightening safety.

## 3. 支撑拆除 / Support removal

U件两组Ø4.5 mm通道方向垂直、位置错开，不是互通十字孔。不得期望从另一方向掏通。B1的斜撑/上夹臂、螺母窝也需切片级拆支撑检查。局部试打后仍不易拆时，需重新设计或换工艺；本次发布没有完成这些几何修改。

Perpendicular hole axes do not imply intersecting passages. Check removal access before printing; forcing hardware through support can crack or distort the part.

## 4. 相机紧固 / Camera attachment

单手/B1使用后双M3：实际突出目标1.8–2.2 mm且严格小于3 mm，不能盲信名义M3×10。双手用底部1/4-20：允许伸入量未明确，须另核；后M3的上限不可借用。

Rear M3 limits and bottom 1/4-20 requirements are different. Do not bottom a screw out to discover the permissible depth. Do not use self-tapping screws in camera threads.

## 5. B1 实机适配未完成 / B1 physical fit is unresolved

电脑包络、12 mm底座和110°开屏角是示意。两夹距离/位置需改CAD重打；只有厚度用M5螺杆调节。端口、风口、硬边、脚垫、上盖视野、夹力、打滑与漆面保护都未实物通过。禁止提支架搬电脑、装夹后合盖或直接压在螺杆上平放。

No physical acceptance test has been completed on the intended laptop. Keep it hand-supported; do not treat the bracket as a carrying handle.

## 6. 性能未认证 / Performance remains unvalidated

全部设计缺额定载荷、长期蠕变、疲劳、跌落及完整温升试验。动捕需真实球心、工作姿态可见性、红外干扰与相机外参验证。STL封闭、BRep有效或无名义体积碰撞均不能替代这些测试。
