Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/home/vagrant/CPTS"
  config.vm.provision "shell",
    inline: "echo 'PYTHONPATH=/home/vagrant/CPTS' >> /etc/environment"
end
