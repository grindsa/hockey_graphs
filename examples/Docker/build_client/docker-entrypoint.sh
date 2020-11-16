#!/bin/bash
# entrypoint script to build a new bundle and push it to production
cd /tmp/ui
npm install
npm install --only=dev
npm run compile

# sync data to prod
cd /tmp
rsync -avze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' ./rest hockeygraphs@hockeygraphs.dynamop.de:~
rsync -avze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' ./ui/dist hockeygraphs@hockeygraphs.dynamop.de:ui

# apply schema migrations
ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de 'python3 manage.py makemigrations && python3 manage.py migrate'

# restart prod
ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de sudo '/etc/init.d/apache2 restart'

exec "$@"
