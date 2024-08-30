#!/bin/bash

echo "[** Cleaning up log files]"

> /vagrant/adminui.log
> /vagrant/normalui.log
> /vagrant/webapi.log
> /vagrant/jotti.log
> /vagrant/pythonapp.log

echo "[** Log files cleared]"