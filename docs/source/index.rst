webscaff documentation
======================
https://github.com/idlesign/webscaff



Description
-----------

*Remote scaffolding and orchestration for web applications*


Used stack
~~~~~~~~~~

* **Debian**-based OS (Ubuntu 18.04, 20.04 tested) as a basis.
* **Git** for source code updates.
* **Systemd** to securely run your webservice.
* **PostgreSQL** as a reliable DBMS.
* **uWSGI** as a platform (handling routing, static, background tasks, etc.).
* **Python 3** to cover your needs.
* **Django** as a rich and solid webframework.

And also:

* **Certbot** integration for free HTTPS certificates (webroot plugin).
* SSH Agent forwarding for project code updates on remote using keys from your system.



Requirements
------------

1. Python 3.6+
2. makeapp 1.3.0+ (to streamline project initialization)



Table of Contents
-----------------

.. toctree::
    :maxdepth: 4

    quickstart
    faq
