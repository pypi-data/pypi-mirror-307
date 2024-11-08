"""
Provides a uniform interface for potentially installed external programs
"""

__all__ = [
    "ExternalProgramInterface"
]

class ExternalProgramInterface:
    name = None
    module = None
    lib_supported = None
    library = None

    @classmethod
    def try_load_lib(cls):
        if cls.library is None:
            if cls.lib_supported is False:
                raise ImportError("Library '{}' is not installed".format(cls.name))
            try:
                cls.library = cls.load_library()
            except ImportError:
                cls.lib_supported = False
            else:
                cls.lib_supported = True
        return cls.lib_supported

    @classmethod
    def get_lib(cls):
        if cls.try_load_lib():
            return cls.library
        else:
            raise ImportError("module {} not installed".format(cls.module))

    @classmethod
    def load_library(cls):
        return __import__(cls.module)
        # raise NotImplementedError("{} needs to implement `load_library`".format(cls.__name__))

    @classmethod
    def method(cls, name):
        return getattr(cls.get_lib(), name)
    @property
    def lib(self):
        return self.get_lib()
    def __getattr__(self, item):
        return self.method(item)