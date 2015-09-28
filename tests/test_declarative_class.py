from collections import OrderedDict
from tri.struct import Struct

from tri.declarative.declarative import declarative_member, declarative


@declarative_member
class Member(Struct):
    pass


@declarative(Member)
class Declarative(object):
    def __init__(self, members):
        self.members = members


def test_constructor_noop():

    subject = Declarative(members={'foo': Member(foo='bar')})

    assert subject.members == {'foo': Member(foo='bar')}


def test_find_members():

    class MyDeclarative(Declarative):
        foo = Member(foo='bar')

    subject = MyDeclarative()
    assert OrderedDict([('foo', Member(foo='bar'))]) == subject.members


def test_find_members_inherited():

    class MyDeclarative(Declarative):
        foo = Member(foo='bar')

    class MyDeclarativeSubclass(MyDeclarative):
        bar = Member(foo='baz')

    subject = MyDeclarativeSubclass()
    assert OrderedDict([('foo', Member(foo='bar')), ('bar', Member(foo='baz'))]) == subject.members


def test_find_members_from_base():

    @declarative(Member)
    class Base(object):
        foo = Member(foo='foo')

    class Sub(Base):
        bar = Member(bar='bar')

    assert OrderedDict([('foo', Member(foo='foo')), ('bar', Member(bar='bar'))]) == Sub.Meta.members


def test_find_members_shadow():
    @declarative(Member)
    class Base(object):
        foo = Member(bar='bar')

    class Sub(Base):
        foo = Member(bar='baz')

    assert OrderedDict([('foo', Member(bar='baz'))]) == Sub.Meta.members


def test_member_attribute_naming():

    @declarative(Member, 'foo')
    class Declarative(object):
        def __init__(self, foo):
            self.foo = foo

    class MyDeclarative(Declarative):
        bar = Member(baz='buzz')

    subject = MyDeclarative()
    assert OrderedDict([('bar', Member(baz='buzz'))]) == subject.foo

