import glob
import types
from typing import List
import inquirer
import os.path
import subprocess
import json
import re


class ModpackPreset:
    name: str
    displayName: str
    modpack_location: str
    server_curse_forge_modpack: str


class ServerConfig:
    ip: str
    password: str
    memory: str
    name: str
    modpack: str


def get_server_config() -> List[ServerConfig]:
    if not os.path.isfile(server_file_name):
        print('could not access servers file.')
        exit(0)

    with open(server_file_name) as json_file:
        return json.load(json_file)


def add_new_server_to_config(new_server: ServerConfig) -> None:
    config = get_server_config()
    config.append(new_server)
    f = open(server_file_name, 'w')
    f.write(json.dumps(config))
    f.close()


def remove_server_from_config(selected_server: ServerConfig) -> None:
    config = get_server_config()
    index = config.index(selected_server)
    del config[index]
    f = open(server_file_name, 'w')
    f.write(json.dumps(config))
    f.close()
    q_list_servers()


def get_modpack_presets() -> List[ModpackPreset]:
    modpacks = []
    for file in glob.glob("./modpackPresets/*.json"):
        with open(file) as json_file:
            modpacks.append(json.load(json_file))
    return modpacks


def generate_inventory(server_config: ServerConfig) -> None:
    password = '' if server_config['password'] == '' else 'ansible_ssh_pass={}'.format(server_config['password'])
    inventory_string = '[mineservers]\n{} ansible_user=root {} #autogenerated'.format(server_config['ip'], password)
    f = open(inventory_file_name, 'w')
    f.write(inventory_string)
    f.close()


def generate_vars(server_config: ServerConfig) -> None:
    selected_modpack = next((x for x in get_modpack_presets() if x['name'] == server_config['modpack']), None)
    values_string = """# Autogenerated config
server_port: "25565"
server_memory: "{}"
server_version: "LATEST"
server_pvp: "TRUE"
server_onlinemode: "TRUE"
server_name: "Anisble Minecraftserver"
server_difficulty: "normal"
server_maxplayers: "20"
server_icon: ""
server_showachievements: "TRUE"
server_ops: ""
server_motd: "Have fun!"
world_location: "{}"
server_curse_forge_modpack: "{}"
user_uid: "6969" 
""".format(server_config['memory'],
               selected_modpack['modpack_location'],
               selected_modpack['server_curse_forge_modpack']
               )
    f = open(values_file_name, 'w')
    f.write(values_string)
    f.close()


def create_server(server_config: ServerConfig) -> None:
    print('Creating Server')
    subprocess.call('./createServer.sh')


def start_server(server_config: ServerConfig) -> None:
    print('Starting Server')
    subprocess.call('./start_server.sh')


def stop_server(server_config: ServerConfig) -> None:
    print('Stopping Server')
    subprocess.call('./stop_server.sh')


def backup_server(server_config: ServerConfig) -> None:
    print('Zipping and downloading the maps to the folder backups')
    subprocess.call('./getBackup.sh')


def get_server_logs(server_config: ServerConfig) -> None:
    print('Getting logs')
    subprocess.call('./getLogs.sh')


def self_hosted_setup() -> None:
    modpacks = []
    for modpack in modpack_presets:
        modpacks.append(('[+] ' + modpack['displayName'], modpack['name']))

    new_server = inquirer.prompt(
        [
            inquirer.Text(name='ip', message='Server ip',
                          validate=lambda _, x: re.match('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', x)),
            inquirer.Password(name='password', message='Server password (SKIP if you are using an ssh key)'),
            inquirer.Text(name='memory', message='Minecraft Server memory eg. "20G", "1024M"',
                          validate=lambda _, x: re.match('^\d{1,4}(G|M)$', x)),
            inquirer.Text(name='name', message='Server name (only visual, can be whatever you like)'),
            inquirer.List(name='modpack', message='Select a modpack preset', choices=modpacks)
        ])

    add_new_server_to_config(new_server)
    q_list_servers()


def q_server_options(selected_server: ServerConfig) -> None:
    inquirer.prompt(
        [inquirer.List('q_server_options', message='Options',
                       choices=[('[Provision] server', create_server), ('[Start] server', start_server),
                                ('[Stop] server', stop_server), ('[Backup] server world', backup_server),
                                ('[Logs] get', get_server_logs),
                                ('[Delete] server from list', remove_server_from_config),
                                ('[Back] to server selection', q_list_servers)])
         ]).get('q_server_options')(selected_server)


def exit_program() -> None:
    exit(0)


def q_list_servers(ignored=True) -> None:
    server_list = []
    for server in get_server_config():
        server_list.append(('-> ' + server['name'], server))
    server_list.append(('[Add] a new server', self_hosted_setup))
    server_list.append(('[Exit]', exit_program))

    result = inquirer.prompt(
        [inquirer.List('action', message='Select Server', choices=server_list)]).get('action')

    if isinstance(result, types.FunctionType):
        result()
    else:
        print(result)
        generate_vars(result)
        generate_inventory(result)
        q_server_options(result)


server_file_name = './servers.json'
inventory_file_name = './inventory'
values_file_name = './vars.yml'
modpack_presets = get_modpack_presets()


def main() -> None:
    q_list_servers()


if __name__ == '__main__':
    main()
