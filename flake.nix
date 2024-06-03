{
  inputs = { nixpkgs.url = "nixpkgs/nixos-unstable"; };

  outputs = { self, ... }@inputs:
    with inputs;
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (pkgs) python311;

      propagatedBuildAndShellInputs = with python311.pkgs; [
        nox
        numpy
        pytest
        opencv4
        matplotlib
        pysdl2
        #pytesseract
        #tesserocr
        python-lsp-server
      ];

      propagatedBuildInputs = with python311.pkgs; [
        opencv4
        pytesseract
        tesserocr
        python-lsp-server
      ];

      nativeBuildAndShellInputs = with pkgs; [
        pkg-config
        #gtk2
        #gtk2-x11
        opencv
        SDL2
        tesseract
      ];

      language = with pkgs; [ autopep8 coverage pylsp-mypy python-lsp-server ];

      pythonTools = with python311.pkgs; [
        autopep8
        coverage
        flake8
        ipython
        mypy
        nox
        pylsp-mypy
        pytest
        python-lsp-server
      ];

      tools = with pkgs; [ imagemagick plantuml graphviz ];
    in {
      hydraJobs = { inherit (self) packages; };

      devShells.${system} = {
        default = pkgs.mkShell {
          nativeBuildInputs = nativeBuildAndShellInputs
            ++ propagatedBuildAndShellInputs ++ tools ++ pythonTools
            ++ (with pkgs; [ ]);
        };

        venv = pkgs.mkShell { nativeBuildInputs = with pkgs; [ python311 ]; };
      };
    };
}
