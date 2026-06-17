import streamlit as st
import os
from google.genai import types
from personas import PERSONAS

def render_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@500;700;900&display=swap');
        
        /* Global Page background & default font configuration */
        .stApp {
            background-color: #0F172A;
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Ensure high contrast for all major text headings */
        h1, h2, h3, h4, h5, h6 {
            color: #F8FAFC !important;
            font-family: 'Outfit', sans-serif;
        }
        
        /* High contrast for all widget labels (form texts) */
        label[data-testid="stWidgetLabel"] p {
            color: #F1F5F9 !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }
        
        /* Radio buttons selection options */
        div[data-testid="stRadio"] label p {
            color: #E2E8F0 !important;
            font-size: 0.95rem !important;
        }
        
        /* Markdown paragraph blocks */
        .stMarkdown p, .stMarkdown li, .stMarkdown ol, .stMarkdown ul {
            color: #E2E8F0 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        
        /* Style Chat bubbles to guarantee perfect contrast */
        div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stChatMessage"] li {
            color: #F8FAFC !important;
            font-size: 1rem !important;
        }
        
        /* Override dark text inside input boxes and apply a customized slate styling */
        div[data-testid="stTextInput"] input {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid #475569 !important;
            font-size: 1rem !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #F59E0B !important;
            box-shadow: 0 0 0 1px #F59E0B !important;
        }

        /* Primary buttons (Submit, Connect, Selected panels) */
        div.stButton > button[kind="primary"], .stButton > button[kind="primaryFormSubmit"] {
            background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25) !important;
            transition: all 0.3s ease-in-out !important;
            width: 100% !important;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.35) !important;
            transform: translateY(-1px);
            color: #FFFFFF !important;
        }

        /* Secondary buttons (Unselected teachers, Reset button) */
        div.stButton > button[kind="secondary"] {
            background-color: #1E293B !important;
            color: #E2E8F0 !important;
            border: 1px solid #475569 !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        
        div.stButton > button[kind="secondary"]:hover {
            border-color: #F59E0B !important;
            color: #F59E0B !important;
            background-color: #334155 !important;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15) !important;
        }

        /* Sidebar Background & Sidebar Text color overrides */
        section[data-testid="stSidebar"] {
            background-color: #1E293B !important;
            border-right: 1px solid #334155;
        }
        section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
            color: #F1F5F9 !important;
        }
        
        /* Title Gradient styling */
        .main-title {
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent !important;
            font-size: 2.8rem;
            font-weight: 900;
            text-align: center;
            margin-top: -10px;
            margin-bottom: 5px;
            letter-spacing: -0.05em;
        }
        
        .subtitle {
            text-align: center;
            color: #94A3B8 !important;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Questionnaire Card Layout styling - targeting native Streamlit border container */
        div[data-testid="stVerticalBlockBorderContainer"] {
            background-color: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid #334155 !important;
            border-radius: 16px !important;
            padding: 2.5rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            margin: 0 auto !important;
            max-width: 900px !important;
        }
        
        .profile-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

def run_dashboard(client):
    # Apply CSS styling
    render_css()
    
    # Main Header
    st.markdown("<h1 class='main-title'>☕ Chai aur Code Learning Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Get concepts explained in terms you understand, customized for 2026.</p>", unsafe_allow_html=True)
    
    # Initialize session state tracking
    if "questionnaire_completed" not in st.session_state:
        st.session_state.questionnaire_completed = False
    if "selected_teacher" not in st.session_state:
        st.session_state.selected_teacher = "Hitesh (Educator)"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}

    # Flow 1: Questionnaire Page
    if not st.session_state.questionnaire_completed:
        with st.container(border=True):
            st.subheader("📋 Step 1: Select Your AI Teacher & Setup Profile")
        st.write("Pick your custom teacher persona. Each teacher specializes in their own field of expertise:")
        
        # Draw dynamic columns for teacher options
        t_cols = st.columns(len(PERSONAS))
        selected_teacher = st.session_state.selected_teacher
        
        for i, (key, info) in enumerate(PERSONAS.items()):
            with t_cols[i]:
                st.markdown(f"""
                <div style="text-align: center; background: #1E293B; padding: 15px; border-radius: 12px; border: 2px solid {info['color'] if selected_teacher == key else '#334155'}; min-height: 250px;">
                    <span style="font-size: 3rem;">{info['avatar']}</span>
                    <h4 style="color: {info['color']}; margin: 10px 0 5px 0;">{info['name']}</h4>
                    <p style="font-size: 0.85rem; color: #E2E8F0; min-height: 35px; margin-bottom: 2px;"><strong>Domain:</strong> {info['domain']}</p>
                    <p style="font-size: 0.8rem; color: #CBD5E1; min-height: 70px;">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Choose {info['name']}", key=f"btn_{i}", use_container_width=True, type="primary" if selected_teacher == key else "secondary"):
                    st.session_state.selected_teacher = key
                    st.rerun()

        st.markdown("<hr style='border-color: #334155;'/>", unsafe_allow_html=True)
        st.write("Tell us about your learning needs:")
        
        current_persona = PERSONAS[selected_teacher]
        
        # # User details with session state keys to prevent resets on rerun
        # p_level = st.select_slider(
        #     "Aapka current knowledge level kya hai? (Experience Level)",
        #     options=["Beginner / absolute fresher", "Intermediate (Know some basics)", "Advanced (In-depth queries)"],
        #     key="user_level"
        # )
        
        p_interest = st.text_input(
            f"Aap kis topic ke baare mein seekhna chahte hain? ({current_persona['domain']})",
            placeholder=current_persona['topic_placeholder'],
            key="user_interest"
        )
        
        p_preference = st.radio(
            "Aapko seekhna kaise pasand hai? (Learning Preference)",
            options=[
                "Kahaani aur analogies ke saath (Storytelling analogies)",
                "Step-by-step structure explanations (Logical breakdowns)",
                "Direct Question-Answer (Q&A sessions)"
            ],
            key="user_preference"
        )
        
        if st.button("🚀 Connect with my AI Teacher", key="btn_connect_teacher", use_container_width=True, type="primary"):
            if not p_interest.strip():
                st.warning("Please specify a topic you want to learn today!")
            else:
                st.session_state.user_profile = {
                    # "level": p_level,
                    "interest": p_interest,
                    "preference": p_preference
                }
                st.session_state.questionnaire_completed = True
                
                # Dynamic initial greeting call
                teacher_name = current_persona['name']
                greeting_instruction = (
                    f"Introduce yourself as {teacher_name}, specializing in {current_persona['domain']}. "
                    f"The user has filled a profile:\n"
                    # f"- Experience: {p_level}\n"
                    f"- Interest Topic: {p_interest}\n"
                    f"- Learning Style: {p_preference}\n\n"
                    f"Write a warm, short initial greeting (under 100 words) in Hinglish. "
                    f"Greet the user, confirm that you will explain things in your domain of expertise ({current_persona['domain']}), "
                    f"and invite them to ask their first question about {p_interest}. Do not write code."
                )
                
                with st.spinner("Connecting with your teacher and generating greeting..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=greeting_instruction,
                            config=types.GenerateContentConfig(temperature=0.7)
                        )
                        st.session_state.messages = [{"role": "assistant", "content": response.text}]
                    except Exception as e:
                        st.session_state.messages = [{
                            "role": "assistant", 
                            "content": f"Hello! Main aapka AI advisor hu. Let's discuss your interest topic: **{p_interest}** in {current_persona['domain']}. Puchiye apna pehla sawaal!"
                        }]
                st.rerun()

    # Flow 2: Chat Mode
    else:
        current_persona = PERSONAS[st.session_state.selected_teacher]
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 3.5rem;">☕</span>
                <h3 style="margin: 0; color: #F59E0B; font-family: 'Outfit', sans-serif;">Chai aur Code</h3>
                <p style="color: #94A3B8; font-size: 0.85rem;">2026 AI Study Portal</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='border-color: #334155;'/>", unsafe_allow_html=True)
            st.subheader("👤 Your Learning Profile")
            st.write(f"**Level:** {st.session_state.user_profile['level']}")
            st.write(f"**Topic:** {st.session_state.user_profile['interest']}")
            st.write(f"**Style:** {st.session_state.user_profile['preference']}")
            
            # Display active teacher sidebar badge
            t_name = current_persona['name']
            t_avatar = current_persona['avatar']
            t_color = current_persona['color']
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid {t_color}; border-radius: 8px; padding: 12px; margin-top: 15px;">
                <div style="font-size: 2rem; text-align: center;">{t_avatar}</div>
                <h4 style="color: {t_color}; text-align: center; margin: 5px 0;">{t_name}</h4>
                <p style="font-size: 0.82rem; color: #E2E8F0; text-align: center; margin-bottom: 4px;"><strong>Domain:</strong> {current_persona['domain']}</p>
                <p style="font-size: 0.8rem; color: #CBD5E1; text-align: center; margin-bottom: 0;">{current_persona['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='border-color: #334155;'/>", unsafe_allow_html=True)
            st.subheader("🚀 Active 2026 Cohorts")
            st.markdown("""
            - 🤖 **Agentic AI & Multi-Agent Systems** (Jan-Mar 2026)
            - ⚙️ **Production LLMOps & Fine-Tuning** (Apr-Jun 2026)
            - 🌐 **Modern Full-Stack & Web3** (Jun-Aug 2026)
            """)
            
            st.markdown("<hr style='border-color: #334155;'/>", unsafe_allow_html=True)
            if st.button("🔄 Reset & Change Teacher", key="btn_reset_teacher", use_container_width=True, type="secondary"):
                st.session_state.questionnaire_completed = False
                st.session_state.messages = []
                st.session_state.user_profile = {}
                st.rerun()

        st.write(f"### Chatting with {current_persona['name']} ({current_persona['domain']})")
        
        # Render message history
        for msg in st.session_state.messages:
            avatar = current_persona['avatar'] if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                
        # Prep prompt system instructions
        profile_context = (
            f"\n\n[USER PROFILE CONTEXT:\n"
            f"- Target Topic: {st.session_state.user_profile['interest']}\n"
            f"- Knowledge Level: {st.session_state.user_profile['level']}\n"
            f"- Learning Preference: {st.session_state.user_profile['preference']}\n"
            f"Custom explain concepts for this background. Remember to answer ONLY within your field of expertise ({current_persona['domain']})!]\n"
        )
        
        base_prompt = current_persona["prompt"]
        if st.session_state.selected_teacher == "Hitesh (Educator)":
            # Load Hitesh system prompt dynamically from file
            system_prompt_path = os.path.join(os.path.dirname(__file__), "system-prompt.txt")
            try:
                with open(system_prompt_path, "r", encoding="utf-8") as f:
                    base_hitesh_prompt = f.read()
            except FileNotFoundError:
                base_hitesh_prompt = "You are Hitesh Choudhary, an experienced coding instructor teaching in Hinglish."
                
            system_instruction = (
                f"{base_hitesh_prompt}\n\n"
                f"[CRITICAL FORMAT INSTRUCTION: Ignore any previous rule requiring responses in a JSON list format. "
                f"Write your response directly as standard formatted Markdown. Do NOT wrap your message in JSON format. "
                f"Always speak in Hinglish and use the Hitesh Choudhary persona.]"
                f"{profile_context}"
            )
        else:
            system_instruction = base_prompt + profile_context

        # Text input chat box
        if user_query := st.chat_input(f"Ask {current_persona['name']} about {st.session_state.user_profile['interest']}..."):
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_query)
                
            st.session_state.messages.append({"role": "user", "content": user_query})
            
            with st.chat_message("assistant", avatar=current_persona['avatar']):
                message_placeholder = st.empty()
                full_response = ""
                
                try:
                    contents = []
                    for m in st.session_state.messages:
                        if m == st.session_state.messages[0] and m["role"] == "assistant":
                            continue
                        contents.append(
                            types.Content(
                                role="user" if m["role"] == "user" else "model",
                                parts=[types.Part.from_text(text=m["content"])]
                            )
                        )
                    
                    response_stream = client.models.generate_content_stream(
                        model="gemini-2.5-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        )
                    )
                    
                    for chunk in response_stream:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                        
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"Oops! Response generation error: {str(e)}"
                    message_placeholder.markdown(full_response)
                    
            st.session_state.messages.append({"role": "assistant", "content": full_response})
