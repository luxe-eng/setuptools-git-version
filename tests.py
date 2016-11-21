import mock
from pytest import mark
from setuptools_git_version import format_version, set_package_info


@mark.parametrize('git_describe, version', [
    ('v25.6-879-gca0be43', 'v25.6.dev879+ca0be43'),
    ('28-0-gca0be43', '28'),
    ('28.0-0-gca0be43', '28.0'),
    ('28.0-1-gca0be43', '28.0.dev1+ca0be43'),
])
def test_git_describe(git_describe, version):
    fmt = '{tag}.dev{commitcount}+{gitsha}'
    assert format_version(git_describe, fmt) == version


def test_set_package_info_ok(tmpdir):
    """
    Simple test of set_package_info(). Must succeed.
    """
    tempfile = tmpdir.join('__pkg__.py')
    dist = mock.MagicMock(get_name=lambda: 'foobar')
    dist.metadata = mock.MagicMock(version='28')
    with mock.patch('setuptools_git_version.validate_version_format', mock.MagicMock()):
        set_package_info(dist, 'package_info', str(tempfile))
    assert tempfile.read() == '''__version__ = "28"
__name__ = "foobar"'''
