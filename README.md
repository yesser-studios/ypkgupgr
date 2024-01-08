[![PyPI release](https://img.shields.io/pypi/v/ypkgupgr)](https://pypi.org/project/ypkgupgr/)
[![GitHub Issues](https://img.shields.io/github/issues/Yesser-Studios/ypkgupgr
)](https://github.com/Yesser-Studios/ypkgupgr/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Yesser-Studios/ypkgupgr)](https://github.com/Yesser-Studios/ypkgupgr/pulls)
[![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Yesser-Studios/ypkgupgr?color=%23e132e1)](https://github.com/Yesser-Studios/ypkgupgr/pulls?q=is%3Apr+is%3Aclosed)
[![GitHub License](https://img.shields.io/github/license/Yesser-Studios/ypkgupgr)](https://github.com/Yesser-Studios/ypkgupgr/blob/main/LICENSE.txt)
[![CodeFactor](https://www.codefactor.io/repository/github/yesser-studios/yesser-engine/badge)](https://www.codefactor.io/repository/github/yesser-studios/ypkgupgr)
![GitHub repo size](https://img.shields.io/github/repo-size/Yesser-Studios/ypkgupgr)
![GitHub Repo stars](https://img.shields.io/github/stars/Yesser-Studios/ypkgupgr?style=flat&color=%23baad00)
[![GitHub Repo forks](https://img.shields.io/github/forks/Yesser-Studios/ypkgupgr?style=flat)](https://github.com/Yesser-Studios/ypkgupgr/fork)
[![Downloads](https://static.pepy.tech/personalized-badge/ypkgupgr?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/ypkgupgr)    

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
