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
st.set_page_config(page_title="Alira - Real Estate Content Generator", layout="wide")

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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Poppins:wght@300;400;500;600&display=swap');
    
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        color: #123C69;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        color: #4A4A4A;
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }
    
    .platform-selector {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
    }
    
    .content-card {
        background-color: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid #F0F0F0;
    }
    
    .action-button {
        background-color: #123C69;
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
        margin: 5px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 14px;
    }
    
    .action-button:hover {
        background-color: #0B2746;
        box-shadow: 0 4px 10px rgba(18,60,105,0.3);
    }
    
    .input-container {
        background-color: #FFFFFF;
        border-radius: 12px 12px 0 0;
        padding: 15px;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        position: sticky;
        bottom: 0;
        z-index: 100;
        margin-top: 15px;
    }
    
    .chat-history-container {
        background-color: #FFFFFF;
        border-radius: 12px 12px 0 0;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #F0F0F0;
        margin-bottom: 0;
        height: 20vh;
        overflow-y: auto;
    }
    
    .image-container {
        border: 1px solid #EFEFEF;
        border-radius: 10px;
        padding: 15px;
        background-color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    
    .platform-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .platform-name {
        font-size: 15px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
    }
    
    .platform-option {
        cursor: pointer;
        padding: 15px;
        text-align: center;
        border-radius: 10px;
        transition: all 0.3s;
        border: 1px solid transparent;
    }
    
    .platform-option:hover {
        background-color: #F6F9FC;
        border: 1px solid #E6EDF7;
    }
    
    .platform-option.selected {
        background-color: #EBF3FA;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #D6E6F2;
    }
    
    h3 {
        font-family: 'Playfair Display', serif;
        color: #123C69;
        font-weight: 600;
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        border-color: #E6EDF7;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #123C69;
        box-shadow: 0 0 0 1px #123C69;
    }

    /* User Avatar Styles */
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #123C69, #5085A5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        box-shadow: 0 3px 10px rgba(18,60,105,0.2);
        margin-right: 15px;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 15px;
        background-color: #F6F9FC;
        border-radius: 10px;
        border: 1px solid #E6EDF7;
    }
    
    .user-details h4 {
        margin: 0;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #123C69;
    }
    
    .user-details p {
        margin: 0;
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        color: #666;
    }
    
    /* Custom radio button styling */
    div.row-widget.stRadio > div {
        display: flex;
        justify-content: center;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        background-color: #F6F9FC;
        border: 1px solid #E6EDF7;
        border-radius: 8px;
        padding: 10px 20px;
        margin: 0 5px;
        transition: all 0.3s;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: #EBF3FA;
        border-color: #D6E6F2;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] input:checked + div {
        background-color: #123C69;
        border-color: #123C69;
    }

    /* Chat window styles */
    .chat-container {
        background-color: #F9FBFD;
        border-radius: 12px;
        padding: 0;
        margin-bottom: 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .chat-message {
        display: flex;
        margin-bottom: 25px;
        position: relative;
    }
    
    .chat-message:last-child {
        margin-bottom: 0;
    }
    
    .chat-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        flex-shrink: 0;
    }
    
    .user-chat-avatar {
        background: linear-gradient(135deg, #123C69, #5085A5);
        box-shadow: 0 3px 8px rgba(18,60,105,0.2);
    }
    
    .assistant-chat-avatar {
        background: linear-gradient(135deg, #5E8B7E, #2F5D62);
        box-shadow: 0 3px 8px rgba(47,93,98,0.2);
    }
    
    .message-content {
        margin-left: 12px;
        background-color: white;
        border-radius: 0 12px 12px 12px;
        padding: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        border: 1px solid #EFEFEF;
        width: 100%;
    }
    
    .user-message .message-content {
        background-color: #F0F7FF;
        border: 1px solid #D6E6F7;
        border-radius: 12px 12px 12px 0;
    }
    
    .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        border-bottom: 1px solid #EFEFEF;
        padding-bottom: 8px;
    }
    
    .message-name {
        font-weight: 600;
        color: #123C69;
        font-family: 'Poppins', sans-serif;
    }
    
    .message-time {
        font-size: 12px;
        color: #999;
        font-family: 'Poppins', sans-serif;
    }
    
    .message-text {
        font-family: 'Poppins', sans-serif;
        line-height: 1.6;
        color: #333;
        white-space: pre-line;
    }
    
    .user-message .message-text {
        font-weight: 400;
    }
    
    .assistant-message .message-text {
        font-weight: 400;
    }
    
    /* Image inside chat message */
    .assistant-message img {
        max-width: 100%;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #EFEFEF;
    }
    
    /* Message input styling */
    .message-input-container {
        display: flex;
        align-items: flex-end;
        gap: 10px;
        padding: 10px;
        background-color: white;
        border-top: 1px solid #E6EDF7;
    }
    
    .send-button {
        background-color: #123C69;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 8px rgba(18,60,105,0.2);
    }
    
    .send-button:hover {
        background-color: #0B2746;
        transform: scale(1.05);
    }
    
    /* Make the chat history take up available space */
    .chat-history-wrapper {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
    }
    
    /* Hide Streamlit elements we don't want */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1rs6os {visibility: hidden;}
    
    /* Style for empty chat */
    .empty-chat {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #999;
        font-family: 'Poppins', sans-serif;
        padding: 40px;
        text-align: center;
    }
    
    .empty-chat-icon {
        font-size: 60px;
        margin-bottom: 20px;
        color: #E6EDF7;
    }
    
    /* Fixed height for chat container */
    /*.main-chat-container {
        height: calc(100vh - 180px);
        display: flex;
        flex-direction: column;
    }*/
    </style>
    """, unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_css()

    # App header
    st.markdown('<h1 class="main-header">Alira</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Premium AI-powered Real Estate Content Assistant</p>', unsafe_allow_html=True)

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_platform' not in st.session_state:
        st.session_state.current_platform = "Facebook"
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Sarah Mitchell"
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "Senior Real Estate Agent"
    if 'scheduled_posts' not in st.session_state:
        st.session_state.scheduled_posts = []

    # Create two columns for layout
    left_col, right_col = st.columns([1, 3])

    with left_col:
        # User avatar and info
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="user-avatar">SM</div>
            <div class="user-details">
                <h4>{st.session_state.user_name}</h4>
                <p>{st.session_state.user_role}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Platform selector
        st.markdown('<div class="platform-selector">', unsafe_allow_html=True)
        
        # Platform selection with visual icons
        st.markdown("""
            <h3>Select Platform</h3>
            <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
                <div class="platform-option" id="facebook">
                    <div class="platform-icon" style="color: #1877F2;">📘</div>
                    <div class="platform-name">Facebook</div>
                </div>
                <div class="platform-option" id="instagram">
                    <div class="platform-icon" style="color: #E1306C;">📷</div>
                    <div class="platform-name">Instagram</div>
                </div>
                <div class="platform-option" id="linkedin">
                    <div class="platform-icon" style="color: #0077B5;">💼</div>
                    <div class="platform-name">LinkedIn</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        platform = st.radio(
            "",
            ["Facebook", "Instagram", "LinkedIn"],
            horizontal=True,
            key="platform_radio",
            index=["Facebook", "Instagram", "LinkedIn"].index(st.session_state.current_platform)
        )
        st.session_state.current_platform = platform
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent generations section
        st.markdown('<div class="platform-selector">', unsafe_allow_html=True)
        st.subheader("Recent Generations")
        
        # Display scheduled posts (if any)
        if st.session_state.scheduled_posts:
            for idx, post in enumerate(st.session_state.scheduled_posts):
                st.markdown(f"""
                    <div style="padding: 10px; border-bottom: 1px solid #EEE;">
                        <p style="font-weight: 500; margin: 0; color: #123C69;">{post["title"]}</p>
                        <p style="font-size: 12px; color: #888; margin: 0;">{post["platform"]} • {post["time"]}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="padding: 10px; border-bottom: 1px solid #EEE;">
                    <p style="font-weight: 500; margin: 0; color: #123C69;">Luxury Beachfront Villa</p>
                    <p style="font-size: 12px; color: #888; margin: 0;">Facebook • 2 hours ago</p>
                </div>
                <div style="padding: 10px; border-bottom: 1px solid #EEE;">
                    <p style="font-weight: 500; margin: 0; color: #123C69;">Downtown Loft Apartment</p>
                    <p style="font-size: 12px; color: #888; margin: 0;">Instagram • Yesterday</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear chat button
        if st.button("🗑️ Start New Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    with right_col:
        # Main chat container
        st.markdown('<div class="main-chat-container">', unsafe_allow_html=True)
        
        # Chat history container
        st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
        
        # Display chat history or empty state
        if not st.session_state.chat_history:
            st.markdown("""
                <div class="empty-chat">
                    <div class="empty-chat-icon">💬</div>
                    <h3>Start a conversation with Alira</h3>
                    <p>Describe your property to generate premium content for your selected platform.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for idx, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    st.markdown(f"""
                        <div class="chat-message user-message">
                            <div class="chat-avatar user-chat-avatar">SM</div>
                            <div class="message-content">
                                <div class="message-header">
                                    <span class="message-name">{st.session_state.user_name}</span>
                                    <span class="message-time">{message["time"]}</span>
                                </div>
                                <div class="message-text">{message["content"]}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Use a unique key for each button by including the message index
                    
                        
                        
                else:
                    st.markdown('<div class="chat-message assistant-message">', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="chat-avatar assistant-chat-avatar">AI</div>
                        <div class="message-content">
                            <div class="message-header">
                                <span class="message-name">Alira Assistant</span>
                                <span class="message-time">{message["time"]}</span>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    # Display image if present
                    if "image_path" in message and message["image_path"]:
                        try:
                            image = Image.open(message["image_path"])
                            st.image(image, use_container_width=True)
                            
                            # Image metadata
                            st.markdown("""
                                <div style="margin-top: 10px; font-family: 'Poppins', sans-serif; font-size: 13px; color: #666; margin-bottom: 15px;">
                                    <span style="color: #123C69; font-weight: 500;">Image ID:</span> PRO-23854 | 
                                    <span style="color: #123C69; font-weight: 500;">Resolution:</span> Premium Quality |
                                    <span style="color: #123C69; font-weight: 500;">License:</span> Commercial
                                </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error displaying image: {str(e)}")
                            
                    # Display the content
                    st.markdown(f"""
                        <div class="message-text">{message["content"]}</div>
                    """, unsafe_allow_html=True)
                    
                    # Button with unique key for each message
                    if st.button("Schedule", key=f"use_content_btn_{idx}"):
                        # Add to scheduled posts
                        post_title = f"AI Generated Content - {st.session_state.current_platform}"
                        st.session_state.scheduled_posts.append({
                            "title": post_title,
                            "platform": st.session_state.current_platform,
                            "time": "Just now",
                            "content": message["content"]
                        })
                        st.success(f"Content added to scheduled posts for {st.session_state.current_platform}")
                        st.rerun()
                    
                    st.markdown('</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Message input area
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        # Platform indicator
        st.markdown(f"""
            <div style="margin-bottom: 10px; font-family: 'Poppins', sans-serif; font-size: 14px;">
                <span style="color: #123C69; font-weight: 500;">Creating content for:</span> {platform}
            </div>
        """, unsafe_allow_html=True)
        
        # Text input and send button in columns
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_area("", 
                              placeholder=f"Describe your property to create a {platform} post...",
                              height=80,
                              key="message_input")
        
        with col2:
            st.markdown("""
                <div style="height: 80px; display: flex; align-items: center; justify-content: center;">
                    <button class="send-button" id="send_btn" form="chat_form">✓</button>
                </div>
            """, unsafe_allow_html=True)
            send_button = st.button("Send", key="send_msg_btn", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Close main container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle message sending
        if send_button and user_input:
            # Add user message to chat history
            current_time = datetime.now().strftime("%I:%M %p")
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "time": current_time
            })
            
            # Generate AI response
            with st.spinner('Alira is thinking...'):
                # Generate content
                generated_content = generate_content_groq(user_input, platform)
                
                # Get random image
                image_path = get_random_image("images")
                
                # Add AI response to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": generated_content,
                    "time": current_time,
                    "image_path": image_path
                })
            
            # Rerun to update the UI
            st.rerun()

# Run the app
if __name__ == "__main__":
    main()