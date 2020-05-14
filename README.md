<p align="center">
  <img alt="AnsibleMine" src="https://raw.githubusercontent.com/wladi0097/AnsibleMine/master/logo.png" width="500"/>
</p>

### Supported Platforms

* Ubuntu 18.04.
* Debian 9 or newer.

### Quick tutorial:
* The host system should have `Python`, `Ansible` and `Python Docker` installed
* Copy the `inventory.example` to `inventory` and fill it with your server(s)
* Configure `vars.yml`
* Put your world.zip or world into `data`
* Run `bash createServer.sh`

## What?

Setup multiple remote Minecraft servers with Ansible and Docker in minutes.

This is using the awesome [docker image](https://github.com/itzg/docker-minecraft-server) provided by [itzg](https://github.com/itzg) in the background.

## Dependencies the host system should have:

This programm was written for Linux and only tested on that.

* [Python](https://www.python.org/downloads/)
* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* [Python Docker](https://pypi.org/project/docker/)

These are host only requirements. They will be automatically installed on the remote system, if they are not already.

## How?

### Prerequisites / Configuration

(required)
1. Copy the `inventory.example` to `inventory` and fill it with your servers. 
  * There are two options:
    * With ssh key already on the servers -> `1.1.1.1 ansible_user=root`
    * With paswords -> `1.1.1.1 ansible_user=root ansible_ssh_pass=pass`

2. Configure `vars.yml`
  * In use vars files and examples can be found in the `examples` folder
  * If you want a vanilla server, just fill out the `#Required` section or keep the default settings.
  * If you want a curseforge modded server the `#Required` section of the vars will be ignored. Just fill out the `server_curse_forge_modpack` and `world_location`.

(optional)
1. Put your `world` folder into `data/` -> `data/world/`
or
1. Provide your zipped world contents as `world.zip` and put this into `data/` (DO NOT ZIP THE FOLDER BUT ITS CONTENT!)

### Create Servers

```bash
bash createServer.sh
```

This command will:
1. Install all dependencies
1. Upload your world
1. (Download the modpack if provided)
1. Start the minecraft server as configured

### Backup all Servers

```bash
bash getBackup.sh
```

* This will save your current world as `ip.timestamp`. Example: `127.0.0.2.1538461589.zip`.
* The backups are downloaded from all servers and are places in the `backups` folder
* To upload a backup, just move it to the `data` folder and call it `world.zip`

