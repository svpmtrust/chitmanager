
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
end
