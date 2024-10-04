import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Functions to store and load values
def store_value(key):
    st.session_state[key] = st.session_state["_" + key]

# Set up session state to manage the current page and user responses
if "page" not in st.session_state:
    st.session_state.page = 1

# Initialize user responses and personal info dictionary in session state
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {}

# Initialize personal info keys in session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "age" not in st.session_state:
    st.session_state.age = 18  # Default age
if "parent_name" not in st.session_state:
    st.session_state.parent_name = ""
if "parent_contact" not in st.session_state:
    st.session_state.parent_contact = ""

# Update sections with new questions
sections = {
    "Abide in Christ": [
        "I practice a regular quiet time and look forward to that time with Christ.",
        "When making choices, I seek Christ’s guidance first.",
        "My relationship with Christ is motivated more by love than duty or fear.",
        "I experience life change as a result of my worship experiences.",
        "When God makes me aware of His specific will in an area of my life, I follow His leading.",
        "I believe Christ provides the only way for a relationship with God.",
        "My actions demonstrate a desire to build God’s kingdom rather than my own.",
        "Peace, contentment, and joy characterize my life rather than worry and anxiety.",
        "I trust Christ to help me through any problem or crisis I face.",
        "I remain confident of God’s love and provision during difficult times."
    ],
    # Add other sections similarly...
}

# Page 1: User Information
if st.session_state.page == 1:
    st.title("Spiritual Growth Assessment")

    st.header("User Information")
    st.session_state.name = st.text_input("Name (required)", value=st.session_state.name)

    st.session_state.age = st.number_input("Age (required)", min_value=0, max_value=120, value=st.session_state.age, step=1)

    if st.session_state.age < 18:
        st.header("Parent Information")
        st.session_state.parent_name = st.text_input("Parent's Name (required)", value=st.session_state.parent_name)
        st.session_state.parent_contact = st.text_input("Parent's Contact Information (required)", value=st.session_state.parent_contact)

    # Show the error message only when the user clicks the Next button
    if st.button("Next"):
        # Validate user input
        if not st.session_state.name:
            st.error("Please enter your name.")
        elif st.session_state.age < 18 and (not st.session_state.parent_name or not st.session_state.parent_contact):
            st.error("Please enter both parent's name and contact information.")
        else:
            st.session_state.page += 1  # Move to the next page

# Pages for each section
elif 2 <= st.session_state.page <= len(sections) + 1:
    section_index = st.session_state.page - 2
    section_name = list(sections.keys())[section_index]

    # Progress Bar Calculation
    total_sections = len(sections)
    progress = (st.session_state.page - 1) / (total_sections + 1)  # +1 for the results page
    st.progress(progress)

    st.header(section_name)

    # Define Likert scale options with a blank default
    likert_scale = ["", "Never", "Rarely", "Sometimes", "Often", "Always"]

    # Initialize responses for the current section
    if section_name not in st.session_state.user_responses:
        st.session_state.user_responses[section_name] = [""] * len(sections[section_name])

    # Ask questions for the current section
    for i, question in enumerate(sections[section_name]):
        # Load the stored value for the question
        response = st.selectbox(question, likert_scale, index=likert_scale.index(st.session_state.user_responses[section_name][i]), key=f"{section_name}_{i}")
        st.session_state.user_responses[section_name][i] = response  # Store response directly

    # Layout for Previous and Next buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Previous"):
            st.session_state.page -= 1

    with col2:
        if st.button("Next",align='right'):
            if any(response == "" for response in st.session_state.user_responses[section_name]):
                st.error("Please answer all questions before proceeding.")
            else:
                st.session_state.page += 1  # Move to the next page

# Page for displaying results
elif st.session_state.page == len(sections) + 2:
    st.header("Results")

    # Calculate averages for each section
    averages = {}
    likert_scale_values = {"Never": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Always": 5}
    for section in sections:
        responses = [likert_scale_values[resp] for resp in st.session_state.user_responses.get(section, []) if resp != ""]
        averages[section] = np.mean(responses) if responses else 0  # Prevent division by zero

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
        st.write(f"{section}: {average:.2f}")

