#include <pybind11/pybind11.h>

#include "pypalp/polytope.hpp"

PYBIND11_MODULE(pypalp, m) {
  pybind11::class_<Polytope>(m, "Polytope")
      .def(pybind11::init<std::string const &>())
      .def(pybind11::init<pybind11::array_t<int> const &>())
      .def("__repr__", &Polytope::repr)
      .def("dim", &Polytope::dim)
      .def("vertices", &Polytope::vertices)
      .def("points", &Polytope::points)
      .def("is_ip", &Polytope::is_ip)
      .def("is_reflexive", &Polytope::is_reflexive)
      .def("normal_form", &Polytope::normal_form,
           pybind11::arg("affine") = false)
      .def("nef_partitions", &Polytope::nef_partitions,
           pybind11::arg("codim") = 2, pybind11::arg("keep_symmetric") = false,
           pybind11::arg("keep_products") = false,
           pybind11::arg("keep_projections") = false,
           pybind11::arg("with_hodge_numbers") = true);
}
