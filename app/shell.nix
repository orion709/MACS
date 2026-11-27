{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    libxkbcommon
    libglvnd
    stdenv.cc.cc.lib
    xorg.libX11
    xorg.libxcb
    xorg.libXext
    xorg.libXrender
    xorg.libXi
    xorg.libXrandr
    xorg.libXfixes
    xorg.libXcursor
    xorg.libXinerama
    xorg.libXau
    xorg.libXdmcp
    libxcb-cursor
    fontconfig
    freetype
    glib
    dbus
    zstd
    libxcb-cursor
    xcb-util-wm
    libxcb-util
    xcb-util-image
    xcb-util-keysyms
    xcb-util-renderutil
    zlib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
      pkgs.libxkbcommon
      pkgs.libglvnd
      pkgs.stdenv.cc.cc.lib
      pkgs.xorg.libX11
      pkgs.xorg.libxcb
      pkgs.xorg.libXext
      pkgs.xorg.libXrender
      pkgs.xorg.libXi
      pkgs.xorg.libXrandr
      pkgs.xorg.libXfixes
      pkgs.xorg.libXcursor
      pkgs.xorg.libXinerama
      pkgs.xorg.libXau
      pkgs.xorg.libXdmcp
      pkgs.libxcb-cursor
      pkgs.fontconfig
      pkgs.freetype
      pkgs.glib
      pkgs.dbus
      pkgs.zstd
      pkgs.libxcb-cursor
      pkgs.xcb-util-wm
      pkgs.libxcb-util
      pkgs.xcb-util-image
      pkgs.xcb-util-keysyms
      pkgs.xcb-util-renderutil
      pkgs.zlib
    ]}:/run/opengl-driver/lib''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  '';
}