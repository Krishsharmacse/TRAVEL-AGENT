import streamlit as st
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)

try:
    from crew import run_travel_itinerary
except ImportError as e:
    st.error(f"Error loading crew module. Ensure backend/crew.py exists and uses absolute imports. Details: {e}")
    st.stop()


def main():
    st.set_page_config(page_title="✈️ AI Travel Itinerary Generator", layout="wide")
    st.title("✈️ AI Travel Itinerary Generator")
    st.markdown("Enter your travel details below to generate a comprehensive itinerary, powered by Gemini and CrewAI.")

    with st.form("itinerary_form"):
        st.header("Trip Details")
        
        destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Duration (days)", min_value=1, value=5)
        with col2:
            travelers = st.number_input("Number of Travelers", min_value=1, value=2)

        col3, col4 = st.columns(2)
        with col3:
            budget = st.number_input("Maximum Budget ($)", min_value=100, value=2500, step=100)
        with col4:
            interests_input = st.text_input("Interests (comma-separated)", 
                                            placeholder="e.g., historical sites, local cuisine, art")
        
        submitted = st.form_submit_button("Generate Itinerary 🚀")

    if submitted:
        if not destination or not interests_input:
            st.error("Please fill in both the **destination** and **interests** fields.")
            return

        interests_list = [i.strip() for i in interests_input.split(',') if i.strip()]

        with st.spinner("The AI Agents are collaborating to generate your itinerary..."):
            try:
                # Call your CrewAI logic
                final_output = run_travel_itinerary(
                    destination=destination,
                    duration=duration,
                    budget=budget,
                    travelers=travelers,
                    interests=interests_list
                )
              
                st.success("Itinerary successfully generated!")
                st.subheader("Your Detailed Travel Itinerary")
               
                st.markdown(final_output) 
              
                st.markdown("---")
                st.subheader("Download Artifacts")
                
                output_files = ['research.md', 'Planing.md', 'budget.md']
             
                download_cols = st.columns(len(output_files)) 
                
                for i, file_name in enumerate(output_files):
                  
                    file_path = os.path.join(PROJECT_ROOT, file_name)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        with download_cols[i]:
                            st.download_button(
                                label=f"Download {file_name}",
                                data=file_content,
                                file_name=file_name,
                                mime="text/markdown",
                                help=f"Downloads the detailed {file_name.replace('.md', ' report')}."
                            )
                    except FileNotFoundError:
                        with download_cols[i]:
                            st.warning(f"File '{file_name}' not found.")
                            

            except Exception as e:
                st.error("An error occurred during crew execution. Please check the terminal for details (rate limits, API keys, etc.).")
                st.exception(e)


if __name__ == "__main__":
    main()