import streamlit as st
from matplotlib import image
import os
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from pathlib import Path


# # absolute path to this file
# FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# # absolute path to this file's root directory
# PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# # absolute path of directory_of_interest
# dir_of_interest = os.path.join(PARENT_DIR, "resources")
#
# # data_path = os.path.join(dir_of_interest, "data", "Cleaned_Hospital.csv")
# #
# # df = pd.read_csv(data_path)
# IMAGE_PATH = os.path.join(dir_of_interest, "images", "hospital.png")
# # Image section of Laptop

# directory of the files and images
cur_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
IMAGE_PATH = cur_dir / "assets" / "hospital.png"
data_path = cur_dir / "resources" / "data" /"Cleaned_Hospital.csv"


st.set_page_config(page_title="Hospital",
                   page_icon="",
                   layout="wide"
)

st.markdown("<h1 style='text-align: center; color: Black;padding: 10px; top-margin:5px'> Neurocare searcher </h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: Blue;'>📌 Hospital Near You </h3>", unsafe_allow_html=True)

import base64

def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_img_as_base64("assets/about-us.jpg")

page_bg_img = f'''
<style>
.stApp {{
background-image: url("data:image/webp;base64,{img_base64}");
background-size: cover;
background-position: center;
}}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


# <style>
# .stApp {
# background-image: url("D:\Downloads\Nearest_Hospital_Chatbot-main (1)\Nearest_Hospital_Chatbot-main\assets\medical-worker.webp");
# background-size: cover;
# background-position: top center;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)
img = image.imread(IMAGE_PATH)


df = pd.read_csv(data_path)


col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

# with col2:
#     st.image(img, width=400, caption="Keep Calm!!! Believe in Neurocare ")

with col3:
    st.write(' ')
st.markdown("<h4 style='color: black; font-size: 30px; font-weight: bold;'>Enter Your Latitude:</h4>", unsafe_allow_html=True)

lat = st.number_input("", value=df.latitude.mean(), min_value=19.445685, max_value=28.256987, step=0.000001, format="%.6f")
error_msg1 = f"Latitude value must be between 19.445685 and 28.256987."
if not 19.445685 <= lat <= 28.256987:
    st.error(error_msg1)
error_msg2 = f"Longitude value must be between 85.126002 and 90.235698."

st.markdown("<h4 style='color: black; font-size: 30px; font-weight: bold;'>Enter Your Longitude:</h4>", unsafe_allow_html=True)
long = st.number_input("", value=df.longitude.mean(), min_value=85.126002, max_value=90.235698, step=0.000001, format="%.6f")
if not 85.126002 <= long <= 90.235698:
    st.error(error_msg2)
    
# st.markdown("<h2 style='text-align: center; color: red;'>🧑‍💻 The Input Section 👩‍💻</h2>", unsafe_allow_html=True)
# error_msg1 = f"Latitude value must be between 19.445685 and 28.256987."
# lat = st.number_input("<h2 style-''>Enter Your Latitude: </h2>", value=df.latitude.mean(), min_value=19.445685, max_value=28.256987, step=0.000001, format="%.6f")

# long = st.number_input("Enter Your Longitude:", value=df.longitude.mean(), min_value=85.126002, max_value=90.235698, step=0.000001, format="%.6f")


st.markdown("""
<style>
div[data-baseweb="input"] {
    display: flex;
    text-align: center
    width: 400px !important;  /* Adjust width */
    height: 50px !important;
    lenght: 70px /* Reduce height */
    font-size: 30px !important; /* Make text slightly bigger */
}
</style>
""", unsafe_allow_html=True)
# st.markdown("<h4 style='color: black; font-size: 30px; font-weight: bold;'>Enter Your Latitude:</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='color: black; font-size: 30px; font-weight: bold;'>Enter the number of Nearest Hospitals you want:</h4>", unsafe_allow_html=True)
num = st.slider("", 2, 10, 5)


# st.markdown("<b><h5 style='text-align: center; color: tomato;'>1) After entering the values please press the Enter ⎆ key 🤔</h5></b>", unsafe_allow_html=True)
# st.markdown("<b><h5 style='text-align: center; color: tomato;'>2) If Error occured i.e. the value is beyond of the renge then please currect that before entering further, this is because "
#             "we are predicting that you are near about West Bengal as the data is restricted to WB 🥺🥺</h5></b>", unsafe_allow_html=True)


ans = np.array((lat, long))

arr = np.transpose(np.array([df.latitude, df.longitude]))

dis = np.sqrt(np.sum((arr-ans)**2, axis=1))

dis = dis.tolist()

newdis = [round(i, 4) for i in dis]

df["Distance"] = newdis

top_5_hos = df.sort_values(by='Distance').head(num)

butt = st.button("Tap & Be Cured 🏥")
if butt:
    st.markdown("<h4 style='text-align: center; color: black;'>Enjoy We found {} Nearest Hospital for you </h4>".format(num),
                unsafe_allow_html=True)

    rg = top_5_hos[['Name Of Hospital', 'Address of Hospital',
       'current address', 'Phone Number', 'Class Recommended', 'latitude',
       'longitude']]
    st.dataframe(rg)
    st.markdown(
        "<h6 style='text-align: left; color: black;'>Double tap on any cell for more info</h6>",
        unsafe_allow_html=True)

    m = folium.Map(location=[lat, long], zoom_start=13)
    folium.Marker(location=[lat, long], icon=folium.Icon(icon='home', color='red', prefix="fa"), popup='Your Location',
                  size=155).add_to(m)

    for index, row in top_5_hos.iterrows():
        # Extract the hospital details from the row
        hospital_location = [row['latitude'], row['longitude']]
        hospital_name = row['Name Of Hospital']
        hospital_address = row['current address']
        hospital_phone = row['Phone Number']
        class_rec = row["Class Recommended"]

        # hovering to show the name of hospital

        #     tooltip_text = f"{hospital_name}"
        #     tooltip = folium.Tooltip(f"{hospital_name}")

        # Create a marker for the hospital
        popup_text = folium.Popup(f"""
<div style='text-align: center; justify-item: center; font-size: 20px;'>
    <b>{hospital_name}</b><br>
    {hospital_address}<br>
    📞 Phone: {hospital_phone}<br>
    {class_rec}
</div>
""", max_width=400)  
    folium.Marker(
    tooltip=str(df.iloc[index]['Name Of Hospital']),
    location=hospital_location,
    popup=popup_text,  # Corrected usage here
    icon=folium.Icon(icon='medkit', prefix='fa', color='red')
).add_to(m)

        # This prevents errors due to long text

        # popup_text = f"<b>{hospital_name}</b><br>{hospital_address}<br>Phone: {hospital_phone}<br>{class_rec}"
        # folium.Marker(
        #     tooltip=str(df.iloc[index]['Name Of Hospital']),
        #     location=hospital_location,
        #     popup=popup_text,
        #     icon=folium.Icon(icon='medkit', prefix='fa', color='red')
        # ).add_to(m)

    # make the map at middle

    col4, col5, col6 = st.columns(3)
    with col4:
        st.write(' ')

    with col5:
        folium_static(m, width=1000, height=650)


    with col6:
        st.write(' ')


    st.markdown(
        "<h5 style = 'color: indigo;'> 1) Squeeze/zoom out the map to view the all of your nearest hospitals</h5>",
        unsafe_allow_html=True)
    st.markdown(
        "<h5 style = 'color: indigo;'> 2) Tap on the pin to view the info regarding the hospitals and its address</h5>",
        unsafe_allow_html=True)
    st.markdown(
        "<b><h5 style = 'color: indigo;'>3) There are too few datas in the dataset of 250 entries</h5></b>",
        unsafe_allow_html=True)
    st.markdown(
        "<b><h5 style ='text-align: center; color: black; font-size: 30px; font-weight: bold'> Hope You Enjoyed 😊 </h5></b>",
        unsafe_allow_html=True)

    # st.subheader("Hope You Enjoyed 😊")


# st.subheader("After Completion, Move back to the previous tab of RASA and complete your conversation 🆓")




