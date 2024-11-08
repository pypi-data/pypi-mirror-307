#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
#
# List of environment variables used:
#
#  NLE_PACKAGE_NAME
#    Prefix of the generated package (defaults to "nle").
#
#  NLE_BUILD_RELEASE
#    If set, builds wheel (s)dist such as to prepare it for upload to PyPI.
#
#  HACKDIR
#    If set, install NetHack's data files in this directory.
#
#  USE_SEEDING
#    If set, seeding is disabled in all NLE environments.
#
import os
import pathlib
import subprocess
import sys
from distutils import spawn
from distutils import sysconfig

import setuptools
from setuptools.command import build_ext


class CMakeBuild(build_ext.build_ext):
    def run(self):  # Necessary for pip install -e.
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        source_path = pathlib.Path(__file__).parent.resolve()
        output_path = (
            pathlib.Path(self.get_ext_fullpath(ext.name))
            .parent.joinpath("nle")
            .resolve()
        )
        hackdir_path = os.getenv("HACKDIR", output_path.joinpath("nethackdir"))

        os.makedirs(self.build_temp, exist_ok=True)
        build_type = "Debug" if self.debug else "Release"

        generator = "Ninja" if spawn.find_executable("ninja") else "Unix Makefiles"

        use_seeding = os.environ.get("USE_SEEDING", "ON")
        use_seeding = {"1": "ON", "0": "OFF"}.get(use_seeding, use_seeding.upper())

        cmake_cmd = [
            "cmake",
            str(source_path),
            "-G%s" % generator,
            "-DPYTHON_SRC_PARENT=%s" % source_path,
            # Tell cmake which Python we want.
            "-DPYTHON_EXECUTABLE=%s" % sys.executable,
            "-DCMAKE_BUILD_TYPE=%s" % build_type,
            "-DCMAKE_INSTALL_PREFIX=%s" % sys.base_prefix,
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%s" % output_path,
            "-DHACKDIR=%s" % hackdir_path,
            "-DPYTHON_INCLUDE_DIR=%s" % sysconfig.get_python_inc(),
            "-DPYTHON_LIBRARY=%s" % sysconfig.get_config_var("LIBDIR"),
            "-DUSE_SEEDING=%s" % use_seeding,
        ]

        build_cmd = ["cmake", "--build", ".", "--parallel"]
        install_cmd = ["cmake", "--install", "."]

        try:
            subprocess.check_call(cmake_cmd, cwd=self.build_temp)
            subprocess.check_call(build_cmd, cwd=self.build_temp)
            # Installs nethackdir. TODO: Can't we do this with setuptools?
            subprocess.check_call(install_cmd, cwd=self.build_temp)
        except subprocess.CalledProcessError:
            # Don't obscure the error with a setuptools backtrace.
            sys.exit(1)


packages = [
    "nle",
    "nle.dataset",
    "nle.env",
    "nle.nethack",
    "nle.agent",
    "nle.scripts",
    "nle.tests",
    "nle.language_wrapper",
    "nle.language_wrapper.agents",
    "nle.language_wrapper.agents.sample_factory",
    "nle.language_wrapper.scripts",
    "nle.language_wrapper.tests",
    "nle.language_wrapper.wrappers",
]

entry_points = {
    "console_scripts": [
        "nle-play = nle.scripts.play:main",
        "nle-ttyrec = nle.scripts.ttyrec:main",
        "nle-ttyplay = nle.scripts.ttyplay:main",
        "nle-ttyplay2 = nle.scripts.ttyplay2:main",
        "nle-read-tty = nle.scripts.read_tty:main",
    ]
}


extras_deps = {
    "dev": [
        "pre-commit>=2.0.1",
        "isort>=5.13.2",
        "cmake_format>=0.6.10",
        "memory-profiler>=0.60.0",
        "pytest>=6.2.5",
        "pytest-benchmark>=3.4.1",
        "sphinx>=2.4.4",
        "sphinx-rtd-theme>=0.4.3",
        "setuptools>=69.5.1",
        "ruff>=0.4.3",
    ],
    "agent": ["torch>=1.3.1"],
}

extras_deps["all"] = [item for group in extras_deps.values() for item in group]


if __name__ == "__main__":
    package_name = "balrog_nle"
    # package_name = os.getenv("NLE_PACKAGE_NAME", "nle")
    cwd = os.path.dirname(os.path.abspath(__file__))
    version = open("version.txt", "r").read().strip()
    sha = "Unknown"

    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=cwd)
            .decode("ascii")
            .strip()
        )
    except subprocess.CalledProcessError:
        pass

    if sha != "Unknown" and not os.getenv("NLE_RELEASE_BUILD"):
        version += "+" + sha[:7]
    print("Building wheel {}-{}".format(package_name, version))

    version_path = os.path.join(cwd, "nle", "version.py")
    with open(version_path, "w") as f:
        f.write("__version__ = '{}'\n".format(version))
        f.write("git_version = {}\n".format(repr(sha)))

    with open("README.md") as f:
        long_description = f.read()

    setuptools.setup(
        name=package_name,
        version="0.9.0",
        description=("BALROG version of The NetHack Learning Environment (NLE)"),
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="The NLE Dev Team and BALROG",
        url="https://github.com/balrog-ai/nle",
        license="NetHack General Public License",
        entry_points=entry_points,
        packages=packages,
        ext_modules=[setuptools.Extension("nle", sources=[])],
        cmdclass={"build_ext": CMakeBuild},
        setup_requires=["pybind11>=2.2"],
        install_requires=["pybind11>=2.2", "numpy>=1.16", "gym==0.23"],
        extras_require=extras_deps,
        python_requires=">=3.8",
        classifiers=[
            "License :: OSI Approved :: Nethack General Public License",
            "Development Status :: 5 - Production/Stable",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: C",
            "Programming Language :: C++",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Games/Entertainment",
        ],
        zip_safe=False,
    )
