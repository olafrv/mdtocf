# https://packaging.python.org/tutorials/packaging-projects/

python3 -m pip install --upgrade setuptools wheel
python3 -m pip install --upgrade twine

rm -rf ./dist ./build *.egg-info
python3 setup.py sdist bdist_wheel

if [ "$1" == "live" ]
then
    python3 -m twine upload --skip-existing --username __token__ --password "$PY_LIVE_TOKEN" dist/*
else
    python3 -m twine upload --skip-existing --username __token__ --password "$PY_TEST_TOKEN" --repository testpypi dist/*
fi