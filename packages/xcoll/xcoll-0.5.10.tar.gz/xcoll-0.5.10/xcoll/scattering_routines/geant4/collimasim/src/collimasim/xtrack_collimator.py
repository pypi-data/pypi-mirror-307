import re
import io
import sys
import numpy as np
import warnings
import json 

import pandas as pd

import xtrack as xt
import collimasim as cs

import subprocess

from enum import Enum, unique
from pathlib import Path

from contextlib import redirect_stdout, redirect_stderr, contextmanager

@unique
class MissingCollimatorAction(Enum):
    ERROR = "error"
    WARN  = "warn"
    SKIP  = "skip"


# Suppress some pandas warning that do not apply to the use case at hand
pd.options.mode.chained_assignment = None


def _calc_betagamma(E0, E):
    gamma = float(E)/E0
    beta = np.sqrt(1.-(1./gamma)**2)

    return beta*gamma


def _norm_to_geom_emittance(norm_emittance, E0, E):
    betagamma = _calc_betagamma(E0, E)
    return norm_emittance / betagamma


def _geom_to_norm_emittance(geom_emittance, E0, E):
    betagamma = _calc_betagamma(E0, E)
    return betagamma * geom_emittance


def _get_twiss_header(tfsfile):
    header = None
    line_no = 0
    with open(tfsfile, "r") as filein:
        for idx, line in enumerate(filein):
            if line.startswith("*"):  # This is the header line, preamble lines start with @
                header = line.replace("*", "").strip().split()  # Strip the comment char
                line_no = idx + 1  # As zero counted
                break  # End the loop early - information found

    return header, line_no


def _load_collimators_tfs(tfsfile):
    header, header_line_no = _get_twiss_header(tfsfile)

    required_columns = {"KEYWORD", "NAME", "BETX", "BETY", "ALFX", "ALFY", "DX", "DY", "X", "Y", "PT"}

    if not required_columns.issubset(set(required_columns)):
        raise KeyError("The required columns in the MAD-X"
                       " TFS file are: {}".format(" ".join(list(required_columns))))

    twiss = pd.read_csv(tfsfile, delim_whitespace=True, skiprows=header_line_no+1,
                        index_col=False, names=header)

    twiss_coll = twiss[twiss["KEYWORD"] == "COLLIMATOR"] # Collimators only
    twiss_coll = twiss[list(required_columns)] # Reduce the data fields
    twiss_coll["NAME"] = twiss_coll["NAME"].str.lower() # Make the names lowercase for easy processing

    twiss_coll.rename(columns={key: key.lower() for key in list(twiss_coll.columns)}, inplace=True)
    twiss_coll.rename(columns={'pt': 'delta'}, inplace=True) # rename PT to delta for consistency
    twiss_coll = twiss_coll.set_index("name").T

    return twiss_coll.to_dict()


def _load_collimators_xtrack(xt_twiss):
    required_columns = {"name", "betx", "bety", "alfx", "alfy", "dx", "dy", "x", "y", "delta"}
    twiss_coll = pd.DataFrame({key: xt_twiss[key] for key in required_columns})
    twiss_coll = twiss_coll.set_index('name').T

    return twiss_coll.to_dict()


def _colldb_format_detector(colldb_file):
    # Detect the likely format of a colldb file
    lines = []
    formats = ('collgaps', 'old_colldb', 'new_colldb', 'yaml_colldb')
    formats_found = {fmt: False for fmt in formats}

    all_old_colldb_lines = True
    all_collgaps_lines = True
    has_yaml_syntax = False
    with open(colldb_file, 'r') as infile:
        for l_no, line in enumerate(infile):
            line = line.strip()
            if line.startswith("#"):
                continue  # Comment
            if len(line.strip()) == 0:
                continue  # Empty line
            lines.append(line)
            # Detect based on the number of items on a line or
            # special charecters for the case of yaml
            if line == '---' or ':' in line:
                has_yaml_syntax = True
            elif len(line.split()) == 1: # Line from an old CollDB
                all_collgaps_lines = False
            elif len(line.split()) == 13:  # Line from collgaps
                all_old_colldb_lines = False
            else:
                all_collgaps_lines = False
                all_old_colldb_lines = False

    formats_found['yaml_colldb'] = has_yaml_syntax
    formats_found['old_colldb'] = all_old_colldb_lines
    formats_found['collgaps'] = all_collgaps_lines
    # The default case is the new CollDB
    # The loader there has checking for valid formats
    formats_found['new_colldb'] = not all_old_colldb_lines \
                                    and not all_collgaps_lines \
                                    and not has_yaml_syntax
    assert sum(formats_found.values()) == 1

    likely_format = [key for key in formats_found if formats_found[key] == True][0]
    print(f"Detected CollDB format: {likely_format}")
    return likely_format


