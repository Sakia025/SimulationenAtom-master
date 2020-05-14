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
/// \file B3aRunAction.cc
/// \brief Implementation of the B3aRunAction class

#include "B3aRunAction.hh"
#include "B3PrimaryGeneratorAction.hh"

#include "G4RunManager.hh"
#include "G4Run.hh"
#include "G4AccumulableManager.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include "meine_globalen_Variablen.hh"
#include "RunActionMessenger.hh"

#include <fstream>
#include <iostream>


meine_globalen_Variablen* obj = new meine_globalen_Variablen();
std::vector<std::string> model_names = obj->model_names_;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B3aRunAction::B3aRunAction()
 : G4UserRunAction(),
   fGoodEvents(0),
   fSumDose(0.),
   fSumDose_eyeparts(model_names.size(), 0.)
{
  fRunMessenger = new RunActionMessenger(this);
  //fFileName = "standardEnergy.dat";
  //add new units for dose
  //
  const G4double milligray = 1.e-3*gray;
  const G4double microgray = 1.e-6*gray;
  const G4double nanogray  = 1.e-9*gray;
  const G4double picogray  = 1.e-12*gray;

  new G4UnitDefinition("milligray", "milliGy" , "Dose", milligray);
  new G4UnitDefinition("microgray", "microGy" , "Dose", microgray);
  new G4UnitDefinition("nanogray" , "nanoGy"  , "Dose", nanogray);
  new G4UnitDefinition("picogray" , "picoGy"  , "Dose", picogray);


  // Register accumulable to the accumulable manager
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->RegisterAccumulable(fGoodEvents);
  accumulableManager->RegisterAccumulable(fSumDose);  //not needed, from B3a example

  //my Eye Detectors
  for (int i = 0; i < (int)fSumDose_eyeparts.size(); i++)
  {
    accumulableManager->RegisterAccumulable(fSumDose_eyeparts[i]);
  }

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B3aRunAction::~B3aRunAction()
{
  delete fRunMessenger;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B3aRunAction::SetFileName(G4String& val)
{
  fFileName = val;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
/*
G4Run* B1RunAction::GenerateRun()
{
  return new B1Run;
}
*/
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B3aRunAction::BeginOfRunAction(const G4Run* run)
{
  G4cout << "### Run " << run->GetRunID() << " start." << G4endl;

  // reset accumulables to their initial values
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->Reset();

  //inform the runManager to save random number seed
  G4RunManager::GetRunManager()->SetRandomNumberStore(false);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B3aRunAction::EndOfRunAction(const G4Run* run)
{
  G4int nofEvents = run->GetNumberOfEvent();
  if (nofEvents == 0) return;

  // Merge accumulables
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->Merge();


  // Print results
  //

  if (IsMaster())
  {
    G4cout
     << G4endl
     << "--------------------End of Global Run-----------------------"
     << G4endl
     << "  The run was " << nofEvents << " events ";
  }

  //Output Filename wird mit set/commands SetFilenames in der run_.mac gesetzt
  std::ofstream myfile(fFileName, std::ofstream::app);
  std::cout << fFileName;
  for(int i = 0; i < (int)fSumDose_eyeparts.size(); i++){
    myfile << "Dose in ," << std::string(model_names[i])<< ", " << G4BestUnit(fSumDose_eyeparts[i].GetValue(),"Dose") << G4endl;
  }

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
