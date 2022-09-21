#!/bin/bash

conan install ..
cmake ..
make -j 8
