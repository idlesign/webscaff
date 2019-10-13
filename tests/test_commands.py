

class TestProj:

    def test_bootstrap(self, run_command_mock, monkeypatch):
        monkeypatch.setattr('webscaff.commands.utils.rsync_patchwork', lambda *args, **kwargs: None)

        assert run_command_mock('run.initialize') == [
            'whoami',
            'id -u mydemo',
            'useradd -s /bin/bash mydemo',
            'adduser tstout mydemo',
            'apt-get update',
            'apt install -y python3-dev python3-pip python3-venv python3-wheel '
            'build-essential libjpeg-dev libxml2-dev libxslt1-dev libpcre3-dev libssl-dev '
            'git postgresql libpq-dev certbot acl mc htop net-tools ncdu',
            'mkdir -p /srv/mydemo',
            'chown -R mydemo:mydemo /srv/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /srv/mydemo',
            'mkdir -p /var/lib/mydemo',
            'chown -R mydemo:mydemo /var/lib/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo',
            'mkdir -p /var/lib/mydemo/dumps',
            'chown -R mydemo:mydemo /var/lib/mydemo/dumps',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo/dumps',
            'mkdir -p /var/lib/mydemo/static',
            'chown -R mydemo:mydemo /var/lib/mydemo/static',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo/static',
            'mkdir -p /var/lib/mydemo/media',
            'chown -R mydemo:mydemo /var/lib/mydemo/media',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo/media',
            'rm -rf /var/cache/mydemo*',
            'mkdir -p /var/cache/mydemo',
            'chown -R mydemo:mydemo /var/cache/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/cache/mydemo',
            'test -e "$(echo /var/lib/mydemo/environ)"',
            'test -e "$(echo /var/lib/mydemo/environ)"',
            'egrep "^production$" "/var/lib/mydemo/environ"',
            'mkdir -p ~/mydemo',
            'ln -sf /srv/mydemo ~/mydemo/code',
            'ln -sf /var/lib/mydemo ~/mydemo/state',
            'ln -sf /var/cache/mydemo ~/mydemo/cache',
            'test -e "$(echo /srv/mydemo/.git)"',
            'test -e "$(echo /srv/mydemo/venv)"',
            'cd /srv/mydemo/mydemo',
            'pip3 install -e .',
            'pip3 install  wheel',
            'pip3 install  -r requirements.txt',
            'ln -sf /srv/mydemo/venv/bin/mydemo /usr/bin/mydemo',
            'pg_config --version',
            'createdb mydemo',
            'createuser mydemo',
            'psql -c "GRANT ALL PRIVILEGES ON DATABASE mydemo TO mydemo"',
            'service postgresql restart',
            'mkdir -p /var/lib/mydemo/static',
            'chown -R mydemo:mydemo /var/lib/mydemo/static',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo/static',
            'mkdir -p /var/lib/mydemo/media',
            'chown -R mydemo:mydemo /var/lib/mydemo/media',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /var/lib/mydemo/media',
            'ln -sf /srv/mydemo/conf/django.py '
            '/srv/mydemo/mydemo/mydemo/settings/settings_production.py',
            'mydemo migrate',
            'mydemo createsuperuser --email idlesign@some.com --username idlesign',
            'touch /var/lib/mydemo/reloader',
            'mkdir -p /var/lib/mydemo/spool',
            'systemctl enable /srv/mydemo/conf/mydemo.service',
            'systemctl start mydemo',
            'mkdir -p /var/lib/mydemo/certbot',
            'certbot --agree-tos --no-eff-email --email idlesign@some.com certonly '
            '--webroot -d mydemo.here -w /var/lib/mydemo/certbot',
            'shutdown -r now',
        ]


class TestSys:

    def test_info(self, run_command_mock):

        assert run_command_mock('info') == [
            'uname -a', 'cat /etc/timezone', 'uptime', 'df -h']

    def test_reboot(self, run_command_mock):

        assert run_command_mock('reboot') == ['shutdown -r now']
