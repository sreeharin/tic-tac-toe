#!/bin/bash

python -m twisted.trial -j 3 test_server
python -m unittest test_game -v
