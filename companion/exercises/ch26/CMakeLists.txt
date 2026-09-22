add_custom_target(ch26-lab DEPENDS echoserver echoclient)
foreach(mode IN ITEMS lifecycle configuration)
  add_test(NAME exercise-ch26-${mode} COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/installed.py" ${mode})
  set_tests_properties(exercise-ch26-${mode} PROPERTIES TIMEOUT 180)
endforeach()
