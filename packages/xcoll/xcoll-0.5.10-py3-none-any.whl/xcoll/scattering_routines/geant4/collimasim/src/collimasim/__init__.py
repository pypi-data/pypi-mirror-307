from .g4interface import PyATInterface, XtrackInterface

try:
    import xtrack
except ModuleNotFoundError:
    print("Xtrack not installed, will not import related features")
else:
    from .xtrack_collimator import Geant4CollimationManager, Geant4Collimator
