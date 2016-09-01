import os
import sys
from setuptools import setup
from setuptools import find_packages


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner'] if needs_pytest else []

    setup_requires = ['build_capi>=0.0.8', 'ncephes>=0.1',
                      'cffi>=1.6'] + pytest_runner
    install_requires = ['pytest', 'ncephes>=0.1', 'scipy>=0.17',
                        'numpy>=1.9', 'numba>=0.27', 'cffi>=1.6',
                        'limix_math>=0.3', 'bidict', 'progressbar2>=3.10',
                        'h5py>=2.6', 'pandas>=0.18', 'nose>=1.3',
                        'tabulate>=0.7', 'six']
    tests_require = install_requires

    metadata = dict(
        name='lim',
        version='0.1.12',
        maintainer="Limix Developers",
        maintainer_email="horta@ebi.ac.uk",
        license="BSD",
        url='http://pmbio.github.io/limix/',
        packages=find_packages(),
        zip_safe=False,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        cffi_modules=["lim/reader/cplink/bed.py:ffi"],
        include_package_data=True,
    )

    try:
        from distutils.command.bdist_conda import CondaDistribution
    except ImportError:
        pass
    else:
        metadata['distclass'] = CondaDistribution
        metadata['conda_buildnum'] = 1
        metadata['conda_features'] = ['mkl']

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)

if __name__ == '__main__':
    setup_package()
