add_custom_target(ch13-lab DEPENDS semantic-logging echoserver)
add_test(NAME exercise-ch13-records COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/records.py" $<TARGET_FILE:semantic-logging>)
add_test(NAME exercise-ch13-part-checkpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch12/configuration.py" checkpoint $<TARGET_FILE:echoserver>)
set_tests_properties(exercise-ch13-records exercise-ch13-part-checkpoint PROPERTIES TIMEOUT 40)
