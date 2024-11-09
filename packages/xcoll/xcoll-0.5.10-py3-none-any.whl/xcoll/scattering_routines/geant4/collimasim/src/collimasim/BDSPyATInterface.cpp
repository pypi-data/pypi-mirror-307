#include "BDSPyATInterface.hh"
#include <cstring>
#include <BDSSamplerCustom.hh>


PyATInterface::PyATInterface(const  std::string& bdsimConfigFile,
                             int    referencePdgIdIn,
                             double referenceEkIn,
                             double relativeEnergyCutIn,
                             int    seedIn,
                             bool   batchMode):
        pdgID(referencePdgIdIn),
        referenceEk(referenceEkIn * CLHEP::GeV),
        relativeEnergyCut(relativeEnergyCutIn),
        seed(seedIn)
{
    stp = new BDSBunchSixTrackLink();
    bds = new BDSIMLink(stp);

    std::string seedStr = std::to_string(seed);
    std::vector<std::string> arguments = {"--file=" + bdsimConfigFile,
                                          "--file=" + bdsimConfigFile,
                                          //"--vis_debug",
                                          "--output=none",
                                          "--seed=" + seedStr,
                                          "--outfile=output_" + seedStr};

    for(auto & argument : arguments)
    {
        argv.push_back(strdup(argument.c_str()));
    }

    if (batchMode)
    {
        std::string batch_flag = "--batch";
        argv.push_back(strdup(batch_flag.c_str()));
    }

    argv.push_back(nullptr);

    // absolute energy cut is in GeV
    double relEKCut = relativeEnergyCut;
    if (relEKCut < 1e-6) // defaults to 0 which means 0eV cut which is bad
    { relEKCut = 1.0; }

    // referenceEk is in GeV
    double minimumEK = relEKCut * (referenceEk);

    G4cout << "Minimum kinetic energy " << minimumEK << " MeV" << G4endl;
    auto data = argv.data();
    try
    { bds->Initialise(argv.size() - 1, &argv[0], true, minimumEK / CLHEP::GeV, false); } // minimumEk in GeV
    catch (const std::exception &e)
    {
        std::cout << e.what() << std::endl;
        exit(1);
    }

    /// Compute variables that will be used for coordinate transforms
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particleDef = particleTable->FindParticle(pdgID);
    if (!particleDef)
    {throw BDSException("BDSBunchUserFile> Particle \"" + std::to_string(pdgID) + "\" not found");}

    BDSIonDefinition* ionDef = nullptr;
    if (BDS::IsIon(particleDef))
    {
        throw std::invalid_argument("Particle \"" + std::to_string(pdgID) + "\" is an ion and is not supported.");
    }

    referenceMass = particleDef->GetPDGMass();
    referenceEnergy = referenceEk + referenceMass;
    referenceMomentum = std::sqrt(referenceEnergy * referenceEnergy - referenceMass * referenceMass);
    beta0 = referenceMomentum / referenceEnergy;

}

PyATInterface::~PyATInterface()
{
    delete bds;
    delete stp;
}


void PyATInterface::addCollimator(const std::string&   name,
                                  const std::string&   material,
                                  double lengthIn,
                                  double apertureIn,
                                  double rotationIn,
                                  double xOffsetIn,
                                  double yOffsetIn,
                                  double jawTiltLeft,
                                  double jawTiltRight,
                                  int    side)
    {

        bool buildLeft  = side == 0 || side == 1;
        bool buildRight = side == 0 || side == 2;
        double length   = lengthIn   * CLHEP::m;
        double aperture = apertureIn * CLHEP::m;

        bool isACrystal = false;

        bds->AddLinkCollimatorJaw(name,
                                  material,
                                  length,
                                  0.5*aperture,
                                  0.5*aperture,
                                  rotationIn,
                                  xOffsetIn, 
                                  yOffsetIn,
                                  jawTiltLeft,
                                  jawTiltRight,
                                  buildLeft,
                                  buildRight,
                                  isACrystal,
                                  0);
    }


