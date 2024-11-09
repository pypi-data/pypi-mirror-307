from setuptools import setup, find_packages

setup(
    name='quiet-nebula',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'quiet-nebula=quiet_nebula.cli:main',
        ],
    },
    description='A package to analyze sales data from a CSV file.',
    author='Semyon Drozdov',
    author_email='s.drozdov@edu.centraluniversity.ru',
)
