import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set up session state to manage the current page
if "page" not in st.session_state:
    st.session_state.page = 1

# Function to navigate to the next page
def next_page():
    st.session_state.page += 1

# Function to navigate to the previous page (if needed)
def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

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
    "Live in the Word": [
        "I regularly read and study my Bible.",
        "I believe the Bible is God’s Word and provides His instructions for life.",
        "I evaluate cultural ideas and lifestyles by biblical standards.",
        "I can answer questions about life and faith from a biblical perspective.",
        "I replace impure or inappropriate thoughts with God’s truth.",
        "I demonstrate honesty in my actions and conversation.",
        "When the Bible exposes an area of my life needing change, I respond to make things right.",
        "Generally, my public and private self are the same",
        "I use the Bible as the guide for the way I think and act.",
        "I study the Bible for the purpose of discovering truth for daily living."
    ],
    "Pray in Faith": [
        "My prayers focus on discovering God’s will more than expressing my needs.",
        "I trust God to answer when I pray and wait patiently on His timing.",
        "My prayers include thanksgiving, praise, confession, and requests.",
        "I expect to grow in my prayer life and intentionally seek help to improve.",
        "I spend as much time listening to God as talking to Him.",
        "I pray because I am aware of my complete dependence on God for everything in my life.",
        "Regular participation in group prayer characterizes my prayer life.",
        "I maintain an attitude of prayer throughout each day.",
        "I believe my prayers impact my life and the lives of others.",
        "I engage in a daily prayer time."
    ],
    "Fellowship with Believers": [
        "I forgive others when their actions harm me.",
        "I admit my errors in relationships and humbly seek forgiveness from the one I’ve hurt.",
        "I allow other Christians to hold me accountable for spiritual growth.",
        "I seek to live in harmony with other members of my family.",
        "I place the interest of others above my self-interest.",
        "I am gentle and kind in my interactions with others.",
        "I encourage and listen to feedback from others to help me discover areas for relationship growth.",
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
        "I help others understand how to effectively share a personal testimony.",
        "I make sure the people I witness to get the follow-up and support needed to grow in Christ.",
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
        "I share biblical truth with those I serve as God gives opportunity.",
        "I act as if other’s needs are as important as my own.",
        "I expect God to use me every day in His kingdom work.",
        "I regularly contribute time to a ministry at my church.",
        "I help others identify ministry gifts and become involved in ministry."
    ]
}

# Initialize user responses dictionary in session state
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {section: [] for section in sections}

# Page 1: User Information
if st.session_state.page == 1:
    st.title("Spiritual Growth Assessment")

    st.header("User Information")
    st.session_state.name = st.text_input("Name (required)")
    st.session_state.age = st.number_input("Age (required)", min_value=0, max_value=120, value=18, step=1)

    if st.session_state.age < 18:
        st.header("Parent Information")
        st.session_state.parent_name = st.text_input("Parent's Name (required)")
        st.session_state.parent_contact = st.text_input("Parent's Contact Information (required)")

    # Only show the error message when the user clicks the Next button
    if st.button("Next"):
        # Validate user input
        if not st.session_state.name:
            st.error("Please enter your name.")
        elif st.session_state.age < 18 and (not st.session_state.parent_name or not st.session_state.parent_contact):
            st.error("Please enter both parent's name and contact information.")
        else:
            next_page()

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
    likert_scale_values = {option: i for i, option in enumerate(likert_scale) if option != ""}

    # Ask questions for the current section
    for question in sections[section_name]:
        response = st.selectbox(question, likert_scale, index=0, key=f"{section_name}_{question}")
        if len(st.session_state.user_responses[section_name]) < len(sections[section_name]):
            st.session_state.user_responses[section_name].append(response)
        else:
            st.session_state.user_responses[section_name][sections[section_name].index(question)] = response

    # Layout for Previous and Next buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Previous"):
            prev_page()

    with col2:
        if st.button("Next"):
            if any(response == "" for response in st.session_state.user_responses[section_name]):
                st.error("Please answer all questions before proceeding.")
            else:
                next_page()

# Page for displaying results
elif st.session_state.page == len(sections) + 2:
    st.header("Results")

    # Calculate averages for each section
    averages = {}
    for section in sections:
        responses = [likert_scale_values[resp] for resp in st.session_state.user_responses[section] if resp != ""]
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
        st.write(f"**{section}:** Your average score is {average:.2f}. This indicates your current level of spiritual growth in this area.")

    if st.button("Previous"):
        prev_page()
