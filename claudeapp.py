import streamlit as st
import os
import random
import requests
import json
from datetime import datetime
from PIL import Image

# Groq API Configuration
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_API_KEY = st.secrets["groq"]["api_key"]

# App title and configuration
st.set_page_config(page_title="Real Estate Content Generator", layout="wide")

# Function to generate content via the Groq API
def generate_content_groq(prompt, platform):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}',
    }
    
    # Platform specific prompts
    platform_prompts = {
        "Facebook": "Generate a promotional real estate post for Facebook. Include a compelling paragraph (100-150 words) that highlights property features and neighborhood benefits. End with 3-4 relevant hashtags.",
        "Instagram": "Create an Instagram caption for a real estate property. Keep it under 100 words, engaging and visually descriptive. Include 5-7 trending real estate hashtags at the end.",
        "LinkedIn": "Craft a professional real estate listing for LinkedIn. Focus on investment potential, property specifications, and market analysis (100-150 words). Include 2-3 professional hashtags."
    }
    
    # Combine platform-specific prompt with user input
    full_prompt = f"{platform_prompts[platform]} Based on this additional information: {prompt}"
    
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": full_prompt}]
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No content generated')
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to get a random image from the folder
def get_random_image(folder_path):
    try:
        # List all files in the folder
        all_files = os.listdir(folder_path)
        
        # Filter out non-image files
        image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            return None
        
        # Select a random image
        selected_image = random.choice(image_files)
        
        # Return the full path
        image_path = os.path.join(folder_path, selected_image)
        return image_path
    except Exception as e:
        st.error(f"Error accessing images: {str(e)}")
        return None

# Custom CSS for better appearance
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #2E7D32;
            text-align: center;
        }
        .platform-selector {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chat-container {
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: 5vh;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }
        .bot-message {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 10px;
        }
        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #E8F5E9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #2E7D32;
            margin-left: 10px;
        }
        .bot-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #E3F2FD;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #1565C0;
            margin-right: 10px;
        }
        .message-bubble {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        .user-bubble {
            background-color: #E8F5E9;
            border: 1px solid #C8E6C9;
        }
        .bot-bubble {
            background-color: #E3F2FD;
            border: 1px solid #BBDEFB;
        }
        .timestamp {
            font-size: 10px;
            color: #757575;
            margin-top: 4px;
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to display chat history
def display_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        timestamp = message["timestamp"]
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <div class="message-bubble user-bubble">
                    <strong>You:</strong> {message['content']}
                    <div class="timestamp">{timestamp}</div>
                </div>
                <div class="user-avatar">U</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <div class="bot-avatar">B</div>
                <div class="message-bubble bot-bubble">
                    <strong>Bot:</strong> {message['content']}
                    <div class="timestamp">{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display content and image
def show_content_and_image(content, platform):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Property Image")
        image_path = get_random_image("images")
        
        if image_path:
            try:
                # Display image directly in Streamlit
                image = Image.open(image_path)
                st.image(image, caption=os.path.basename(image_path), use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying image: {str(e)}")
                st.info("Please make sure your 'images' folder contains valid image files.")
        else:
            st.warning("No images found in the 'images' folder.")
    
    with col2:
        st.subheader(f"{platform} Content")
        st.write(content)
        
        # Add copy button functionality
        if st.button("Schedule"):
            st.success("Scheduling Post now.....")
            

# Main app function
def main():
    # Load custom CSS
    load_css()
    
    # App header
    st.markdown('<h1 class="main-header">Alira</h1>', unsafe_allow_html=True)
    
    # Create two columns for layout
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        
        st.markdown('<div class="platform-selector">', unsafe_allow_html=True)
        
        # Add platform icons for visual appeal
        st.markdown("""
            <h3>Select Platform</h3>
            <div style="display: flex; justify-content: space-around; margin-bottom: 10px;">
                <div style="text-align: center;">
                    <div style="font-size: 24px; color: #1877F2;">📘</div>
                    <div>Facebook</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; color: #E1306C;">📷</div>
                    <div>Instagram</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 24px; color: #0077B5;">💼</div>
                    <div>LinkedIn</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        platform = st.radio(
            "",  # Hide the label since we have custom icons above
            ["Facebook", "Instagram", "LinkedIn"],
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    
    with right_col:
        # Initialize session state for chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        display_chat()
        
        # Input area for user prompt
        user_input = st.chat_input(f"Describe the property to create a {platform} post...")
        
        if user_input:
            timestamp = datetime.now().strftime('%H:%M')
            
            # Add user's message to chat history
            st.session_state.messages.append({
                "role": "user", 
                "content": user_input, 
                "timestamp": timestamp
            })
            
            # Generate content using Groq API
            with st.spinner(f'Creating your {platform} post...'):
                generated_content = generate_content_groq(user_input, platform)
            
            # Handle API errors
            if generated_content.startswith("Error") or generated_content.startswith("An error occurred"):
                st.error(f"Error: {generated_content}")
            else:
                # Add bot's response to chat history
                bot_timestamp = datetime.now().strftime('%H:%M')
                st.session_state.messages.append({
                    'role': 'bot', 
                    'content': generated_content, 
                    'timestamp': bot_timestamp
                })
                
                # Show content and image preview
                show_content_and_image(generated_content, platform)
            
            # Refresh the display to show new messages
            st.rerun()
        
        # Check if there's a recent conversation to display content for
        if st.session_state.messages and len(st.session_state.messages) >= 2:
            last_message = st.session_state.messages[-1]
            if last_message['role'] == 'bot':
                st.subheader("Latest Generated Content")
                with st.expander("View Post Content and Image", expanded=True):
                    show_content_and_image(last_message['content'], platform)

# Run the app
if __name__ == "__main__":
    main()