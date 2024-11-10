from packaging.version import Version

from packaging_version_increment.enums import IncrementEnum
from packaging_version_increment.increment import increment_version, update_version


class IncrementVersion(Version):
    def increment(self, part: IncrementEnum = IncrementEnum.micro) -> Version:
        new_version = increment_version(self, part)

        self.__init__(str(new_version))

        return new_version

    def update(self, *args, **kwargs) -> Version:
        new_version = update_version(self, beta=10)

        self.__init__(str(new_version))

        return new_version
