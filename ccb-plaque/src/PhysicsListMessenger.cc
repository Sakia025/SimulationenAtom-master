#include "G4UIdirectory.hh"
#include "G4UIcmdWithAString.hh"

#include "PhysicsListMessenger.hh"
#include "PhysicsList.hh"

PhysicsListMessenger::PhysicsListMessenger(PhysicsList* pPhys)
    : G4UImessenger(), fPhysicsList(pPhys),
      fPListCmd(0)
{
    fPhysDir = new G4UIdirectory("/ccb/phys/");
    fPhysDir->SetGuidance("physics list commands");

    fPListCmd = new G4UIcmdWithAString("/ccb/phys/addPhysics", this);
    fPListCmd->SetGuidance("Add modula physics list.");
    fPListCmd->SetParameterName("PList", false);
    fPListCmd->AvailableForStates(G4State_PreInit);
    fPListCmd->SetToBeBroadcasted(false);
}

PhysicsListMessenger::~PhysicsListMessenger()
{
    delete fPListCmd;
    delete fPhysDir;
}

void PhysicsListMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if( command == fPListCmd )
    {
        fPhysicsList->AddPhysicsList(newValue);
    }
}
