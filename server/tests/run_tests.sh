#!/bin/bash

. ../env/bin/activate
python -m twisted.trial test_server
python -m unittest test_game -v
