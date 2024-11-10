#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Programming Acessory Kit Repo
# ..................................
# Copyright (c) 2018-2023, reactive-firewall
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/pypak/LICENSE.md
# ......................................................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ......................................................................

import weakref as _weakref

__all__ = [
	"""__package__""", """__module__""", """__name__""", """__doc__""",
	"""nothing""", """anything"""
]


__package__ = """pypak"""


__module__ = """pypak.anything"""


__file__ = """pypak/anything.py"""


__doc__ = """In OOP everything is something so the base object can be anything.

	Minimal Acceptance Testing:

	First setup test fixtures by importing anything.

	>>> import pypak
	>>>

	>>> pypak.anything.__doc__ is not None
	True
	>>>

	Testcase 0: Anything should be.

	>>> pypak.anything.anything() is not None
	True
	>>>

	Testcase 1: Anything should be identifiable.
		A: Test that the __id__ atribute is initialized.
		B: Test that the __id__ atribute is an int.

	>>> pypak.anything.anything().__id__ is not None
	True
	>>>
	>>> isinstance(pypak.anything.anything().__id__, int)
	True
	>>>

	Testcase 2: Instances of Anything should be identifiable by thier hash.
		A: Test creating an instance.
		B: Test an instance is identifiable.
		C: Test an instance is identifiable by it's hash.

	>>> any_thing_fixture = pypak.anything.anything()
	>>> any_thing_fixture.__id__ is not None
	True
	>>> any_thing_fixture.__id__ == hash(any_thing_fixture)
	True
	>>> isinstance(any_thing_fixture.__id__, int)
	True
	>>>

	Testcase 3: Instances of Anything should be new-style python classes with a __dict__ attribute.
		A: Test that the __dict__ atribute is initialized
		B: Test that the __dict__ atribute is a dict.

	>>> pypak.anything.anything().__dict__ is not None
	True
	>>>

"""


