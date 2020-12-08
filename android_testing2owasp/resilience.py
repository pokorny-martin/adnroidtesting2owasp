import typing
from .scenario import TestScenario


class Resilience1(TestScenario):
    root = False

    def __init__(self, root: typing.Optional[bool] = None):
        if root is not None:
            self.root = root

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_root = self.root or other.root
        return self.__class__(new_root)


class Resilience2(TestScenario):
    checking_adb = False

    def __init__(self, checking_adb: typing.Optional[bool] = None):
        if checking_adb is not None:
            self.checking_adb = checking_adb

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_checking_adb = self.checking_adb or other.checking_adb
        return self.__class__(new_checking_adb)


class Resilience3(TestScenario):
    sandbox_permission = False
    detail = []

    def __init__(self,
                 sandbox_permission: typing.Optional[bool] = None,
                 detail: typing.Optional[typing.List[str]] = None):
        if sandbox_permission is not None:
            self.sandbox_permission = sandbox_permission
        if detail is not None:
            self.detail = detail

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_sandbox_permission = self.sandbox_permission or other.sandbox_permission
        new_detail = [detail for detail in self.detail]
        for detail in other.detail:
            if detail not in new_detail:
                new_detail.append(detail)
        return self.__class__(new_sandbox_permission, new_detail)


class Resilience6(TestScenario):
    signature_code_checking = False
    detail = []

    def __init__(self,
                 signature_code_checking: typing.Optional[bool] = None,
                 detail: typing.Optional[typing.List[str]] = None):
        if signature_code_checking is not None:
            self.signature_code_checking = signature_code_checking
        if detail is not None:
            self.detail = detail

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_signature_code_checking = self.signature_code_checking or other.signature_code_checking
        new_detail = [detail for detail in self.detail]
        for detail in other.detail:
            if detail not in new_detail:
                new_detail.append(detail)
        return self.__class__(new_signature_code_checking, new_detail)


class Resilience10(TestScenario):
    device_id = False
    android_id = False

    def __init__(self,
                 device_id: typing.Optional[bool] = None,
                 android_id: typing.Optional[bool] = None):
        if device_id is not None:
            self.device_id = device_id
        if android_id is not None:
            self.android_id = android_id

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_device_id = self.device_id or other.device_id
        new_android_id = self.android_id or other.android_id
        return self.__class__(new_device_id, new_android_id)
