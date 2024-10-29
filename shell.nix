{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.numpy
    pkgs.python311Packages.pandas
    pkgs.python311Packages.matplotlib
    pkgs.python311Packages.yfinance
    pkgs.python311Packages.jupyter
    pkgs.python311Packages.flask
  ];

  shellHook = ''
    echo "Development environment with Python 3.9, numpy, yfinance, pandas, and matplotlib is ready."
  '';
}
