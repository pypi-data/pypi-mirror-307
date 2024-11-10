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

__all__ = [
	"""__package__""", """__module__""", """__name__""", """__version__""", """__prolog__""",
	"""__doc__""", """anything""", """__super_import__"""
]


__package__ = """pypak"""


__module__ = """pypak"""


__name__ = """pypak"""


global __version__


__version__ = """1.0.0"""


__prolog__ = str("""pypak library version {version}.""").format(version=__version__)


__doc__ = __prolog__ + """

	Minimal Acceptance Testing:

	First setup test fixtures by importing anything.

		>>> import pypak
		>>>

		>>> pypak.__doc__ is not None
		True
		>>>

		>>> pypak.__version__ is not None
		True
		>>>

		Testcase 0: Docs should have a prolog.

		>>> pypak.__prolog__ is not None
		True
		>>> pypak.__prolog__ in pypak.__doc__
		True
		>>>

		Testcase 1: pypak.anything should have a doctests.

		>>> pypak.anything.__module__ is not None
		True
		>>>

		Testcase 2: Anything should be.

		>>> type(pypak.anything.anything) is not None
		True
		>>>

		Testcase 3: Anything should be.

		>>> pypak.anything.anything() is not None
		True
		>>>

	"""


try:
	import sys
	if sys.__name__ is None:
		raise ImportError("OMG! we could not import os. We're like in the matrix! ABORT. ABORT.")
except Exception as err:
	raise ImportError(err)


def __super_import__(module_named_x):
	"""
		A wrapper for importing that allows reuse. WARNING: Only intended for pypak internals.

		pypak should still be imported the normal way:

		:Param module_named_x: - the name of the module
		:Returns module: the module

		>>> import pypak
		>>>

		Usage:

		>>> pypak.__super_import__(\"os\") #doctest: +ELLIPSIS
		<module \'os\' ...>
		>>>

	"""
	_panic_fixture = ImportError()
	_panic_fixture.args = ("""[CWE-758]""", """[PEP-366]""")
	_panic_fixture.message = str("{globtxt} Failed to import.").format(globtxt=str(module_named_x))
	try:
		module_obj = None
		if str(module_named_x) not in sys.modules:
			module_obj = __import__(module_named_x)
			sys.modules[module_named_x] = module_obj
		else:  # pragma: no branch
			module_obj = sys.modules[module_named_x]
		globals()[module_named_x] = module_obj
		return module_obj
	except Exception:
		raise _panic_fixture
	raise _panic_fixture


os = __super_import__("""os""")


os.path = __super_import__("""os.path""")


try:
	_DIR_NAME = str(".")
	_PARENT_DIR_NAME = str("..")
	_BASE_NAME = os.path.dirname(__file__)
	try:
		if str("pypak") in __file__:
			search_list = [
				os.path.abspath(os.path.join(_BASE_NAME, _PARENT_DIR_NAME)),
				os.path.abspath(os.path.join(_BASE_NAME, _DIR_NAME))
			]
			for __sys_path__ in search_list:
				if __sys_path__ not in sys.path:
					sys.path.insert(0, __sys_path__)
	except Exception:
		raise ImportError("pypak failed to import.")
except Exception as ImportErr:
	print(str(type(ImportErr)))
	print(str(ImportErr))
	print(str((ImportErr.args)))
	ImportErr = None
	del ImportErr
	raise ImportError(str("pypak Failed to Import"))


try:
	if """pypak.anything""" not in sys.modules:
		from . import anything as anything
	else:  # pragma: no branch
		anything = sys.modules["""pypak.anything"""]
except Exception as importErr:
	del importErr
	import pypak.anything as anything


if __name__ in "__main__":
	raise ImportError(str("Failed to become an entrypoint instead of a Library. No Magic here."))
	exit(255)  # nocov

