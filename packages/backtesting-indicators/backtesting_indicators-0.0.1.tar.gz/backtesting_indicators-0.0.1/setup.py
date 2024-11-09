from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Libreria de indicadores de pandas-ta para usar en backtesting.py'
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
# Configurando
setup(
        name="backtesting_indicators", 
        version=VERSION,
        author="Mariano Damian Ferro Villanueva",
        author_email="<ferro.mariano@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/ferromariano/backtesting-indicators",
        packages=find_packages(),
        install_requires=[
            'backtesting',
            'pandas-ta',
            'pandas',
        ], 
        keywords=['python', 'backtesting.py', 'backtesting', 'indicators'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)