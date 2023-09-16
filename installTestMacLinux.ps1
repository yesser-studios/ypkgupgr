python3 -m pip install --upgrade pip
pip3 install --upgrade build
Remove-Item "dist" -Recurse
python3 -m build
pip3 install --force-reinstall ./dist/*.whl