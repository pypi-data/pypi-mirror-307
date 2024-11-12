from os.path import isdir, join
from platform import system

from setuptools import Extension, find_packages, setup
from setuptools.command.build import build
from wheel.bdist_wheel import bdist_wheel


class Build(build):
    def run(self):
        if isdir("queries"):
            dest = join(self.build_lib, "caqtus_parsing", "queries")
            self.copy_tree("queries", dest)
        super().run()


class BdistWheel(bdist_wheel):
    def get_tag(self):
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp312", "abi3"
        return python, abi, platform


setup(
    packages=find_packages("bindings/python/src"),
    package_dir={"": "bindings/python/src"},
    package_data={
        "caqtus_parsing": ["*.pyi", "py.typed"],
        "caqtus_parsing.queries": ["*.scm"],
    },
    ext_package="caqtus_parsing",
    ext_modules=[
        Extension(
            name="_binding",
            sources=[
                "bindings/python/src/caqtus_parsing/binding.c",
                "src/parser.c",
                # NOTE: if your language uses an external scanner, add it here.
            ],
            extra_compile_args=(
                [
                    "-std=c11",
                    "-fvisibility=hidden",
                ]
                if system() != "Windows"
                else [
                    "/std:c11",
                    "/utf-8",
                ]
            ),
            define_macros=[
                ("Py_LIMITED_API", "0x03090000"),
                ("PY_SSIZE_T_CLEAN", None),
                ("TREE_SITTER_HIDE_SYMBOLS", None),
            ],
            include_dirs=["src"],
            py_limited_api=True,
        )
    ],
    cmdclass={"build": Build, "bdist_wheel": BdistWheel},
    zip_safe=False,
)
