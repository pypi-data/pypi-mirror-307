from .Interface import *

__all__ = [
    "VPythonInterface",
    "VTKInterface"
]

class VPythonInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the VPython visualization toolkit
    """
    name = 'VPython'
    module = 'vpython'

class VTKInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the VPython visualization toolkit
    """
    name = 'VTK'
    module = 'vtk'

    @classmethod
    def graphics_object(cls, obj):
        return cls.method('vtk'+obj)()
    @classmethod
    def named_colors(cls):
        return cls.method('vtkNamedColors')()