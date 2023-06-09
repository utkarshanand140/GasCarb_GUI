import streamlit as st
import streamlit_authenticator as stauth
import yaml

# hashed_passwords = stauth.Hasher(['123', '456']).generate()
# print(hashed_passwords)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('You are logged in')

    st.number_input("Pick a number",0.0, 100.0)
elif st.session_state["authentication_status"] is False:
    st.error('Username or Password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
