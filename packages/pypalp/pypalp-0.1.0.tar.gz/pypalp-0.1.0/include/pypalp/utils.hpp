#pragma once

#include <iostream>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include "pypalp/global.hpp"

// PALP exits if there's any error. This would cause the Python interpreter to
// exit, so instead we check if outFIlE was closed properly and throw an
// exception otherwise.
void check_final_status() {
  if (outFILE != nullptr) {
    std::cout << outFILE << std::endl;
    char buffer[1024] = {};
    std::rewind(outFILE);
    fgets(buffer, sizeof(buffer), outFILE);
    std::cout << "PALP output:\n " << buffer << std::endl;
    std::fclose(outFILE);
    if (inFILE) {
      std::fclose(inFILE);
    }
    throw std::runtime_error("PALP error");
  }
}

void read_into_file(pybind11::array_t<int> const &matrix, std::FILE *file) {
  if (!file) {
    throw std::runtime_error("Invalid file");
  }

  pybind11::buffer_info buf = matrix.request();

  if (buf.ndim == 1) { // Input as weight system
    int *ptr = static_cast<int *>(buf.ptr);
    ssize_t len = buf.shape[0];

    char buffer[32];
    for (ssize_t i = 0; i < len; i++) {
      std::snprintf(buffer, sizeof(buffer), "%d ", ptr[i]);
      std::fputs(buffer, file);
    }
    std::fputs("\n", file);
  } else if (buf.ndim == 2) { // Input as matrix of points
    int *ptr = static_cast<int *>(buf.ptr);
    ssize_t rows = buf.shape[0];
    ssize_t cols = buf.shape[1];

    char buffer[32];
    std::snprintf(buffer, sizeof(buffer), "%ld %ld\n", rows, cols);
    std::fputs(buffer, file);

    for (ssize_t i = 0; i < rows; i++) {
      for (ssize_t j = 0; j < cols; j++) {
        std::snprintf(buffer, sizeof(buffer), "%d ", ptr[i * cols + j]);
        std::fputs(buffer, file);
      }
      std::fputs("\n", file);
    }
  } else {
    throw std::runtime_error("Input should be a vector or matrix");
  }
  std::rewind(file);
}
