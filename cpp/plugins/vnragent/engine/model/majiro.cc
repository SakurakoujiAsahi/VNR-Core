// majiro.cc
// 4/20/2014 jichi
// See: http://dev.haeleth.net/majiro.shtml
// See: http://bbs.sumisora.org/read.php?tid=10983263
// See: http://bbs.sumisora.org/read.php?tid=10917044
// See: http://bbs.sumisora.org/read.php?tid=225250
#include "engine/model/majiro.h"
#include "engine/enginecontroller.h"
#include "engine/enginehash.h"
#include "memdbg/memsearch.h"
#include <qt_windows.h>

/** Private data */

ulong MajiroEngine::search(ulong startAddress, ulong stopAddress)
{
  enum { sub_esp = 0xec81 }; // caller pattern: sub esp = 0x81,0xec
  return MemDbg::findCallerAddress((ulong)::TextOutA, sub_esp, startAddress, stopAddress);
  //addr = 0x41af90; // レミニセンス function address
  //return addr && hookAddress(addr);
}

/**
 *  Compute ITH's split value from the first parameter of the hooked function.
 *  Let eax be arg1, the original logic in MajiroSpecialHook is:
 *      ([eax+0x28] & 0xff) | (([eax+0x48] >> 1) & 0xffffff00)
 */
inline static DWORD splitOf(DWORD *arg1)
{ return (arg1[10] & 0xff) | ((arg1[18] >> 1) & 0xffffff00); }

/**
 *  TODO: The current split cannot distinguish name and choices
 *  The current hooked function have line-breaking issue
 *
 *  Sample game: レミニセンス
 *  int __cdecl sub_41AF90(CHAR ch, int arg2, LPCSTR str, arg4, arg5);
 *    String          = byte ptr  4
 *    arg_4           = dword ptr  8
 *    lpString        = dword ptr  0Ch
 *    arg_C           = dword ptr  10h
 *    arg_10          = dword ptr  14h
 *  - arg1: LPCSTR, font family name (MS Gothic)
 *  - arg2: LPSIZE, size of the canvas to draw
 *  - arg3: LPCSTR, starting address of the string to paint
 *  - arg4: LPSTR, output string, could be zero (in 罪深き終末論)
 *  - arg5: int, constant, always 1
 *  - return: width of the text, = 26 * text length
 *  Scenario text's ch seems to always be one.
 *
 *  Callers:
 *  0x41aa10 @ 0x416ab0 // Scenario
 *  0x41f650 // Name
 *
 *  Guessed function signature:
 *  - typedef int (__cdecl *hook_fun_t)(LPCSTR, LPSIZE, LPCSTR, LPCSTR, int);
 *  - int __cdecl newHookFun(LPCSTR fontName1, LPSIZE canvasSize2, LPCSTR text3, LPSTR output4, int const5)
 */

void MajiroEngine::hook(HookStack *stack)
{
  static QByteArray data_; // persistent storage, which makes this function not thread-safe

  LPDWORD arg1 = (LPDWORD)stack->args[0];
  LPCSTR text3 = (LPCSTR)stack->args[2];

  // Compute ITH signature
  DWORD returnAddress = stack->retaddr,
        split = splitOf(arg1);
  // The following logic is consistent with VNR's old texthook
  //auto sig = Engine::hashThreadSignature(returnAddress, split, Engine::UnknownRole);
  auto sig = Engine::hashThreadSignature(returnAddress, split);

  data_ = EngineController::instance()->dispatchTextA(text3, sig);
  //dmsg(QString::fromLocal8Bit(ret));
  stack->args[2] = (DWORD)data_.constData(); // reset arg3
}

// EOF

/*

// Used to get function's return address
// http://stackoverflow.com/questions/8797943/finding-a-functions-address-in-c
#pragma intrinsic(_ReturnAddress)

int __cdecl newHookFun(LPCSTR fontName1, LPSIZE canvasSize2, LPCSTR text3, LPSTR output4, int const5)
{
  // Compute ITH signature
  DWORD returnAddress = (DWORD)_ReturnAddress(),
        split = splitOf((DWORD *)fontName1);
  // The following logic is consistent with VNR's old texthook
  auto signature = Engine::hashThreadSignature(returnAddress, split);

  //return oldHook(arg1, arg2, str, arg4, arg5);
#ifdef DEBUG
  qDebug() << QString::fromLocal8Bit(fontName1) << ":"
           << canvasSize2->cx << "," << canvasSize2->cy << ":"
           << QString::fromLocal8Bit(text3) << ":"
           << QString::fromLocal8Bit(output4 ? output4 : "(null)") << ":"
           << const5 << ";"
           << " signature: " << QString::number(signature, 16);
#endif // DEBUG
  auto q = EngineController::instance();
  QByteArray data = q->dispatchTextA(text3, signature, Engine::UnknownRole);
  if (!data.isEmpty())
    return oldHookFun(fontName1, canvasSize2, data, output4, const5);
  else {
    // Estimated painted character width for MS Gothic, assume SJIS on average takes up two chars
    enum { CharWidth = 13 };
    return CharWidth * ::strlen(text3);
  }
}
bool MajiroEngine::detach()
{
  if (!::hookAddress || !::oldHookFun)
    return false;
  bool ok = detours::restore<hook_fun_t>(::hookAddress, ::oldHookFun);
  ::hookAddress = 0;
  return ok;
}
*/
