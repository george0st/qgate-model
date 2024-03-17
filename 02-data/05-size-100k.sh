#!/bin/sh

# size 10k with 2k bundles
python main.py generate -l 2-size-10K -c 10000 -b 2000

# or
# size 10k with smaller 1k bundles
# python main.py generate -l 2-size-10K -c 10000 -b 1000