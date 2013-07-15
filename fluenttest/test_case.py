import mock


class _PrototypeObject:
    pass


class TestCase(object):
    allowed_exceptions = ()

    @classmethod
    def setup_class(cls):
        cls.exception = None
        cls.patches = _PrototypeObject()
        cls._patches = []

        cls.configure()
        try:
            cls.run_test()
        except cls.allowed_exceptions as exc:
            cls.exception = exc

    @classmethod
    def teardown_class(cls):
        for patcher in cls._patches:
            patcher.stop()

    @classmethod
    def configure(cls):
        pass

    @classmethod
    def patch(cls, target, patch_name=None, **kwargs):
        if patch_name is None:
            patch_name = target.replace('.', '_')
        patcher = mock.patch(target, **kwargs)
        patched = patcher.start()
        cls._patches.append(patcher)
        setattr(cls.patches, patch_name, patched)
        return patched

    @classmethod
    def patch_instance(cls, target, **kwargs):
        patched_class = cls.patch(target, **kwargs)
        return patched_class, patched_class.return_value

    @classmethod
    def run_test(cls):
        raise NotImplementedError
