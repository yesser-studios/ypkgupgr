python3 -m pip install --upgrade pip
pip3 install --upgrade build
rm -r ./dist
python3 -m build
python3 -m pip install --force-reinstall --find-links=./dist ypkgupgr