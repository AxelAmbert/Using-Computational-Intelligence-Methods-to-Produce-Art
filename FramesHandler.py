from BiomorphCreator import *


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class FrameHandler:

    def __init__(self, master):
        self.frames = (BiomorphCreator(master))