from setuptools import setup


setup(
    name='setuptools-git-version',
    version='1.0.5',
    url='https://github.com/luxe-eng/setuptools-git-version',
    description='Automatically set package version from Git.',
    license='http://opensource.org/licenses/MIT',
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    py_modules=['setuptools_git_version'],
    install_requires=[
        'setuptools >= 8.0',
    ],
    entry_points="""
        [distutils.setup_keywords]
        version_format = setuptools_git_version:validate_version_format
        package_info = setuptools_git_version:set_package_info
    """,
)
