#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/utilities.hpp"

namespace py = pybind11;

PYBIND11_MODULE(ODESolver, m) {
    py::class_<ODESolver>(m, "ODESolver")
        .def(py::init<>())
        .def("setParameters", &ODESolver::setParameters)
        .def("runge_kutta_4th", &ODESolver::runge_kutta_4th,
             py::arg("initialState"), py::arg("t0"), py::arg("t_end"), py::arg("h"), py::arg("linear_damping"))
        .def("output", &ODESolver::output)
        .def("optimizeDamping", &ODESolver::optimizeDamping)
        .def("getOmega", &ODESolver::getOmega)
        .def("setOmega", &ODESolver::setOmega)
        .def("getC1", &ODESolver::getC1)
        .def("setC1", &ODESolver::setC1)
        .def("calculatePower", &ODESolver::calculatePower);
}