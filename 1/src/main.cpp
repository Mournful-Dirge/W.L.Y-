#include "../include/utilities.hpp"
#include <vector>
#include <cmath>

int main() {
    ODESolver solver;

    // 设置参数
    solver.setParameters(
        4866,   // mA 浮子质量（kg）
        2433,   // mB 振子质量（kg）
        1335.535, //m_add 垂荡惯性附加质量（kg）
        80000.0,  // k_e 弹簧刚度 (N/m)
        10000.0,   // C1 直线阻尼系数（N·s/m）
        656.3616,    // C2 垂荡兴波阻尼系数 (N·s/m)
        6250.0,  // F 垂荡激励力振幅 (N)
        1.4005,    // omega 入射波浪频率 (s-1)
        1025.0, // rho0 海水的密度 (kg/m3)
        9.81,   // g 重力加速度 (m/s2)
        0.5,    // H
        0.3,    // h
        0.1,    // R
        0.2,    // xA0
        -0.1    // xA1
    );

    // 初始状态：[xA, xB, vA, vB]
    vector<double> initialState = {0.0, 0.0, 0.0, 0.0};

    // 时间范围和步长
    double t0 = 0.0;
    double t_end = 40.0 * 2 * M_PI / 1.4005;
    double h = 0.2;

    // 问题一：线性阻尼
    vector<vector<double>> results1 = solver.runge_kutta_4th(initialState, t0, t_end, h, true);
    solver.output(results1);

    // 问题一：非线性阻尼
    vector<vector<double>> results2 = solver.runge_kutta_4th(initialState, t0, t_end, h, false);
    solver.output(results2);

    // 问题二：优化阻尼系数
    solver.optimizeDamping();

    return 0;
}