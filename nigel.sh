#!/bin/sh

if [ ! -d ./exports ]
then
   mkdir ./exports
fi

python ./collector.py &

python ./visualize.py
