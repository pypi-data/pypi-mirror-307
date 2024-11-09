from setuptools import setup, find_packages
from blackforge import version

setup(
    name='Blackforge',
    version=f"{version.BLACKFORGE_MAJOR}.{version.BLACKFORGE_MINOR}.{version.BLACKFORGE_PATCH}",
    description='Light Shines Brighter In The Dark.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zeroth.bat@gmail.com',
    url='https://github.com/d34d0s/BlackForge',
    packages=find_packages(),
    package_data={"blackforge": ['assets/*']},
    install_requires=[
        "GLFW",
        "Numpy",
        "Numba",
        "PyGLM",
        "PyOpenGL",
        "ModernGL",
        "Pygame-CE",
        "SetupTools",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)