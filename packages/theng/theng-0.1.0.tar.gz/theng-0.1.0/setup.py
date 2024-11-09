import distutils.command.build
from setuptools import setup


# Override build command
class BuildCommand(distutils.command.build.build):
    def initialize_options(self):
        distutils.command.build.build.initialize_options(self)
        self.build_base = '../build'

setup(
    cmdclass={"build": BuildCommand},
)