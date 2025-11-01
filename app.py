import streamlit as st
import os
from chatbot import generate_response

# Set page config as first command
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Check for API key
if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ GEMINI_API_KEY not found. Please set it in your environment variables.")
    st.stop()

st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.user-message {
    background-color: #d1ecf1;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.bot-message {
    background-color: #e8f4f8;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✈️ AI Travel Itinerary Planner</h1>', unsafe_allow_html=True)

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'trip_details' not in st.session_state:
    st.session_state.trip_details = None

if 'itinerary_text' not in st.session_state:
    st.session_state.itinerary_text = ""

with st.sidebar:
    st.header("Quick Start Examples 🚀")
    
    example1 = st.button("Tokyo: 7 days, $3000, 2 people")
    example2 = st.button("Paris: 5 days, $2000, 2 people")
    example3 = st.button("Bali: 10 days, $5000, 4 people")
    
    if example1:
        st.session_state.conversation.append(("user", "Plan a 7-day trip to Tokyo with $3000 budget for 2 people"))
    if example2:
        st.session_state.conversation.append(("user", "I want to visit Paris for 5 days with $2000"))
    if example3:
        st.session_state.conversation.append(("user", "Family vacation to Bali for 10 days, budget $5000"))
    
    if st.button("🔄 Start New Conversation"):
        st.session_state.conversation = []
        st.session_state.trip_details = None
        st.session_state.itinerary_text = ""
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat with Travel Assistant 💬")
    
    for speaker, message in st.session_state.conversation:
        if speaker == "user":
            st.markdown(f'<div class="user-message"><b>You:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>Travel Assistant:</b> {message}</div>', unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", placeholder="e.g., I want to plan a trip to Japan for 10 days...")
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            st.session_state.conversation.append(("user", user_input))
            
            with st.spinner("🔄 Creating your itinerary..."):
                response, trip_details = generate_response(user_input)
                st.session_state.conversation.append(("bot", response))
                
                if trip_details:
                    st.session_state.trip_details = trip_details
                    st.session_state.itinerary_text = f"""Travel Itinerary for {trip_details['destination']}
Duration: {trip_details['duration']} days
Budget: ${trip_details['budget']}
Travelers: {trip_details['travelers']} people
Interests: {', '.join(trip_details['interests'])}

{response}"""
            
            st.rerun()

    if st.session_state.trip_details and st.session_state.itinerary_text:
        st.download_button(
            label="📥 Download Itinerary",
            data=st.session_state.itinerary_text,
            file_name=f"{st.session_state.trip_details['destination']}_itinerary.txt",
            mime="text/plain"
        )

with col2:
    st.subheader("Quick Planning Form 🎯")
    
    with st.form("quick_plan_form"):
        destination = st.text_input("Destination 🌍", placeholder="e.g., Tokyo, Japan")
        duration = st.number_input("Duration (days) 📅", min_value=1, max_value=30, value=7)
        budget = st.number_input("Budget ($) 💰", min_value=100, max_value=10000, value=2000)
        travelers = st.number_input("Number of Travelers 👥", min_value=1, max_value=10, value=2)
        
        interests = st.multiselect(
            "Interests ❤️",
            ["Culture", "Adventure", "Food", "Relaxation", "Shopping", "Nature"],
            default=["Culture", "Food"]
        )
        
        quick_submit = st.form_submit_button("Generate Itinerary 🚀")
        
        if quick_submit and destination:
            user_message = f"I want to visit {destination} for {duration} days with ${budget} budget for {travelers} people interested in {', '.join(interests)}"
            st.session_state.conversation.append(("user", user_message))
            
            with st.spinner("🔄 Creating your itinerary..."):
                response, trip_details = generate_response(user_message)
                st.session_state.conversation.append(("bot", response))
                
                if trip_details:
                    st.session_state.trip_details = trip_details
                    st.session_state.itinerary_text = f"""Travel Itinerary for {trip_details['destination']}
Duration: {trip_details['duration']} days
Budget: ${trip_details['budget']}
Travelers: {trip_details['travelers']} people
Interests: {', '.join(trip_details['interests'])}

{response}"""
            
            st.rerun()

    if st.session_state.trip_details and st.session_state.itinerary_text:
        st.download_button(
            label="📥 Download Itinerary (Quick Form)",
            data=st.session_state.itinerary_text,
            file_name=f"{st.session_state.trip_details['destination']}_itinerary.txt",
            mime="text/plain",
            key="download_quick"
        )