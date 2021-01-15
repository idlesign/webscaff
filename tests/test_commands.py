from freezegun import freeze_time


class TestUtils:

    def test_cfg(self, run_command_mock, capsys):
        assert run_command_mock('cfg') == []
        read = capsys.readouterr()
        assert '"name": "mydemo"' in read.out


class TestProj:

    def test_dump(self, run_command_mock):

        with freeze_time('2020-01-11T11:55'):

            assert run_command_mock('run.backup') == [
                'mkdir -p /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump',
                'bash -c "cd /var/lib/mydemo/media && tar -czf /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump/media.tar.gz *"',
                'bash -c "cd /etc/letsencrypt && tar -czf /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump/certbot.tar.gz *"',
                'pg_dump -Fc mydemo > /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump/db.dump',
                'bash -c "cd /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump && tar -czf /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump.tar.gz *"',
                'rm -rf /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump.tar.gz',
                'rm -rf /var/lib/mydemo/dumps/2020-01-11T1155-mydemo_dump',
            ]

    def test_restore(self, run_command_mock):
        assert run_command_mock('run.restore', '/nonexistent') == []
        assert run_command_mock('run.restore', '/tmp') == [
            'put /tmp /var/lib/mydemo/dumps/tmp',
            'mkdir -p /var/lib/mydemo/dumps/tmp',
            'tar -xzf /var/lib/mydemo/dumps/tmp -C /var/lib/mydemo/dumps/tmp',
            'rm -rf /var/lib/mydemo/dumps/tmp',
            'mkdir -p /var/lib/mydemo/media',
            'tar -xzf /var/lib/mydemo/dumps/tmp/media.tar.gz -C /var/lib/mydemo/media',
            'mkdir -p /etc/letsencrypt',
            'tar -xzf /var/lib/mydemo/dumps/tmp/certbot.tar.gz -C /etc/letsencrypt',
            'dropdb mydemo',
            'createdb mydemo',
            'pg_restore --dbname mydemo /var/lib/mydemo/dumps/tmp/db.dump',
            'rm -rf /var/lib/mydemo/dumps/tmp',
        ]

    def test_bootstrap(self, run_command_mock, monkeypatch):
        monkeypatch.setattr('webscaff.commands.utils.rsync_patchwork', lambda *args, **kwargs: None)

        assert run_command_mock('run.initialize') == [
            'whoami',
            'id -u mydemo',
            'useradd -s /bin/bash mydemo',
            'adduser tstout mydemo',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            "echo '' >> /var/lib/mydemo/bootstrap",
            'cat /var/lib/mydemo/bootstrap',
            'apt-get update',
            'apt install -y python3-dev python3-pip python3-venv python3-wheel '
            'build-essential libjpeg-dev libxml2-dev libxslt1-dev libpcre3-dev libssl-dev '
            'git postgresql libpq-dev certbot acl mc htop net-tools ncdu',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^apt$" "/var/lib/mydemo/bootstrap"',
            'mkdir -p /srv/mydemo',
            'chown -R mydemo:mydemo /srv/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /srv/mydemo',
            'mkdir -p /var/lib/mydemo',
            'chown -R mydemo:mydemo /var/lib/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo',
            'mkdir -p /var/lib/mydemo/dumps',
            'chown -R mydemo:mydemo /var/lib/mydemo/dumps',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/dumps',
            'mkdir -p /var/lib/mydemo/static',
            'chown -R mydemo:mydemo /var/lib/mydemo/static',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/static',
            'mkdir -p /var/lib/mydemo/media',
            'chown -R mydemo:mydemo /var/lib/mydemo/media',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/media',
            'rm -rf /var/cache/mydemo*',
            'mkdir -p /var/cache/mydemo',
            'chown -R mydemo:mydemo /var/cache/mydemo',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/cache/mydemo',
            'test -e "$(echo /var/lib/mydemo/environ)"',
            'test -e "$(echo /var/lib/mydemo/environ)"',
            'egrep "^production$" "/var/lib/mydemo/environ"',
            'mkdir -p ~/mydemo',
            'ln -sf /srv/mydemo ~/mydemo/code',
            'ln -sf /var/lib/mydemo ~/mydemo/state',
            'ln -sf /var/cache/mydemo ~/mydemo/cache',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^paths$" "/var/lib/mydemo/bootstrap"',
            'test -e "$(echo /srv/mydemo/.git)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^git$" "/var/lib/mydemo/bootstrap"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^configs$" "/var/lib/mydemo/bootstrap"',
            'test -e "$(echo /srv/mydemo/venv)"',
            'cd /srv/mydemo',
            'pip3 install -e .',
            'pip3 install  wheel',
            'pip3 install  -r /srv/mydemo/requirements.txt',
            'ln -sf /srv/mydemo/venv/bin/mydemo /usr/bin/mydemo',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^venv$" "/var/lib/mydemo/bootstrap"',
            'pg_config --version',
            'createdb mydemo',
            'createuser mydemo',
            'psql -c "GRANT ALL PRIVILEGES ON DATABASE mydemo TO mydemo"',
            'service postgresql restart',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^pg$" "/var/lib/mydemo/bootstrap"',
            'mkdir -p /var/lib/mydemo/static',
            'chown -R mydemo:mydemo /var/lib/mydemo/static',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/static',
            'mkdir -p /var/lib/mydemo/media',
            'chown -R mydemo:mydemo /var/lib/mydemo/media',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/media',
            'ln -sf /srv/mydemo/conf/env_production.py '
            '/srv/mydemo/mydemo/settings/env_production.py',
            'mydemo migrate',
            'mydemo createsuperuser --email idlesign@some.com --username idlesign',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^django$" "/var/lib/mydemo/bootstrap"',
            'touch /var/lib/mydemo/reloader',
            'mkdir -p /var/lib/mydemo/spool',
            'chown -R mydemo:mydemo /var/lib/mydemo/spool',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/spool',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^uwsgi$" "/var/lib/mydemo/bootstrap"',
            'systemctl enable --now /srv/mydemo/conf/mydemo.service',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^service$" "/var/lib/mydemo/bootstrap"',
            'mkdir -p /var/lib/mydemo/certbot',
            'chown -R mydemo:mydemo /var/lib/mydemo/certbot',
            'setfacl -Rm "g:mydemo:rwX,d:g:mydemo:rwX,m:rwx" /var/lib/mydemo/certbot',
            'certbot',
            'ln -sf /srv/mydemo/conf/mydemo-certbot-hook.sh '
            '/etc/letsencrypt/renewal-hooks/deploy/mydemo',
            'certbot --agree-tos --no-eff-email --email idlesign@some.com certonly '
            '--webroot -d mydemo.here -w /var/lib/mydemo/certbot',
            'setfacl -Rm "g:mydemo:--x" /etc/letsencrypt/archive/',
            'setfacl -Rm "g:mydemo:r-x" /etc/letsencrypt/archive/mydemo.here/',
            'setfacl -Rm "g:mydemo:--x" /etc/letsencrypt/live/',
            'setfacl -Rm "g:mydemo:r-x" /etc/letsencrypt/live/mydemo.here/',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'test -e "$(echo /var/lib/mydemo/bootstrap)"',
            'egrep "^certbot$" "/var/lib/mydemo/bootstrap"',
            'shutdown -r now'
        ]


class TestSys:

    def test_info(self, run_command_mock):

        assert run_command_mock('info') == [
            'who', 'uname -a', 'cat /etc/timezone', 'uptime', 'df -h', 'journalctl --disk-usage']

    def test_reboot(self, run_command_mock):

        assert run_command_mock('sys.utils.reboot') == ['shutdown -r now']
