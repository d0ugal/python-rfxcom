#! /usr/bin/env bash
set -xe

if [ $TOX_ENV == "coverage" ]
then
  pip install coveralls
  tox
  coveralls
else
  tox -e $TOX_ENV
fi
