Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder ".", "/home/vagrant/lazy_unit_tester"
  config.vm.provision "shell",
   inline: "sudo apt-get update"
  config.vm.provision "shell",
   inline: "sudo apt-get install python-pip -y"
  config.vm.provision "shell",
   inline: "sudo pip install /home/vagrant/lazy_unit_tester"
  config.vm.provision "shell",
   inline: "python /home/vagrant/lazy_unit_tester/tests/test_create_tests.py"
end
