#! /bin/sh
chown -R mydemo:mydemo /etc/letsencrypt/archive/mydemo.here/.*
mydemo uwsgi_reload
