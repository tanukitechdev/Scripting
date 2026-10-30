#26/05/2026
#Realizado por: Luis Miguel Espinoza


#Script Python para extracción de logs pfblocker

#1. Conexión SSH
#Se verifica que la conexión de manera local con SSH a pfsense sea correcta. Dentro del símbolo del sistema, colocamos el siguiente comando:
#ssh admin@[IP pfsense]

#Una vez dado ENTER nos pedirá que coloquemos la contraseña del usuario. Si al ingresar la contraseña aparece le menú de pfsense, la conexión SSH está completamente habilitada. 

import paramiko
import os


# 1. Configuración de conexión SSH a pfsense (credenciales)
host_pfsense = "192.168.X.X" #IP del pfsense DMNT
username = "" #usuario admin pfsense
password = "" #Contraseña de usuario admin
port = 22

# 2. Rutas del archivo log de pfblocker (Bloqueos de dominio e IP)
remote_path_dnsbl = "/var/log/pfblockerng/dnsbl.log" #Lista DNSBL
remote_path_ip = "/var/log/pfblockerng/ip_block.log"  #Lista ip_block

local_path_dnsbl = "../logs/dnsbl_crudo.log"
local_path_ip = "../logs/ip_crudo.log"

def descargar_log_pfsense():
    
    ssh = paramiko.SSHClient() #Inicializar cliente SSH
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Aceptar automáticamente la llave del pfsense en caso de ser primera vez

    try:
        print(f"Iniciando conexión segura con {host_pfsense}...")

        #Conexión con el servidor
        ssh.connect(hostname=host_pfsense, port=port, username=username, password=password)
        print("Se estableció la conexión de manera exitosa")

        #Abir el canal SFTP para la transferencia de los archivos
        print("Abriendo canal SFTP...")
        sftp = ssh.open_sftp()

        #Descarga de archivo
        print(f"Descargando archivos log desde: {remote_path_dnsbl} y {remote_path_ip}...")
        sftp.get(remote_path_dnsbl, local_path_dnsbl)
        sftp.get(remote_path_ip, local_path_ip)

        #Cerrar conexiones
        sftp.close()
        ssh.close()
        print(f"El proceso ha terminado. Archivos guardados de forma local en '{remote_path_dnsbl}' y '{remote_path_ip}'")

    except Exception as e:
        print(f"Se ha producido un error durante el pipeline de extracción {e}")

if __name__ == "__main__":
    descargar_log_pfsense()

    
