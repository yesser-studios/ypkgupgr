[![PyPI release](https://img.shields.io/pypi/v/ypkgupgr)](https://pypi.org/project/ypkgupgr/)
[![License](https://img.shields.io/github/license/Yesser-Studios/ypkgupgr)](https://github.com/Yesser-Studios/ypkgupgr/blob/master/LICENSE.md)
[![Downloads](https://static.pepy.tech/personalized-badge/ypkgupgr?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/ypkgupgr)
![GitHub issues](https://img.shields.io/github/issues/Yesser-Studios/ypkgupgr)  
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Build status](https://github.com/Yesser-Studios/ypkgupgr/actions/workflows/python-publish.yml/badge.svg)

# ypkgupgr
## The pip package updater by yesseruser

```
pip install ypkgupgr
```

This is a package updater that updates all outdated packages when run.  

This package works with Python 3.9+.

To install, follow the steps listed here:  
[Installation](https://github.com/yesseruser/ypkgupgr/wiki/Installation)

Here's the wiki page:  
[Wiki](https://github.com/yesseruser/ypkgupgr/wiki)

If you're running the package from a python file, please **use a subprocess** instead of importing and calling the `update_packages` function. This is because the package can update itself and can result in an error because of the code changing.
