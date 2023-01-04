#!/bin/bash

set -e 
set -o pipefail
# example test directories.
#   ...   in ./*/test_*
#   ...   in ./doc/test_*
#   ...   in ./examples/test_*
#   ...   in ./unit/test_*
for entry in ./examples/test_*
do
  # Tests have to run separately bc of the NEURON package linking
  echo "Testing $entry"
  pytest $entry
done
