# Sistema para medir pérdidas de acoplamiento entre guías de onda

Este repositorio contiene el código desarrollado para mi tesis de Maestría en Ciencias Aplicadas titulada:

**“Implementación de un sistema para la medición de pérdidas de acoplamiento entre guías de onda con diferente geometría”**  
**Autor:** Guillermo Márquez Rodríguez  
**Universidad Autónoma de San Luis Potosí (UASLP)**

El proyecto implementa un sistema óptico y computacional para caracterizar perfiles de haz y estimar pérdidas de acoplamiento entre fibras ópticas y guías de onda fabricadas mediante intercambio iónico o deposición polimérica.

---

## 🔬 Objetivo del proyecto

Desarrollar un método preciso y reproducible para medir pérdidas de acoplamiento entre:

- Fibra óptica monomodo  
- Guías de onda canal fabricadas por intercambio iónico  
- Guías de onda poliméricas  

El método se basa en:

1. **Adquisición experimental del perfil 2D del haz** mediante un analizador THORLABS.  
2. **Procesamiento computacional** en Python usando:  
   - Cálculo del *Full Width at Half Maximum* (FWHM)  
   - Ajustes gaussianos  
   - Extracción de parámetros geométricos del modo  
3. **Cálculo del coeficiente de acoplamiento η** entre dos guías mediante la teoría modal.  
4. **Estimación de pérdidas de acoplamiento** en decibeles.

---

## 📁 Estructura del repositorio

coupling-loss-waveguides/
│
├── code/
│ ├── ancho_del_pulso_EX.py
│ ├── coeficiente_de_acoplamiento_EX.py
│ └── .keep
│
├── docs/
│ ├── tesis_Guillermo_Marquez.pdf
│ └── .keep
│
├── requirements.txt
└── README.md

---

## 🧠 Descripción de los scripts

### 📌 `ancho_del_pulso_EX.py`
Script que procesa los datos del analizador de haz:

- Lee archivos `.txt` generados por el equipo  
- Calcula FWHM en los ejes X e Y  
- Realiza ajustes gaussianos utilizando `scipy.optimize.curve_fit`  
- Visualiza perfiles experimentales vs. ajuste  
- Extrae parámetros modales necesarios para el cálculo de pérdidas  

Incluye una interfaz gráfica mediante Tkinter para seleccionar archivos.

---

### 📌 `coeficiente_de_acoplamiento_EX.py`
Script que implementa las ecuaciones para:

- Calcular el coeficiente de acoplamiento `η`  
- Calcular pérdidas por acoplamiento en decibeles mediante:

\[
P_a = -10 \log_{10}(\eta)
\]

El script solicita los valores geométricos obtenidos del código anterior (a, b, c, d, e, f) y entrega valores numéricos de η y Pa.

---

## 🧪 Instalación de dependencias

Ejecutar:

```bash
pip install -r requirements.txt

Ejecución del código
Cálculo de FWHM y ajustes gaussianos:
python3 code/ancho_del_pulso_EX.py
El script solicitará un archivo de datos .txt.

Cálculo de pérdidas de acoplamiento:
python3 code/coeficiente_de_acoplamiento_EX.py
El programa pedirá los parámetros para realizar el cálculo.

Documento completo de la tesis
La versión PDF de la tesis se encuentra en:
/docs/tesis_Guillermo_Marquez.pdf
Incluye:
Fabricación de guías de onda (fotolitografía e intercambio iónico)
Metodología experimental
Montaje óptico completo
Procesamiento con Python
Análisis de resultados y eficiencia modal
Propuestas de mejora (automatización y ML para perfiles multimodo)

Propósito académico
Este repositorio forma parte de mi portafolio académico para aplicar a un Doctorado en Ciencias Computacionales, con intereses en:
Esteganografía
Fotónica aplicada
Procesamiento digital de señales ópticas
Optical interconnects y waveguide engineering
Machine learning para análisis de perfiles modales

Autor
Guillermo Márquez Rodríguez
Ingeniero Físico · Maestro en Ciencias Aplicadas
