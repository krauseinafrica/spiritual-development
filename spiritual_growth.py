import streamlit as st
import numpy as np
import plotly.graph_objects as go
import openai
from openai import OpenAI
from oauth2client.service_account import ServiceAccountCredentials

# def authenticate_gsheets():
#     creds_dict = st.secrets["gcp_service_account"]
#     creds = ServiceAccountCredentials.from_json_keyfile_dict(
#         creds_dict, ["https://www.googleapis.com/auth/spreadsheets"]
#     )
#     client = gspread.authorize(creds)
#     return client

# # Connect to Google Sheets
# client = authenticate_gsheets()
# sheet = client.open("Streamlit Spiritual Formations").sheet1  # Open the first sheet



# client = OpenAI(api_key = "<API_KEY>")
# client = st.secrets["openai"]["API_KEY"]

# Set your OpenAI API key
client = OpenAI(api_key = st.secrets["openai"]["API_KEY"])

# Functions to store and load values
def store_value(key):
    st.session_state[key] = st.session_state["_" + key]

section_descriptions = {
    "Abide in Christ": """Abiding in Christ means nurturing a close relationship with Him, allowing His presence to guide your life. It involves trusting His love and seeking His will in all aspects of life. As you draw near to Christ, you will experience transformation and spiritual growth.  
**Scripture Reference:**  
*"I am the vine; you are the branches. Whoever abides in me and I in him, he it is that bears much fruit, for apart from me you can do nothing."* — John 15:5""",

    "Live in the Word": """Living in the Word emphasizes the importance of engaging with Scripture regularly. The Bible provides guidance, wisdom, and truth that shape your beliefs and actions. By studying God’s Word, you equip yourself to navigate life's challenges and grow in your faith.  
**Scripture Reference:**  
*"Your word is a lamp to my feet and a light to my path."* — Psalm 119:105""",

    "Pray in Faith": """Prayer is vital for developing a strong relationship with God. It allows you to communicate with Him, express your needs, and seek His guidance. Praying in faith strengthens your trust in God and deepens your understanding of His will for your life.  
**Scripture Reference:**  
*"And whatever you ask in prayer, you will receive, if you have faith."* — Matthew 21:22""",

    "Fellowship with Believers": """Fellowship with other believers fosters community and accountability in your spiritual journey. By encouraging one another, sharing burdens, and building meaningful relationships, you grow together in faith and reflect Christ's love to the world.  
**Scripture Reference:**  
*"And let us consider how to stir up one another to love and good works, not neglecting to meet together, as is the habit of some, but encouraging one another."* — Hebrews 10:24-25""",

    "Witness to the World": """Being a witness to the world involves sharing your faith with others. By living out your beliefs and communicating the message of Christ, you can impact the lives of those around you and fulfill the Great Commission to spread the Gospel.  
**Scripture Reference:**  
*"Go therefore and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit."* — Matthew 28:19""",

    "Minister to Others": """Ministering to others is an expression of Christ's love in action. By serving those in need and using your spiritual gifts, you reflect God’s compassion and contribute to the well-being of your community. Your acts of service can lead others to experience God's love firsthand.  
**Scripture Reference:**  
*"For even the Son of Man came not to be served but to serve, and to give his life as a ransom for many."* — Mark 10:45""",
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
if "email" not in st.session_state:
    st.session_state.email = ""
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
    st.write("Please fill in your personal information below. Include your parent's information (if applicable). We will be adding in the ability to email the results to yourself and share with others in a future version. ")
    st.session_state.name = st.text_input("Name (required)", value=st.session_state.name)
    st.session_state.email = st.text_input("Email (required)", value=st.session_state.email)
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

    # Display the section description
    st.markdown(section_descriptions[section_name])  # Show section description

    # Define Likert scale options with a blank default
    default_likert_scale = ["", "Never", "Rarely", "Sometimes", "Often", "Always"]

    # Define additional Likert scale options for specific questions
    additional_likert_scales = {
        "Question 1": ["", "Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],  # For Question 1
        "Question 2": ["", "Not at All True", "A Little True", "Somewhat True", "Mostly True", "Completely True"],  # For Question 2
    # Add more specific questions and their respective scales as needed
    }  

    # Initialize responses for the current section
    if section_name not in st.session_state.user_responses:
        st.session_state.user_responses[section_name] = [""] * len(sections[section_name])

    # Ask questions for the current section
    for i, question in enumerate(sections[section_name]):
        # Determine the appropriate Likert scale for the question
        if question in additional_likert_scales:
            likert_scale = additional_likert_scales[question]  # Use specific scale if exists
        else:
            likert_scale = default_likert_scale  # Default scale for all other questions

        # Load the stored value for the question
        response = st.selectbox(question, likert_scale, index=likert_scale.index(st.session_state.user_responses[section_name][i]), key=f"{section_name}_{i}")
        st.session_state.user_responses[section_name][i] = response  # Store response directly

    # Layout for Previous and Next buttons
    col1, col2 = st.columns([1, 1])  # Two columns of equal width

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

    # Display the radar chart
    st.plotly_chart(fig)

    # Show average scores
    st.header("Average Scores")
    for section, average in averages.items():
        st.write(f"{section}: {average:.2f}")

    # Initialize insights in session state
    if 'insights_generated' not in st.session_state:
        st.session_state.insights_generated = False

    # Option to interpret results
    if st.button("Get Insights on Your Results"):
        if not st.session_state.insights_generated:
            with st.spinner("Getting insights..."):
                # Generate interpretations using your existing function
                for section in sections.keys():
                    interpretation = generate_interpretation(section, averages[section])
                    st.markdown(f"### **{section} Insights**")
                    st.write(interpretation)
                
                st.session_state.insights_generated = True  # Mark insights as generated
        else:
            st.warning("Insights have already been generated. Please refresh to get new insights.")
