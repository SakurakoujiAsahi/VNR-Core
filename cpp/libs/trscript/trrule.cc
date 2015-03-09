// trrule.cc
// 9/20/2014 jichi

#include "trscript/trrule.h"
#include "trscript/trescape.h"
#include "cpputil/cppregex.h"
//#include <QDebug>

#define SK_NO_QT
#define DEBUG "trrule.cc"
#include "sakurakit/skdebug.h"

// Construction

void TranslationScriptRule::init(const param_type &param, bool precompile_regex)
{
  id = param.id;
  category = param.category;
  source = param.source;
  target = param.target;

  if (param.f_icase)
    flags |= IcaseFlag;
  if (param.f_force)
    flags |= ForceFlag;

  if (param.f_regex) {
    flags |= RegexFlag;
    if (precompile_regex)
      try {
        cache_re();
      } catch (...) { // boost::bad_pattern
        DWERR("invalid term: " << param.id << ", regex pattern: " << param.source);
        valid = false;
        return;
      }
  }

  valid = true; // must do this at the end
}

void TranslationScriptRule::init_list(const param_type &param,
     param_list::const_iterator begin, param_list::const_iterator end)
{
  enum { precompile_regex = false }; // delay compiling regex
  init(param);
  if (!valid)
    return;
  child_count = std::distance(begin, end);
  if (child_count) {
    children = new Self[child_count];
    for (size_t pos = 0; pos < child_count; pos++)
      children[pos].init(*begin++, precompile_regex);
    flags |= ListFlag; // must do this at last
  }
}

// Render

// A sample expected output without escape:
// <a href='json://{"type":"term","id":12345,"source":"pattern","target":"text"}'>pattern</a>
std::wstring TranslationScriptRule::render_target(const std::wstring &matched_text) const
{
  if (id.empty()) // do not render mark if there is no termid
    return L"<u>" + target + L"</u>";

  std::wstring ret = L"{\"type\":\"term\"";
  ret.append(L",\"id\":")
     .append(id);

  std::wstring ws = matched_text;
  if (ws.empty() && !is_regex()) // do not save regex pattern to save memory
    ws = source;
  if (!ws.empty()) {
    std::string s = ::trescape(ws);
    ret.append(L",\"source\":\"")
       .append(s.cbegin(), s.cend())
       .push_back('"');
  }

  if (!target.empty()) {
    std::string s = ::trescape(target);
    ret.append(L",\"target\":\"")
       .append(s.cbegin(), s.cend())
       .push_back('"');
  }
  ret.push_back('}');

  ret.insert(0, L"<a href='json://");
  ret.push_back('\'');

  //if (!markStyle.empty())
  //  ret.append(" style=\"")
  //     .append(markStyle)
  //     .append("\"");

  ret.push_back('>');
  ret.append(target)
     .append(L"</a>");
  return ret;
}

// Replacement

void TranslationScriptRule::string_replace(std::wstring &ret, bool mark) const
{
  if (target.empty()) {
    if (is_icase())
      boost::ierase_all(ret, source);
    else
      boost::erase_all(ret, source);
  } else {
    std::wstring repl = mark ? render_target() : target;
    if (is_icase())
      boost::ireplace_all(ret, source, repl);
    else
      boost::replace_all(ret, source, repl);
  }
}

void TranslationScriptRule::regex_replace(std::wstring &ret, bool mark) const
{
  try {
    // match_default is the default value
    // format_all is needed to enable all features, but it is sligntly slower
    cache_re();
    if (target.empty() || !mark)
      ret = boost::regex_replace(ret, *source_re, target,
          boost::match_default|boost::format_all);
    else {
      auto repl = [this](const boost::wsmatch &m) {
        return render_target(m[0]);
      };
      ret = boost::regex_replace(ret, *source_re, repl,
          boost::match_default|boost::format_all);
    }
  } catch (...) {
    DWERR("invalid term: " << id << ", regex pattern: " << source);
    valid = false;
  }
}

bool TranslationScriptRule::regex_exists(const std::wstring &t) const
{
  try {
    cache_re();
    return ::cpp_regex_contains(t, *source_re);
  } catch (...) {
    DWERR("invalid term: " << id << ", regex pattern: " << source);
    valid = false;
    return false;
  }
}

bool TranslationScriptRule::children_replace(std::wstring &ret, bool mark) const
{
  if (child_count && children)
    for (size_t i = 0; i < child_count; i++) {
      const auto &c = children[i];
      if (c.is_valid() && c.replace(ret, mark) && !exists(ret))
        return true;
    }
  return false;
}

// EOF