def _load_colldb_yaml(filename):
    raise ValueError('Loading of yaml format CollDB not implemented yet.')


def _load_colldb_old(filename):

    float_num = r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'  # Float
    sep = r'\s+'

    # Not sure what the value 3 from last is, so it is not named
    coll_re = re.compile(r'''
    #{sep}
    (?P<name>.+){sep}
    (?P<name_lower>.+){sep}
    (?P<nsigma>{float_num}){sep}
    (?P<material>[a-zA-Z]+){sep}
    (?P<length>{float_num}){sep}
    (?P<angle>{float_num}){sep}
    ({float_num}){sep}
    (?P<betax>{float_num}){sep}
    (?P<betay>{float_num}){sep}
    '''.format(sep=sep, float_num=float_num), re.VERBOSE)

    with open(filename, "r") as infile:
        colldb_contents = infile.read()

    # List of dicts for each match (collimator)
    matches = [m.groupdict() for m in coll_re.finditer(colldb_contents)]

    # Make into a dict by name for easy access
    collimator_data = {}
    for m in matches:
        cname = m["name"].lower().strip()
        collimator_data[cname] = {"nsigma" : float(m["nsigma"]),
                                  "angle" : float(m["angle"]),
                                  "length" : float(m["length"]),
                                  "material": m["material"],
                                  }

    #print(collimator_data)
    return collimator_data


def _load_colldb_new(filename):
    with open(filename, "r") as infile:
        coll_data_string = ""
        family_settings = {}
        family_types = {}
        onesided = {}
        tilted = {}

        for l_no, line in enumerate(infile):
            if line.startswith("#"):
                continue  # Comment
            if len(line.strip()) == 0:
                continue  # Empty line
            sline = line.split()
            if len(sline) < 6:
                if sline[0].lower() == "nsig_fam":
                    family_settings[sline[1]] = sline[2]
                    family_types[sline[1]] = sline[3]
                elif sline[0].lower() == "onesided":
                    onesided[sline[1]] = int(sline[2])
                elif sline[0].lower() == "tilted":
                    tilted[sline[1]] = [float(sline[2]), float(sline[3])]
                elif sline[0].lower() == "settings":
                    pass  # Acknowledge and ignore this line
                else:
                    raise ValueError(f"Unknown setting {line}")
            else:
                coll_data_string += line

    names = ["name", "opening", "material", "length", "angle", "offset"]

    df = pd.read_csv(io.StringIO(coll_data_string), delim_whitespace=True,
                     index_col=False, skip_blank_lines=True, names=names)

    df["angle"] = np.deg2rad(df["angle"]) # convert to radians
    df["name"] = df["name"].str.lower() # Make the names lowercase for easy processing
    df["nsigma"] = df["opening"].apply(lambda s: float(family_settings.get(s, s)))
    df["type"] = df["opening"].apply(lambda s: family_types.get(s, "UNKNOWN"))
    df["side"] = df["name"].apply(lambda s: onesided.get(s, 0))
    df["tilt_left"] = df["name"].apply(lambda s: np.deg2rad(tilted.get(s, [0, 0])[0]))
    df["tilt_right"] = df["name"].apply(lambda s: np.deg2rad(tilted.get(s, [0, 0])[1]))
    df = df.set_index("name").T

    # Ensure the collimators marked as one-sided or tilted are actually defined
    defined_set = set(df.columns) # The data fram was transposed so columns are names
    onesided_set = set(onesided.keys())
    tilted_set = set(tilted.keys())
    if not onesided_set.issubset(defined_set):
        different = onesided_set - defined_set
        raise SystemExit('One-sided collimators not defined: {}'.format(", ".join(different)))
    if not tilted_set.issubset(defined_set):
        different = tilted_set - defined_set
        raise SystemExit('Tilted collimators not defined: {}'.format(",".join(different)))
    return df.to_dict()


