from distutils.core import setup

setup(
    name='TEPSimulation',
    version='0.1dev',
    description='Python implementation of the Tennessee Eastman simulation',
    author='Hussein Saafan',
    author_email='hsaafan@uwaterloo.ca',
    url='https://github.com/hsaafan/TEPSimulation',
    packages=['tepsimulation', ],
    license='MIT License',
    long_description=open('README.MD').read(),
)
