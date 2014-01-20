# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.define "rpm" do |rpm|
    rpm.vm.box = "centos65"
    rpm.vm.box_url = "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.1/centos65-x86_64-20131205.box"
    rpm.vm.network :private_network, ip: "192.168.33.10"
    rpm.vm.network "forwarded_port", guest: 80, host: 8080
    rpm.vm.provision :shell do |shell|
      shell.path = "./build/rpm/setup.sh"
      shell.privileged = false
    end
  end

  config.vm.define "deb" do |deb|
    deb.vm.box = "debian70"
    deb.vm.box_url = "https://dl.dropboxusercontent.com/u/86066173/debian-wheezy.box"
    deb.vm.network :private_network, ip: "192.168.33.11"
    deb.vm.provision :shell do |shell|
      shell.path = "./build/deb/setup_deb.sh"
    end
  end

end
