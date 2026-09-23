add_custom_target(ch07-lab DEPENDS echoserver)
add_test(NAME exercise-ch07-independent-peers COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch01/independent-peers.py" $<TARGET_FILE:echoserver>)
add_test(NAME exercise-ch07-occupied-endpoint COMMAND "${Python3_EXECUTABLE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../ch03/occupied-port.py" $<TARGET_FILE:echoserver>)
set_tests_properties(exercise-ch07-independent-peers exercise-ch07-occupied-endpoint PROPERTIES TIMEOUT 180)
