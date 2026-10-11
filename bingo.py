# =========================================================
#  ZONA DE JUEGOS VIP — Sin contador de giros visible
# =========================================================
import json
import os
import random
import time
from datetime import datetime
from urllib.parse import quote

import streamlit as st

# =========================================================
#  CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="ZONA DE JUEGOS VIP 🎰",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

CLAVE_ADMIN    = "Juan*316*"
WHATSAPP_ADMIN = "584120139004"
WHATSAPP_INFO  = "584242004015"
CONTACTO_INFO  = "0424-200-4015"

APUESTA_MINIMA_ANIMALITOS = 200
OPCIONES_APUESTA          = [200, 400, 600, 800, 1000]
RATE_COMISION             = 0.30
RATE_POTE                 = 0.70

PRECIO_BINGO_FIG     = 200
COMISION_BINGO_FIG   = 60
PREMIO_BINGO_FIG     = 100

PRECIO_BINGO_LLENO   = 500
COMISION_BINGO_LLENO = 100
PREMIO_BINGO_LLENO   = 400

GIROS_ALTERNADOS = [10, 14]
ARCHIVO_DATOS    = "datos_vip.json"

DATOS_PAGO = [
    ("🏦 Banco",    "Banesco (0134)"),
    ("🪪 Cédula",   "V-6.865.149"),
    ("📱 Teléfono", "0412-0139004"),
    ("👤 Titular",  "Juan"),
]

ANIMALITOS = [
    "01 🐬 Delfín", "02 🐋 Ballena", "03 🐊 Caimán", "04 🐻 Oso", "05 🐘 Elefante",
    "06 🐅 Tigre",  "07 🦁 León",     "08 🦅 Águila", "09 🐵 Mono", "10 🐎 Caballo",
    "11 🐂 Toro",   "12 🐕 Perro",    "13 🐈 Gato",   "14 🐓 Gallo","15 🐍 Serpiente",
    "16 🦓 Cebra",  "17 🦒 Jirafa",   "18 🦊 Zorro",  "19 🐺 Lobo", "20 🦌 Venado",
]

