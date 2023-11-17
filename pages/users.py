import streamlit as st
from sqlalchemy import create_engine, Boolean,text, Date, select, distinct, MetaData, Table, Column, Integer, String, insert, JSON
import pandas as pd
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def check_authenticated():
    #if not st.session_state.get("logged_in"):
    #    st.warning("Por favor, inicia sesión para acceder a esta página.")
    #    st.stop()
    return True


# Read the DATABASE_URI from the .env file
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

engine = create_engine(db_uri)

# Create the "user" table
metadata = MetaData()
metadata.create_all(engine)


def connect_to_db():
    try:
        engine = create_engine(db_uri)
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        st.stop()

# Function to fetch data from the database based on filter criteria
def fetch_users_data():
    conn = connect_to_db()
    query = 'SELECT * FROM "user"'
    try:
        data = pd.read_sql(query, conn)
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error fetching and displaying filtered data: {e}")
    finally:
        conn.close()

def page_users():
    check_authenticated()
    if st.sidebar.button("Cerrar sesión"):
                st.session_state.logged_in = False
                st.success("Has cerrado sesión exitosamente.")
                st.rerun()

    st.title("Users tribu:")

    if st.button("Fetch and Display Users"):
        fetch_users_data()

    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Delete a User")

    del_user = st.text_input("Select the user email that you want to delete:")

    if st.button("Delete User"):
        with engine.connect() as connection:
            # Delete the company from the table
            delete_user = text(f'DELETE FROM "user" WHERE email = \'{del_user}\'')
            connection.execute(delete_user)
            connection.commit()
            st.success('User deleted successfully!')


    ####################################
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Add a new user")
    # Add a new company
    email = st.text_input('Email')
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    password = st.text_input('Password', type="password")
    empresa_id = st.text_input('Empresa ID')
    trial = st.checkbox('Trial')



    if st.button("Add User"):
        data = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'user_metadata': {},
            'empresa_id': int(empresa_id),
            'trial': trial,
        }
        print(data)

        json_data = json.dumps(data)
        print('json data',json_data)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        api_url = "https://pre-xavinibe.azurewebsites.net/auth/register"
        #api_url = 'http://127.0.0.1:5000/auth/register'

        response = requests.post(api_url, headers=headers, data=json_data)
        #print('response: ', response)
        #print('response.text: ', response.text)
        if response.status_code == 201:
            st.success('User added successfully!')
            #user_data = response.json()
            #st.json(user_data)
        else:
            st.error("Error in adding user to the database.")
            st.error(response.text)

    ####################################
    # update a user
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Update a user")
    st.subheader("Todos los campos menos los checkbox si los dejas en blanco no cambian.")
    # Select the user to update
    update_user_email = st.text_input("Select the user email you want to update:")
    # Input fields for the updated information
    updated_email = st.text_input('Updated Email')
    updated_first_name = st.text_input('Updated First Name')
    updated_last_name = st.text_input('Updated Last Name')
    updated_empresa_id = st.text_input('Updated Empresa ID')
    updated_trial = st.checkbox('Trial, if not selected equal to False.')
    update_active = st.checkbox('Active, if not selected equal to False.')

    if st.button('Update User'):
        with engine.connect() as connection:
            # Select the user to update
            query = text(f'SELECT * FROM "user" WHERE email = \'{update_user_email}\'')
            result = connection.execute(query)
            existing_user = result.fetchone()
            #print('existing_user: ', existing_user)
            #print('existing_user.trial: ', existing_user.trial)
            if existing_user:
                # Update the user in the table
                if updated_trial != "":
                    updated_email_q = f"""email = '{updated_email}',"""
                else:
                    updated_email_q = ""
                
                if updated_first_name != "":
                    updated_first_name_q = f"""first_name = '{updated_first_name}',"""
                else:
                    updated_first_name_q = ""
                
                if updated_last_name != "":
                    updated_last_name_q = f"""last_name = '{updated_last_name}',"""
                else:   
                    updated_last_name_q = ""
                
                if updated_empresa_id != "":
                    updated_empresa_id_q = f"""empresa_id = '{updated_empresa_id}',"""
                else:
                    updated_empresa_id_q = ""

                if updated_trial != existing_user.trial:
                    updated_trial_q = f"""trial = '{updated_trial}',"""
                else:
                    updated_trial_q = ""
                
                if update_active != existing_user.active:
                    update_active_q = f"""active = '{update_active}',"""
                else:
                    update_active_q = ""

                query_formation  = f"""
                    UPDATE "user"
                    SET {updated_email_q} 
                    {updated_first_name_q}
                    {updated_last_name_q}
                    {updated_empresa_id_q}
                    {updated_trial_q}
                    {update_active_q}
                    WHERE email = '{update_user_email}'
                """
                # delete last , 
                query_formation =  query_formation.rsplit(',', 1)
                query_formation = query_formation[0] + query_formation[1]
                #print('query_formation: ', query_formation)
                update_query = text(query_formation)
                connection.execute(update_query)
                connection.commit()
                st.success(f"User '{update_user_email}' updated successfully!")
            else:
                st.error("User does not exist!")

page_users()