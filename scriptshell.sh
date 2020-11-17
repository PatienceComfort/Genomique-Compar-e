#!/bin/bash

liste=ls *.bl
for i in ${liste[*]};
do
  python3 parsefin.py ${i} ${i}_besthit
done
