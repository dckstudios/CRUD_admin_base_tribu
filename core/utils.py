import streamlit as st
from pathlib import Path
import psycopg2


def conection_sql (statement):
    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=st.secrets['HOST'],
        port=st.secrets['PORT'],
        database=st.secrets['DATABASE'],
        user=st.secrets['USER'],
        password=st.secrets['PASSWORD']
    )

    # Crear un cursor
    cur = conn.cursor()


    try:
        # Ejecutar la consulta SQL
        cur.execute(statement)

        # Obtener los resultados
        results = cur.fetchall()

        # Hacer algo con los resultados
        result =[]
        for row in results:
            result.append(row)
        print(result)
        return (result)

    except psycopg2.Error as e:
        print("Error al ejecutar la consulta SQL:", e)
        return ("Error al ejecutar la consulta SQL")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cur.close()
        conn.close()