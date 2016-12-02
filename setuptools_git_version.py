from distutils.errors import DistutilsSetupError
from pkg_resources import get_distribution
from subprocess import check_output


command = 'git describe --tags --long --dirty'
fmt = '{tag}.{commitcount}+{gitsha}'


def validate_version_format(dist, attr, value):
    try:
        version = check_output(command.split()).decode('utf-8').strip()
    except:
        version = get_distribution(dist.get_name()).version
    else:
        version = format_version(version=version, fmt=value)
    dist.metadata.version = version


def set_package_info(dist, attr, value):
    """
    Write the package version and package name
    into a file.
    """
    #1. Check that the version is set
    if not dist.metadata.version:
        if not hasattr(dist, 'version_format'):
             raise DistutilsSetupError('`version_format` must be set.')
        validate_version_format(dist, 'version_format', dist.version_format)
    #2. Write the version and name into the file
    with open(value, 'w') as f:
        f.write('__version__ = "{0}"\n'.format(dist.metadata.version))
        f.write('__name__ = "{0}"'.format(dist.get_name()))

def format_version(version, fmt=fmt):
    parts = version.split('-')
    assert len(parts) in (3, 4)
    dirty = len(parts) == 4
    tag, count, sha = parts[:3]
    if count == '0':# and not dirty:
        return tag
    return fmt.format(tag=tag, commitcount=count, gitsha=sha.lstrip('g'))


if __name__ == "__main__":
    # determine version from git
    git_version = check_output(command.split()).decode('utf-8').strip()
    git_version = format_version(version=git_version)

    # monkey-patch `setuptools.setup` to inject the git version
    import setuptools
    original_setup = setuptools.setup

    def setup(version=None, *args, **kw):
        return original_setup(version=git_version, *args, **kw)

    setuptools.setup = setup

    # import the packages's setup module
    import setup
