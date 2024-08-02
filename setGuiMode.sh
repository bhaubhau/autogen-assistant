#!/bin/bash

sudo cp grubGui /etc/default/grub
sudo update-grub
sudo systemctl enable graphical.target --force
sudo systemctl set-default graphical.target
