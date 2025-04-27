#!/usr/bin/env bash

sudo pkill chrome

google-chrome --remote-debugging-port=15001 \
  --disable-dev-shm-usage \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --window-position=0,0 \
  --disable-session-crashed-bubble \
  --hide-crash-restore-bubble \
  --profile-directory=mychrome1 \
  --no-sandbox \
  --disable-webgl \
  --disable-webgl2 \
  --disable-gpu \
  --disable-gpu-compositing \
  --disable-gpu-driver-error-check \
  --disable-blink-features=AutomationControlled \
  --disable-automation \
  --disable-features=site-per-process