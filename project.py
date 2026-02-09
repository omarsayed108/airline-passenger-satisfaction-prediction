import streamlit as st
import joblib
import numpy as np
import base64

st.set_page_config(page_title="✈️ Airline Satisfaction Predictor", layout="wide")

# Load the trained RandomForest model
model = joblib.load("random_Model.pkl")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_local(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_local("airplane.png")

# Sidebar
with st.sidebar:
    st.title("📋 About the Project")
    st.write(
        """
        This project predicts **Airline Customer Satisfaction** based on flight and service experience data.

        Made with 💡 and ✈️ to improve airline services.
        """
    )
    st.markdown("---")

    # Initialize session state variables if not present
    if "show_team" not in st.session_state:
        st.session_state.show_team = False
    if "show_images" not in st.session_state:
        st.session_state.show_images = False

    # Button to toggle team members
    if st.button("Team Members"):
        st.session_state.show_team = not st.session_state.show_team

    if st.session_state.show_team:
        st.subheader("Team Members")
        st.markdown(
            """
            - Hager  
            - Omar  
            - Shada  
            - Mourad  
            - Salma  
            - Mostafa
            """
        )

    st.markdown("---")

    # Button to toggle plots
    if st.button("Visualizations"):
        st.session_state.show_images = not st.session_state.show_images

    if st.session_state.show_images:
        st.subheader("Visualizations")
        st.image("plot.png", caption="Plot 1", use_container_width=True)
        st.image("plot2.png", caption="Plot 2", use_container_width=True)
        st.image("plot4.png", caption="Plot 1", use_container_width=True)
        st.image("plot8.png", caption="Plot 2", use_container_width=True)
        st.image("plot1.png", caption="Plot 1", use_container_width=True)

st.title("🎯 Airline Customer Satisfaction Prediction")
st.markdown("### Please enter passenger details:")

def categorize_flight_distance(distance):
    if distance < 500:
        return "Short"
    elif distance < 1500:
        return "Medium"
    else:
        return "Long"

def categorize_age(age):
    if age < 18:
        return "Teen"
    elif age < 30:
        return "Young Adult"
    elif age < 50:
        return "Adult"
    else:
        return "Senior"

gender_map = {"Female": 0, "Male": 1}
customer_type_map = {"Loyal Customer": 0, "Disloyal Customer": 1}
travel_type_map = {"Business Travel": 0, "Personal Travel": 1}
class_map = {"Business": 0, "Eco": 1, "Eco Plus": 2}
flight_distance_map = {"Long": 0, "Medium": 1, "Short": 2}
age_map = {"Adult": 0, "Senior": 1, "Teen": 2, "Young Adult": 3}

def scale_5(x):
    return x / 5.0

# Inputs vertically stacked
gender = st.selectbox("Gender", list(gender_map.keys()))
customer_type = st.selectbox("Customer Type", list(customer_type_map.keys()))
age_input = st.number_input("Age (years)", min_value=0, max_value=120, value=30)
travel_type = st.selectbox("Type of Travel", list(travel_type_map.keys()))
flight_class = st.selectbox("Flight Class", list(class_map.keys()))
flight_distance = st.number_input("Flight Distance (km)", min_value=0, value=500)

st.markdown("### Rate the following (1: Poor, 5: Excellent):")
wifi = st.slider("Inflight Wifi Service", 0, 5, 1)
time_convenient = st.slider("Departure/Arrival Time Convenience", 0, 5, 1)
online_booking = st.slider("Ease of Online Booking", 0, 5, 1)
food = st.slider("Food and Drink Quality", 0, 5, 1)
online_boarding = st.slider("Online Boarding", 0, 5, 1)
seat_comfort = st.slider("Seat Comfort", 0, 5, 1)
entertainment = st.slider("Inflight Entertainment", 0, 5, 1)
onboard_service = st.slider("On-board Service", 0, 5, 1)
legroom = st.slider("Leg Room Service", 0, 5, 1)
baggage = st.slider("Baggage Handling", 0, 5, 1)
checkin = st.slider("Check-in Service", 0, 5, 1)
inflight_service = st.slider("Inflight Service", 0, 5, 1)
cleanliness = st.slider("Cleanliness", 0, 5, 1)
dep_delay = st.number_input("Departure Delay (minutes)", min_value=0, value=0)
arr_delay = st.number_input("Arrival Delay (minutes)", min_value=0, value=0)

# Prepare input for model
gender_val = gender_map[gender]
cust_type_val = customer_type_map[customer_type]
travel_val = travel_type_map[travel_type]
class_val = class_map[flight_class]

fd_cat = categorize_flight_distance(flight_distance)
fd_val = flight_distance_map[fd_cat]

age_cat = categorize_age(age_input)
age_val = age_map[age_cat]

wifi_val = scale_5(wifi)
time_conv_val = scale_5(time_convenient)
online_book_val = scale_5(online_booking)
food_val = scale_5(food)
online_board_val = scale_5(online_boarding)
seat_comf_val = scale_5(seat_comfort)
entertainment_val = scale_5(entertainment)
onboard_serv_val = scale_5(onboard_service)
legroom_val = scale_5(legroom)
baggage_val = scale_5(baggage)
checkin_val = scale_5(checkin)
inflight_serv_val = scale_5(inflight_service)
cleanliness_val = scale_5(cleanliness)
total_delay_val = (dep_delay + arr_delay) / 100.0

input_data = np.array([[
    gender_val,
    cust_type_val,
    age_val,
    travel_val,
    class_val,
    fd_val,
    wifi_val,
    time_conv_val,
    online_book_val,
    food_val,
    online_board_val,
    seat_comf_val,
    entertainment_val,
    onboard_serv_val,
    legroom_val,
    baggage_val,
    checkin_val,
    inflight_serv_val,
    cleanliness_val,
    total_delay_val
]])

if st.button("🚀 Predict Satisfaction"):
    pred = model.predict(input_data)[0]
    result = "✅ Satisfied" if pred == 1 else "❌ Neutral or Dissatisfied"
    st.success(f"Prediction: {result}")