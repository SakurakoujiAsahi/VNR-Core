#pragma once

// winasmdef.h
// 5/25/2015 jichi

#define s1_0d           0,0,0,0 // 0x0000
#define s1_pushad       0x60    // pushad
#define s1_popad        0x61    // popad
#define s1_pushfd       0x9c    // pushfd
#define s1_popfd        0x9d    // popfd
#define s1_push_esp     0x54    // push esp
#define s1_pop_esp      0x5c    // pop esp
#define s1_push_0d      0x68, s1_0d // push 0x0000
#define s1_mov_ecx_0d   0xb9, s1_0d // mov ecx, 0x0000
#define s1_call_0d      0xe8, s1_0d // call 0x0000

// EOF
