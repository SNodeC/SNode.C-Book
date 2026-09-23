add_custom_target(ch25-lab DEPENDS dispatch-lab)
add_test(NAME exercise-ch25-composition COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch18/dispatch.py" framing $<TARGET_FILE:dispatch-lab>)
set_tests_properties(exercise-ch25-composition PROPERTIES TIMEOUT 30)
