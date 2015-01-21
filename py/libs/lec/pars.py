# coding: utf8
# pars.py
# 1/20/2015 jichi
# See: LEC English to Russian Translation Engine.exe
#
# Debug method:
# - LEC Power Translator 15, select local translation service
# - Do translation once
# - Use OllyDbg to hook to the LEC engine executabe
# - Debug functions in pars.dll
# - Find runtime parameters
#
# DWORD __stdcall InitContext(BYTE arg1=0, const char *path, BYTE arg3=0, BYTE arg4=0, BYTE arg5=0, int arg6=1, int arg7=0, BYTE arg8=1);
# BOOL __stdcall CloseContext();
# DWORD __stdcall TranslateMem(UINT fmt=0xd, HGLOBAL in, HGLOBAL *out);
#
# Example path: C:\Program Files\Power Translator 15\PARS\EnRu\DIC\gen_
# It must be char instead of wchar_t.
#
# CloseContext will raise if InitContext failed.
#
# Runtime stack when TranslateMem is invoked:
# 0150FCE4   0040C54D  RETURN to LEC_Engl.0040C54D from pars.TranslateMem
# 0150FCE8   0000000D  ; jichi: arg1 is 0xd
# 0150FCEC   0078E6E8  UNICODE "hello world"
# 0150FCF0   0150FEF4 -> changed to 0x95001c
# 0150FCF4   7456571C
# 0150FCF8   00000000
# 0150FCFC   0068FDC0
# 0150FD00   0068FDC0
# 0150FD04   0150FD5A  ASCII "RtlDecodePointer"
# 0150FD08   00689B88  UNICODE "hello world"
# 0150FD0C   0150FD50
# 0150FD10   00000001
# 0150FD14  /0150FDB4
# 0150FD18  |777AFA22  RETURN to ntdll.777AFA22 from ntdll.RtlLeaveCriticalSection
# 0150FD1C  |777A70F2  RETURN to ntdll.777A70F2 from ntdll.777A32F4
# 0150FD20  |777AF9E8  RETURN to ntdll.777AF9E8 from ntdll.777A70E8
# 0150FD24  |76E3CB85  shell32.76E3CB85
#
# Runtime stack when InitContext is invoked:
# 013AF860   0040A3AC  RETURN to LEC_Engl.0040A3AC
# 013AF864   00000000  ; arg1
# 013AF868   008D8930  ASCII "C:\Program Files\Power Translator 15\PARS\EnRu\DIC\gen_"
# 013AF86C   00000000  ; arg3
# 013AF870   00000000  ; arg4
# 013AF874   00000000  ; arg5
# 013AF878   00000001  ; arg6
# 013AF87C   00000000  ; arg7
# 013AF880   00000001  ; arg8
# 013AF884   94C0AC07
# 013AF888   008DB150
# 013AF88C   008DF288
# 013AF890   013AF87C
# 013AF894   009F237E  ASCII "\DIC\gen_"
# 013AF898   013AF978
# 013AF89C   004E9100  LEC_Engl.004E9100
# 013AF8A0   95AC461B
# 013AF8A4   94C0AD4B
# 013AF8A8   00000002
#
# TranslateMem:
#
# 0040BCAD     CC             INT3
# 0040BCAE     CC             INT3
# 0040BCAF     CC             INT3
# 0040BCB0  /$ 55             PUSH EBP
# 0040BCB1  |. 8BEC           MOV EBP,ESP
# 0040BCB3  |. 6A FF          PUSH -0x1
# 0040BCB5  |. 68 806D5100    PUSH LEC_Engl.00516D80
# 0040BCBA  |. 64:A1 00000000 MOV EAX,DWORD PTR FS:[0]
# 0040BCC0  |. 50             PUSH EAX
# 0040BCC1  |. 81EC 64010000  SUB ESP,0x164
# 0040BCC7  |. A1 08725600    MOV EAX,DWORD PTR DS:[0x567208]
# 0040BCCC  |. 33C5           XOR EAX,EBP
# 0040BCCE  |. 8945 F0        MOV DWORD PTR SS:[EBP-0x10],EAX
# 0040BCD1  |. 50             PUSH EAX
# 0040BCD2  |. 8D45 F4        LEA EAX,DWORD PTR SS:[EBP-0xC]
# 0040BCD5  |. 64:A3 00000000 MOV DWORD PTR FS:[0],EAX
# 0040BCDB  |. 898D 9CFEFFFF  MOV DWORD PTR SS:[EBP-0x164],ECX
# 0040BCE1  |. 8D45 B8        LEA EAX,DWORD PTR SS:[EBP-0x48]
# 0040BCE4  |. 50             PUSH EAX                                 ; /Arg1
# 0040BCE5  |. E8 467DFFFF    CALL LEC_Engl.00403A30                   ; \LEC_Engl.00403A30
# 0040BCEA  |. 83C4 04        ADD ESP,0x4
# 0040BCED  |. 8985 98FEFFFF  MOV DWORD PTR SS:[EBP-0x168],EAX
# 0040BCF3  |. 8B8D 98FEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x168]
# 0040BCF9  |. 898D 94FEFFFF  MOV DWORD PTR SS:[EBP-0x16C],ECX
# 0040BCFF  |. C745 FC 000000>MOV DWORD PTR SS:[EBP-0x4],0x0
# 0040BD06  |. 68 2C635300    PUSH LEC_Engl.0053632C                   ; /Arg3 = 0053632C ASCII "\pars.dll"
# 0040BD0B  |. 8B95 94FEFFFF  MOV EDX,DWORD PTR SS:[EBP-0x16C]         ; |
# 0040BD11  |. 52             PUSH EDX                                 ; |Arg2
# 0040BD12  |. 8D45 D4        LEA EAX,DWORD PTR SS:[EBP-0x2C]          ; |
# 0040BD15  |. 50             PUSH EAX                                 ; |Arg1
# 0040BD16  |. E8 B5260300    CALL LEC_Engl.0043E3D0                   ; \LEC_Engl.0043E3D0
# 0040BD1B  |. 83C4 0C        ADD ESP,0xC
# 0040BD1E  |. C645 FC 02     MOV BYTE PTR SS:[EBP-0x4],0x2
# 0040BD22  |. 6A 00          PUSH 0x0                                 ; /Arg2 = 00000000
# 0040BD24  |. 6A 01          PUSH 0x1                                 ; |Arg1 = 00000001
# 0040BD26  |. 8D4D B8        LEA ECX,DWORD PTR SS:[EBP-0x48]          ; |
# 0040BD29  |. E8 72E40100    CALL LEC_Engl.0042A1A0                   ; \LEC_Engl.0042A1A0
# 0040BD2E  |. 837D EC 10     CMP DWORD PTR SS:[EBP-0x14],0x10
# 0040BD32  |. 72 0B          JB SHORT LEC_Engl.0040BD3F
# 0040BD34  |. 8B4D D8        MOV ECX,DWORD PTR SS:[EBP-0x28]
# 0040BD37  |. 898D 90FEFFFF  MOV DWORD PTR SS:[EBP-0x170],ECX
# 0040BD3D  |. EB 09          JMP SHORT LEC_Engl.0040BD48
# 0040BD3F  |> 8D55 D8        LEA EDX,DWORD PTR SS:[EBP-0x28]
# 0040BD42  |. 8995 90FEFFFF  MOV DWORD PTR SS:[EBP-0x170],EDX
# 0040BD48  |> 8B85 90FEFFFF  MOV EAX,DWORD PTR SS:[EBP-0x170]
# 0040BD4E  |. 50             PUSH EAX                                 ; /FileName
# 0040BD4F  |. FF15 34245300  CALL DWORD PTR DS:[<&KERNEL32.LoadLibrar>; \LoadLibraryA
# 0040BD55  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BD5B  |. 8901           MOV DWORD PTR DS:[ECX],EAX
# 0040BD5D  |. 8B95 9CFEFFFF  MOV EDX,DWORD PTR SS:[EBP-0x164]
# 0040BD63  |. 833A 00        CMP DWORD PTR DS:[EDX],0x0
# 0040BD66  |. 74 60          JE SHORT LEC_Engl.0040BDC8
# 0040BD68  |. 68 1C635300    PUSH LEC_Engl.0053631C                   ;  ASCII "TranslateMem"
# 0040BD6D  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BD73  |. E8 88000000    CALL LEC_Engl.0040BE00
# 0040BD78  |. 50             PUSH EAX                                 ; |hModule
# 0040BD79  |. FF15 38245300  CALL DWORD PTR DS:[<&KERNEL32.GetProcAdd>; \GetProcAddress
# 0040BD7F  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BD85  |. 8941 04        MOV DWORD PTR DS:[ECX+0x4],EAX
# 0040BD88  |. 68 10635300    PUSH LEC_Engl.00536310                   ;  ASCII "InitContext"
# 0040BD8D  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BD93  |. E8 68000000    CALL LEC_Engl.0040BE00
# 0040BD98  |. 50             PUSH EAX                                 ; |hModule
# 0040BD99  |. FF15 38245300  CALL DWORD PTR DS:[<&KERNEL32.GetProcAdd>; \GetProcAddress
# 0040BD9F  |. 8B95 9CFEFFFF  MOV EDX,DWORD PTR SS:[EBP-0x164]
# 0040BDA5  |. 8942 08        MOV DWORD PTR DS:[EDX+0x8],EAX
# 0040BDA8  |. 68 00635300    PUSH LEC_Engl.00536300                   ;  ASCII "CloseContext"
# 0040BDAD  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BDB3  |. E8 48000000    CALL LEC_Engl.0040BE00
# 0040BDB8  |. 50             PUSH EAX                                 ; |hModule
# 0040BDB9  |. FF15 38245300  CALL DWORD PTR DS:[<&KERNEL32.GetProcAdd>; \GetProcAddress
# 0040BDBF  |. 8B8D 9CFEFFFF  MOV ECX,DWORD PTR SS:[EBP-0x164]
# 0040BDC5  |. 8941 0C        MOV DWORD PTR DS:[ECX+0xC],EAX
# 0040BDC8  |> C745 FC FFFFFF>MOV DWORD PTR SS:[EBP-0x4],-0x1
# 0040BDCF  |. 6A 00          PUSH 0x0                                 ; /Arg2 = 00000000
# 0040BDD1  |. 6A 01          PUSH 0x1                                 ; |Arg1 = 00000001
# 0040BDD3  |. 8D4D D4        LEA ECX,DWORD PTR SS:[EBP-0x2C]          ; |
# 0040BDD6  |. E8 C5E30100    CALL LEC_Engl.0042A1A0                   ; \LEC_Engl.0042A1A0
# 0040BDDB  |. 8B4D F4        MOV ECX,DWORD PTR SS:[EBP-0xC]
# 0040BDDE  |. 64:890D 000000>MOV DWORD PTR FS:[0],ECX
# 0040BDE5  |. 59             POP ECX
# 0040BDE6  |. 8B4D F0        MOV ECX,DWORD PTR SS:[EBP-0x10]
# 0040BDE9  |. 33CD           XOR ECX,EBP
# 0040BDEB  |. E8 9B910D00    CALL LEC_Engl.004E4F8B
# 0040BDF0  |. 8BE5           MOV ESP,EBP
# 0040BDF2  |. 5D             POP EBP
# 0040BDF3  \. C3             RETN
# 0040BDF4     CC             INT3
# 0040BDF5     CC             INT3
# 0040BDF6     CC             INT3
#
# InitContext
# ebp-4 is reserved as return value on the stack
#
# 006499C3   90               NOP
# 006499C4 > 55               PUSH EBP
# 006499C5   8BEC             MOV EBP,ESP
# 006499C7   6A 00            PUSH 0x0  ; jichi: this is return value
# 006499C9   53               PUSH EBX
# 006499CA   56               PUSH ESI
# 006499CB   33C0             XOR EAX,EAX
# 006499CD   55               PUSH EBP
# 006499CE   68 E09A6400      PUSH pars.00649AE0    ; jichi: this is CloseContext function
# 006499D3   64:FF30          PUSH DWORD PTR FS:[EAX]   ; jichi: push fs:[0]
# 006499D6   64:8920          MOV DWORD PTR FS:[EAX],ESP    ; jichi: mov fs:[0],esp
# 006499D9   803D 04B26400 00 CMP BYTE PTR DS:[0x64B204],0x0    : jichi: ds[0x64B204] is zero, this might be a static bool initialized variable
# 006499E0   74 05            JE SHORT pars.006499E7
# 006499E2   E8 35F7FFFF      CALL pars.0064911C    ; jichi: this reached if this function is intialized twice
# 006499E7   8B75 0C          MOV ESI,DWORD PTR SS:[EBP+0xC] ; jichi: esi=arg2, normal code path
# 006499EA   33DB             XOR EBX,EBX   ; jichi; ebx = 0
# 006499EC   EB 4E            JMP SHORT pars.00649A3C
# 006499EE   80C3 01          ADD BL,0x1
# 006499F1   73 05            JNB SHORT pars.006499F8
# 006499F3   E8 989EF9FF      CALL pars.005E3890
# 006499F8   8D55 FC          LEA EDX,DWORD PTR SS:[EBP-0x4] ; jichi: return value
# 006499FB   8BC6             MOV EAX,ESI
# 006499FD   E8 C6CFF9FF      CALL pars.005E69C8
# 00649A02   8B55 FC          MOV EDX,DWORD PTR SS:[EBP-0x4] ; jichi: return value
# 00649A05   33C0             XOR EAX,EAX
# 00649A07   8AC3             MOV AL,BL
# 00649A09   48               DEC EAX
# 00649A0A   83F8 07          CMP EAX,0x7
# 00649A0D   76 05            JBE SHORT pars.00649A14
# 00649A0F   E8 749EF9FF      CALL pars.005E3888
# 00649A14   40               INC EAX
# 00649A15   6BC0 20          IMUL EAX,EAX,0x20
# 00649A18   71 05            JNO SHORT pars.00649A1F
# 00649A1A   E8 719EF9FF      CALL pars.005E3890
# 00649A1F   8D04C5 C4006500  LEA EAX,DWORD PTR DS:[EAX*8+0x6500C4]
# 00649A26   B9 FF000000      MOV ECX,0xFF
# 00649A2B   E8 FCACF9FF      CALL pars.005E472C
# 00649A30   8BC6             MOV EAX,ESI
# 00649A32   E8 69CEF9FF      CALL pars.005E68A0
# 00649A37   03F0             ADD ESI,EAX
# 00649A39   83C6 01          ADD ESI,0x1
# 00649A3C   803E 00          CMP BYTE PTR DS:[ESI],0x0 ; jichi: compare if esi=arg2[0] is zero
# 00649A3F   74 05            JE SHORT pars.00649A46    ; jichi: if yes, something wrong
# 00649A41   80FB 08          CMP BL,0x8                ; jichi: normal path, ebx = 0
# 00649A44  ^72 A8            JB SHORT pars.006499EE    ; jichi: if is bl < -0x8
# 00649A46   BA C4016500      MOV EDX,pars.006501C4 ; jichi: if arg2[0] is 0, maybe, arg2 is the commandline parameters
# 00649A4B   8A4D 10          MOV CL,BYTE PTR SS:[EBP+0x10]  ; jichi: arg3
# 00649A4E   8A45 08          MOV AL,BYTE PTR SS:[EBP+0x8]  ; jichi: arg1
# 00649A51   E8 36F6FFFF      CALL pars.0064908C ; jichi: this is probabily parsing command line parameters arg1 and arg2
# 00649A56   84C0             TEST AL,AL
# 00649A58   74 59            JE SHORT pars.00649AB3
# 00649A5A   C605 04B26400 01 MOV BYTE PTR DS:[0x64B204],0x1    ; jichi: this reset the initialized variable
# 00649A61   8A45 08          MOV AL,BYTE PTR SS:[EBP+0x8]   ; jichi: arg1
# 00649A64   A2 C4096500      MOV BYTE PTR DS:[0x6509C4],AL
# 00649A69   8A45 14          MOV AL,BYTE PTR SS:[EBP+0x14]  ; jichi: arg4
# 00649A6C   A2 BC016500      MOV BYTE PTR DS:[0x6501BC],AL
# 00649A71   8A45 18          MOV AL,BYTE PTR SS:[EBP+0x18]   ; jichi: arg5
# 00649A74   A2 BD016500      MOV BYTE PTR DS:[0x6501BD],AL
# 00649A79   8B45 1C          MOV EAX,DWORD PTR SS:[EBP+0x1C]      ; jichi: arg6
# 00649A7C   A3 C0016500      MOV DWORD PTR DS:[0x6501C0],EAX
# 00649A81   A1 DCB46400      MOV EAX,DWORD PTR DS:[0x64B4DC]
# 00649A86   C700 C0996400    MOV DWORD PTR DS:[EAX],pars.006499C0
# 00649A8C   A1 18B46400      MOV EAX,DWORD PTR DS:[0x64B418]
# 00649A91   8A55 24          MOV DL,BYTE PTR SS:[EBP+0x24]  ; jichi: arg8
# 00649A94   8810             MOV BYTE PTR DS:[EAX],DL
# 00649A96   837D 20 00       CMP DWORD PTR SS:[EBP+0x20],0x0    ; jichi: arg7
# 00649A9A   74 13            JE SHORT pars.00649AAF
# 00649A9C   8B45 20          MOV EAX,DWORD PTR SS:[EBP+0x20]   ; jichi: arg7
# 00649A9F   A3 C8096500      MOV DWORD PTR DS:[0x6509C8],EAX
# 00649AA4   A1 DCB46400      MOV EAX,DWORD PTR DS:[0x64B4DC]
# 00649AA9   C700 90996400    MOV DWORD PTR DS:[EAX],pars.00649990
# 00649AAF   33DB             XOR EBX,EBX
# 00649AB1   EB 17            JMP SHORT pars.00649ACA
# 00649AB3   8B1D 2CB56400    MOV EBX,DWORD PTR DS:[0x64B52C]          ; pars.0064C8B4
# 00649AB9   8B1B             MOV EBX,DWORD PTR DS:[EBX]
# 00649ABB   81E3 FFFF0000    AND EBX,0xFFFF
# 00649AC1   85DB             TEST EBX,EBX
# 00649AC3   79 05            JNS SHORT pars.00649ACA
# 00649AC5   E8 BE9DF9FF      CALL pars.005E3888
# 00649ACA   33C0             XOR EAX,EAX
# 00649ACC   5A               POP EDX
# 00649ACD   59               POP ECX
# 00649ACE   59               POP ECX
# 00649ACF   64:8910          MOV DWORD PTR FS:[EAX],EDX
# 00649AD2   68 E79A6400      PUSH pars.00649AE7
# 00649AD7   8D45 FC          LEA EAX,DWORD PTR SS:[EBP-0x4]
# 00649ADA   E8 CDA9F9FF      CALL pars.005E44AC
# 00649ADF   C3               RETN
# 00649AE0  ^E9 67A3F9FF      JMP pars.005E3E4C
# 00649AE5  ^EB F0            JMP SHORT pars.00649AD7
# 00649AE7   8BC3             MOV EAX,EBX
# 00649AE9   5E               POP ESI
# 00649AEA   5B               POP EBX
# 00649AEB   59               POP ECX
# 00649AEC   5D               POP EBP
# 00649AED   C2 2000          RETN 0x20
#
# CloseContext
# 00649AF0 > C605 04B26400 00 MOV BYTE PTR DS:[0x64B204],0x0
# 00649AF7   E8 20F6FFFF      CALL pars.0064911C


