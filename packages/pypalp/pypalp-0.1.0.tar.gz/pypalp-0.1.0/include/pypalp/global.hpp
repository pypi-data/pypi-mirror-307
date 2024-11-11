#pragma once

#include <cstdio>

// PALP uses some global variables (unfortunately), so we define them here.

FILE *inFILE = nullptr, *outFILE = nullptr;

extern "C" {

// Defined in Vertex.c
void Sort_PPL(PolyPointList *_P, VertexNumList *_V);

// Defined in E_Poly.c
void Compute_E_Poly(EPoly *_EP, PolyPointList *_P_D, VertexNumList *_V_D,
                    EqList *_E_D, PolyPointList *_P_N, VertexNumList *_V_N,
                    EqList *_E_N, int *_codim, Flags *_F, time_t *_Tstart,
                    clock_t *_Cstart);
void Make_Gore_Poly(PolyPointList *_P, PolyPointList *_DP, PolyPointList *_P_D,
                    PolyPointList *_P_N, VertexNumList *_V, PartList *_PTL,
                    int *_codim, int *_n);
int Remove_Proj(PolyPointList *_P, int *_codim);
void Make_EN(PolyPointList *_P, VertexNumList *_V, EqList *_EN, int *_codim);
int Make_Mirror(EPoly *_EP, int h[][POLY_Dmax], int D, int dim);
}
