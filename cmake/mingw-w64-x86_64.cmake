# Toolchain file: cross-compile for 64-bit Windows from Linux/WSL with MinGW-w64
# (apt install mingw-w64)

set(CMAKE_SYSTEM_NAME      Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(TOOLCHAIN_PREFIX x86_64-w64-mingw32)

# Use the "posix" thread-model variants: they support std::thread / std::mutex,
# which wxWidgets and modern C++ code need (the "win32" variants may not).
set(CMAKE_C_COMPILER   ${TOOLCHAIN_PREFIX}-gcc-posix)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}-g++-posix)
set(CMAKE_RC_COMPILER  ${TOOLCHAIN_PREFIX}-windres)

# Search for libraries/headers only in the MinGW sysroot, never in the
# Linux system dirs (so the Linux wxWidgets is never picked up by mistake)
set(CMAKE_FIND_ROOT_PATH /usr/${TOOLCHAIN_PREFIX})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Prebuilt wxWidgets for MinGW (built and installed once, shared by all
# projects). Override with -DWX_MINGW_ROOT=... or the WX_MINGW_ROOT env var.
if (NOT WX_MINGW_ROOT)
    if (DEFINED ENV{WX_MINGW_ROOT})
        set(WX_MINGW_ROOT "$ENV{WX_MINGW_ROOT}")
    else ()
        set(WX_MINGW_ROOT "$ENV{HOME}/opt/wxWidgets-3.2.6-mingw64")
    endif ()
endif ()
list(APPEND CMAKE_FIND_ROOT_PATH "${WX_MINGW_ROOT}")
list(APPEND CMAKE_PREFIX_PATH    "${WX_MINGW_ROOT}")
