import typing


class TestScenario:
    def check_attribute(self, attribute):
        if attribute is not None:
            if len(attribute) != 0:
                return True
        return False

    def new_attrib(self, attrib_1: typing.Optional[typing.Set[str]], attrib_2: typing.Optional[typing.Set[str]]):
        new_attrib = None
        if attrib_1 is None:
            new_attrib = attrib_2
        elif attrib_2 is None:
            new_attrib = attrib_1
        else:
            new_attrib = attrib_1 | attrib_2
        return new_attrib

    def combine(self, other):
        raise NotImplementedError(self.__class__.__name__ + " method combine must be overridden")

    def to_dict(self):
        dc = {}
        for key, value in self.__dict__.items():
            val = None
            if isinstance(value, set):
                val = list(value)
            else:
                val = value
            dc[key] = val
        return dc
