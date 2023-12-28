import psycopg2
import streamlit as st





def get_all_prompt_name():
    # Conectarse a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )
    # Crear un cursor
    cur = conn.cursor()

    # Crear una tabla "prompts" si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id serial PRIMARY KEY,
            text text,
            namespace text
        )
    """)

    cur.execute("SELECT namespace FROM prompts ")
    result = cur.fetchall()
    print(result)
    retrieved_text=""    
    if result:
        prompt_names = result
        prompt_names_list = [name[0] for name in prompt_names]
        retrieved_text = prompt_names_list
    else:
        retrieved_text = []

    conn.close()

    return retrieved_text


def get_current_prompt(namespace):
    namespace = namespace.lower()
    # Conectarse a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )
    # Crear un cursor
    cur = conn.cursor()

    # Crear una tabla "prompts" si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id serial PRIMARY KEY,
            text text,
            namespace text
        )
    """)

    cur.execute("SELECT text FROM prompts where namespace='"+namespace+"'")
    result = cur.fetchone()
    retrieved_text=""    
    if result:
        retrieved_text = result[0]
    conn.close()

    return retrieved_text

def save_update_prompt(input_text,namespace):
    namespace = namespace.lower()
    # Conectarse a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )
    # Crear un cursor
    cur = conn.cursor()
    cur.execute("SELECT text FROM prompts where namespace='"+namespace+"'")
    result = cur.fetchone()
    
    if result:
        # Si existe, actualizar el valor existente
        cur.execute("UPDATE prompts SET text = %s WHERE namespace = %s", (input_text,namespace))
        conn.commit()
        st.success(f"Prompt actualizado correctamente")
    else:
        # Si no existe, insertar un nuevo valor
        cur.execute("INSERT INTO prompts (text,namespace) VALUES (%s,%s)", (input_text,namespace))
        conn.commit()
        st.success(f"Prompt guardado correctamente")


    # Cerrar la conexión a la base de datos al final
    conn.close()


def save_create_prompt(input_text,namespace):
    # Conectarse a la base de datos PostgreSQL
    namespace = namespace.lower()
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )
    # Crear un cursor
    cur = conn.cursor()
    cur.execute("SELECT text FROM prompts where namespace='"+namespace+"'")
    result = cur.fetchone()
    
    if result:
        # Si existe, actualizar el valor existente        
        st.warning(f"El prompt ya Existe un prompt con eel nombre \"{namespace}\", intente con oun namespace diferente")
        conn.close()
    else:
        # Si no existe, insertar un nuevo valor
        cur.execute("INSERT INTO prompts (text,namespace) VALUES (%s,%s)", (input_text,namespace))
        conn.commit()
        print(cur.query)
        st.success(f"Prompt guardado correctamente")
        conn.close()

def delete_prompt(namespace):
    # Conectarse a la base de datos PostgreSQL
    namespace = namespace.lower()
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )
    # Crear un cursor
    cur = conn.cursor()
    cur.execute("DELETE FROM prompts WHERE namespace = %s", (namespace,))
    conn.commit()
    print(cur.query)
 
    conn.close()
    st.success(f"Prompt borrado correctamente")
  