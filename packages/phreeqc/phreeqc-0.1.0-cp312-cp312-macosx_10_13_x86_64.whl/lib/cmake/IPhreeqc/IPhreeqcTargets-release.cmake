#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "IPhreeqc::_phreeqc" for configuration "Release"
set_property(TARGET IPhreeqc::_phreeqc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IPhreeqc::_phreeqc PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/_phreeqc.3.6.3.cpython-312-darwin.so"
  IMPORTED_SONAME_RELEASE "@rpath/_phreeqc.3.cpython-312-darwin.so"
  )

list(APPEND _cmake_import_check_targets IPhreeqc::_phreeqc )
list(APPEND _cmake_import_check_files_for_IPhreeqc::_phreeqc "${_IMPORT_PREFIX}/lib/_phreeqc.3.6.3.cpython-312-darwin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
