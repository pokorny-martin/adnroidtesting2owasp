import typing
from .scenario import TestScenario


class Code1(TestScenario):
    valid = False

    def __init__(self, valid: typing.Optional[bool] = None):
        if valid is not None:
            self.valid = valid

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_valid = self.valid or other.valid
        return self.__class__(new_valid)


class Code2(TestScenario):
    not_debuggable = False

    def __init__(self, not_debuggable: typing.Optional[bool] = None):
        if not_debuggable is not None:
            self.not_debuggable = not_debuggable

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_not_debuggable = self.not_debuggable or other.not_debuggable
        return self.__class__(new_not_debuggable)


class Code3(TestScenario):
    stripped = {}

    def __init__(self,
                 name: str,
                 is_stripped: typing.Optional[bool] = None,
                 _stripped: typing.Optional[typing.Dict[str, bool]] = None):
        if _stripped is not None:
            self.stripped = _stripped
        else:
            if is_stripped is not None:
                is_stripped = False
            self.stripped[name] = is_stripped

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None

        new_stripped = self.stripped
        for key, value in other.stripped.items():
            try:
                new_stripped[key] = other.stripped[key] and new_stripped[key]
            except KeyError:
                new_stripped[key] = value
        return self.__class__("", _stripped=new_stripped)


class Code4(TestScenario):
    stripped = {}
    not_debuggable = False

    def __init__(self,
                 name: str,
                 is_stripped: typing.Optional[bool] = None,
                 not_debuggable: typing.Optional[bool] = None,
                 _stripped: typing.Optional[typing.Dict[str, bool]] = None):

        if _stripped is not None:
            self.stripped = _stripped
        else:
            if is_stripped is not None:
                is_stripped = False
            self.stripped[name] = is_stripped

        if not_debuggable is not None:
            self.not_debuggable = not_debuggable

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None

        new_not_debuggable = self.not_debuggable or other.not_debuggable
        new_stripped = self.stripped
        for key, value in other.stripped.items():
            try:
                new_stripped[key] = other.stripped[key] and new_stripped[key]
            except KeyError:
                new_stripped[key] = value
        return self.__class__("", not_debuggable=new_not_debuggable, _stripped=new_stripped)
