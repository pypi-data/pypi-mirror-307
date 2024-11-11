from setuptools import setup,find_packages
setup(name='OSM2LES',
      version='0.0.18',
      description='Transfer building footprint to 2D DEM for LES simulation',
      author=['Jiachen Lu','Negin Nazarian','Melissa Hart'],
      author_email='jiachensc@gmail.com',
      requires= ['numpy','matplotlib','shapely','pandas','scipy','osmnx'], 
      install_requires= ['numpy','matplotlib','shapely','pandas','scipy','osmnx','netCDF4'], 
      packages=["OSM2LES"],
      license="MIT",
      python_requires=">=3.6",
      )
