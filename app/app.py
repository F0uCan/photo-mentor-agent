import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import sys
import json
from datetime import date, datetime, timedelta
from pillow_heif import register_heif_opener

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from utils import get_detailed_exif, format_mentor_prompt

HISTORY_FILE = os.path.join(BASE_DIR, "challenges_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
            except:
                return {}
    return {}

def save_success(day):
    history = load_history()
    history[day] = "✅"
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

CHALLENGES = [
    "Leading Lines: Use lines to guide the viewer's eye to the subject.",
    "Frame within a Frame: Find a natural opening (window, doorway, trees) to frame your subject.",
    "Rule of Thirds: Place your main subject off-center on one of the intersecting grid lines.",
    "Golden Hour Glow: Capture the warm light just after sunrise or just before sunset.",
    "Minimalism: Less is more. Use negative space and an isolated subject.",
    "Reflections: Use water, glass, or metal to capture a clear reflection.",
    "Urban Patterns: Find repetitive shapes or textures in the city architecture.",
    "Low Angle (Worm's Eye View): Get down on the ground and shoot upwards."
]

today_str = date.today().isoformat()
challenge_index = hash(today_str) % len(CHALLENGES)
TODAYS_CHALLENGE = CHALLENGES[challenge_index]

register_heif_opener()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ API Key missing. Please check your setup!")
    st.stop()

genai.configure(api_key=API_KEY)

st.set_page_config(page_title="My Photography Journey", page_icon="☀️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFF9F5; }
    .stButton>button {
        border-radius: 25px; border: none; background-color: #FF8C42;
        color: white; font-weight: bold; padding: 0.6rem 2rem; transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #E67E22; transform: scale(1.05); color: white; }
    [data-testid="stSidebar"] { background-color: #FDE8D7; }
    h1, h2, h3 { color: #4A4A4A; font-family: 'Segoe UI', sans-serif; }
    
    .challenge-box {
        background-color: #fff0e6; border-left: 5px solid #FF8C42;
        padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    
    .cal-day {
        display: inline-block; width: 30px; height: 30px;
        line-height: 30px; text-align: center;
        border: 1px solid #FFDAB9; border-radius: 5px;
        margin: 2px; font-size: 0.8rem; color: #4A4A4A;
    }
    .cal-success { background-color: #FF8C42; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

MENTOR_PROMPT = """
Role: The "Friendly Lens" - Photography Mentor & Creative Guide.
Philosophy: Be a friend, not a judge. Use examples to explain technical points.

MANDATORY RESPONSE TEMPLATE:
# 🎨 Artistic Vision: [Creative Title]

## ✨ What Shines
- [Highlight 1 or 2 strengths. Example: "The golden hour light in Ubatuba adds a beautiful warmth."]

## 📐 Composition & Perspectives
- **Current View:** [Analysis of framing]
- **New Ideas:** [Suggest 1 alternative angle or crop to avoid clutter. Example: "Try getting lower for a heroic POV."]

## 🛠️ Technical Insights
- **Settings Choice:** [Comment on EXIF data with context]
- **Pro Tip:** [1 simple technical tweak for next time]

## 🧪 Lightroom Recipe
- **Basic Mix:** [Slider tweaks like Exposure, Shadows, etc.]
- **Creative Touch:** [HSL or Masking suggestion]

---
**Growth Tip:** [One inspiring thought. Example: "Don't fear the shadows; sometimes what you don't show is more interesting than what you do."]

Language: Portuguese(Brazil).
"""

CHALLENGE_JUDGE_PROMPT = """
Role: Photography Challenge Judge.
Task: Determine if the provided image fulfills the specific Daily Challenge criteria described by the user.
Tone: Encouraging but fair.

MANDATORY RESPONSE TEMPLATE:

# 🎯 Challenge Verdict: [ACCEPTED ✅ / TRY AGAIN 🔄]

## 🧐 Judge's Analysis
- [Explain clearly WHY it passed or why it missed the specific criteria of the challenge.]

---
*Keep practicing! Tomorrow is a new challenge.*

Language: Portuguese(Brazil).
"""

with st.sidebar:
    st.title("🎨 Creative Hub")
    
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_choice = st.selectbox("Escolha a 'Vibe' do Mentor:", models, index=0)
    except:
        model_choice = "models/gemini-1.5-flash"
    
    st.markdown("---")

    st.subheader("🏆 Quadro de Medalhas")
    history = load_history()
    
    cols = st.columns(7)
    for i in range(7):
        d = date.today() - timedelta(days=6-i)
        d_str = d.isoformat()
        is_success = d_str in history
        
        label = "✅" if is_success else d.strftime("%d")
        bg_class = "cal-success" if is_success else ""
        
        cols[i].markdown(f'<div class="cal-day {bg_class}">{label}</div>', unsafe_allow_html=True)
    
    st.write(f"**Total de conquistas:** {len(history)}")
    st.markdown("---")

    # Learning Journal
    st.subheader("📓 My Learning Journal")
    journal_entry = st.text_area("O que descobriu hoje?", placeholder="Ex: Percebi que as sombras contam histórias...")
    if st.button("Salvar Nota"):
        if journal_entry:
            journal_path = os.path.join(BASE_DIR, "journal.md")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(journal_path, "a", encoding="utf-8") as f:
                f.write(f"### {timestamp}\n{journal_entry}\n\n")
            st.success("Nota salva!")
        else:
            st.warning("Escreva algo primeiro!")
            
    if os.path.exists(os.path.join(BASE_DIR, "journal.md")):
        with st.expander("📖 Ver meu Progresso"):
            with open(os.path.join(BASE_DIR, "journal.md"), "r", encoding="utf-8") as f:
                st.markdown(f.read())

# 5. Main Content
st.title("☀️ My Photography Journey")

st.markdown(f"""
<div class="challenge-box">
    <h3>🎯 Desafio de Hoje: {TODAYS_CHALLENGE.split(':')[0]}</h3>
    <p>{TODAYS_CHALLENGE.split(':')[1]}</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("✨ Compartilhe sua foto aqui...", type=['jpg', 'jpeg', 'png', 'heic'])

if uploaded_file:
    image = Image.open(uploaded_file)
    exif_data = get_detailed_exif(image)
    device = exif_data.get('Model', 'Sua Câmera')

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(image, caption=f"Capturada com {device}", use_container_width=True)
    with col2:
        st.subheader("📊 Detalhes da Foto")
        if exif_data:
            st.json(exif_data)
        else:
            st.info("Metadados não encontrados.")

    st.write("---")
    st.subheader("🤔 O que o mentor deve fazer?")
    is_challenge_submission = st.checkbox(f"🎯 Enviar para o desafio '{TODAYS_CHALLENGE.split(':')[0]}'!", value=False)
    
    button_label = "✨ Avaliar meu Desafio!" if is_challenge_submission else "✨ Pedir Mentoria"
    
    if st.button(button_label):
        with st.spinner("Analisando..."):
            try:
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    system_instruction=CHALLENGE_JUDGE_PROMPT if is_challenge_submission else MENTOR_PROMPT
                )

                if is_challenge_submission:
                    user_prompt = f"Aqui está minha submissão para o desafio: '{TODAYS_CHALLENGE}'. Eu tive sucesso?"
                else:
                    user_prompt = format_mentor_prompt(device, exif_data)
                
                response = model.generate_content([user_prompt, image])
                
                st.markdown("---")
                st.markdown(response.text)

                res_upper = response.text.upper()
                if is_challenge_submission and ("ACCEPTED" in res_upper or "ACEITO" in res_upper):
                    save_success(today_str)
                    st.balloons()
                    st.success("Desafio concluído! Verifique seu Quadro de Medalhas.")
                    st.rerun()

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

st.markdown("---")
st.caption("A peaceful corner for photography lovers. Stay curious.")