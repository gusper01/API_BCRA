import requests
import certifi
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Función para obtener datos de la API
def obtener_datos(desde, hasta):
    url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/1/{desde}/{hasta}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Error: {response.status_code}")
        return []

# Obtener datos para 2022 y 2023
datos_2022 = obtener_datos('2022-01-01', '2022-12-31')
datos_2023 = obtener_datos('2023-01-01', '2023-12-31')

# Obtener datos para el año actual (desde enero hasta hoy)
hoy = datetime.today().strftime('%Y-%m-%d')
datos_actuales = obtener_datos(f'{datetime.today().year}-01-01', hoy)

# Crear DataFrames con los datos
df_2022 = pd.DataFrame(datos_2022)
df_2023 = pd.DataFrame(datos_2023)
df_actuales = pd.DataFrame(datos_actuales)

# Convertir la columna 'fecha' a datetime
df_2022['fecha'] = pd.to_datetime(df_2022['fecha'])
df_2023['fecha'] = pd.to_datetime(df_2023['fecha'])
df_actuales['fecha'] = pd.to_datetime(df_actuales['fecha'])

# Crear el gráfico
fig = go.Figure()

# Añadir la línea de datos 2022
fig.add_trace(go.Scatter(
    x=df_2022['fecha'],
    y=df_2022['valor'],
    mode='lines',
    name='Reservas Internacionales 2022',
    line=dict(color='royalblue', width=2),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))

# Añadir la línea de datos 2023
fig.add_trace(go.Scatter(
    x=df_2023['fecha'],
    y=df_2023['valor'],
    mode='lines',
    name='Reservas Internacionales 2023',
    line=dict(color='green', width=2),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))

# Añadir la línea de datos actuales
fig.add_trace(go.Scatter(
    x=df_actuales['fecha'],
    y=df_actuales['valor'],
    mode='lines',
    name=f'Reservas Internacionales {datetime.today().year}',
    line=dict(color='orange', width=2, dash='dash'),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))

# Añadir anotaciones (ejemplo de fechas importantes)
# annotations = [
#     dict(x='2023-08-23', y=29004, xref='x', yref='y',
#          text='Aumento significativo', showarrow=True, arrowhead=2, ax=0, ay=-40),
#     dict(x='2023-07-31', y=24092, xref='x', yref='y',
#          text='Baja significativa', showarrow=True, arrowhead=2, ax=0, ay=-40)
# ]
# fig.update_layout(annotations=annotations)

# Añadir selector de rango de fechas
fig.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(step='all')
        ])
    ),
    rangeslider=dict(visible=True),
    type='date'
)

# Configurar el layout del gráfico
fig.update_layout(
    title='Plot - Evolución de las Reservas Internacionales',
    xaxis_title='Fecha',
    yaxis_title='Valor',
    template='plotly_white',
    hovermode='x unified'
)

# Guardar el gráfico en un archivo HTML
fig.write_html('docs/reservas_internacionales.html')

print("El gráfico se ha guardado como 'reservas_internacionales.html'")
