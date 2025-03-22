#include "../include/utilities.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <memory>
#include <iomanip>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "utilities.hpp"
using namespace std;
namespace py = pybind11;

ODESolver::ODESolver() : mA(1.0), mB(1.0),m_add(1.0), k_e(1.0), C1(1.0), C2(1.0), F(1.0), omega(1.0), rho0(1.0), g(9.81), H(1.0), h(1.0), R(1.0), xA0(1.0), xA1(0.0) {}

ODESolver::ODESolver(const ODESolver& other) : mA(other.mA), mB(other.mB), k_e(other.k_e), C1(other.C1), C2(other.C2), F(other.F), omega(other.omega), rho0(other.rho0), g(other.g), H(other.H), h(other.h), R(other.R), xA0(other.xA0), xA1(other.xA1) {}

ODESolver::~ODESolver() {}

ODESolver &ODESolver::operator=(const ODESolver &other)
{
    //自赋值检查
    if (this == &other) return *this;

    mA = other.mA;
    mB = other.mB;
    m_add = other.m_add;
    k_e = other.k_e;
    C1 = other.C1;
    C2 = other.C2;
    F = other.F;
    omega = other.omega;
    rho0 = other.rho0;
    g = other.g;
    H = other.H;
    h = other.h;
    R = other.R;
    xA0 = other.xA0;
    xA1 = other.xA1;

    return *this;
}

void ODESolver::setParameters(double mA, double mB, double m_add, double k_e, double C1, double C2, double F, double omega, double rho0, double g, double H, double h, double R, double xA0, double xA1)
{
    this->mA = mA;
    this->mB = mB;
    this->m_add = m_add;
    this->k_e = k_e;
    this->C1 = C1;
    this->C2 = C2;
    this->F = F;
    this->omega = omega;
    this->rho0 = rho0;
    this->g = g;
    this->H = H;
    this->h = h;
    this->R = R;
    this->xA0 = xA0;
    this->xA1 = xA1;
}

double ODESolver::computeBuoyancyTerm(double xA)
{
    if (xA >= xA0) {
        return rho0 * g * M_PI * R * R * (H + h * (xA - xA0) / (xA1 - xA0));
    } else {
        return rho0 * g * M_PI * R * R * H;
    }
}

void ODESolver::systemDynamics(const vector<double> &state, vector<double> &dstate_dt, double t, bool linear_damping)
{
    double xA = state[0];
    double xB = state[1];
    double vA = state[2];
    double vB = state[3];

    double buoyancyTerm = computeBuoyancyTerm(xA);
    double rel_vel = vA - vB;

    dstate_dt[0] = vA;
    dstate_dt[1] = vB;

    if (linear_damping) {
        dstate_dt[2] = (F * cos(omega * t) - C1 * rel_vel - C2 * vA - k_e * (xA - xB) - buoyancyTerm) / (mA + m_add);
        dstate_dt[3] = (-k_e * (xB - xA) - C1 * rel_vel) / mB;
    } else {
        // 非线性阻尼情况
        double damping_force = C1 * pow(fabs(rel_vel), 0.5) * rel_vel;
        dstate_dt[2] = (F * cos(omega * t) - damping_force - C2 * vA - k_e * (xA - xB) - buoyancyTerm) / (mA + m_add);
        dstate_dt[3] = (-k_e * (xB - xA) - damping_force) / mB;
    }
}

vector<vector<double>> ODESolver::runge_kutta_4th(const vector<double> &initialState, double t0, double t_end, double h, bool linear_damping)
{
    vector<vector<double>> results;
    int numSteps = static_cast<int>((t_end - t0) / h);
    vector<double> currentState = initialState;

    results.push_back(currentState);

    for (int i = 0; i < numSteps; ++i) {
        double t = t0 + i * h;

        vector<double> k1(currentState.size());
        vector<double> k2(currentState.size());
        vector<double> k3(currentState.size());
        vector<double> k4(currentState.size());

        systemDynamics(currentState, k1, t, linear_damping);

        vector<double> tempState2 = currentState;
        for (size_t j = 0; j < tempState2.size(); ++j) {
            tempState2[j] += 0.5 * h * k1[j];
        }
        systemDynamics(tempState2, k2, t + 0.5 * h, linear_damping);

        vector<double> tempState3 = currentState;
        for (size_t j = 0; j < tempState3.size(); ++j) {
            tempState3[j] += 0.5 * h * k2[j];
        }
        systemDynamics(tempState3, k3, t + 0.5 * h, linear_damping);

        vector<double> tempState4 = currentState;
        for (size_t j = 0; j < tempState4.size(); ++j) {
            tempState4[j] += h * k3[j];
        }
        systemDynamics(tempState4, k4, t + h, linear_damping);

        vector<double> newState(currentState.size());
        for (size_t j = 0; j < newState.size(); ++j) {
            newState[j] = currentState[j] + (h / 6.0) * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]);
        }

        currentState = newState;
        results.push_back(currentState);
    }

    return results;
}

void ODESolver::output(const vector<vector<double>>& results)
{
    cout << "时间\t浮子位移\t振子位移\t浮子速度\t振子速度" << endl;
    for (size_t i = 0; i < results.size(); ++i) {
        double t = i * h;
        cout << t << "\t" << results[i][0] << "\t" << results[i][1] << "\t" << results[i][2] << "\t" << results[i][3] << endl;
    }
}

double ODESolver::calculatePower(const vector<vector<double>> &results, double C1, bool linear_damping)
{
    double power = 0.0;
    for (const auto& state : results) {
        double rel_vel = state[2] - state[3];
        if (linear_damping) {
            power += C1 * rel_vel * rel_vel;
        } else {
            power += C1 * pow(fabs(rel_vel) + 1e-10, 0.5) * rel_vel * rel_vel;
        }
    }
    return power / results.size();
}

void ODESolver::optimizeDamping()
{
    double max_power = 0.0;
    double optimal_C1 = 0.0;
    double optimal_alpha = 0.0;

    vector<double> initialState = {0.0, 0.0, 0.0, 0.0};
    double t0 = 0.0;
    double t_end = 40.0 * 2 * M_PI / omega;
    double h = 0.2;

    for (double C1 = 0.0; C1 <= 100000.0; C1 += 1000.0) {
        for (double alpha = 0.0; alpha <= 1.0; alpha += 0.1) {
            this->C1 = C1;
            vector<vector<double>> results = runge_kutta_4th(initialState, t0, t_end, h, false);
            double power = calculatePower(results, C1, false);
            if (power > max_power) {
                max_power = power;
                optimal_C1 = C1;
                optimal_alpha = alpha;
            }
        }
    }

    cout << "最大输出功率: " << max_power << " W\n";
    cout << "最优阻尼系数: " << optimal_C1 << " N·s/m\n";
    cout << "最优幂指数: " << optimal_alpha << "\n";
}