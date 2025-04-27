#!/usr/bin/env bash

sudo pkill chrome
google-chrome --remote-debugging-port=15001 \
  --disable-dev-shm-usage \
  --no-first-run \
  --no-default-browser-check \
  --disable-infobars \
  --window-position=0,0 \
  --disable-session-crashed-bubble \
  --hide-crash-restore-bubble