import typing
from .scenario import TestScenario


class Arch1(TestScenario):
    components = None
    files = None
    activities = None

    def __init__(self,
                 components: typing.Optional[typing.Set[str]] = None,
                 files: typing.Optional[typing.Set[str]] = None,
                 activities: typing.Optional[typing.Set[str]] = None):
        if self.check_attribute(components):
            self.components = components
        if self.check_attribute(files):
            self.files = files
        if self.check_attribute(activities):
            self.activities = activities

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_components = self.new_attrib(self.components, other.components)
        new_files = self.new_attrib(self.files, other.files)
        new_activities = self.new_attrib(self.activities, other.activities)
        return self.__class__(new_components, new_files, new_activities)