def _load_collgaps(filename):
     names = ["id", "name", "angle", "betax",  "betay",  "halfgap", "material",
              "length", "sigx", "sigy", "tilt1",  "tilt2", "nsigma"]

     df = pd.read_csv(filename, delim_whitespace=True, index_col=False, names=names, header=0, comment='#')
     df["name"] = df["name"].str.lower() # Make the names lowercase for easy processing
     df = df.set_index("name").T

     return df.to_dict()


def _subprocess_bdsim_get_mass(pdg_id, json_out_file):
    '''
    This is worker function for get_mass_from_pdg_id(pdg_id), do not use 
    on it's own
    '''
    # Initialise BDSIM (the Geant4 kernel)
    dummy_bdsim_file = Path('_dummy_settings.gmad')
    with open(dummy_bdsim_file, 'w') as bdsimfile:
        # ignored, just need the file and beam definition to launch bdsim
        # it needs to be an ion so the ion tables get loaded, in addition to
        # all the normal particles
        bdsimfile.write('beam, particle="ion 208 82", momentum=42*GeV;\n')

    # dummy values as we only case about the mass
    g4link = cs.XtrackInterface(bdsimConfigFile=str(dummy_bdsim_file),
                                referencePdgId=int(pdg_id),
                                referenceEk=42, # BDSIM expects GeV
                                relativeEnergyCut=0.42,
                                seed=42, referenceIonCharge=0,
                                batchMode=True)

    mass = g4link.getReferenceMass() * 1e9 # convert to eV

    dummy_bdsim_file.unlink()

    with open(Path(json_out_file), 'w') as outfile:
        json.dump(obj={'mass_ev': mass}, fp=outfile)


def get_mass_from_pdg_id(pdg_id):
    '''
    This is a hacky utility function that is neccessary because 
    BDSIM isn't re-entry safe when loaded from the pybind11 c++ extension,
    and there is no good way to reload the extension. Subprocess
    offsers complete isolation so can safely load a dummy BDSIM and get the 
    mass of the particle.
    '''
    # Serialize the argument to pass it to the subprocess
    kwargs = {'json_out_file': 'reference_mass.json', 'pdg_id': pdg_id}
    argument_str = json.dumps(kwargs)

    subprocess.run([sys.executable, "-c",
                    ("import os;"
                     "import sys;"
                     "import json;"
                     "sys.stdout = open(os.devnull, 'w');"
                     "from collimasim.xtrack_collimator import _subprocess_bdsim_get_mass;"
                     f"_subprocess_bdsim_get_mass(**json.loads('{argument_str}'))")],
                     stdout = subprocess.DEVNULL, # Don't need the output from this - chceked later
                     # stderr = subprocess.DEVNULL,
                     )

    # The output is in a json file, load and delete when done
    mass_file_path = Path(kwargs['json_out_file'])
    if not mass_file_path.exists():
        raise Exception(f'Coud not load mass for PDG ID {pdg_id}.')
    
    with open(mass_file_path, 'r') as infile:
        mass = json.load(infile)['mass_ev']
    mass_file_path.unlink()
    return mass


