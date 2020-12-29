#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

echo $SCRIPTPATH

$SCRIPTPATH/v/bin/python -u $SCRIPTPATH/parental_controls.py $SCRIPTPATH/env.json