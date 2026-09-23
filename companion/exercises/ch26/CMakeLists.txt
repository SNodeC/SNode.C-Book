add_custom_target(ch26-lab DEPENDS persistence-lab minigateway)
add_test(NAME exercise-ch26-part-checkpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch24/database.py" checkpoint $<TARGET_FILE:persistence-lab> $<TARGET_FILE:minigateway>)
set_tests_properties(exercise-ch26-part-checkpoint PROPERTIES TIMEOUT 120 LABELS equipped)
