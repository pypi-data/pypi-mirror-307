#include "BDSBunchSixTrackLink.hh"
#include "BDSException.hh"
#include "BDSIMLink.hh"
#include "BDSIonDefinition.hh"
#include "BDSParticleCoordsFull.hh"
#include "BDSParticleDefinition.hh"
#include "BDSPhysicsUtilities.hh"

#include "G4Electron.hh"
#include "G4GenericIon.hh"
#include "G4IonTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4ParticleTable.hh"
#include "G4Types.hh"

#include "CLHEP/Units/PhysicalConstants.h"
#include "CLHEP/Units/SystemOfUnits.h"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <set>
#include <string>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// The struct is only used for inactive particle coodrinates for now
struct PyATCoordinates{
    double x;
    double px;
    double y;
    double py;
    double deltap;
    double ct;
};

class PyATInterface
{
public:
    PyATInterface() = delete;  // No default constructor

    PyATInterface(const  std::string& bdsimConfigFile,
                  int    referencePdgIdIn,
                  double referenceMomentum,
                  double relativeEnergyCutIn,
                  int    seedIn,
                  bool   batchMode);

    virtual ~PyATInterface();

    void addCollimator(const std::string&   name,
                       const std::string&   material,
                       double lengthIn,
                       double apertureIn,
                       double rotationIn,
                       double xOffsetIn,
                       double yOffsetIn,
                       double jawTiltLeft,
                       double jawTiltRight,
                       int    side);

    void addParticle(const py::array_t<double>& coordiantes);

    void collimate();
    void clearData();
    void selectCollimator(const std::string& name);
    double GetEnergyDifferential();

    py::array_t<double> collimateReturn();

private:
    BDSIMLink* bds = nullptr;
    BDSBunchSixTrackLink* stp = nullptr;
    std::vector<char *> argv;
    std::vector<bool> particleActiveState;

    std::vector<PyATCoordinates*> pyATParticles;

    long long int pdgID = 0;
    double referenceEk = 0.0;
    double relativeEnergyCut = 0.0;
    int seed = 0;

    G4double referenceMass = 0.0;
    G4double referenceMomentum = 0.0;
    G4double referenceEnergy = 0.0;
    G4double beta0 = 0.0;  // relativistic beta for the primary particle

    G4double energyIn = 0.0;
    G4double energyOut = 0.0;

    std::string currentCollimatorName;
    int maxParticleID = 0;

    bool processingDone = false;
};