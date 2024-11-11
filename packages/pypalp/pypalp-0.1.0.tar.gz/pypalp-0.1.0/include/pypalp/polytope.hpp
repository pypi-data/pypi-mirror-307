#pragma once

#include <memory>
#include <optional>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <tuple>

#include "pypalp/palp_types.hpp"
#include "pypalp/utils.hpp"

struct Polytope {

  // Everything that is defined in poly.c in PALP
  std::unique_ptr<CWS> CW;
  std::unique_ptr<Weight> W;
  std::unique_ptr<VertexNumList> V;
  std::unique_ptr<EqList> E;
  std::unique_ptr<EqList> DE;
  std::unique_ptr<BaHo> BH;
  std::unique_ptr<VaHo> VH;
  std::unique_ptr<PolyPointList> P;
  std::unique_ptr<PolyPointList> DP;
  std::unique_ptr<FaceInfo> FI;
  std::unique_ptr<PairMatStruct> PM;
  std::unique_ptr<PairMatStruct> DPM;
  std::unique_ptr<C5stats> C5S;

  // Additional data structures
  std::unique_ptr<NormalForm> NF;
  std::unique_ptr<AffineNormalForm> ANF;
  std::unique_ptr<VPermList> VP;

  // Cached results from computations
  bool ran_Find_Equations;
  bool ran_EL_to_PPL;
  bool ran_Sort_VL;
  bool ran_Make_VEPM;
  bool ran_Complete_Poly;
  std::optional<bool> is_ip_;
  std::optional<bool> is_reflexive_;
  std::optional<pybind11::array_t<Long>> vertices_;
  std::optional<pybind11::array_t<Long>> points_;
  std::optional<pybind11::array_t<Long>> normal_form_;
  std::optional<pybind11::array_t<Long>> affine_normal_form_;

  Polytope(std::string const &input) {
    std::atexit(check_final_status);

    inFILE = std::tmpfile();
    outFILE = std::tmpfile();

    std::fwrite(input.c_str(), sizeof(char), input.size(), inFILE);
    std::fputs("\n", inFILE);
    std::rewind(inFILE);

    CW = std::make_unique<CWS>();
    P = std::make_unique<PolyPointList>();

    Read_CWS_PP(CW.get(), P.get());

    std::fclose(inFILE);
    std::fclose(outFILE);
    outFILE = nullptr;

    ran_Find_Equations = false;
    ran_EL_to_PPL = false;
    ran_Sort_VL = false;
    ran_Make_VEPM = false;
    ran_Complete_Poly = false;
  }

  Polytope(pybind11::array_t<int> const &matrix) {
    std::atexit(check_final_status);

    inFILE = std::tmpfile();
    outFILE = std::tmpfile();

    read_into_file(matrix, inFILE);

    CW = std::make_unique<CWS>();
    P = std::make_unique<PolyPointList>();

    Read_CWS_PP(CW.get(), P.get());

    std::fclose(inFILE);
    std::fclose(outFILE);
    outFILE = nullptr;

    ran_Find_Equations = false;
    ran_EL_to_PPL = false;
    ran_Sort_VL = false;
    ran_Make_VEPM = false;
    ran_Complete_Poly = false;
  }

  int dim() { return P->n; }

  std::string repr() {
    std::string output;
    output += "A ";
    output += std::to_string(dim());
    output += "-dimensional PALP polytope";
    return output;
  }

  pybind11::array_t<Long> vertices() {
    if (vertices_.has_value()) {
      return vertices_.value();
    }

    std::atexit(check_final_status);
    outFILE = std::tmpfile();

    if (!V) {
      V = std::make_unique<VertexNumList>();
    }
    if (!E) {
      E = std::make_unique<EqList>();
    }
    if (!DP) {
      DP = std::make_unique<PolyPointList>();
    }

    if (!ran_Find_Equations) {
      is_ip_ = Find_Equations(P.get(), V.get(), E.get());
      ran_Find_Equations = true;
    }
    if (!ran_EL_to_PPL && is_ip_.value()) {
      is_reflexive_ = EL_to_PPL(E.get(), DP.get(), &P->n);
      ran_EL_to_PPL = true;
    }
    if (!ran_Sort_VL) {
      Sort_VL(V.get());
      ran_Sort_VL = true;
    }

    std::fclose(outFILE);
    outFILE = nullptr;

    ssize_t num_vert = V->nv;
    ssize_t dim = P->n;

    auto result = pybind11::array_t<Long>({num_vert, dim});

    auto buf = result.mutable_data();

    for (int i = 0; i < num_vert; i++) {
      for (int j = 0; j < dim; j++) {
        buf[i * dim + j] = P->x[V->v[i]][j];
      }
    }

    vertices_ = std::move(result);

    return vertices_.value();
  }

