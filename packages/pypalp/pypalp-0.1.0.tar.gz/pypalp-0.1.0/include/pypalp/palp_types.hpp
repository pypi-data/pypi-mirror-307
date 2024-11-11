#pragma once

extern "C" {
#include "Global.h"
#include "LG.h"
#include "Nef.h"
}

// We we reexport some types used in PALP and wrap others into structs to make
// them more convenient.

struct PairMatStruct {
  PairMat data;
};

struct VPermList {
  int data[SYM_Nmax][VERT_Nmax];
};

struct NormalForm {
  Long data[POLY_Dmax][VERT_Nmax];
};

struct AffineNormalForm {
  Long data[POLY_Dmax][VERT_Nmax];
};
