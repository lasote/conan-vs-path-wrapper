import os

from conans import ConanFile, tools

class VsPathWrapperConan(ConanFile):
    name = "vs_path_wrapper"
    version = "1.0"
    license = "MIT"
    url = "https://github.com/lasote/conan-vs-path-wrapper"
    description = "Use this package as a fake build_require to your Visual Studio installation, you will be able " \
                  "to build your dependency tree controlling the order of the PATH, specially if you are using " \
                  "subsystems like MSYS or CYGWIN. This PATH will be injected in the same order the build_requires " \
                  "are applied."
    settings = "os", "compiler", "build_type", "arch"

    def package_id(self):
        self.info.header_only()  # Only one package, like header only, actually an empty package

    def package_info(self):
        allvars = tools.vcvars_dict(self.settings)
        path = allvars["PATH"].split(os.pathsep)

        def relevant_path(path):
            return "Visual" in path or "Microsoft" in path or "MS" in path

        path = [entry for entry in path if relevant_path(entry)]  # very weak
        self.env_info.PATH = path
