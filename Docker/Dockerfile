FROM vz-uyuni-s125.tf.local:5000/toaster-sles12sp3-products
MAINTAINER Admin User "noemail@example.com"

ARG repo
ARG cert

RUN echo "$cert" > /etc/pki/trust/anchors/RHN-ORG-TRUSTED-SSL-CERT.pem
RUN update-ca-certificates
RUN echo "$repo" > /etc/zypp/repos.d/susemanager:dockerbuild.repo

ADD nsswitch.conf /etc/nsswitch.conf
ADD avahi-daemon.conf /root/avahi-daemon.conf
ADD sles12sp5.repo /etc/zypp/repos.d/sles12sp5.repo

ADD add_packages.sh /root/add_packages.sh
RUN /root/add_packages.sh
