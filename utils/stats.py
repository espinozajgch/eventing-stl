import pandas as pd

def resumen_acciones_por_minuto(df_sb, df_op, df_ws):
    # Añadir columna Minute y Provider
    df_sb['Minute'] = df_sb['StartTime'] // 60
    df_sb['Provider'] = 'StatsBomb'

    df_op['Minute'] = df_op['StartTime'] // 60
    df_op['Provider'] = 'Opta'

    df_ws['Minute'] = df_ws['StartTime'] // 60
    df_ws['Provider'] = 'Wyscout'

    # Unir todos los DataFrames
    df_all = pd.concat([df_sb, df_op, df_ws])

    # Agrupar por minuto y proveedor
    grouped = df_all.groupby(['Provider', 'Minute']).size().reset_index(name='Acciones')

    # Resumen estadístico por proveedor
    summary = grouped.groupby('Provider')['Acciones'].describe().round(2)

    # Añadir columna con total de acciones por proveedor
    total_actions = grouped.groupby('Provider')['Acciones'].sum()
    summary['Acciones totales'] = total_actions

    # Renombrar columnas en español
    summary = summary.rename(columns={
        'count': 'Conteo',
        'mean': 'Media',
        'std': 'Desviación estándar',
        'min': 'Mínimo',
        '25%': 'Percentil 25',
        '50%': 'Mediana',
        '75%': 'Percentil 75',
        'max': 'Máximo'
    })

    return summary
