find_package(Python3 REQUIRED COMPONENTS Interpreter)
foreach(chapter IN ITEMS ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 ch13 ch14 ch15 ch18 ch28 ch30)
  add_subdirectory(${chapter})
endforeach()
