find_package(Python3 REQUIRED COMPONENTS Interpreter)
foreach(chapter IN ITEMS ch01 ch02 ch03 ch18 ch28 ch30)
  add_subdirectory(${chapter})
endforeach()
