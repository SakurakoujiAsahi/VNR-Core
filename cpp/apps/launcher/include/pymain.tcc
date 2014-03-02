// pymain.tcc
// 10/6/2012 jichi
#include "cc/ccmacro.h"
#include <windows.h>
#include <string>
#include <memory>

#if !defined(PYTHON_PATH) || !defined(PY_PATH)
# error "app path not defined"
#endif

//#define DEBUG "main"
//#include "sakurakit/skdebug.h"
//#ifdef DEBUG
//  #include <QtCore>
//  #define DOUT(_msg)    qDebug() << "main:" << _msg
//#else
  #define DOUT(_dummy)  (void)0
//#endif // DEBUG

// - Launcher -

namespace { // unnamed

inline std::string dirname(const std::string &path)
{ return path.substr(0, path.find_last_of('\\')); }

inline std::wstring dirname(const std::wstring &path)
{ return path.substr(0, path.find_last_of(L'\\')); }

} // unnamed namespace

// - Main -

int CALLBACK WinMain(__in HINSTANCE hInstance, __in HINSTANCE hPrevInstance, __in LPSTR lpCmdLine, __in int nCmdShow)
{
  CC_UNUSED(hInstance);
  CC_UNUSED(hPrevInstance);
  CC_UNUSED(nCmdShow);

  enum { BUFFER_SIZE = MAX_PATH * 3 };
  WCHAR wszBuffer[BUFFER_SIZE];
  if (::GetModuleFileNameW(0, wszBuffer, BUFFER_SIZE) == BUFFER_SIZE)
    return -1;

  std::wstring wsDir = dirname(wszBuffer);
  std::wstring wsApp = wsDir + L"\\" PYTHON_PATH;
  std::wstring wsAppPath = dirname(wsApp);

  // See: http://msdn.microsoft.com/en-us/library/windows/desktop/cc144102(v=vs.85).aspx
  //::SetFileAttributesW(wsDir.c_str(), FILE_ATTRIBUTE_READONLY);

  DOUT(QString::fromStdWString(app));

  STARTUPINFOW siStartupInfo;
  ::memset(&siStartupInfo, 0, sizeof(siStartupInfo));
  siStartupInfo.cb = sizeof(siStartupInfo);

  PROCESS_INFORMATION piProcessInfo;
  ::memset(&piProcessInfo, 0, sizeof(piProcessInfo));

  LPVOID lpEnvironment = nullptr;

  std::wstring wsCmdLine =
      L"\"" + wsApp + L"\"" L" "
      //L"-OO " // python -OO optimization
      L"-B " // python -B to skip generating byte code, http://stackoverflow.com/questions/154443/how-to-avoid-pyc-files
      L"\"" + wsDir + L"\\" PY_PATH L"\"";

  // See: http://codingmisadventures.wordpress.com/2009/03/10/retrieving-command-line-parameters-from-winmain-in-win32/
  if (lpCmdLine &&
      ::MultiByteToWideChar(CP_ACP, 0, lpCmdLine, -1, wszBuffer, BUFFER_SIZE) &&
      wszBuffer[0]) {
    if (wszBuffer[0] != L' ')
      wsCmdLine += L" ";
    wsCmdLine += wszBuffer;
  }
  ::memcpy(wszBuffer, wsCmdLine.c_str(), (wsCmdLine.size() + 1) * sizeof(wchar_t));
  LPWSTR wszCmdLine = wszBuffer;

  // See: http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425(v=vs.85).aspx
  //
  // BOOL WINAPI CreateProcess(
  //   __in_opt     LPCTSTR lpApplicationName,
  //   __inout_opt  LPTSTR lpCommandLine,
  //   __in_opt     LPSECURITY_ATTRIBUTES lpProcessAttributes,
  //   __in_opt     LPSECURITY_ATTRIBUTES lpThreadAttributes,
  //   __in         BOOL bInheritHandles,
  //   __in         DWORD dwCreationFlags,
  //   __in_opt     LPVOID lpEnvironment,
  //   __in_opt     LPCTSTR lpCurrentDirectory,
  //   __in         LPSTARTUPINFO lpStartupInfo,
  //   __out        LPPROCESS_INFORMATION lpProcessInformation
  // );
  //
  BOOL bResult = ::CreateProcessW(
    wsApp.c_str(),      // app path
    wszCmdLine,         // app args
    0, 0,               // security attributes
    FALSE,              // inherited
    CREATE_DEFAULT_ERROR_MODE, // creation flags
    lpEnvironment,
    wsAppPath.c_str(),
    &siStartupInfo,
    &piProcessInfo
  );

  return bResult ? 0 : -1;
}

// EOF
