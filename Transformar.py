#26/05/2026
#Elaborado por: Luis Miguel Espinoza

#Script para transformar los datos de los archivos log de pfblacker a formato csv para power BI

#Importar librerías

import pandas as pd
import os

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS (VARIABLES)
# ==========================================
# Rutas para el pipeline de Dominios (DNSBL)
archivo_crudo_dnsbl = "../logs/dnsbl_crudo.log"
archivo_limpio_dnsbl = "../datos_limpios/reporte_pfblocker_limpio.csv"

# Rutas para el nuevo pipeline de IPs
archivo_crudo_ip = "../logs/ip_crudo.log"
archivo_limpio_ip = "../datos_limpios/reporte_pfsense_ip_limpio.csv"

# Diccionario global para mapear los meses
meses_num = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}


# ==========================================
# 2. FUNCIÓN DE TRANSFORMACIÓN DE DOMINIOS (DNSBL)
# ==========================================
def transformar_datos_dnsbl():
    if not os.path.exists(archivo_crudo_dnsbl):
        print(f"Error: No se encuentra el archivo {archivo_crudo_dnsbl}.")
        return

    print("Iniciando extracción de texto para Dominios (DNSBL)...")
    datos_procesados = []

    with open(archivo_crudo_dnsbl, 'r', encoding='utf-8', errors='ignore') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            partes = [p.strip() for p in linea.split(',')]
            
            if len(partes) >= 5:
                fecha_bloque = partes[1]
                componentes_fecha = fecha_bloque.split()
                
                if len(componentes_fecha) == 3:
                    mes_texto, dia, hora = componentes_fecha
                    mes = meses_num.get(mes_texto, "05")
                    if len(dia) == 1:
                        dia = "0" + dia
                else:
                    dia, mes, hora = "26", "05", "12:00:00"

                fecha_final = f"{dia}/{mes}/2026"

                datos_procesados.append({
                    'Fecha': fecha_final,
                    'Hora': hora,
                    'IP_Origen': partes[3],
                    'Dominio': partes[2],
                    'Lista_Bloqueo': partes[4],
                    'Categoria': partes[5] if len(partes) > 5 else "DNSBL_Block"
                })

    if datos_procesados:
        df = pd.DataFrame(datos_procesados)
        existe_archivo = os.path.exists(archivo_limpio_dnsbl)
        df.to_csv(archivo_limpio_dnsbl, mode='a', index=False, header=not existe_archivo, encoding='utf-8')
        print(f"¡Éxito! Se añadieron {len(df)} filas nuevas al histórico de Dominios.")
    else:
        print("No se encontraron registros de dominios válidos.")


# ==========================================
# 3. FUNCIÓN DE TRANSFORMACIÓN DE IPs (NUEVA)
# ==========================================
def transformar_datos_ip():
    if not os.path.exists(archivo_crudo_ip):
        print(f"Error: No se encuentra el archivo {archivo_crudo_ip}.")
        return

    print("Iniciando extracción de registros de bloqueo de IP con posiciones reales...")
    datos_procesados = []

    with open(archivo_crudo_ip, 'r', encoding='utf-8', errors='ignore') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            partes = [p.strip() for p in linea.split(',')]
            
            # Validamos basándonos en la estructura de 17 campos que vimos en tu captura
            if len(partes) >= 15:
                try:
                    # 1. Procesar Fecha y Hora desde partes[0]
                    fecha_bloque = partes[0]
                    componentes_fecha = fecha_bloque.split()
                    
                    if len(componentes_fecha) == 3:
                        mes_texto, dia, hora = componentes_fecha
                        mes = meses_num.get(mes_texto, "06")
                        if len(dia) == 1:
                            dia = "0" + dia
                    else:
                        dia, mes, hora = "01", "06", "12:00:00"
                    
                    fecha_final = f"{dia}/{mes}/2026"

                    # 2. Extraer datos usando las posiciones reales de la captura
                    interfaz_red = f"{partes[3]} ({partes[2]})" # Genera: "LAN (igb2)"
                    ip_origen = partes[8]
                    ip_destino = partes[9]
                    protocolo = partes[7]
                    puerto_destino = partes[11]
                    lista_ip = partes[14]
                    categoria_ip = partes[16] if len(partes) > 16 else "IP_Block"
                    
                    datos_procesados.append({
                        'Fecha': fecha_final,
                        'Hora': hora,
                        'Interfaz': interfaz_red,
                        'IP_Origen': ip_origen,
                        'IP_Destino': ip_destino,
                        'Puerto_Destino': puerto_destino,
                        'Protocolo': protocolo,
                        'Lista_Bloqueo_IP': lista_ip,
                        'Categoria_IP': categoria_ip
                    })
                    
                except Exception as ex:
                    continue

    if datos_procesados:
        df = pd.DataFrame(datos_procesados)
        existe_archivo = os.path.exists(archivo_limpio_ip)
        df.to_csv(archivo_limpio_ip, mode='a', index=False, header=not existe_archivo, encoding='utf-8')
        print(f"¡Éxito! Se añadieron {len(df)} filas nuevas al histórico de IPs.")
    else:
        print("No se encontraron registros de IP válidos.")


# ==========================================
# 4. EJECUCIÓN DEL PIPELINE BI-CANAL
# ==========================================
if __name__ == "__main__":
    # Ejecuta el procesamiento de dominios bloqueados
    transformar_datos_dnsbl()
    
    # Ejecuta el procesamiento de IPs bloqueadas
    transformar_datos_ip()
    
    print("\n--- Pipeline de datos finalizado correctamente ---")

