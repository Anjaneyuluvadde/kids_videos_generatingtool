import streamlit as st
import os
import base64
from modules.renderer import render_video

st.set_page_config(page_title="AI Kid Video Gen", page_icon="🪄", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Premium UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #ffffff;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Premium Typography */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4, #FFE66D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem !important;
        text-align: center;
        padding-top: 2rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        color: #a5b4fc;
        margin-bottom: 3rem;
    }

    /* Styling the Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #e0e7ff !important;
        font-weight: 600;
    }

    /* Glassmorphism Cards */
    div.css-1r6slb0, div.css-12oz5g7 {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div.css-1r6slb0:hover, div.css-12oz5g7:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }

    /* Uploader Styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(99, 102, 241, 0.5) !important;
        border-radius: 20px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #818cf8 !important;
        background-color: rgba(99, 102, 241, 0.1) !important;
    }

    /* Primary Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        box-shadow: 0 10px 20px -10px rgba(236, 72, 153, 0.5);
        width: 100%;
        margin-top: 20px;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 15px 25px -10px rgba(236, 72, 153, 0.8);
    }
    
    /* Info/Warning Boxes */
    div[data-testid="stAlert"] {
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        color: #bfdbfe;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>🪄 Magic Video Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Turn your assets into stunning, beat-synced kids videos instantly.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=60)
    st.markdown("### 🎬 Project Settings")
    template = st.selectbox("Style Template", ["ABC Learning", "Animal Story", "Kids Rhymes", "Motivation", "Cartoon Slideshow"])
    resolution = st.selectbox("Video Format", ["1080x1920 (Shorts/Reels)", "1920x1080 (YouTube Landscape)"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Engine Options")
    use_whisper = st.toggle("🧠 AI Auto-Captions (Whisper)", value=True)
    st.caption("Locally process audio for smart, synchronized subtitles.")
    
    st.markdown("---")
    st.markdown("### 💡 How to use")
    st.info("1. Upload your raw images/videos.\\n2. Add a catchy background track.\\n3. Hit generate and let the magic happen!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 Visual Assets")
    uploaded_images = st.file_uploader("Drop images & video clips here", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'mp4'], help="Support for multiple files.")

with col2:
    st.markdown("### 🎵 Audio Track")
    uploaded_music = st.file_uploader("Drop background music here", type=['mp3', 'wav'], help="Upload an MP3 or WAV file.")


st.markdown("<br>", unsafe_allow_html=True)

# Generate Button Area
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    if st.button("✨ GENERATE MASTERPIECE"):
        if not uploaded_images or not uploaded_music:
            st.warning("⚠️ Please upload both visual assets and an audio track to begin.")
        else:
            with st.status("🎬 Directing your video...", expanded=True) as status:
                st.write("🔍 Analyzing visual assets...")
                st.write("🎶 Syncing transitions to audio beats...")
                if use_whisper:
                    st.write("📝 Generating dynamic subtitles via AI...")
                st.write("🎨 Applying premium effects & rendering...")
                
                try:
                    output_path = render_video(uploaded_images, uploaded_music, template, resolution, use_whisper)
                    status.update(label="✨ Video Rendered Successfully!", state="complete", expanded=False)
                    
                    st.balloons()
                    
                    st.success("Your masterpiece is ready!")
                    
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Final Video",
                            data=file,
                            file_name="magic_video_output.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                except Exception as e:
                    status.update(label="Render failed", state="error", expanded=True)
                    st.error(f"Error details: {str(e)}")
