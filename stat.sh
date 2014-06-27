#!/bin/bash
# 8/6/2013 jichi
#set +x
echo Line numbers for different languages

echo -n Total:
find . -type f \( \
  -name '*.*' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n Python:
find . -type f \( \
  -name '*.py' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n C/C++:
find . -type f \( \
  -name '*.h' \
  -o -name '*.c' \
  -o -name '*.cc' \
  -o -name '*.cpp' \
  -o -name '*.pro' \
  -o -name '*.pri' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n QML:
find . -type f \( \
  -name '*.qml' \
  -o -name 'qmldir' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n HTML/CSS/Javascript:
find . -type f \( \
  -name '*.html' \
  -o -name '*.haml' \
  -o -name '*.css' \
  -o -name '*.js' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n Ruby/HAML/SASS/Coffee:
find . -type f \( \
  -name '*.rb' \
  -o -name '*.sass' \
  -o -name '*.coffee' \
  -o -name '*.haml' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n XML/YAML:
find . -type f \( \
  -name '*.xml' \
  -o -name '*.yaml' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n CMD/Shell/Makefile:
find . -type f \( \
  -name '*.cmd' \
  -o -name '*.sh' \
  -o -name Makefile \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

echo -n TS:
find . -type f \( \
  -name '*.ts' \
  \) | xargs wc -l | tail -1 | sed 's/ total//'

exit

# EOF

# 6/25/2014
Line numbers for different languages
Total:  478897
Python:   93184
C/C++:   71457
QML:   18468
HTML/CSS/Javascript:   13475
Ruby/HAML/SASS/Coffee:    5796
XML/YAML:    2032
CMD/Shell/Makefile:    1473
TS:   46276
