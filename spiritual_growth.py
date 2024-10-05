import streamlit as st
import numpy as np
import plotly.graph_objects as go
import openai
from openai import OpenAI

# client = OpenAI(api_key = "<API_KEY>")
# client = st.secrets["openai"]["API_KEY"]

# Set your OpenAI API key
client = OpenAI(api_key = st.secrets["openai"]["API_KEY"])

# Functions to store and load values
def store_value(key):
    st.session_state[key] = st.session_state["_" + key]

# Section descriptions
section_descriptions = {
    "User Information": "Please fill in your personal information and your parent's information (if applicable) to help us understand your context better.",
    "Abide in Christ": "This section assesses your relationship with Christ, focusing on your personal time with Him and how it influences your life.",
    "Live in the Word": "Here, we evaluate how you engage with the Bible and apply its teachings in your daily life.",
    "Pray in Faith": "This section focuses on your prayer life, including how you communicate with God and your expectations in prayer.",
    "Fellowship with Believers": "In this section, we look at your relationships with other Christians and how you engage in community.",
    "Witness to the World": "This section evaluates how you share your faith and engage with those who do not know Christ.",
    "Minister to Others": "Here, we assess how you serve others and use your spiritual gifts in ministry."
}
    
# Create openai connection
def generate_interpretation(section_name, average_score):
    prompt = f"""
    I am a Christian filling out a Spiritual Growth assessment and need help interpretting the results from a spiritual mentor.
    Please help interpret the results of each section in the spiritual growth assessment and highlight where they are doing well and where they have opporutnities to grow based on their answers to questions in each section. 
    Provide a sentence explaining what each section is measuring based on a summary of the questions asked. 
    Review questions that scored the lowest in each section to help recommend next steps. Keep suggestions to one sentence and add scripture references from the Bible for guidance if applicable.
    Also highlight areas they seem to be doing well to encourage them with one sentence highlight questions they scored higher on, if applicable.
    Respond as if you are talking to the person filling out the form. 
    # Use markdown to title each section's response with the section name
    The section "{section_name}" in a spiritual growth assessment has an average score of {average_score} on a scale of 1-5, where 1 means "Never" and 5 means "Always." 
    Provide the person filling out the form an interpretation of what this score means in terms of spiritual growth for the person and offer guidance on how they can improve in this area.
    """
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.7
    )
    return response.choices[0].text.strip()

    

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
        "I regularly spend quiet time with Christ and look forward to it.",
        "When making choices, I seek Christ’s guidance first.",
        "My relationship with Christ is motivated more by love than duty or fear.",
        "I experience life change as a result of my worship experiences.",
        "When God makes me aware of His specific will in an area of my life, I follow His leading.",
        "I believe that Jesus is the only way to have a relationship with God.",
        "My actions demonstrate a desire to build God’s kingdom rather than my own.",
        "I experience peace, contentment, and joy in my life instead of worry and anxiety.",
        "I trust Christ to help me through any problem or crisis I face.",
        "I remain confident of God’s love and provision during difficult times."
    ],
    "Live in the Word": [
        "I regularly read and study my Bible.",
        "I believe the Bible is God’s Word and provides His instructions for life.",
        "I compare ideas from culture to what the Bible teaches.",
        "I can answer questions about life and faith from a biblical perspective.",
        "I replace impure or inappropriate thoughts with God’s truth.",
        "I demonstrate honesty in my actions and conversation.",
        "When the Bible exposes an area of my life needing change, I respond to make things right.",
        "I try to be the same person in public and private.",
        "I use the Bible as the guide for the way I think and act.",
        "I study the Bible for the purpose of discovering truth for daily living."
    ],
    "Pray in Faith": [
        "When I pray, I focus more on finding out what God wants than just sharing my needs.",
        "I trust God to answer when I pray and wait patiently on His timing.",
        "My prayers include thanksgiving, praise, confession, and requests.",
        "I expect to grow in my prayer life and intentionally seek help to improve.",
        "I spend as much time listening to God as talking to Him.",
        "I pray because I am aware of my complete dependence on God for everything in my life.",
        "Regular participation in group prayer characterizes my prayer life.",
        "I try to keep a prayerful attitude throughout my day.",
        "I believe my prayers impact my life and the lives of others.",
        "I engage in a daily prayer time."
    ],
    "Fellowship with Believers": [
        "I forgive others when their actions harm me.",
        "I admit my errors in relationships and humbly seek forgiveness from the one I’ve hurt.",
        "I allow other Christians to hold me accountable for spiritual growth.",
        "I seek to live in harmony with other members of my family.",
        "I put the needs of others before my own.",
        "I am gentle and kind in my interactions with others.",
        "I welcome feedback from others to help me improve my relationships.",
        "I show patience in my relationships with family and friends.",
        "I encourage others by pointing out their strengths rather than criticizing their weaknesses.",
        "My time commitments demonstrate that I value relationships over work/career/hobbies."
    ],
    "Witness to the World": [
        "I share my faith in Christ with non-believers.",
        "I regularly pray for non-believers I know.",
        "I make my faith known to my neighbors and/or fellow employees.",
        "I intentionally maintain relationships with non-believers in order to share my testimony.",
        "When confronted about my faith, I remain consistent and firm in my testimony.",
        "I help others learn how to share their personal stories about faith.",
        "I ensure that those I share my faith with receive support to help them grow in Christ.",
        "I encourage my church and friends to support mission efforts.",
        "I am prepared to share my testimony at any time.",
        "My actions demonstrate a belief in and commitment to the Great Commission (Matthew 28:19-20)."
    ],
    "Minister to Others": [
        "I understand my spiritual gifts and use those gifts to serve others.",
        "I serve others expecting nothing in return.",
        "I sacrificially contribute my finances/resources to help others in my church and community.",
        "I go out of my way to show love to people I meet.",
        "Meeting the needs of others provides a sense of purpose in my life.",
        "I share what the Bible teaches with those I help when I have the chance.",
        "I act as if others' needs are as important as my own.",
        "I expect God to use me every day in His kingdom work.",
        "I regularly contribute time to a ministry at my church.",
        "I assist others in discovering their gifts and getting involved in serving."
    ]
}

# Page 1: User Information
if st.session_state.page == 1:
    st.title("Spiritual Growth Assessment")

    st.header("User Information")
    st.write(section_descriptions["User Information"])

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
    st.write(section_descriptions[section])
    
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
        if st.button("Next"):
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

        # Generate interpretation using OpenAI
        with st.spinner(f"Interpreting your results for '{section}'..."):
            interpretation = generate_interpretation(section, average)
        
        st.write(interpretation)
