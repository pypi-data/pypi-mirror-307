import setuptools
from setuptools import setup, find_packages

# python setup.py install
setup(
    name='pissy',
    version='0.0.3',
    # packages=find_packages(where='src'),
    packages=setuptools.find_namespace_packages('src'),
    package_dir={'': 'src'},  # 指定包的根目录为src
    install_requires=[
        'typer>=0.12.0',
        'loguru==0.7.2',
        'setuptools',
        'sqlalchemy==2.0.36',
        'cx-oracle==8.3.0',
        'pymysql==1.1.1',
        'python-box==7.2.0',
        'jsonschema==4.23.0',
        'kafka-python-ng',
    ],
    entry_points={
        "console_scripts": [
            "pissy=pissy.app:main",
        ],
    },
)