void PyATInterface::addParticle(const py::array_t<double>& coordiantes)
{
    // Process the incoming numpy array
    py::buffer_info info = coordiantes.request();
    auto ptr = static_cast<double *>(info.ptr);

    auto x = (G4double) *ptr++;
    auto xp = (G4double) *ptr++;
    auto y = (G4double) *ptr++;
    auto yp = (G4double) *ptr++;
    auto deltap = (G4double) *ptr++;
    auto ct = (G4double) *ptr;

    if (!std::isfinite(x))
    {
        particleActiveState.push_back(false); // if the first coordinates is a NaN do not process the particle
        auto particle_coords = new PyATCoordinates{x, xp, y, yp, deltap, ct};
        pyATParticles.push_back(particle_coords);
        return;
    }
    else
    {
        particleActiveState.push_back(true);
        auto particle_coords = new PyATCoordinates{x, xp, y, yp, deltap, ct};
        pyATParticles.push_back(particle_coords);
    }

    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particleDef = particleTable->FindParticle(pdgID);
    if (!particleDef)
    {throw BDSException("BDSBunchUserFile> Particle \"" + std::to_string(pdgID) + "\" not found");}

    BDSIonDefinition* ionDef = nullptr;
    if (BDS::IsIon(particleDef))
    {
        throw std::invalid_argument("Particle \"" + std::to_string(pdgID) + "\" is an ion and is not supported.");
    }

    G4double mass = particleDef->GetPDGMass();
    G4double p = referenceMomentum * (G4double) deltap + referenceMomentum;
    G4double totalEnergy = std::sqrt(p * p + mass * mass);
    G4double t = - (G4double) ct * CLHEP::m / CLHEP::c_light; // this is time difference in ns TODO: how to treat the minus?

    G4double zp = BDSBunch::CalculateZp(xp,yp,1);

    BDSParticleCoordsFull coords = BDSParticleCoordsFull(x * CLHEP::m,
                                                         y * CLHEP::m,
                                                         0,
                                                         xp,
                                                         yp,
                                                         zp,
                                                         t,
                                                         0,
                                                         totalEnergy,
                                                         1);

    // Add the energy of the particle to a total count
    // This allows to calculate the differential between energy in and energy out,
    // which is an approximation of the energy lost in the collimator
    energyIn += totalEnergy;

    // Wrap in our class that calculates momentum and kinetic energy.
    // Requires that one of E, Ek, P be non-zero (only one).

    BDSParticleDefinition* particleDefinition = nullptr;
    try
    {
        particleDefinition = new BDSParticleDefinition(particleDef, totalEnergy * CLHEP::GeV, 0, 0, 1, ionDef);
    }
    catch (const BDSException& e)
    {// if we throw an exception the object is invalid for the delete on the next loop
        particleDefinition = nullptr; // reset back to nullptr for safe delete
        return;
    }

    if (particleDefinition)
    {
        maxParticleID++;
        int pyatID = maxParticleID; // Set the particle ID to the current particle count
        stp->AddParticle(particleDefinition, coords, pyatID, pyatID);
        auto part = stp->GetNextParticleLocal();
        bds->SetCurrentMaximumExternalParticleID(maxParticleID);
    }
}


void PyATInterface::collimate()
{
    if (!stp->Size())
    {
        std::cout << "No particles loaded, skip processing" << std::endl;
        return;
    }

    bds->BeamOn((G4int)stp->Size());
}


void PyATInterface::selectCollimator(const std::string& collimatorName)
{
    currentCollimatorName = collimatorName;
    // This doesn't throw an error if the element doesn't exist
    bds->SelectLinkElement(collimatorName);

    // Check if the element exists by querying the index: -1 means it doesn't exist
    if (bds->GetLinkIndex(collimatorName) == -1)
        {throw std::runtime_error("Element not found " + collimatorName);}
}


void PyATInterface::clearData()
{
    bds->ClearSamplerHits();
    stp->ClearParticles();
    currentCollimatorName.clear();

    for (auto part : pyATParticles)
    {
        delete part;
    }

    std::vector<PyATCoordinates*>().swap(pyATParticles);
    std::vector<bool>().swap(particleActiveState);

    maxParticleID = 0;

    energyIn = 0.0;
    energyOut = 0.0;
    processingDone = false;
}


double PyATInterface::GetEnergyDifferential()
{
    if (!processingDone)
        {throw std::runtime_error("The energy differential can only be computed when the processing is complete");}

    return (energyIn - energyOut) / CLHEP::GeV;
}

