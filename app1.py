import streamlit as st
import pandas as pd
import pickle

with open('Swiggy.pkl','rb')as f:
    best_model=pickle.load(f)


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Swiggy Delivery Time Prediction",
    page_icon="🍔",
    layout="wide"
)


# ==================================================
# COLOR THEME
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F7F3FC;
    }

    h1 {
        color: #6A1B9A;
    }

    h2 {
        color: #7B1FA2;
    }

    h3 {
        color: #8E24AA;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD MODEL
# ==================================================

model = pickle.load(open("swiggy.pkl", "rb"))


# ==================================================
# TITLE
# ==================================================

st.title("🍔 Swiggy Delivery Time Prediction")

st.subheader("How Soon Will Your Food Arrive?")

st.write(
    "Enter the delivery details below to estimate how many "
    "minutes your food may take to arrive."
)

st.divider()


# ==================================================
# IMAGE AND INFORMATION
# ==================================================

col1, col2 = st.columns(2)


with col1:

    st.image(
        "Swiggy delivery time image.png",
        use_container_width=True
    )


with col2:

    st.subheader("💡 What Affects Delivery Time?")

    st.info(
        """
        📍 Distance – Longer distances may require more travel time.

        🚦 Traffic – Heavy traffic can delay the delivery.

        🌦️ Weather – Poor weather conditions may affect travel.

        ⏰ Timing – Busy hours can increase delivery time.

        🛵 Multiple Deliveries – Handling more orders may require
        additional time.
        """
    )


st.divider()


# ==================================================
# DELIVERY INPUTS
# ==================================================

st.header("📝 Enter Delivery Details")

st.write(
    "Provide the details below to get an estimated delivery time."
)


# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🛵 Delivery Partner",
        "🍔 Order & Conditions",
        "⏰ Order Timing"
    ]
)


# ==================================================
# TAB 1 - DELIVERY PARTNER
# ==================================================

with tab1:

    st.subheader("🛵 Know Your Delivery Partner")

    col1, col2 = st.columns(2)


    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=60,
            value=25
        )

        ratings = st.slider(
            "Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.0,
            step=0.1
        )


    with col2:

        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "motorcycle",
                "scooter",
                "electric_scooter",
                "bicycle"
            ]
        )

        vehicle_condition = st.selectbox(
            "Vehicle Condition",
            [0, 1, 2]
        )

        st.caption(
            "0 = Poor | 1 = Average | 2 = Good"
        )


# ==================================================
# TAB 2 - ORDER AND CONDITIONS
# ==================================================

with tab2:

    st.subheader("🍔 Tell Us About Your Order")

    col1, col2 = st.columns(2)


    with col1:

        order_type = st.selectbox(
            "Order Type",
            [
                "snack",
                "meal",
                "drinks",
                "buffet"
            ]
        )

        distance = st.number_input(
            "Distance (km)",
            min_value=0.5,
            max_value=30.0,
            value=5.0,
            step=0.1
        )

        multiple_deliveries = st.number_input(
            "Multiple Deliveries",
            min_value=0,
            max_value=5,
            value=1
        )


    with col2:

        weather = st.selectbox(
            "Weather",
            [
                "sunny",
                "cloudy",
                "fog",
                "stormy",
                "sandstorms",
                "windy"
            ]
        )

        traffic = st.selectbox(
            "Traffic",
            [
                "low",
                "medium",
                "high",
                "jam"
            ]
        )

        festival = st.selectbox(
            "Festival",
            [
                "no",
                "yes"
            ]
        )

        city = st.selectbox(
            "City Type",
            [
                "urban",
                "metropolitian",
                "semi-urban"
            ]
        )


# ==================================================
# TAB 3 - ORDER TIMING
# ==================================================

with tab3:

    st.subheader("⏰ When Did You Place Your Order?")

    col1, col2 = st.columns(2)


    with col1:

        order_hour = st.slider(
            "Order Time (Hour)",
            0,
            23,
            12
        )

        day_of_week = st.selectbox(
            "Day of Week",
            [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday"
            ]
        )


    with col2:

        is_weekend = st.selectbox(
            "Weekend?",
            [
                "no",
                "yes"
            ]
        )

        pickup_time = st.number_input(
            "Pickup Time (minutes)",
            min_value=1,
            max_value=60,
            value=15
        )


st.divider()


# ==================================================
# PREDICTION BUTTON
# ==================================================

