import ctypes
from ctypes.util import find_library

openblas_lib = ctypes.cdll.LoadLibrary(find_library('openblas'))

def get_num_threads():
    """Get the current number of threads used by the OpenBLAS server."""
    return openblas_lib.openblas_get_num_threads()

def get_num_procs():
    """Get the total number of physical processors"""
    return openblas_lib.openblas_get_num_procs()
