add_custom_target(ch23-lab DEPENDS sse-server sse-eventsource-client)
add_test(NAME exercise-ch23 COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/solution.py"
  $<TARGET_FILE:sse-server>)
set_tests_properties(exercise-ch23 PROPERTIES TIMEOUT 40)
