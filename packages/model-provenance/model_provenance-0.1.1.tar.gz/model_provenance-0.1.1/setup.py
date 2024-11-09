from setuptools import setup, find_packages

setup(
    name='model_provenance',
    version='0.1.1',
    description='A package to track model metadata and provenance for scikit-learn and other ML models',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'joblib',
    ],
    python_requires='>=3.7',
)
