#!/bin/bash

rm -rf __pycache__ build dist urlwait.egg-info
python setup.py sdist bdist_wheel
twine upload -s dist/*
