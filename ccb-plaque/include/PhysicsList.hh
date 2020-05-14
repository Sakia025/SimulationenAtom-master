#ifndef PhysicsList_h
#define PhysicsList_h 1

#include "G4VModularPhysicsList.hh"
#include "globals.hh"

class G4VPhysicsConstructor;
class PhysicsListMessenger;

class PhysicsList: public G4VModularPhysicsList
{
public:
    PhysicsList();
    virtual ~PhysicsList();
    virtual void ConstructParticle();
    void AddPhysicsList(const G4String& name);
    virtual void ConstructProcess();

private:
    PhysicsListMessenger* fMessenger;
    G4String fEmName;
    G4VPhysicsConstructor*  fEmPhysicsList;
    G4VPhysicsConstructor* radDecayPhysicsList;
};

#endif
