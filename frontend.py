import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("One-Day Tour Planning Assistant")

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = st.text_input("Enter your User ID:")

user_id = st.session_state['user_id']

if user_id:
    with st.form("preferences_form"):
        city = st.text_input("City to visit", "Rome")
        date = st.date_input("Trip Date")
        start_time = st.text_input("Start Time", "09:00 AM")
        end_time = st.text_input("End Time", "06:00 PM")
        budget = st.number_input("Enter your budget ($)", 0, 1000, 100)
        interests = st.multiselect("Select your interests", ["Historical Sites", "Food", "Shopping"])
        starting_point = st.text_input("Starting Point", "City Center")
        submitted = st.form_submit_button("Save Preferences")

        if submitted:
            preferences = {
                "user_id": user_id,
                "city": city,
                "date": str(date),
                "start_time": start_time,
                "end_time": end_time,
                "interests": interests,
                "budget": budget,
                "starting_point": starting_point
            }
            response = requests.post(f"{BACKEND_URL}/collect_preferences/", json=preferences)
            if response.status_code == 200:
                st.success("Preferences saved successfully!")

    if st.button("Generate Itinerary"):
        response = requests.post(f"{BACKEND_URL}/generate_itinerary/", json=preferences)
        if response.status_code == 200:
            st.write(response.json()["itinerary"])
