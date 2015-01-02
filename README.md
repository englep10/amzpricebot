Amazon Price Bot
-----------

Get notified when items go on sale.

# Installing Vagrant

In order to run Vagrant, you need:

- VirtualBox installed
- Ruby installed (should be on your system already)
- Vagrant 1.1+ installed (see
  http://docs.vagrantup.com/v2/installation/index.html).

This should be all it takes to set up Vagrant.

You will also need to install ansible so that Vagrant can use playbooks to provision the VM

    sudo pip install ansible

Now bootstrap your virtual machines with the following command. Note that you do not need to download any "box" manually. This project already includes a `Vagrantfile` to get you up and running, and will get one for you if needed.

`vagrant up`

and go grab yourself a coffee...

If something goes wrong, refer to Vagrant's [Getting Started
Guide](http://docs.vagrantup.com/v2/getting-started/index.html).

The contents of `code` will be available inside the VM at /data/code