  pybind11::array_t<Long> points() {
    if (points_.has_value()) {
      return points_.value();
    }

    std::atexit(check_final_status);
    outFILE = std::tmpfile();

    if (!V) {
      V = std::make_unique<VertexNumList>();
    }
    if (!E) {
      E = std::make_unique<EqList>();
    }
    if (!DP) {
      DP = std::make_unique<PolyPointList>();
    }
    if (!PM) {
      PM = std::make_unique<PairMatStruct>();
    }

    if (!ran_Find_Equations) {
      is_ip_ = Find_Equations(P.get(), V.get(), E.get());
      ran_Find_Equations = true;
    }
    if (!ran_EL_to_PPL && is_ip_.value()) {
      is_reflexive_ = EL_to_PPL(E.get(), DP.get(), &P->n);
      ran_EL_to_PPL = true;
    }
    if (!ran_Sort_VL) {
      Sort_VL(V.get());
      ran_Sort_VL = true;
    }
    if (!ran_Make_VEPM) {
      Make_VEPM(P.get(), V.get(), E.get(), PM->data);
      ran_Make_VEPM = true;
    }
    if (!ran_Complete_Poly) {
      Complete_Poly(PM->data, E.get(), V->nv, P.get());
      ran_Complete_Poly = true;
    }

    std::fclose(outFILE);
    outFILE = nullptr;

    ssize_t num_pts = P->np;
    ssize_t dim = P->n;

    auto result = pybind11::array_t<Long>({num_pts, dim});

    auto buf = result.mutable_data();

    for (int i = 0; i < num_pts; i++) {
      for (int j = 0; j < dim; j++) {
        buf[i * dim + j] = P->x[i][j];
      }
    }

    points_ = std::move(result);

    return points_.value();
  }

  bool is_ip() {
    // This is computed in vertices()
    vertices();
    return is_ip_.value();
  }

  bool is_reflexive() {
    // This is computed in vertices()
    vertices();
    // It is not defined if it is not IP
    return is_reflexive_.value_or(false);
  }

  pybind11::array_t<Long> normal_form(bool affine) {
    if (affine and affine_normal_form_.has_value()) {
      return affine_normal_form_.value();
    } else if (!affine and normal_form_.has_value()) {
      return normal_form_.value();
    }

    // Make sure vertices have been computed
    vertices();

    std::atexit(check_final_status);
    outFILE = std::tmpfile();

    if (affine) {
      if (!ANF) {
        ANF = std::make_unique<AffineNormalForm>();
      }
      Make_ANF(P.get(), V.get(), E.get(), ANF->data);

      std::fclose(outFILE);
      outFILE = nullptr;

      ssize_t num_vert = V->nv;
      ssize_t dim = P->n;

      auto result = pybind11::array_t<Long>({num_vert, dim});

      auto buf = result.mutable_data();

      for (int i = 0; i < dim; i++) {
        for (int j = 0; j < num_vert; j++) {
          buf[j * dim + i] = ANF->data[i][j];
        }
      }

      ANF = nullptr;

      affine_normal_form_ = std::move(result);
      return affine_normal_form_.value();
    } else {
      if (!NF) {
        NF = std::make_unique<NormalForm>();
      }
      if (!VP) {
        VP = std::make_unique<VPermList>();
      }
      int SymNum;
      Make_Poly_Sym_NF(P.get(), V.get(), E.get(), &SymNum, VP->data, NF->data,
                       0, 0, 0);

      std::fclose(outFILE);
      outFILE = nullptr;

      ssize_t num_vert = V->nv;
      ssize_t dim = P->n;

      auto result = pybind11::array_t<Long>({num_vert, dim});

      auto buf = result.mutable_data();

      for (int i = 0; i < dim; i++) {
        for (int j = 0; j < num_vert; j++) {
          buf[j * dim + i] = NF->data[i][j];
        }
      }

      NF = nullptr;
      VP = nullptr;

      normal_form_ = std::move(result);
      return normal_form_.value();
    }
  }

