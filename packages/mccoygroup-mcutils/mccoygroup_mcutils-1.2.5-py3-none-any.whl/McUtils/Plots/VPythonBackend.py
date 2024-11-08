


class VPythonBackend:

    def __init__(self,
                 title=None,
                 legend=None,
                 window=None,
                 cube=None,
                 use_axes=True,
                 interactor=None,
                 renderer=None,
                 background='white',
                 image_size=(640, 480),
                 viewpoint=(5, 5, 5),
                 focalpoint=(0, 0, 0),
                 scale=(1, 1, 1)
                 ):
        import vpython
        vpython.canvas()