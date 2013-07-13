import inspect
import unittest

import mock

import fluenttest


class MockedTestCase(fluenttest.TestCase):
    __test__ = False

    configure = mock.Mock()
    run_test = mock.Mock()


class FluentTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.class_attrs = dict(
            (a.name, a)
            for a in inspect.classify_class_attrs(fluenttest.TestCase)
        )

    def should_implement_setup_class(self):
        self.assert_is_class_method('setup_class')

    def should_implement_teardown_class(self):
        self.assert_is_class_method('teardown_class')

    def should_implement_configure(self):
        self.assert_is_class_method('configure')

    def should_implement_run_test(self):
        self.assert_is_class_method('run_test')

    def assert_is_class_method(self, name):
        self.assertEquals(self.class_attrs[name].kind, 'class method')


class SetupClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test = MockedTestCase()
        cls.test.setup_class()

    def should_call_configure(self):
        self.test.configure.assert_called_once_with()

    def should_call_run_test(self):
        self.test.run_test.assert_called_once_with()

    def should_create_patches_attribute(self):
        self.assertIsNotNone(getattr(self.test, 'patches'))

    def should_create_and_initialize_exception_attribute(self):
        self.assertIsNone(self.test.exception)


class _PatchedBaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with mock.patch('fluenttest.test_case.mock') as cls.mock_module:
            cls.patcher = cls.mock_module.patch.return_value
            cls.test = MockedTestCase()
            cls.test.setup_class()
            cls.execute_test_steps()
            cls.test.teardown_class()


class TeardownClass(_PatchedBaseTest):

    @classmethod
    def execute_test_steps(cls):
        cls.patches = [mock.Mock(), mock.Mock()]
        cls.mock_module.patch.side_effect = cls.patches

        cls.test.patch('first_patch')
        cls.test.patch('second_patch')

    def should_stop_all_patches(self):
        for patcher in self.patches:
            patcher.stop.assert_called_once_with()


class _WhenPatchingBaseCase(_PatchedBaseTest):

    patch_target = None
    specified_patch_name = None
    kwargs = {'arg': mock.sentinel.arg}

    @classmethod
    def execute_test_steps(cls):
        cls.return_value = cls.test.patch(
            cls.patch_target,
            patch_name=cls.specified_patch_name,
            **cls.kwargs
        )

    def should_patch_target(self):
        self.mock_module.patch.assert_any_call(
            self.patch_target, **self.kwargs)

    def should_start_patch(self):
        self.patcher.start.assert_called_once_with()

    def should_return_patch(self):
        self.assertIs(self.return_value,
                      self.patcher.start.return_value)


class WhenPatchingSimpleTarget(_WhenPatchingBaseCase):

    patch_target = 'simple_target'

    def should_register_patch_name_asis(self):
        self.assertIs(self.test.patches.simple_target, self.return_value)


class WhenPatchingDottedTarget(_WhenPatchingBaseCase):

    patch_target = 'dotted.name'

    def should_register_sanitized_patch_name(self):
        self.assertIs(self.test.patches.dotted_name, self.return_value)


class WhenPatchingWithNameSpecified(_WhenPatchingBaseCase):

    patch_target = 'patch.target'
    specified_patch_name = 'name_override'

    def should_register_with_specified_name(self):
        self.assertIs(self.test.patches.name_override, self.return_value)


class WhenPatchingAnInstance(_PatchedBaseTest):

    patch_target = 'target.class'
    kwargs = {'kwarg': mock.sentinel.kwarg}

    @classmethod
    def execute_test_steps(cls):
        cls.patched_class = cls.patcher.start.return_value
        cls.return_value = cls.test.patch_instance(
            'target.class', **cls.kwargs)

    def should_register_patched_class(self):
        self.assertIs(
            self.test.patches.target_class,
            self.patched_class,
        )

    def should_return_patched_class_and_new_instance(self):
        self.assertEquals(
            self.return_value,
            (self.patched_class, self.patched_class.return_value),
        )

    def should_call_patch(self):
        self.mock_module.patch.assert_called_once_with(
            self.patch_target, **self.kwargs)


class WhenPatchingAnInstanceWithNameSpecified(WhenPatchingAnInstance):

    patch_target = 'class.name'

    @classmethod
    def execute_test_steps(cls):
        cls.patched_class = cls.patcher.start.return_value
        cls.return_value = cls.test.patch_instance(
            'class.name', patch_name='target_class', **cls.kwargs)


class TheDefaultRunTestImplementation(unittest.TestCase):

    def should_raise_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            fluenttest.TestCase.run_test()


class WhenRunTestRaiseException(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raised_exception = Exception()
        cls.test = MockedTestCase()
        cls.test.run_test.side_effect = cls.raised_exception

        cls.test.setup_class()

    def it_should_be_captured(self):
        self.assertIs(self.test.exception, self.raised_exception)