class Geant4CollimationManager:

    def __init__(self, collimator_file, bdsim_config_file, tfs_file, emittance_norm, reference_pdg_id,
                 reference_kinetic_energy, relative_energy_cut, seed, material_rename_map={}, batchMode=True):

        unit_GeV = 1e9 # GeV to MeV

        # Energy units in Xtrack are eV
        self.collimator_file = collimator_file
        self.bdsim_config_file = bdsim_config_file
        self.tfs_file = tfs_file
        self.reference_pdg_id = reference_pdg_id
        self.reference_kinetic_energy = reference_kinetic_energy
        self.relative_energy_cut = relative_energy_cut
        self.seed = seed

        self.material_rename_map = material_rename_map

        # Allow for an asymmetric beam via a in iterable emittance assignment
        try:
            iter(emittance_norm)
            self.emit_norm_x = emittance_norm[0]
            self.emit_norm_y = emittance_norm[1]
        except TypeError:
            self.emit_norm_x = emittance_norm
            self.emit_norm_y = emittance_norm

        # Initialise BDSIM (the Geant4 kernel)
        self.g4link = cs.XtrackInterface(bdsimConfigFile=self.bdsim_config_file,
                                         referencePdgId=self.reference_pdg_id,
                                         referenceEk=self.reference_kinetic_energy / unit_GeV, # BDSIM expects GeV
                                         relativeEnergyCut=self.relative_energy_cut,
                                         seed=self.seed, referenceIonCharge=0, batchMode=batchMode)
                                         # Batch mode disables visualisation

        self.reference_mass = self.g4link.getReferenceMass() * unit_GeV # BDSIM gives the mass in GeV

        # Load the collimator settings and optics separately as not sure if all MAD-X collimators are needed
        if isinstance(self.tfs_file, xt.twiss.TwissTable):
            self._collimator_optics = _load_collimators_xtrack(self.tfs_file)
        elif isinstance(self.tfs_file, str):
            self._collimator_optics = _load_collimators_tfs(self.tfs_file)
        else:
            raise Exception('Collimator optics can only be an Xtrack twiss dict,'
                            ' or a path to a MAD-X twiss file')
        if isinstance(self.collimator_file, str):
            self._collimator_settings = self._load_collimator_data(self.collimator_file)
        elif isinstance(self.collimator_file, dict):
            self._collimator_settings = self.collimator_file
        else:
            raise Exception(f'Unsupported collimator data fromat {self.collimator_file}')

        self.collimators = {}
        self._load_collimators()
        #self._load_collimators_collgaps()

        # Debug
        #for cname in self.collimators:
        #    print(cname, self.collimators[cname]["nsigma"], self.collimators[cname]["halfgap"])

        #with open(f"cgaps_{self.collimator_file}", "w") as outfile:
        #    for cname in self.collimators:
        #        outfile.write("{} {} {}\n".format(cname,
        #                                        self.collimators[cname]["nsigma"],
        #                                        self.collimators[cname]["halfgap"]))

    def _load_collimator_data(self, collimator_file):
        detected_format = _colldb_format_detector(collimator_file)
        loader_dispatch = {'collgaps': _load_collgaps, 
                           'new_colldb': _load_colldb_new, 
                           'old_colldb': _load_colldb_old,
                           'yaml_colldb': _load_colldb_yaml}

        data = loader_dispatch[detected_format](collimator_file)
        return data

    def _calc_collimator_halfgap(self, name):
        # Calculate the geometric emittances first
        totalEnergy = self.reference_kinetic_energy + self.reference_mass
        emit_geom_x = _norm_to_geom_emittance(self.emit_norm_x, self.reference_mass, totalEnergy)
        emit_geom_y = _norm_to_geom_emittance(self.emit_norm_y, self.reference_mass, totalEnergy)

        betx = self._collimator_optics[name]["betx"]
        bety = self._collimator_optics[name]["bety"]

        nsigma = self._collimator_settings[name]["nsigma"]
        angle  = self._collimator_settings[name]["angle"]

        a = nsigma * np.sqrt(betx * emit_geom_x)
        b = nsigma * np.sqrt(bety * emit_geom_y)

        x = a * np.cos(angle)
        y = b * np.sin(angle)

        return np.sqrt(x**2 + y**2)

    def _load_collimators(self):

        for cname in self._collimator_settings:
            cdata = self._collimator_settings[cname]
            copt = self._collimator_optics[cname]

            if cdata['nsigma'] < 900:
                halfgap = self._calc_collimator_halfgap(cname)

                mat_def = cdata["material"]
                material = self.material_rename_map.get(mat_def, mat_def)

                # Compute the offset for the collimators - placed around the closed orbit
                x_offset = copt['x']
                y_offset = copt['y']

                self.g4link.addCollimator(cname, material, cdata["length"], 
                                        apertureLeft=halfgap, apertureRight=halfgap,
                                        rotation=cdata["angle"], 
                                        xOffset=x_offset, yOffset=y_offset,
                                        jawTiltLeft=cdata.get("tilt_left", 0.),
                                        jawTiltRight=cdata.get("tilt_right", 0.), 
                                        side=cdata.get("side", 0))

                # Merge all the info about the collimator in the same dictionary for storage
                self.collimators[cname] = {**cdata, **copt}
                self.collimators[cname]["halfgap"] = halfgap
            else:
                print(f'Collimator {cname} with gap of {cdata["nsigma"]} sigma ignored.')

    def _load_collimators_collgaps(self):
        collimators = np.genfromtxt(self.collimator_file, dtype=None, encoding=None, comments='#')

        # This would be nicer with pandas, but don't need the dependency just for this one bit
        for coll in collimators:
            name = coll[1]
            material = coll[6]
            length = float(coll[7])
            angle = float(coll[2])
            halfgap = float(coll[5])

            # TODO: add the closed orbit at the collimator
             # side=0 means both jaws
            side = 0 # Default for now

            self.g4link.addCollimator(name, material, length, aperture=halfgap*2,
                                      rotation=angle, xOffset=0, yOffset=0, side=0)

            self.collimators[name] = {"material": material,
                                      "length": length,
                                      "halfgap": halfgap,
                                      "angle": angle,
                                      "side": side,
                                      }

    def process_collimator(self, collimator_name, particles):
        self.g4link.clearData() # Clear the old data - bunch particles and hits

        print(f"Processing collimator: {collimator_name}")

        # This temp delta is necessary because for primary particles, the coordinates are
        # modified in place. But for the longitudinal plane there are 3 coordinates that must
        # be updated, so pass a copy of the delta for the update in place and trigger the
        # correct update of the 3 coordinates later
        delta_temp = particles._delta.copy()

        # Using a list allows to package the required coordinates without copying
        coordinates = [particles.x, particles.y, particles.px, particles.py,
                       particles.zeta, delta_temp, particles.chi, particles.charge_ratio,
                       particles.s, particles.pdg_id, particles.particle_id, particles.state,
                       particles.at_element, particles.at_turn]

        self.g4link.addParticles(coordinates)
        # The collimators must be defined already in the g4manager
        self.g4link.selectCollimator(collimator_name)

        self.g4link.collimate() # Performs the physical interaction simulation

        # Modifies the primary coordinates in place and returns a list of arrays for the
        # coordinates of the secondary particles.
        products = self.g4link.collimateReturn(coordinates)

        # Force the update using the private member _delta
        # as the update_delta method only updates the delta for active particles
        particles._delta[:len(delta_temp)] = delta_temp
        particles.update_delta(delta_temp)

        return products

    def make_xtg4_collimator(self, name):
        name = name.lower()
        if name not in self.collimators:
            raise KeyError(f"Collimator {name} is not defined in the Geant4 model")

        g4coll = cs.Geant4Collimator(name=name, g4manager=self)
        xtg4coll = xt.BeamInteraction(name=name, interaction_process=g4coll,
                                      length=self.collimators[name]["length"])

        return xtg4coll

    def place_all_collimators(self, sequence, on_missing=None):
        # Make the collimators
        for name in self.collimators:
            coll = self.make_xtg4_collimator(name)
            self.place_xtg4_collimator(sequence, coll, on_missing=on_missing)


    def place_xtg4_collimator(self, sequence, xtg4_collimator, on_missing=None):
        '''
        A function to expand a collimator from a marker or an active-length-only
        collimator to a full-size element. To achieve that, all the elements found
        inside the collimator length are discarded, and the outer-most drifts are
        trimmed to fit the thick collimator.
        '''

        coll_name = xtg4_collimator.interaction_process.name
        coll_length = xtg4_collimator.length

        if on_missing is None:
            on_missing = "warn"
        exception_type = MissingCollimatorAction(on_missing)

        try:
            coll_idx = sequence.element_names.index(coll_name.lower())
        except ValueError:
            msg = f"Collimator {coll_name} not found in sequence"
            if exception_type == MissingCollimatorAction.ERROR:
                raise ValueError(msg)
            elif exception_type == MissingCollimatorAction.WARN:
                warnings.warn(msg)

        s_pos = sequence.get_s_elements()

        s_ups = s_pos[coll_idx]
        s_dns = s_pos[coll_idx + 1]
        s_cent = (s_ups + s_dns) / 2
        len_c_xt = s_dns - s_ups

        coll_edge_ups = s_cent - coll_length / 2
        coll_edge_dns = s_cent + coll_length / 2

        sequence.insert_element(at_s=coll_edge_ups, element=xtg4_collimator, name=coll_name.lower())


class Geant4Collimator:
    def __init__(self, name, g4manager):
        self.name = name
        self.g4manager = g4manager

    def interact(self, particles):
        # The track method is needed for tracking in Xtrack
        return self.g4manager.process_collimator(self.name, particles)
