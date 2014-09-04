from fluenttest.test_case import TestCase

version_info = (3, 0, 0)
__version__ = '.'.join(str(x) for x in version_info)
__all__ = [
    'TestCase',
    '__version__',
    'version_info',
]
