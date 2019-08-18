# AnsibleMine

!! Remote server must be debian 9 or newer !!

## What?

Setup a remote Minecraft server with Ansible and Docker in 1 minute!

## Dependencies you have to install yourself:

* [Python](https://www.python.org/downloads/)
* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* [Python Docker](https://pypi.org/project/docker/)

## How?

### Prerequisites

(required)
1. Copy the `inventory.example` to `inventory` and fill it with your servers
1. Configure `vars.yml`

(optional)
1. Put your `world` folder into `data/` -> `data/world/`

### Create Servers

```bash
bash createServer.sh
```

### Backup all Servers

```bash
bash getBackup.sh
```
