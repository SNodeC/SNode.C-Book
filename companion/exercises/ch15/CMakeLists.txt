add_custom_target(ch15-lab DEPENDS echoclient tls-policy-lab)
add_test(NAME exercise-ch15-bounded-retry COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/recovery.py" retry $<TARGET_FILE:echoclient>)
add_test(NAME exercise-ch15-part-checkpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/recovery.py" checkpoint $<TARGET_FILE:echoclient>
  $<TARGET_FILE:tls-policy-lab>)
set_tests_properties(exercise-ch15-bounded-retry exercise-ch15-part-checkpoint PROPERTIES TIMEOUT 180)
