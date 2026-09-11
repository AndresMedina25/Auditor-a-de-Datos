import pandas as pd
import numpy as np

# ==========================================
# FASE 1: SIMULACIÓN DE DATOS CRUDOS
# (Generamos un Excel con respuestas de encuesta)
# ==========================================
def generar_datos_simulados():
    datos = {
        'ID_Encuesta': [1001, 1002, 1003, 1004, 1005, 1006],
        'Edad': [25, 12, np.nan, 45, 150, 30], 
        'Ocupacion': ['Ingeniero', 'Ingeniero', 'Estudiante', 'Médico', 'Desempleado', np.nan],
        'Trabaja_Actualmente': ['Sí', 'Sí', 'No', 'Sí', 'No', 'Sí'],
        'Ingresos_USD': [2000, 5000, 0, 4500, 0, 1500]
    }
    df_crudo = pd.DataFrame(datos)
    df_crudo.to_excel('datos_crudos_encuesta.xlsx', index=False)
    print("Archivo 'datos_crudos_encuesta.xlsx' generado con éxito.\n")

# ==========================================
# FASE 2: SCRIPT DE AUDITORÍA Y QA
# ==========================================
def ejecutar_qa_datos():
    print("Iniciando auditoría de calidad de datos...")
    
    # 1. Cargar la base de datos
    df = pd.read_excel('datos_crudos_encuesta.xlsx')
    
    # Columna para registrar los errores encontrados
    df['Fallas_QA'] = ""

    # --- REGLA DE QA 1: Datos obligatorios faltantes (Missings) ---
    columnas_obligatorias = ['Edad', 'Ocupacion']
    for col in columnas_obligatorias:
        # Detecta valores nulos (NaN)
        filtro_vacios = df[col].isnull()
        df.loc[filtro_vacios, 'Fallas_QA'] += f"[Dato faltante en: {col}] "

    # --- REGLA DE QA 2: Incongruencias lógicas (Cross-checking) ---
    # Incongruencia A: Menor de 18 años pero con profesión de nivel superior
    filtro_edad_profesion = (df['Edad'] < 18) & (df['Ocupacion'].isin(['Ingeniero', 'Médico']))
    df.loc[filtro_edad_profesion, 'Fallas_QA'] += "[Incongruencia: Menor de edad con profesión avanzada] "

    # Incongruencia B: Dice no trabajar, pero reporta ingresos mayores a 0
    filtro_ingresos = (df['Trabaja_Actualmente'] == 'No') & (df['Ingresos_USD'] > 0)
    df.loc[filtro_ingresos, 'Fallas_QA'] += "[Incongruencia lógica: No trabaja pero reporta ingresos] "

    # --- REGLA DE QA 3: Valores fuera de rango (Outliers) ---
    # La edad debe estar entre 18 y 99 años (asumiendo que es una encuesta para adultos)
    filtro_outliers = (df['Edad'] > 100) | (df['Edad'] < 0)
    df.loc[filtro_outliers, 'Fallas_QA'] += "[Alerta Outlier: Edad ilógica] "

    # 3. Filtrar y exportar el reporte
    # Nos quedamos solo con las filas que tienen algún mensaje de error
    df_errores = df[df['Fallas_QA'] != ""]
    
    if not df_errores.empty:
        # Guardamos el reporte QA en un nuevo Excel
        df_errores.to_excel('reporte_QA_inconsistencias.xlsx', index=False)
        print(f"Auditoría finalizada. Se encontraron {len(df_errores)} registros con errores.")
        print("Revisa el archivo generado: 'reporte_QA_inconsistencias.xlsx'")
    else:
        print("Auditoría finalizada. Los datos están 100% limpios.")

# Ejecución del programa
if __name__ == "__main__":
    generar_datos_simulados()
    ejecutar_qa_datos()