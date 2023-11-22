python -m pip install --upgrade pip
pip install --upgrade build
Remove-Item "dist" -Recurse
python -m build
python -m pip install --force-reinstall --no-index --find-links=.\dist yesserpackageupdater