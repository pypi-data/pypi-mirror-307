from setuptools import setup, find_packages
import sys

# Check the Python version before proceeding with the setup
if sys.version_info < (3, 10):
    sys.exit('Python >= 3.10 is required. Your version is {}'.format(sys.version))

setup(
    name='bahc',
    version='2.0.3',
    description='Bootstrap Average Hierarchical Clustering for filtering covariance matrices',
    author='Christian Bongiorno',
    author_email='christian.bongiorno@centralesupelec.fr',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bongiornoc/bahc',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'statsmodels',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)