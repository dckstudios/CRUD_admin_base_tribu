import streamlit as st




def login():
    st.title("Plataforma de control de usuarios i empresas de tribu.")
    st.write("Por favor, inicie sesión para continuar.")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    
    if st.button("Iniciar sesión"):
        if username == "admin" and password == "admin":
            st.success("Has iniciado sesión como admin.")
            st.session_state["logged_in"] = True
            
            if st.button("Empezar"):
                st.experimental_set_query_params(logged_in=True)
        else:
            st.error("Usuario o contraseña incorrectos.")



def main():
    if st.session_state.get("logged_in"):
        st.title(f"Bienvenido a la Plataforma de control de usuarios i empresas de tribu.")

        # Agregar un botón de cierre de sesión
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.logged_in = False
            st.success("Has cerrado sesión exitosamente.")
            st.rerun()
            return  # Salir de la función main después de cerrar sesión
    else:
        login()

















if __name__ == "__main__":
    main()
