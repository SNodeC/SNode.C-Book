add_custom_target(ch16-lab DEPENDS dispatch-lab)
foreach(mode IN ITEMS framing limits)
  add_test(NAME exercise-ch16-${mode} COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/../ch17/dispatch.py" ${mode} $<TARGET_FILE:dispatch-lab>)
  set_tests_properties(exercise-ch16-${mode} PROPERTIES TIMEOUT 180)
endforeach()
