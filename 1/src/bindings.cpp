#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/utilities.hpp"

namespace py = pybind11;

PYBIND11_MODULE(ODESolver, m) {
    py::class_<ODESolver>(m, "ODESolver")
        .def(py::init<>())
        .def("runge_kutta_4th", &ODESolver::runge_kutta_4th,
             py::arg("initialState"), py::arg("t0"), py::arg("t_end"), py::arg("dt"))
        .def("setParameters", &ODESolver::setParameters)
        .def("computeBuoyancyTerm", &ODESolver::computeBuoyancyTerm)
        .def("systemDynamics", &ODESolver::systemDynamics)
        .def("output", &ODESolver::output);
}