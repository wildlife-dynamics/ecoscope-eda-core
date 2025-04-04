#!/bin/bash

python_version=$1

command="pixi run \
--manifest-path pixi.toml \
--locked --environment py${python_version} \
pytest src/ecoscope_eda_core/ -vv"

shift 1
if [ -n "$*" ]; then
    extra_args=$*
    command="$command $extra_args"
fi

echo "Running command: $command"
eval $command
