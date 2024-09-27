#!/bin/bash

( cd "${PWD/\/docs\/*/}" && wget -O docs/assets/glossary/dictionary.txt https://raw.githubusercontent.com/nesi/nesi-wordlist/main/outputs/dictionary.txt )
