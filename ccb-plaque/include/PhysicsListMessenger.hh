#ifndef PhysicsListMessenger_h
#define PhysicsListMessenger_h 1

#include "G4UImessenger.hh"
#include "globals.hh"

class PhysicsList;
class G4UIdirectory;
class G4UIcmdWithAString;

class PhysicsListMessenger: public G4UImessenger
{
public:
    PhysicsListMessenger(PhysicsList* );
    virtual ~PhysicsListMessenger();
    virtual void SetNewValue(G4UIcommand*, G4String);

private:
    PhysicsList* fPhysicsList;
    G4UIdirectory*             fPhysDir;
    G4UIcmdWithAString*        fPListCmd;
};

#endif
