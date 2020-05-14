# ccb-plaque-simulation

Geant4 application for calculating a depth dose profile of the CCB-type ruthenium eye plaque

## Installation and running

1. You need the latest version of the GEANT4 toolkit to compile this application. GEANT4 download and installation instructions: http://geant4.web.cern.ch/geant4/ 
2. Create a folder "ccbPlaque" download the ccb-plaque-simulation source
3. Create a folder "ccbPlaque-build"
4. Go to the bin folder in your GEANT4 installation, e.g. "cd $HOME/geant4/geant4.10.2-install/bin/ "
5. Execute geant4.sh: ". geant4.sh"
5. Go to the build folder "cd pathTo/ccbPlaque-build"
6. Execute cmake e.g. "cmake -DGeant4_DIR=$HOME/geant4/geant4.10.2-install/lib/Geant4-10.2.0 pathTo/ccbPlaque"
7. Execute make "make -j4"
8. Start the macro run1.mac "./ccbPlaque run1.mac"
9. The depth dose will be printed in the terminal.
10. Optional: launch the gui with "./ccbPlaque" without a macro file as parameter.

## Acknowledgments

The geometrical description of the eye plaque is based on the ICRU 72 Report.

The physics list of the simulation is based on the GEANT4 example "medical/electronScattering2".  This software includes software developed by Members of the Geant4 Collaboration ( http://cern.ch/geant4 ).