if __name__ == '__main__': # DEBUG
  import sys
  sys.path.append("..")

import ctypes, os
#from sakurakit import msvcrt
from sakurakit.skdebug import dprint, dwarn
import lecdef

# Export global functions
#strcpy = ctypes.cdll.msvcrt.strcpy
wcscpy = ctypes.cdll.msvcrt.wcscpy

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalFree = ctypes.windll.kernel32.GlobalFree
#GlobalSize = ctypes.windll.kernel32.GlobalSize
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
CF_UNICODETEXT = 0xd

def GlobalGetW(mem):
  """
  @param  mem  HGLOBAL
  @return  unicode or None
  """
  p = GlobalLock(mem)
  if p:
    text = ctypes.c_wchar_p(p)
    GlobalUnlock(mem)
    if text:
      return text.value

def GlobalPutW(mem, text):
  """
  @param  mem  HGLOBAL
  @param  text  unicode
  @return  bool
  """
  p = GlobalLock(mem)
  if p:
    wcscpy(ctypes.c_wchar_p(p), text)
    GlobalUnlock(mem)
    return True
  return False

BUFFER_SIZE = lecdef.DLL_BUFFER_SIZE

ENGINE_DLL = 'pars'   # PARS/EnRu/pars.dll
#ENGINE_ENCODING = 'utf16'

