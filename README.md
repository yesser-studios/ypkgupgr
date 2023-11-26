# yesserpackageupdater
## The pip package updater by yesseruser

This is a package updater that updates all outdated packages when run.  

To install, follow the steps listed here:  
[Installation](https://github.com/yesseruser/YesserPackageUpdater/wiki/Installation)

Here's the wiki page:  
[Wiki](https://github.com/yesseruser/YesserPackageUpdater/wiki)

~This package only works on Windows.~  
This package works on any operating system since update 1.1.5

If you're running the package from a python file, please **use a subprocess** instead of importing and calling the `update_packages` function. This is because the package can update itself and it can result in an error because of the code changing.