# =========================================================
#  ESTILOS VIP PREMIUM
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Poppins:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp {
    background:
        radial-gradient(1400px 700px at 5% -10%, #3b0764 0%, transparent 55%),
        radial-gradient(1200px 650px at 105% 5%, #831843 0%, transparent 55%),
        radial-gradient(900px 600px at 50% 120%, #0369a1 0%, transparent 50%),
        linear-gradient(180deg, #05060d 0%, #0a0b18 100%);
    color: #f1f5f9;
}
h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif; letter-spacing: 1px; }
h1 { color: #00ffcc !important; text-shadow: 0 0 22px rgba(0,255,204,.55); }
h2 { color: #ff007f !important; text-shadow: 0 0 18px rgba(255,0,127,.55); }
h3, h4 { color: #a78bfa !important; }
p, li, span, label { color: #cbd5e1; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #05060d);
    border-right: 1px solid #1f2c47;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #ff007f 0%, #7928ca 100%);
    color: #fff !important; font-weight: 800; border: 0;
    border-radius: 14px; padding: .65rem 1.6rem;
    box-shadow: 0 6px 24px rgba(255, 0, 127, 0.45);
    transition: transform .2s ease, box-shadow .2s ease;
    letter-spacing: .5px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 34px rgba(121, 40, 202, 0.7);
}
.stButton > button:disabled {
    background: linear-gradient(90deg, #4b5563, #374151) !important;
    box-shadow: none !important; opacity: .55;
}
.stTextInput input, .stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #0f172a !important; color: #e8eefc !important;
    border-radius: 12px !important; border: 1px solid #243352 !important;
}

/* ============ TARJETAS ============ */
.metric-card {
    background: linear-gradient(135deg, rgba(20,27,45,.95), rgba(10,14,23,.95));
    border: 2px solid rgba(255, 0, 127, 0.35);
    padding: 22px; border-radius: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,.55);
    text-align: center; margin-bottom: 12px;
}
.metric-card h3 { color: #00ffcc !important; font-size: 14px; letter-spacing: 2px; margin: 0; }
.metric-card h1 { color: #ffd700 !important; font-size: 34px; margin: 8px 0 0 0; }

/* ============ POTE GIGANTE ============ */
.pote-gigante {
    background: linear-gradient(135deg, #facc15, #f59e0b, #dc2626);
    border: 4px solid #fef08a;
    border-radius: 28px;
    padding: 34px 40px;
    text-align: center;
    margin: 18px 0;
    box-shadow: 0 0 70px rgba(250,204,21,.7);
    animation: brillar 1.4s ease-in-out infinite alternate;
}
@keyframes brillar {
    from { box-shadow: 0 0 40px rgba(250,204,21,.6); transform: scale(1); }
    to   { box-shadow: 0 0 95px rgba(250,204,21,1);   transform: scale(1.02); }
}
.pote-label  { color:#1a1205; font-size:16px; font-weight:900; letter-spacing:5px; }
.pote-monto  { color:#fff; font-size:82px; font-weight:900;
               font-family:'Orbitron', sans-serif;
               text-shadow: 5px 5px 0 #7c2d12, 0 0 40px rgba(255,255,255,.5);
               margin: 8px 0; letter-spacing: 2px; }
.pote-sub    { color:#1a1205; font-size:14px; font-weight:700; }

/* ============ JACKPOT BANNER ============ */
.jackpot-banner {
    background: linear-gradient(90deg, #f5af19 0%, #f12711 100%);
    padding: 15px; border-radius: 12px; text-align: center;
    font-size: 22px; font-weight: 900; color: #fff;
    box-shadow: 0 0 25px rgba(245, 175, 25, 0.6);
    animation: pulse 2s infinite; letter-spacing: 2px;
}
@keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.02); } }

/* ============ CARTÓN ============ */
.carton { display:inline-block; background:#0f172a; padding:12px;
    border-radius:16px; border:2px solid #243352;
    box-shadow: 0 14px 30px rgba(0,0,0,.5); }
.fila { display:flex; gap:6px; margin-bottom:6px; }
.celda { width:54px; height:54px; display:flex; align-items:center;
    justify-content:center; border-radius:10px; background:#16213a;
    color:#c7d2fe; font-weight:700; font-size:16px; border:1px solid #26355a; }
.celda.marcada { background: linear-gradient(135deg,#ff007f,#7928ca);
    color:#fff; border-color:#ff007f; box-shadow: 0 0 12px rgba(255,0,127,.7); }
.celda.libre { background: linear-gradient(135deg,#ffd166,#f59e0b);
    color:#1a1205; border-color:#ffd166; }
.letra { width:54px; height:38px; display:flex; align-items:center;
    justify-content:center; border-radius:10px;
    background: linear-gradient(135deg,#7c3aed,#4c1d95);
    color:#fff; font-weight:800; font-size:18px; }

/* ============ PILLS ============ */
.pill { display:inline-block; padding:4px 12px; border-radius:999px;
    font-size:12px; font-weight:700; letter-spacing:.5px; }
.pill-ok   { background:#14532d; color:#86efac; border:1px solid #22c55e; }
.pill-wait { background:#78350f; color:#fcd34d; border:1px solid #f59e0b; }
.pill-no   { background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; }
.pill-info { background:#1e3a8a; color:#bfdbfe; border:1px solid #3b82f6; }
.pill-vip  { background:#4c1d95; color:#ddd6fe; border:1px solid #8b5cf6; }

/* ============ ANUNCIO DE GANADOR PREMIUM ============ */
.ganador-pantalla {
    background:
        radial-gradient(900px 400px at 50% 0%, #fef08a 0%, transparent 60%),
        linear-gradient(135deg, #facc15 0%, #f59e0b 45%, #dc2626 100%);
    border: 6px solid #fef08a;
    border-radius: 32px;
    padding: 50px 40px;
    text-align: center;
    margin: 24px 0;
    box-shadow: 0 0 90px rgba(250,204,21,.85), inset 0 0 60px rgba(255,255,255,.3);
    animation: brillarGanador 1.2s ease-in-out infinite alternate;
    position: relative;
    overflow: hidden;
}
@keyframes brillarGanador {
    from { box-shadow: 0 0 50px rgba(250,204,21,.7), inset 0 0 40px rgba(255,255,255,.2); }
    to   { box-shadow: 0 0 120px rgba(250,204,21,1), inset 0 0 80px rgba(255,255,255,.4); }
}
.ganador-pantalla::before {
    content: "";
    position: absolute; inset: 0;
    background: repeating-linear-gradient(45deg,
        rgba(255,255,255,.08) 0px, rgba(255,255,255,.08) 20px,
        transparent 20px, transparent 40px);
    animation: rayas 6s linear infinite;
    pointer-events: none;
}
@keyframes rayas { from { transform: translateX(0); } to { transform: translateX(80px); } }

.ganador-trofeo {
    font-size: 90px;
    animation: girar 2s ease-in-out infinite;
    display: inline-block;
}
@keyframes girar {
    0%,100% { transform: rotate(-10deg) scale(1); }
    50%     { transform: rotate(10deg) scale(1.15); }
}
.ganador-titulo {
    color: #1a1205; font-size: 32px; font-weight: 900;
    letter-spacing: 6px; margin: 10px 0;
    font-family: 'Orbitron', sans-serif;
    text-shadow: 2px 2px 0 #fff;
}
.ganador-nombre {
    color: #fff; font-size: 56px; font-weight: 900;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 4px; margin: 14px 0;
    text-shadow: 4px 4px 0 #7c2d12, 0 0 30px rgba(255,255,255,.9);
}
.ganador-animal {
    color: #1a1205; font-size: 24px; font-weight: 800;
    margin: 10px 0;
    background: rgba(255,255,255,.6);
    padding: 10px 24px; border-radius: 999px;
    display: inline-block;
}
.ganador-monto {
    color: #fff; font-size: 62px; font-weight: 900;
    font-family: 'Orbitron', sans-serif;
    text-shadow: 4px 4px 0 #7c2d12, 0 0 40px rgba(255,255,255,.9);
    margin: 12px 0 4px 0;
}
.ganador-sub {
    color: #1a1205; font-size: 16px; font-weight: 700;
    letter-spacing: 3px;
}

/* ============ INFO BOX ============ */
.info-box {
    background: linear-gradient(135deg, #065f46, #064e3b);
    border: 2px solid #34d399; border-radius: 16px;
    padding: 16px 20px; text-align: center; margin: 12px 0;
}
.info-titulo { color:#d1fae5; font-size:13px; letter-spacing:2px; font-weight:700; }
.info-valor  { color:#fff; font-size:22px; font-weight:800; margin-top:6px; }
.info-resto  { color:#a7f3d0; font-size:13px; margin-top:6px; }

/* ============ GRID ANIMALITOS ============ */
.animal-grid { display:grid; grid-template-columns: repeat(5, 1fr); gap:8px; }
.animal-btn {
    background:#131c31; border:1px solid #26355a; border-radius:12px;
    padding:10px; text-align:center; font-weight:700; color:#cbd5e1;
}
.animal-btn.win {
    background: linear-gradient(135deg,#22c55e,#15803d);
    color:#04140a; border-color:#22c55e;
    box-shadow: 0 0 18px rgba(34,197,94,.7);
}
.animal-btn.taken {
    background: linear-gradient(135deg,#7f1d1d,#450a0a);
    color:#fca5a5; border-color:#ef4444;
    text-decoration: line-through; opacity: .85;
}

/* ============ RULETA ============ */
.ruleta-frame {
    background: radial-gradient(circle at 50% 40%, #1e1b4b, #05060d);
    border: 4px solid #a78bfa; border-radius: 24px;
    padding: 30px; text-align: center;
    box-shadow: 0 0 50px rgba(167,139,250,.55);
    margin: 12px 0;
}
.ruleta-numero {
    font-family: 'Orbitron', sans-serif;
    font-size: 90px; font-weight: 900;
    color: #ffd700;
    text-shadow: 0 0 30px rgba(255,215,0,.8);
}
.ruleta-label { color:#a78bfa; font-size:14px; letter-spacing:3px; font-weight:700; }

hr { border-color:#1f2c47; }
</style>
""", unsafe_allow_html=True)

# =========================================================
#  PERSISTENCIA
# =========================================================
def guardar_datos():
    datos = {
        "pote_animalitos":     ss.pote_animalitos,
        "giros_realizados":    ss.giros_realizados,
        "indice_giros":        ss.indice_giros,
        "historial_ruleta":    ss.historial_ruleta,
        "apuestas_animalitos": ss.apuestas_animalitos,
        "cartones_fig":        ss.cartones_fig,
        "balotas_fig":         ss.balotas_fig,
        "pausa_fig":           ss.pausa_fig,
        "ganador_fig":         ss.ganador_fig,
        "cartones_lleno":      ss.cartones_lleno,
        "balotas_lleno":       ss.balotas_lleno,
        "pausa_lleno":         ss.pausa_lleno,
        "ganador_lleno":       ss.ganador_lleno,
        "comision_total":      ss.comision_total,
        "ganadores_hist":      ss.ganadores_hist,
        "contador_carton":     ss.contador_carton,
        "referencias_usadas":  ss.referencias_usadas,
        "ultimo_ganador_ruleta": ss.ultimo_ganador_ruleta,
        "hora_ultima_ronda":   ss.hora_ultima_ronda,
    }
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"No se pudo guardar: {e}")


def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return {}
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# =========================================================
#  ESTADO
# =========================================================
ss = st.session_state
_d = cargar_datos()

ss.setdefault("pote_animalitos",     _d.get("pote_animalitos", 0))
ss.setdefault("giros_realizados",    _d.get("giros_realizados", 0))
ss.setdefault("indice_giros",        _d.get("indice_giros", 0))
ss.setdefault("historial_ruleta",    _d.get("historial_ruleta", []))
ss.setdefault("apuestas_animalitos", _d.get("apuestas_animalitos", []))

ss.setdefault("cartones_fig", _d.get("cartones_fig", []))
ss.setdefault("balotas_fig",  _d.get("balotas_fig", []))
ss.setdefault("pausa_fig",    _d.get("pausa_fig", False))
ss.setdefault("ganador_fig",  _d.get("ganador_fig", None))

ss.setdefault("cartones_lleno", _d.get("cartones_lleno", []))
ss.setdefault("balotas_lleno",  _d.get("balotas_lleno", []))
ss.setdefault("pausa_lleno",    _d.get("pausa_lleno", False))
ss.setdefault("ganador_lleno",  _d.get("ganador_lleno", None))

ss.setdefault("comision_total",     _d.get("comision_total", 0))
ss.setdefault("ganadores_hist",     _d.get("ganadores_hist", []))
ss.setdefault("contador_carton",    _d.get("contador_carton", 5000))
ss.setdefault("referencias_usadas", _d.get("referencias_usadas", {}))

ss.setdefault("ultimo_ganador_ruleta", _d.get("ultimo_ganador_ruleta", None))
ss.setdefault("hora_ultima_ronda",     _d.get("hora_ultima_ronda", None))

ss.setdefault("admin_ok", False)
ss.setdefault("auto_fig", False)
ss.setdefault("auto_lleno", False)
ss.setdefault("ultimo_canto_fig", 0.0)
ss.setdefault("ultimo_canto_lleno", 0.0)
ss.setdefault("intervalo_fig", 5)
ss.setdefault("intervalo_lleno", 5)

# =========================================================
#  HELPERS
# =========================================================
def guardar():
    guardar_datos()


def nuevo_codigo(prefijo="V"):
    ss.contador_carton += 1
    return f"{prefijo}-{ss.contador_carton}"


def normalizar_ref(ref):
    return str(ref).strip().lower()


def referencia_ya_usada(ref):
    r = normalizar_ref(ref)
    if not r:
        return False
    return r in ss.referencias_usadas


def referencia_ya_usada_donde(ref):
    r = normalizar_ref(ref)
    info = ss.referencias_usadas.get(r)
    if not info:
        return None
    return f"{info.get('juego','—')} (por {info.get('jugador','—')})"


def registrar_referencia(ref, juego, jugador, extra=""):
    r = normalizar_ref(ref)
    ss.referencias_usadas[r] = {
        "juego": juego,
        "jugador": jugador,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "extra": extra,
    }
    guardar()


def animalito_ya_vendido(animal):
    if not animal:
        return False
    return any(a["animal"] == animal for a in ss.apuestas_animalitos)


def quien_tiene_animalito(animal):
    for a in ss.apuestas_animalitos:
        if a["animal"] == animal:
            return a["nombre"]
    return None


def animalitos_disponibles():
    vendidos = {a["animal"] for a in ss.apuestas_animalitos}
    return [a for a in ANIMALITOS if a not in vendidos]


def giros_de_esta_ronda():
    return GIROS_ALTERNADOS[ss.indice_giros % len(GIROS_ALTERNADOS)]


def avanzar_indice_giros():
    ss.indice_giros += 1


def generar_carton_bingo():
    rangos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    cols = [random.sample(range(a, b + 1), 5) for a, b in rangos]
    m = [[cols[c][f] for c in range(5)] for f in range(5)]
    m[2][2] = "★"
    return m


def carton_html(matriz, balotas):
    letras = ["B", "I", "N", "G", "O"]
    html = '<div class="carton"><div class="fila">' + "".join(
        f'<div class="letra">{l}</div>' for l in letras) + '</div>'
    for fila in matriz:
        html += '<div class="fila">'
        for v in fila:
            if v == "★":
                html += '<div class="celda libre">★</div>'
            elif v in balotas:
                html += f'<div class="celda marcada">{v}</div>'
            else:
                html += f'<div class="celda">{v}</div>'
        html += '</div>'
    html += '</div>'
    return html


def contar_figura(matriz, balotas):
    m = lambda v: v == "★" or v in balotas
    esquinas = all(m(matriz[r][c]) for r, c in [(0,0),(0,4),(4,0),(4,4)])
    diag = all(m(matriz[i][i]) for i in range(5))
    diag2 = all(m(matriz[i][4-i]) for i in range(5))
    lat_i = all(m(matriz[i][0]) for i in range(5))
    lat_d = all(m(matriz[i][4]) for i in range(5))
    return {"4 Esquinas": esquinas,
            "Diagonal": diag or diag2,
            "Lateral": lat_i or lat_d}


def carton_lleno(matriz, balotas):
    return all(v == "★" or v in balotas for fila in matriz for v in fila)


def link_whatsapp(numero, mensaje):
    return f"https://wa.me/{numero}?text={quote(mensaje)}"


def boton_whatsapp(numero, mensaje, texto, color="#25d366"):
    return (
        f'<a href="{link_whatsapp(numero, mensaje)}" target="_blank" '
        f'style="display:inline-block;padding:12px 22px;margin:6px 6px 6px 0;'
        f'background:linear-gradient(135deg,{color},#128c7e);color:#fff;'
        f'font-weight:700;border-radius:12px;text-decoration:none;'
        f'box-shadow:0 8px 20px rgba(37,211,102,.4)">'
        f'{texto}</a>'
    )


def reproducir(nombre_archivo):
    if os.path.exists(nombre_archivo):
        try:
            st.audio(nombre_archivo, format="audio/mp3", autoplay=True)
        except Exception:
            pass


def registrar_ganador(area, detalle):
    ss.ganadores_hist.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "area": area,
        **detalle,
    })
    guardar()


def anuncio_ganador_premium(nombre, animal, premio):
    st.markdown(
        f'<div class="ganador-pantalla">'
        f'<div class="ganador-trofeo">🏆</div>'
        f'<div class="ganador-titulo">¡TENEMOS GANADOR!</div>'
        f'<div class="ganador-nombre">{nombre}</div>'
        f'<div class="ganador-animal">🐾 Acertó: {animal}</div>'
        f'<div class="ganador-monto">{premio:,} Bs</div>'
        f'<div class="ganador-sub">¡FELICIDADES! 🎉</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.balloons()
    reproducir("ganador.mp3")


def seccion_historial_ganadores(titulo="🏆 SALÓN DE LA FAMA",
                                filtro_area=None,
                                limite=10):
    st.markdown(f"### {titulo}")
    st.caption("Aquí están los últimos ganadores reales de la sala. "
               "¡El pote SÍ se entrega! 🎉")

    historial = ss.ganadores_hist
    if filtro_area:
        historial = [g for g in historial if g.get("area","").startswith(filtro_area)]

    if not historial:
        st.info("📭 Aún no hay ganadores registrados. ¡Sé el primero en ganar! 🍀")
        return

    historial_ord = sorted(historial, key=lambda x: x.get("fecha",""), reverse=True)[:limite]

    ultimo = historial_ord[0]
    st.markdown(
        f'<div class="ganador-pantalla" style="padding: 30px 26px; margin: 10px 0;">'
        f'<div class="ganador-trofeo" style="font-size:60px">🏆</div>'
        f'<div class="ganador-titulo" style="font-size:20px">'
        f'ÚLTIMO GANADOR · {ultimo.get("area","—")}</div>'
        f'<div class="ganador-nombre" style="font-size:38px">'
        f'{ultimo.get("jugador","—")}</div>'
        f'<div class="ganador-monto" style="font-size:44px">'
        f'{ultimo.get("premio_bs",0):,} Bs</div>'
        f'<div class="ganador-sub" style="font-size:12px">'
        f'📅 {ultimo.get("fecha","—")}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    if len(historial_ord) > 1:
        st.markdown("#### 📜 Ganadores anteriores")
        for g in historial_ord[1:]:
            st.markdown(
                f'<div class="metric-card" style="text-align:left;padding:12px 16px;'
                f'margin-bottom:8px;border-color:rgba(255,215,0,.35)">'
                f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap">'
                f'<div>🏆 <b>{g.get("jugador","—")}</b></div>'
                f'<div style="color:#ffd700;font-weight:900">'
                f'{g.get("premio_bs",0):,} Bs</div>'
                f'</div>'
                f'<div style="color:#94a3b8;font-size:12px;margin-top:4px">'
                f'🎮 {g.get("area","—")} · 🐾 {g.get("detalle","—")} · '
                f'📅 {g.get("fecha","—")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with st.expander(f"🔎 Ver TODOS los ganadores ({len(historial)})"):
        for g in sorted(historial, key=lambda x: x.get("fecha",""), reverse=True):
            st.markdown(
                f'<div class="metric-card" style="text-align:left;padding:10px 14px;'
                f'margin-bottom:6px">'
                f'🏆 <b>{g.get("jugador","—")}</b> · '
                f'<span style="color:#ffd700;font-weight:900">'
                f'{g.get("premio_bs",0):,} Bs</span> · '
                f'<span style="color:#94a3b8">{g.get("fecha","—")}</span><br>'
                f'<span style="color:#a78bfa;font-size:12px">'
                f'{g.get("area","—")} · {g.get("detalle","—")}</span>'
                f'</div>',
                unsafe_allow_html=True
            )


# =========================================================
#  BARRA LATERAL
# =========================================================
with st.sidebar:
    st.markdown("# 💎 SALA VIP")
    st.markdown("---")
    juego = st.radio(
        "Selecciona tu juego:",
        [
            "🔥 Ruleta de Animalitos",
            "🎟️ Bingo Figuras (200 Bs)",
            "🏆 Bingo Cartón Lleno (500 Bs)",
            "💼 Panel del Organizador",
        ],
        key="menu_principal",
    )
    st.markdown("---")

    st.markdown(
        f'<div class="info-box" style="background:linear-gradient(135deg,#7c2d12,#450a0a);'
        f'border-color:#f59e0b">'
        f'<div class="info-titulo" style="color:#fef3c7">💰 POTE ACTUAL</div>'
        f'<div class="info-valor" style="color:#ffd700;font-size:26px">'
        f'{ss.pote_animalitos} Bs</div>'
        f'</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="info-box">'
        f'<div class="info-titulo">📞 INFORMACIÓN</div>'
        f'<div class="info-valor">{CONTACTO_INFO}</div>'
        f'<div class="info-resto">Para cualquier duda</div>'
        f'</div>', unsafe_allow_html=True)
    st.markdown(
        boton_whatsapp(
            WHATSAPP_INFO,
            "Hola, necesito información sobre la Zona de Juegos VIP.",
            "📲 WhatsApp",
        ),
        unsafe_allow_html=True,
    )
    st.caption("🔞 Juega responsablemente.")


# =========================================================
#  PÁGINA · 🔥 RULETA DE ANIMALITOS
# =========================================================
if juego == "🔥 Ruleta de Animalitos":
    st.title("🔥 RULETA DE ANIMALITOS")

    # ============ ANUNCIO DE GANADOR ============
    if ss.ultimo_ganador_ruleta:
        g = ss.ultimo_ganador_ruleta
        anuncio_ganador_premium(g["nombre"], g["animal"], g["premio"])

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✔️ Ya lo vi, continuar", use_container_width=True,
                         key="btn_cerrar_ganador"):
                ss.ultimo_ganador_ruleta = None
                guardar()
                st.rerun()
        with col_b:
            msg = (f"🎉 ¡FELICIDADES {g['nombre']}! Ganaste el pote de la "
                   f"Ruleta de Animalitos con {g['animal']}. "
                   f"Premio: {g['premio']} Bs 🏆")
            st.markdown(
                boton_whatsapp(g.get("telefono", WHATSAPP_ADMIN), msg,
                                "📲 Felicitar al ganador"),
                unsafe_allow_html=True)
        st.markdown("---")

    # ============ POTE GIGANTE ============
    st.markdown(
        f'<div class="pote-gigante">'
        f'<div class="pote-label">💰 POTE ACUMULADO EN VIVO 💰</div>'
        f'<div class="pote-monto">{ss.pote_animalitos:,} Bs</div>'
        f'<div class="pote-sub">¡El ganador se lo lleva TODO! 🏆</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ⏱️ Variable interna (no se muestra)
    total_esta_ronda = giros_de_esta_ronda()

    # ============ COMPRA ============
    col_izq, col_der = st.columns([1.1, 1], gap="large")

    with col_izq:
        st.markdown("### 📝 Registra tu apuesta")
        with st.form("form_animalito", clear_on_submit=True):
            nombre = st.text_input("Tu nombre y apellido:")
            telefono = st.text_input("Tu WhatsApp (ej: 584120000000):")

            disponibles = animalitos_disponibles()
            if not disponibles:
                st.error("🚫 **¡Todos los animalitos ya fueron vendidos en esta ronda!**")
                animal_elegido = None
            else:
                st.info(f"🎟️ **Animalitos disponibles: {len(disponibles)} "
                        f"de {len(ANIMALITOS)}**")
                animal_elegido = st.selectbox(
                    "Elige tu animalito 🐾 (solo disponibles):",
                    disponibles,
                )

            monto_str = st.selectbox(
                f"💰 Monto de tu apuesta (mínimo {APUESTA_MINIMA_ANIMALITOS} Bs):",
                [f"{x} Bs" for x in OPCIONES_APUESTA],
            )
            monto_int = int(monto_str.replace(" Bs", ""))
            aporte_pote = int(monto_int * RATE_POTE)
            comision_calc = int(monto_int * RATE_COMISION)
            st.caption(
                f"💡 **{monto_int} Bs** → **{aporte_pote} Bs** al pote · "
                f"comisión de {comision_calc} Bs."
            )

            ref_pago = st.text_input("N° de referencia del Pago Móvil:")
            btn = st.form_submit_button("🌟 ¡Apostar y jugar!")

        if btn:
            if not animal_elegido:
                st.error("🚫 No hay animalitos disponibles. Espera la próxima ronda.")
            elif nombre.strip() and telefono.strip() and ref_pago.strip():
                if referencia_ya_usada(ref_pago):
                    donde = referencia_ya_usada_donde(ref_pago)
                    st.error(f"⛔ La referencia **{ref_pago}** ya fue registrada "
                             f"en **{donde}**.")
                elif animalito_ya_vendido(animal_elegido):
                    dueno = quien_tiene_animalito(animal_elegido)
                    st.error(f"🚫 El animalito **{animal_elegido}** ya fue vendido "
                             f"a **{dueno}**. Elige otro.")
                else:
                    apuesta = {
                        "id": f"AP-{len(ss.apuestas_animalitos)+1}",
                        "nombre": nombre.strip(),
                        "telefono": telefono.strip(),
                        "animal": animal_elegido,
                        "referencia": ref_pago.strip(),
                        "monto": monto_int,
                        "aporte_pote": aporte_pote,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    ss.apuestas_animalitos.append(apuesta)
                    ss.pote_animalitos += aporte_pote
                    ss.comision_total += comision_calc
                    registrar_referencia(ref_pago, "Ruleta de Animalitos",
                                         nombre.strip(),
                                         extra=f"Animal: {animal_elegido} · "
                                               f"Monto: {monto_int} Bs")
                    st.balloons()
                    st.success(f"🎉 ¡Apuesta registrada, **{nombre}**! "
                               f"Vas con el **{animal_elegido}** por "
                               f"**{monto_int} Bs**.")
                    msg = (f"Hola, soy {nombre}. Acabo de apostar {monto_int} Bs "
                           f"en la Ruleta de Animalitos. Elegí: {animal_elegido}. "
                           f"Referencia: {ref_pago}.")
                    st.markdown(boton_whatsapp(WHATSAPP_ADMIN, msg,
                                                "📲 Avisar por WhatsApp"),
                                unsafe_allow_html=True)
            else:
                st.error("⚠️ Completa todos los campos.")

    with col_der:
        st.markdown("### 📱 Datos para Pago Móvil")
        filas = "".join(
            f"<tr><td style='padding:6px 14px 6px 0;color:#94a3b8'>{k}</td>"
            f"<td style='padding:6px 0;color:#e8eefc;font-weight:600'>{v}</td></tr>"
            for k, v in DATOS_PAGO)
        st.markdown(
            f'<div class="metric-card"><table style="border-collapse:collapse">{filas}</table>'
            f'<p style="margin-top:10px;color:#ffd700;font-weight:800">'
            f'Monto mínimo: {APUESTA_MINIMA_ANIMALITOS} Bs</p>'
            f'<p style="color:#94a3b8;font-size:13px">200, 400, 600, 800 o 1000 Bs</p></div>',
            unsafe_allow_html=True)

    # ============ ANIMALITOS VENDIDOS ============
    if ss.apuestas_animalitos:
        st.markdown("---")
        st.markdown("### 🎯 Animalitos ya vendidos en esta ronda")
        for a in ss.apuestas_animalitos:
            st.markdown(
                f'<div class="metric-card" style="text-align:left;padding:10px 16px">'
                f'🐾 <b>{a["animal"]}</b> · '
                f'👤 {a["nombre"]} · '
                f'💰 {a.get("monto",200)} Bs'
                f'</div>', unsafe_allow_html=True)

    # ============ RULETA EN VIVO ============
    st.markdown("---")
    st.markdown("### 🎰 Ruleta en vivo")

    if ss.historial_ruleta:
        ultimo = ss.historial_ruleta[-1]
        st.markdown(
            f'<div class="ruleta-frame">'
            f'<div class="ruleta-label">ÚLTIMO ANIMALITO</div>'
            f'<div class="ruleta-numero">{ultimo.split(" ")[0]}</div>'
            f'<div style="font-size:34px;margin-top:8px">{ultimo.split(" ",1)[1]}</div>'
            f'</div>', unsafe_allow_html=True)
    else:
        st.info("⏳ El organizador aún no ha iniciado los giros.")

    st.markdown("### 📜 Historial de la ronda actual")
    if ss.historial_ruleta:
        st.markdown(" ➔ ".join(
            f'<span style="display:inline-block;margin:4px;padding:8px 14px;'
            f'border-radius:10px;background:#16213a;color:#ffd700;font-weight:700;'
            f'border:1px solid #26355a">{a}</span>' for a in ss.historial_ruleta),
            unsafe_allow_html=True)
    else:
        st.caption("Sin giros todavía.")

    # ============ GRID DE ANIMALITOS ============
    st.markdown("### 🐾 Los 20 animalitos")
    ganadores_ronda = set(ss.historial_ruleta)
    vendidos = {a["animal"] for a in ss.apuestas_animalitos}

    grid_html = '<div class="animal-grid">'
    for a in ANIMALITOS:
        if a in ganadores_ronda:
            cls = "animal-btn win"
        elif a in vendidos:
            cls = "animal-btn taken"
        else:
            cls = "animal-btn"
        grid_html += f'<div class="{cls}">{a}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # ============ SALÓN DE LA FAMA ============
    st.markdown("---")
    seccion_historial_ganadores(
        titulo="🏆 SALÓN DE LA FAMA — RULETA DE ANIMALITOS",
        filtro_area="Ruleta",
        limite=5,
    )


# =========================================================
#  PÁGINA · 🎟️ BINGO FIGURAS
# =========================================================
elif juego == "🎟️ Bingo Figuras (200 Bs)":
    st.title("🎟️ BINGO FIGURAS")
    st.markdown(f"### Costo: **{PRECIO_BINGO_FIG} Bs** · Premio: "
                f"**{PREMIO_BINGO_FIG} Bs** (50% del pozo)")
    st.markdown("---")

    if ss.ganador_fig:
        g = ss.ganador_fig
        anuncio_ganador_premium(g["nombre"], g.get("figura","Bingo"), PREMIO_BINGO_FIG)
        if st.button("✔️ Continuar", key="btn_cerrar_ganador_fig"):
            ss.ganador_fig = None
            ss.pausa_fig = False
            ss.balotas_fig = []
            guardar()
            st.rerun()
        st.markdown("---")

    st.markdown("### 🎯 Figuras ganadoras")
    st.info("4 Esquinas · Diagonal · Línea Lateral (B u O)")

    col_a, col_b = st.columns([1.1, 1], gap="large")
    with col_a:
        st.markdown("### 🛒 Compra tu cartón")
        with st.form("form_fig", clear_on_submit=True):
            nombre = st.text_input("Nombre y apellido:")
            telefono = st.text_input("Tu WhatsApp (ej: 584120000000):")
            ref = st.text_input("N° referencia del Pago Móvil:")
            enviar = st.form_submit_button(f"💳 Comprar cartón ({PRECIO_BINGO_FIG} Bs)")

        if enviar:
            if nombre.strip() and telefono.strip() and ref.strip():
                if referencia_ya_usada(ref):
                    donde = referencia_ya_usada_donde(ref)
                    st.error(f"⛔ Referencia ya registrada en **{donde}**.")
                else:
                    carton = {
                        "id": nuevo_codigo("F"),
                        "codigo": nuevo_codigo("FIG"),
                        "nombre": nombre.strip(),
                        "telefono": telefono.strip(),
                        "referencia": ref.strip(),
                        "matriz": generar_carton_bingo(),
                        "estado": "Pendiente",
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    ss.cartones_fig.append(carton)
                    ss.comision_total += COMISION_BINGO_FIG
                    registrar_referencia(ref, "Bingo Figuras", nombre.strip(),
                                         extra=f"Cartón: {carton['codigo']}")
                    st.success(f"✅ Cartón **{carton['codigo']}** registrado.")
                    msg = (f"Hola, soy {nombre}. Compré un cartón de Bingo Figuras. "
                           f"Código: {carton['codigo']}. Ref: {ref}.")
                    st.markdown(boton_whatsapp(WHATSAPP_ADMIN, msg,
                                                "📲 Avisar por WhatsApp"),
                                unsafe_allow_html=True)
            else:
                st.error("⚠️ Completa todos los campos.")

    with col_b:
        st.markdown("### 📱 Datos para Pago Móvil")
        filas = "".join(
            f"<tr><td style='padding:6px 14px 6px 0;color:#94a3b8'>{k}</td>"
            f"<td style='padding:6px 0;color:#e8eefc;font-weight:600'>{v}</td></tr>"
            for k, v in DATOS_PAGO)
        st.markdown(
            f'<div class="metric-card"><table style="border-collapse:collapse">{filas}</table>'
            f'<p style="margin-top:10px;color:#ffd700;font-weight:800">'
            f'Monto: {PRECIO_BINGO_FIG} Bs</p></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Consulta tu cartón")
    busqueda = st.text_input("Ingresa tu código o teléfono:", key="busq_fig")
    if busqueda:
        encontrados = [c for c in ss.cartones_fig
                       if busqueda.strip() in c["telefono"]
                       or busqueda.upper() == c.get("codigo","").upper()]
        if not encontrados:
            st.warning("No se encontraron cartones con ese dato.")
        for c in encontrados:
            color = {"Activo":"pill-ok", "Pendiente":"pill-wait"}.get(c["estado"],"pill-info")
            st.markdown(
                f'<div class="metric-card" style="text-align:left">'
                f'<span class="pill {color}">{c["estado"]}</span> '
                f'<span class="pill pill-vip">{c["codigo"]}</span> · {c["nombre"]}'
                f'</div>', unsafe_allow_html=True)
            st.markdown(carton_html(c["matriz"], ss.balotas_fig),
                        unsafe_allow_html=True)
            st.markdown("---")

    st.markdown("---")
    seccion_historial_ganadores(
        titulo="🏆 SALÓN DE LA FAMA — BINGO FIGURAS",
        filtro_area="Bingo Figuras",
        limite=5,
    )


# =========================================================
#  PÁGINA · 🏆 BINGO CARTÓN LLENO
# =========================================================
elif juego == "🏆 Bingo Cartón Lleno (500 Bs)":
    st.title("🏆 BINGO ÉLITE — CARTÓN LLENO")
    st.markdown(f"### Costo: **{PRECIO_BINGO_LLENO} Bs** · Premio: "
                f"**{PREMIO_BINGO_LLENO} Bs** (80% del pozo)")
    st.markdown("---")

    if ss.ganador_lleno:
        g = ss.ganador_lleno
        anuncio_ganador_premium(g["nombre"], "Cartón Lleno", PREMIO_BINGO_LLENO)
        if st.button("✔️ Continuar", key="btn_cerrar_ganador_lleno"):
            ss.ganador_lleno = None
            ss.pausa_lleno = False
            ss.balotas_lleno = []
            guardar()
            st.rerun()
        st.markdown("---")

    col_a, col_b = st.columns([1.1, 1], gap="large")
    with col_a:
        st.markdown("### 🛒 Compra tu cartón Élite")
        with st.form("form_lleno", clear_on_submit=True):
            nombre = st.text_input("Nombre y apellido:")
            telefono = st.text_input("Tu WhatsApp (ej: 584120000000):")
            ref = st.text_input("N° referencia del Pago Móvil:")
            enviar = st.form_submit_button(f"💎 Comprar cartón ({PRECIO_BINGO_LLENO} Bs)")

        if enviar:
            if nombre.strip() and telefono.strip() and ref.strip():
                if referencia_ya_usada(ref):
                    donde = referencia_ya_usada_donde(ref)
                    st.error(f"⛔ Referencia ya registrada en **{donde}**.")
                else:
                    carton = {
                        "id": nuevo_codigo("L"),
                        "codigo": nuevo_codigo("LLENO"),
                        "nombre": nombre.strip(),
                        "telefono": telefono.strip(),
                        "referencia": ref.strip(),
                        "matriz": generar_carton_bingo(),
                        "estado": "Pendiente",
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    ss.cartones_lleno.append(carton)
                    ss.comision_total += COMISION_BINGO_LLENO
                    registrar_referencia(ref, "Bingo Cartón Lleno",
                                         nombre.strip(),
                                         extra=f"Cartón: {carton['codigo']}")
                    st.success(f"✅ Cartón **{carton['codigo']}** registrado.")
                    msg = (f"Hola, soy {nombre}. Compré un cartón Élite. "
                           f"Código: {carton['codigo']}. Ref: {ref}.")
                    st.markdown(boton_whatsapp(WHATSAPP_ADMIN, msg,
                                                "📲 Avisar por WhatsApp"),
                                unsafe_allow_html=True)
            else:
                st.error("⚠️ Completa todos los campos.")

    with col_b:
        st.markdown("### 📱 Datos para Pago Móvil")
        filas = "".join(
            f"<tr><td style='padding:6px 14px 6px 0;color:#94a3b8'>{k}</td>"
            f"<td style='padding:6px 0;color:#e8eefc;font-weight:600'>{v}</td></tr>"
            for k, v in DATOS_PAGO)
        st.markdown(
            f'<div class="metric-card"><table style="border-collapse:collapse">{filas}</table>'
            f'<p style="margin-top:10px;color:#ffd700;font-weight:800">'
            f'Monto: {PRECIO_BINGO_LLENO} Bs</p></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Consulta tu cartón Élite")
    busqueda = st.text_input("Ingresa tu código o teléfono:", key="busq_lleno")
    if busqueda:
        encontrados = [c for c in ss.cartones_lleno
                       if busqueda.strip() in c["telefono"]
                       or busqueda.upper() == c.get("codigo","").upper()]
        if not encontrados:
            st.warning("No se encontraron cartones con ese dato.")
        for c in encontrados:
            color = {"Activo":"pill-ok", "Pendiente":"pill-wait"}.get(c["estado"],"pill-info")
            st.markdown(
                f'<div class="metric-card" style="text-align:left">'
                f'<span class="pill {color}">{c["estado"]}</span> '
                f'<span class="pill pill-vip">{c["codigo"]}</span> · {c["nombre"]}'
                f'</div>', unsafe_allow_html=True)
            st.markdown(carton_html(c["matriz"], ss.balotas_lleno),
                        unsafe_allow_html=True)
            st.markdown("---")

    st.markdown("---")
    seccion_historial_ganadores(
        titulo="🏆 SALÓN DE LA FAMA — BINGO CARTÓN LLENO",
        filtro_area="Bingo Lleno",
        limite=5,
    )


# =========================================================
#  PÁGINA · 💼 PANEL DEL ORGANIZADOR
# =========================================================
else:
    st.title("💼 PANEL DEL ORGANIZADOR")
    st.markdown("---")

    if not ss.admin_ok:
        with st.form("login_admin"):
            clave = st.text_input("Contraseña de administrador:", type="password")
            entrar = st.form_submit_button("🔐 Ingresar")
        if entrar:
            if clave == CLAVE_ADMIN:
                ss.admin_ok = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta.")
        st.stop()

    st.markdown(
        f'<div class="metric-card" style="border-color:rgba(255,215,0,.5)">'
        f'<h3>💰 COMISIONES TOTALES</h3>'
        f'<h1>{ss.comision_total:,} Bs</h1></div>',
        unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔥 Ruleta", "🎟️ Bingo Figuras", "🏆 Bingo Lleno",
        "📊 Historial", "🔍 Referencias"
    ])

    # ============== TAB 1: RULETA ==============
    with tab1:
        st.markdown("### 🎰 Control de la Ruleta")

        # 🎯 Variable interna para la lógica de entrega
        total_ronda = giros_de_esta_ronda()

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🎰 Girar ruleta", use_container_width=True,
                         key="btn_girar"):
                resultado = random.choice(ANIMALITOS)

                placeholder = st.empty()
                for _ in range(18):
                    temp = random.choice(ANIMALITOS)
                    placeholder.markdown(
                        f'<div class="ruleta-frame">'
                        f'<div class="ruleta-label">GIRANDO...</div>'
                        f'<div class="ruleta-numero">{temp.split(" ")[0]}</div>'
                        f'</div>', unsafe_allow_html=True)
                    time.sleep(0.07)
                placeholder.markdown(
                    f'<div class="ruleta-frame">'
                    f'<div class="ruleta-label">🎉 ¡RESULTADO!</div>'
                    f'<div class="ruleta-numero">{resultado.split(" ")[0]}</div>'
                    f'<div style="font-size:30px;margin-top:8px">'
                    f'{resultado.split(" ",1)[1]}</div>'
                    f'</div>', unsafe_allow_html=True)
                reproducir("ruleta.mp3")

                ss.historial_ruleta.append(resultado)
                ss.giros_realizados += 1
                guardar()

                if ss.giros_realizados >= total_ronda:
                    posibles = [a for a in ss.apuestas_animalitos
                                if a["animal"] in ss.historial_ruleta]

                    if posibles:
                        ganador = random.choice(posibles)
                        premio = ss.pote_animalitos

                        ss.ultimo_ganador_ruleta = {
                            "nombre":   ganador["nombre"],
                            "telefono": ganador["telefono"],
                            "animal":   ganador["animal"],
                            "premio":   premio,
                            "fecha":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }

                        registrar_ganador("Ruleta", {
                            "jugador":  ganador["nombre"],
                            "telefono": ganador["telefono"],
                            "detalle":  f"Acertó {ganador['animal']} · "
                                        f"Apostó {ganador.get('monto',200)} Bs",
                            "premio_bs": premio,
                        })

                        st.balloons()
                        st.success(
                            f"🎉 ¡EL GANADOR ES **{ganador['nombre']}**! "
                            f"Acertó el {ganador['animal']} y se lleva "
                            f"TODO el pote: **{premio} Bs** 🏆"
                        )

                        ss.pote_animalitos = 0
                    else:
                        st.warning(
                            f"😔 Nadie acertó en esta ronda. El pote se "
                            f"ACUMULA para la próxima (Pote actual: "
                            f"{ss.pote_animalitos} Bs)."
                        )

                    ss.giros_realizados = 0
                    ss.historial_ruleta = []
                    ss.apuestas_animalitos = []
                    avanzar_indice_giros()
                    ss.hora_ultima_ronda = datetime.now().strftime("%Y-%m-%d %H:%M")
                    guardar()

        with c2:
            if st.button("🔄 Nueva ronda (limpiar)", use_container_width=True,
                         key="btn_nueva_ruleta"):
                ss.giros_realizados = 0
                ss.historial_ruleta = []
                ss.apuestas_animalitos = []
                avanzar_indice_giros()
                guardar()
                st.success("🔄 Ronda reiniciada.")
                st.rerun()

        with c3:
            if st.button("💎 Entregar pote manual", use_container_width=True,
                         key="btn_entregar_pote"):
                if ss.apuestas_animalitos:
                    ganador = random.choice(ss.apuestas_animalitos)
                    premio = ss.pote_animalitos
                    ss.ultimo_ganador_ruleta = {
                        "nombre":   ganador["nombre"],
                        "telefono": ganador["telefono"],
                        "animal":   ganador["animal"],
                        "premio":   premio,
                        "fecha":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    registrar_ganador("Ruleta (manual)", {
                        "jugador":  ganador["nombre"],
                        "telefono": ganador["telefono"],
                        "detalle":  f"Manual · {ganador['animal']}",
                        "premio_bs": premio,
                    })
                    ss.pote_animalitos = 0
                    guardar()
                    st.success(f"Pote entregado a {ganador['nombre']}.")
                    st.rerun()
                else:
                    st.warning("No hay apuestas registradas.")

        st.markdown("---")
        st.markdown("### 📝 Apuestas actuales")
        if ss.apuestas_animalitos:
            total_apostado = sum(a.get("monto", 200) for a in ss.apuestas_animalitos)
            st.markdown(f"**Total apostado en esta ronda:** {total_apostado} Bs")
            for a in ss.apuestas_animalitos:
                st.markdown(
                    f"- 🐾 **{a['animal']}** · {a['nombre']} · "
                    f"💰 {a.get('monto',200)} Bs · "
                    f"📞 {a['telefono']} · Ref: {a['referencia']}")
        else:
            st.caption("Sin apuestas en esta ronda.")

        st.markdown("---")
        st.markdown("### 📜 Historial de la ronda")
        if ss.historial_ruleta:
            st.markdown(" ➔ ".join(ss.historial_ruleta))
        else:
            st.caption("Sin giros.")

    # ============== TAB 2: BINGO FIGURAS ==============
    with tab2:
        st.markdown("### 🎟️ Control del Bingo Figuras")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ Cantar balota", use_container_width=True,
                         key="btn_cantar_fig", disabled=ss.pausa_fig):
                disp = [n for n in range(1, 76) if n not in ss.balotas_fig]
                if disp:
                    nueva = random.choice(disp)
                    ss.balotas_fig.append(nueva)
                    for c in ss.cartones_fig:
                        if c["estado"] != "Activo":
                            continue
                        figs = contar_figura(c["matriz"], ss.balotas_fig)
                        logros = [k for k, v in figs.items() if v]
                        if logros:
                            ss.ganador_fig = {
                                "codigo": c["codigo"],
                                "nombre": c["nombre"],
                                "telefono": c["telefono"],
                                "figura": ", ".join(logros),
                            }
                            ss.pausa_fig = True
                            registrar_ganador("Bingo Figuras", {
                                "jugador": c["nombre"],
                                "telefono": c["telefono"],
                                "detalle": c["codigo"],
                                "premio_bs": PREMIO_BINGO_FIG,
                            })
                            break
                    guardar()
                    st.rerun()
        with c2:
            if st.button("🔄 Reiniciar balotas", use_container_width=True,
                         key="btn_reset_fig"):
                ss.balotas_fig = []
                ss.pausa_fig = False
                ss.ganador_fig = None
                guardar()
                st.rerun()
        with c3:
            etiqueta = "⏸️ Detener auto" if ss.auto_fig else "⚡ Auto sorteo"
            if st.button(etiqueta, use_container_width=True, key="btn_auto_fig"):
                ss.auto_fig = not ss.auto_fig
                ss.ultimo_canto_fig = time.time()
                st.rerun()

        if ss.auto_fig:
            st.caption("⏱️ Auto sorteo activo")
            if time.time() - ss.ultimo_canto_fig >= ss.intervalo_fig:
                disp = [n for n in range(1, 76) if n not in ss.balotas_fig]
                if disp:
                    nueva = random.choice(disp)
                    ss.balotas_fig.append(nueva)
                    for c in ss.cartones_fig:
                        if c["estado"] != "Activo":
                            continue
                        figs = contar_figura(c["matriz"], ss.balotas_fig)
                        logros = [k for k, v in figs.items() if v]
                        if logros:
                            ss.ganador_fig = {
                                "codigo": c["codigo"],
                                "nombre": c["nombre"],
                                "telefono": c["telefono"],
                                "figura": ", ".join(logros),
                            }
                            ss.pausa_fig = True
                            ss.auto_fig = False
                            registrar_ganador("Bingo Figuras", {
                                "jugador": c["nombre"],
                                "telefono": c["telefono"],
                                "detalle": c["codigo"],
                                "premio_bs": PREMIO_BINGO_FIG,
                            })
                            break
                    ss.ultimo_canto_fig = time.time()
                    guardar()
                time.sleep(0.5)
                st.rerun()

        st.markdown(f"**Balotas cantadas:** {len(ss.balotas_fig)}/75")

        st.markdown("### 🎫 Cartones registrados")
        for c in ss.cartones_fig:
            color = {"Activo":"pill-ok","Pendiente":"pill-wait"}.get(c["estado"],"pill-info")
            with st.expander(f"{c['codigo']} · {c['nombre']} · {c['estado']}"):
                st.markdown(
                    f'<span class="pill {color}">{c["estado"]}</span> '
                    f'📞 {c["telefono"]} · Ref: {c["referencia"]}',
                    unsafe_allow_html=True)
                st.markdown(carton_html(c["matriz"], ss.balotas_fig),
                            unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1:
                    if c["estado"] != "Activo":
                        if st.button("✅ Activar", key=f"act_fig_{c['id']}"):
                            c["estado"] = "Activo"
                            guardar()
                            st.rerun()
                with b2:
                    if st.button("🗑️ Eliminar", key=f"del_fig_{c['id']}"):
                        ss.cartones_fig.remove(c)
                        guardar()
                        st.rerun()

    # ============== TAB 3: BINGO LLENO ==============
    with tab3:
        st.markdown("### 🏆 Control del Bingo Cartón Lleno")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶️ Cantar balota", use_container_width=True,
                         key="btn_cantar_lleno", disabled=ss.pausa_lleno):
                disp = [n for n in range(1, 76) if n not in ss.balotas_lleno]
                if disp:
                    nueva = random.choice(disp)
                    ss.balotas_lleno.append(nueva)
                    for c in ss.cartones_lleno:
                        if c["estado"] != "Activo":
                            continue
                        if carton_lleno(c["matriz"], ss.balotas_lleno):
                            ss.ganador_lleno = {
                                "codigo": c["codigo"],
                                "nombre": c["nombre"],
                                "telefono": c["telefono"],
                            }
                            ss.pausa_lleno = True
                            registrar_ganador("Bingo Lleno", {
                                "jugador": c["nombre"],
                                "telefono": c["telefono"],
                                "detalle": c["codigo"],
                                "premio_bs": PREMIO_BINGO_LLENO,
                            })
                            break
                    guardar()
                    st.rerun()
        with c2:
            if st.button("🔄 Reiniciar balotas", use_container_width=True,
                         key="btn_reset_lleno"):
                ss.balotas_lleno = []
                ss.pausa_lleno = False
                ss.ganador_lleno = None
                guardar()
                st.rerun()
        with c3:
            etiqueta = "⏸️ Detener auto" if ss.auto_lleno else "⚡ Auto sorteo"
            if st.button(etiqueta, use_container_width=True, key="btn_auto_lleno"):
                ss.auto_lleno = not ss.auto_lleno
                ss.ultimo_canto_lleno = time.time()
                st.rerun()

        if ss.auto_lleno:
            st.caption("⏱️ Auto sorteo activo")
            if time.time() - ss.ultimo_canto_lleno >= ss.intervalo_lleno:
                disp = [n for n in range(1, 76) if n not in ss.balotas_lleno]
                if disp:
                    nueva = random.choice(disp)
                    ss.balotas_lleno.append(nueva)
                    for c in ss.cartones_lleno:
                        if c["estado"] != "Activo":
                            continue
                        if carton_lleno(c["matriz"], ss.balotas_lleno):
                            ss.ganador_lleno = {
                                "codigo": c["codigo"],
                                "nombre": c["nombre"],
                                "telefono": c["telefono"],
                            }
                            ss.pausa_lleno = True
                            ss.auto_lleno = False
                            registrar_ganador("Bingo Lleno", {
                                "jugador": c["nombre"],
                                "telefono": c["telefono"],
                                "detalle": c["codigo"],
                                "premio_bs": PREMIO_BINGO_LLENO,
                            })
                            break
                    ss.ultimo_canto_lleno = time.time()
                    guardar()
                time.sleep(0.5)
                st.rerun()

        st.markdown(f"**Balotas cantadas:** {len(ss.balotas_lleno)}/75")

        st.markdown("### 🎫 Cartones registrados")
        for c in ss.cartones_lleno:
            color = {"Activo":"pill-ok","Pendiente":"pill-wait"}.get(c["estado"],"pill-info")
            with st.expander(f"{c['codigo']} · {c['nombre']} · {c['estado']}"):
                st.markdown(
                    f'<span class="pill {color}">{c["estado"]}</span> '
                    f'📞 {c["telefono"]} · Ref: {c["referencia"]}',
                    unsafe_allow_html=True)
                st.markdown(carton_html(c["matriz"], ss.balotas_lleno),
                            unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1:
                    if c["estado"] != "Activo":
                        if st.button("✅ Activar", key=f"act_lleno_{c['id']}"):
                            c["estado"] = "Activo"
                            guardar()
                            st.rerun()
                with b2:
                    if st.button("🗑️ Eliminar", key=f"del_lleno_{c['id']}"):
                        ss.cartones_lleno.remove(c)
                        guardar()
                        st.rerun()

    # ============== TAB 4: HISTORIAL ==============
    with tab4:
        st.markdown("### 📊 Historial de ganadores")
        if not ss.ganadores_hist:
            st.caption("Aún no hay ganadores registrados.")
        else:
            for g in reversed(ss.ganadores_hist):
                st.markdown(
                    f'<div class="metric-card" style="text-align:left">'
                    f'<b>{g["area"]}</b> · {g["fecha"]}<br>'
                    f'🏆 Ganador: <b>{g["jugador"]}</b> · '
                    f'📞 {g["telefono"]}<br>'
                    f'Detalle: {g["detalle"]} · '
                    f'Premio: <b>{g["premio_bs"]} Bs</b>'
                    f'</div>', unsafe_allow_html=True)
        if st.button("🗑️ Borrar historial", key="btn_del_hist"):
            ss.ganadores_hist = []
            guardar()
            st.rerun()

    # ============== TAB 5: REFERENCIAS ==============
    with tab5:
        st.markdown("### 🔍 Verificador de referencias")
        ref_check = st.text_input("Ingresa una referencia para verificar:",
                                  key="ref_check_admin")
        if ref_check.strip():
            if referencia_ya_usada(ref_check):
                info = ss.referencias_usadas.get(normalizar_ref(ref_check), {})
                st.error("⛔ Esta referencia YA fue usada.")
                st.markdown(
                    f'<div class="metric-card" style="text-align:left">'
                    f'<b>Juego:</b> {info.get("juego","—")}<br>'
                    f'<b>Jugador:</b> {info.get("jugador","—")}<br>'
                    f'<b>Fecha:</b> {info.get("fecha","—")}<br>'
                    f'<b>Detalle:</b> {info.get("extra","—")}'
                    f'</div>', unsafe_allow_html=True)
            else:
                st.success(f"✅ La referencia **{ref_check}** está disponible.")

        st.markdown(f"### 📋 Total de referencias: **{len(ss.referencias_usadas)}**")
        with st.expander("Ver todas las referencias usadas"):
            for r, info in sorted(ss.referencias_usadas.items(),
                                  key=lambda x: x[1].get("fecha",""),
                                  reverse=True):
                st.markdown(
                    f'<div class="metric-card" style="text-align:left;padding:12px">'
                    f'<code style="color:#ffd700">{r}</code> · '
                    f'<b>{info.get("juego","—")}</b> · '
                    f'{info.get("jugador","—")} · '
                    f'<span style="color:#94a3b8">{info.get("fecha","—")}</span>'
                    f'</div>', unsafe_allow_html=True)

        if st.button("🗑️ Borrar TODAS las referencias", key="btn_del_refs"):
            ss.referencias_usadas = {}
            guardar()
            st.success("Referencias borradas.")
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Cerrar sesión admin", key="btn_logout"):
        ss.admin_ok = False
        ss.auto_fig = False
        ss.auto_lleno = False
        st.rerun()
