from ODESolver import ODESolver
from helpers import show
import pandas as pd
import sys
sys.path.append("~/文档/GitHub/W.L.Y-/1/build")

# 创建 ODESolver 实例
solver = ODESolver()

# 设置参数
solver.setParameters(
        4866,   # mA 浮子质量（kg）
        2433,   # mB 振子质量（kg）
        80000.0,  # k_e 弹簧刚度 (N/m)
        10.0,   # C1
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
p = 0.2    #步长

# 初始状态
initialState = [1.0, 1.0, 0.0, 0.0]

# 运行 Runge-Kutta 4th 方法
results = solver.runge_kutta_4th(initialState, t0, t_end, p)

df = pd.DataFrame(results, columns=['时间', '浮子位移', '振子位移', '浮子速度', '振子速度'])

# 输出结果
solver.output(results)
df.to_excel('results.xlsx', index=False)
show(results, p)