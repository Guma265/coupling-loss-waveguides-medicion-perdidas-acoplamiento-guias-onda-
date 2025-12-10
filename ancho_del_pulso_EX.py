import pandas as pd
import numpy as np
import matplotlib
from scipy.signal import savgol_filter # Para suavizar señales
from scipy.optimize import curve_fit # Para el ajuste gaussiano
matplotlib.use('TkAgg')  # Establecemos el backend de Matplotlib para usar Tkinter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Aumentar el tamaño de la letra en todas las gráficas
plt.rcParams.update({'font.size': 16})

# Definición de la función gaussiana
# amp: amplitud, mu: media, sigma: desviación estándar
def gaussiana(x, amp, mu, sigma):
    return amp * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Función para calcular el FWHM en el eje X
# df: DataFrame con los datos, columna_valor: columna de intensidad, columna_posicion: columna de posiciones
# usar_ventana: si se desea usar una ventana de búsqueda alrededor del máximo
def calcular_fwhm(df, columna_valor, columna_posicion, usar_ventana=True, window_size=7500):
    # Encontramos el valor máximo y el índice donde ocurre
    max_value = df[columna_valor].max()
    half_max_value = max_value / 2
    max_value_index = df[columna_valor].idxmax()

    # Si se utiliza una ventana de búsqueda
    if usar_ventana:
         # Definimos la ventana alrededor del máximo
        window_start = max(0, max_value_index - window_size)
        window_end = min(len(df), max_value_index + window_size)
        df_window = df.iloc[window_start:window_end]

        # Encontramos los puntos donde la señal cruza la mitad del valor máximo
        start_index = df_window[df_window.index < max_value_index][columna_valor].sub(half_max_value).abs().idxmin()
        end_index = df_window[df_window.index > max_value_index][columna_valor].sub(half_max_value).abs().idxmin()

        # Convertimos los índices locales de la ventana en índices globales del DataFrame original
        start_index_global = df.index[window_start + (start_index - window_start)]
        end_index_global = df.index[window_start + (end_index - window_start)]
    else:
        # Si no se usa ventana, encontramos directamente los índices en el DataFrame completo
        start_index_global = df[df.index < max_value_index][columna_valor].sub(half_max_value).abs().idxmin()
        end_index_global = df[df.index > max_value_index][columna_valor].sub(half_max_value).abs().idxmin()

    # Calculamos el FWHM como la distancia entre los puntos donde la señal cruza la mitad del máximo
    fwhm = df.loc[end_index_global, columna_posicion] - df.loc[start_index_global, columna_posicion]
    return fwhm, start_index_global, end_index_global, half_max_value, max_value_index

# Función principal que nos procesa el archivo de datos, realiza los ajustes gaussianos y grafica
def calcular_fwhm_y(df, columna_valor, columna_posicion):
    max_value = df[columna_valor].max()
    half_max_value = max_value / 2
    max_value_index = df[columna_valor].idxmax()

    start_index = df[df.index < max_value_index][columna_valor].sub(half_max_value).abs().idxmin()
    end_index = df[df.index > max_value_index][columna_valor].sub(half_max_value).abs().idxmin()

    fwhm = df.loc[end_index, columna_posicion] - df.loc[start_index, columna_posicion]
    return fwhm, start_index, end_index, half_max_value, max_value_index

