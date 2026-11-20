cmake_minimum_required(VERSION 3.28)
project(gui_ex_05_a VERSION 1.0.0)

# Product metadata - used for the .exe version info, the About box and the
# Windows installer (installer/installer.nsi)
set(APP_DISPLAY_NAME "wxWidgets Showcase")
set(APP_PUBLISHER    "wxShowcase")
set(APP_COPYRIGHT    "(C) 2026")

if (WIN32)
    enable_language(RC)   # icon, manifest and version info (resources/app.rc)
endif ()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- wxWidgets ---------------------------------------------------------------
# Use an installed wxWidgets if available (e.g. apt install libwxgtk3.2-dev),
# otherwise download and build it automatically (first build takes a while).
# For the MinGW cross-build, a prebuilt wxWidgets install is used (see
# WX_MINGW_ROOT in cmake/mingw-w64-x86_64.cmake); it ships a CMake config.
if (WIN32)
    find_package(wxWidgets 3.2 CONFIG QUIET COMPONENTS core base)
else ()
    find_package(wxWidgets 3.2 QUIET COMPONENTS core base)
endif ()

if (TARGET wx::core)
    message(STATUS "Using prebuilt wxWidgets from ${wxWidgets_DIR}")
    set(WX_LIBS wx::core wx::base)
elseif (wxWidgets_FOUND)
    include(${wxWidgets_USE_FILE})
    set(WX_LIBS ${wxWidgets_LIBRARIES})
else ()
    message(STATUS "wxWidgets not found - fetching it from GitHub")
    include(FetchContent)
    set(wxBUILD_SHARED OFF CACHE BOOL "" FORCE)   # link statically
    set(wxBUILD_SAMPLES OFF CACHE STRING "" FORCE)
    set(wxBUILD_TESTS OFF CACHE STRING "" FORCE)
    set(wxBUILD_DEMOS OFF CACHE BOOL "" FORCE)
    FetchContent_Declare(
        wxWidgets
        GIT_REPOSITORY https://github.com/wxWidgets/wxWidgets.git
        GIT_TAG        v3.2.6
        GIT_SHALLOW    TRUE
    )
    FetchContent_MakeAvailable(wxWidgets)
    set(WX_LIBS wx::core wx::base)
endif ()

# --- Executable --------------------------------------------------------------
# Put the built executable into <project>/exe/<platform>
#   Linux   -> exe/linux
#   Windows -> exe/windows  (native Windows build or MinGW cross-compile)
if (WIN32)
    set(EXE_PLATFORM windows)
elseif (APPLE)
    set(EXE_PLATFORM macos)
else ()
    set(EXE_PLATFORM linux)
endif ()
set(EXE_OUTPUT_DIR ${CMAKE_SOURCE_DIR}/exe/${EXE_PLATFORM})

configure_file(resources/version.h.in ${CMAKE_BINARY_DIR}/generated/version.h @ONLY)

add_executable(gui_ex_05_a main.cpp MainFrame.cpp MainFrame.h)
target_link_libraries(gui_ex_05_a PRIVATE ${WX_LIBS})
target_include_directories(gui_ex_05_a PRIVATE ${CMAKE_BINARY_DIR}/generated)

if (WIN32)
    target_sources(gui_ex_05_a PRIVATE resources/app.rc)
    # let the resource compiler find app.ico / app.manifest
    target_include_directories(gui_ex_05_a PRIVATE
        $<$<COMPILE_LANGUAGE:RC>:${CMAKE_SOURCE_DIR}/resources>)
endif ()

# MinGW: link the GCC runtime statically so the .exe runs on Windows
# without needing extra DLLs (libstdc++, libgcc, libwinpthread)
if (MINGW)
    target_link_options(gui_ex_05_a PRIVATE -static -static-libgcc -static-libstdc++
                                            $<$<CONFIG:Release>:-s>)   # strip release builds
endif ()

set_target_properties(gui_ex_05_a PROPERTIES
    WIN32_EXECUTABLE TRUE            # no console window on Windows
    RUNTIME_OUTPUT_DIRECTORY         ${EXE_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY_DEBUG   ${EXE_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${EXE_OUTPUT_DIR}
)

# --- Windows installer ---------------------------------------------------------
# cmake --build --preset windows-release --target installer
#   -> dist/gui_ex_05_a-<version>-win64-setup.exe
# Needs NSIS (Linux/WSL: sudo apt install nsis, Windows: https://nsis.sourceforge.io).
if (WIN32)
    find_program(MAKENSIS_EXECUTABLE makensis
                 PATHS "$ENV{ProgramFiles\(x86\)}/NSIS" "$ENV{ProgramFiles}/NSIS")
    if (MAKENSIS_EXECUTABLE)
        set(DIST_DIR ${CMAKE_SOURCE_DIR}/dist)
        add_custom_target(installer
            COMMAND ${CMAKE_COMMAND} -E make_directory ${DIST_DIR}
            COMMAND ${MAKENSIS_EXECUTABLE} -V2 -INPUTCHARSET UTF8
                    "-DAPP_VERSION=${PROJECT_VERSION}"
                    "-DAPP_NAME=${APP_DISPLAY_NAME}"
                    "-DAPP_PUBLISHER=${APP_PUBLISHER}"
                    "-DAPP_COPYRIGHT=${APP_COPYRIGHT}"
                    "-DAPP_EXE_SRC=$<TARGET_FILE:gui_ex_05_a>"
                    "-DOUT_DIR=${DIST_DIR}"
                    ${CMAKE_SOURCE_DIR}/installer/installer.nsi
            DEPENDS gui_ex_05_a
            COMMENT "Building Windows installer in ${DIST_DIR}"
            VERBATIM)
    else ()
        message(STATUS "makensis not found - 'installer' target disabled (sudo apt install nsis)")
    endif ()
endif ()
