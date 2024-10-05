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

section_descriptions = {
    "Abide in Christ": """### **1. Abide in Christ**  
**Summary:**  
Abiding in Christ means nurturing a close relationship with Him, allowing His presence to guide your life. It involves trusting His love and seeking His will in all aspects of life. As you draw near to Christ, you will experience transformation and spiritual growth.  
**Scripture Reference:**  
*"I am the vine; you are the branches. Whoever abides in me and I in him, he it is that bears much fruit, for apart from me you can do nothing."* — John 15:5""",

    "Live in the Word": """### **2. Live in the Word**  
**Summary:**  
Living in the Word emphasizes the importance of engaging with Scripture regularly. The Bible provides guidance, wisdom, and truth that shape your beliefs and actions. By studying God’s Word, you equip yourself to navigate life's challenges and grow in your faith.  
**Scripture Reference:**  
*"Your word is a lamp to my feet and a light to my path."* — Psalm 119:105""",

    "Pray in Faith": """### **3. Pray in Faith**  
**Summary:**  
Prayer is vital for developing a strong relationship with God. It allows you to communicate with Him, express your needs, and seek His guidance. Praying in faith strengthens your trust in God and deepens your understanding of His will for your life.  
**Scripture Reference:**  
*"And whatever you ask in prayer, you will receive, if you have faith."* — Matthew 21:22""",

    "Fellowship with Believers": """### **4. Fellowship with Believers**  
**Summary:**  
Fellowship with other believers fosters community and accountability in your spiritual journey. By encouraging one another, sharing burdens, and building meaningful relationships, you grow together in faith and reflect Christ's love to the world.  
**Scripture Reference:**  
*"And let us consider how to stir up one another to love and good works, not neglecting to meet together, as is the habit of some, but encouraging one another."* — Hebrews 10:24-25""",

    "Witness to the World": """### **5. Witness to the World**  
**Summary:**  
Being a witness to the world involves sharing your faith with others. By living out your beliefs and communicating the message of Christ, you can impact the lives of those around you and fulfill the Great Commission to spread the Gospel.  
**Scripture Reference:**  
*"Go therefore and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit."* — Matthew 28:19""",

    "Minister to Others": """### **6. Minister to Others**  
**Summary:**  
Ministering to others is an expression of Christ's love in action. By serving those in need and using your spiritual gifts, you reflect God’s compassion and contribute to the well-being of your community. Your acts of service can lead others to experience God's love firsthand.  
**Scripture Reference:**  
*"For even the Son of Man came not to be served but to serve, and to give his life as a ransom for many."* — Mark 10:45""",
}

# Initialize session state variables if not already done
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {section: {} for section in section_descriptions.keys()}

    
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
    st.write("Please fill in your personal information and your parent's information (if applicable) to help us understand your context better.")

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

# User Information Section
if st.session_state.page == 0:
    st.header("User Information")
    st.write("Please fill in your personal information and your parent's information (if applicable) to help us understand your context better.")
    
    # User info fields here
    name = st.text_input("Name", key="name")
    age = st.number_input("Age", min_value=1, max_value=120, value=18, key="age")
    parent_name = st.text_input("Parent's Name (if applicable)", key="parent_name")

    # Navigation buttons
    if st.button("Next"):
        if name and age:
            st.session_state.page += 1
        else:
            st.warning("Please fill out your name and age before proceeding.")

# Dynamic Sections for Each Assessment Area
sections = list(section_descriptions.keys())
for idx, section in enumerate(sections):
    if st.session_state.page == idx + 1:
        st.header(section)
        st.write(section_descriptions[section])  # Add description for the section

        # Questions for the section
        questions = ["Question 1", "Question 2"]  # Replace with your actual questions
        for question in questions:
            response_key = f"{section}_{question}"
            st.radio(question, options=["Never", "Rarely", "Sometimes", "Often", "Always"], key=response_key)
            st.session_state.responses[section][question] = st.session_state.get(response_key, None)

        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous"):
                st.session_state.page -= 1
        with col2:
            if st.button("Next"):
                if all(st.session_state.responses[section].get(question) for question in questions):
                    st.session_state.page += 1
                else:
                    st.warning("Please answer all questions before proceeding.")

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
