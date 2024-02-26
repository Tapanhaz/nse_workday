from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='nse_workday',
   version='0.0.5',
   description='For Calculating days based on NSE Holidays(2010-2024)',
   author='Tapan Hazarika',
   url='https://github.com/Tapanhaz/nse_workday',
   long_description=long_description,
   long_description_content_type="text/markdown",
   packages=['nse_workday'],
   package_data={'nse_workday': ['hlist.d', 'exclist.d', 'py.typed', '__init__.pyi', 'nse_workday.pyi']}
)