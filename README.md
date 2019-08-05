# AnsibleMine

!! Remote server must be debian 9 or newer !!

## What?

Setup a remote Minecraft server with Ansible and Docker in 1 minute!

## Dependencies

* [Python](https://www.python.org/downloads/)
* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* [Python Docker](https://pypi.org/project/docker/)

## How?

1. Put your `world` folder into `data/` -> `data/world/`
1. Copy the `inventory.example` to `inventory`
1. Put your servers into the `inventory`
1. Run `createServer.sh` or `ansible-playbook playbook.yml -i inventory`