class _Loader(object):

  def __init__(self):
    self.initialized = False
    self._dll = None
    self._buffer = None

  @property
  def buffer(self):
    """
    @return  int
    """
    if not self._buffer:
      dprint("alloc buffer")
      self._buffer = GlobalAlloc(0, BUFFER_SIZE)
    return self._buffer

  #def freeBuffer(self):
  #  if self._buffer:
  #    dprint("free buffer")
  #    msvcrt.free(self._buffer)
  #    self._buffer = None

  @property
  def dll(self):
    if not self._dll:
      try:
        self._dll = ctypes.WinDLL(ENGINE_DLL)
        dprint("pars engine dll is loaded")
      except (WindowsError, AttributeError), e:
        self._dll = None
        dwarn("failed to load pars", e)
    return self._dll

  #def hasDll(self): return bool(self._dll)

  def _initPath(self):
    """Return the directory path of the dll
    @return  str not unicode (c_char_p)
    @raise  WindowsError, AttributeError
    """
    from win32api import GetModuleFileName
    dllpath = GetModuleFileName(self.dll._handle)
    #dllpath = dllpath.encode('utf8', errors='ignore')
    return os.path.dirname(dllpath)

  def init(self):
    """Initialize the engine
    @return  bool
    @raise  WindowsError, AttributeError

    DWORD __stdcall InitContext(BYTE arg1=0, const char *path, BYTE arg3=0, BYTE arg4=0, BYTE arg5=0, int arg6=1, int arg7=0, BYTE arg8=1);
    """
    dprint("enter")
    path = self._initPath() + r'\DIC\gen_'
    #path = os.path.join(path, r'DIC\gen_')
    #path = r'.\DIC\gen_'
    #dprint(path)
    #path = r'C:\Program Files\Power Translator 15\PARS\EnRu\DIC\gen_'
    res = self.dll.InitContext(
      0, # arg1
      path, #ctypes.c_char_p(path), # arg2  must be str instead of unicode
      0, # arg3
      0, # arg4
      0, # arg5
      1, # arg6
      0, # arg7
      1, # arg8
    )
    dprint("leave: res = %s" % res)
    return res == 0

  def end(self):
    """Destroy the engine
    @return  bool
    @raise  WindowsError, AttributeError

    BOOL __stdcall CloseContext();
    """
    ok = self.dll.CloseContext()
    if self._buffer:
      GlobalFree(self._buffer)
      self._buffer = None
    dprint("ok = %s" % ok)
    return bool(ok)

  def translate(self, text):
    """
    @param  text  str not unicode
    @return  unicode or None
    @raise  WindowsError, AttributeError

    DWORD __stdcall TranslateMem(UINT fmt, HGLOBAL in, HGLOBAL *out);
    """
    input = self.buffer
    GlobalPutW(input, text)
    output = ctypes.c_ulong(0)
    ok = 0 == self.dll.TranslateMem(CF_UNICODETEXT, input, ctypes.addressof(output))
    if ok and output.value:
      return GlobalGetW(output)

