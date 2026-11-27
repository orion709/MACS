
{ pkgs ? import <nixpkgs> {} }:

let
  libs = with pkgs; [
    # C++ / OpenGL
    stdenv.cc.cc.lib
    libglvnd
    libxkbcommon

    # X11
    libx11
    libxcb
    libxext
    libxrender
    libxi
    libxrandr
    libxfixes
    libxcursor
    libxinerama
    libxau
    libxdmcp

    # XCB / Qt6
    libxcb-cursor
    libxcb-wm
    libxcb-util
    libxcb-image
    libxcb-keysyms
    libxcb-render-util

    # Wayland
    wayland
    libxkbcommon

    # Other
    fontconfig
    freetype
    glib
    dbus
    zlib
    zstd
    expat
    libpng
  ];

in pkgs.mkShell {
  packages = libs;

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath libs}:/run/opengl-driver/lib''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

    # Не даём системным Qt-плагинам конфликтовать с PyQt6.
    unset QT_PLUGIN_PATH
    unset QT_QPA_PLATFORM_PLUGIN_PATH
  '';
}