def procesar_y_graficar(file_path_new, num_picos_x, guia_tipo):
     # Abrimos el archivo de datos seleccionado y lo leemos línea por línea
    with open(file_path_new, 'r', encoding='ISO-8859-1') as file:
        file_content_new = file.readlines()

    # Convertimos las líneas del archivo en una lista de datos y columnas
    data = [line.split('\t') for line in file_content_new[11:]]
    columns = file_content_new[10].split('\t')
    df = pd.DataFrame(data, columns=columns)

    # Convertimos las columnas de texto en datos numéricos
    df['Pos X [µm]'] = pd.to_numeric(df['Pos X [µm]'].str.replace(',', '.'), errors='coerce')
    df['X Value [%]'] = pd.to_numeric(df['X Value [%]'].str.replace(',', '.'), errors='coerce')
    df['Pos Y [µm]'] = pd.to_numeric(df['Pos Y [µm]'].str.replace(',', '.'), errors='coerce')
    df['Y Value [%]'] = pd.to_numeric(df['Y Value [%]'].str.replace(',', '.'), errors='coerce')

    # Definimos si utilizaremos ventana en función del número de picos
    usar_ventana = num_picos_x > 1

    # Calculamos el FWHM para el eje X y mostramos la información
    fwhm_x, start_x, end_x, half_max_x, max_x_index = calcular_fwhm(df, 'X Value [%]', 'Pos X [µm]', usar_ventana)
    fwhm_start_to_max_x = df.loc[max_x_index, 'Pos X [µm]'] - df.loc[start_x, 'Pos X [µm]']
    fwhm_max_to_end_x = df.loc[end_x, 'Pos X [µm]'] - df.loc[max_x_index, 'Pos X [µm]']
    
    #etiqueta_x1 = 'e' if guia_tipo == 2 else 'b'
    #etiqueta_x2 = 'f' if guia_tipo == 2 else 'c'

    etiqueta_x1 = 'd' if guia_tipo == 2 else 'a'
    etiqueta_x2 = 'd' if guia_tipo == 2 else 'a'    

    print(f"\nFWHM X: {fwhm_x}")
    print(f"Longitud {etiqueta_x1}: {fwhm_start_to_max_x}")
    print(f"Longitud {etiqueta_x2}: {fwhm_max_to_end_x}")

    # Estimaciones iniciales más robustas
    initial_amp = df['X Value [%]'].max()
    initial_mu = df['Pos X [µm]'][df['X Value [%]'].idxmax()]
    initial_sigma = (df['Pos X [µm]'].max() - df['Pos X [µm]'].min()) / 6  # Suposición basada en la dispersión de los datos

    # Ajuste gaussiano para X
    try:
        popt_x, pcov_x = curve_fit(gaussiana, df['Pos X [µm]'].values, df['X Value [%]'].values,
                                   p0=[initial_amp, initial_mu, initial_sigma], maxfev=100000)
        
        # Gráfica original con ajuste gaussiano
        plt.figure(figsize=(12, 6))
        plt.plot(df['Pos X [µm]'], df['X Value [%]'], 'b-', label='Datos Originales X')
        plt.plot(df['Pos X [µm]'], gaussiana(df['Pos X [µm]'], *popt_x), 'r--', label='Ajuste Gaussiano X')
        """plt.title('Ajuste Gaussiano para X')"""
        plt.xlabel('Distancia [µm] (X)')
        plt.ylabel('Intensidad Normalizada [%]')
        
        plt.plot([df.loc[start_x, 'Pos X [µm]'], df.loc[max_x_index, 'Pos X [µm]']], 
                 [half_max_x, half_max_x], color='g', linestyle='-', label=etiqueta_x1)
        plt.plot([df.loc[max_x_index, 'Pos X [µm]'], df.loc[end_x, 'Pos X [µm]']], 
                 [half_max_x, half_max_x], color='black', linestyle='-', label=etiqueta_x2)
        
        plt.legend()
        plt.show()

        # Calcula el FWHM basado en el ajuste gaussiano
        fwhm_gauss_x = 2.355 * popt_x[2]
        fwhm_start_x = popt_x[1] - fwhm_gauss_x / 2
        fwhm_end_x = popt_x[1] + fwhm_gauss_x / 2
        print(f"\nFWHM para X después del ajuste gaussiano: {fwhm_gauss_x:.2f}")
        print(f"Longitud {etiqueta_x1}: {fwhm_start_x - popt_x[1]:.2f}")
        print(f"Longitud {etiqueta_x2}: {fwhm_end_x - popt_x[1]:.2f}")
    except RuntimeError as e:
        print(f"No se pudo ajustar la curva gaussiana: {e}")

    # Ajuste gaussiano para Y
    initial_amp_y = df['Y Value [%]'].max()
    initial_mu_y = df['Pos Y [µm]'][df['Y Value [%]'].idxmax()]
    initial_sigma_y = (df['Pos Y [µm]'].max() - df['Pos Y [µm]'].min()) / 6  # Suposición basada en la dispersión de los datos

    try:
        popt_y, pcov_y = curve_fit(gaussiana, df['Pos Y [µm]'].values, df['Y Value [%]'].values,
                                   p0=[initial_amp_y, initial_mu_y, initial_sigma_y], maxfev=100000)
        
        # Gráfica original con ajuste gaussiano
        plt.figure(figsize=(12, 6))
        plt.plot(df['Pos Y [µm]'], df['Y Value [%]'], 'b-', label='Datos Originales Y')
        plt.plot(df['Pos Y [µm]'], gaussiana(df['Pos Y [µm]'], *popt_y), 'r--', label='Ajuste Gaussiano Y')
        """plt.title('Ajuste Gaussiano para Y')"""
        plt.xlabel('Distancia [µm] (Y)')
        plt.ylabel('Intensidad Normalizada [%]')
        
        fwhm_y, start_y, end_y, half_max_y, max_y_index = calcular_fwhm_y(df, 'Y Value [%]', 'Pos Y [µm]')
        
        #etiqueta_y1 = 'd' if guia_tipo == 2 else 'a'
        #etiqueta_y2 = 'd' if guia_tipo == 2 else 'a'

        etiqueta_y1 = 'e' if guia_tipo == 2 else 'b'
        etiqueta_y2 = 'f' if guia_tipo == 2 else 'c'
        
        plt.plot([df.loc[start_y, 'Pos Y [µm]'], df.loc[max_y_index, 'Pos Y [µm]']], 
                 [half_max_y, half_max_y], color='g', linestyle='-', label=etiqueta_y1)
        plt.plot([df.loc[max_y_index, 'Pos Y [µm]'], df.loc[end_y, 'Pos Y [µm]']], 
                 [half_max_y, half_max_y], color='black', linestyle='-', label=etiqueta_y2)
        
        plt.legend()
        plt.show()

        fwhm_start_to_max_y = df.loc[max_y_index, 'Pos Y [µm]'] - df.loc[start_y, 'Pos Y [µm]']
        fwhm_max_to_end_y = df.loc[end_y, 'Pos Y [µm]'] - df.loc[max_y_index, 'Pos Y [µm]']
        print(f"\nFWHM Y: {fwhm_y}")
        print(f"Longitud {etiqueta_y1}: {fwhm_start_to_max_y}")
        print(f"Longitud {etiqueta_y2}: {fwhm_max_to_end_y}")

        # Calcula el FWHM basado en el ajuste gaussiano
        fwhm_gauss_y = 2.355 * popt_y[2]
        fwhm_start_y = popt_y[1] - fwhm_gauss_y / 2
        fwhm_end_y = popt_y[1] + fwhm_gauss_y / 2
        print(f"\nFWHM para Y después del ajuste gaussiano: {fwhm_gauss_y:.2f}")
        print(f"Longitud {etiqueta_y1}: {fwhm_start_y - popt_y[1]:.2f}")
        print(f"Longitud {etiqueta_y2}: {fwhm_end_y - popt_y[1]:.2f}")
    except RuntimeError as e:
        print(f"No se pudo ajustar la curva gaussiana: {e}")

    # Graficamos los pulsos para X con alisamiento
    x_smooth = savgol_filter(df['X Value [%]'], window_length=51, polyorder=3)
    plt.figure(figsize=(12, 6))
    plt.plot(df['Pos X [µm]'], x_smooth, label='Datos del Pulso X')
    plt.title('Perfil X')
    plt.xlabel('Distancia [µm]')
    plt.ylabel('Intensidad Normalizada [%]')
    
    plt.plot([df.loc[start_x, 'Pos X [µm]'], df.loc[max_x_index, 'Pos X [µm]']], 
             [half_max_x, half_max_x], color='g', linestyle='-', label=etiqueta_x1)
    plt.plot([df.loc[max_x_index, 'Pos X [µm]'], df.loc[end_x, 'Pos X [µm]']], 
             [half_max_x, half_max_x], color='r', linestyle='-', label=etiqueta_x2)
    
    plt.grid(True)
    plt.legend()
    plt.show()

    # Graficamos los pulsos para Y con alisamiento
    y_smooth = savgol_filter(df['Y Value [%]'], window_length=51, polyorder=3)
    plt.figure(figsize=(12, 6))
    plt.plot(df['Pos Y [µm]'], y_smooth, label='Datos del Pulso Y')
    plt.title('Perfil Y')
    plt.xlabel('Distancia [µm]')
    plt.ylabel('Intensidad Normalizada [%]')
    
    plt.plot([df.loc[start_y, 'Pos Y [µm]'], df.loc[max_y_index, 'Pos Y [µm]']], 
             [half_max_y, half_max_y], color='g', linestyle='-', label=etiqueta_y1)
    plt.plot([df.loc[max_y_index, 'Pos Y [µm]'], df.loc[end_y, 'Pos Y [µm]']], 
             [half_max_y, half_max_y], color='r', linestyle='-', label=etiqueta_y2)
    
    plt.grid(True)
    plt.legend()
    plt.show()

# Configuramos el Tkinter para el diálogo de selección de archivos
root = tk.Tk()
root.withdraw() 

# Abrimos el diálogo para seleccionar un archivo de texto
file_path_new = filedialog.askopenfilename(
    title="Selecciona un archivo",
    filetypes=[("Archivos de texto", "*.txt")]
)

root.destroy()  

if file_path_new:
    guia_tipo = int(input("Ingrese 1 para fibra óptica o 2 para guía de onda: "))
    num_picos_x = int(input("Ingrese el número de picos en la señal X: "))
    procesar_y_graficar(file_path_new, num_picos_x, guia_tipo)
else:
    print("No se seleccionó ningún archivo.")
