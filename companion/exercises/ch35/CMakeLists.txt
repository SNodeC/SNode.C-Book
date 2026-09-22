add_custom_target(ch35-lab DEPENDS minigateway)
add_test(NAME exercise-ch35 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
  $<TARGET_FILE:minigateway>)
set_tests_properties(exercise-ch35 PROPERTIES TIMEOUT 40)
