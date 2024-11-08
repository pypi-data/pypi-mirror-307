"""
Provides support for chemical toolkits
"""

from .Interface import *

__all__ = [
    "OpenBabelInterface",
    "PybelInterface",
    "RDKitInterface",
    "OpenChemistryInterface"
]

class OpenBabelInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the OpenBabel toolkit (which is installed with anaconda)
    """
    name = 'OpenBabel'
    module = 'openbabel.openbabel'

class PybelInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the OpenBabel toolkit (which is installed with anaconda)
    """
    name = 'Pybel'
    module = 'openbabel.pybel'

class RDKitInterface(ExternalProgramInterface):
    name = 'RDKit'
    module = 'rdkit'

class OpenChemistryInterface:
    name = 'OpenChemistry'
    module = 'openchemistry.io'

# PYBEL_SUPPORTED = None
    # OB_SUPPORTED = None
    # def __init__(self):
    #     self._lib = None
    # @classmethod
    # def _pybel_installed(cls):
    #     if cls.PYBEL_SUPPORTED is None:
    #         try:
    #             import openbabel.pybel
    #         except ImportError:
    #             cls.PYBEL_SUPPORTED = False
    #         else:
    #             cls.PYBEL_SUPPORTED = True
    #
    #     return cls.PYBEL_SUPPORTED
    # @classmethod
    # def _ob_installed(cls):
    #     if cls.OB_SUPPORTED is None:
    #         try:
    #             import openbabel.openbabel
    #         except ImportError:
    #             cls.OB_SUPPORTED = False
    #         else:
    #             cls.OB_SUPPORTED = True
    #
    #     return cls.OB_SUPPORTED
    # @property
    # def pybel(self):
    #     if self._pybel is None:
    #         if self._pybel_installed():
    #             import openbabel.pybel as lib
    #             self._pybel = lib
    #         else:
    #             raise ImportError("OpenBabel isn't installed")
    #     return self._pybel
    # @property
    # def openbabel(self):
    #     if self._ob is None:
    #         if self._ob_installed():
    #             import openbabel.openbabel as lib
    #             self._ob = lib
    #         else:
    #             raise ImportError("OpenBabel isn't installed")
    #     return self._ob


