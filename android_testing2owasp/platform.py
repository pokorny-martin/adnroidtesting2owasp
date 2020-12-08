import typing
from .scenario import TestScenario


class Platform1(TestScenario):
    permissions = None

    def __init__(self, permissions: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(permissions):
            self.permissions = permissions

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_permissions = self.new_attrib(self.permissions, other.permissions)
        return self.__class__(new_permissions)


class Platform4(TestScenario):
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


class Platform5(TestScenario):
    javascript_in_webview = False

    def __init__(self,
                 javascript_in_webview: typing.Optional[bool] = None):
        if javascript_in_webview is not None:
            self.javascript_in_webview = javascript_in_webview

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_javascript_in_webview = self.javascript_in_webview or other.javascript_in_webview
        return self.__class__(new_javascript_in_webview)


class Platform9(TestScenario):
    intent_filters = None

    def __init__(self,
                 intent_filters: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(intent_filters):
            self.intent_filters = intent_filters

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_intent_filters = self.new_attrib(self.intent_filters, other.intent_filters)
        return self.__class__(new_intent_filters)
