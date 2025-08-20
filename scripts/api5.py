import requests
import certifi
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Función para obtener datos de la API
def obtener_datos(desde, hasta):
    #url = f"https://api.bcra.gob.ar/estadisticas/v3.0/monetarias/1/{desde}/{hasta}"
    url = f"https://api.bcra.gob.ar/estadisticas/v3.0/monetarias/1?desde={desde}&hasta={hasta}"

    response = requests.get(url, verify=False)
    #response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Error: {response.status_code}")
        return []

# Obtener datos para 2022 y 2023
datos_2022 = obtener_datos('2022-01-01', '2022-12-31')
datos_2023 = obtener_datos('2023-01-01', '2023-12-31')
datos_2024 = obtener_datos('2024-01-01', '2024-12-31')

# Obtener datos para el año actual (desde enero hasta hoy)
hoy = datetime.today().strftime('%Y-%m-%d')
hora_actual = datetime.now().strftime('%H:%M:%S')
datos_actuales = obtener_datos(f'{datetime.today().year}-01-01', hoy)
print(hoy)
# Crear DataFrames con los datos
df_2022 = pd.DataFrame(datos_2022)
df_2023 = pd.DataFrame(datos_2023)
df_2024 = pd.DataFrame(datos_2024)
df_actuales = pd.DataFrame(datos_actuales)

# Convertir la columna 'fecha' a datetime
df_2022['fecha'] = pd.to_datetime(df_2022['fecha'])
df_2023['fecha'] = pd.to_datetime(df_2023['fecha'])
df_2024['fecha'] = pd.to_datetime(df_2024['fecha'])
df_actuales['fecha'] = pd.to_datetime(df_actuales['fecha'])
print(df_actuales.tail(10))
# Crear el gráfico
fig = go.Figure()

# Añadir la línea de datos 2022
fig.add_trace(go.Scatter(
    x=df_2022['fecha'],
    y=df_2022['valor'],
    mode='lines',
    name='Reservas Internacionales 2022',
    line=dict(color='royalblue', width=4),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))

# Añadir la línea de datos 2023
fig.add_trace(go.Scatter(
    x=df_2023['fecha'],
    y=df_2023['valor'],
    mode='lines',
    name='Reservas Internacionales 2023',
    line=dict(color='green', width=4),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=df_2024['fecha'],
    y=df_2024['valor'],
    mode='lines',
    name='Reservas Internacionales 2023',
    line=dict(color='yellow', width=4),
    hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
))
# Añadir la línea de datos actuales
fig.add_trace(go.Scatter(
    x=df_actuales['fecha'],
    y=df_actuales['valor'],
    mode='lines',
    name=f'Reservas Internacionales {datetime.today().year}',
    line=dict(color='orange', width=4, dash='dash'),
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
# fig.update_xaxes(
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label='1m', step='month', stepmode='backward'),
#             dict(count=6, label='6m', step='month', stepmode='backward'),
#             dict(step='all')
#         ])
#     ),
#     rangeslider=dict(visible=True),
#     type='date'
# )
# fig.add_annotation(
#     text="Fuente: API BCRA. Datos obtenidos mediante requests.",
#     xref='paper', yref='paper',
#     x=0.5, y=-0.1,
#     showarrow=False,
#     font=dict(size=10, color="grey"),
#     align='center'
# )
# Configurar el layout del gráfico
fig.update_layout(
    title='Plot - Evolución de las Reservas Internacionales',
    xaxis_title='Fecha',
    yaxis_title='Valor',
    template='plotly_white',
    hovermode='x unified'
)

# Generar el gráfico como un objeto HTML
plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

# Crear el HTML final con el encabezado, gráfico y pie de página
header = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gráfico de Reservas Internacionales</title>
</head>
<body>
    <h1>Ejemplo de uso API BCRA</h1>
    <h2>Generado el {fecha_hora}</h2>
"""

footer = """
    <footer>
        <p style="font-size: small; color: gray;">Source: API BCRA</p>
    </footer>
</body>
</html>
"""

# Insertar el gráfico en el cuerpo del HTML
html_content = header.format(fecha_hora=datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + plot_html + footer

# Guardar el contenido final en un archivo HTML
with open('docs/index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)
