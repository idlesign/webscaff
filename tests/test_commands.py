

class TestProj:

    def test_bootstrap(self, run_command_mock, monkeypatch):
        monkeypatch.setattr('webscaff.commands.utils.rsync_patchwork', lambda *args, **kwargs: None)

        assert run_command_mock('initialize') == [
            'whoami',
            'id -u mydemo',
            'useradd -s /bin/bash mydemo',
            'adduser tstout mydemo',
            'apt-get update',
            'apt install -y python3-dev python3-pip python3-venv python3-wheel '
            'build-essential libjpeg-dev libxml2-dev libxslt1-dev libpcre3-dev libssl-dev '
            'git postgresql libpq-dev certbot acl mc htop net-tools',
            'mkdir -p /srv/mydemo',
            'chown -R mydemo:mydemo /srv/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /srv/mydemo',
            'ln -sf /srv/mydemo ~/mydemo',
            'test -e "$(echo /srv/mydemo/.git)"',
            'test -e "$(echo /srv/mydemo/venv)"',
            'cd /srv/mydemo/mydemo',
            'pip3 install -e .',
            'pip3 install  wheel',
            'pip3 install  -r requirements.txt',
            'ln -sf /srv/mydemo/venv/bin/mydemo /usr/bin/mydemo',
            'mkdir -p /srv/mydemo/runtime',
            'chown -R mydemo:mydemo /srv/mydemo/runtime',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /srv/mydemo/runtime',
            'test -e "$(echo /srv/mydemo/runtime/environ)"',
            'test -e "$(echo /srv/mydemo/runtime/environ)"',
            'egrep "^production$" "/srv/mydemo/runtime/environ"',
            'pg_config --version',
            'createdb mydemo',
            'createuser mydemo',
            'psql -c "GRANT ALL PRIVILEGES ON DATABASE mydemo TO mydemo"',
            'service postgresql restart',
            'mkdir -p /srv/mydemo/runtime/static',
            'chown -R mydemo:mydemo /srv/mydemo/runtime/static',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /srv/mydemo/runtime/static',
            'mkdir -p /srv/mydemo/runtime/media',
            'chown -R mydemo:mydemo /srv/mydemo/runtime/media',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX" /srv/mydemo/runtime/media',
            'ln -sf /srv/mydemo/conf/django.py '
            '/srv/mydemo/mydemo/mydemo/settings/settings_production.py',
            'mydemo migrate',
            'mydemo createsuperuser --email idlesign@some.com --username idlesign',
            'touch /srv/mydemo/runtime/reloader',
            'mkdir -p /srv/mydemo/runtime/spool',
            'mydemo uwsgi_sysinit > /srv/mydemo/conf/mydemo.service',
            'systemctl enable /srv/mydemo/conf/mydemo.service',
            'systemctl start mydemo',
            'mkdir -p /srv/mydemo/runtime/certbot',
            'certbot --agree-tos --no-eff-email --email idlesign@some.com certonly '
            '--webroot -d mydemo.here -w /srv/mydemo/runtime/certbot',
            'shutdown -r now',
        ]


class TestSys:

    def test_info(self, run_command_mock):

        assert run_command_mock('info') == [
            'uname -a', 'cat /etc/timezone', 'uptime', 'df -h']

    def test_reboot(self, run_command_mock):

        assert run_command_mock('reboot') == ['shutdown -r now']
