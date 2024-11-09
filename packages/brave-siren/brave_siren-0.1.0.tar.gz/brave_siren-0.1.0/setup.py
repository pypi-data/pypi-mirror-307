from setuptools import setup, find_packages

setup(
    name='brave_siren',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'brave-siren=brave_siren.cli:main',
        ],
    },
    description='A package to generate receipts from order data in JSON format.',
    author='Semyon Drozdov',
    author_email='s.drozdov@edu.centraluniversity.ru',
)
