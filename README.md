# configdiffer
A tool that can fetch the original version of configuration files (/etc/stuff) from the source, and compare it with the one in use. Only works with apt (Debian deriatives)

## Examples
```
$ ./configdiffer.py /etc/rsyslog.conf
File /etc/rsyslog.conf is associated with package rsyslog, installed version 8.2102.0-2+deb11u1
Downloading package... Done.
File saved to /tmp/tmpjprbxnzj/rsyslog_8.2102.0-2+deb11u1_amd64.deb
diff below:

```
