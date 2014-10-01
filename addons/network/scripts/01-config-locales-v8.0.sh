#!/bin/bash
# file: 01-config-locales-v8.0.sh 

locale-gen fr_FR
dpkg-reconfigure locales
