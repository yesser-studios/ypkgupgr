python -m pip install --upgrade pip
pip install --upgrade build
Remove-Item "dist" -Recurse
python -m build
pip install --force-reinstall ./dist/*.whl