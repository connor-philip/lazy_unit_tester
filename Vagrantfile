Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/home/vagrant/lazy_unit_tester"
  config.vm.provision "shell",
    inline: "echo 'PYTHONPATH=/home/vagrant/lazy_unit_tester' >> /etc/environment"
end
