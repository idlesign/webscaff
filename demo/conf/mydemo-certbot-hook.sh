#! /bin/sh
chown -R mydemo:mydemo /etc/letsencrypt/archive/mydemo.here/.*
systemctl restart mydemo.service
