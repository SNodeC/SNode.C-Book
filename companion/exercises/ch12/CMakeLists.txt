# Reuse the canonical EchoPair; configuration belongs to its existing public surface.
add_custom_target(ch12-lab DEPENDS echoserver)
foreach(mode IN ITEMS precedence discovery)
  add_test(NAME exercise-ch12-${mode} COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/configuration.py" ${mode} $<TARGET_FILE:echoserver>)
  set_tests_properties(exercise-ch12-${mode} PROPERTIES TIMEOUT 180)
endforeach()
