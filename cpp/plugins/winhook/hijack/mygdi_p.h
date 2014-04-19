#pragma once
// mygdi_p.h
// 4/14/2014 jichi
#include <windows.h>

// - GDI32 -

BOOL WINAPI MyTextOutA(
  __in HDC hdc,
  __in int nXStart,
  __in int nYStart,
  __in LPCSTR lpString,
  __in int cchString
);
BOOL WINAPI MyTextOutW(
  _In_  HDC hdc,
  _In_  int nXStart,
  _In_  int nYStart,
  _In_  LPCWSTR lpString,
  _In_  int cchString
);

BOOL WINAPI MyExtTextOutA(
  _In_  HDC hdc,
  _In_  int X,
  _In_  int Y,
  _In_  UINT fuOptions,
  _In_  const RECT *lprc,
  _In_  LPCSTR lpString,
  _In_  UINT cbCount,
  _In_  const INT *lpDx
);
BOOL WINAPI MyExtTextOutW(
  _In_  HDC hdc,
  _In_  int X,
  _In_  int Y,
  _In_  UINT fuOptions,
  _In_  const RECT *lprc,
  _In_  LPCWSTR lpString,
  _In_  UINT cbCount,
  _In_  const INT *lpDx
);

int WINAPI MyDrawTextA(
  _In_     HDC hDC,
  _Inout_  LPCSTR lpchText,
  _In_     int nCount,
  _Inout_  LPRECT lpRect,
  _In_     UINT uFormat
);
int WINAPI MyDrawTextW(
  _In_     HDC hDC,
  _Inout_  LPCWSTR lpchText,
  _In_     int nCount,
  _Inout_  LPRECT lpRect,
  _In_     UINT uFormat
);

int WINAPI MyDrawTextExA(
  _In_     HDC hdc,
  _Inout_  LPSTR lpchText,
  _In_     int cchText,
  _Inout_  LPRECT lprc,
  _In_     UINT dwDTFormat,
  _In_     LPDRAWTEXTPARAMS lpDTParams
);
int WINAPI MyDrawTextExW(
  _In_     HDC hdc,
  _Inout_  LPWSTR lpchText,
  _In_     int cchText,
  _Inout_  LPRECT lprc,
  _In_     UINT dwDTFormat,
  _In_     LPDRAWTEXTPARAMS lpDTParams
);

#define MY_GDI_FUNCTIONS_INITIALIZER \
   { "TextOutA", "gdi32.dll", MyTextOutA }, \
   { "TextOutW", "gdi32.dll", MyTextOutW }, \
   { "ExtTextOutA", "gdi32.dll", MyExtTextOutA }, \
   { "ExtTextOutW", "gdi32.dll", MyExtTextOutW }, \
   { "DrawTextA", "gdi32.dll", MyDrawTextA }, \
   { "DrawTextW", "gdi32.dll", MyDrawTextW }, \
   { "DrawTextExA", "gdi32.dll", MyDrawTextExA }, \
   { "DrawTextExW", "gdi32.dll", MyDrawTextExW }

// EOF
