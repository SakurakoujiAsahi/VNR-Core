#pragma once

// hijack_p.h
// 1/27/2013 jichi

#include <windows.h>

#define HIJACK_FUNCTIONS_INITIALIZER \
   { "kernel32.dll", "GetProcAddress", ::GetProcAddress, Hijack::myGetProcAddress }, \
   { "kernel32.dll", "LoadLibraryA", ::LoadLibraryA, Hijack::myLoadLibraryA }, \
   { "kernel32.dll", "LoadLibraryW", ::LoadLibraryW, Hijack::myLoadLibraryW }, \
   { "kernel32.dll", "LoadLibraryExA", ::LoadLibraryExA, Hijack::myLoadLibraryExA }, \
   { "kernel32.dll", "LoadLibraryExW", ::LoadLibraryExW, Hijack::myLoadLibraryExW }, \
   { "user32.dll", "TrackPopupMenu", ::TrackPopupMenu, Hijack::myTrackPopupMenu }, \
   { "user32.dll", "TrackPopupMenuEx", ::TrackPopupMenuEx, Hijack::myTrackPopupMenuEx }, \
   { "gdi32.dll", "CreateFontA", ::CreateFontA, Hijack::myCreateFontA }, \
   { "gdi32.dll", "CreateFontW", ::CreateFontW, Hijack::myCreateFontW }, \
   { "gdi32.dll", "CreateFontIndirectA", ::CreateFontIndirectA, Hijack::myCreateFontIndirectA }, \
   { "gdi32.dll", "CreateFontIndirectW", ::CreateFontIndirectW, Hijack::myCreateFontIndirectW }
   //{ "gdi32.dll", "TextOutA", ::TextOutA, Hijack::myTextOutA }

namespace Hijack {

struct FunctionInfo {
  LPCSTR moduleName;
  LPCSTR functionName;
  LPVOID oldFunctionAddress;
  LPVOID newFunctionAddress;
};

void overrideModuleFunctions(HMODULE hModule);
void restoreModuleFunctions(HMODULE hModule);

// Return my function used to override proc name
LPVOID getOverridingFunctionAddress(HMODULE hModule, LPCSTR lpProcName);

// - KERNEL32 -

LPVOID WINAPI myGetProcAddress(
  _In_ HMODULE hModule,
  _In_ LPCSTR lpProcName
);
HMODULE WINAPI myLoadLibraryA(
  _In_  LPCSTR lpFileName
);
HMODULE WINAPI myLoadLibraryW(
  _In_  LPCWSTR lpFileName
);
HMODULE WINAPI myLoadLibraryExA(
  _In_ LPCSTR lpFileName,
  __reserved HANDLE hFile,  // _Reserved_ not supported in MSVC 2010
  _In_ DWORD dwFlags
);
HMODULE WINAPI myLoadLibraryExW(
  _In_ LPCWSTR lpFileName,
  __reserved HANDLE hFile,
  _In_ DWORD dwFlags
);

// - USER32 -

BOOL WINAPI myTrackPopupMenu(
  _In_ HMENU hMenu,
  _In_ UINT uFlags,
  _In_ int x,
  _In_ int y,
  _In_ int nReserved,
  _In_ HWND hWnd,
  _In_opt_ CONST RECT *prcRect
);
BOOL WINAPI myTrackPopupMenuEx(
  _In_ HMENU hMenu,
  _In_ UINT uFlags,
  _In_ int x,
  _In_ int y,
  _In_ HWND hWnd,
  _In_opt_ LPTPMPARAMS lptpm
);

// - GDI32 -

HFONT WINAPI myCreateFontIndirectA(
  _In_  const LOGFONTA *lplf
);

HFONT WINAPI myCreateFontIndirectW(
  _In_  const LOGFONTW *lplf
);


HFONT WINAPI myCreateFontA(
  _In_  int nHeight,
  _In_  int nWidth,
  _In_  int nEscapement,
  _In_  int nOrientation,
  _In_  int fnWeight,
  _In_  DWORD fdwItalic,
  _In_  DWORD fdwUnderline,
  _In_  DWORD fdwStrikeOut,
  _In_  DWORD fdwCharSet,
  _In_  DWORD fdwOutputPrecision,
  _In_  DWORD fdwClipPrecision,
  _In_  DWORD fdwQuality,
  _In_  DWORD fdwPitchAndFamily,
  _In_  LPCSTR lpszFace
);

HFONT WINAPI myCreateFontW(
  _In_  int nHeight,
  _In_  int nWidth,
  _In_  int nEscapement,
  _In_  int nOrientation,
  _In_  int fnWeight,
  _In_  DWORD fdwItalic,
  _In_  DWORD fdwUnderline,
  _In_  DWORD fdwStrikeOut,
  _In_  DWORD fdwCharSet,
  _In_  DWORD fdwOutputPrecision,
  _In_  DWORD fdwClipPrecision,
  _In_  DWORD fdwQuality,
  _In_  DWORD fdwPitchAndFamily,
  _In_  LPCWSTR lpszFace
);

} // namespace Hijack

