#!/bin/bash

. ../env/bin/activate
python -m twisted.trial test_server
