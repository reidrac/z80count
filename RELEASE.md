How to make a release
=====================

1. Bump the version in `z80count/z80count.py` and commit the change.
2. Tag that commit with the same version number.
3. Push the commit and the tags (with --tags).
4. Build dist files:
```
rm -f dist/*
python setup.py sdist bdist_wheel
python3 setup.py sdist bdist_wheel
```
5. Publish on PyPi:
```
twine upload dist/*
```

The release can be checked at: https://pypi.org/project/z80count/

Version numbers
---------------

Read: https://semver.org/

