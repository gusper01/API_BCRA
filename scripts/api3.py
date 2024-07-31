import requests
import certifi
import plotly.graph_objects as go
import pandas as pd

# Parámetros de la solicitud
desde = '2023-01-01'  # Fecha de inicio (formato YYYY-MM-DD)
hasta = '2023-12-31'  # Fecha de fin (formato YYYY-MM-DD)

# URL de la API
url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/1/{desde}/{hasta}"

response = requests.get(url, verify=False)
# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener los datos en formato JSON
    data = response.json()['results']

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Convertir la columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Crear el gráfico
    fig = go.Figure()

    # Añadir la línea de datos
    fig.add_trace(go.Scatter(
        x=df['fecha'],
        y=df['valor'],
        mode='lines',
        name='Reservas Internacionales',
        line=dict(color='royalblue', width=2),
        hovertemplate='Fecha: %{x}<br>Valor: %{y:.2f}<extra></extra>'
    ))

    # Añadir anotaciones (ejemplo de fechas importantes)
    annotations = [
        dict(x='2023-08-23', y=29004, xref='x', yref='y',
             text='Aumento significativo', showarrow=True, arrowhead=2, ax=0, ay=-40),
        dict(x='2023-07-31', y=24092, xref='x', yref='y',
             text='Baja significativa', showarrow=True, arrowhead=2, ax=0, ay=-40)
    ]
    fig.update_layout(annotations=annotations)

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
        title='Evolución de las Reservas Internacionales',
        xaxis_title='Fecha',
        yaxis_title='Valor',
        template='plotly_white',
        hovermode='x unified'
    )

    # Guardar el gráfico en un archivo HTML
    fig.write_html('reservas_internacionales_profesional.html')

    print("El gráfico se ha guardado como 'reservas_internacionales_profesional.html'")
else:
    print(f"Error: {response.status_code}")
