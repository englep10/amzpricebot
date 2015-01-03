Amazon Price Bot
================

Get notified when items go on sale.

Prereqs
-------

- VirtualBox
- Ruby
- Vagrant 1.1+
- Ansible

Install
-------

Once you have these requirements installed, cd to the `amzpricebot` dir and run:

`vagrant up`

then go grab yourself a coffee...

If something goes wrong, refer to Vagrant's [Getting Started
Guide](http://docs.vagrantup.com/v2/getting-started/index.html).

Use
---

From `amzpricebot` directory:

    cp code/example.settings.py code/settings.py

Edit the settings.py file with your google email/pwd and the items you wish to watch.  Each section under "watch" contains the name, desired price, and URL.
When done run:

    vagrant ssh

This will connect you to the VM.
Now run:

    sudo /etc/init.d/celeryd start
    sudo /etc/init.d/celerybeat start

And the watchers will begin.