import streamlit as st
import pandas as pd
import numpy as np
import pickle
import traceback

with open("app/artifacts/df.pkl", "rb") as file:
    df = pickle.load(file)

with open("app/artifacts/pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

st.title("Real Estate Price Prediction🏡")

# Create four rows of three columns each
row1 = st.columns(4)
row2 = st.columns(4)
row3 = st.columns(4)
row4 = st.columns(4)
row5 = st.columns(3)
row6 = st.columns(3)

amenities = {'24 X 7 Security',
 'ATM',
 'Cafeteria',
 'Car Parking',
 'Childrens play area',
 'Club House',
 'Full Power Backup',
 'Golf Course',
 'Gymnasium',
 'Hospital',
 'Indoor Games',
 'Intercom',
 'Jogging Track',
 'Landscaped Gardens',
 'Lift(s)',
 'Maintenance Staff',
 'Multipurpose Room',
 'Rain Water Harvesting',
 'School',
 'Shopping Mall',
 'Sports Facility',
 'Staff Quarter',
 'Swimming Pool',
 'Vaastu Compliant'}

amenity_scores = {
    '24 X 7 Security': 5,
    'ATM': 3,
    'Cafeteria': 3,
    'Car Parking': 4,
    'Childrens play area': 4,
    'Club House': 4,
    'Full Power Backup': 5,
    'Golf Course': 5,
    'Gymnasium': 4,
    'Hospital': 5,
    'Indoor Games': 3,
    'Intercom': 2,
    'Jogging Track': 4,
    'Landscaped Gardens': 4,
    'Lift(s)': 4,
    'Maintenance Staff': 3,
    'Multipurpose Room': 4,
    'Rain Water Harvesting': 3,
    'School': 5,
    'Shopping Mall': 5,
    'Sports Facility': 4,
    'Staff Quarter': 2,
    'Swimming Pool': 5,
    'Vaastu Compliant': 3
}


furnishings = {'AC',
 'BED',
 'Dining Table',
 'Gas connection',
 'Microwave',
 'Refrigerator',
 'Sofa',
 'TV',
 'Wardrobe',
 'Washing Machine',
 'Wifi'}

furnish_details_scores = {
    'AC': 8,
    'BED': 10,
    'Dining Table': 7,
    'Gas connection': 6,
    'Microwave': 7,
    'Refrigerator': 8,
    'Sofa': 6,
    'TV': 5,
    'Wardrobe': 7,
    'Washing Machine': 8,
    'Wifi': 9
}


# property_type
with row1[0]:
    property_type = st.selectbox("Property Type", ["Flat", "House"])

# Localities
with row1[1]:
    locality = st.selectbox("Locality", df['locality'].unique().tolist())

# area
with row1[2]:
    area = st.number_input("Area", value=0)

#Bedroom
with row1[3]:
    bedroom = st.selectbox("Number of Bedroom", sorted(df['bhk'].unique().tolist()))

# Bathrooms
with row2[0]:
    bathroom = st.selectbox("Number of Bathrooms", sorted(df['bathrooms'].unique().tolist()))

# Balconies
with row2[1]:
    balcony = st.selectbox("Number of Balconies", sorted(df['balconies'].unique().tolist()))

# floor
with row2[2]:
    floor = st.selectbox("Number of Floors", sorted(df['floor'].unique().tolist()))

# Facing
with row2[3]:
    facing = st.selectbox('Facing', df['facing'].unique())

# age_of_property
with row3[0]:
    property_age = st.selectbox("Property Age", df['age_of_property'].unique().tolist())

# new/resale
with row3[1]:
    new_resale = st.selectbox("New/Resale", df['new_resale'].unique())

# Furnishing Type
with row3[2]:
    furnishing_type = st.selectbox("Furnishing Type", df['furnishing_type'].unique())

# Amenities
with row3[3]:
    amenities = st.multiselect("Amenities", amenities)

# Furnishings
with row4[0]:
    furnishings = st.multiselect("Furnishings", furnishings)

# Study Room
with row4[1]:
    study_room = st.selectbox("Study Room", ['Yes', 'No'])

# Pooja Room
with row4[2]:
    pooja_room = st.selectbox("Pooja Room", ['Yes', 'No'])

# Servant Room
with row4[3]:
    servant_room = st.selectbox("Servant Room", ['Yes', 'No'])

if st.button("Predict House Price"):

    if amenities:
        amenities_score = sum([amenity_scores[amenity] for amenity in amenities if amenity in amenity_scores])
    else:
        amenities_score = 0  

    if furnishings:
        furnishings_score = sum([furnish_details_scores[furnishing] for furnishing in furnishings if furnishing in furnish_details_scores])
    else:
        furnishings_score = 0  

    # Convert study_room, servant_room and pooja_room to binary
    study_room_binary = 1 if study_room == 'Yes' else 0
    servant_room_binary = 1 if servant_room == 'Yes' else 0
    pooja_room_binary =  1 if pooja_room == 'Yes' else 0

    data = [
        [
            property_type,       
            bedroom,              
            area,                 
            locality,             
            new_resale,           
            property_age,         
            bathroom,             
            floor,                
            balcony,              
            furnishing_type,      
            facing,               
            amenities_score,      
            furnishings_score,
            study_room_binary,   
            servant_room_binary,  
            pooja_room_binary    
        ]
    ]

    # Column names should match the pipeline's expected input
    columns = [
        'property_type', 'bhk', 'area', 'locality', 'new_resale', 
        'age_of_property', 'bathrooms', 'floor', 'balconies',
        'furnishing_type', 'facing', 'amenities_score','furnishing_score',
        'study_room', 'servant_room', 'pooja_room'
    ]

    # Create the DataFrame for prediction, ensuring no lists are passed
    df_input = pd.DataFrame(data, columns=columns)


    predicted_price =  np.expm1(pipeline.predict(df_input)[0])
    rounded_price = np.round(float(predicted_price), 2)


    st.success(f"Predicted Price: {rounded_price} Crores")




