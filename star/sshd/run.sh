#!/bin/sh

# restore host keys or generate if not present
cp /host_keys/* /etc/ssh/
ssh-keygen -A
cp /etc/ssh/ssh_host_* /host_keys

# do not detach (-D), log to stderr (-e), passthrough other arguments
/usr/sbin/sshd -D -e "$@"