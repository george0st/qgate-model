#!/bin/sh

# size 100k with 2k bundles
python main.py generate -l 2-size-100K -c 100000 -b 2000

# or
# size 100k with smaller 3k bundles
# python main.py generate -l 2-size-100K -c 100000 -b 3000