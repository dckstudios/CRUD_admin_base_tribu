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

# Create the "tribu_services" table
metadata = MetaData()
tribu_services_table = Table('tribu_services', metadata,
                     Column('service_id', Integer, primary_key=True, autoincrement=True),
                     Column('name', String),
                     Column('platform_id', Integer),
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
    query = "SELECT * FROM tribu_services"

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
            
    st.title("Tribu Services:")

    if st.button("Fetch and Display Data"):
        fetch_and_display_data()
    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Delete a service")

    del_tribu_service = st.text_input("Select the service you want to delete:")

    if st.button("Delete service"):
        with engine.connect() as connection:
            query = text(f'SELECT * FROM "tribu_services" WHERE name = \'{del_tribu_service}\'')
            result = connection.execute(query)
            existing_user = result.fetchone()
            service_id = existing_user[0]
            delete_from_usage=text(f'DELETE FROM "usage" WHERE service_id = \'{str(service_id)}\'')
            connection.execute(delete_from_usage)
            # Delete the service from the table
            delete_tribu_service=text(f'DELETE FROM "tribu_services" WHERE service_id = \'{str(service_id)}\'')
            connection.execute(delete_tribu_service)
            connection.commit()
            st.success('Service deleted successfully!')

    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Add a new service")
    # Add a new service
    nombre_tribu_service = st.text_input('Service Name')
    platform_tribu_service = st.text_input('Platform Id')

    if st.button('Add Service'):
        with engine.connect() as connection:
            # Insert the new service into the table
            new_service_data = {
                'name': nombre_tribu_service,
                'platform_id':platform_tribu_service,
            }
            connection.execute(insert(tribu_services_table).values(new_service_data))
            connection.commit()
            st.success('tribu service added successfully!')


    ####################################
    # update a service
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Update a service")
    st.subheader("Los campos que dejes en blanco no cambian.")
    # Select the service to update
    update_service_name = st.text_input("Select the service name you want to update:")


    # Input fields for the updated information
    updated_nombre_service = st.text_input('Updated service Name')
    update_platform_id = st.text_input("Updated the platform_id")

    if st.button('Update Service'):
        with engine.connect() as connection:
            # Check if the platform exists
            query = text(f"SELECT * FROM tribu_services WHERE name = '{update_service_name}'")
            result = connection.execute(query)
            existing_service = result.fetchone()

            if existing_service:
                if updated_nombre_service != "":
                    updated_nombre_service_q = f"""name = '{updated_nombre_service}',"""
                else:
                    updated_nombre_service_q = ""
            if existing_service:
                if update_platform_id != "":
                    update_platform_id_q = f"""platform_id = '{update_platform_id}',"""
                else:
                    update_platform_id_q = ""   

                query_formation  = f"""
                    UPDATE tribu_services
                    SET {updated_nombre_service_q}
                    {update_platform_id_q}
                    WHERE name = '{update_service_name}'
                """
                # delete last , 
                query_formation =  query_formation.rsplit(',', 1)
                query_formation = query_formation[0] + query_formation[1]

                #print('query_formation: ', query_formation)
                update_query = text(query_formation)
                connection.execute(update_query)
                connection.commit()
                st.success(f"Tribu Service '{update_service_name}' updated successfully!")
            else:
                st.error(f"Tribu Service '{update_service_name}' not found.")


page_companies()