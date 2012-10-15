import os
import sys

from setuptools import setup, find_packages

extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(name='nbt2yaml',
      version="0.2.1",
      description="Read and write Minecraft NBT files using Yaml.",
      long_description=file(readme).read(),
      classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      ],
      keywords='minecraft',
      author='Mike Bayer',
      author_email='mike_mp@zzzcomputing.com',
      url='http://bitbucket.org/zzzeek/nbt2yaml',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      zip_safe=False,
      install_requires=['PyYAML'],
      scripts=[
                'scripts/nbtedit',
                'scripts/nbt2yaml',
                'scripts/yaml2nbt'
                ],
      test_suite='nose.collector',
      tests_require=['nose'],
      **extra
)
