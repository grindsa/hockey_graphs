#!/bin/bash

cd /tmp/ui
npm install
npm install --only=dev
npm run compile

exec "$@"