  std::vector<std::tuple<std::vector<std::vector<int>>,
                         std::optional<std::vector<std::vector<int>>>,
                         std::optional<int>>>
  nef_partitions(int codim, bool keep_symmetric, bool keep_products,
                 bool keep_projections, bool with_hodge_numbers) {
    // We don't cache any results for this function
    // We take the polytope as an N polytope!

    // Make sure the polytope is reflexive
    if (!is_reflexive()) {
      throw std::runtime_error("the polytope must be reflexive");
    }

    if (POLY_Dmax < (P->n + codim - 1)) {
      throw std::runtime_error(
          "this computation requires POLY_Dmax to be increased");
    }

    points(); // All points MUST be computed

    std::atexit(check_final_status);
    outFILE = std::tmpfile();

    std::vector<std::tuple<std::vector<std::vector<int>>,
                           std::optional<std::vector<std::vector<int>>>,
                           std::optional<int>>>
        nef_parts;

    // Start algorithm in Make_E_Poly

    Flags NEF_F;
    NEF_F.Sym = !keep_symmetric;
    NEF_F.Dir = keep_products;
    NEF_F.Proj = keep_projections;
    NEF_F.t = 0;
    NEF_F.S = 0;
    NEF_F.T = 0;

    auto NEF_EP = std::make_unique<EPoly>();
    auto NEF_PTL = std::make_unique<PartList>();
    auto NEF_P_D = std::make_unique<PolyPointList>();
    auto NEF_P_N = std::make_unique<PolyPointList>();
    auto NEF_V_D = std::make_unique<VertexNumList>();
    auto NEF_V_N = std::make_unique<VertexNumList>();
    auto NEF_E_D = std::make_unique<EqList>();
    auto NEF_E_N = std::make_unique<EqList>();
    auto NEF_DP = std::make_unique<PolyPointList>();
    auto NEF_DV = std::make_unique<VertexNumList>();
    auto NEF_DE = std::make_unique<EqList>();

    auto NEF_P = std::make_unique<PolyPointList>(*P);
    auto NEF_E = std::make_unique<EqList>(*E);
    auto NEF_V = std::make_unique<VertexNumList>(*V);
    Make_Dual_Poly(NEF_P.get(), NEF_V.get(), NEF_E.get(), NEF_DP.get());
    Find_Equations(NEF_DP.get(), NEF_DV.get(), NEF_DE.get());
    Sort_PPL(NEF_DP.get(), NEF_DV.get());

    // Not used, but they need to be initialized
    time_t Tstart = time(NULL);
    clock_t Cstart = clock();

    NEF_Flags NF;
    NF.Sym = NEF_F.Sym;
    NF.noconvex = 0;
    NF.Test = 0;
    NF.Sort = 1;

    part_nef(NEF_P.get(), NEF_V.get(), NEF_E.get(), NEF_PTL.get(), &codim, &NF);

    for (int n = 0; n < NEF_PTL->n; n++) {
      Make_Gore_Poly(NEF_P.get(), NEF_DP.get(), NEF_P_D.get(), NEF_P_N.get(),
                     NEF_V.get(), NEF_PTL.get(), &codim, &n);
      NEF_PTL->Proj[n] = Remove_Proj(NEF_P_D.get(), &codim);
      NEF_PTL->DProj[n] = Remove_Proj(NEF_P_N.get(), &codim);
      Find_Equations(NEF_P_D.get(), NEF_V_D.get(), NEF_E_D.get());
      Find_Equations(NEF_P_N.get(), NEF_V_N.get(), NEF_E_N.get());
      Sort_PPL(NEF_P_N.get(), NEF_V_N.get());

      if (((!NEF_PTL->Proj[n]) || NEF_F.Proj) &&
          ((!NEF_PTL->DirProduct[n]) || NEF_F.Dir)) {
        Make_EN(NEF_P_D.get(), NEF_V_D.get(), NEF_E_N.get(), &codim);
        Compute_E_Poly(NEF_EP.get(), NEF_P_D.get(), NEF_V_D.get(),
                       NEF_E_D.get(), NEF_P_N.get(), NEF_V_N.get(),
                       NEF_E_N.get(), &codim, &NEF_F, &Tstart, &Cstart);

        // Output
        std::optional<int> chi;
        int D = (NEF_P_D->n + 1);
        int dim = (NEF_P->n - codim);
        int h[POLY_Dmax][POLY_Dmax] = {{0}, {0}};
        int S[VERT_Nmax];

        if (with_hodge_numbers) {
          chi = Make_Mirror(NEF_EP.get(), h, D, dim);
        }

        if ((NEF_P_D->np - codim) > VERT_Nmax) {
          std::cerr << "this nef partition requires VERT_Nmax to be increased"
                    << std::endl;
          continue;
        }

        for (int i = 0; i < (NEF_P_D->np - codim); i++) {
          S[i] = 0;
          for (int j = 0; j < (codim - 1); j++) {
            if (NEF_P_D->x[i][j]) {
              S[i] = (j + 1);
            }
          }
        }

        std::vector<std::vector<int>> nef_part;
        std::vector<int> part;

        for (int i = 0; i < codim; i++) {
          for (int k = 0; k < NEF_PTL->nv; k++) {
            if (NEF_PTL->S[n][k] == i) {
              part.push_back(k);
            }
          }
          nef_part.push_back(std::move(part));
        }

        std::optional<std::vector<std::vector<int>>> hodge_numbers;
        if (with_hodge_numbers) {
          hodge_numbers = std::vector<std::vector<int>>(dim + 1);
          for (int i = 0; i < dim + 1; i++) {
            for (int j = 0; j < dim + 1; j++) {
              int ii = (i == dim ? 0 : i);
              int jj = (j == dim ? 0 : j);
              hodge_numbers.value()[i].push_back(h[ii][jj]);
            }
          }
        }

        nef_parts.push_back(std::make_tuple(std::move(nef_part),
                                            std::move(hodge_numbers), chi));
      }
    }

    // End algorithm in Make_E_Poly

    std::fclose(outFILE);
    outFILE = nullptr;

    return nef_parts;
  }
};
