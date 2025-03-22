from ODESolver import ODESolver
from helpers import show
from helpers import visualize_power_distribution
import numpy as np
import pandas as pd
import sys
sys.path.append("~/文档/GitHub/W.L.Y-/1/build")

# 创建 ODESolver 实例
solver = ODESolver()

# 设置参数
solver.setParameters(
        4866.0,   # mA 浮子质量（kg）
        2433.0,   # mB 振子质量（kg）
        1335.535,    #m_add 振荡附加质量（kg）
        80000.0,  # k_e 弹簧刚度 (N/m)
        100.0,   # C1
        656.3616,    # C2 垂荡兴波阻尼系数 (N·s/m)
        6250.0,  # F 垂荡激励力振幅 (N)
        1.4005,    # omega 入射波浪频率 (s-1)
        1025.0, # rho0 海水的密度 (kg/m3)
        9.81,   # g 重力加速度 (m/s2)
        0.5,    # H
        0.3,    # h
        0.1,    # R
        0.2,    # xA0
        -0.1    # xA1
)

t0 = 0.0
t_end = 10.0
h_step = 0.2  # 步长

# 初始状态
initialState = [1.0, 1.0, 0.0, 0.0]

# 运行 Runge-Kutta 4th 方法
results = solver.runge_kutta_4th(initialState, t0, t_end, h_step, False)

# 将结果转换为DataFrame
time = np.arange(0, t_end + h_step, h_step)
df = pd.DataFrame({
    '时间': time[:len(results)],
    '浮子位移': [result[0] for result in results],
    '振子位移': [result[1] for result in results],
    '浮子速度': [result[2] for result in results],
    '振子速度': [result[3] for result in results]
})

# 输出结果
solver.output(results)
df.to_excel('results.xlsx', index=False)
show(results, h_step)

# 设置参数（问题二中的参数）
solver.setParameters(
    4866.0,  # 浮子质量（kg）
    2433.0,  # 振子质量（kg）
    100.0,  # 垂荡惯性附加质量
    80000.0,  # 弹簧刚度 (N/m)
    10.0,  # 阻尼系数
    656.3616,  # 垂荡兴波阻尼系数 (N·s/m)
    6250.0,  # 垂荡激励力振幅 (N)
    1.4005,  # 入射波浪频率 (s-1)
    1025.0,  # 海水的密度 (kg/m3)
    9.81,  # 重力加速度 (m/s2)
    0.5,  # 浮子圆柱部分高度
    0.3,  # 浮子圆锥部分高度
    0.1,  # 浮子半径
    0.2,  # 浮子圆柱部分完全浸入海水时的浮子位移
    -0.1  # 浮子圆柱部分完全露出海水时的浮子位移
)

# 调用优化函数
solver.optimizeDamping()

# 可视化功率分布
visualize_power_distribution(solver)