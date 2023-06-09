import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode

# hashed_passwords = stauth.Hasher(['123', '456']).generate()
# print(hashed_passwords)


hide_default_format = """
       <style>
       #MainMenu {visibility: ; }
       footer {visibility: hidden;}
       </style>
       """

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# st.set_page_config(layout="wide")
st.set_page_config(page_title="Gas Carburize App")
st.markdown(hide_default_format, unsafe_allow_html=True)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


page_header = st.markdown("<h1 style='text-align: center; color: white;'>Welcome to GasCarb Online!</h1>", unsafe_allow_html=True)

name, authentication_status, username = authenticator.login('Login', 'main')
forgot_psswd = """
<a style='text-align: center;' href="mailto:govindg_at_iisc.ac.in?subject=Forgot%20Password%20Request" target="_blank">Forgot password?</a>
"""
psswd = st.markdown(forgot_psswd, unsafe_allow_html=True)


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    psswd.empty()
    page_header.empty()
    st.write(f'Welcome *{st.session_state["name"]}*')

    tab1, tab2, tab3, tab4 = st.tabs(["Experimental Data", "Computational Parameters","Graphs","Contours"])

    with tab1:

    

        with st.sidebar:
            st.header('Input Process Parameters')
            st.number_input("Initial Carbon Concentration in sample (Wt%C)",0.0,10.0,0.15)
            st.number_input("Carburizing Temperature (K)",0,2000,1200)
            st.number_input("Activation Time (hours)",0.0,100.0,2.0)
            st.number_input("Diffusion Time (hours)",0.0,100.0,1.5)
            st.number_input("Carbon Potential of atmosphere - activation period (Wt%C)",0.0,100.0,1.2)
            st.number_input("Carbon Potential of atmosphere - diffusion period (Wt%C)",0.0,100.0,0.8)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.header('Dimensions')
            dimension = st.radio('Choose Dimension',['1-Dimension','2-Dimension'])

            if dimension=='1-Dimension':
                st.selectbox('Pick type of 1-Dimension',['1-D Cartesian','1-D Cyllindrical','1-D Spherical'])
            else:
                st.selectbox('Pick type of 2-Dimension',['2-D Cartesian','2-D Cyllindrical','2-D Spherical'])

        
        
        st.header('Enter Experimental Data')
        df = pd.DataFrame({"concentration": [0,0,0,0,0,0,0,0,0,0], "distance": [0,0,0,0,0,0,0,0,0,0]})

        col1, col2 = st.columns(2)
        
        grid_options = {
            "columnDefs": [
                {
                    "headerName": "Concentration (in Wt%)",
                    "field": "concentration",
                    "editable": True,
                },
                {
                    "headerName": "Distance (in mm)",
                    "field": "distance",
                    "editable": True,
                },
            ],
        }

        with col1:
            grid_return = AgGrid(data=df, gridOptions=grid_options,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS )
            new_df = grid_return["data"]

            
        with col2:
            st.number_input("Hours",0,100)
            st.number_input("Temperature",0,100)
            st.radio('',['Boost Period','Diffusion Period'])
            st.button('Execute Process')

    with tab2:
        st.header('Enter the Computational Model Values')
        st.number_input("Time (time scale) [Boost & Diffusion Period]",0,2000,1000)
        st.number_input("Grids (Input grid poitns)",0,1000,100)
        st.number_input("Distance from surface of sample (mm)",0,100,10)

    


    
elif st.session_state["authentication_status"] is False:
    st.error('Username or Password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your Username and Password')


footer="""<style>
a:link , a:visited{
color: lightblue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>© Copyright <a style=' text-align: center;' href="https://materials.iisc.ac.in/~govindg/" target="_blank">Govind S. Gupta</a> . All Rights Reserved.</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
