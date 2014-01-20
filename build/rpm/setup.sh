#!/usr/bin/env bash

SOURCE_DIR="/home/vagrant/gitlab-ci"
RUBY_PATCH="p353"

function build_ruby {
    sudo yum -y install rpmdevtools readline libyaml libyaml-devel readline-devel ncurses ncurses-devel \
           gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel db4-devel byacc make libffi-devel


    wget https://raw.github.com/nmilford/specfiles/master/ruby-2.0/ruby-2.0.spec -O ~/rpmbuild/SPECS/ruby-2.0.spec

    if [ ! -f  ~/rpmbuild/SOURCES/ruby-2.0.0-$RUBY_PATCH.tar.gz ]; then
        wget http://ftp.ruby-lang.org/pub/ruby/2.0/ruby-2.0.0-$RUBY_PATCH.tar.gz -O ~/rpmbuild/SOURCES/ruby-2.0.0-$RUBY_PATCH.tar.gz
    fi

    sed -i "s/rubyminorver.*p0/rubyminorver $RUBY_PATCH/g" ~/rpmbuild/SPECS/ruby-2.0.spec
    rpmbuild -bb ~/rpmbuild/SPECS/ruby-2.0.spec
}


sudo yum install -y rpmbuild mock fedpkg git libyaml-devel readline-devel zlib-devel libffi-devel openssl-devel nginx mysql-server mysql-client redis
sudo usermod -a -G mock vagrant

#build_ruby

if [ ! -d $SOURCE_DIR ]; then
    git clone https://gitlab.com/gitlab-org/gitlab-ci.git $SOURCE_DIR
fi

git --work-tree=$SOURCE_DIR --git-dir=$SOURCE_DIR/.git  archive master --format=tar --prefix=gitlab_ci-0.0.1/opt/gitlab_ci/ | gzip > ~/rpmbuild/SOURCES/gitlab_ci.tar.gz
rpmbuild -bb /vagrant/build/rpm/gitlab-ci.spec


sudo rpm -e gitlab_ci
sudo rpm -Uvh /home/vagrant/rpmbuild/RPMS/noarch/gitlab_ci-0.0.1-1.el6.noarch.rpm