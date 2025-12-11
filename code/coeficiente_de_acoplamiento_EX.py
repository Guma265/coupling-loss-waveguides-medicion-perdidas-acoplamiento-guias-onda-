import math

def optimized_calculo_eta(a, b, c, d, e, f):
    """
    Calcula el coeficiente de acoplamiento (η) entre dos guías de onda o fibras ópticas.
    
    Parámetros:
    a, b, c, d, e, f (float): Son los parámetros de las guías de onda.
                            

    Retorno:
    eta (float): El coeficiente de acoplamiento, que indica qué tan bien se acoplan las guías.
    """
    
    # Calcular los términos intermedios con la suma de los inversos cuadrados.
    term1 = (1 / b**2 + 1 / e**2)**(-0.5)
    term2 = (1 / c**2 + 1 / f**2)**(-0.5)
    
    # Fórmula de η: se calcula utilizando los términos intermedios y los parámetros de entrada
    eta = (4 * (term1 + term2)**2) / (a * d * (b + c) * (e + f) * (1 / a**2 + 1 / d**2))
    
    return eta

def optimized_calculo_pa_db(eta):
    """
    Calcula las pérdidas por acoplamiento (P_a) en decibeles (dB) a partir del coeficiente de acoplamiento (η).
    
    Parámetros:
    eta (float): El coeficiente de acoplamiento previamente calculado.

    Retorno:
    pa_db (float): Las pérdidas por acoplamiento en decibeles (dB).
    """
    
    # Se utiliza la fórmula estándar de pérdidas por acoplamiento en decibeles: P_a[dB] = -10 * log10(eta)
    pa_db = -10 * math.log10(eta)
    
    return pa_db

def optimized_main():
    """
    Función principal que solicita los parámetros al usuario y calcula tanto el coeficiente de acoplamiento (η) 
    como las pérdidas por acoplamiento (P_a[dB]).
    
    Funcionalidad:
    1. Solicita al usuario que introduzca los seis parámetros: a, b, c, d, e, f.
    2. Llama a las funciones 'optimized_calculo_eta' y 'optimized_calculo_pa_db' para realizar los cálculos.
    3. Imprime el coeficiente de acoplamiento y las pérdidas por acoplamiento en dB.
    
    Excepciones:
    - Si el usuario introduce un valor no numérico, se captura el error y se muestra un mensaje.
    """
    
    try:
        # Solicitar los valores para los parámetros a, b, c, d, e, f al usuario.
        values = [float(input(f"Introduce el valor para {var}: ")) for var in "abcdef"]
        a, b, c, d, e, f = values

        # Calcular el coeficiente de acoplamiento (η).
        eta = optimized_calculo_eta(*values)
        
        # Calcular las pérdidas por acoplamiento en dB.
        pa_db = optimized_calculo_pa_db(eta)

        # Mostrar los resultados al usuario.
        print(f"El coeficiente de acoplamiento es de: {eta}")
        print(f"Las perdidas por acoplamiento son de: {pa_db} dB")
    
    except ValueError:
        # Captura el error si se introduce un valor no numérico.
        print("Error: Se introdujo un valor no válido.")

# Este bloque asegura que la función 'optimized_main' solo se ejecuta si el script se ejecuta directamente,
# y no cuando se importa como módulo en otro script.
if __name__ == "__main__":
    optimized_main()
