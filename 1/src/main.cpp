#include "../include/utilities.hpp"
using namespace std;

int main() {
    ODESolver solver;

    // 设置参数
    solver.setParameters(
        10.0,   // mA
        5.0,    // mB
        200.0,  // k_e
        10.0,   // C1
        5.0,    // C2
        100.0,  // F
        2.0,    // omega
        1000.0, // rho0
        9.81,   // g
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
    double t_end = 10.0;
    double h = 0.01;

    // 求解
    vector<vector<double>> results = solver.runge_kutta_4th(initialState, t0, t_end, h);

    // 输出结果
    solver.output(results);

    return 0;
}