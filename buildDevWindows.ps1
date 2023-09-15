python -m pip install --upgrade pip
pip install --upgrade build
pip install --upgrade twine
Remove-Item "dist" -Recurse
python -m build
twine upload dist/*