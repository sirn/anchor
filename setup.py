from setuptools import setup, find_packages

requires = ["twisted"]
setup(
    name='Anchor',
    version='0.1',
    description='Local DNS responder and port forwarding tool',
    author='Kridsada Thanabulpong',
    author_email='sirn@ogsite.net',
    url='http://code.grid.in.th/',
    packages=find_packages(),
    install_requires=requires)
