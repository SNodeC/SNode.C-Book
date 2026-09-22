add_custom_target(ch27-lab DEPENDS ch26-lab)
foreach(mode IN ITEMS diagnosis checkpoint)
  add_test(NAME exercise-ch27-${mode} COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/../ch26/installed.py" ${mode})
  set_tests_properties(exercise-ch27-${mode} PROPERTIES TIMEOUT 300)
endforeach()
