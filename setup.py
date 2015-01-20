from setuptools import setup

setup(name='IFUpy',
      version='0.1',
      description='IFU data analysis suite.',
      url='',
      author='Nicholas Earl, Tommy LeBlanc',
      author_email='nearl@stsci.edu, tl.commodore@gmail.com',
      license='Claus-3 BSD',
      packages=['ifupy'],
      zip_safe=False,
      install_requires=['numpy>=1.9.0',
                        'scipy>=0.14',
                        'astropy>=0.4.2'])