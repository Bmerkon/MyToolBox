from setuptools import setup,find_packages

setup(name='bmerkon_toolbox',
      version='0.1',
      description='Bmerkon own work',
      author='Bmerkon',
      author_email='pizza1989521.ok@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False, 
      install_requires=['numpy', 'pandas', 'sklearn'])
