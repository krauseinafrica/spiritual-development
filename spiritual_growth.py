import streamlit as st
import pandas as pd
import numpy as np
from math import pi
import plotly.graph_objects as go

# Function to calculate average scores for each section
def calculate_averages(responses, sections):
    averages = {}
    for section in sections:
        averages[section] = np.mean(responses[section])
    return averages

# Define the sections and questions
sections = {
    "Abide in Christ": [f"Abide in Christ - Question {i}" for i in range(1, 6)],
    "Live in the Word": [f"Live in the Word - Question {i}" for i in range(1, 6)],
    "Pray in Faith": [f"Pray in Faith - Question {i}" for i in range(1, 6)],
    "Fellowship with Believers": [f"Fellowship with Believers - Question {i}" for i in range(1, 6)],
    "Witness to the World": [f"Witness to the World - Question {i}" for i in range(1, 6)],
    "Minister to Others": [f"Minister to Others - Question {i}" for i in range(1, 6)]
}

# Initialize user responses dictionary
user_responses = {section: [] for section in sections}

st.title("Spiritual Growth Assessment")

# User Information
st.header("User Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)

if age < 18:
    st.header("Parent Information")
    parent_name = st.text_input("Parent's Name")
    parent_contact = st.text_input("Parent's Contact Information")

# Walk through each section and ask questions
for section, questions in sections.items():
    st.header(section)
    for question in questions:
        response = st.slider(question, min_value=1, max_value=5, step=1)
        user_responses[section].append(response)

# Calculate and display results
if st.button("Submit"):
    averages = calculate_averages(user_responses, sections)

    # Create radar chart
    fig = go.Figure()

    categories = list(averages.keys())
    values = list(averages.values())
    values += values[:1]  # Close the radar chart loop

    categories += categories[:1]

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Spiritual Growth Assessment'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )

    st.plotly_chart(fig)

    # Brief explanation of the results
    st.header("Results Summary")
    for section, average in averages.items():
        st.write(f"**{section}:** Your average score is {average:.2f}. This indicates your current level of spiritual growth in this area.")