class Loader(object):
  def __init__(self):
    self.__d = _Loader()

  def __del__(self):
    self.destroy()

  def init(self): # -> bool
    d = self.__d
    if not d.initialized:
      try: d.initialized = d.init()
      except (WindowsError, AttributeError): pass
    return d.initialized

  def isInitialized(self): return self.__d.initialized

  def destroy(self):
    d = self.__d
    if d.initialized:
      try: d.end()
      except Exception, e: dwarn("warning: exception", e)
      d.initialized = False
    #d.freeBuffer()

  def translate(self, text):
    """
    @param  text
    @return   unicode not None
    @throw  RuntimeError
    """
    if isinstance(text, str):
      text = text.decode('utf8', errors='ignore')
    if not text:
      return ''
    try: return self.__d.translate(text) or ""
    except (WindowsError, AttributeError), e:
      dwarn("failed to load pars dll", e)
      raise RuntimeError("failed to access pars dll")

if __name__ == '__main__': # DEBUG
  lecpath = r"C:\Program Files\Power Translator 15"
  #lecpath = r"Z:\Local\Windows\Applications\Power Translator 15"
  enginepath = lecpath + r"\PARS\EnRu"
  os.environ['PATH'] += os.pathsep + enginepath
  l = Loader()
  l.init()
  t = "hello world"
  ret = l.translate(t)
  l.destroy()
  print ret

# EOF
