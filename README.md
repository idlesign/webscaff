webscaff
========
https://github.com/idlesign/webscaff


[![PyPI - Version](https://img.shields.io/pypi/v/webscaff)](https://pypi.python.org/pypi/webscaff)
[![License](https://img.shields.io/pypi/l/webscaff)](https://pypi.python.org/pypi/webscaff)
[![Coverage](https://img.shields.io/coverallsCoverage/github/idlesign/webscaff)](https://coveralls.io/r/idlesign/webscaff)
[![Docs](https://img.shields.io/readthedocs/webscaff)](https://webscaff.readthedocs.io/)

## Description

*Remote scaffolding and orchestration for web applications*

### Used stack

* **Debian**-based OS (Ubuntu 18.04, 20.04, 22.04 tested) as a basis.
* **Git** for source code updates.
* **Systemd** to securely run your webservice.
* **PostgreSQL** as a reliable DBMS.
* **uWSGI** as a platform (handling routing, static, background tasks, etc.).
* **Python 3** to cover your needs.
* **Django** as a rich and solid webframework.

And also:

* **Certbot** integration for free HTTPS certificates (webroot plugin).
* SSH Agent forwarding for project code updates on remote using keys from your system.


### A taste of it

After install the `webscaff` command is available.

```bash
; We rollout project skeleton using `makeapp`.
$ makeapp new myproject -d "My webscaff project" -t webscaff /home/some/here

; Switch into project directory containing `wscaff.yml` which is used by webscaff.
$ cd /home/some/here

; Get basic information about the remote.
$ webscaff info

; Prepare the remote for you web application.
$ webscaff run.initialize
```

Webscaff offers a number of useful command, among them:

```bash
; Rollout a new version of yor project from repository.
$ webscaff rollout

; Make a backup and download to local directory.
$ webscaff run.backup
```

More commands are available.

Detailed instructions could be found in the documentation.

## Documentation

https://webscaff.readthedocs.io
