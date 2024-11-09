# remah
mixed modeling approaches


## installation
```
$ pip install remah
Collecting remah
  Downloading remah-0.0.4-py3-none-any.whl.metadata (1.2 kB)
Downloading remah-0.0.4-py3-none-any.whl (2.6 kB)
Installing collected packages: remah
Successfully installed remah-0.0.4
```

```
$ pip show remah
Name: remah
Version: 0.0.4
Summary: python package for mixed modeling approaches
Home-page: https://github.com/dudung/remah
Author: Sparisoma Viridi
Author-email: dudung@gmail.com
License: MIT
Location: V:\tf\Lib\site-packages
Requires:
Required-by:
```


## usage
```
$ python
Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from remah import info
>>> print(info.ramah())
Hello, I am remah ramah!
>>> exit()
```


## test
```
$ pip install -e .
Obtaining file:///M:/remah
  Preparing metadata (setup.py) ... done
Installing collected packages: remah
  Running setup.py develop for remah
Successfully installed remah-0.0.5
```

```
pip show remah
Name: remah
Version: 0.0.5
Summary: python package for mixed modeling approaches
Home-page: https://github.com/dudung/remah
Author: Sparisoma Viridi
Author-email: dudung@gmail.com
License: MIT
Location: M:\remah\src
Editable project location: M:\remah\src
Requires:
Required-by:
```

```
$ python -m unittest tests\test_info.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```


## uninstallation
```
$ pip uninstall remah
Found existing installation: remah 0.0.5
Uninstalling remah-0.0.5:
  Would remove:
    v:\tf\lib\site-packages\remah.egg-link
Proceed (Y/n)? Y
  Successfully uninstalled remah-0.0.5
```

```
$ pip show remah
WARNING: Package(s) not found: remah
```

```
$ python
Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import remah
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'remah'
>>> exit()
```


```
python -m unittest tests\test_info.py
E
======================================================================
ERROR: test_info (unittest.loader._FailedTest.test_info)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_info
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\unittest\loader.py", line 137, in loadTestsFromName
    module = __import__(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^
  File "M:\remah\tests\test_info.py", line 8, in <module>
    from remah.info import ramah
ModuleNotFoundError: No module named 'remah'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
```

## releases
Use following steps to create a new release
+ Edit `setup.py`, advance version number, save it.
+ Commit and push the work.
+ Visit [releases page](https://github.com/dudung/remah/releases) of the repository.
+ Draft a new release.
+ Choose a tag, find or create new one.
+ Generate release notes if necessary.
+ Fill release title and describe the release.
+ Set as the latest release.
+ Publish release.

After a few minutes visit the page on PyPi https://pypi.org/project/remah/.
