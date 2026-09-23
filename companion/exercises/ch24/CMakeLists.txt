add_custom_target(ch24-lab DEPENDS dispatch-lab persistence-lab minigateway)
add_test(NAME exercise-ch24-composition COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch17/dispatch.py" framing $<TARGET_FILE:dispatch-lab>)
set_tests_properties(exercise-ch24-composition PROPERTIES TIMEOUT 180)
add_test(NAME exercise-ch24-part-checkpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch23/database.py" checkpoint $<TARGET_FILE:persistence-lab> $<TARGET_FILE:minigateway>)
set_tests_properties(exercise-ch24-part-checkpoint PROPERTIES TIMEOUT 180 LABELS equipped)