py::array_t<double> PyATInterface::collimateReturn()
{
    // Access the sampler hits - particles reaching the planes for transport back
    const BDSHitsCollectionSamplerLink* hits = bds->SamplerHits();

    size_t hitsCount = hits ? hits->GetSize() : 0;

    // Count the number of secondary particles
    size_t secondaryCount = 0;
    for (size_t i = 0; i < hitsCount; i++)
    {
        auto hit = (*hits)[i];
        if (hit->externalParticleID != hit->externalParentID) { secondaryCount++; }
    }

    // The output arrays has slots for all primary particles, regardless if lost or not, and for secondary particles
    size_t output_size = particleActiveState.size() + secondaryCount;

    // Prepare the numpy array that will be returned
    auto result = py::array(py::buffer_info(
            nullptr,            /* Pointer to data (nullptr -> ask NumPy to allocate!) */
            sizeof(double),     /* Size of one item */
            py::format_descriptor<double>::value, /* Buffer format */
            2,          /* How many dimensions? */
            { 6, (int) output_size },  /* Number of elements for each dimension */
            { sizeof(double), 6 * sizeof(double) }  /* Strides for each dimension */
    ));

    auto buf = result.request();

    auto *array_ptr = (double *) buf.ptr;

    // Loop through the particles in the *original* bunch - the primaries
    size_t hits_index = 0;
    size_t secondary_write_offset = particleActiveState.size();

    bool prim_survied = false;
    double sum_deltaplusone_sec = 0.0;


    for (size_t i=0; i < particleActiveState.size(); i++)
    {
        auto original_coordinates = pyATParticles.at(i);
        if (!particleActiveState.at(i))
        {
            // The particle was inactive coming in - keep the original coordinates
            array_ptr[i*6]  = original_coordinates->x;
            array_ptr[i*6 + 1] = original_coordinates->px;
            array_ptr[i*6 + 2]  = original_coordinates->y;
            array_ptr[i*6 + 3] = original_coordinates->py;
            array_ptr[i*6 + 4] = original_coordinates->deltap;
            array_ptr[i*6 + 5] = original_coordinates->ct;
            continue;
        }

        auto part = stp->GetNextParticle(); // Advance through the bunch
        auto prim_part_id = stp->CurrentExternalParticleID(); // Get the ID of the primary particle

        // Now start looping over the hits - the particles to be returned to the tracker
        // These can be primary or secondary particles. Each primary can produce 0, 1, or 2+ products
        // The products need to be sorted to keep the array order - surviving primary particles are all
        // filled in first. If a primary didn't survive, make its coords NaNs to keep the array structure.
        // The hits are ordered by primary event, so just need one loop.
        while (hits_index < hitsCount)
        {
            BDSHitSamplerLink* hit = (*hits)[hits_index];

            if (hit->externalParentID != prim_part_id) { // The hits corresponding to the current primary are exhausted
                break;
            }

            const BDSParticleCoordsFull &coords = hit->coords;

            double mass = hit-> mass;
            double E  = coords.totalEnergy;

            energyOut += E; // Update the tally of outgoing energy for computation of energy lost

            double p = std::sqrt(E * E - mass * mass);

            double deltap = (p - referenceMomentum) / referenceMomentum;

            double collLength = bds->GetArcLengthOfLinkElement(currentCollimatorName);
            /// Need to compensate for the geometry construction in BDSIM
            /// There is a safety margin that is added to the collimator legnth
            double collMargin = 2.5 * BDSSamplerCustom::ChordLength();

            //double ct = (collLength + collMargin) / beta0 - CLHEP::c_light * coords.T;
            double ct = CLHEP::c_light * ((collLength + collMargin) / (CLHEP::c_light * beta0) - coords.T);

            auto track_id = hit->externalParticleID;

            size_t out_index; // The index of the slot to populate in the output array

            if (track_id == hit->externalParentID){
                // This is a primary particle as its parent is itself
                prim_survied = true;
                out_index = i;
            }
            else
            {
                // Secondary particles are populated in the array slots after all the primary particles
                out_index = secondary_write_offset;
                secondary_write_offset++;
            }

            array_ptr[out_index*6]  = coords.x / CLHEP::m;
            array_ptr[out_index*6 + 1] = coords.xp;
            array_ptr[out_index*6 + 2]  = coords.y / CLHEP::m;
            array_ptr[out_index*6 + 3] = coords.yp;
            array_ptr[out_index*6 + 4] = deltap;
            array_ptr[out_index*6 + 5] = ct / CLHEP::m;

            // Accumulate the delta of the secondary particles to correct the delta of the
            // lost primary particle
            sum_deltaplusone_sec += (deltap + 1);

            hits_index++;
        }

        if (!prim_survied) // The primary didn't survive - populate with NaNs
        {
            double delta_lost = original_coordinates->deltap - sum_deltaplusone_sec;

            array_ptr[i*6]  = original_coordinates->x;
            array_ptr[i*6 + 1] = original_coordinates->px;
            array_ptr[i*6 + 2]  = original_coordinates->y;
            array_ptr[i*6 + 3] = original_coordinates->py;

            array_ptr[i*6 + 4] = delta_lost;
            // array_ptr[i*6 + 5] = std::numeric_limits<double>::infinity(); //std::nan(""); // This marks the particle as lost;
            array_ptr[i*6 + 5] = std::nan(""); // This marks the particle as lost;
        }

        prim_survied = false; // reset for next particle
        sum_deltaplusone_sec = 0;

    }

    processingDone = true; // Mark the processing as completed, enabling access to energy lost at the collimator

    return result;
}