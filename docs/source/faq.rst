Q & A
=====


1. Getting *Private key file is encrypted* ``paramiko`` error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try the following:

* Upgrade ``paramiko`` to the latest version.
* https://unix.stackexchange.com/a/12201/32880
* https://askubuntu.com/a/853578/33408

2. How to upgrade OS
~~~~~~~~~~~~~~~~~~~~

This roughly boils to:

1. Restrict service access.

   ``$ webscaff off``

2. Backup data.

   ``$ webscaff run.backup``

   .. note:: If you use a cloud service this may also prove disk images/backups.

3. Start OS upgrade procedure.

   ``$ webscaff sys.utils.os-upgrade``

4. Upgrade PostgreSQL cluster.

   ``$ webscaff sys.pg.cluster-upgrade X``

   .. note:: Where ``X`` is a previous PG version to upgrade from, e.g ``12``.

5. Cleanup from unused packages.

   ``$ webscaff sys.apt.autoremove``

6. Upgrade virtual environment to use a new system Python version.

   ``$ webscaff run.venv.repopulate``

7. Restart your service.

   ``$ webscaff restart``

   .. note:: Use ``$ webscaff log`` in a separate terminal window to see how the restart is happening.

