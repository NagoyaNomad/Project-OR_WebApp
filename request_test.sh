#!/usr/bin/env zsh

curl -X POST \
-F students=@resource/students.csv \
-F cars=@resource/cars.csv \
-o resource/solution.csv \
http://127.0.0.1:5000/api