class nothing(object):
	"""
		Metaclass wrapper for everything. Anything can be nothing ... go figure.

		Testing:

		Testcase 1: Test nothing.
			A: import the module pypak.anything (Test Fixture)
			B: Test that nothing is part of the module pypak.anything

		>>> import pypak.anything
		>>>
		>>> pypak.anything.nothing.__module__ is not None
		True
		>>>
		>>> pypak.anything.nothing.__module__ is None
		False
		>>>
		>>> print(pypak.anything.nothing.__module__) #doctest: +ELLIPSIS
		pypak.anything
		>>>
		>>> print(pypak.anything.nothing.__name__)
		nothing
		>>>

	"""

	__module__ = """pypak.anything"""

	__name__ = """nothing"""

	__slots__ = ("""__weakref__""", """__real_data__""", """__real_id__""",)

	def __init__(self, **kwds):
		"""
			Wrapper for object.__init__ constructor.

			Testing:

			Testcase 1: Test by call.
				A: import the module pypak.anything (Test Fixture)
				B: Test that nothing can be.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>> fixturecls is not None
			True
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>

		"""
		self.__real_data__ = None
		self.__real_id__ = None

	def __get_data__(self):
		"""
			Wrapper for object.__get__ descriptor

			Testing:

			Testcase 1: Test by call.
				A: import the module pypak.anything (Test Fixture)
				B: Test that data can be extracted.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__get_data__()
			{}
			>>>

		"""
		if not getattr(self, """__real_data__""", None):
			return dict({})
		return self.__real_data__

	def __set_data__(self, value):
		"""
			Wrapper for object.__get__ descriptor

			Testing:

			Testcase 1: Test by call to get.
				A: import the module pypak.anything (Test Fixture)
				B: Test that data can be extracted.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__set_data__({}) #doctest: +ELLIPSIS
			>>> fixturecls.__get_data__() #doctest: +ELLIPSIS
			{}
			>>>

			Testcase 2: Test by call to set.
				A: import the module pypak.anything (Test Fixture)
				B: Test that data can be set and extracted.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{}
			>>>
			>>> fixturecls.__data__ = {"data": "it works", "matter": object()}
			>>>
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>>
			>>> fixturecls.__data__ = {"data": "it still works", "nope": 1} #doctest: +ELLIPSIS
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{...it still works...}
			>>>

		"""
		def __quantum_physics(__quantum, __non_quantum_keys):
			"""Magic unicorn power. TL;DR; Used to weakref stuff"""
			for __quark_state, __quark in __quantum.items():
				if __quark_state not in __non_quantum_keys:
					try:
						yield __quark_state, _weakref.ref(__quark)
					except TypeError:
						yield __quark_state, __quark
		__volatile_keys__ = nothing.__slots__ # ["""__dict__""", """__real_data__""", """__real_id__"""]
		if not getattr(self, """__real_data__""", None):
			self.__real_data__ = dict({})
		self.__real_data__ = dict({k: v for k, v in __quantum_physics(value, __volatile_keys__)})
		self.__real_id__ = id(self.__real_data__)

	def __del_data__(self):
		"""
			Wrapper for object.__get__ descriptor

			Testing:

			Testcase 1: Test by call.
				A: import the module pypak.anything (Test Fixture)
				B: Test that data can be set and extracted.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__del_data__() # no errors expected
			>>>

			Testcase 2: Test by call to del.
				A: import the module pypak.anything (Test Fixture)
				B: Test that data can be set and extracted and de-alocated.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{}
			>>>
			>>> fixturecls.__data__ = {"data": "it works"} #doctest: +ELLIPSIS
			>>>
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>>
			>>> del fixturecls.__data__ # no errors expected
			>>>

		"""
		if self.__real_data__:
			del self.__real_data__

	def __get_id__(self):
		"""
			Wrapper for object.__get__ descriptor

			Testing:

			Testcase 1: Test by call.
				A: import the module pypak.anything (Test Fixture)
				B: Test that id can be calculated.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__get_id__() > 0
			True
			>>> fixturecls.__get_id__() == id(fixturecls.__real_data__)
			True
			>>> fixturecls.__get_id__() == fixturecls.__get_id__()
			True
			>>> id(fixturecls.__real_data__) == id(fixturecls.__real_data__)
			True
			>>>
			>>> id(fixturecls.__real_data__) == fixturecls.__get_id__()
			True
			>>>

		"""
		if not self.__real_id__:
			return id(self.__real_data__)
		return self.__real_id__

	def __set_id__(self, value):
		"""
			Wrapper for object.__set__ descriptor

			Testing:

			Testcase 1: Test by call to get.
				A: import the module pypak.anything (Test Fixture)
				B: Test that id can be calculated.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__set_id_(123) #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...is read only...
			>>>
			>>> fixturecls.__get_id__() > 0 #doctest: +ELLIPSIS
			True
			>>>

			Testcase 2: Test by altering __data__.
				A: import the module pypak.anything (Test Fixture)
				B: Test that id can be calculated.
				C: Test that __data__ can be changed.
				D: Test that id can be recalculated (and is not same as B.)

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>> fixturecls.__set_id_(123) #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...is read only...
			>>> fixturecls.__get_id__() > 0 #doctest: +ELLIPSIS
			True
			>>> old_fixture_id = int(fixturecls.__get_id__())
			>>> fixturecls.__data__ = {"data": "it works"}
			>>> new_fixture_id = int(fixturecls.__get_id__())
			>>> fixturecls.__get_id__() == new_fixture_id
			True
			>>> fixturecls.__get_id__() == old_fixture_id
			False
			>>>
			>>> old_fixture_id != new_fixture_id
			True
			>>>

		"""
		raise AttributeError("""'__id__' is read only""")

	def __del_id__(self):
		"""
			Wrapper for object.__del__ descriptor

			Testing:

			Testcase 1: Test by call.
				A: import the module pypak.anything (Test Fixture)
				B: Test that id can be de-alocated.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>> fixturecls.__del_id__() # no errors expected
			>>>

			Testcase 2: Test by call to del.
				A: import the module pypak.anything (Test Fixture)
				B: Test that id can be set and extracted and de-alocated.

			>>> import pypak.anything
			>>>
			>>> fixturecls = nothing()
			>>>
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>>
			>>>
			>>> fixturecls.__real_id__ = 123 #doctest: +ELLIPSIS
			>>> del fixturecls.__id__ # no errors expected
			>>>

		"""
		if self.__real_id__:
			del self.__real_id__

	def __repr__(self):
		"""Overloads __builtin__.object.__rpr__(self) and __builtin__.type.__rpr__(self)

			Reports this is a none type. Literally:
				<class nothing>

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: nothing is representable as text.

			>>> repr(pypak.anything.nothing()) is not None
			True
			>>> print(repr(pypak.anything.nothing())) #doctest: +ELLIPSIS
			<class \'pypak.anything.nothing\'>
			>>>

		"""
		return str("""{open}class \'{name}\'{close}""").format(
			name=str("""{mod}.{cls}""").format(
				mod=str(self.__class__.__module__), cls=str(self.__class__.__name__)
			),
			open="""<""",
			close=""">"""
		)

	def __del__(self):
		"""Overloads __builtin__.object.__del__(self)

			Inverse of __init__. Literally: anti-nothing

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: nothing is anihalated without complaint.

			>>> quantum = pypak.anything.nothing()
			>>> quantum is not None
			True
			>>> del quantum
			>>> quantum.__dict__ #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			NameError: name 'quantum' is not defined
			>>>

		"""
		self.__del_id__()
		self.__del_data__()

	__data__ = property(
		__get_data__, __set_data__, __del_data__,
		"""Stores Instance data of anything.

			Full dynamic lifecycle usage...

			Example: Test by calls to get/set/del.
				A: imports the module pypak.anything (Example Fixture)
				B: Shows that data can be set and extracted and de-alocated.

			>>> import pypak.anything as _anything
			>>>
			>>> fixturecls = _anything.nothing()
			>>> type(fixturecls)
			<class 'pypak.anything.nothing'>
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{}
			>>> fixturecls.__data__ = {"data": "it works"} #doctest: +ELLIPSIS
			>>> fixturecls.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>> del fixturecls.__data__ # no errors expected
			>>>

		"""
	)

	__id__ = property(
		__get_id__, __set_id__, __del_id__,
		"""Instance ID of anything based on it's data.

			Full dynamic lifecycle usage...

			Example: Test by calls to get/set/del.
				A: imports the module pypak.anything (Example Fixture)
				B: Shows that __id__ can extracted and de-alocated but not directly set.

			>>> import pypak.anything as _anything
			>>>
			>>> mynothing = _anything.nothing()
			>>> type(mynothing)
			<class 'pypak.anything.nothing'>
			>>> isinstance(mynothing.__id__, int) or isinstance(mynothing.__id__, long)
			True
			>>> mynothing.__id__ = {"id": "won't work"} #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...is read only...
			>>>
			>>> isinstance(mynothing.__id__, int) or isinstance(mynothing.__id__, long)
			True
			>>> del mynothing.__id__ # no errors expected
			>>>

		"""
	)


