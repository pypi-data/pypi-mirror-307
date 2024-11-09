from setuptools import Extension
import os

ext_modules = [Extension(
        "msgspec._core",
        [os.path.join("msgspec", "_core.c")],
)]

def pdm_build_update_setup_kwargs(context, setup_kwargs):
    setup_kwargs.update(ext_modules=ext_modules)