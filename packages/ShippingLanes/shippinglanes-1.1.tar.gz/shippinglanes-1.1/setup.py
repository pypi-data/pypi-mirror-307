from setuptools import setup, Extension
import pybind11

cpp_args = ['-std=c++11', '-stdlib=libc++', '-mmacosx-version-min=10.7']

sfc_module = Extension(
    'ShippingLanes',
    sources=['module.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=cpp_args,
)

setup(
    name='ShippingLanes',
    version='1.1',
    description='Python package that routes shipping lanes against US highway networks.',
    ext_modules=[sfc_module],
)