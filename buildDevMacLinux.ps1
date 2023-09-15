python3 -m pip install --upgrade pip
pip3 install --upgrade build
Remove-Item "dist" -Recurse
python3 -m build
python3 -m twine upload dist/*