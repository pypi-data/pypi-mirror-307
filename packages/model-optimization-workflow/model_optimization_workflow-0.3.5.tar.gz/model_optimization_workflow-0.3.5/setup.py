from setuptools import setup, find_packages

setup(
    name='model_optimization_workflow',
    version='0.3.5',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'configs': ['*.yaml'],
    },
    install_requires=[
        'matplotlib',
        'seaborn',
        'optuna~=4.0.0',
        'pyyaml',
        'market-data-assembler~=1.0.6',
        'scikit-learn',
        'plotly',
        'openpyxl'
    ],
    author='Maksym Usanin',
    author_email='usanin.max@gmail.com',
    description='Model optimization workflow',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
