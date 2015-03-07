from distutils.core import setup

setup(
    name='colors',
    version='0.0.1',
    author='Erin Braswell and Fabian von Feilitzsch',
    author_email='erin@cos.io',
    packages=['colors'],
    url='https://github.com/erinspace/colors',
    license='LICENSE',
    description='Generate random colors for use in graphs, or anywhere you want some colors!',
    long_description=open('README').read(),
    install_requires=['webcolors']
)
