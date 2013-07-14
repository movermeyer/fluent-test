import inspect
import types


class ClassTester:

    def __init__(self, cls):
        self.cls = cls
        self.info = {}
        for attr in inspect.classify_class_attrs(self.cls):
            self.info[attr.name] = attr

    def implements_method(self, name):
        return name in self.info and self.info[name].kind == 'method'

    def is_subclass_of(self, parent_class):
        return issubclass(self.cls, lookup_class(parent_class))

    def has_attribute(self, name, typed=None):
        if name not in self.info:
            return False
        if typed is not None:
            return isinstance(getattr(self.cls, name), typed)
        return True


def the_class(cls, matcher_class=None):
    matcher_class = matcher_class or ClassTester
    return matcher_class(cls)


def lookup_class(class_name):
    if isinstance(class_name, types.StringTypes):
        path = class_name.split('.')
        target = __import__(path[0])
        for next_segment in path[1:]:
            target = getattr(target, next_segment)
        return target
    if isinstance(class_name, types.TypeType):
        return class_name
    if isinstance(class_name, types.ClassType):
        return class_name
    raise AssertionError("I can't look up a class name from " +
                         str(class_name))
