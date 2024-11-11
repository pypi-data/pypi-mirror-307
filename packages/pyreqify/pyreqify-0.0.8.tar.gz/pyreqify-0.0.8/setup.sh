pip install -e .
python -m build
twine upload --verbose -r testpypi dist/*