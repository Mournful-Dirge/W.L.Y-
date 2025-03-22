#include <vector>
using namespace std;

#ifndef UTILITIES_H
#define UTILITIES_H

class ODESolver {
private:
    double mA; // 浮子质量
    double mB; // 振子质量
    double m_add; //垂荡惯性附加质量
    double k_e; // 弹簧刚度
    double C1; // 阻尼系数
    double C2; // 阻尼系数
    double F; // 波浪激励力幅值
    double omega; // 波浪频率
    double rho0; // 海水密度
    double g; // 重力加速度
    double H; // 浮子圆柱部分高度
    double h; // 浮子圆锥部分高度
    double R; // 浮子半径
    double xA0; // 浮子圆柱部分完全浸入海水时的浮子位移
    double xA1; // 浮子圆柱部分完全露出海水时的浮子位移
public:
    // 默认构造函数
    ODESolver();
    // 拷贝构造函数
    ODESolver(const ODESolver& other);
    // 析构函数
    ~ODESolver();
    // 赋值运算符重载
    ODESolver& operator=(const ODESolver& other);
    //设置参数
    void setParameters(double mA, double mB, double m_add, double k_e, double C1, double C2, double F, double omega, double rho0, double g, double H, double h, double R, double xA0, double xA1);
    // 计算浮力项
    double computeBuoyancyTerm(double xA);
    // 解微分方程函数
    void systemDynamics(const vector<double>& state, vector<double>& dstate_dt, double t, bool linear_damping);
    // 四阶龙格-库塔法求解
    vector<vector<double>> runge_kutta_4th(const vector<double>& initialState, double t0, double t_end, double h, bool linear_damping);
    // 计算输出功率
    double calculatePower(const vector<vector<double>>& results, double C1, bool linear_damping);
    // 优化阻尼系数
    void optimizeDamping();
    // 输出结果
    void output (const vector<vector<double>>& results);
    
    double getOmega() const { return omega; }
    void setOmega(double omega) { this->omega = omega; }
    double getC1() const { return C1; }
    void setC1(double C1) { this->C1 = C1; }
};

#endif //UTILITIES_H