with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "pynel";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    # MicroPython 1.17 is closer to Python 3.4, but that's no longer
    # available in nixpkgs
    (python37.withPackages (pypkgs: [ pypkgs.pip pypkgs.virtualenv ]))
    pipenv
  ];
  shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
  '';
}


