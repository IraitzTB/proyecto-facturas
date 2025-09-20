import streamlit as st
import streamlit_authenticator as stauth

from facturas import parse_invoice, check_folder, save_invoice_for_user, store_json

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

import yaml
from yaml.loader import SafeLoader

with open("app/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get("authentication_status"):
    authenticator.logout()
    st.write(f"Welcome *{st.session_state.get('name')}*")

    check_folder(st.session_state.username)

    # Upload flow (protected)
    uploaded_file = st.file_uploader(
        "Upload an invoice (PDF)",
        type=["pdf"],
    )

    if uploaded_file is not None:
        # add username to stored data
        save_path = save_invoice_for_user(uploaded_file, st.session_state.username)
        if uploaded_file.type == "application/pdf":
            pdf = uploaded_file.read()

            result = parse_invoice(pdf, uploaded_file.name)
            # store_json(json_output, st.session_state.username)
            st.success(f"Invoice parsed and saved to {save_path}")
            st.json(result.data)
        else:
            st.write("Not implemented yet")

elif st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password")