class anything(nothing):
	"""
		Generic anything object.

		data stops here: see https://docs.python.org/2.7/reference/datamodel.html#invoking-descriptors

		Testing:

		Testcase 1: Test nothing.
			A: import the module pypak.anything (Test Fixture)
			B: Test that anything is part of the module pypak.anything

		>>> import pypak.anything
		>>>
		>>> pypak.anything.anything.__module__ is not None
		True
		>>>
		>>> pypak.anything.anything.__module__ is None
		False
		>>>
		>>> print(pypak.anything.anything.__module__) #doctest: +ELLIPSIS
		pypak.anything
		>>>
		>>> print(pypak.anything.anything.__name__) #doctest: +ELLIPSIS
		anything
		>>>

	"""

	__module__ = """pypak.anything"""

	__name__ = """anything"""

	def __init__(self, *args, **kwds):
		"""
			Initializes the ID of anything.
			:Returns self: - the anything instance

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 0: Anything should be.

			>>> pypak.anything.anything() is not None
			True
			>>>

			Testcase 1: Anything should not be just some object.
				A: Test creating anything
				B: Test creating an object ()
				C: Test the test fixtures are different instances

			>>> any_thing = pypak.anything.anything()
			>>> some_object = object()
			>>> any_thing is not None
			True
			>>> some_object is not None
			True
			>>> any_thing is not some_object
			True
			>>> some_object is not any_thing
			True
			>>> print(type(any_thing)) #doctest: +ELLIPSIS
			<... \'pypak.anything.anything\'>
			>>>

			Testcase 2 (Really Testcase 1 continued)
				Re-Use A thru C as a fixture
				D: Anything should not be just some object but can be an object.

			>>> any_thing = pypak.anything.anything()
			>>> some_object = object()
			>>> any_thing is not None
			True
			>>> some_object is not None
			True
			>>> any_thing is not some_object
			True
			>>> some_object is not any_thing
			True
			>>> type(any_thing) is not type(some_object)
			True
			>>> type(some_object) is not type(any_thing)
			True
			>>> isinstance(any_thing, type(some_object))
			True
			>>> isinstance(some_object, type(any_thing))
			False
			>>> issubclass(type(any_thing), type(some_object))
			True
			>>>

			Testcase 3: Anything should not be just some object.
				A: Test creating anything with some data

			>>> mapping = dict({"__real_data__": dict({"thetest": "it works"})})
			>>> any_thing = pypak.anything.anything(**mapping)
			>>> any_thing is not None
			True
			>>> any_thing.__data__ is not None
			True
			>>> print(type(any_thing)) #doctest: +ELLIPSIS
			<... \'pypak.anything.anything\'>
			>>> any_thing.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>>

		"""
		super(anything, self).__init__(*args, **kwds)
		for key, value in kwds.items():
			if key not in nothing.__slots__:
				super(anything, self).__setattr__(key, value)
			else:
				super(nothing, self).__setattr__(key, value)

	def __getattr__(self, name):
		"""
			Overloads object.__getattr__(self, name) to support __id__

			:Param self: - An Anything instance.
			:Param name: - The name of an attribute or the key of a Key Value Pair (kvp).
			:Returns value: - The value of the data if found.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be identifiable.
				A: Test that the __id__ atribute is initialized.
				B: Test that the __id__ atribute is an int.

			>>> pypak.anything.anything().__id__ is not None
			True
			>>>
			>>> isinstance(pypak.anything.anything().__id__, int)
			True
			>>>

			Testcase 2: Anything should be a type.
				A: Test that the __id__ atribute is initialized.
				B: Test that the __id__ atribute is an int.

			>>> pypak.anything.anything().__id__ is not None
			True
			>>>
			>>> isinstance(pypak.anything.anything().__id__, int)
			True
			>>>

			Testcase 3: Instances of Anything should be new-style types with a __dict__ attribute.
				A: Test that the __dict__ atribute is initialized
				B: Test that the __dict__ atribute is a class __dict__ attribute (i.e. NOT a dict)

			>>> test_fixture = pypak.anything.anything()
			>>> test_fixture.__getattr__("__dict__") #doctest: +ELLIPSIS
			{}
			>>> test_fixture.__dict__ is not None
			True
			>>> isinstance(test_fixture.__dict__, dict)
			True
			>>>

			Testcase 4: Instances of Anything should always have an id even when they don't.
				A: Test that the __id__ atribute is generated from nothing when needed

			>>> paradox_fixture = pypak.anything.anything()
			>>> paradox_fixture.__getattr__("__id__") is not None
			True
			>>> paradox_fixture.__getattr__("__id__") is not id(paradox_fixture)
			True
			>>> paradox_fixture.__getattr__("__id__") == hash(paradox_fixture)
			True
			>>> paradox_fixture.__getattr__("__id__") == paradox_fixture.__id__
			True
			>>>

			Testcase 3: Instances of Anything should have a __data__ attribute.
				A: Test that the __data__ atribute is initialized
				B: Test that the __data__ atribute is a dict.

			>>> test_fixture = pypak.anything.anything()
			>>> test_fixture.__getattr__("__data__") #doctest: +ELLIPSIS
			{}
			>>> test_fixture.__data__ is not None
			True
			>>> isinstance(test_fixture.__data__, dict)
			True
			>>>

		"""
		if str(name) == str("""__data__""") or str(name) == str("""data"""):
			return self.__getattribute__("""__data__""")
		elif str(name) == str("""__id__""") or str(name) == str("""id"""):
			return self.__getattribute__("""__id__""")
		elif str("""__real_data__""") not in str(name) and str(name) in sorted(self.__data__.keys()):
			return self.__getattribute__("""__data__""").__getitem__(name)
		elif str(name) == str("""__dict__"""):
			return self.__getattr__("""__data__""")
		else:
			return super(anything, self).__getattribute__(name)

	def __getattribute__(self, name):
		"""
			Overloads object.__getattribute__(self, name) to support __id__

			:Param self: - An Anything instance.
			:Param name: - The name of an attribute or the key of a Key Value Pair (kvp).
			:Returns value: - The value of the data if found.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be identifiable.
			A: Test that the __id__ atribute is initialized.
			B: Test that the __id__ atribute is an int.

			>>> pypak.anything.anything().__id__ is not None
			True
			>>>
			>>> isinstance(pypak.anything.anything().__id__, int)
			True
			>>>

			Testcase 2: Anything can get any data

			>>> pypak.anything.anything().data is not None
			True
			>>>
			>>> isinstance(pypak.anything.anything().data, dict)
			True
			>>>
			>>> pypak.anything.anything().__data__ is not None
			True
			>>>
			>>> isinstance(pypak.anything.anything().__data__, dict)
			True
			>>>

		"""
		if str(name) == str("""__data__""") or str(name) == str("""data"""):
			return super(anything, self).__getattribute__("""__data__""")
		elif str(name) == str("""__id__""") or str(name) == str("""id"""):
			return super(anything, self).__getattribute__("""__id__""")
		elif str(name) == str("""__dict__"""):
			return self.__getattribute__("""__data__""")
		elif str(name) == str("""__real_data__"""):
			return super(nothing, self).__getattribute__("""__real_data__""")
		else:
			return super(anything, self).__getattribute__(name)

	def __setattr__(self, name, value):
		"""
			Overloads object.__setattr__(self, name, value) to support __id__

			:Param self: - An Anything instance.
			:Param name: - The name of an attribute or the key of a Key Value Pair (kvp).
			:Param value: - The value of the named data.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Instances of Anything should be able to contain instance data

			>>> any_thing_fixture = pypak.anything.anything()
			>>> any_thing_fixture.junk = "5"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> any_thing_fixture.__id__ is not None
			True
			>>> any_thing_fixture.__junk__ = "6"
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> print(any_thing_fixture.__junk__)
			6
			>>> any_thing_fixture.__id__ = 123456789
			>>>
			>>> any_thing_fixture.__id__ is not None
			True
			>>> del any_thing_fixture.__junk__
			>>> del any_thing_fixture
			>>>

			Testcase 2: Instances of Anything should be able to set id

			>>> any_thing_fixture = pypak.anything.anything()
			>>> any_thing_fixture.junk = "1"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'1\'...}
			>>> any_thing_fixture.__id__ is not None
			True
			>>> any_thing_fixture.__junk__ = "2"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'1\'...}
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'1\'...}
			>>> print(any_thing_fixture.__junk__)
			2
			>>> any_thing_fixture.junk = "3"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'3\'...}
			>>> any_thing_fixture.__id__ = 123456789
			>>>
			>>> any_thing_fixture.__id__ is not None
			True
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'3\'...}
			>>> any_thing_fixture.__id__ = 98765421.0 #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			ValueError:...integer...
			>>>
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'3\'...}
			>>> del any_thing_fixture.__junk__
			>>> del any_thing_fixture
			>>>

			Testcase 3: Instances of Anything should be able to contain instance data literally

			>>> src_fixture = pypak.anything.anything()
			>>> dst_fixture = pypak.anything.anything()
			>>> src_fixture.junk = "it works"
			>>> src_fixture.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>> dst_fixture.__data__ #doctest: +ELLIPSIS
			{}
			>>> dst_fixture.__dict__ = src_fixture.__dict__.copy()
			>>> dst_fixture.__data__ #doctest: +ELLIPSIS
			{...it works...}
			>>> del src_fixture
			>>> del dst_fixture
			>>>

		"""
		if str(name) == str("""__id__""") or str(name) == str("""id"""):
			if (value is None) or isinstance(value, int):
				super(nothing, self).__setattr__("""__real_id__""", value)
			else:
				raise ValueError("""'__id__' must be an integer!""")
		elif str(name) == str("""__data__""") or str(name) == str("""data"""):
			super(anything, self).__setattr__("""__data__""", value)
		elif str(name) == str("""__dict__"""):
			self.__setattr__("""__data__""", value)
		elif str("__real_data__") not in str(name) and str(name) in sorted(self.__data__.keys()):
			__old_data = self.__getattribute__("""__data__""")
			__old_data.__setitem__(name, value)
			self.__setattr__("""__data__""", __old_data)
		elif str("__real_data__") not in str(name) and str(name) in sorted(self.__dict__.keys()):
			super(anything, self).__setattr__(name, value)
		elif str("__") not in str(name):
			__old_data = self.__getattribute__("""__data__""")
			__old_data.__setitem__(name, value)
			self.__setattr__("""__data__""", __old_data)
		else:
			super(nothing, self).__setattr__(name, value)

	def __delattr__(self, name):
		"""
			Overloads object.__delattr__(self, name) to support __id__

			:Param self: - An Anything instance.
			:Param name: - The name of an attribute or the key of a Key Value Pair (kvp).

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Instances of Anything should be able to delete contained instance data

			>>> any_thing_fixture = pypak.anything.anything()
			>>> any_thing_fixture.junk = "5"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> any_thing_fixture.__junk__ = "6"
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> print(any_thing_fixture.__junk__)
			6
			>>> any_thing_fixture.__id__ is not None
			True
			>>> del any_thing_fixture.__junk__
			>>> del any_thing_fixture.junk
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{}
			>>> del any_thing_fixture.__id__
			>>> any_thing_fixture.__id__ is not None
			True
			>>>
			>>> del any_thing_fixture.__data__
			>>> any_thing_fixture.__data__ is not None
			True
			>>>

			Testcase 1: Instances of Anything should be able to delete contained instance data

			>>> any_thing_fixture = pypak.anything.anything()
			>>> any_thing_fixture.junk = "5"
			>>> print(any_thing_fixture.__data__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> any_thing_fixture.__junk__ = "5"
			>>> print(any_thing_fixture.__dict__) #doctest: +ELLIPSIS
			{...\'junk\': \'5\'...}
			>>> any_thing_fixture.__id__ = 123456789
			>>>
			>>> any_thing_fixture.__id__ is not None
			True
			>>> del any_thing_fixture.__junk__
			>>> del any_thing_fixture.junk
			>>> any_thing_fixture.__id__ is not None
			True
			>>> del any_thing_fixture.__id__
			>>> del any_thing_fixture.__id__
			>>> any_thing_fixture.__id__ is not None
			True
			>>> del any_thing_fixture._bad_key_ #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...[CWE-476]...
			>>> del any_thing_fixture.__name__ #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...[CWE-476]...
			>>> del any_thing_fixture
			>>>

			"""
		if str(name) == str("""__id__""") or str(name) == str("""id"""):
			pass
		elif str(name) == str("""__data__""") or str(name) == str("""data"""):
			super(anything, self).__delattr__("""__data__""")
		elif str(name) == str("""__dict__"""):
			self.__delattr__("""__data__""")
		elif str("__real_data__") not in str(name) and str(name) in sorted(self.__data__.keys()):
			super(anything, self).__data__.__delitem__(name)
		elif str(name) in sorted(self.__dict__.keys()):
			super(anything, self).__delattr__(name)
		elif str("__") not in str(name):
			__PIAP_CWE_476_MSG__ = str(
				"""[CWE-476] Data key is not valid (posible CWE-825)"""
			).format(nm=name)
			raise AttributeError(__PIAP_CWE_476_MSG__)
		else:
			super(nothing, self).__delattr__(name)

	def __index__(self):
		"""
			Overloads __builtin__.object.__index__(self).
			:Returns __index__: - the index of this instance.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be indexable.
				A: Test that the __index__ result is initialized.
				B: Test that the __index__ result is an int.
				C: Test that the __index__ result is not fixed by default.

			>>> fixture_a = pypak.anything.anything()
			>>> fixture_b = pypak.anything.anything()
			>>> fixture_b._change_ = True
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>> fixture_a.__index__() is not None
			True
			>>> fixture_b.__index__() is not None
			True
			>>> isinstance(fixture_a.__index__(), int)
			True
			>>> isinstance(fixture_b.__index__(), int)
			True
			>>> fixture_a.__index__() is not fixture_b.__index__()
			True
			>>> fixture_b.__index__() is not fixture_a.__index__()
			True
			>>> fixture_c = (fixture_a.__index__() > fixture_b.__index__())
			>>> fixture_d = (fixture_b.__index__() > fixture_a.__index__())
			>>> fixture_e = (fixture_b.__index__() == fixture_a.__index__())
			>>> fixture_c or fixture_d or fixture_e
			True
			>>> fixture_c and fixture_d and fixture_e
			False
			>>>

		"""
		return self.__getattribute__("""id""")

	def __hash__(self):
		"""
			Overloads __builtin__.object.__hash__(self) to support hashing.
			:Returns __hash__: - the hash of this instance.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be indexable.
			A: Test that the __hash__ result is initialized.
			B: Test that the __hash__ result is an int or long.
			C: Test that the __hash__ result is not fixed by default.

			>>> fixture_a = pypak.anything.anything()
			>>> fixture_b = pypak.anything.anything()
			>>> fixture_b._change_ = True
			>>> print(fixture_b.__data__) #doctest: +ELLIPSIS
			{...\'_change_\': ...}
			>>> print(fixture_a.__data__) #doctest: +ELLIPSIS
			{}
			>>> print(fixture_b.__dict__) #doctest: +ELLIPSIS
			{...\'_change_\': ...}
			>>> print(fixture_a.__dict__) #doctest: +ELLIPSIS
			{...}
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>> hash(fixture_a) is not None
			True
			>>> hash(fixture_b) is not None
			True
			>>> isinstance(hash(fixture_a), int) or isinstance(hash(fixture_a), long)
			True
			>>> isinstance(hash(fixture_b), int) or isinstance(hash(fixture_b), long)
			True
			>>> hash(fixture_a) is not hash(fixture_b)
			True
			>>> hash(fixture_b) is not hash(fixture_a)
			True
			>>> fixture_c = (hash(fixture_b) > hash(fixture_a))
			>>> fixture_d = (hash(fixture_a) > hash(fixture_b))
			>>> fixture_e = (hash(fixture_b) == hash(fixture_a))
			>>> fixture_c or fixture_d or fixture_e
			True
			>>> fixture_c and fixture_d and fixture_e
			False
			>>>

		"""
		return super(anything, self).__getattribute__("""__id__""")

	def __del__(self):
		"""
			Overloads __builtin__.object.__del__(self) to releases the id when deleted.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should maintain an id until GCed (even if not static nor unique).
				A: Test creating anything
				B: Test that instance is fixed until changed (identity test)
				C: Repeat A & B with another instance
				D: Ensure they are different instances
				E: Delete the instances (should be error free)

			>>> test_obj = pypak.anything.anything()
			>>> test_obj.__id__ == test_obj.__id__
			True
			>>> other_obj = pypak.anything.anything()
			>>> other_obj.__id__ == other_obj.__id__
			True
			>>> other_obj._change_ = "different"
			>>> print(other_obj.__data__) #doctest: +ELLIPSIS
			{...\'_change_\': ...}
			>>> other_obj.__id__ == other_obj.__id__
			True
			>>> print(test_obj.__data__)
			{}
			>>> test_obj is not None
			True
			>>> other_obj is not None
			True
			>>> test_obj.__id__ is not None
			True
			>>> other_obj.__id__ is not None
			True
			>>> other_obj._change_ is not None
			True
			>>> test_obj.__id__ != other_obj.__id__
			True
			>>> test_obj.__id__ == test_obj.__id__ and test_obj.__id__ != other_obj.__id__
			True
			>>> del test_obj
			>>> del other_obj
			>>>

			Testcase 1: Anything should maintain an id until GCed (even if not static nor unique).
				A: Test creating anything
				B: Test that instance is fixed until changed (identity test)
				C: Change that instance
				D: Delete the instances (should be error free)

			>>> test_obj = pypak.anything.anything()
			>>> test_obj.__id__ == test_obj.__id__
			True
			>>> test_obj is not None
			True
			>>> test_obj.datablob = str("Some Test Data")
			>>> test_obj.__id__ == test_obj.__id__
			True
			>>> del test_obj
			>>>

		"""
		super(anything, self).__delattr__("""__id__""") # force free the id

	def __dir__(self):
		"""
			Overloads __builtin__.object.__dir__(self)
			:Returns list: - the list of atributes

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: dir(anything) is error free

			>>> dir(pypak.anything.anything()) is not None
			True
			>>>

			Testcase 2: dir(anything) is not empty

			>>> len(dir(pypak.anything.anything())) > 3
			True
			>>>

			Testcase 3: dir(anything) has data and id

			>>> test_dir_fixture  = pypak.anything.anything()
			>>> len(dir(test_dir_fixture)) > 3
			True
			>>> str("__data__") in dir(test_dir_fixture)
			True
			>>> str("__id__") in dir(test_dir_fixture)
			True
			>>>

		"""
		return sorted(["""__dict__""", """__data__""", """__id__"""] + dir(super(self.__class__, self)))

	def __getstate__(self):
		"""
			Overloads __builtin__.object.__getstate__(self)
			Special thanks to the optimizations on https://stackoverflow.com/questions/31433989/
			:Returns dict: - the data of the instance.

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be able to unpickle.
				A: Test that state is real (not in the matrix)

			>>> fixture_a = pypak.anything.anything()
			>>> fixture_a._change_ = True
			>>> fixture_a.__getstate__() is not None
			True
			>>> fixture_a.__getstate__() is not None
			True
			>>>

			Testcase 2: Anything should be able to pickle.
				A: Test that input becomes output

			>>> fixture_a = pypak.anything.anything()
			>>> fixture_b = pypak.anything.anything()
			>>> fixture_a._change_ = True
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>> fixture_a.__class__ is fixture_b.__class__
			True
			>>> fixture_b.__class__ is fixture_a.__class__
			True
			>>> fixture_a._change_ is not None
			True
			>>> fixture_b._change_ is not None #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...
			>>> import pickle
			>>> jar = open('/tmp/test_data.pkl', 'wb')
			>>> pickle.dump(fixture_a, jar)
			>>> jar.close()
			>>> pkl_file = open('/tmp/test_data.pkl', 'rb') # connect to the pickled data
			>>> fixture_b = pickle.load(pkl_file) # load it into a variable
			>>> print(fixture_b) #doctest: +ELLIPSIS
			<anything with id ... and data={...}>
			>>> pkl_file.close()
			>>> fixture_b._change_
			True
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>>

		"""
		__volatile_keys__ = ["""__real_data__""", """__data__""", """__id__"""]
		return dict({k: v for k, v in self.__data__.items() if k not in __volatile_keys__})

	def __setstate__(self, state):
		"""
			Overloads __builtin__.object.__setstate__(self, state)

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: Anything should be able to unpickle.
				A: Test that input becomes output

			>>> fixture_a = pypak.anything.anything()
			>>> fixture_b = pypak.anything.anything()
			>>> fixture_a._change_ = True
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>> fixture_a._change_ is not None
			True
			>>> type(fixture_a) == type(fixture_b)
			True
			>>> type(fixture_a.__class__) == type(fixture_b.__class__)
			True
			>>> fixture_b._change_ is not None #doctest: +ELLIPSIS, +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			...
			AttributeError:...
			>>> import pickle
			>>> jar = open('/tmp/test_data.pkl', 'wb')
			>>> pickle.dump(fixture_a, jar)
			>>> jar.close()
			>>> pkl_file = open('/tmp/test_data.pkl', 'rb') # connect to the pickled data
			>>> fixture_b = pickle.load(pkl_file) # load it into a variable
			>>> print(fixture_b) #doctest: +ELLIPSIS
			<anything with id ... and data={...}>
			>>> pkl_file.close()
			>>> fixture_b._change_
			True
			>>> fixture_a is not fixture_b
			True
			>>> fixture_b is not fixture_a
			True
			>>>

		"""
		__skip_keys__ = ["""__real_data__""", """__data__""", """__id__"""]
		super(anything, self).__setattr__(
			"""__data__""",
			dict(
				{k: v for k, v in state.items() if k not in __skip_keys__}
			)
		)
		self.__id__ = id((super(self.__class__, self).__class__, (state)))

	def __str__(self):
		"""
			Overloads __builtin__.object.__str__(self)

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: anything is printable.

			>>> str(pypak.anything.anything()) is not None
			True
			>>> print(str(pypak.anything.anything())) #doctest: +ELLIPSIS
			<anything with id ... and data={}>
			>>>

		"""
		return str("""{open}{name} with id {idnum} and data={thedata}{close}""").format(
			name=str(self.__class__.__name__),
			idnum=str(self.id),
			thedata=repr(self.__getstate__()),
			open="""<""",
			close=""">"""
		)

	def __repr__(self):
		"""Overloads __builtin__.object.__rpr__(self)

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: anything is representable as text.

			>>> repr(pypak.anything.anything()) is not None
			True
			>>> repr(pypak.anything.anything()) #doctest: +ELLIPSIS
			\'{\"class\": pypak.anything.anything, \"id\": ..., \"data\": dict({})}\'
			>>>

		"""
		return str("""{open}"class": {name}, "id": {idnum}, "data": dict({data}){close}""").format(
			name=str("""{mod}.{cls}""").format(
				mod=str(self.__class__.__module__), cls=str(self.__class__.__name__)
			),
			idnum=str(self.id),
			data=repr(self.data),
			open="""{""",
			close="""}"""
		)

	def __bytes__(self):
		"""
			Wrapper function for anything.__bytes__(self)

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: cross-python bytes compatable.

			>>> pypak.anything.anything().__bytes__() is not None
			True
			>>> print(str(pypak.anything.anything().__bytes__().decode('utf_8'))) #doctest: +ELLIPSIS
			{...}
			>>>

			Testcase 2: data in bytes.

			>>> test_fixture = pypak.anything.anything()
			>>> test_fixture is not None
			True
			>>> test_fixture.__bytes__() is not None
			True
			>>> test_fixture.somedata = str("This is data")
			>>> test_fixture.gooddata = str("abcdefghijklmnopqrstuvwxyz")
			>>> test_fixture.moredata = [int(x) for x in range(0, 127)]
			>>> test_fixture.baddata = range(128, 256)
			>>> print(str(test_fixture.__bytes__().decode('utf_8'))) #doctest: +ELLIPSIS
			{...}
			>>>

		"""
		return repr(self.__getstate__()).encode('utf_8', 'backslashreplace')

	def __unicode__(self):
		"""
			Wrapper function for anything.__str__(self)

			Testing:

			First setup test fixtures by importing anything.

			>>> import pypak.anything
			>>>

			Testcase 1: cross-python string compatable.

			>>> pypak.anything.anything().__unicode__() is not None
			True
			>>> print(pypak.anything.anything().__unicode__()) #doctest: +ELLIPSIS
			<anything with id ... and data={}>
			>>>

		"""
		return self.__str__()
