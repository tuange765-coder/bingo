# =========================================================
#  BINGO VIRTUAL ONLINE — Con hora del sorteo y modo prueba
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

CLAVE_ADMIN       = "Juan*316*"          # 👈 TU CONTRASEÑA
WHATSAPP_ADMIN    = "584120000000"       # 👈 Tu WhatsApp (código país + número)
PRECIO_FIGURAS    = 200
PRECIO_LLENO      = 500
INTERVALO_DEFECTO = 5
ARCHIVO_DATOS     = "datos.json"
CARPETA_COMPROB   = "comprobantes"

os.makedirs(CARPETA_COMPROB, exist_ok=True)

DATOS_PAGO = [
    ("🏦 Banco",    "Banco de Venezuela / Banesco"),
    ("🪪 Cédula",   "V-XX.XXX.XXX"),
    ("📱 Teléfono", "04XX-XXX-XXXX"),
    ("👤 Titular",  "Nombre del Titular"),
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

.codigo-box {
    background: linear-gradient(135deg, #16a34a, #065f46);
    border: 2px dashed #86efac;
    border-radius: 16px;
    padding: 18px 22px;
    text-align: center;
    margin: 12px 0;
    box-shadow: 0 0 30px rgba(34,197,94,.35);
}
.codigo-titulo { color:#d1fae5; font-size:13px; letter-spacing:2px; font-weight:700; }
.codigo-valor  { color:#fff; font-size:34px; font-weight:800; letter-spacing:4px;
                 margin-top:6px; font-family: 'Courier New', monospace; }

.pendiente-box {
    background: linear-gradient(135deg, #78350f, #451a03);
    border: 2px dashed #fcd34d;
    border-radius: 16px;
    padding: 18px 22px;
    text-align: center;
    margin: 12px 0;
}
.pendiente-titulo { color:#fef3c7; font-size:15px; font-weight:700; }
.pendiente-texto  { color:#fde68a; font-size:13px; margin-top:6px; }

.hora-box {
    background: linear-gradient(135deg, #1e40af, #1e3a8a);
    border: 2px solid #60a5fa;
    border-radius: 16px;
    padding: 16px 22px;
    text-align: center;
    margin: 12px 0;
    box-shadow: 0 0 25px rgba(59,130,246,.35);
}
.hora-titulo { color:#dbeafe; font-size:13px; letter-spacing:2px; font-weight:700; }
.hora-valor  { color:#fff; font-size:28px; font-weight:800; margin-top:6px; }
.hora-resto  { color:#93c5fd; font-size:14px; margin-top:6px; }

.prueba-banner {
    background: linear-gradient(135deg, #b45309, #78350f);
    border: 2px dashed #fbbf24;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 16px;
    text-align: center;
    color: #fef3c7;
    font-weight: 700;
    letter-spacing: 1px;
}

hr { border-color:#1f2c47; }
</style>
""", unsafe_allow_html=True)

# =========================================================
#  PERSISTENCIA
# =========================================================
def guardar_datos():
    datos = {
        "partidas": ss.partidas,
        "partida_actual": ss.partida_actual,
        "cartones": ss.cartones,
        "contador_id": ss.contador_id,
        "contador_partida": ss.contador_partida,
        "ganadores": ss.ganadores,
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

ss.setdefault("partidas",         _datos["partidas"]         if _datos else {})
ss.setdefault("partida_actual",   _datos["partida_actual"]   if _datos else None)
ss.setdefault("cartones",         _datos["cartones"]         if _datos else [])
ss.setdefault("contador_id",      _datos["contador_id"]      if _datos else 1000)
ss.setdefault("contador_partida", _datos["contador_partida"] if _datos else 0)
ss.setdefault("ganadores",        _datos["ganadores"]        if _datos else [])
ss.setdefault("admin_ok", False)
ss.setdefault("auto_sorteo", False)
ss.setdefault("intervalo_auto", INTERVALO_DEFECTO)
ss.setdefault("ultimo_canto", 0.0)
ss.setdefault("ultima_balota_vista", None)
# Modo prueba
ss.setdefault("modo_prueba", False)
ss.setdefault("numeros_prueba", [])

# =========================================================
#  FUNCIONES
# =========================================================
def crear_partida(nombre, pozo_base=0):
    ss.contador_partida += 1
    pid = f"P-{ss.contador_partida:03d}"
    ss.partidas[pid] = {
        "id": pid,
        "nombre": nombre.strip() or f"Partida {pid}",
        "estado": "Abierta",
        "numeros_cantados": [],
        "pozo_base": int(pozo_base),
        "hora_sorteo": None,
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


def generar_carton():
    rangos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    columnas = [random.sample(range(a, b + 1), 5) for a, b in rangos]
    matriz = [[columnas[c][f] for c in range(5)] for f in range(5)]
    matriz[2][2] = "★"
    return matriz


def generar_codigo_unico():
    existentes = {c.get("codigo") for c in ss.cartones if c.get("codigo")}
    while True:
        chars = string.ascii_uppercase + string.digits
        codigo = "BNG-" + "".join(random.choices(chars, k=4))
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
        if n in cantados:
            cls = f"bola on {clase_extra}".strip()
        else:
            cls = "bola"
        html += f'<div class="{cls}">{n}</div>'
    html += '</div>'
    return html


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


def registrar_ganador(partida, carton, tipo_premio):
    ss.ganadores.append({
        "fecha":    datetime.now().strftime("%Y-%m-%d %H:%M"),
        "partida":  partida["nombre"],
        "carton":   carton.get("codigo", carton["id"]),
        "jugador":  carton["nombre"],
        "telefono": carton["telefono"],
        "premio":   tipo_premio,
    })
    guardar_datos()


def exportar_csv(ganadores):
    buf = io.StringIO()
    campos = ["fecha", "partida", "carton", "jugador", "telefono", "premio"]
    w = csv.DictWriter(buf, fieldnames=campos)
    w.writeheader()
    for g in ganadores:
        w.writerow({k: g.get(k, "") for k in campos})
    return buf.getvalue().encode("utf-8")


def reproducir_sonido():
    if os.path.exists("balota.mp3"):
        try:
            st.audio("balota.mp3", format="audio/mp3", autoplay=True)
        except Exception:
            pass


def tiempo_restante(hora_str):
    """Devuelve un timedelta hasta la hora objetivo, o None si ya pasó."""
    if not hora_str:
        return None
    try:
        objetivo = datetime.strptime(hora_str, "%Y-%m-%d %H:%M")
        delta = objetivo - datetime.now()
        return delta
    except Exception:
        return None


def formatear_delta(delta):
    """Devuelve un texto amigable con el tiempo restante."""
    if delta is None:
        return ""
    if delta.total_seconds() <= 0:
        return "¡El sorteo está en curso!"
    dias = delta.days
    horas, rem = divmod(delta.seconds, 3600)
    minutos, segundos = divmod(rem, 60)
    if dias > 0:
        return f"{dias}d {horas}h {minutos}m"
    if horas > 0:
        return f"{horas}h {minutos}m {segundos}s"
    if minutos > 0:
        return f"{minutos}m {segundos}s"
    return f"{segundos}s"


if not ss.partidas:
    crear_partida("Partida de Bienvenida", pozo_base=0)


# =========================================================
#  BARRA LATERAL
# =========================================================
with st.sidebar:
    st.markdown("## 🎟️ Bingo Virtual")
    st.markdown("---")
    opcion = st.radio(
        "Navegación",
        ["🛒 Comprar / Ver Cartón", "📺 Sorteo en Vivo", "⚙️ Administrador"],
    )
    st.markdown("---")
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
        color = {"Abierta": "pill-ok", "En curso": "pill-wait", "Cerrada": "pill-no"}[p["estado"]]
        st.markdown(f'<span class="pill {color}">{p["estado"]}</span>',
                    unsafe_allow_html=True)

        # --- Hora del sorteo en sidebar ---
        if p.get("hora_sorteo"):
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
                       if c["estado"] == "Activo" and c["partida_id"] == ss.partida_actual])
        st.markdown(f"**🎫 Cartones activos:** `{activos}`")
    st.markdown("---")
    st.caption("🔞 Juega responsablemente.")


# =========================================================
#  PÁGINA 1 · COMPRAR / VER CARTÓN
# =========================================================
if opcion == "🛒 Comprar / Ver Cartón":
    st.title("🛒 Compra tu Cartón de Bingo")
    st.markdown("---")

    p = partida_actual()
    if not p:
        st.error("No hay partida activa. Contacta al administrador.")
        st.stop()

    # --- Banner con la hora programada ---
    if p.get("hora_sorteo"):
        delta = tiempo_restante(p["hora_sorteo"])
        st.markdown(
            f'<div class="hora-box">'
            f'<div class="hora-titulo">⏰ SORTEO PROGRAMADO</div>'
            f'<div class="hora-valor">{p["hora_sorteo"]}</div>'
            f'<div class="hora-resto">⏳ Faltan: {formatear_delta(delta)}</div>'
            f'</div>', unsafe_allow_html=True)

    if p["estado"] == "Cerrada":
        st.warning("⛔ Esta partida está cerrada. Elige otra en la barra lateral.")

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
        if "Figuras" in modalidad:
            costo, tipo = PRECIO_FIGURAS, "Figuras"
        else:
            costo, tipo = PRECIO_LLENO, "Lleno"

        st.markdown(
            f'<div class="card"><h4>💵 Costo del cartón</h4>'
            f'<h2 style="margin:0">{costo} Bs</h2>'
            f'<small>Modalidad: {tipo}</small></div>',
            unsafe_allow_html=True)

        st.markdown("### 2️⃣ Realiza el Pago Móvil")
        filas = "".join(
            f"<tr><td style='padding:6px 14px 6px 0;color:#94a3b8'>{k}</td>"
            f"<td style='padding:6px 0;color:#e8eefc;font-weight:600'>{v}</td></tr>"
            for k, v in DATOS_PAGO)
        st.markdown(f'<div class="card"><table style="border-collapse:collapse">{filas}</table></div>',
                    unsafe_allow_html=True)

        st.info("📌 **Importante:** tu código de cartón se te entregará "
                "**una vez el administrador confirme tu pago**.")

    with col_der:
        st.markdown("### 3️⃣ Registra tu pago")
        with st.form("form_registro", clear_on_submit=True):
            nombre     = st.text_input("Nombre y Apellido:")
            telefono   = st.text_input("Teléfono (WhatsApp, ej: 584120000000):")
            referencia = st.text_input("N° de Referencia del Pago Móvil:")
            comprobante = st.file_uploader(
                "📷 Captura del comprobante (jpg/png):",
                type=["jpg", "jpeg", "png"])
            enviar = st.form_submit_button("✅ Enviar comprobante")

        if enviar:
            if nombre and telefono and referencia and p["estado"] != "Cerrada":
                carton = {
                    "id": nuevo_id_carton(),
                    "codigo": None,
                    "nombre": nombre.strip(),
                    "telefono": telefono.strip(),
                    "referencia": referencia.strip(),
                    "tipo": tipo,
                    "costo": costo,
                    "matriz": generar_carton(),
                    "estado": "Pendiente",
                    "partida_id": p["id"],
                    "comprobante": None,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                if comprobante is not None:
                    ruta = os.path.join(CARPETA_COMPROB, f"{carton['id']}.png")
                    with open(ruta, "wb") as f:
                        f.write(comprobante.getbuffer())
                    carton["comprobante"] = ruta

                ss.cartones.append(carton)
                guardar_datos()

                st.markdown(
                    '<div class="pendiente-box">'
                    '<div class="pendiente-titulo">⏳ Pago en revisión</div>'
                    '<div class="pendiente-texto">'
                    'Tu comprobante fue recibido. Cuando el administrador '
                    'confirme tu pago, recibirás tu <b>código de cartón</b>.</div>'
                    '</div>', unsafe_allow_html=True)

                msg = (f"Hola, soy {carton['nombre']}. Envié mi comprobante "
                       f"para la partida {p['nombre']}. Modalidad: {carton['tipo']} "
                       f"({carton['costo']} Bs). Referencia: {carton['referencia']}.")
                st.markdown(
                    f'<a href="{link_whatsapp(WHATSAPP_ADMIN, msg)}" target="_blank" '
                    f'style="display:inline-block;padding:10px 18px;margin-top:8px;'
                    f'background:linear-gradient(135deg,#25d366,#128c7e);color:#fff;'
                    f'font-weight:700;border-radius:12px;text-decoration:none">'
                    f'📲 Avisar al administrador por WhatsApp</a>',
                    unsafe_allow_html=True)
            elif p["estado"] == "Cerrada":
                st.error("⛔ La partida está cerrada, no se aceptan registros.")
            else:
                st.error("⚠️ Completa todos los campos del formulario.")

    # --- CONSULTA ---
    st.markdown("---")
    st.markdown("### 🔍 Consultar el código de mi cartón")
    st.caption("Ingresa tu teléfono o la referencia del pago para ver el estado "
               "y, si ya fue confirmado, tu código de cartón.")

    busqueda = st.text_input("Teléfono o referencia del pago:")

    if busqueda:
        encontrados = [c for c in ss.cartones
                       if busqueda.strip() in c["telefono"]
                       or busqueda.strip() == c["referencia"]]
        if not encontrados:
            st.warning("No se encontraron cartones con ese dato.")

        for c in encontrados:
            nombre_partida = ss.partidas.get(c["partida_id"], {}).get("nombre", "—")
            estado = c["estado"]

            if estado == "Activo":
                st.markdown(
                    f'<div class="codigo-box">'
                    f'<div class="codigo-titulo">🎟️ CÓDIGO DE TU CARTÓN</div>'
                    f'<div class="codigo-valor">{c.get("codigo","—")}</div>'
                    f'</div>', unsafe_allow_html=True)
                st.success(f"✅ Pago confirmado · Partida: **{nombre_partida}** · "
                           f"Modalidad: **{c['tipo']}**")
                st.markdown(
                    f'<div style="text-align:center">'
                    f'{carton_html(c["matriz"], numeros_cantados())}</div>',
                    unsafe_allow_html=True)

            elif estado == "Pendiente":
                st.markdown(
                    '<div class="pendiente-box">'
                    '<div class="pendiente-titulo">⏳ Pago en revisión</div>'
                    '<div class="pendiente-texto">'
                    'Aún no se ha confirmado tu pago. Cuando el administrador lo '
                    'valide, aparecerá aquí tu código de cartón.</div>'
                    '</div>', unsafe_allow_html=True)
                st.caption(f"📞 {c['telefono']} · Ref: {c['referencia']} · "
                           f"Partida: {nombre_partida}")

            else:
                st.error(f"⛔ Pago rechazado · Partida: {nombre_partida} · "
                         f"Ref: {c['referencia']}")
                st.caption("Contacta al administrador por WhatsApp para más información.")


# =========================================================
#  PÁGINA 2 · SORTEO EN VIVO
# =========================================================
elif opcion == "📺 Sorteo en Vivo":
    st.title("📺 Cantadora de Balotas en Vivo")
    p = partida_actual()
    if not p:
        st.error("No hay partida activa.")
        st.stop()

    st.markdown(f"### 🎮 Partida: **{p['nombre']}** "
                f'<span class="pill pill-info">{p["estado"]}</span>',
                unsafe_allow_html=True)

    # --- Hora programada ---
    if p.get("hora_sorteo"):
        delta = tiempo_restante(p["hora_sorteo"])
        st.markdown(
            f'<div class="hora-box">'
            f'<div class="hora-titulo">⏰ SORTEO PROGRAMADO</div>'
            f'<div class="hora-valor">{p["hora_sorteo"]}</div>'
            f'<div class="hora-resto">⏳ Faltan: {formatear_delta(delta)}</div>'
            f'</div>', unsafe_allow_html=True)
    else:
        st.caption("ℹ️ El administrador aún no ha programado la hora del sorteo.")

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
            st.info("⏳ El sorteo aún no ha comenzado. ¡Atento al administrador!")

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
#  PÁGINA 3 · ADMINISTRADOR
# =========================================================
else:
    st.title("⚙️ Panel de Administrador")
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

    # -------- GESTIÓN DE PARTIDAS --------
    with st.expander("🎮 Gestión de partidas", expanded=False):
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            nombre_nueva = st.text_input("Nombre de la nueva partida:",
                                         placeholder="Ej: Partida Navideña")
            pozo_inicial = st.number_input("Pozo base inicial (Bs):",
                                           min_value=0, value=0, step=50)
        with col_p2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Crear partida"):
                if nombre_nueva.strip():
                    pid = crear_partida(nombre_nueva, pozo_inicial)
                    st.success(f"✅ Partida **{pid}** creada.")
                    st.rerun()
                else:
                    st.warning("Escribe un nombre.")

        if ss.partidas:
            st.markdown("#### Partidas existentes")
            for pid, pa in list(ss.partidas.items()):
                color = {"Abierta": "pill-ok", "En curso": "pill-wait",
                         "Cerrada": "pill-no"}[pa["estado"]]
                cc1, cc2, cc3, cc4 = st.columns([3, 1.2, 1.2, 1])
                cc1.markdown(f'**{pid}** · {pa["nombre"]} '
                             f'<span class="pill {color}">{pa["estado"]}</span>',
                             unsafe_allow_html=True)
                with cc2:
                    nuevo_estado = st.selectbox(
                        "Estado", ["Abierta", "En curso", "Cerrada"],
                        index=["Abierta", "En curso", "Cerrada"].index(pa["estado"]),
                        key=f"est_{pid}", label_visibility="collapsed")
                    if nuevo_estado != pa["estado"]:
                        pa["estado"] = nuevo_estado
                        guardar_datos()
                        st.rerun()
                with cc3:
                    if st.button("🔄 Reiniciar", key=f"reset_{pid}"):
                        pa["numeros_cantados"] = []
                        guardar_datos()
                        st.rerun()
                with cc4:
                    if st.button("🗑️ Eliminar", key=f"del_p_{pid}"):
                        ss.cartones = [c for c in ss.cartones if c["partida_id"] != pid]
                        ss.partidas.pop(pid)
                        if ss.partida_actual == pid:
                            ss.partida_actual = next(iter(ss.partidas), None)
                        guardar_datos()
                        st.rerun()

    # -------- PROGRAMAR HORA DEL SORTEO --------
    p = partida_actual()
    if not p:
        st.warning("Crea una partida primero.")
        st.stop()

    st.markdown(f"### 🎮 Partida activa: **{p['nombre']}** "
                f'<span class="pill pill-info">{p["estado"]}</span>',
                unsafe_allow_html=True)

    with st.expander("⏰ Programar hora del sorteo", expanded=not p.get("hora_sorteo")):
        st.markdown("Elige la fecha y hora en la que iniciará el sorteo en vivo. "
                    "Los jugadores verán una cuenta regresiva automáticamente.")
        col_h1, col_h2, col_h3 = st.columns([1.2, 1, 1])
        with col_h1:
            fecha_sel = st.date_input("📅 Fecha del sorteo:",
                                      value=datetime.now().date())
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
            st.info(f"⏰ Hora actual programada: **{p['hora_sorteo']}** · "
                    f"⏳ Faltan: **{formatear_delta(delta)}**")
            if st.button("🗑️ Borrar hora programada"):
                p["hora_sorteo"] = None
                guardar_datos()
                st.rerun()

    st.markdown("---")

    # =========================
    #  MODO PRUEBA
    # =========================
    with st.expander("🧪 Modo Prueba (sorteo de prueba sin afectar la partida real)",
                     expanded=ss.modo_prueba):
        st.caption("Aquí puedes hacer sorteos de prueba como administrador. "
                   "Las balotas que cantes aquí **NO** afectan la partida real ni "
                   "los cartones de los jugadores.")

        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if st.button("🎲 Cantar balota de PRUEBA"):
                disp = [n for n in range(1, 76) if n not in ss.numeros_prueba]
                if disp:
                    ss.numeros_prueba.append(random.choice(disp))
                    st.rerun()
                else:
                    st.warning("Ya se cantaron las 75 balotas en modo prueba.")
        with col_t2:
            if st.button("🔄 Reiniciar prueba"):
                ss.numeros_prueba = []
                st.rerun()
        with col_t3:
            nuevo_modo = st.toggle("🎯 Modo prueba ACTIVO",
                                   value=ss.modo_prueba,
                                   key="toggle_modo_prueba")
            ss.modo_prueba = nuevo_modo

        if ss.numeros_prueba:
            st.markdown(f"**Última balota de prueba:** "
                        f"`{ss.numeros_prueba[-1]}` · "
                        f"Total: `{len(ss.numeros_prueba)}/75`")
            st.markdown(tablero_html(ss.numeros_prueba, clase_extra="test"),
                        unsafe_allow_html=True)
            st.markdown("**Historial de prueba:** " +
                        " ".join(
                            f'<span style="display:inline-block;margin:3px;'
                            f'padding:6px 12px;border-radius:10px;'
                            f'background:#78350f;color:#fcd34d;font-weight:700;'
                            f'border:1px solid #f59e0b">{n}</span>'
                            for n in ss.numeros_prueba),
                        unsafe_allow_html=True)
        else:
            st.info("Aún no has cantado balotas de prueba. Pulsa **🎲 Cantar balota de PRUEBA**.")

    # Banner si el modo prueba está activo
    if ss.modo_prueba:
        st.markdown(
            '<div class="prueba-banner">'
            '🧪 MODO PRUEBA ACTIVO — Los sorteos reales están siendo monitoreados'
            '</div>', unsafe_allow_html=True)

    # -------- CONTROL DEL SORTEO REAL --------
    st.markdown("### 🎰 Control del sorteo real")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("▶️ Cantar balota"):
            disp = [n for n in range(1, 76) if n not in p["numeros_cantados"]]
            if disp:
                p["numeros_cantados"].append(random.choice(disp))
                guardar_datos()
                st.rerun()
            else:
                st.warning("Ya se cantaron las 75 balotas.")
    with c2:
        etiqueta = "⏸️ Detener auto" if ss.auto_sorteo else "⚡ Auto sorteo"
        if st.button(etiqueta):
            ss.auto_sorteo = not ss.auto_sorteo
            ss.ultimo_canto = time.time()
            st.rerun()
    with c3:
        if st.button("🔄 Reiniciar balotas"):
            p["numeros_cantados"] = []
            ss.auto_sorteo = False
            guardar_datos()
            st.rerun()
    with c4:
        if st.button("🚪 Salir"):
            ss.admin_ok = False
            ss.auto_sorteo = False
            st.rerun()

    with st.expander("⚙️ Configuración del sorteo automático", expanded=ss.auto_sorteo):
        ss.intervalo_auto = st.slider(
            "Segundos entre balotas:", min_value=1, max_value=30,
            value=ss.intervalo_auto)
        st.caption(f"⏱️ Una balota cada **{ss.intervalo_auto}** segundos.")
        if ss.auto_sorteo:
            restante = max(0, ss.intervalo_auto - (time.time() - ss.ultimo_canto))
            st.info(f"🟢 Auto sorteo ACTIVO · Próxima balota en ~{restante:.1f}s")

    if ss.auto_sorteo:
        ahora = time.time()
        if ahora - ss.ultimo_canto >= ss.intervalo_auto:
            disp = [n for n in range(1, 76) if n not in p["numeros_cantados"]]
            if disp:
                p["numeros_cantados"].append(random.choice(disp))
                ss.ultimo_canto = ahora
                guardar_datos()
            else:
                ss.auto_sorteo = False
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
        st.info("Aún no hay cartones registrados en esta partida.")
    else:
        # Contador de pendientes
        pendientes = len([c for c in cartones_p if c["estado"] == "Pendiente"])
        if pendientes:
            st.warning(f"⏳ Tienes **{pendientes}** cartón(es) pendiente(s) por confirmar.")

        for c in cartones_p:
            color = {"Activo": "pill-ok", "Pendiente": "pill-wait",
                     "Rechazado": "pill-no"}.get(c["estado"], "pill-info")
            with st.expander(f"🎟️ {c['id']} · {c['nombre']} · {c['estado']}"):
                st.markdown(
                    f'<span class="pill {color}">{c["estado"]}</span> '
                    f'<span style="color:#94a3b8;font-size:13px">'
                    f'📞 {c["telefono"]} · Ref: {c["referencia"]} · '
                    f'{c["tipo"]} · {c["costo"]} Bs</span>',
                    unsafe_allow_html=True)

                if c.get("codigo"):
                    st.markdown(
                        f'<div class="codigo-box">'
                        f'<div class="codigo-titulo">CÓDIGO ASIGNADO</div>'
                        f'<div class="codigo-valor">{c["codigo"]}</div>'
                        f'</div>', unsafe_allow_html=True)

                if c.get("comprobante") and os.path.exists(c["comprobante"]):
                    st.image(c["comprobante"], caption="Comprobante de pago",
                             width=320)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(carton_html(c["matriz"], p["numeros_cantados"]),
                            unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                b1, b2, b3 = st.columns(3)
                with b1:
                    if c["estado"] != "Activo":
                        if st.button("✅ Confirmar pago y dar código",
                                     key=f"ok_{c['id']}"):
                            if not c.get("codigo"):
                                c["codigo"] = generar_codigo_unico()
                            c["estado"] = "Activo"
                            guardar_datos()
                            st.success(f"✅ Pago confirmado. "
                                       f"Código entregado: **{c['codigo']}**")
                            st.rerun()
                    else:
                        st.button("✅ Pago confirmado", disabled=True,
                                  key=f"okd_{c['id']}")
                with b2:
                    if st.button("⛔ Rechazar", key=f"no_{c['id']}"):
                        c["estado"] = "Rechazado"
                        guardar_datos()
                        st.rerun()
                with b3:
                    if st.button("🗑️ Eliminar", key=f"del_{c['id']}"):
                        ss.cartones.remove(c)
                        guardar_datos()
                        st.rerun()

                if c["estado"] == "Activo" and c.get("codigo"):
                    msg_ok = (f"✅ ¡Hola {c['nombre']}! Tu pago fue confirmado. "
                              f"Tu código de cartón es *{c['codigo']}* para la "
                              f"partida {p['nombre']}. ¡Mucha suerte! 🍀")
                elif c["estado"] == "Pendiente":
                    msg_ok = (f"Hola {c['nombre']}, estamos verificando tu pago "
                              f"para la partida {p['nombre']}. "
                              f"En breve recibirás tu código de cartón.")
                else:
                    msg_ok = (f"Hola {c['nombre']}, tu pago para la partida "
                              f"{p['nombre']} no pudo ser verificado.")

                texto_boton = ("📲 Enviar código por WhatsApp"
                               if c["estado"] == "Activo" else
                               "📲 Contactar por WhatsApp")
                st.markdown(
                    f'<a href="{link_whatsapp(c["telefono"], msg_ok)}" '
                    f'target="_blank" style="display:inline-block;'
                    f'padding:8px 14px;background:linear-gradient(135deg,#25d366,#128c7e);'
                    f'color:#fff;font-weight:700;border-radius:10px;'
                    f'text-decoration:none;margin-bottom:10px">'
                    f'{texto_boton}</a>',
                    unsafe_allow_html=True)

                if c["estado"] == "Activo" and p["numeros_cantados"]:
                    figs = contar_figura(c["matriz"], p["numeros_cantados"])
                    logros = [k for k, v in figs.items() if v]
                    if carton_lleno(c["matriz"], p["numeros_cantados"]):
                        st.success(f"🏆 ¡CARTÓN LLENO! Ganador: {c['nombre']} "
                                   f"({c.get('codigo','—')})")
                        if st.button("🏅 Registrar ganador (Lleno)",
                                     key=f"win_lleno_{c['id']}"):
                            registrar_ganador(p, c, "Cartón Lleno")
                            st.success("✅ Ganador registrado.")
                    elif logros:
                        st.info(f"🎯 Figura completada: {', '.join(logros)} — "
                                f"{c['nombre']} ({c.get('codigo','—')})")
                        if st.button("🏅 Registrar ganador (Figura)",
                                     key=f"win_fig_{c['id']}"):
                            registrar_ganador(p, c, ", ".join(logros))
                            st.success("✅ Ganador registrado.")

    # -------- GANADORES --------
    st.markdown("---")
    st.markdown("### 🏆 Historial de ganadores")
    if not ss.ganadores:
        st.caption("Aún no se han registrado ganadores.")
    else:
        st.dataframe(ss.ganadores, use_container_width=True)
        csv_bytes = exportar_csv(ss.ganadores)
        st.download_button(
            "⬇️ Descargar ganadores (CSV)",
            data=csv_bytes,
            file_name=f"ganadores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
