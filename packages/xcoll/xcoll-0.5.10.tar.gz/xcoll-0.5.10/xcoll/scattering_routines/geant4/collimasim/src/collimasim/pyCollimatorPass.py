import numpy

import collimasim

'''
This is a specialised pass method that performs a full simulation of physical
interactions in collimators using Geant4. The interface to BDSIM (Geant4) is
provided by the collimasim package.

The interface must be initialised first, with a list of parameters and a file
containing the collimator specification. All collimators that will be used
must be provided in the collimator file and are accessed by name. Currently,
collimators are limited to block jaw collimators, and the geometry model is
built automatically.

The passmethods contains a function trackFunction(), used for tracking by pyat,
and has to be in the python path or in at.integrators

The element creation is as follows:

collimator = elements.Element('MyColl', 1.0, PassMethod='pyCollimatorPass')

To be noted:
The name of a collimator using the pyCollimatorPass method must match a
collimator defined during initialisation. For collimators where a physical
interaction simulation is not required, please specify a different pass method,
e.g. drift.
'''

bdsimlink = None # Keep this as a global variable for now

def load_collgaps(collgaps_file):
    coll_dict = {}

    coll_data = numpy.genfromtxt(collgaps_file, dtype=None, encoding=None, comments='#')

    for coll in coll_data:
        name = coll[1].lower()
        one_coll = {}

        one_coll["material"] = coll[6]
        one_coll["length"] = float(coll[7])
        one_coll["angle"] = float(coll[2])
        one_coll["halfgap"] = float(coll[5])
        # The collgaps do not specify the offsets
        # or if a collimator is one-sided
        # TODO: add the closed orbit at the collimator
        one_coll["xoffs"] = 0
        one_coll["yoffs"] = 0
        one_coll["side"] = 0 # 0 is two sided

        coll_dict[name] = one_coll

    return coll_dict


def initialise(bdsim_config_file, collimator_info, reference_pdg_id,
               reference_Ek, relative_energy_cut, seed):

    global bdsimlink

    # Initialise a code interface
    if bdsimlink is not None:
        return

    bdsimlink = collimasim.PyATInterface(bdsimConfigFile=bdsim_config_file,
                                         referencePdgId=reference_pdg_id,
                                         referenceEk=reference_Ek,
                                         relativeEnergyCut=relative_energy_cut,
                                         seed=seed, batchMode=True)

    if isinstance(collimator_info, dict):
        collimators = collimator_info
    else:
        collimators = load_collgaps(collimator_info)

    for name in collimators:
        cdict = collimators[name]
        material = cdict["material"]
        length = cdict["length"]
        angle = cdict["angle"]
        halfgap = cdict["halfgap"]
        xoffs = cdict["xoffs"]
        yoffs = cdict["yoffs"]
        side = cdict["side"]

        bdsimlink.addCollimator(name, material, length, aperture=halfgap*2,
                                rotation=angle, xOffset=xoffs, yOffset=yoffs,
                                jawTiltLeft=0.0, jawTiltRight=0.0,
                                side=side)


def process_particles(collimator_name):
    # MAD-X convention uses . in the names, while pyAT convention uses _
    # Provide handling for MAD-X name to avoid trivial issues
    try:
        bdsimlink.selectCollimator(collimator_name)
    except RuntimeError:
        try:
            collimator_name_madx = collimator_name.replace("_", ".").lower()
            bdsimlink.selectCollimator(collimator_name_madx)
        except RuntimeError:
            raise ValueError(f"No collimator {collimator_name} (or "
                             f"{collimator_name_madx} defined)")

    print(f"Processing collimator: {collimator_name}")
    # Perform the Geant4 simulation
    bdsimlink.collimate()

    # Collect the surviving particles - a 1D array with n * 6 elements
    arr_out = bdsimlink.collimateReturn()

    return arr_out


def trackFunction(rin,elem=None):
    if bdsimlink is None:
        raise ValueError("The Geant4 interface is not initialised. Call"
                         " pyCollimatorPass.initialise(...) before tracking")

    bdsimlink.clearData() # Clear the old data

    name = elem.FamName
    # rin is a (6,n) array
    for rtmp in numpy.atleast_2d(rin.T):
        if hasattr(elem,'T1'): rtmp += elem.T1
        if hasattr(elem,'R1'): rtmp[:] = numpy.dot(elem.R1,rtmp)
        bdsimlink.addParticle(rtmp)

    rout = process_particles(name)

    # The returned array may be longer than the original
    # due to secondary particles. Access by index and only
    # change only the primary coordinates
    for i in range(len(rin.T)):
        part = rout.T[i, :]
        if hasattr(elem,'R2'): part[:] = numpy.dot(elem.R2, part)
        if hasattr(elem,'T2'): part += elem.T2

        rin.T[i, :] = part

    #return rin # This return value doesn't seem to be used by pyAT
