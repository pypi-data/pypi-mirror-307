#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "IPhreeqc::_phreeqc" for configuration "Release"
set_property(TARGET IPhreeqc::_phreeqc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IPhreeqc::_phreeqc PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/_phreeqc.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/_phreeqc.cp312-win_amd64.pyd"
  )

list(APPEND _cmake_import_check_targets IPhreeqc::_phreeqc )
list(APPEND _cmake_import_check_files_for_IPhreeqc::_phreeqc "${_IMPORT_PREFIX}/lib/_phreeqc.lib" "${_IMPORT_PREFIX}/bin/_phreeqc.cp312-win_amd64.pyd" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
