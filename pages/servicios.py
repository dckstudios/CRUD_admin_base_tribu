import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from resources.services_resources import get_all_services_with_platform
load_dotenv()
def check_authenticated():
    #if not st.session_state.get("logged_in"):
    #    st.warning("Por favor, inicia sesión para acceder a esta página.")
    #    st.stop()
    return True
# Configura la aplicación Streamlit

st.title("Lista de Servicios con Plataforma")

# Crea una tabla en Streamlit para mostrar los resultados
table_data = []
services_with_platform = get_all_services_with_platform()
df = pd.DataFrame([(service.service_id, service.name, platform.name) for service, platform in services_with_platform], columns=["ID del Servicio", "Nombre del Servicio", "Nombre de la Plataforma"])

# Configurar paginación
page_size = 5
page_number = st.number_input("Selecciona la página", 1, value=1)

# Calcular el índice de inicio y fin para la paginación
start_idx = (page_number - 1) * page_size
end_idx = start_idx + page_size

# Mostrar la tabla paginada
st.table(df.iloc[start_idx:end_idx])


