#
# Copyright (c) 2020, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

cucim_set_build_shared_libs(OFF)

# Disable visibility to not expose unnecessary symbols
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN YES)

# Set RPATH
if (NOT APPLE)
    set(CMAKE_INSTALL_RPATH $ORIGIN)
endif ()

################################################################################
# Add library: cufile_stub
################################################################################
add_library(cufile_stub
        include/cufile_stub.h
        src/cufile_stub.cpp
        )

set_source_files_properties(src/cufile_stub.cpp PROPERTIES LANGUAGE CUDA)

# Compile options
set_target_properties(cufile_stub
    PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
        CUDA_STANDARD 17
        CUDA_STANDARD_REQUIRED YES
        CUDA_EXTENSIONS NO
        CUDA_SEPARABLE_COMPILATION ON
        CUDA_RUNTIME_LIBRARY Shared
        # To prevent the error message: /usr/bin/ld: ../lib/libcufile_stub.a(cufile_stub.cpp.o): relocation R_X86_64_PC32 against symbol `__fatbinwrap_46_tmpxft_00005869_00000000_6_cufile_stub_cpp1_ii_1e2ddd49' can not be used when making a shared object; recompile with -fPIC
        POSITION_INDEPENDENT_CODE ON
#        SOVERSION ${PROJECT_VERSION_MAJOR}
#        VERSION ${PROJECT_VERSION}
)

# Note: Looks like the following line causes error on CMake 3.18.4 (it is working on 3.18.2). Keeping it for now.
set(CUCIM_REQUIRED_FEATURES cxx_std_17 cuda_std_17)
target_compile_features(cufile_stub PRIVATE ${CUCIM_REQUIRED_FEATURES})
# Use generator expression to avoid `nvcc fatal   : Value '-std=c++17' is not defined for option 'Werror'`
target_compile_options(cufile_stub
    PRIVATE
        $<$<COMPILE_LANGUAGE:CXX>:-Werror -Wall -Wextra>
        )

## Link libraries
    target_link_libraries(cufile_stub
            PUBLIC
                ${CMAKE_DL_LIBS}
            )
# Enabling CUCIM_STATIC_GDS assumes that lib/libcufile_static.a and include/cufile.h is available
# under the current folder.
if (CUCIM_STATIC_GDS)
    add_library(deps::gds_static STATIC IMPORTED GLOBAL)
    set(GDS_STATIC_LIB_PATH ${CMAKE_CURRENT_LIST_DIR}/lib/libcufile_static.a)
    set_target_properties(deps::gds_static PROPERTIES
        IMPORTED_LOCATION "${GDS_STATIC_LIB_PATH}"
        INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_LIST_DIR}/include"
    )
    target_link_libraries(cufile_stub
            PUBLIC
                ${CMAKE_DL_LIBS}
            INTERFACE
                $<BUILD_INTERFACE:deps::gds_static>
            )

    target_compile_definitions(cufile_stub
        PUBLIC
            CUCIM_STATIC_GDS=1
    )
    target_include_directories(cufile_stub
            PUBLIC
                $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/include>
            PRIVATE
                ${CMAKE_CURRENT_SOURCE_DIR}/../cpp/include # for including helper.h in cucim/dynlib
            )
else()
    target_include_directories(cufile_stub
            PUBLIC
                # add path to cufile.h explicitly. ${TOP}/temp/gds would be available by `./run copy_gds_files_`
                $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../temp/gds/lib64>
                $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/include>
            PRIVATE
                ${CMAKE_CURRENT_SOURCE_DIR}/../cpp/include # for including helper.h in cucim/dynlib
            )
endif()

add_library(deps::gds ALIAS cufile_stub)

# Do not generate SONAME as this would be used as a stub library for building on CentOS until cufile has a static library.
# Need to use IMPORTED_NO_SONAME when using this .so file.
# : https://stackoverflow.com/questions/27261288/cmake-linking-shared-c-object-from-externalproject-produces-binaries-with-rel
#set_target_properties(cufile_stub PROPERTIES NO_SONAME 1)
#target_link_options(cufile_stub PRIVATE "LINKER:-soname=cufile.so")
## Build a fake libcufile.so
#set_target_properties(cufile_stub PROPERTIES OUTPUT_NAME "cufile")


#
#################################################################################
## Add tests
#################################################################################
#add_subdirectory(tests)

cucim_restore_build_shared_libs()
