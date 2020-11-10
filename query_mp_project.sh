#!/bin/bash

if [ "$1" == "-h" -o "$1" == "--help" -o "$1" == "" ]; then
    echo "Usage: $0 <include one of> -- <must include>"
    exit 0
fi

if [ ! -e MP_API_KEY ]; then
    echo "=========================================================="
    echo "You need to obtain a materials project API key!"
    echo "Go to https://materialsproject.org"
    echo "Click on 'Login' to login/create an account."
    echo "Then go to Dashboard and 'Generate API Key'."
    echo "Grab the character string an place it in a file MP_API_KEY"
    echo "=========================================================="
    exit 1
fi

IN=""
while [ -n "$1" ]; do
    if [ "$1" == "--" ]; then
        shift 1
        break
    fi
    if [ -z "$IN" ]; then
        IN="\"$1\""
    else
        IN="$IN,\"$1\""
    fi
    shift 1
done

ALL=""
while [ -n "$1" ]; do
    if [ -z "$ALL" ]; then
        ALL="\"$1\""
    else
        ALL="$ALL,\"$1\""
    fi
    shift 1
done

MP_API_KEY=$(cat MP_API_KEY)

#curl https://www.materialsproject.org/rest/v2/materials/mp-1234/vasp?API_KEY=$MP_API_KEY

CRITERIA='{"elements": {"$in": ['$IN'], "$all": ['$ALL']}, "nelements":1}'
PROPERTIES='["material_id", "pretty_formula", "elements", "nelements", "energy", "energy_per_atom", "density", "volume", "nsites", "band_gap", "total_magnetization", "elasticity", "piezo", "diel", "copyright", "cif"]'

curl -s --header "X-API-KEY: $MP_API_KEY" "https://www.materialsproject.org/rest/v2/query" -F "criteria=$CRITERIA" -F "properties=$PROPERTIES"


