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

# Create the "platform" table
metadata = MetaData()
platform_table = Table('tribu_platform', metadata,
                     Column('platform_id', Integer, primary_key=True, autoincrement=True),
                     Column('name', String),
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
    query = "SELECT * FROM tribu_platform"

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
            
    st.title("Platform tribu:")

    if st.button("Fetch and Display Data"):
        fetch_and_display_data()
    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Delete a platform")

    del_platform = st.text_input("Select the platform you want to delete:")

    if st.button("Delete Platform"):
        with engine.connect() as connection:
            # Delete the platform from the table
            delete_platform = text(f"DELETE FROM tribu_platform WHERE name = '{del_platform}'")
            connection.execute(delete_platform)
            connection.commit()
            st.success('Platform deleted successfully!')

    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Add a new platform")
    # Add a new platform
    nombre_platform = st.text_input('Platform Name')


    if st.button('Add Platform'):
        with engine.connect() as connection:
            # Insert the new platform into the table
            new_Platform_data = {
                'name': nombre_platform,

            }
            connection.execute(insert(platform_table).values(new_Platform_data))
            connection.commit()
            st.success('Platform added successfully!')


    ####################################
    # update a platform
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Update a platform")
    st.subheader("Los campos que dejes en blanco no cambian.")
    # Select the platform to update
    update_platform_name = st.text_input("Select the platform name you want to update:")

    # Input fields for the updated information
    updated_nombre_platform = st.text_input('Updated platform Name')


    if st.button('Update Platform'):
        with engine.connect() as connection:
            # Check if the platform exists
            query = text(f"SELECT * FROM tribu_platform WHERE name = '{update_platform_name}'")
            result = connection.execute(query)
            existing_platform = result.fetchone()

            if existing_platform:
                if updated_nombre_platform != "":
                    updated_nombre_platform_q = f"""name = '{updated_nombre_platform}',"""
                else:
                    updated_nombre_platform_q = ""
               

                query_formation  = f"""
                    UPDATE tribu_platform
                    SET {updated_nombre_platform_q}
                    WHERE name = '{update_platform_name}'
                """
                # delete last , 
                query_formation =  query_formation.rsplit(',', 1)
                query_formation = query_formation[0] + query_formation[1]

                #print('query_formation: ', query_formation)
                update_query = text(query_formation)
                connection.execute(update_query)
                connection.commit()
                st.success(f"Platform '{update_platform_name}' updated successfully!")
            else:
                st.error(f"Platform '{update_platform_name}' not found.")


page_companies()