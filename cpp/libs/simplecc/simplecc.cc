// simplecc.cc
// 10/18/2014 jichi

#include "simplecc/simplecc.h"
#include "cpputil/cppunicode.h"
#include <utf8.h>
#include <fstream>
#include <unordered_map>
//#include <iostream>

//#define DELIM   '\t' // deliminator of the rule pair

/** Helpers */

namespace { // unnamed

enum : char { CH_COMMENT = '#' }; // beginning of a comment

// http://stackoverflow.com/questions/6140223/c-boost-encode-decode-utf-8
inline void utf8to32(const std::string &src, cpp_u32string &target)
{ utf8::unchecked::utf8to32(src.begin(), src.end(), std::back_inserter(target)); }

} // unnamed namespace

/** Private class */

class SimpleChineseConverterPrivate
{
public:
  typedef std::unordered_map<wchar_t, wchar_t> map_type;
  map_type map;
};

/** Public class */

// Construction

SimpleChineseConverter::SimpleChineseConverter() : d_(new D) {}
SimpleChineseConverter::~SimpleChineseConverter() { delete d_; }

int SimpleChineseConverter::size() const { return d_->map.size(); }
bool SimpleChineseConverter::isEmpty() const { return d_->map.empty(); }

void SimpleChineseConverter::clear() { d_->map.clear(); }

// Initialization
bool SimpleChineseConverter::addFile(const std::wstring &path, bool reverse)
{
#ifdef _MSC_VER
  std::ifstream fin(path);
#else
  std::string spath(path.begin(), path.end());
  std::ifstream fin(spath.c_str());
#endif // _MSC_VER
  if(!fin.is_open())
    return false;
  //fin.imbue(UTF8_LOCALE);

  std::string line;
  cpp_u32string u32line;
  while (std::getline(fin, line)) {
    u32line.clear();
    ::utf8to32(line, u32line);
    if (u32line.size() >= 3 && u32line[0] != CH_COMMENT && !cpp_u32high(u32line[0])) {
      if (reverse) {
        if (!cpp_u32high(u32line[2]))
          d_->map[u32line[2]] = u32line[0];
        if (line.size() >= 5 && !cpp_u32high(u32line[4]))
          d_->map[u32line[4]] = u32line[0];
      } else
        if (!cpp_u32high(u32line[2]))
          d_->map[u32line[0]] = u32line[2];
    }
  }

  fin.close();
  return true;
}

// Conversion

std::wstring SimpleChineseConverter::convert(const std::wstring &text) const
{
  if (text.empty() || d_->map.empty())
    return text;

  std::wstring ret = text;
  D::map_type::iterator p;
  for (size_t i = 0; i < text.size(); i++)
    if (!isascii(text[i])) { // only convert kanji
      p = d_->map.find(text[i]);
      if (p != d_->map.end())
        ret[i] = p->second;
    }
  return ret;
}

// EOF
