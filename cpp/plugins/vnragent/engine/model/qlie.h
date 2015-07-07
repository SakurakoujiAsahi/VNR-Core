#pragma once

// qlie.h
// 7/5/2015 jichi

#include "engine/enginemodel.h"

class QLiEEngine : public EngineModel
{
  SK_EXTEND_CLASS(QLiEEngine, EngineModel)
  static bool attach();
  static QString rubyCreate(const QString &rb, const QString &rt);
  static QString rubyRemove(const QString &text);

public:
  QLiEEngine()
  {
    name = "EmbedQLiE";
    enableDynamicEncoding = true;
    newLineString = "[n]";
    matchFiles << "GameData/*.pack";
    attachFunction = &Self::attach;
    rubyCreateFunction = &Self::rubyCreate;
    rubyRemoveFunction = &Self::rubyRemove;
  }
};

// EOF