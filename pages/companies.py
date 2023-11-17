import streamlit as st
from sqlalchemy import create_engine,text, select, distinct, MetaData, Table, Column, Integer, String, insert
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
def check_authenticated():
    #if not st.session_state.get("logged_in"):
    #    st.warning("Por favor, inicia sesión para acceder a esta página.")
    #    st.stop()
    return True

db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

engine = create_engine(db_uri)

# Create the "empresa" table
metadata = MetaData()
empresa_table = Table('empresa', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('nombre_empresa', String),
                     Column('direccion', String),
                     Column('poblacion', String),
                     Column('provincia', String),
                     Column('codigo_postal', String),
                     Column('pais', String),
                     Column('cif', String),
                     )
metadata.create_all(engine)

def connect_to_db():
    try:
        engine = create_engine(db_uri)
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        st.stop()

def fetch_and_display_data():
    conn = connect_to_db()
    query = "SELECT * FROM empresa"

    try:
        data = pd.read_sql(query, conn)
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error fetching and displaying data: {e}")
    finally:
        conn.close()

def page_companies():
    check_authenticated()
    if st.sidebar.button("Cerrar sesión"):
                st.session_state.logged_in = False
                st.success("Has cerrado sesión exitosamente.")
                st.rerun()
            
    st.title("Empresas tribu:")

    if st.button("Fetch and Display Data"):
        fetch_and_display_data()
    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Delete a company")

    del_company = st.text_input("Select the company you want to delete:")

    if st.button("Delete Company"):
        with engine.connect() as connection:
            # Delete the company from the table
            delete_company = text(f"DELETE FROM empresa WHERE nombre_empresa = '{del_company}'")
            connection.execute(delete_company)
            connection.commit()
            st.success('Company deleted successfully!')

    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Add a new company")
    # Add a new company
    nombre_empresa = st.text_input('Company Name')
    direccion = st.text_input('Address')
    poblacion = st.text_input('City')
    provincia = st.text_input('Province')
    codigo_postal = st.text_input('Postal Code')
    pais = st.text_input('Country')
    cif = st.text_input('CIF')

    if st.button('Add Company'):
        with engine.connect() as connection:
            # Insert the new company into the table
            new_company_data = {
                'nombre_empresa': nombre_empresa,
                'direccion': direccion,
                'poblacion': poblacion,
                'provincia': provincia,
                'codigo_postal': codigo_postal,
                'pais': pais,
                'cif': cif,
            }
            connection.execute(insert(empresa_table).values(new_company_data))
            connection.commit()
            st.success('Company added successfully!')


    ####################################
    # update a company
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Update a company")
    st.subheader("Los campos que dejes en blanco no cambian.")
    # Select the company to update
    update_company_name = st.text_input("Select the company name you want to update:")

    # Input fields for the updated information
    updated_nombre_empresa = st.text_input('Updated Company Name')
    updated_direccion = st.text_input('Updated Address')
    updated_poblacion = st.text_input('Updated City')
    updated_provincia = st.text_input('Updated Province')
    updated_codigo_postal = st.text_input('Updated Postal Code')
    updated_pais = st.text_input('Updated Country')
    updated_cif = st.text_input('Updated CIF')

    if st.button('Update Company'):
        with engine.connect() as connection:
            # Check if the company exists
            query = text(f"SELECT * FROM empresa WHERE nombre_empresa = '{update_company_name}'")
            result = connection.execute(query)
            existing_company = result.fetchone()

            if existing_company:
                if updated_nombre_empresa != "":
                    updated_nombre_empresa_q = f"""nombre_empresa = '{updated_nombre_empresa}',"""
                else:
                    updated_nombre_empresa_q = ""
                
                if updated_direccion != "":
                    updated_direccion_q = f"""direccion = '{updated_direccion}',"""
                else:
                    updated_direccion_q = ""
                
                if updated_poblacion != "":
                    updated_poblacion_q = f"""poblacion = '{updated_poblacion}',"""
                else:
                    updated_poblacion_q = ""
                
                if updated_provincia != "":
                    updated_provincia_q = f"""provincia = '{updated_provincia}',"""
                else:
                    updated_provincia_q = ""
                
                if updated_codigo_postal != "":
                    updated_codigo_postal_q = f"""codigo_postal = '{updated_codigo_postal}',"""
                else:
                    updated_codigo_postal_q = ""
                
                if updated_pais != "":
                    updated_pais_q = f"""pais = '{updated_pais}',"""
                else:
                    updated_pais_q = ""
                
                if updated_cif != "":
                    updated_cif_q = f"""cif = '{updated_cif}',"""
                else:
                    updated_cif_q = ""

                query_formation  = f"""
                    UPDATE empresa
                    SET {updated_nombre_empresa_q}
                    {updated_direccion_q}
                    {updated_poblacion_q}
                    {updated_provincia_q}
                    {updated_codigo_postal_q}
                    {updated_pais_q}
                    {updated_cif_q}
                    WHERE nombre_empresa = '{update_company_name}'
                """
                # delete last , 
                query_formation =  query_formation.rsplit(',', 1)
                query_formation = query_formation[0] + query_formation[1]

                #print('query_formation: ', query_formation)
                update_query = text(query_formation)
                connection.execute(update_query)
                connection.commit()
                st.success(f"Company '{update_company_name}' updated successfully!")
            else:
                st.error(f"Company '{update_company_name}' not found.")


page_companies()