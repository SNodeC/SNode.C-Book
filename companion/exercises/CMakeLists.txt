find_package(Python3 REQUIRED COMPONENTS Interpreter)
foreach(chapter IN ITEMS ch01 ch03 ch23 ch35 ch37)
  add_subdirectory(${chapter})
endforeach()
