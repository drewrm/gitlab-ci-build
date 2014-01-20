Name: gitlab_ci
Version: 0.0.1
Release:	1%{?dist}
Summary: Gitlab CI Controller
Group: test
License: none
URL: http://gitlab.org/gitlab-ci
Source0: %{name}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: nginx mysql-server redis
%define  debug_package %{nil}

%description

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
cp -R . %{buildroot}/

mkdir -p %{buildroot}/etc/init.d/
cp ./opt/gitlab_ci/lib/support/init.d/gitlab_ci %{buildroot}/etc/init.d/
sed -i "s/APP_ROOT=.*$/APP_ROOT='\/opt\/gitlab_ci'/g" %{buildroot}/etc/init.d/gitlab_ci

mkdir -p %{buildroot}/etc/nginx/conf.d/
cp ./opt/gitlab_ci/lib/support/nginx/gitlab_ci %{buildroot}/etc/nginx/conf.d/gitlab_ci.conf
sed -i "s/\/home\/gitlab_ci\/gitlab-ci/\/opt\/gitlab_ci/g" %{buildroot}/etc/nginx/conf.d/gitlab_ci.conf

mkdir -p  %{buildroot}/opt/gitlab_ci/tmp/sockets/
mkdir -p  %{buildroot}/opt/gitlab_ci/tmp/pids/
mkdir -p  %{buildroot}/opt/gitlab_ci/log/
cp %{buildroot}/opt/gitlab_ci/config/application.yml.example %{buildroot}/opt/gitlab_ci/config/application.yml

cp %{buildroot}/opt/gitlab_ci/config/puma.rb.example %{buildroot}/opt/gitlab_ci/config/puma.rb
sed -i "s/\(application_path\).=.*$/\1 = '\/opt\/gitlab_ci'/g"  %{buildroot}/opt/gitlab_ci/config/puma.rb

cp %{buildroot}/opt/gitlab_ci/config/database.yml.mysql %{buildroot}/opt/gitlab_ci/config/database.yml
sed -i  "s/username:.*root/username: gitlab_ci/g" %{buildroot}/opt/gitlab_ci/config/database.yml
sed -i  "s/password:.*$/password: gitlab_ci/g" %{buildroot}/opt/gitlab_ci/config/database.yml
sed -i  "s/#.*host:.*localhost/host: localhost/g" %{buildroot}/opt/gitlab_ci/config/database.yml

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root,-)
/etc/init.d/gitlab_ci
%defattr(-,root,root,-)
/etc/nginx/conf.d/gitlab_ci.conf
%defattr(-,gitlab_ci,gitlab_ci,-)
/opt/gitlab_ci
%doc

%pre
id gitlab_ci > /dev/null 2>&1
if [ $? -ne 0 ]; then
    useradd -d /opt/gitlab_ci gitlab_ci
fi

%post
sed -i "s/server_name ci.gitlab.org/server_name $(hostname)/g" /etc/nginx/conf.d/gitlab_ci.conf
cd /opt/gitlab_ci && (sudo -u gitlab_ci -i bundle check || sudo -u gitlab_ci -i bundle install --without postgres development test --deployment)
cd /opt/gitlab_ci && sudo -u gitlab_ci -i bundle exec rake assets:precompile RAILS_ENV=production
cd /opt/gitlab_ci && sudo -u gitlab_ci -i bundle exec whenever -w RAILS_ENV=production
%preun

service gitlab_ci status

if [ $? -eq 0 ]; then
    service gitlab_ci stop
fi

%changelog