add_custom_target(ch22-lab DEPENDS mqtt-role-lab mqtt-broker-lab minigateway)
add_test(NAME exercise-ch22-unavailable-output COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch28/solution.py" $<TARGET_FILE:minigateway>)
add_test(NAME exercise-ch22-part-checkpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch20/mqtt.py" checkpoint $<TARGET_FILE:mqtt-role-lab> $<TARGET_FILE:mqtt-broker-lab> $<TARGET_FILE:minigateway>)
set_tests_properties(exercise-ch22-unavailable-output exercise-ch22-part-checkpoint PROPERTIES TIMEOUT 60)
