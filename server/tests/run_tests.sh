#!/bin/bash

. ../env/bin/activate
python -m twisted.trial -j 3 test_server
python -m unittest test_game -v
