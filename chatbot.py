import re
from crew import create_travel_itinerary

conversation_state = {}

def extract_travel_details(message):
    details = {
        'destination': None,
        'duration': None,
        'budget': None,
        'travelers': None,
        'interests': []
    }
    
    message_lower = message.lower()
    
    dest_patterns = [
        r'to\s+([a-zA-Z\s\-,]+?)(?:\s+for|\s+with|\s+and|\s*$)',
        r'in\s+([a-zA-Z\s\-,]+?)(?:\s+for|\s+with|\s+and|\s*$)',
        r'visit\s+([a-zA-Z\s\-,]+?)(?:\s+for|\s+with|\s+and|\s*$)'
    ]
    
    for pattern in dest_patterns:
        match = re.search(pattern, message_lower)
        if match:
            potential_dest = match.group(1).strip()
            if potential_dest and any(c.isalpha() for c in potential_dest):
                details['destination'] = potential_dest
                break
    
    duration_match = re.search(r'(\d+)\s+days?', message_lower)
    if duration_match:
        details['duration'] = int(duration_match.group(1))
    
    budget_match = re.search(r'\$?(\d+[,.]?\d*)', message_lower)
    if budget_match:
        budget_str = budget_match.group(1).replace(',', '')
        try:
            details['budget'] = float(budget_str)
        except ValueError:
            pass
    
    traveler_match = re.search(r'(\d+)\s+(people|persons|travelers)', message_lower)
    if traveler_match:
        details['travelers'] = int(traveler_match.group(1))
    
    interest_keywords = {
        'culture': ['culture', 'museum', 'history', 'art'],
        'adventure': ['adventure', 'hiking', 'outdoor', 'sports'],
        'food': ['food', 'cuisine', 'restaurant', 'dining'],
        'relaxation': ['relax', 'spa', 'beach', 'peaceful'],
        'shopping': ['shopping', 'mall', 'market'],
        'nature': ['nature', 'wildlife', 'parks', 'animals']
    }
    
    for interest, keywords in interest_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            if interest not in details['interests']:
                details['interests'].append(interest)
    
    return details

def get_missing_info(details):
    missing = []
    if not details.get('destination'):
        missing.append("destination")
    if not details.get('duration'):
        missing.append("duration")
    if not details.get('budget'):
        missing.append("budget")
    if not details.get('travelers'):
        missing.append("number of travelers")
    return missing

def generate_response(user_message, user_id="default"):
    global conversation_state
    
    if user_id not in conversation_state:
        conversation_state[user_id] = {
            'destination': None,
            'duration': None,
            'budget': None,
            'travelers': None,
            'interests': []
        }
    
    state = conversation_state[user_id]
    new_details = extract_travel_details(user_message)
    
    for key, value in new_details.items():
        if value:
            if key == 'interests' and value:
                current_interests = state.get('interests', [])
                for interest in value:
                    if interest not in current_interests:
                        current_interests.append(interest)
                state['interests'] = current_interests
            else:
                state[key] = value
    
    missing = get_missing_info(state)
    
    if missing:
        questions = {
            'destination': "Where would you like to go? 🌍",
            'duration': "How many days will you be traveling? 📅",
            'budget': "What's your total budget for the trip? 💰",
            'number of travelers': "How many people will be traveling? 👨‍👩‍👧‍👦"
        }
        return questions.get(missing[0], "Can you tell me more about your travel plans?"), None
    else:
        details = state
        
        if not details.get('interests'):
            details['interests'] = ['culture']
        
        try:
            itinerary = create_travel_itinerary(
                destination=details['destination'],
                duration=details['duration'],
                budget=details['budget'],
                travelers=details['travelers'],
                interests=details['interests']
            )
            
            conversation_state[user_id] = {
                'destination': None,
                'duration': None,
                'budget': None,
                'travelers': None,
                'interests': []
            }
            
            response_text = f"""🎉 **Your Personalized Itinerary for {details['destination']}!**

{itinerary}

- 📍 Destination: {details['destination']}
- 📅 Duration: {details['duration']} days
- 💰 Budget: ${details['budget']}
- 👥 Travelers: {details['travelers']} people
- ❤️ Interests: {', '.join(details['interests'])}"""

            return response_text, details
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}", None