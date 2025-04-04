#!/bin/bash

python_version=$1

pixi run \
--manifest-path pixi.toml \
--locked --environment py${python_version} \
mypy
