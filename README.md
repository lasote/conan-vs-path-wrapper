# conan-vs-path-wrapper

Disclaimer
==========

This will work only from Conan 1.0


Introduction
============

When you are using a Windows subsystem like ``MSYS2`` or ``CYGWIN``, sometimes you want to use your Visual Studio
compiler or an specific MinGW but the build tools from the subsystem, like ``make``.

You can use a profile to use MSYS2 and MinGW with the exact version do you need:

```
include(default)

[build_requires]
mingw_installer/1.0@conan/stable # Will be installed with the version according to the settings below.
msys2_installer/latest@bincrafters/stable


[settings]
compiler=gcc
compiler.version=5.4
compiler.libcxx=libstdc++11
compiler.exception=seh
compiler.threads=posix
```

When you execute ``self.run`` passing the parameter ``win_bash=True``, Conan internally will execute the available
"bash.exe" and adjust the PATH inside the shell prepending all the ``self.deps_env_info`` PATH variables,
(the requires declared paths):

You can run a command specifying that it will run in the available bash:

``` 

   self.run("./configure", win_bash=True)

```

So, in this case, Conan will put in the PATH the MinGW, then the MSYS2. So, will locate the "bash.exe" from
the MSYS2 package, and, inside the bash.exe, will locate first the mingw compiler `gcc.exe`.


Why this package?
=================

If you want the Visual Studio compiler available, with Conan you can use the build helper ``MSBuild`` to build
a project, or just ``vcvars_command`` or ``vcvars`` context manager to adjust the needed environment variables to locate
the Visual Studio compiler and build tools.

But there are situations where the PATHS collide. For example, the linker from Visual Studio ``link.exe`` collides with a ``link`` command 
from the subsystem (command to manage simbolic links), that is because, as Visual Studio is not a ``build_require``
the specified build_requires PATH will be put before all the rest. So it can happen that the build system of 
a library, expecting MSYS2 tools but the Visual Studio compiler, will fail.

This situation happens in the ICU library and ffmpeg, for example.

This package internally uses the ``vcvars`` to declare in the ``self.env_info`` the PATH, so now we can
specify the build_require in the right order and Conan will inject the Visual Studio path in the right order:

``` 

include(default)

[build_requires]
vswrapper/1.0@conan/testing
msys2_installer/latest@bincrafters/stable

```

Now if we run the command again, the Visual Studio PATHs will be first, then the msys2 directories:

``` 

   self.run("./configure", win_bash=True)

```