#!/bin/bash

sudo cp grubTerm /etc/default/grub
sudo update-grub
sudo systemctl enable multi-user.target --force
sudo systemctl set-default multi-user.target