st.subheader("🍽️ Ready to Find Out?")


if st.button(
    "🚀 Calculate Delivery Time",
    use_container_width=True
):


    # ==================================================
    # CREATE INPUT DATAFRAME
    # ==================================================

    input_df = pd.DataFrame({

        "age": [age],

        "ratings": [ratings],

        "weather": [weather],

        "traffic": [traffic],

        "vehicle_condition": [vehicle_condition],

        "type_of_order": [order_type],

        "type_of_vehicle": [vehicle_type],

        "festival": [festival],

        "city_type": [city],

        "distance": [distance],

        "is_weekend": [is_weekend],

        "order_time_hour": [order_hour],

        "order_day_of_week": [day_of_week],

        "pickup_time_minutes": [pickup_time],

        "multiple_deliveries": [multiple_deliveries]

    })


    # ==================================================
    # CONVERT WEEKEND
    # ==================================================

    input_df["is_weekend"] = input_df[
        "is_weekend"
    ].map({
        "no": 0,
        "yes": 1
    })


    # ==================================================
    # FEATURE ENGINEERING
    # ==================================================

    input_df["distance_per_delivery"] = (
        input_df["distance"] /
        (input_df["multiple_deliveries"] + 1)
    )


    input_df["is_peak_hour"] = input_df[
        "order_time_hour"
    ].apply(
        lambda x: 1 if 18 <= x <= 22 else 0
    )


    input_df["is_rush"] = (
        (input_df["traffic"] == "jam") &
        (input_df["is_weekend"] == 1)
    ).astype(int)


    input_df["weekend_peak"] = (
        (input_df["is_weekend"] == 1) &
        (input_df["is_peak_hour"] == 1)
    ).astype(int)


    # ==================================================
    # FINAL COLUMN ORDER
    # ==================================================

    input_df = input_df[
        [
            "age",
            "ratings",
            "weather",
            "traffic",
            "vehicle_condition",
            "type_of_order",
            "type_of_vehicle",
            "festival",
            "city_type",
            "distance",
            "is_weekend",
            "order_time_hour",
            "order_day_of_week",
            "pickup_time_minutes",
            "multiple_deliveries",
            "distance_per_delivery",
            "is_peak_hour",
            "is_rush",
            "weekend_peak"
        ]
    ]


    # ==================================================
    # MAKE PREDICTION
    # ==================================================

    try:

        prediction = model.predict(input_df)

        result = float(prediction[0])


        # ==================================================
        # DISPLAY RESULT
        # ==================================================

        st.success("🎉 Prediction Completed!")

        st.header(
            f"🕒 Estimated Delivery Time: {result:.0f} Minutes"
        )


        # ==================================================
        # SIMPLE MESSAGE
        # ==================================================

        if result <= 25:

            st.info(
                "⚡ Your food is expected to arrive relatively quickly."
            )

        elif result <= 40:

            st.warning(
                "🕒 Your food may take a moderate amount of time to arrive."
            )

        else:

            st.error(
                "🚦 Your food may take longer than usual to arrive."
            )


        # ==================================================
        # DELIVERY SUMMARY
        # ==================================================

        st.subheader("📋 Your Delivery Summary")

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Distance",
                f"{distance:.1f} km"
            )


        with col2:

            st.metric(
                "Traffic",
                traffic.title()
            )


        with col3:

            st.metric(
                "Rating",
                f"{ratings:.1f} ⭐"
            )


        with col4:

            st.metric(
                "Pickup Time",
                f"{pickup_time} min"
            )


        # ==================================================
        # PREDICTION DETAILS
        # ==================================================

        with st.expander("🔍 View Prediction Details"):

            st.write("Age:", age)

            st.write("Rating:", ratings)

            st.write(
                "Vehicle Type:",
                vehicle_type
            )

            st.write(
                "Vehicle Condition:",
                vehicle_condition
            )

            st.write(
                "Order Type:",
                order_type
            )

            st.write(
                "Distance:",
                distance,
                "km"
            )

            st.write(
                "Multiple Deliveries:",
                multiple_deliveries
            )

            st.write(
                "Weather:",
                weather
            )

            st.write(
                "Traffic:",
                traffic
            )

            st.write(
                "Festival:",
                festival
            )

            st.write(
                "City Type:",
                city
            )


    except Exception as e:

        st.error(
            "❌ Unable to calculate the delivery time."
        )

        st.write(e)



