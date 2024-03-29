#!/bin/bash
set -e

echo "172.16.82.150 vz-uyuni-srv.tf.local vz-uyuni-srv" > /etc/hosts

#zypper rr Test-Channel-x86_64 || :

# temporarily disable non-working repo
#zypper mr --disable Test-Channel-x86_64 || :
#zypper --non-interactive --gpg-auto-import-keys ref

# install, configure, and start avahi
#zypper --non-interactive in avahi
#cp /root/avahi-daemon.conf /etc/avahi/avahi-daemon.conf
#/usr/sbin/avahi-daemon -D

# re-enable normal repo and remove helper repo
#zypper mr --enable Test-Channel-x86_64 || :
#zypper rr sles12sp5

# do the real test
#zypper --non-interactive --gpg-auto-import-keys ref
#zypper --non-interactive in aaa_base aaa_base-extras net-tools timezone vim less sudo tar
