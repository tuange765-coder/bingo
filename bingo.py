# =========================================================
#  BINGO VIRTUAL ONLINE — App completa y corregida
#  Panel de administrador oculto para usuarios
# =========================================================
import csv
import io
import json
import os
import random
import string
import time
from datetime import datetime, timedelta
from urllib.parse import quote

import streamlit as st

# =========================================================
#  CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Bingo Virtual Online",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CLAVE_ADMIN       = "Juan*316*"
WHATSAPP_ADMIN    = "584120139004"
CONTACTO_INFO     = "0424-200-4015"
WHATSAPP_INFO     = "584242004015"
PRECIO_FIGURAS    = 200
PRECIO_LLENO      = 500
INTERVALO_DEFECTO = 5
ARCHIVO_DATOS     = "datos.json"
CARPETA_COMPROB   = "comprobantes"

os.makedirs(CARPETA_COMPROB, exist_ok=True)

DATOS_PAGO = [
    ("🏦 Banco",    "Banesco (0134)"),
    ("🪪 Cédula",   "V-6.865.149"),
    ("📱 Teléfono", "0412-0139004"),
    ("👤 Titular",  "Juan"),
]

# =========================================================
#  ESTILOS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp {
    background:
        radial-gradient(1100px 550px at 8% -10%, #1e3a8a 0%, transparent 60%),
        radial-gradient(900px 500px at 105% 5%, #7c3aed 0%, transparent 55%),
        linear-gradient(180deg, #070b16 0%, #0d1424 100%);
    color: #e8eefc;
}
h1, h2, h3, h4 { color: #ffd166 !important; letter-spacing: .4px; }
p, li, span, label { color: #cbd5e1; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a30, #0a1120);
    border-right: 1px solid #1f2c47;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #ffd166, #f59e0b);
    color: #1a1205 !important; font-weight: 700; border: 0;
    border-radius: 12px; padding: .55rem 1.1rem;
    box-shadow: 0 8px 20px rgba(245,158,11,.25);
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 26px rgba(245,158,11,.45);
}
.stTextInput input, .stNumberInput input { background: #0f172a !important; color: #e8eefc !important;
    border-radius: 10px !important; border: 1px solid #243352 !important; }
.card { background: linear-gradient(160deg, rgba(22,33,58,.95), rgba(13,20,36,.95));
    border: 1px solid #243352; border-radius: 18px; padding: 20px 22px;
    box-shadow: 0 18px 40px rgba(0,0,0,.35); margin-bottom: 16px; }
.balota-wrap { text-align:center; padding: 10px 0 6px 0; }
.balota { width: 170px; height: 170px; border-radius: 50%;
    display:inline-flex; align-items:center; justify-content:center;
    font-size: 72px; font-weight: 800; color:#1a1205;
    background: radial-gradient(circle at 30% 30%, #fff6cf, #ffd166 45%, #f59e0b 100%);
    box-shadow: 0 0 0 10px rgba(255,209,102,.14), 0 20px 45px rgba(245,158,11,.5);
    animation: pop .45s ease; }
@keyframes pop { from { transform: scale(.6); opacity:.2 } to { transform: scale(1); opacity:1 } }
.tablero { display:grid; grid-template-columns: repeat(15, 1fr); gap:6px; }
.bola { aspect-ratio: 1/1; display:flex; align-items:center; justify-content:center;
    border-radius: 10px; background:#131c31; color:#4d5c7d;
    font-weight:700; font-size:13px; border:1px solid #1e2b46; }
.bola.on { background: linear-gradient(135deg,#22c55e,#15803d);
    color:#04140a; border-color:#22c55e; box-shadow: 0 0 14px rgba(34,197,94,.55); }
.bola.test { background: linear-gradient(135deg,#f59e0b,#b45309);
    color:#fff; border-color:#f59e0b; box-shadow: 0 0 14px rgba(245,158,11,.55); }
.carton { display:inline-block; background:#0f172a; padding:12px;
    border-radius:16px; border:1px solid #243352; box-shadow: 0 14px 30px rgba(0,0,0,.4); }
.fila { display:flex; gap:6px; margin-bottom:6px; }
.celda { width:54px; height:54px; display:flex; align-items:center; justify-content:center;
    border-radius:10px; background:#16213a; color:#c7d2fe;
    font-weight:700; font-size:16px; border:1px solid #26355a; }
.celda.marcada { background: linear-gradient(135deg,#f43f5e,#be123c);
    color:#fff; border-color:#f43f5e; box-shadow: 0 0 12px rgba(244,63,94,.6); }
.celda.libre { background: linear-gradient(135deg,#ffd166,#f59e0b);
    color:#1a1205; border-color:#ffd166; }
.letra { width:54px; height:38px; display:flex; align-items:center; justify-content:center;
    border-radius:10px; background: linear-gradient(135deg,#7c3aed,#4c1d95);
    color:#fff; font-weight:800; font-size:18px; }
.pill { display:inline-block; padding:4px 12px; border-radius:999px;
    font-size:12px; font-weight:700; letter-spacing:.4px; }
.pill-ok   { background:#14532d; color:#86efac; border:1px solid #22c55e; }
.pill-wait { background:#78350f; color:#fcd34d; border:1px solid #f59e0b; }
.pill-no   { background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; }
.pill-info { background:#1e3a8a; color:#bfdbfe; border:1px solid #3b82f6; }
.pill-cash { background:#4c1d95; color:#ddd6fe; border:1px solid #8b5cf6; }
.pill-man  { background:#7c2d12; color:#fed7aa; border:1px solid #ea580c; }
.pill-pause{ background:#7f1d1d; color:#fecaca; border:1px solid #ef4444; }
.pill-free { background:#065f46; color:#a7f3d0; border:1px solid #10b981; }

.free-banner {
    background: linear-gradient(135deg, #065f46, #0891b2);
    border: 2px dashed #67e8f9;
    border-radius: 16px;
    padding: 16px 22px;
    margin: 12px 0;
    text-align: center;
    color: #cffafe;
    font-weight: 700;
    letter-spacing: 1px;
}
.codigo-box {
    background: linear-gradient(135deg, #16a34a, #065f46);
    border: 2px dashed #86efac;
    border-radius: 16px;
    padding: 18px 22px; text-align: center; margin: 12px 0;
    box-shadow: 0 0 30px rgba(34,197,94,.35);
}
.codigo-titulo { color:#d1fae5; font-size:13px; letter-spacing:2px; font-weight:700; }
.codigo-valor  { color:#fff; font-size:34px; font-weight:800; letter-spacing:4px;
                 margin-top:6px; font-family: 'Courier New', monospace; }

.ganador-box {
    background: linear-gradient(135deg, #facc15, #f59e0b, #dc2626);
    border: 3px solid #fef08a; border-radius: 20px;
    padding: 26px 30px; text-align: center; margin: 16px 0;
    box-shadow: 0 0 60px rgba(250,204,21,.6);
    animation: brillar 1.4s ease-in-out infinite alternate;
}
@keyframes brillar {
    from { box-shadow: 0 0 30px rgba(250,204,21,.45); transform: scale(1); }
    to   { box-shadow: 0 0 70px rgba(250,204,21,.85); transform: scale(1.015); }
}
.ganador-titulo { color:#1a1205; font-size:26px; font-weight: 900;
                  letter-spacing: 3px; margin-bottom: 6px; }
.ganador-codigo { color:#fff; font-size:52px; font-weight: 900;
                  letter-spacing: 6px; font-family: 'Courier New', monospace;
                  text-shadow: 3px 3px 0 #7c2d12; margin: 10px 0; }
.ganador-detalle{ color:#1a1205; font-size:16px; font-weight: 700; }

.pausa-box {
    background: linear-gradient(135deg, #7f1d1d, #450a0a);
    border: 3px dashed #fca5a5; border-radius: 16px;
    padding: 18px 22px; text-align: center; margin: 12px 0;
    color: #fecaca; font-weight: 700; letter-spacing: 2px;
    animation: pulso 1.2s ease-in-out infinite;
}
@keyframes pulso { 0%,100% { opacity: 1; } 50% { opacity: .55; } }

.pendiente-box {
    background: linear-gradient(135deg, #78350f, #451a03);
    border: 2px dashed #fcd34d; border-radius: 16px;
    padding: 18px 22px; text-align: center; margin: 12px 0;
}
.pendiente-titulo { color:#fef3c7; font-size:15px; font-weight:700; }
.pendiente-texto  { color:#fde68a; font-size:13px; margin-top:6px; }

.efectivo-box {
    background: linear-gradient(135deg, #4c1d95, #2e1065);
    border: 2px dashed #c4b5fd; border-radius: 16px;
    padding: 18px 22px; text-align: center; margin: 12px 0;
}
.efectivo-titulo { color:#ddd6fe; font-size:15px; font-weight:700; }
.efectivo-texto  { color:#c4b5fd; font-size:13px; margin-top:6px; }

.hora-box {
    background: linear-gradient(135deg, #1e40af, #1e3a8a);
    border: 2px solid #60a5fa; border-radius: 16px;
    padding: 16px 22px; text-align: center; margin: 12px 0;
    box-shadow: 0 0 25px rgba(59,130,246,.35);
}
.hora-titulo { color:#dbeafe; font-size:13px; letter-spacing:2px; font-weight:700; }
.hora-valor  { color:#fff; font-size:28px; font-weight:800; margin-top:6px; }
.hora-resto  { color:#93c5fd; font-size:14px; margin-top:6px; }

.prueba-banner {
    background: linear-gradient(135deg, #b45309, #78350f);
    border: 2px dashed #fbbf24; border-radius: 14px;
    padding: 14px 20px; margin-bottom: 16px;
    text-align: center; color: #fef3c7;
    font-weight: 700; letter-spacing: 1px;
}
hr { border-color:#1f2c47; }
</style>
""", unsafe_allow_html=True)

# =========================================================
#  PERSISTENCIA
# =========================================================
def guardar_datos():
    datos = {
        "partidas": ss.partidas, "partida_actual": ss.partida_actual,
        "cartones": ss.cartones, "contador_id": ss.contador_id,
        "contador_partida": ss.contador_partida, "ganadores": ss.ganadores,
        "mesas_amistosas": ss.mesas_amistosas,
        "mesa_amistosa_actual": ss.mesa_amistosa_actual,
        "cartones_amistosos": ss.cartones_amistosos,
        "contador_mesa": ss.contador_mesa,
        "contador_carton_libre": ss.contador_carton_libre,
    }
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"No se pudo guardar: {e}")


def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return None
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# =========================================================
#  ESTADO
# =========================================================
ss = st.session_state
_datos = cargar_datos()

ss.setdefault("partidas",         _datos.get("partidas", {})         if _datos else {})
ss.setdefault("partida_actual",   _datos.get("partida_actual")        if _datos else None)
ss.setdefault("cartones",         _datos.get("cartones", [])          if _datos else [])
ss.setdefault("contador_id",      _datos.get("contador_id", 1000)     if _datos else 1000)
ss.setdefault("contador_partida", _datos.get("contador_partida", 0)   if _datos else 0)
ss.setdefault("ganadores",        _datos.get("ganadores", [])         if _datos else [])
ss.setdefault("mesas_amistosas",       _datos.get("mesas_amistosas", {})       if _datos else {})
ss.setdefault("mesa_amistosa_actual",  _datos.get("mesa_amistosa_actual")       if _datos else None)
ss.setdefault("cartones_amistosos",    _datos.get("cartones_amistosos", [])    if _datos else [])
ss.setdefault("contador_mesa",         _datos.get("contador_mesa", 0)          if _datos else 0)
ss.setdefault("contador_carton_libre", _datos.get("contador_carton_libre", 5000) if _datos else 5000)

ss.setdefault("admin_ok", False)
ss.setdefault("auto_sorteo", False)
ss.setdefault("intervalo_auto", INTERVALO_DEFECTO)
ss.setdefault("ultimo_canto", 0.0)
ss.setdefault("ultima_balota_vista", None)
ss.setdefault("modo_prueba", False)
ss.setdefault("numeros_prueba", [])
ss.setdefault("ultimo_carton_manual", None)
ss.setdefault("jugador_ident", None)
ss.setdefault("auto_sorteo_amistoso", False)
ss.setdefault("ultimo_canto_amistoso", 0.0)
ss.setdefault("ultima_balota_vista_amistosa", None)

# =========================================================
#  FUNCIONES GENERALES
# =========================================================
def generar_carton():
    rangos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    columnas = [random.sample(range(a, b + 1), 5) for a, b in rangos]
    matriz = [[columnas[c][f] for c in range(5)] for f in range(5)]
    matriz[2][2] = "★"
    return matriz


def generar_codigo_unico(prefijo="BNG-"):
    existentes = {c.get("codigo") for c in ss.cartones if c.get("codigo")}
    existentes |= {c.get("codigo") for c in ss.cartones_amistosos if c.get("codigo")}
    while True:
        chars = string.ascii_uppercase + string.digits
        codigo = prefijo + "".join(random.choices(chars, k=4))
        if codigo not in existentes:
            return codigo


def carton_html(matriz, cantados):
    letras = ["B", "I", "N", "G", "O"]
    html = '<div class="carton"><div class="fila">' + "".join(
        f'<div class="letra">{l}</div>' for l in letras) + '</div>'
    for fila in matriz:
        html += '<div class="fila">'
        for v in fila:
            if v == "★":
                html += '<div class="celda libre">★</div>'
            elif v in cantados:
                html += f'<div class="celda marcada">{v}</div>'
            else:
                html += f'<div class="celda">{v}</div>'
        html += '</div>'
    html += '</div>'
    return html


def tablero_html(cantados, clase_extra=""):
    html = '<div class="tablero">'
    for n in range(1, 76):
        cls = f"bola on {clase_extra}".strip() if n in cantados else "bola"
        html += f'<div class="{cls}">{n}</div>'
    html += '</div>'
    return html


def contar_figura(matriz, cantados):
    marcado = lambda v: v == "★" or v in cantados
    esquinas = all(marcado(matriz[r][c]) for r, c in [(0,0),(0,4),(4,0),(4,4)])
    diagonal  = all(marcado(matriz[i][i]) for i in range(5))
    diagonal2 = all(marcado(matriz[i][4-i]) for i in range(5))
    lateral_i = all(marcado(matriz[i][0]) for i in range(5))
    lateral_d = all(marcado(matriz[i][4]) for i in range(5))
    return {"4 Esquinas": esquinas,
            "Diagonal":   diagonal or diagonal2,
            "Lateral":    lateral_i or lateral_d}


def carton_lleno(matriz, cantados):
    return all(v == "★" or v in cantados for fila in matriz for v in fila)


def link_whatsapp(numero, mensaje):
    return f"https://wa.me/{numero}?text={quote(mensaje)}"


def boton_whatsapp(numero, mensaje, texto, color="#25d366"):
    return (
        f'<a href="{link_whatsapp(numero, mensaje)}" target="_blank" '
        f'style="display:inline-block;padding:12px 22px;margin:6px 6px 6px 0;'
        f'background:linear-gradient(135deg,{color},#128c7e);color:#fff;'
        f'font-weight:700;border-radius:12px;text-decoration:none;'
        f'box-shadow:0 8px 20px rgba(37,211,102,.35);'
        f'transition:transform .15s ease">'
        f'{texto}</a>'
    )


def reproducir_sonido():
    if os.path.exists("balota.mp3"):
        try:
            st.audio("balota.mp3", format="audio/mp3", autoplay=True)
        except Exception:
            pass


def tiempo_restante(hora_str):
    if not hora_str:
        return None
    try:
        return datetime.strptime(hora_str, "%Y-%m-%d %H:%M") - datetime.now()
    except Exception:
        return None


def formatear_delta(delta):
    if delta is None:
        return ""
    if delta.total_seconds() <= 0:
        return "¡El sorteo está en curso!"
    d = delta.days; h, rem = divmod(delta.seconds, 3600); m, s = divmod(rem, 60)
    if d > 0: return f"{d}d {h}h {m}m"
    if h > 0: return f"{h}h {m}m {s}s"
    if m > 0: return f"{m}m {s}s"
    return f"{s}s"


def seccion_info_whatsapp(titulo="📞 INFORMACIÓN",
                          subtitulo="Para cualquier duda del Bingo",
                          mensaje="Hola, necesito información sobre el Bingo Virtual.",
                          texto_boton="📲 Escribir por WhatsApp"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f'<div class="hora-box" style="background:linear-gradient(135deg,#065f46,#064e3b);'
            f'border-color:#34d399">'
            f'<div class="hora-titulo" style="color:#d1fae5">{titulo}</div>'
            f'<div class="hora-valor" style="font-size:22px">{CONTACTO_INFO}</div>'
            f'<div class="hora-resto" style="color:#a7f3d0">{subtitulo}</div>'
            f'</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(boton_whatsapp(WHATSAPP_INFO, mensaje, texto_boton),
                    unsafe_allow_html=True)


# =========================================================
#  FUNCIONES PARTIDAS CON APUESTA
# =========================================================
def crear_partida(nombre, pozo_base=0):
    ss.contador_partida += 1
    pid = f"P-{ss.contador_partida:03d}"
    ss.partidas[pid] = {
        "id": pid, "nombre": nombre.strip() or f"Partida {pid}",
        "estado": "Abierta", "numeros_cantados": [],
        "pozo_base": int(pozo_base), "hora_sorteo": None,
        "pausada": False, "ganador": None,
    }
    if ss.partida_actual is None:
        ss.partida_actual = pid
    guardar_datos()
    return pid


def partida_actual():
    if ss.partida_actual and ss.partida_actual in ss.partidas:
        return ss.partidas[ss.partida_actual]
    return None


def numeros_cantados():
    p = partida_actual()
    return p["numeros_cantados"] if p else []


def calcular_pozo(pid):
    p = ss.partidas.get(pid)
    if not p:
        return 0
    activos = sum(c["costo"] for c in ss.cartones
                  if c["estado"] == "Activo" and c["partida_id"] == pid)
    return p["pozo_base"] + activos


def nuevo_id_carton():
    ss.contador_id += 1
    return f"C-{ss.contador_id}"


def registrar_ganador(partida, carton, tipo_premio):
    ss.ganadores.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "partida": partida["nombre"],
        "carton": carton.get("codigo", carton["id"]),
        "jugador": carton["nombre"], "telefono": carton["telefono"],
        "premio": tipo_premio, "metodo": carton.get("metodo_pago", "—"),
    })
    guardar_datos()


def exportar_csv(ganadores):
    buf = io.StringIO()
    campos = ["fecha", "partida", "carton", "jugador", "telefono", "premio", "metodo"]
    w = csv.DictWriter(buf, fieldnames=campos); w.writeheader()
    for g in ganadores:
        w.writerow({k: g.get(k, "") for k in campos})
    return buf.getvalue().encode("utf-8")


def buscar_cartones_jugador(ident):
    ident = str(ident).strip()
    return [c for c in ss.cartones
            if ident in c["telefono"]
            or ident.upper() == (c.get("codigo") or "").upper()]


def verificar_ganador(p):
    if p.get("ganador"):
        return None
    for c in ss.cartones:
        if c["partida_id"] != p["id"] or c["estado"] != "Activo":
            continue
        if c.get("tipo") == "Lleno":
            if carton_lleno(c["matriz"], p["numeros_cantados"]):
                return {"carton": c, "premio": "Cartón Lleno"}
        else:
            figs = contar_figura(c["matriz"], p["numeros_cantados"])
            logros = [k for k, v in figs.items() if v]
            if logros:
                return {"carton": c, "premio": ", ".join(logros)}
    return None


def agregar_balota(p):
    if p.get("pausada"):
        return False, "La partida está pausada."
    disp = [n for n in range(1, 76) if n not in p["numeros_cantados"]]
    if not disp:
        return False, "Ya se cantaron las 75 balotas."
    p["numeros_cantados"].append(random.choice(disp))
    gan = verificar_ganador(p)
    if gan:
        carton = gan["carton"]
        p["ganador"] = {
            "carton_id": carton["id"],
            "codigo":    carton.get("codigo", "—"),
            "nombre":    carton["nombre"],
            "telefono":  carton["telefono"],
            "premio":    gan["premio"],
            "fecha":     datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        p["pausada"] = True
        ss.auto_sorteo = False
        guardar_datos()
        return True, f"🎉 ¡BINGO! {carton.get('codigo', carton['id'])}"
    guardar_datos()
    return True, "Balota cantada."


def reanudar_partida(p):
    p["pausada"] = False; p["ganador"] = None
    guardar_datos()


def cerrar_por_ganador(p):
    g = p.get("ganador")
    if g:
        carton = next((c for c in ss.cartones if c["id"] == g["carton_id"]), None)
        if carton:
            registrar_ganador(p, carton, g["premio"])
    p["estado"] = "Cerrada"
    guardar_datos()


# =========================================================
#  FUNCIONES MESA AMISTOSA
# =========================================================
def crear_mesa_amistosa(nombre):
    ss.contador_mesa += 1
    mid = f"M-{ss.contador_mesa:03d}"
    ss.mesas_amistosas[mid] = {
        "id": mid,
        "nombre": nombre.strip() or f"Mesa {mid}",
        "numeros_cantados": [],
        "pausada": False,
        "ganador": None,
        "creada": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    if ss.mesa_amistosa_actual is None:
        ss.mesa_amistosa_actual = mid
    guardar_datos()
    return mid


def mesa_amistosa_actual():
    if ss.mesa_amistosa_actual and ss.mesa_amistosa_actual in ss.mesas_amistosas:
        return ss.mesas_amistosas[ss.mesa_amistosa_actual]
    return None


def nuevo_id_carton_libre():
    ss.contador_carton_libre += 1
    return f"LIB-{ss.contador_carton_libre}"


def agregar_carton_amistoso(mesa_id, nombre_jugador):
    carton = {
        "id": nuevo_id_carton_libre(),
        "codigo": generar_codigo_unico("FUN-"),
        "mesa_id": mesa_id,
        "nombre": nombre_jugador.strip(),
        "matriz": generar_carton(),
        "creado": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    ss.cartones_amistosos.append(carton)
    guardar_datos()
    return carton


def cartones_de_mesa(mesa_id):
    return [c for c in ss.cartones_amistosos if c["mesa_id"] == mesa_id]


def verificar_ganador_amistoso(mesa):
    if mesa.get("ganador"):
        return None
    cantados = mesa["numeros_cantados"]
    for c in cartones_de_mesa(mesa["id"]):
        if carton_lleno(c["matriz"], cantados):
            return {"carton": c, "premio": "Cartón Lleno"}
        figs = contar_figura(c["matriz"], cantados)
        logros = [k for k, v in figs.items() if v]
        if logros:
            return {"carton": c, "premio": ", ".join(logros)}
    return None


def agregar_balota_amistosa(mesa):
    if mesa.get("pausada"):
        return False, "La mesa está pausada."
    disp = [n for n in range(1, 76) if n not in mesa["numeros_cantados"]]
    if not disp:
        return False, "Ya se cantaron las 75 balotas."
    mesa["numeros_cantados"].append(random.choice(disp))
    gan = verificar_ganador_amistoso(mesa)
    if gan:
        c = gan["carton"]
        mesa["ganador"] = {
            "carton_id": c["id"],
            "codigo":    c.get("codigo", "—"),
            "nombre":    c["nombre"],
            "premio":    gan["premio"],
            "fecha":     datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        mesa["pausada"] = True
        ss.auto_sorteo_amistoso = False
        guardar_datos()
        return True, f"🎉 ¡BINGO! {c['nombre']} ({c['codigo']})"
    guardar_datos()
    return True, "Balota cantada."


def reanudar_mesa(mesa):
    mesa["pausada"] = False; mesa["ganador"] = None
    guardar_datos()


def nueva_ronda_mesa(mesa):
    mesa["numeros_cantados"] = []
    mesa["pausada"] = False
    mesa["ganador"] = None
    ss.auto_sorteo_amistoso = False
    guardar_datos()


def borrar_mesa(mesa_id):
    ss.cartones_amistosos = [c for c in ss.cartones_amistosos if c["mesa_id"] != mesa_id]
    ss.mesas_amistosas.pop(mesa_id, None)
    if ss.mesa_amistosa_actual == mesa_id:
        ss.mesa_amistosa_actual = next(iter(ss.mesas_amistosas), None)
    guardar_datos()


if not ss.partidas:
    crear_partida("Partida de Bienvenida", pozo_base=0)


# =========================================================
#  BANNERS
# =========================================================
def mostrar_banner_ganador(p):
    if p.get("pausada") and p.get("ganador"):
        g = p["ganador"]
        st.markdown(
            f'<div class="ganador-box">'
            f'<div class="ganador-titulo">🎉 ¡B I N G O! 🎉</div>'
            f'<div class="ganador-codigo">{g["codigo"]}</div>'
            f'<div class="ganador-detalle">'
            f'Ganador: <b>{g["nombre"]}</b> · Premio: <b>{g["premio"]}</b>'
            f'</div></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="pausa-box">🛑 PARTIDA PAUSADA — El administrador confirmará al ganador</div>',
            unsafe_allow_html=True)
        return True
    return False


def mostrar_banner_ganador_mesa(mesa):
    if mesa.get("pausada") and mesa.get("ganador"):
        g = mesa["ganador"]
        st.markdown(
            f'<div class="ganador-box">'
            f'<div class="ganador-titulo">🎉 ¡B I N G O! 🎉</div>'
            f'<div class="ganador-codigo">{g["codigo"]}</div>'
            f'<div class="ganador-detalle">'
            f'Ganador: <b>{g["nombre"]}</b> · Premio: <b>{g["premio"]}</b>'
            f'</div></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="pausa-box">🛑 MESA PAUSADA — '
            'Pulsa "Nueva ronda" para jugar otra vez</div>',
            unsafe_allow_html=True)
        return True
    return False


# =========================================================
#  BARRA LATERAL
# =========================================================
with st.sidebar:
    st.markdown("## 🎟️ Bingo Virtual")
    st.markdown("---")

    if ss.jugador_ident:
        cartones_j = buscar_cartones_jugador(ss.jugador_ident)
        nombre_mostrar = cartones_j[0]["nombre"] if cartones_j else ss.jugador_ident
        st.markdown(f"### 👤 {nombre_mostrar}")
        st.caption(f"Identificado como: `{ss.jugador_ident}`")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            ss.jugador_ident = None
            st.rerun()
        st.markdown("---")

    # ===== MENÚ DE NAVEGACIÓN (sin mostrar Administrador a usuarios) =====
    opciones_menu = ["👤 Mi Cartón", "🛒 Comprar Cartón",
                     "🎲 Juego Amistoso", "📺 Sorteo en Vivo"]

    # Solo si ya está logueado como admin, agregamos la pestaña
    if ss.admin_ok:
        opciones_menu.append("⚙️ Administrador")

    opcion = st.radio("Navegación", opciones_menu)
    st.markdown("---")

    # ===== ACCESO SECRETO AL PANEL DE ADMINISTRADOR =====
    if not ss.admin_ok:
        with st.expander("🔒", expanded=False):
            with st.form("form_login_secreto", clear_on_submit=True):
                clave = st.text_input("Contraseña:", type="password",
                                      label_visibility="collapsed",
                                      placeholder="Contraseña…")
                entrar = st.form_submit_button("Entrar", use_container_width=True)
            if entrar:
                if clave == CLAVE_ADMIN:
                    ss.admin_ok = True
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta.")
        st.markdown("---")
    else:
        st.markdown(
            '<span class="pill pill-ok">🔓 Sesión admin activa</span>',
            unsafe_allow_html=True)
        if st.button("🚪 Salir del panel admin", use_container_width=True):
            ss.admin_ok = False
            ss.auto_sorteo = False
            st.rerun()
        st.markdown("---")

    # ===== Panel de partida / mesa =====
    if opcion != "🎲 Juego Amistoso":
        st.markdown("### 🎮 Partida actual")
        if ss.partidas:
            opciones_partidas = {p["id"]: p["nombre"] for p in ss.partidas.values()}
            indice = list(opciones_partidas.keys()).index(ss.partida_actual) \
                     if ss.partida_actual in opciones_partidas else 0
            pid_sel = st.selectbox(
                "Selecciona la partida:",
                options=list(opciones_partidas.keys()),
                format_func=lambda k: f"{k} · {opciones_partidas[k]}",
                index=indice, key="selector_partida",
            )
            ss.partida_actual = pid_sel
            p = partida_actual()
            color = {"Abierta": "pill-ok", "En curso": "pill-wait",
                     "Cerrada": "pill-no"}[p["estado"]]
            st.markdown(f'<span class="pill {color}">{p["estado"]}</span>',
                        unsafe_allow_html=True)
            if p.get("pausada"):
                st.markdown('<span class="pill pill-pause">⏸️ PAUSADA POR BINGO</span>',
                            unsafe_allow_html=True)
            if p.get("hora_sorteo") and not p.get("pausada"):
                delta = tiempo_restante(p["hora_sorteo"])
                st.markdown(
                    f'<div class="hora-box">'
                    f'<div class="hora-titulo">⏰ SORTEO PROGRAMADO</div>'
                    f'<div class="hora-valor">{p["hora_sorteo"]}</div>'
                    f'<div class="hora-resto">⏳ {formatear_delta(delta)}</div>'
                    f'</div>', unsafe_allow_html=True)
        st.markdown("---")
        if ss.partida_actual:
            st.markdown(f"**🎱 Balotas:** `{len(numeros_cantados())}/75`")
            activos = len([c for c in ss.cartones
                           if c["estado"] == "Activo"
                           and c["partida_id"] == ss.partida_actual])
            st.markdown(f"**🎫 Cartones activos:** `{activos}`")
    else:
        st.markdown("### 🎲 Mesa amistosa actual")
        if ss.mesas_amistosas:
            opciones_m = {m["id"]: m["nombre"] for m in ss.mesas_amistosas.values()}
            indice_m = list(opciones_m.keys()).index(ss.mesa_amistosa_actual) \
                       if ss.mesa_amistosa_actual in opciones_m else 0
            mid_sel = st.selectbox(
                "Mesa:",
                options=list(opciones_m.keys()),
                format_func=lambda k: f"{k} · {opciones_m[k]}",
                index=indice_m, key="selector_mesa",
            )
            ss.mesa_amistosa_actual = mid_sel
            m = mesa_amistosa_actual()
            if m.get("pausada"):
                st.markdown('<span class="pill pill-pause">⏸️ BINGO</span>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<span class="pill pill-free">🎉 JUGANDO</span>',
                            unsafe_allow_html=True)
            st.markdown(f"**🎱 Balotas:** `{len(m['numeros_cantados'])}/75`")
            st.markdown(f"**🎫 Cartones:** `{len(cartones_de_mesa(m['id']))}`")
        else:
            st.caption("Aún no hay mesas creadas.")

    # ===== INFORMACIÓN + WHATSAPP =====
    st.markdown("---")
    st.markdown(
        f'<div class="hora-box" style="background:linear-gradient(135deg,#065f46,#064e3b);'
        f'border-color:#34d399">'
        f'<div class="hora-titulo" style="color:#d1fae5">📞 INFORMACIÓN</div>'
        f'<div class="hora-valor" style="font-size:22px">{CONTACTO_INFO}</div>'
        f'<div class="hora-resto" style="color:#a7f3d0">'
        f'Para cualquier duda del Bingo</div>'
        f'</div>', unsafe_allow_html=True)
    st.markdown(
        boton_whatsapp(
            WHATSAPP_INFO,
            "Hola, necesito información sobre el Bingo Virtual.",
            "📲 Escribir por WhatsApp",
        ),
        unsafe_allow_html=True,
    )
    st.caption("🔞 Juega responsablemente.")


# =========================================================
#  PÁGINA · 🎲 JUEGO AMISTOSO
# =========================================================
if opcion == "🎲 Juego Amistoso":
    st.title("🎲 Sala de Juego Amistoso")
    st.markdown(
        '<div class="free-banner">'
        '🎉 MODO SIN APUESTAS · Juega con tus amigos por diversión · Sin pagos'
        '</div>', unsafe_allow_html=True)

    seccion_info_whatsapp(
        titulo="📞 INFORMACIÓN",
        subtitulo="Escríbenos para cualquier duda",
        mensaje="Hola, tengo dudas sobre el Juego Amistoso del Bingo.",
        texto_boton="📲 WhatsApp",
    )
    st.markdown("---")

    with st.expander("🛠️ Crear o elegir mesa amistosa", expanded=not ss.mesas_amistosas):
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            nuevo_nombre_mesa = st.text_input(
                "Nombre de la nueva mesa:",
                placeholder="Ej: Tarde de amigos, Cumpleaños, Reunión familiar…")
        with col_c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Crear mesa"):
                if nuevo_nombre_mesa.strip():
                    mid = crear_mesa_amistosa(nuevo_nombre_mesa)
                    ss.mesa_amistosa_actual = mid
                    st.success(f"✅ Mesa **{mid}** creada.")
                    st.rerun()
                else:
                    st.warning("Escribe un nombre.")

        if ss.mesas_amistosas:
            st.markdown("#### Mesas existentes")
            for mid, m in list(ss.mesas_amistosas.items()):
                cc1, cc2, cc3 = st.columns([3, 1.2, 1])
                icono = "⏸️" if m.get("pausada") else "🎉"
                cc1.markdown(
                    f'{icono} **{mid}** · {m["nombre"]} · '
                    f'`{len(cartones_de_mesa(mid))}` cartones · '
                    f'`{len(m["numeros_cantados"])}/75` balotas')
                with cc2:
                    if st.button("▶️ Entrar", key=f"entrar_{mid}"):
                        ss.mesa_amistosa_actual = mid
                        st.rerun()
                with cc3:
                    if st.button("🗑️ Eliminar", key=f"delm_{mid}"):
                        borrar_mesa(mid)
                        st.rerun()

    mesa = mesa_amistosa_actual()
    if not mesa:
        st.info("💡 Crea una mesa amistosa para empezar a jugar.")
        st.stop()

    st.markdown("---")

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"### 🎮 Mesa: **{mesa['nombre']}**")
        st.caption(f"ID: `{mesa['id']}` · "
                   f"Creada: {mesa.get('creada','—')} · "
                   f"Cartones: **{len(cartones_de_mesa(mesa['id']))}**")
    with col_h2:
        if st.button("🧹 Nueva ronda (limpiar balotas)", use_container_width=True):
            nueva_ronda_mesa(mesa)
            st.success("🔁 Balotas reiniciadas. ¡Listos para otra ronda!")
            st.rerun()

    mostrar_banner_ganador_mesa(mesa)

    with st.expander("➕ Agregar cartón para un amigo", expanded=True):
        st.caption("Escribe el nombre de tu amigo y se genera un cartón único.")
        with st.form("form_add_amigo", clear_on_submit=True):
            col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
            with col_f1:
                nombre_amigo = st.text_input("Nombre del amigo:")
            with col_f2:
                cant_rapida = st.number_input("Cantidad (mismo amigo):",
                                              min_value=1, max_value=6, value=1)
            with col_f3:
                st.markdown("<br>", unsafe_allow_html=True)
                crear_c = st.form_submit_button("🎟️ Generar cartón(es)")

        if crear_c:
            if nombre_amigo.strip():
                nuevos = []
                for _ in range(int(cant_rapida)):
                    nuevos.append(agregar_carton_amistoso(mesa["id"],
                                                          nombre_amigo))
                st.success(f"✅ {len(nuevos)} cartón(es) generado(s) para "
                           f"**{nombre_amigo.strip()}**.")
                for n in nuevos:
                    st.markdown(
                        f'<div class="codigo-box">'
                        f'<div class="codigo-titulo">🎟️ {n["nombre"]}</div>'
                        f'<div class="codigo-valor">{n["codigo"]}</div>'
                        f'</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'{carton_html(n["matriz"], mesa["numeros_cantados"])}</div>',
                        unsafe_allow_html=True)
                    st.markdown("<hr>", unsafe_allow_html=True)
            else:
                st.error("⚠️ Escribe el nombre del amigo.")

    st.markdown("---")
    st.markdown("### 🎰 Cantar balotas (organizador)")

    if mesa.get("pausada"):
        st.error("🛑 **Mesa PAUSADA por Bingo.** Pulsa *Nueva ronda* para volver "
                 "a jugar.")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶️ Cantar balota", disabled=mesa.get("pausada"),
                     use_container_width=True):
            ok, msg = agregar_balota_amistosa(mesa)
            if ok:
                st.rerun()
            else:
                st.warning(msg)
    with c2:
        etiqueta = "⏸️ Detener auto" if ss.auto_sorteo_amistoso else "⚡ Auto sorteo"
        if st.button(etiqueta, disabled=mesa.get("pausada") and not ss.auto_sorteo_amistoso,
                     use_container_width=True):
            ss.auto_sorteo_amistoso = not ss.auto_sorteo_amistoso
            ss.ultimo_canto_amistoso = time.time()
            st.rerun()
    with c3:
        if st.button("🔄 Reiniciar balotas", use_container_width=True):
            nueva_ronda_mesa(mesa)
            st.rerun()

    with st.expander("⚙️ Sorteo automático amistoso"):
        ss.intervalo_auto = st.slider("Segundos entre balotas:", 1, 30,
                                      ss.intervalo_auto)

    if ss.auto_sorteo_amistoso and not mesa.get("pausada"):
        ahora = time.time()
        if ahora - ss.ultimo_canto_amistoso >= ss.intervalo_auto:
            agregar_balota_amistosa(mesa)
            ss.ultimo_canto_amistoso = ahora
        time.sleep(1.0)
        st.rerun()

    if mesa["numeros_cantados"] and \
       ss.ultima_balota_vista_amistosa != mesa["numeros_cantados"][-1]:
        ss.ultima_balota_vista_amistosa = mesa["numeros_cantados"][-1]
        reproducir_sonido()

    st.markdown("---")
    col_a, col_b = st.columns([1, 1.6], gap="large")
    cantados = mesa["numeros_cantados"]
    with col_a:
        if cantados:
            st.markdown(
                f'<div class="card"><h4 style="text-align:center">🎱 Última balota</h4>'
                f'<div class="balota-wrap"><div class="balota">{cantados[-1]}</div></div>'
                f'<p style="text-align:center;color:#94a3b8">'
                f'Balota N° {len(cantados)} de 75</p></div>',
                unsafe_allow_html=True)
        else:
            st.info("⏳ Aún no se ha cantado ninguna balota.")
    with col_b:
        st.markdown("### 🎯 Tablero de 75 balotas")
        st.markdown(tablero_html(cantados), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎫 Cartones de esta mesa")

    cartones_m = cartones_de_mesa(mesa["id"])
    if not cartones_m:
        st.info("Todavía no hay cartones. Agrega uno arriba.")
    else:
        for c in cartones_m:
            g_mesa = mesa.get("ganador")
            es_ganador = bool(g_mesa and g_mesa.get("carton_id") == c["id"])
            etiqueta = " 🏆" if es_ganador else ""
            with st.expander(f"🎟️ {c['codigo']} · {c['nombre']}{etiqueta}"):
                st.markdown(
                    f'<span class="pill pill-free">Código: {c["codigo"]}</span> '
                    f'<span class="pill pill-info">{c["nombre"]}</span>',
                    unsafe_allow_html=True)
                if es_ganador:
                    st.success(f"🏆 ¡GANADOR! Premio: {g_mesa['premio']}")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(carton_html(c["matriz"], cantados),
                            unsafe_allow_html=True)

                if cantados:
                    figs = contar_figura(c["matriz"], cantados)
                    logros = [k for k, v in figs.items() if v]
                    faltan = sum(1 for fila in c["matriz"] for v in fila
                                 if v != "★" and v not in cantados)
                    st.caption(f"🎯 Figuras: "
                               f"**{', '.join(logros) if logros else 'ninguna'}** · "
                               f"Casillas faltantes: **{faltan}**")

                colp1, colp2 = st.columns([1, 1])
                with colp1:
                    if st.button("🗑️ Eliminar cartón", key=f"delc_{c['id']}"):
                        ss.cartones_amistosos = [
                            x for x in ss.cartones_amistosos if x["id"] != c["id"]]
                        guardar_datos(); st.rerun()
                with colp2:
                    if st.button("🔁 Regenerar matriz", key=f"regen_{c['id']}"):
                        c["matriz"] = generar_carton()
                        guardar_datos()
                        st.success("Matriz regenerada.")
                        st.rerun()

    st.markdown("---")
    st.markdown("### 📜 Historial de balotas")
    if cantados:
        st.markdown(" ".join(
            f'<span style="display:inline-block;margin:4px;padding:8px 14px;'
            f'border-radius:10px;background:#16213a;color:#ffd166;font-weight:700;'
            f'border:1px solid #26355a">{n}</span>' for n in cantados),
            unsafe_allow_html=True)
    else:
        st.caption("Sin balotas.")


# =========================================================
#  PÁGINA · 👤 MI CARTÓN
# =========================================================
elif opcion == "👤 Mi Cartón":
    st.title("👤 Mi Cartón de Bingo")
    st.markdown("---")

    if not ss.jugador_ident:
        st.markdown("### 🔐 Ingresa para ver tu cartón")
        st.caption("Usa el **teléfono** con el que te registraste o el "
                   "**código de tu cartón**.")
        with st.form("form_login_jugador"):
            ident = st.text_input("📱 Teléfono o 🎟️ Código de cartón:",
                                  placeholder="Ej: 584120139004  ó  BNG-7X4K")
            entrar = st.form_submit_button("🎟️ Ver mis cartones")
        if entrar:
            if ident.strip():
                ss.jugador_ident = ident.strip(); st.rerun()
            else:
                st.error("Debes ingresar tu teléfono o código.")
        st.info("💡 Si vas a jugar con amigos, ve a **🎲 Juego Amistoso**.")
        seccion_info_whatsapp(
            titulo="📞 INFORMACIÓN",
            subtitulo="Para cualquier duda del Bingo",
            mensaje="Hola, necesito información sobre el Bingo Virtual.",
            texto_boton="📲 WhatsApp",
        )
        st.stop()

    ident = ss.jugador_ident
    mis_cartones = buscar_cartones_jugador(ident)

    if not mis_cartones:
        st.warning(f"No encontramos cartones asociados a **{ident}**.")
        if st.button("🔓 Probar con otro dato"):
            ss.jugador_ident = None; st.rerun()
        st.stop()

    jugador_nombre = mis_cartones[0]["nombre"]
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"### 👋 ¡Hola, **{jugador_nombre}**!")
        st.caption(f"📱 {ident} · Tienes **{len(mis_cartones)}** cartón(es)")
    with col_h2:
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            ss.jugador_ident = None; st.rerun()

    activos   = len([c for c in mis_cartones if c["estado"] == "Activo"])
    pendientes = len([c for c in mis_cartones if c["estado"] == "Pendiente"])
    rechazados = len([c for c in mis_cartones if c["estado"] == "Rechazado"])
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("✅ Confirmados", activos)
    cc2.metric("⏳ Pendientes",  pendientes)
    cc3.metric("⛔ Rechazados",  rechazados)
    st.markdown("---")

    for c in mis_cartones:
        partida_obj = ss.partidas.get(c["partida_id"], {})
        nombre_partida = partida_obj.get("nombre", "—")
        cantados_p = partida_obj.get("numeros_cantados", [])
        estado = c["estado"]
        metodo = c.get("metodo_pago", "Pago Móvil")
        color_m = "pill-cash" if metodo == "Efectivo" else "pill-info"

        gan_partida = partida_obj.get("ganador")
        es_ganador = bool(gan_partida and gan_partida.get("carton_id") == c["id"])

        if estado == "Activo":
            if es_ganador:
                st.balloons()
                st.markdown(
                    f'<div class="ganador-box">'
                    f'<div class="ganador-titulo">🎉 ¡HAS GANADO! 🎉</div>'
                    f'<div class="ganador-codigo">{c.get("codigo","—")}</div>'
                    f'<div class="ganador-detalle">'
                    f'Premio: <b>{gan_partida["premio"]}</b> · '
                    f'Partida: <b>{nombre_partida}</b><br>'
                    f'¡Contáctanos por WhatsApp para reclamar tu premio!'
                    f'</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="codigo-box">'
                    f'<div class="codigo-titulo">🎟️ TU CÓDIGO · {nombre_partida}</div>'
                    f'<div class="codigo-valor">{c.get("codigo","—")}</div>'
                    f'</div>', unsafe_allow_html=True)

            colx1, colx2, colx3 = st.columns([1, 1, 1])
            colx1.markdown('<span class="pill pill-ok">✅ PAGO CONFIRMADO</span>',
                           unsafe_allow_html=True)
            colx2.markdown(f'<span class="pill {color_m}">Método: {metodo}</span>',
                           unsafe_allow_html=True)
            colx3.markdown(f'<span class="pill pill-info">{c["tipo"]}</span>',
                           unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div style="text-align:center">'
                f'{carton_html(c["matriz"], cantados_p)}</div>',
                unsafe_allow_html=True)

            if cantados_p:
                st.caption(f"🎱 Balotas cantadas: **{len(cantados_p)}/75** · "
                           f"Ref: {c['referencia']}")
                figs = contar_figura(c["matriz"], cantados_p)
                logros = [k for k, v in figs.items() if v]
                if carton_lleno(c["matriz"], cantados_p) and not es_ganador:
                    st.success("🎉 Tu cartón está **LLENO**.")
                elif logros and not es_ganador:
                    st.info(f"🎯 Figuras completadas: **{', '.join(logros)}**")
                elif not es_ganador:
                    st.caption("🍀 Aún no completas ninguna figura.")
            else:
                st.caption("⏳ El sorteo aún no ha comenzado.")

        elif estado == "Pendiente":
            if metodo == "Efectivo":
                st.markdown(
                    f'<div class="efectivo-box">'
                    f'<div class="efectivo-titulo">💵 Pago en efectivo pendiente · {nombre_partida}</div>'
                    f'<div class="efectivo-texto">'
                    f'Cuando el organizador reciba el dinero, verás tu código.</div>'
                    f'</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="pendiente-box">'
                    f'<div class="pendiente-titulo">⏳ Pago Móvil en revisión · {nombre_partida}</div>'
                    f'<div class="pendiente-texto">'
                    f'En cuanto sea confirmado, verás aquí el código de tu cartón.</div>'
                    f'</div>', unsafe_allow_html=True)
            st.caption(f"📞 Ref: {c['referencia']} · Modalidad: {c['tipo']} · "
                       f"Costo: {c['costo']} Bs")
        else:
            st.error(f"⛔ Pago rechazado · Partida: {nombre_partida} · "
                     f"Ref: {c['referencia']}")
        st.markdown("---")

    st.markdown("### 💬 ¿Dudas con tu pago o cartón?")
    st.markdown(
        f'<div class="hora-box" style="background:linear-gradient(135deg,#065f46,#064e3b);'
        f'border-color:#34d399">'
        f'<div class="hora-titulo" style="color:#d1fae5">📞 INFORMACIÓN Y SOPORTE</div>'
        f'<div class="hora-valor" style="font-size:24px">{CONTACTO_INFO}</div>'
        f'</div>', unsafe_allow_html=True)

    col_wa1, col_wa2 = st.columns(2)
    with col_wa1:
        st.markdown(
            boton_whatsapp(
                WHATSAPP_INFO,
                f"Hola, soy {jugador_nombre}, tengo dudas sobre mis cartones del Bingo.",
                "📲 Información general",
            ),
            unsafe_allow_html=True,
        )
    with col_wa2:
        msg_ayuda = f"Hola, soy {jugador_nombre}, necesito ayuda con mis cartones."
        st.markdown(
            boton_whatsapp(
                WHATSAPP_ADMIN,
                msg_ayuda,
                "📲 Escribir al organizador",
                color="#0ea5e9",
            ),
            unsafe_allow_html=True,
        )


# =========================================================
#  PÁGINA · 🛒 COMPRAR CARTÓN
# =========================================================
elif opcion == "🛒 Comprar Cartón":
    st.title("🛒 Compra tu Cartón de Bingo")
    st.markdown("---")

    p = partida_actual()
    if not p:
        st.error("No hay partida activa."); st.stop()

    if p.get("pausada") and p.get("ganador"):
        mostrar_banner_ganador(p)
        st.warning("⛔ Mientras la partida esté pausada, no se aceptan compras.")
        st.stop()

    if p.get("hora_sorteo"):
        delta = tiempo_restante(p["hora_sorteo"])
        st.markdown(
            f'<div class="hora-box">'
            f'<div class="hora-titulo">⏰ SORTEO PROGRAMADO</div>'
            f'<div class="hora-valor">{p["hora_sorteo"]}</div>'
            f'<div class="hora-resto">⏳ Faltan: {formatear_delta(delta)}</div>'
            f'</div>', unsafe_allow_html=True)

    seccion_info_whatsapp(
        titulo="📞 ¿DUDAS CON TU PAGO?",
        subtitulo="Escríbenos por WhatsApp, te ayudamos al instante",
        mensaje="Hola, tengo una duda sobre el pago del Bingo.",
        texto_boton="📲 WhatsApp",
    )
    st.markdown("---")

    if p["estado"] == "Cerrada":
        st.warning("⛔ Esta partida está cerrada.")

    col_izq, col_der = st.columns([1.2, 1], gap="large")

    with col_izq:
        st.markdown("### 1️⃣ Elige tu modalidad")
        modalidad = st.radio(
            "Modalidad de juego:",
            [
                f"🎯 Figuras (4 Esquinas / Lateral / Diagonal) — {PRECIO_FIGURAS} Bs",
                f"🏆 Cartón Lleno — {PRECIO_LLENO} Bs",
            ],
        )
        costo, tipo = (PRECIO_FIGURAS, "Figuras") if "Figuras" in modalidad \
                      else (PRECIO_LLENO, "Lleno")

        st.markdown(
            f'<div class="card"><h4>💵 Costo del cartón</h4>'
            f'<h2 style="margin:0">{costo} Bs</h2>'
            f'<small>Modalidad: {tipo}</small></div>',
            unsafe_allow_html=True)

        st.markdown("### 2️⃣ Elige tu método de pago")
        metodo_pago = st.radio("Método de pago:",
                               ["📱 Pago Móvil", "💵 Efectivo (en persona)"])

        if "Pago Móvil" in metodo_pago:
            st.markdown("#### 📱 Datos para Pago Móvil")
            filas = "".join(
                f"<tr><td style='padding:6px 14px 6px 0;color:#94a3b8'>{k}</td>"
                f"<td style='padding:6px 0;color:#e8eefc;font-weight:600'>{v}</td></tr>"
                for k, v in DATOS_PAGO)
            st.markdown(
                f'<div class="card"><table style="border-collapse:collapse">{filas}</table></div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="efectivo-box">'
                '<div class="efectivo-titulo">💵 Pago en Efectivo</div>'
                '<div class="efectivo-texto">'
                'Debes entregar el monto al organizador. '
                'Cuando confirme que lo recibió, tu código será activado.'
                '</div></div>', unsafe_allow_html=True)

    with col_der:
        st.markdown("### 3️⃣ Registra tus datos")

        if "Pago Móvil" in metodo_pago:
            with st.form("form_registro_pm", clear_on_submit=True):
                nombre      = st.text_input("Nombre y Apellido:")
                telefono    = st.text_input("Teléfono (WhatsApp, ej: 584120000000):")
                referencia  = st.text_input("N° de Referencia del Pago Móvil:")
                comprobante = st.file_uploader("📷 Captura del comprobante:",
                                               type=["jpg", "jpeg", "png"])
                enviar = st.form_submit_button("📱 Enviar comprobante")
            if enviar:
                if nombre and telefono and referencia and p["estado"] != "Cerrada":
                    carton = {
                        "id": nuevo_id_carton(), "codigo": None,
                        "nombre": nombre.strip(), "telefono": telefono.strip(),
                        "referencia": referencia.strip(), "tipo": tipo,
                        "costo": costo, "matriz": generar_carton(),
                        "estado": "Pendiente", "partida_id": p["id"],
                        "comprobante": None, "metodo_pago": "Pago Móvil",
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    if comprobante is not None:
                        ruta = os.path.join(CARPETA_COMPROB, f"{carton['id']}.png")
                        with open(ruta, "wb") as f:
                            f.write(comprobante.getbuffer())
                        carton["comprobante"] = ruta
                    ss.cartones.append(carton); guardar_datos()
                    st.success(f"🎉 Cartón **{carton['id']}** creado. Cuando el "
                               "organizador confirme tu pago, verás tu código "
                               "en **👤 Mi Cartón**.")
                    msg = (f"Hola, soy {carton['nombre']}. Envié mi Pago Móvil "
                           f"para {p['nombre']}. Ref: {carton['referencia']}.")
                    st.markdown(
                        boton_whatsapp(WHATSAPP_ADMIN, msg, "📲 Avisar por WhatsApp"),
                        unsafe_allow_html=True)
                else:
                    st.error("⚠️ Completa todos los campos.")
        else:
            with st.form("form_registro_ef", clear_on_submit=True):
                nombre_e   = st.text_input("Nombre y Apellido:")
                telefono_e = st.text_input("Teléfono (WhatsApp, ej: 584120000000):")
                nota       = st.text_area("Nota para el organizador (opcional):")
                enviar_e = st.form_submit_button("💵 Registrar pago en efectivo")
            if enviar_e:
                if nombre_e and telefono_e and p["estado"] != "Cerrada":
                    carton = {
                        "id": nuevo_id_carton(), "codigo": None,
                        "nombre": nombre_e.strip(), "telefono": telefono_e.strip(),
                        "referencia": "EFECTIVO", "nota": nota.strip(),
                        "tipo": tipo, "costo": costo, "matriz": generar_carton(),
                        "estado": "Pendiente", "partida_id": p["id"],
                        "comprobante": None, "metodo_pago": "Efectivo",
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    ss.cartones.append(carton); guardar_datos()
                    st.success(f"💵 Cartón **{carton['id']}** reservado.")
                else:
                    st.error("⚠️ Completa nombre y teléfono.")

        st.markdown("---")
        st.info("💡 Para ver tus cartones, ve a **👤 Mi Cartón**. "
                "Si vas a jugar con amigos sin apostar, ve a **🎲 Juego Amistoso**.")


# =========================================================
#  PÁGINA · 📺 SORTEO EN VIVO
# =========================================================
elif opcion == "📺 Sorteo en Vivo":
    st.title("📺 Cantadora de Balotas en Vivo")
    p = partida_actual()
    if not p:
        st.error("No hay partida activa."); st.stop()

    st.markdown(f"### 🎮 Partida: **{p['nombre']}** "
                f'<span class="pill pill-info">{p["estado"]}</span>',
                unsafe_allow_html=True)

    seccion_info_whatsapp(
        titulo="📞 INFORMACIÓN",
        subtitulo="¿Dudas? Escríbenos por WhatsApp",
        mensaje="Hola, tengo una consulta sobre el sorteo en vivo.",
        texto_boton="📲 WhatsApp",
    )

    mostrar_banner_ganador(p)

    if not p.get("pausada") and p.get("hora_sorteo"):
        delta = tiempo_restante(p["hora_sorteo"])
        st.markdown(
            f'<div class="hora-box">'
            f'<div class="hora-titulo">⏰ SORTEO PROGRAMADO</div>'
            f'<div class="hora-valor">{p["hora_sorteo"]}</div>'
            f'<div class="hora-resto">⏳ Faltan: {formatear_delta(delta)}</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([1, 1.6], gap="large")
    cantados = p["numeros_cantados"]

    with col_a:
        if cantados:
            st.markdown(
                f'<div class="card"><h4 style="text-align:center">🎱 Última balota</h4>'
                f'<div class="balota-wrap"><div class="balota">{cantados[-1]}</div></div>'
                f'<p style="text-align:center;color:#94a3b8">'
                f'Balota N° {len(cantados)} de 75</p></div>',
                unsafe_allow_html=True)
        else:
            st.info("⏳ El sorteo aún no ha comenzado.")

        if st.button("🔄 Actualizar pantalla"):
            st.rerun()

    with col_b:
        st.markdown("### 🎯 Tablero de 75 balotas")
        st.markdown(tablero_html(cantados), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📜 Historial de balotas cantadas")
    if cantados:
        st.markdown(" ".join(
            f'<span style="display:inline-block;margin:4px;padding:8px 14px;'
            f'border-radius:10px;background:#16213a;color:#ffd166;font-weight:700;'
            f'border:1px solid #26355a">{n}</span>' for n in cantados),
            unsafe_allow_html=True)
    else:
        st.caption("Sin balotas por ahora.")


# =========================================================
#  PÁGINA · ⚙️ ADMINISTRADOR (solo visible si admin_ok)
# =========================================================
elif opcion == "⚙️ Administrador" and ss.admin_ok:
    st.title("⚙️ Panel de Administrador")
    st.markdown("---")

    # Doble verificación por si alguien intenta forzar la URL
    if not ss.admin_ok:
        st.error("⛔ Acceso denegado. Debes iniciar sesión como administrador.")
        st.stop()

    with st.expander("🎮 Gestión de partidas (con apuesta)", expanded=False):
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            nombre_nueva = st.text_input("Nombre de la nueva partida:")
            pozo_inicial = st.number_input("Pozo base inicial (Bs):",
                                           min_value=0, value=0, step=50)
        with col_p2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Crear partida"):
                if nombre_nueva.strip():
                    pid = crear_partida(nombre_nueva, pozo_inicial)
                    st.success(f"✅ Partida **{pid}** creada."); st.rerun()
                else:
                    st.warning("Escribe un nombre.")
        if ss.partidas:
            st.markdown("#### Partidas existentes")
            for pid, pa in list(ss.partidas.items()):
                color = {"Abierta": "pill-ok", "En curso": "pill-wait",
                         "Cerrada": "pill-no"}[pa["estado"]]
                cc1, cc2, cc3, cc4 = st.columns([3, 1.2, 1.2, 1])
                cc1.markdown(
                    f'**{pid}** · {pa["nombre"]} '
                    f'<span class="pill {color}">{pa["estado"]}</span>'
                    + (' <span class="pill pill-pause">⏸️</span>'
                       if pa.get("pausada") else ""),
                    unsafe_allow_html=True)
                with cc2:
                    nuevo_estado = st.selectbox(
                        "Estado", ["Abierta", "En curso", "Cerrada"],
                        index=["Abierta", "En curso", "Cerrada"].index(pa["estado"]),
                        key=f"est_{pid}", label_visibility="collapsed")
                    if nuevo_estado != pa["estado"]:
                        pa["estado"] = nuevo_estado; guardar_datos(); st.rerun()
                with cc3:
                    if st.button("🔄 Reiniciar", key=f"reset_{pid}"):
                        pa["numeros_cantados"] = []
                        pa["pausada"] = False; pa["ganador"] = None
                        guardar_datos(); st.rerun()
                with cc4:
                    if st.button("🗑️ Eliminar", key=f"del_p_{pid}"):
                        ss.cartones = [c for c in ss.cartones if c["partida_id"] != pid]
                        ss.partidas.pop(pid)
                        if ss.partida_actual == pid:
                            ss.partida_actual = next(iter(ss.partidas), None)
                        guardar_datos(); st.rerun()

    p = partida_actual()
    if not p:
        st.warning("Crea una partida primero."); st.stop()

    st.markdown(f"### 🎮 Partida activa: **{p['nombre']}** "
                f'<span class="pill pill-info">{p["estado"]}</span>',
                unsafe_allow_html=True)

    if p.get("pausada") and p.get("ganador"):
        g = p["ganador"]
        mostrar_banner_ganador(p)
        st.markdown("### 🎛️ Acciones sobre el ganador")
        acc1, acc2 = st.columns(2)
        with acc1:
            if st.button("🏆 Confirmar ganador y CERRAR partida",
                         use_container_width=True):
                cerrar_por_ganador(p)
                st.success("✅ Ganador registrado y partida cerrada.")
                st.rerun()
        with acc2:
            if st.button("▶️ Reanudar partida (seguir cantando)",
                         use_container_width=True):
                reanudar_partida(p)
                st.info("▶️ Partida reanudada.")
                st.rerun()
        msg_gan = (f"🎉 ¡FELICIDADES {g['nombre']}! Has ganado el Bingo.\n\n"
                   f"🎟️ Cartón: *{g['codigo']}*\n"
                   f"🏆 Premio: {g['premio']}\n"
                   f"🎮 Partida: {p['nombre']}\n\n"
                   f"Coordino contigo la entrega del premio.")
        st.markdown(
            boton_whatsapp(g["telefono"], msg_gan,
                           "📲 Felicitar al ganador por WhatsApp"),
            unsafe_allow_html=True)
        st.markdown("---")

    with st.expander("➕ Crear cartón manualmente (para pagos recibidos)",
                     expanded=False):
        with st.form("form_carton_manual", clear_on_submit=True):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                m_nombre   = st.text_input("Nombre del jugador:")
                m_telefono = st.text_input("WhatsApp (ej: 584120000000):")
                m_tipo     = st.selectbox("Modalidad:", ["Figuras", "Lleno"])
            with col_m2:
                m_metodo     = st.selectbox("Método de pago recibido:",
                                            ["Efectivo", "Pago Móvil"])
                m_referencia = st.text_input("Referencia / Nota (opcional):")
                m_nota       = st.text_input("Nota interna (opcional):")
            crear = st.form_submit_button("🎟️ Generar cartón ahora")
        if crear:
            if m_nombre.strip() and m_telefono.strip():
                costo = PRECIO_FIGURAS if m_tipo == "Figuras" else PRECIO_LLENO
                nuevo = {
                    "id": nuevo_id_carton(), "codigo": generar_codigo_unico(),
                    "nombre": m_nombre.strip(), "telefono": m_telefono.strip(),
                    "referencia": m_referencia.strip() or "MANUAL",
                    "nota": m_nota.strip(), "tipo": m_tipo, "costo": costo,
                    "matriz": generar_carton(), "estado": "Activo",
                    "partida_id": p["id"], "comprobante": None,
                    "metodo_pago": m_metodo, "creado_por_admin": True,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                ss.cartones.append(nuevo); guardar_datos()
                ss.ultimo_carton_manual = nuevo
                st.success(f"✅ Cartón **{nuevo['id']}** · Código "
                           f"**{nuevo['codigo']}** creado."); st.rerun()
            else:
                st.error("⚠️ Nombre y WhatsApp son obligatorios.")
        if ss.ultimo_carton_manual:
            cm = ss.ultimo_carton_manual
            st.markdown("---")
            st.markdown("#### 🎉 Último cartón generado")
            st.markdown(
                f'<div class="codigo-box">'
                f'<div class="codigo-titulo">🎟️ CÓDIGO · {cm["nombre"]}</div>'
                f'<div class="codigo-valor">{cm["codigo"]}</div>'
                f'</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center">'
                        f'{carton_html(cm["matriz"], p["numeros_cantados"])}</div>',
                        unsafe_allow_html=True)
            msg_admin = (
                f"✅ ¡Hola {cm['nombre']}! Tu pago fue recibido. "
                f"Tu cartón para la partida *{p['nombre']}* está ACTIVO.\n\n"
                f"🎟️ Código: *{cm['codigo']}*\n"
                f"🎯 Modalidad: {cm['tipo']}\n"
                f"💰 Monto: {cm['costo']} Bs\n\n"
                f"Entra a la app y pulsa *👤 Mi Cartón*. ¡Mucha suerte! 🍀"
            )
            st.markdown(boton_whatsapp(cm["telefono"], msg_admin,
                                       "📲 Enviar código por WhatsApp"),
                        unsafe_allow_html=True)
            if st.button("🧹 Ocultar último cartón generado"):
                ss.ultimo_carton_manual = None; st.rerun()

    with st.expander("⏰ Programar hora del sorteo", expanded=False):
        col_h1, col_h2, col_h3 = st.columns([1.2, 1, 1])
        with col_h1:
            fecha_sel = st.date_input("📅 Fecha:", value=datetime.now().date())
        with col_h2:
            hora_sel = st.time_input("🕐 Hora:",
                                     value=(datetime.now() + timedelta(hours=1)).time())
        with col_h3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Guardar hora"):
                p["hora_sorteo"] = f"{fecha_sel} {hora_sel.strftime('%H:%M')}"
                guardar_datos()
                st.success(f"✅ Sorteo programado para **{p['hora_sorteo']}**")
                st.rerun()
        if p.get("hora_sorteo"):
            delta = tiempo_restante(p["hora_sorteo"])
            st.info(f"⏰ Programada: **{p['hora_sorteo']}** · "
                    f"⏳ Faltan: **{formatear_delta(delta)}**")
            if st.button("🗑️ Borrar hora programada"):
                p["hora_sorteo"] = None; guardar_datos(); st.rerun()

    st.markdown("---")

    with st.expander("🧪 Modo Prueba", expanded=ss.modo_prueba):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("🎲 Cantar balota de PRUEBA"):
                disp = [n for n in range(1, 76) if n not in ss.numeros_prueba]
                if disp:
                    ss.numeros_prueba.append(random.choice(disp)); st.rerun()
                else:
                    st.warning("Ya se cantaron las 75 balotas.")
        with col_t2:
            if st.button("🔄 Reiniciar prueba"):
                ss.numeros_prueba = []; st.rerun()
        with col_t3:
            ss.modo_prueba = st.toggle("🎯 Modo prueba ACTIVO",
                                       value=ss.modo_prueba,
                                       key="toggle_modo_prueba")
        if ss.numeros_prueba:
            st.markdown(tablero_html(ss.numeros_prueba, clase_extra="test"),
                        unsafe_allow_html=True)

    if ss.modo_prueba:
        st.markdown('<div class="prueba-banner">🧪 MODO PRUEBA ACTIVO</div>',
                    unsafe_allow_html=True)

    st.markdown("### 🎰 Control del sorteo real")
    partida_pausada = bool(p.get("pausada"))
    if partida_pausada:
        st.error("🛑 **Partida PAUSADA por Bingo.** Resuelve al ganador arriba.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("▶️ Cantar balota", disabled=partida_pausada):
            ok, msg = agregar_balota(p)
            if ok:
                st.rerun()
            else:
                st.warning(msg)
    with c2:
        etiqueta = "⏸️ Detener auto" if ss.auto_sorteo else "⚡ Auto sorteo"
        if st.button(etiqueta, disabled=partida_pausada and not ss.auto_sorteo):
            ss.auto_sorteo = not ss.auto_sorteo
            ss.ultimo_canto = time.time(); st.rerun()
    with c3:
        if st.button("🔄 Reiniciar balotas"):
            p["numeros_cantados"] = []
            p["pausada"] = False; p["ganador"] = None
            ss.auto_sorteo = False
            guardar_datos(); st.rerun()
    with c4:
        if st.button("🚪 Salir del admin"):
            ss.admin_ok = False; ss.auto_sorteo = False; st.rerun()

    with st.expander("⚙️ Configuración del sorteo automático",
                     expanded=ss.auto_sorteo):
        ss.intervalo_auto = st.slider("Segundos entre balotas:", 1, 30,
                                      ss.intervalo_auto)

    if ss.auto_sorteo and not partida_pausada:
        ahora = time.time()
        if ahora - ss.ultimo_canto >= ss.intervalo_auto:
            agregar_balota(p)
            ss.ultimo_canto = ahora
        time.sleep(1.0)
        st.rerun()

    if p["numeros_cantados"] and ss.ultima_balota_vista != p["numeros_cantados"][-1]:
        ss.ultima_balota_vista = p["numeros_cantados"][-1]
        reproducir_sonido()

    st.markdown("---")

    col_x, col_y = st.columns([1, 1.6], gap="large")
    with col_x:
        if p["numeros_cantados"]:
            st.markdown(
                f'<div class="card"><h4 style="text-align:center">Última balota</h4>'
                f'<div class="balota-wrap"><div class="balota">'
                f'{p["numeros_cantados"][-1]}</div></div></div>',
                unsafe_allow_html=True)
        st.metric("💰 Pozo acumulado", f"{calcular_pozo(p['id'])} Bs")
        st.metric("🎱 Balotas cantadas", f"{len(p['numeros_cantados'])}/75")
        st.metric("🎫 Cartones de esta partida",
                  len([c for c in ss.cartones if c["partida_id"] == p["id"]]))
    with col_y:
        st.markdown("### 🎯 Tablero general")
        st.markdown(tablero_html(p["numeros_cantados"]), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎫 Gestión de cartones de esta partida")

    cartones_p = [c for c in ss.cartones if c["partida_id"] == p["id"]]
    if not cartones_p:
        st.info("Aún no hay cartones registrados.")
    else:
        pendientes = len([c for c in cartones_p if c["estado"] == "Pendiente"])
        if pendientes:
            st.warning(f"⏳ **{pendientes}** cartón(es) por confirmar.")

        for c in cartones_p:
            color = {"Activo": "pill-ok", "Pendiente": "pill-wait",
                     "Rechazado": "pill-no"}.get(c["estado"], "pill-info")
            metodo = c.get("metodo_pago", "Pago Móvil")
            pill_m = "pill-cash" if metodo == "Efectivo" else "pill-info"
            tag_manual = " <span class='pill pill-man'>ADMIN</span>" \
                         if c.get("creado_por_admin") else ""
            es_ganador = bool(p.get("ganador") and p["ganador"]["carton_id"] == c["id"])
            tag_gan = " <span class='pill pill-ok'>🏆 GANADOR</span>" if es_ganador else ""

            with st.expander(f"🎟️ {c['id']} · {c['nombre']} · {c['estado']} · {metodo}"):
                st.markdown(
                    f'<span class="pill {color}">{c["estado"]}</span> '
                    f'<span class="pill {pill_m}">{metodo}</span>{tag_manual}{tag_gan} '
                    f'<span style="color:#94a3b8;font-size:13px">'
                    f'📞 {c["telefono"]} · Ref: {c["referencia"]} · '
                    f'{c["tipo"]} · {c["costo"]} Bs</span>',
                    unsafe_allow_html=True)
                if c.get("nota"):
                    st.info(f"📝 Nota: {c['nota']}")
                if c.get("codigo"):
                    st.markdown(
                        f'<div class="codigo-box">'
                        f'<div class="codigo-titulo">CÓDIGO ASIGNADO</div>'
                        f'<div class="codigo-valor">{c["codigo"]}</div>'
                        f'</div>', unsafe_allow_html=True)
                if c.get("comprobante") and os.path.exists(c["comprobante"]):
                    st.image(c["comprobante"], caption="Comprobante", width=320)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(carton_html(c["matriz"], p["numeros_cantados"]),
                            unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                b1, b2, b3 = st.columns(3)
                with b1:
                    if c["estado"] != "Activo":
                        etiqueta_btn = ("💵 Confirmar efectivo y activar"
                                        if metodo == "Efectivo"
                                        else "📱 Confirmar Pago Móvil y dar código")
                        if st.button(etiqueta_btn, key=f"ok_{c['id']}"):
                            if not c.get("codigo"):
                                c["codigo"] = generar_codigo_unico()
                            c["estado"] = "Activo"; guardar_datos()
                            st.success(f"✅ Confirmado. Código: **{c['codigo']}**")
                            st.rerun()
                    else:
                        st.button("✅ Activo", disabled=True, key=f"okd_{c['id']}")
                with b2:
                    if st.button("⛔ Rechazar", key=f"no_{c['id']}"):
                        c["estado"] = "Rechazado"; guardar_datos(); st.rerun()
                with b3:
                    if st.button("🗑️ Eliminar", key=f"del_{c['id']}"):
                        ss.cartones.remove(c); guardar_datos(); st.rerun()

                if c["estado"] == "Activo" and c.get("codigo"):
                    msg_ok = (f"✅ ¡Hola {c['nombre']}! Tu pago fue confirmado. "
                              f"Tu código es *{c['codigo']}*. Entra a la app "
                              f"en *👤 Mi Cartón*. ¡Suerte! 🍀")
                elif c["estado"] == "Pendiente":
                    msg_ok = f"Hola {c['nombre']}, estamos verificando tu pago."
                else:
                    msg_ok = f"Hola {c['nombre']}, tu pago no pudo ser verificado."

                texto_boton = ("📲 Enviar código por WhatsApp"
                               if c["estado"] == "Activo" else
                               "📲 Contactar por WhatsApp")
                st.markdown(boton_whatsapp(c["telefono"], msg_ok, texto_boton),
                            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏆 Historial de ganadores (con apuesta)")
    if not ss.ganadores:
        st.caption("Aún no se han registrado ganadores.")
    else:
        st.dataframe(ss.ganadores, use_container_width=True)
        csv_bytes = exportar_csv(ss.ganadores)
        st.download_button(
            "⬇️ Descargar ganadores (CSV)", data=csv_bytes,
            file_name=f"ganadores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.markdown("### 🎲 Mesas amistosas (sin apuestas)")
    if not ss.mesas_amistosas:
        st.caption("No hay mesas amistosas creadas. Ve a **🎲 Juego Amistoso**.")
    else:
        for mid, m in ss.mesas_amistosas.items():
            cartones_m = cartones_de_mesa(mid)
            g_actual = m.get("ganador")
            estado_txt = "⏸️ Pausada por Bingo" if m.get("pausada") else "🎉 Jugando"
            with st.expander(f"{estado_txt} · {mid} · {m['nombre']}"):
                st.markdown(
                    f"**Balotas cantadas:** {len(m['numeros_cantados'])}/75  \n"
                    f"**Cartones:** {len(cartones_m)}  \n"
                    f"**Creada:** {m.get('creada','—')}")
                if g_actual:
                    st.success(f"🏆 Último ganador: **{g_actual['nombre']}** "
                               f"({g_actual['codigo']}) · Premio: {g_actual['premio']}")
                st.markdown("**Jugadores:**")
                for c in cartones_m:
                    st.markdown(f"- 🎟️ `{c['codigo']}` · **{c['nombre']}**")
                if st.button("🗑️ Eliminar mesa", key=f"delm_admin_{mid}"):
                    borrar_mesa(mid)
                    st.rerun()

    st.markdown("---")
    seccion_info_whatsapp(
        titulo="📞 INFORMACIÓN GENERAL",
        subtitulo="Tu número de contacto para los jugadores",
        mensaje="Hola, necesito información sobre el Bingo Virtual.",
        texto_boton="📲 WhatsApp",
    )
