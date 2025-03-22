import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

# 设置全局字体和样式
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['lines.linewidth'] = 2

def show(results, dt):
    """
    绘制 ODESolver 计算结果的位移和速度随时间变化的图表。

    参数：
    results (list): ODESolver 计算结果，格式为列表的列表
    dt (float): 时间步长
    """
    title_prefix = "System Dynamic"
    
    # 提取时间序列
    time = [i * dt for i in range(len(results))]
    
    # 提取位移和速度数据
    buoy_displacement = [result[0] for result in results]
    oscillator_displacement = [result[1] for result in results]
    buoy_velocity = [result[2] for result in results]
    oscillator_velocity = [result[3] for result in results]

    # 创建位移图
    fig, ax = plt.subplots()
    ax.plot(time, buoy_displacement, label='Buoy Displacement', color='blue', marker='o', markevery=0.1)
    ax.plot(time, oscillator_displacement, label='Oscillator Displacement', color='red', marker='s', markevery=0.1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Displacement (m)')
    ax.set_title(f'Variation of {title_prefix} Displacement with Time')
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.xaxis.grid(False)  # 只显示水平网格线
    plt.tight_layout()
    plt.show()

    # 创建速度图
    fig, ax = plt.subplots()
    ax.plot(time, buoy_velocity, label='Buoy Velocity', color='blue', marker='o', markevery=0.1)
    ax.plot(time, oscillator_velocity, label='Oscillator Velocity', color='red', marker='s', markevery=0.1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Velocity (m/s)')
    ax.set_title(f'Variation of {title_prefix} Velocity with Time')
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.xaxis.grid(False)  # 只显示水平网格线
    plt.tight_layout()
    plt.show()
    
# 可视化功率分布
def visualize_power_distribution(solver):
    # 参数范围
    C1_values = np.arange(0, 100001, 1000)
    alpha_values = np.arange(0, 1.1, 0.1)
    C1_mesh, alpha_mesh = np.meshgrid(C1_values, alpha_values, indexing='ij')
    power_mesh = np.zeros_like(C1_mesh, dtype=np.float64) 

    # 初始状态
    initialState = [0.0, 0.0, 0.0, 0.0]
    t0 = 0.0
    t_end = 40.0 * 2 * np.pi / solver.getOmega()
    h_step = 0.2

    # 计算每个参数组合的功率
    for i, C1 in enumerate(C1_values):
        for j, alpha in enumerate(alpha_values):
            solver.setC1(C1)
            results = solver.runge_kutta_4th(initialState, t0, t_end, h_step, False)
            power = solver.calculatePower(results, C1, False)
            if np.isnan(power):
                print(f"Warning: NaN value encountered at C1={C1}, alpha={alpha}")
                power = 0.0
            power_mesh[i, j] = power

    # 绘制3D曲面图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(C1_mesh, alpha_mesh, power_mesh, cmap='viridis')
    ax.set_xlabel('Damping Coefficient C1 (N·s/m)')
    ax.set_ylabel('Exponent alpha')
    ax.set_zlabel('Output Power (W)')
    ax.set_title('Output Power Distribution')
    plt.show()