rmdir "dist" -Recurse
python -m build
twine upload dist/*