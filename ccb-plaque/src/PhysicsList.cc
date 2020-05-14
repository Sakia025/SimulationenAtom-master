// physics list from example "medical/electronScattering2/src/PhysicsList.cc" without StepMax and G4decay process, extended by radioactive decay

#include "G4EmStandardPhysics.hh"
#include "G4EmStandardPhysics_option1.hh"
#include "G4EmStandardPhysics_option2.hh"
#include "G4EmStandardPhysics_option3.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4EmStandardPhysicsSS.hh"
#include "G4EmStandardPhysicsWVI.hh"
#include "G4EmStandardPhysicsGS.hh"
#include "G4EmLivermorePhysics.hh"
#include "G4EmPenelopePhysics.hh"
#include "G4EmLowEPPhysics.hh"

#include "G4LossTableManager.hh"
#include "G4UnitsTable.hh"

#include "G4ParticleDefinition.hh"
#include "G4ProcessManager.hh"

// Bosons
#include "G4ChargedGeantino.hh"
#include "G4Geantino.hh"
#include "G4Gamma.hh"
#include "G4OpticalPhoton.hh"

// leptons
#include "G4MuonPlus.hh"
#include "G4MuonMinus.hh"
#include "G4NeutrinoMu.hh"
#include "G4AntiNeutrinoMu.hh"

#include "G4Electron.hh"
#include "G4Positron.hh"
#include "G4NeutrinoE.hh"
#include "G4AntiNeutrinoE.hh"

// Hadrons
#include "G4MesonConstructor.hh"
#include "G4BaryonConstructor.hh"
#include "G4IonConstructor.hh"
#include "G4GenericIon.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4SystemOfUnits.hh"

#include "PhysicsList.hh"
#include "PhysicsListMessenger.hh"

PhysicsList::PhysicsList()
    : G4VModularPhysicsList(), fMessenger(0), fEmPhysicsList(0)
{
    fMessenger = new PhysicsListMessenger(this);

    // EM physics
    fEmName = G4String("emstandard_opt4");
    fEmPhysicsList = new G4EmStandardPhysics_option4(1);

    if (verboseLevel > -1)
    {
        G4cout << "PhysicsList::Constructor with default list: <"
               << fEmName << ">" << G4endl;
    }

    radDecayPhysicsList = new G4RadioactiveDecayPhysics();
    G4LossTableManager::Instance();
    SetVerboseLevel(0);
}

PhysicsList::~PhysicsList()
{
    delete fEmPhysicsList;
    delete radDecayPhysicsList;
    delete fMessenger;
}

void PhysicsList::ConstructParticle()
{
    // pseudo-particles
    G4Geantino::GeantinoDefinition();
    G4ChargedGeantino::ChargedGeantinoDefinition();

    // gamma
    G4Gamma::GammaDefinition();

    // optical photon
    G4OpticalPhoton::OpticalPhotonDefinition();

    // leptons
    G4Electron::ElectronDefinition();
    G4Positron::PositronDefinition();
    G4MuonPlus::MuonPlusDefinition();
    G4MuonMinus::MuonMinusDefinition();

    G4NeutrinoE::NeutrinoEDefinition();
    G4AntiNeutrinoE::AntiNeutrinoEDefinition();
    G4NeutrinoMu::NeutrinoMuDefinition();
    G4AntiNeutrinoMu::AntiNeutrinoMuDefinition();

    // mesons
    G4MesonConstructor mConstructor;
    mConstructor.ConstructParticle();

    // barions
    G4BaryonConstructor bConstructor;
    bConstructor.ConstructParticle();

    // ions
    G4IonConstructor iConstructor;
    iConstructor.ConstructParticle();

    // Required by MT even if ion physics not used
    G4GenericIon::GenericIonDefinition();
}

void PhysicsList::ConstructProcess()
{
    AddTransportation();
    fEmPhysicsList->ConstructProcess();
    radDecayPhysicsList -> ConstructProcess();
}

void PhysicsList::AddPhysicsList(const G4String& name)
{
    if (verboseLevel > -1)
    {
        G4cout << "PhysicsList::AddPhysicsList: <" << name << ">" << G4endl;
    }

    if (name == fEmName) return;

    if (name == "emstandard_opt0")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysics(1);
    }
    else if (name == "emstandard_opt1")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysics_option1(1);
    }
    else if (name == "emstandard_opt2")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysics_option2(1);
    }
    else if (name == "emstandard_opt3")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysics_option3(1);
    }
    else if (name == "emstandard_opt4")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysics_option4(1);
    }
    else if (name == "emlowenergy")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmLowEPPhysics(1);
    }
    else if (name == "emstandardSS")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysicsSS(1);
    }
    else if (name == "emstandardWVI")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysicsWVI(1);
    }
    else if (name == "emstandardGS")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmStandardPhysicsGS(1);
    }
    else if (name == "emlivermore")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmLivermorePhysics(1);
    }
    else if (name == "empenelope")
    {
        fEmName = name;
        delete fEmPhysicsList;
        fEmPhysicsList = new G4EmPenelopePhysics(1);
    }
    else
    {
        G4cout << "Error in physics list selection" << G4endl;
    }
}
