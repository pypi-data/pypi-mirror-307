from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name='mailoxy',
      version='1.0.2',
      description='maimai llc tool box',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='llc',
      author_email='gllc153220@gmail.com',
      packages=find_packages(),
      install_requires=[
          'httpx',
          'crypto',
          'pycryptodome',
          'orjson',
          'h2',
          'pydantic',
          'Loguru',
          'UnityPy',
          'Pillow',
          'asgiref'
      ],
      include_package_data=True,
      package_data={
          '': ['*.pyd'],
      },
      license='Mozilla Public License',
      platforms="windows",
      )
