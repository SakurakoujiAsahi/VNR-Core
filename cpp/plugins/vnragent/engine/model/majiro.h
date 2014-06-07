#pragma once

// majiro.h
// 4/20/2014 jichi

#include "engine/engine.h"
#include "util/codepage.h"

class MajiroEngine : public AbstractEngine
{
  SK_EXTEND_CLASS(MajiroEngine, AbstractEngine)
  SK_DISABLE_COPY(MajiroEngine)

  static void hookFunction(HookStack *stack);
public:
  MajiroEngine()
    : Base("Majiro", Util::SjisCodePage, BlockingAttribute)
  { setHookFunction(hookFunction); }

  static bool match();
protected:
  bool attach() override;
  //bool detach() override;
};

// EOF