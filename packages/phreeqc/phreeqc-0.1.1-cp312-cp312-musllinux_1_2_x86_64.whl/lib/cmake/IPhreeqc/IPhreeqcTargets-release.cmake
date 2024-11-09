#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "IPhreeqc::_phreeqc" for configuration "Release"
set_property(TARGET IPhreeqc::_phreeqc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IPhreeqc::_phreeqc PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/_phreeqc.cpython-312-x86_64-linux-musl.so.3.6.3"
  IMPORTED_SONAME_RELEASE "_phreeqc.cpython-312-x86_64-linux-musl.so.3"
  )

list(APPEND _cmake_import_check_targets IPhreeqc::_phreeqc )
list(APPEND _cmake_import_check_files_for_IPhreeqc::_phreeqc "${_IMPORT_PREFIX}/lib/_phreeqc.cpython-312-x86_64-linux-musl.so.3.6.3" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
