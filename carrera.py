import random
import time
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS CSS NITRO
# ==========================================
st.set_page_config(
    page_title="Nitro Typing Race", page_icon="🏎️", layout="centered"
)

st.markdown(
    """
    <style>
    /* Fondo estilo Pista Nocturna / Cyberpunk */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%) !important;
        color: #f8fafc !important;
    }

    .main .block-container {
        max-width: 900px !important;
        padding-top: 1.5rem !important;
        background: rgba(15, 23, 42, 0.85) !important;
        border-radius: 16px !important;
        border: 2px solid #22c55e !important;
        box-shadow: 0 0 30px rgba(34, 197, 94, 0.3) !important;
    }

    /* Título estilo carreras */
    .race-title {
        font-family: 'Impact', sans-serif;
        color: #eab308;
        font-size: 2.6rem;
        text-align: center;
        letter-spacing: 2px;
        text-shadow: 3px 3px 0px #000, 0 0 15px rgba(234, 179, 8, 0.6);
        margin-bottom: 20px;
    }

    /* Pista de Carreras */
    .track-container {
        background: #1e293b;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    .lane {
        position: relative;
        height: 45px;
        background: #0f172a;
        border-radius: 8px;
        margin-bottom: 10px;
        border-dash: dashed 2px #475569;
        display: flex;
        align-items: center;
        padding: 0 10px;
        overflow: hidden;
    }

    .car-icon {
        font-size: 28px;
        position: absolute;
        transition: left 0.3s ease-out;
    }

    .finish-line {
        position: absolute;
        right: 15px;
        font-size: 24px;
    }

    /* Cuadro del Texto Objetivo */
    .phrase-box {
        background: #0f172a;
        border-left: 4px solid #3b82f6;
        padding: 18px;
        border-radius: 8px;
        font-size: 20px;
        font-family: 'Courier New', monospace;
        line-height: 1.5;
        color: #f1f5f9;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }

    /* Tarjetas de Métricas */
    .metric-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        border: 1px solid #334155;
    }
    .metric-label { font-size: 12px; color: #94a3b8; text-transform: uppercase; }
    .metric-val { font-size: 26px; font-weight: bold; color: #22c55e; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BASE DE FRASES PARA EL TEST
# ==========================================
PHRASES = [
    (
        "La velocidad de tu teclado determina la victoria en la pista nitro de"
        " carreras."
    ),
    (
        "El código limpio y bien estructurado permite crear aplicaciones"
        " rápidas e interactivas."
    ),
    (
        "Un verdadero desarrollador prueba su código antes de realizar el"
        " primer commit en github."
    ),
    (
        "Superar tus propios límites requiere práctica constante y enfoque en"
        " la precisión del texto."
    ),
]


def safe_rerun():
  if hasattr(st, "rerun"):
    st.rerun()
  elif hasattr(st, "experimental_rerun"):
    st.experimental_rerun()


# ==========================================
# 3. ESTADO DE LA SESIÓN
# ==========================================
if "race_state" not in st.session_state:
  st.session_state.race_state = "READY"  # READY, RACING, FINISHED
if "phrase" not in st.session_state:
  st.session_state.phrase = random.choice(PHRASES)
if "start_time" not in st.session_state:
  st.session_state.start_time = None
if "end_time" not in st.session_state:
  st.session_state.end_time = None
if "ai_progress" not in st.session_state:
  st.session_state.ai_progress = 0


def start_race():
  st.session_state.phrase = random.choice(PHRASES)
  st.session_state.race_state = "RACING"
  st.session_state.start_time = time.time()
  st.session_state.end_time = None
  st.session_state.ai_progress = 0


def reset_race():
  st.session_state.race_state = "READY"
  st.session_state.start_time = None
  st.session_state.end_time = None
  st.session_state.ai_progress = 0


# ==========================================
# 4. INTERFAZ Y LÓGICA DE JUEGO
# ==========================================
st.markdown(
    '<div class="race-title">🏎️ NITRO TYPING RACE 🏁</div>',
    unsafe_allow_html=True,
)

# Calculo del progreso del jugador
user_text = st.session_state.get("user_input_key", "")
target_phrase = st.session_state.phrase

player_progress = 0
if len(target_phrase) > 0 and user_text:
  matching = 0
  for idx, char in enumerate(user_text):
    if idx < len(target_phrase) and char == target_phrase[idx]:
      matching += 1
    else:
      break
  player_progress = min(int((matching / len(target_phrase)) * 85), 85)

# Progreso de la IA (Avanza progresivamente durante la carrera)
if (
    st.session_state.race_state == "RACING"
    and st.session_state.start_time is not None
):
  elapsed = time.time() - st.session_state.start_time
  # La IA avanza aproximadamente a 40 WPM (aprox 3.5% por segundo)
  st.session_state.ai_progress = min(int(elapsed * 3.8), 85)

# Renderizado de la pista de carreras
st.markdown(
    f"""
<div class="track-container">
    <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;">🏎️ TU AUTO (JUGADOR)</div>
    <div class="lane">
        <span class="car-icon" style="left: {player_progress}%;">🏎️</span>
        <span class="finish-line">🏁</span>
    </div>
    <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;">🤖 RIVAL (BOT IA)</div>
    <div class="lane">
        <span class="car-icon" style="left: {st.session_state.ai_progress}%;">🚗</span>
        <span class="finish-line">🏁</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Verificación de final de carrera
if (
    user_text == target_phrase
    and st.session_state.race_state == "RACING"
    and st.session_state.start_time is not None
):
  st.session_state.end_time = time.time()
  st.session_state.race_state = "FINISHED"

# Métricas en tiempo real
wpm = 0
accuracy = 100
if (
    st.session_state.start_time is not None
    and st.session_state.race_state != "READY"
):
  current_end = (
      st.session_state.end_time
      if st.session_state.end_time
      else time.time()
  )
  elapsed_mins = max((current_end - st.session_state.start_time) / 60.0, 0.001)
  words_typed = len(user_text.split())
  wpm = int(words_typed / elapsed_mins)

  if len(user_text) > 0:
    correct = sum(
        1 for a, b in zip(target_phrase, user_text) if a == b
    )
    accuracy = int((correct / len(user_text)) * 100)

c1, c2, c3 = st.columns(3)
with c1:
  st.markdown(
      f"""<div class="metric-card"><div class="metric-label">⚡ Velocidad WPM</div><div class="metric-val">{wpm}</div></div>""",
      unsafe_allow_html=True,
  )
with c2:
  st.markdown(
      f"""<div class="metric-card"><div class="metric-label">🎯 Precisión</div><div class="metric-val">{accuracy}%</div></div>""",
      unsafe_allow_html=True,
  )
with c3:
  status_text = (
      "EN CARRERA 🚦"
      if st.session_state.race_state == "RACING"
      else (
          "¡VICTORIA! 🏆"
          if st.session_state.race_state == "FINISHED"
          else "LISTO 🟢"
      )
  )
  st.markdown(
      f"""<div class="metric-card"><div class="metric-label">Estado</div><div class="metric-val" style="font-size:20px; color:#eab308;">{status_text}</div></div>""",
      unsafe_allow_html=True,
  )

st.write("---")

# Zona de Escribir / Texto Objetivo
if st.session_state.race_state == "READY":
  st.info("💡 Haz clic en **'¡INICIAR CARRERA!'** para comenzar el temporizador.")
  if st.button(
      "🚀 ¡INICIAR CARRERA!", use_container_width=True, type="primary"
  ):
    start_race()
    safe_rerun()

elif st.session_state.race_state == "RACING":
  st.markdown(
      f'<div class="phrase-box">{target_phrase}</div>', unsafe_allow_html=True
  )

  typed_input = st.text_input(
      "Escribe el texto exacto aquí:",
      key="user_input_key",
      placeholder="Comienza a escribir...",
  )

elif st.session_state.race_state == "FINISHED":
  st.markdown(
      f'<div class="phrase-box" style="border-color:#22c55e;">{target_phrase}</div>',
      unsafe_allow_html=True,
  )

  if player_progress >= st.session_state.ai_progress:
    st.balloons()
    st.success(
        f"🎉 **¡GANASTE LA CARRERA!** Completaste la prueba con **{wpm} WPM** y"
        f" **{accuracy}%** de precisión."
    )
  else:
    st.error(
        f"🤖 **La IA cruzó la meta primero.** Lograste **{wpm} WPM**. ¡Vuelve a"
        " intentarlo!"
    )

  if st.button("🔄 REPETIR CARRERA", use_container_width=True):
    reset_race()
    safe_rerun()