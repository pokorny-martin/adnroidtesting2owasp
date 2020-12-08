import typing
from .scenario import TestScenario


class Storage1(TestScenario):
    key_store = False
    detail = []

    def __init__(self,
                 key_store: typing.Optional[bool] = None,
                 detail: typing.Optional[typing.List[str]] = None):
        if key_store is not None:
            self.key_store = key_store
        if detail is not None:
            self.detail = detail

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_key_store = self.key_store or other.key_store
        new_detail = [detail for detail in self.detail]
        for detail in other.detail:
            if detail not in new_detail:
                new_detail.append(detail)
        return self.__class__(new_key_store, new_detail)

class Storage2(TestScenario):
    external_storage_permission = False
    detail = []

    def __init__(self,
                 external_storage_permission: typing.Optional[bool] = None,
                 detail: typing.Optional[typing.List[str]] = None):
        if external_storage_permission is not None:
            self.external_storage_permission = external_storage_permission
        if detail is not None:
            self.detail = detail

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_external_storage_permission = self.external_storage_permission or other.external_storage_permission
        new_detail = [detail for detail in self.detail]
        for detail in other.detail:
            if detail not in new_detail:
                new_detail.append(detail)
        return self.__class__(new_external_storage_permission, new_detail)


class Storage3(TestScenario):
    log_sources = None
    strings = None

    def __init__(self,
                 log_sources: typing.Optional[typing.Set[str]] = None,
                 strings: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(log_sources):
            self.log_sources = log_sources
        if self.check_attribute(strings):
            self.strings = strings

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_log_sources = self.new_attrib(self.log_sources, other.log_sources)
        new_strings = self.new_attrib(self.strings, other.strings)
        return self.__class__(new_log_sources, new_strings)


class Storage4(TestScenario):
    trackers = None
    urls = None

    def __init__(self,
                 trackers: typing.Optional[typing.Set[str]] = None,
                 urls: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(trackers):
            self.trackers = trackers
        if self.check_attribute(urls):
            self.urls = urls

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_trackers = self.new_attrib(self.trackers, other.trackers)
        new_urls = self.new_attrib(self.urls, other.urls)
        return self.__class__(new_trackers, new_urls)


class Storage6(TestScenario):
    shared_services = None

    def __init__(self,
                 shared_services: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(shared_services):
            self.intent_filters = shared_services

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_shared_services = self.new_attrib(self.shared_services, other.shared_services)
        return self.__class__(new_shared_services)


class Storage8(TestScenario):
    adb_back_up = False
    back_up = False
    strings = None

    def __init__(self,
                 adb_back_up: typing.Optional[bool] = None,
                 back_up: typing.Optional[bool] = None,
                 strings: typing.Optional[typing.Set[str]] = None):
        if adb_back_up is not None:
            self.adb_back_up = adb_back_up
        if back_up is not None:
            self.back_up = back_up
        if self.check_attribute(strings):
            self.strings = strings

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_adb_back_up = self.adb_back_up or other.adb_back_up
        new_back_up = self.back_up or other.back_up
        new_strings = self.new_attrib(self.strings, other.strings)
        return self.__class__(new_adb_back_up, new_back_up, new_strings)
