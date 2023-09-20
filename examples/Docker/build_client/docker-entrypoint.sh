#!/bin/bash
# entrypoint script to build a new bundle and push it to production
P1=$1

cd /tmp/ui
npm install
#
# npm install --only=dev
npm install webpack
npm run compile


if [ $1 = "deploy" ]; then
    echo "deploy"
    # sync data to prod
    cd /tmp
    rsync -rvze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' --backup ./rest hockeygraphs@hockeygraphs.dynamop.de:~
    rsync -rvze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' --backup ./locale hockeygraphs@hockeygraphs.dynamop.de:~
    rsync -rvze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' --backup ./ui/dist hockeygraphs@hockeygraphs.dynamop.de:ui
    rsync -rvze 'ssh -i id_ed25519 -o "StrictHostKeyChecking=no"' --backup ./static/img hockeygraphs@hockeygraphs.dynamop.de:static

    # apply schema migrations
    ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de 'python3 manage.py makemigrations && python3 manage.py migrate'
    # compile locales
    ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de 'python3 manage.py compilemessages'

    # update delwebstat_scraper
    ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de sudo 'pip3 install delstat_scraper --upgrade'

    # restart prod
    ssh -i id_ed25519 hockeygraphs@hockeygraphs.dynamop.de sudo '/etc/init.d/apache2 restart'

else
    echo "no deploy"
fi

exec "$@"
