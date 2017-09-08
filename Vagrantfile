# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.synced_folder ".", '/home/ubuntu/hydroponics'
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python-pip nmap
    pip install ansible
  SHELL

end
