//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
//
/// \file B3aRunAction.hh
/// \brief Definition of the B3aRunAction class

#ifndef B3aRunAction_h
#define B3aRunAction_h 1

#include "G4UserRunAction.hh"
#include "G4Accumulable.hh"
#include "globals.hh"
#include "meine_globalen_Variablen.hh"
#include <vector>


class G4Run;
class G4LogicalVolume;
class RunActionMessenger;
/// Run action class

class B3aRunAction : public G4UserRunAction, public meine_globalen_Variablen
{
  public:
    B3aRunAction();
    virtual ~B3aRunAction();

    //virtual G4Run* GenerateRun(); //kam aus dem abspeichern von Henning, brauch ich das wirklich?
    virtual void BeginOfRunAction(const G4Run*);
    virtual void   EndOfRunAction(const G4Run*);

    void CountEvent()           { fGoodEvents += 1; };
    void SumDose(G4double dose) { fSumDose += dose; };
    void SumDose_eyeparts(G4double dose, G4int nr) { fSumDose_eyeparts[nr] += dose; };
    // Histogram name
    void SetFileName(G4String& val);
private:
    G4Accumulable<G4int>    fGoodEvents;
    G4Accumulable<G4double> fSumDose;
    std::vector<G4Accumulable<G4double>> fSumDose_eyeparts;

    RunActionMessenger*     fRunMessenger;
    G4String fFileName;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif
