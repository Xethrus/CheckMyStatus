#!/bin/bash

pyre --search-path $(python -c 'import site; print(site.getsitepackages()[0])')
