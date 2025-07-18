# webscaff changelog


## Unreleased
* ++ 'info' now show Linux distribution information.
* ++ 'rollout --from-local' now can handle symlinks.
* ** Drop support for Python 3.6.
* ** Use pseudoterminal for 'os-upgrade' and 'screen'.


v1.0.0 [2022-11-27]
-------------------
+ Add 'sys.pg.cluster_upgrade' and 'sys.pg.cluster_drop' commands.
+ Add 'sys.utils.os-upgrade' command.
+ Add 'sys.utils.screen' command.
+ Added 'sys.apt.autoremove' command.
+ Command 'rollout' now supports '--from-local' option.
+ New command 'run.venv.populate'.
* Exposed run.git.pull command.


v0.3.2 [2021-12-19]
-------------------
* Enabled sys.apt.upgrade command.


v0.3.1 [2021-01-15]
-------------------
* Fix 'run.initialize' command permission error.


v0.3.0 [2021-01-15]
-------------------
+ New 'cfg' command.
* Enhance 'run.initialize' command: save progress to be able to resume.
* Enhance 'sys.cat' command: add 'printout' param.


v0.2.1 [2020-10-12]
-------------------
* Workaround patchwork issue: invoke.vendor.six.


v0.2.0 [2020-09-20]
-------------------
+ 'cache_init' now just empties cache directory by default.
+ 'info' now prints out current user information.
* Bootstrap spooler directory with right permissions.
* Improved boostrap of Certbot.


v0.1.0 [2020-02-16]
-------------------
+ Basic functionality.