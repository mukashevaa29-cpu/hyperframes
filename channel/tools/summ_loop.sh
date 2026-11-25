#!/bin/bash
# summarize each video once its frames.npz exists
R=$1; T=$2
while true; do
  left=0
  for v in $R/videos/*.mkv; do
    n=$(basename $v .mkv)
    if [ ! -f $R/analysis/$n/summary.json ]; then
      left=1
      if [ -f $R/analysis/$n/frames.npz ] && [ -f $R/analysis/$n/loudness.txt ] && [ $(( $(date +%s) - $(stat -c %Y $R/analysis/$n/loudness.txt) )) -gt 90 ]; then python3 -I $T/summarize.py $v $R/analysis; fi
    fi
  done
  [ $left = 0 ] && break
  sleep 60
done
echo ALL SUMMARIZED
