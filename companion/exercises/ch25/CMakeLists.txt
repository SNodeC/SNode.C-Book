# Repeat the public environment experiment at the component-ownership boundary.
add_custom_target(ch25-lab DEPENDS ch02-lab)
foreach(mode IN ITEMS consumer component)
  add_test(NAME exercise-ch25-${mode} COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/../ch02/solution.py" ${mode})
  set_tests_properties(exercise-ch25-${mode} PROPERTIES TIMEOUT 180)
endforeach()
