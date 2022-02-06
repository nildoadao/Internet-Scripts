#!/usr/bin/env python3
import os
from os import listdir

class Servidor:
    hostname = ""
    kernel = ""
    interfaces = []
    mount_points = []

    def __init__(self):
        self.hostname = ""
        self.kernel = ""
        self.interfaces = []
        self.mount_points = []

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def add_mount(self, mount):
        self.mount_points.append(mount)

    def set_hostname(self, host):
        self.hostname = host

    def set_kernel(self, kernel):
        self.kernel = kernel

def build_servers_antes_list():
    antes_files = listdir("./antes")
    server_list = []
    for item in antes_files:
        if "kernel" in item:
            server_list.append(item.split('_')[0])
    return server_list

def build_servers_depois_list():
    antes_files = listdir("./depois")
    server_list = []
    for item in antes_files:
        if "kernel" in item:
            server_list.append(item.split('_')[0])
    return server_list

def check_state_antes():
    servers = []

    for host in build_servers_antes_list():
        server = Servidor()
        server.set_hostname(host)

        try:
            with open("./antes/{}_rede.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.add_interface(line.strip())
        except:
            server.add_interface("Erro leitura")

        try:
            with open("./antes/{}_mounts.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.add_mount(line.strip())
        except:
            server.add_mount("Erro leitura")

        try:
            with open("./antes/{}_kernel.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.set_kernel(line.strip())
        except:
            server.set_kernel("Erro leitura")

        servers.append(server)

    return servers

def check_state_depois():
    servers = []

    for host in build_servers_depois_list():
        server = Servidor()
        server.set_hostname(host)
        
        try:
            with open("./depois/{}_rede.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.add_interface(line.strip())
        except:
            server.add_interface("Erro leitura")

        try:
            with open("./depois/{}_mounts.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.add_mount(line.strip())
        except:
            server.add_mount("Erro leitura")

        try:
            with open("./depois/{}_kernel.txt".format(host), mode="r") as f:
                for line in f.readlines():
                    server.set_kernel(line.strip())
        except:
            server.set_kernel("Erro leitura")

        servers.append(server)

    return servers

def check_kernel_update(kernel):
    updated_kernel = "5.10.16.3"
    if updated_kernel in kernel:
        return "\t- Kernel OK\n"
    else:
        return "\t* Kernel Não Atualizado\n"

def check_rede(server_antes, server_depois):
    response = ""
    for rede in server_antes.interfaces:
        if not interface_exists(rede, server_depois):
            response += "\t* interface {} não encontrada\n".format(rede)   
    if response == "":
        response = "\t- Interfaces OK\n"
    return response

def check_mounts(server_antes, server_depois):
    response = ""
    for mount in server_antes.mount_points:
        if not mount_exists(mount, server_depois):
            response += "\t* mount: {} não encontrado\n".format(mount)   
    if response == "":
        response = "\t- Mount Points OK\n"
    return response

def get_server_by_name(host, server_list):  
    for item in server_list:
        if host in item.hostname:
            return item
    return None

def interface_exists(interface_name, server):
    status = False
    for interface in server.interfaces:
        if interface == interface_name:
            status = True
    return status

def mount_exists(mount_name, server):
    status = False
    for mount in server.mount_points:
        if mount == mount_name:
            status = True
    return status

servers_antes = check_state_antes()
servers_depois = check_state_depois()

for antes in servers_antes:
    depois = get_server_by_name(antes.hostname, servers_depois)
    with open("logs_consolidados.txt", mode="a") as f:
        f.writelines("{}\n".format(antes.hostname))
        if depois is None:
            f.writelines("\t* Servidor {} não aparece na lista depois\n".format(antes.hostname))
            continue
        f.writelines("{}".format(check_kernel_update(depois.kernel)))
        f.writelines("{}".format(check_rede(antes,depois)))
        f.writelines("{}".format(check_mounts(antes,depois)))
    