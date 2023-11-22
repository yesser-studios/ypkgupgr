python -m pip install --upgrade pip
pip install --upgrade build
rm -r dist
python -m build
python -m pip install --force-reinstall --no-index --find-links=.\dist yesserpackageupdater