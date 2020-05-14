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
/// \file B3aEventAction.cc
/// \brief Implementation of the B3aEventAction class

#include "B3aEventAction.hh"
#include "B3aRunAction.hh"

#include "G4RunManager.hh"
#include "G4Event.hh"

#include "G4SDManager.hh"
#include "G4HCofThisEvent.hh"
#include "G4THitsMap.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include "meine_globalen_Variablen.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

meine_globalen_Variablen* obj_EA = new meine_globalen_Variablen();
std::vector<std::string> model_names_EA = obj_EA->model_names_;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B3aEventAction::B3aEventAction(B3aRunAction* runAction)
 : G4UserEventAction(),
   fRunAction(runAction),
   fCollID_eyeparts(model_names_EA.size(), -1) //sets all the ID's of all the eyepart detectors to -1
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B3aEventAction::~B3aEventAction()
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B3aEventAction::BeginOfEventAction(const G4Event* /*evt*/)
{ }


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B3aEventAction::EndOfEventAction(const G4Event* evt )
{
   //Hits collections
  //
  G4HCofThisEvent* HCE = evt->GetHCofThisEvent();
  if(!HCE) return;

   // Get hits collections IDs
  if(fCollID_eyeparts[0] < 0){
    fCollID_eyeparts = B3aEventAction::setCollIDs();
  }

  //meine Dose deposit in eyeparts
  std::map<G4int,G4double*>::iterator itr;
  std::vector<G4double> eye_doses(model_names_EA.size(), 0.);
  G4double eye_dose = 0.;
  std::vector<G4THitsMap<G4double>*> evtMaps;
  //std::cout << "o00o0o0o0o0o0o0o0o0o0o0o000o0o0o0o0o00o0o0o00o0o00o0" << std::endl;
  for(int i = 0; i < int(fCollID_eyeparts.size()); i++)
  {
    eye_dose = 0.;
    evtMaps.push_back((G4THitsMap<G4double>*)(HCE->GetHC(fCollID_eyeparts[i])));
    for (itr = evtMaps[i]->GetMap()->begin(); itr != evtMaps[i]->GetMap()->end(); itr++)
    {
      eye_dose = *(itr->second);  //siehe B3a basic example
    }
    eye_doses[i] = eye_dose;  //das hier wäre nicht nötig im nächsten if kann man auch einfach eye_dose schreiben, aber vlt sehe ich enfach gerade den Grnd nicht mehr, es schadet jedenfalls nicht

    if (eye_doses[i] > 0.) fRunAction->SumDose_eyeparts(eye_doses[i], i);
  }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

std::vector<G4int> B3aEventAction::setCollIDs()
{
  G4SDManager* SDMan = G4SDManager::GetSDMpointer();
  std::vector<G4int> fCollID_eyeparts_init;
  G4int eyes_ID;

  for(unsigned long int i = 0; i < model_names_EA.size(); i++)
  {
    eyes_ID = SDMan->GetCollectionID("my_" + std::string(model_names_EA[i]) + "_Scorer/TotalDose");
    fCollID_eyeparts_init.push_back(eyes_ID);
  }
  return fCollID_eyeparts_init;
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