// EOF

/*
BOOL WINAPI myTextOutA(
  _In_  HDC hdc,
  _In_  int nXStart,
  _In_  int nYStart,
  _In_  LPCSTR lpString,
  _In_  int cchString
);
BOOL WINAPI myTextOutW(
  _In_  HDC hdc,
  _In_  int nXStart,
  _In_  int nYStart,
  _In_  LPCWSTR lpString,
  _In_  int cchString
);

int WINAPI MyMessageBoxA(
  _In_opt_ HWND hWnd,
  _In_opt_ LPCSTR lpText,
  _In_opt_ LPCSTR lpCaption,
  _In_ UINT uType
);
int WINAPI MyMessageBoxW(
  _In_ HWND hWnd,
  _In_ LPCWSTR lpText,
  _In_ LPCWSTR lpCaption,
  _In_ UINT uType
);
*/

// - DirectX -

//#include <d3d9.h>
//IDirect3D9* WINAPI MyDirect3DCreate9(
//  UINT SDKVersion
//);

/*
HDC WINAPI MyGetDC(
  _In_ HWND hWnd
);
HDC WINAPI MyGetDCEx(
  _In_ HWND hWnd,
  _In_ HRGN hrgnClip,
  _In_ DWORD flags
);

HDC WINAPI MyBeginPaint(
  _In_ HWND hWnd,
  _Out_ LPPAINTSTRUCT lpPaint
);
#include <d3dx9core.h>
//
//INT WINAPI MyDrawTextW(
//  _In_ LPD3DXSPRITE pSprite,
//  _In_ LPCWSTR pString,
//  _In_ INT Count,
//  _In_ LPRECT pRect,
//  _In_ DWORD Format,
//  _In_ D3DCOLOR Color
//);

HRESULT MyD3DXCreateFontA(
  _In_ LPDIRECT3DDEVICE9 pDevice,
  _In_ INT Height,
  _In_ UINT Width,
  _In_ UINT Weight,
  _In_ UINT MipLevels,
  _In_ BOOL Italic,
  _In_ DWORD CharSet,
  _In_ DWORD OutputPrecision,
  _In_ DWORD Quality,
  _In_ DWORD PitchAndFamily,
  _In_ LPCSTR pFacename,
  _Out_ LPD3DXFONT *ppFont
);

HRESULT MyD3DXCreateFontW(
  _In_ LPDIRECT3DDEVICE9 pDevice,
  _In_ INT Height,
  _In_ UINT Width,
  _In_ UINT Weight,
  _In_ UINT MipLevels,
  _In_ BOOL Italic,
  _In_ DWORD CharSet,
  _In_ DWORD OutputPrecision,
  _In_ DWORD Quality,
  _In_ DWORD PitchAndFamily,
  _In_ LPCWSTR pFacename,
  _Out_ LPD3DXFONT *ppFont
);
   { "D3DXCreateFontA", "d3dx9_24.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_24.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_25.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_25.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_26.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_26.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_27.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_27.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_28.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_28.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_29.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_29.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_30.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_30.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_31.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_31.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_32.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_32.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_33.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_33.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_34.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_34.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_35.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_35.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_36.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_36.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_37.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_37.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_38.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_38.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_39.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_39.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_40.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_40.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_41.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_41.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_42.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_42.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9_43.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9_43.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9d_33.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9d_33.dll", MyD3DXCreateFontW },
   { "D3DXCreateFontA", "d3dx9d_43.dll", MyD3DXCreateFontA },
   { "D3DXCreateFontW", "d3dx9d_43.dll", MyD3DXCreateFontW }
*/