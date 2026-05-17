"""
CryptoLab — Complete Streamlit App
All TPs 1-6 fully interactive.
"""

import streamlit as st
import pandas as pd
import textwrap
import secrets as secrets_mod
import hashlib
import time

def _html(markup: str) -> None:
    clean = textwrap.dedent(markup)
    if hasattr(st, "html"):
        st.html(clean)
    else:
        st.markdown(clean, unsafe_allow_html=True)

from crypto_algorithms import (
    Caesar, Affine, SimpleSubstitution, Vigenere, OTP, Playfair, Hill,
    RC4, AES, DES, TripleDES, AESFinalists,
    RSA, RSA_PSS, ElGamal, DiffieHellman, ECC, ECDSA as ECDSALib,
    HashFunctions, SHA256Scratch, HMAC,
    DSA,
    ShamirSecretSharing, Paillier,
    Schnorr, FeigeFiatShamir,
    SecureTCPServer, SecureTCPClient, SecureUDPChat, PGPHybrid, EVoting,
    gcd,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CryptoLab — Cryptography Studio",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --bg: #07080F;
        --bg-2: #0E1120;
        --panel: rgba(20, 24, 42, 0.55);
        --panel-2: rgba(28, 32, 56, 0.6);
        --border: rgba(255,255,255,0.07);
        --border-strong: rgba(255,255,255,0.14);
        --text: #ECEFF7;
        --text-dim: #9CA3B8;
        --text-faint: #6B7390;
        --accent: #8B5CF6;
        --accent-2: #06B6D4;
        --accent-3: #F472B6;
        --success: #34D399;
        --danger: #F87171;
      }
      html, body, [class*="css"], .stApp, .stMarkdown, .stText, .stTextInput, .stTextArea {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      }
      code, pre, .stCodeBlock, .stCode {
        font-family: 'JetBrains Mono', ui-monospace, monospace !important;
      }
      .stApp {
        background:
          radial-gradient(900px 500px at 8% -10%, rgba(139,92,246,0.22), transparent 55%),
          radial-gradient(800px 500px at 110% 5%, rgba(6,182,212,0.16), transparent 55%),
          radial-gradient(700px 500px at 50% 110%, rgba(244,114,182,0.10), transparent 55%),
          var(--bg);
        background-attachment: fixed;
      }
      #MainMenu, footer { visibility: hidden; height: 0; }
      header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.5rem !important;
      }
      header[data-testid="stHeader"] button[kind="header"],
      header[data-testid="stHeader"] [data-testid="stBaseButton-headerNoPadding"] {
        color: #ECEFF7 !important;
      }
      .block-container { padding-top: 0.6rem !important; padding-bottom: 4rem !important; max-width: 1240px !important; }
      .hero {
        position: relative;
        padding: 30px 36px 28px 36px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(139,92,246,0.18), rgba(6,182,212,0.12) 60%, rgba(244,114,182,0.10));
        border: 1px solid var(--border-strong);
        margin-bottom: 22px;
        overflow: hidden;
        box-shadow: 0 30px 80px -30px rgba(139,92,246,0.35), 0 1px 0 rgba(255,255,255,0.04) inset;
      }
      .hero::before {
        content: "";
        position: absolute; inset: -1px;
        background: radial-gradient(600px 200px at 100% 0%, rgba(255,255,255,0.06), transparent 60%);
        pointer-events: none;
      }
      .hero .eyebrow {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11.5px; font-weight: 600; letter-spacing: 0.18em;
        text-transform: uppercase; color: #B4A4FF;
        display: flex; align-items: center; gap: 10px;
      }
      .hero .eyebrow .dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: #8B5CF6; box-shadow: 0 0 0 4px rgba(139,92,246,0.18);
        animation: pulse 2s ease-in-out infinite;
      }
      @keyframes pulse {
        0%,100% { box-shadow: 0 0 0 4px rgba(139,92,246,0.18); }
        50%     { box-shadow: 0 0 0 8px rgba(139,92,246,0.05); }
      }
      .hero h1 {
        margin: 8px 0 6px 0;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 38px; font-weight: 700; letter-spacing: -0.025em;
        line-height: 1.05;
        background: linear-gradient(180deg, #FFFFFF 30%, #B6BCD2 100%);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
      }
      .hero p.tagline { margin: 4px 0 14px 0; color: var(--text-dim); font-size: 15px; max-width: 720px; }
      .hero .badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
      .badge {
        font-size: 11px; font-weight: 500; padding: 5px 11px; border-radius: 999px;
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
        color: #C8CFE2; backdrop-filter: blur(10px);
      }
      .badge.accent { background: rgba(139,92,246,0.14); border-color: rgba(139,92,246,0.35); color: #D8CDFF; }
      .badge.cyan   { background: rgba(6,182,212,0.12);  border-color: rgba(6,182,212,0.32);  color: #B6EAF6; }
      .howto {
        position: relative; padding: 16px 18px 16px 46px; border-radius: 14px;
        background: linear-gradient(180deg, rgba(6,182,212,0.07), rgba(6,182,212,0.02));
        border: 1px solid rgba(6,182,212,0.22); margin: 6px 0 22px 0;
        font-size: 14px; color: #D6DEEC;
      }
      .howto::before { content: "📘"; position: absolute; left: 14px; top: 14px; font-size: 18px; }
      .howto .title {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: #FFFFFF;
        font-size: 13.5px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 6px;
      }
      .howto ol { margin: 0 0 0 18px; padding: 0; }
      .howto li { margin: 3px 0; line-height: 1.55; }
      .howto b { color: #FFFFFF; }
      .theory-box {
        padding: 14px 18px 14px 46px; border-radius: 14px; position: relative;
        background: linear-gradient(180deg, rgba(139,92,246,0.08), rgba(139,92,246,0.02));
        border: 1px solid rgba(139,92,246,0.22); margin: 0 0 18px 0;
        font-size: 13.5px; color: #D6DEEC; line-height: 1.7;
      }
      .theory-box::before { content: "📐"; position: absolute; left: 14px; top: 14px; font-size: 18px; }
      .theory-box .title {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: #FFFFFF;
        font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 6px;
      }
      .answer-box {
        padding: 14px 18px 14px 46px; border-radius: 14px; position: relative;
        background: linear-gradient(180deg, rgba(52,211,153,0.10), rgba(52,211,153,0.02));
        border: 1px solid rgba(52,211,153,0.30); margin: 16px 0 0 0;
        font-size: 13.5px; color: #D6DEEC; line-height: 1.7;
      }
      .answer-box::before { content: "✅"; position: absolute; left: 14px; top: 14px; font-size: 18px; }
      .answer-box .title {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: #34D399;
        font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 6px;
      }
      .section {
        font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600;
        letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint);
        margin: 22px 0 8px 0; display: flex; align-items: center; gap: 10px;
      }
      .section::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, var(--border-strong), transparent); }
      .result-label { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--text-faint); margin: 14px 0 4px 0; font-weight: 600; }
      section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050610 0%, #0A0C18 100%);
        border-right: 1px solid var(--border);
      }
      section[data-testid="stSidebar"] > div { padding-top: 8px; }
      .brand { padding: 10px 4px 18px 4px; border-bottom: 1px solid var(--border); margin-bottom: 14px; }
      .brand .logo { display: flex; align-items: center; gap: 12px; }
      .brand .logo .mark {
        width: 38px; height: 38px; border-radius: 11px; display: grid; place-items: center;
        font-size: 19px; background: linear-gradient(135deg, #8B5CF6, #06B6D4);
        box-shadow: 0 8px 24px -8px rgba(139,92,246,0.6);
      }
      .brand h2 { margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 19px; font-weight: 700; letter-spacing: -0.01em; }
      .brand .sub { margin: 2px 0 0 0; font-size: 11.5px; color: var(--text-faint); letter-spacing: 0.04em; }
      .cat-label {
        font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700;
        letter-spacing: -0.005em; color: #FFFFFF; padding: 22px 8px 10px 8px; margin-top: 6px;
        display: flex; align-items: center; gap: 10px; border-top: 1px solid var(--border); position: relative;
      }
      .cat-label::after { content: ""; position: absolute; left: 8px; bottom: 4px; width: 22px; height: 2px; border-radius: 2px; background: linear-gradient(90deg, #8B5CF6, #06B6D4); }
      .cat-label .ic { font-size: 18px; width: 30px; height: 30px; display: grid; place-items: center; background: linear-gradient(135deg, rgba(139,92,246,0.20), rgba(6,182,212,0.14)); border: 1px solid rgba(139,92,246,0.30); border-radius: 9px; }
      section[data-testid="stSidebar"] .stButton > button {
        width: 100%; border-radius: 10px; border: 1px solid transparent; background: transparent;
        color: var(--text-dim); font-weight: 500; font-size: 13.5px; padding: 8px 12px;
        text-align: left; justify-content: flex-start !important; transition: all .15s ease;
      }
      section[data-testid="stSidebar"] .stButton > button:hover { background: rgba(139,92,246,0.10); color: #FFFFFF; border-color: rgba(139,92,246,0.25); }
      section[data-testid="stSidebar"] .stButton > button p { font-weight: 500 !important; }
      section[data-testid="stSidebar"] .nav-active .stButton > button {
        background: linear-gradient(90deg, rgba(139,92,246,0.22), rgba(139,92,246,0.04));
        color: #FFFFFF; border-color: rgba(139,92,246,0.38);
        box-shadow: 0 0 0 1px rgba(139,92,246,0.18) inset;
      }
      .main .stButton > button, div[data-testid="stHorizontalBlock"] .stButton > button {
        border-radius: 11px; border: 1px solid var(--border-strong);
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        color: #E6EAF5; font-weight: 500; padding: 9px 16px; transition: all .18s ease;
      }
      .main .stButton > button:hover, div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        border-color: rgba(139,92,246,0.55);
        background: linear-gradient(180deg, rgba(139,92,246,0.18), rgba(139,92,246,0.04));
        color: #FFFFFF; transform: translateY(-1px);
        box-shadow: 0 8px 22px -10px rgba(139,92,246,0.6);
      }
      .stButton > button:focus { box-shadow: none !important; outline: none !important; }
      .stButton > button:active { transform: translateY(0); }
      .stTextInput > div > div, .stTextArea > div > div, .stNumberInput > div > div,
      .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(20, 24, 42, 0.6) !important; border: 1px solid var(--border) !important; border-radius: 11px !important;
      }
      .stTextInput input, .stTextArea textarea, .stNumberInput input { color: #ECEFF7 !important; }
      .stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; font-size: 13.5px !important; }
      .stTextInput > label, .stTextArea > label, .stNumberInput > label,
      .stSelectbox > label, .stSlider > label, .stMultiSelect > label {
        font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase;
        letter-spacing: 0.08em; color: var(--text-faint) !important;
      }
      .stCodeBlock, pre { border-radius: 12px !important; border: 1px solid var(--border) !important; background: rgba(8, 10, 22, 0.7) !important; }
      .stCodeBlock code { font-size: 13.5px !important; }
      .stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; border-bottom: 1px solid var(--border); margin-bottom: 14px; }
      .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 10px 10px 0 0; padding: 10px 18px; color: var(--text-dim); font-weight: 500; }
      .stTabs [aria-selected="true"] { background: rgba(139,92,246,0.10) !important; color: #FFFFFF !important; border-bottom: 2px solid #8B5CF6 !important; }
      div[data-testid="stAlert"] { border-radius: 12px !important; border: 1px solid var(--border-strong) !important; backdrop-filter: blur(10px); }
      div[data-testid="stMetric"] { background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 16px 18px; backdrop-filter: blur(10px); }
      div[data-testid="stMetricLabel"] { color: var(--text-faint) !important; font-size: 11.5px !important; text-transform: uppercase; letter-spacing: 0.1em; }
      div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 18px !important; }
      .streamlit-expanderHeader, [data-testid="stExpander"] summary { background: var(--panel) !important; border-radius: 11px !important; border: 1px solid var(--border) !important; font-weight: 500 !important; }
      .stSlider [data-baseweb="slider"] > div > div { background: linear-gradient(90deg, #8B5CF6, #06B6D4) !important; }
      .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }
      .step-row { display: flex; gap: 8px; margin: 10px 0 18px 0; flex-wrap: wrap; }
      .step-chip { display: flex; align-items: center; gap: 8px; padding: 7px 13px; border-radius: 999px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); font-size: 12.5px; color: var(--text-dim); }
      .step-chip .num { width: 20px; height: 20px; border-radius: 50%; background: rgba(255,255,255,0.06); color: var(--text-dim); display: grid; place-items: center; font-size: 11px; font-weight: 700; }
      .step-chip.done { color: #FFFFFF; border-color: rgba(52,211,153,0.4); background: rgba(52,211,153,0.10); }
      .step-chip.done .num { background: #34D399; color: #062117; }
      .step-chip.current { color: #FFFFFF; border-color: rgba(139,92,246,0.5); background: rgba(139,92,246,0.15); box-shadow: 0 0 0 3px rgba(139,92,246,0.10); }
      .step-chip.current .num { background: #8B5CF6; color: #FFFFFF; }
      .party { padding: 16px 18px; border-radius: 14px; background: var(--panel); border: 1px solid var(--border); backdrop-filter: blur(10px); }
      .party h4 { margin: 0 0 8px 0; font-size: 14px; font-family: 'Space Grotesk', sans-serif; display: flex; align-items: center; gap: 8px; }
      .party .role { font-size: 10.5px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.12em; }
    </style>
    """)

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION DATA
# ─────────────────────────────────────────────────────────────────────────────
PAGES = {
    "Classical Ciphers": {
        "icon": "📜",
        "items": [
            ("Caesar",              "🏛️", "Shift cipher · TP1 Ex1.1"),
            ("Affine",              "📐", "Linear transformation · TP1"),
            ("Simple Substitution", "🔤", "Permutation key · TP1"),
            ("Vigenere",            "🗝️", "Polyalphabetic · TP1 Ex1.2"),
            ("One-Time Pad",        "📨", "Information-theoretic · TP1 Ex1.4"),
            ("Playfair",            "🎴", "5×5 digram cipher · TP1"),
            ("Hill",                "🧮", "Matrix-based cipher · TP1 Ex1.3"),
        ],
    },
    "Modern Symmetric": {
        "icon": "🛡️",
        "items": [
            ("AES",          "🔒", "Advanced Encryption Standard · TP2 Ex2.3"),
            ("DES / 3DES",   "🗝️", "Data Encryption Standard · TP2 Ex2.2"),
            ("RC4",          "🌊", "Stream cipher · TP2 Ex2.1"),
            ("AES Finalists","🏆", "5 NIST finalists benchmark · TP2 Ex2.4"),
        ],
    },
    "Asymmetric": {
        "icon": "🔑",
        "items": [
            ("RSA",            "🔐", "Rivest–Shamir–Adleman · TP3 Ex3.2"),
            ("ElGamal",        "🧠", "Discrete logarithm · TP3 Ex3.3"),
            ("Diffie-Hellman", "🤝", "Key exchange · TP3 Ex3.1"),
            ("ECC",            "📈", "Elliptic Curve Crypto · TP3 Ex3.4"),
        ],
    },
    "Hash Functions": {
        "icon": "🧬",
        "items": [
            ("Hash Functions", "#️⃣", "MD5 / SHA-256 / SHA-512 · TP4"),
            ("SHA-256 Scratch","⚙️",  "Full from-scratch implementation · TP4 Ex4.2"),
            ("HMAC",           "🔏",  "Message Authentication Code · TP4"),
        ],
    },
    "Digital Signatures": {
        "icon": "✍️",
        "items": [
            ("RSA Signatures", "📝", "PSS + PKCS#1 v1.5 · TP5 Ex5.1"),
            ("ElGamal Sign",   "✒️", "ElGamal signature scheme · TP5 Ex5.2"),
            ("DSA",            "📋", "Digital Signature Algorithm · TP5 Ex5.3"),
            ("ECDSA",          "🔺", "Elliptic Curve DSA · TP5 Ex5.3"),
        ],
    },
    "Secret Sharing": {
        "icon": "🧩",
        "items": [
            ("Shamir (k,n)", "🧩", "Threshold sharing · TP6"),
        ],
    },
    "Homomorphic Encryption": {
        "icon": "➕",
        "items": [
            ("Paillier", "➕", "Additive homomorphism · TP6 Ex6.4"),
        ],
    },
    "Identification Protocols": {
        "icon": "🪪",
        "items": [
            ("Schnorr ZKP",       "🕵️", "Zero-knowledge proof · TP6"),
            ("Feige-Fiat-Shamir", "🪪", "Quadratic residues · TP6"),
        ],
    },
    "Secure Applications": {
        "icon": "🌐",
        "items": [
            ("Live Secure Chat","📡","Real network chat · TP6 Ex6.1/6.3"),
            ("Secure TCP",    "🔌", "AES+RSA+HMAC over sockets · TP6 Ex6.1"),
            ("Secure UDP Chat","💬","AES-CTR+HMAC chat · TP6 Ex6.3"),
            ("PGP Hybrid",    "📧", "PGP-style encrypt+sign · TP6"),
        ],
    },
}

CATEGORY_OF, SUBTITLE_OF, ICON_OF = {}, {}, {}
for cat, data in PAGES.items():
    for algo, icon, sub in data["items"]:
        CATEGORY_OF[algo] = cat
        SUBTITLE_OF[algo] = sub
        ICON_OF[algo] = icon

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "Caesar"

with st.sidebar:
    _html("""
        <div class="brand">
          <div class="logo">
            <div class="mark">🔐</div>
            <div>
              <h2>CryptoLab</h2>
              <p class="sub">Cryptography studio · TP 1-6</p>
            </div>
          </div>
        </div>
        """)

    search = st.text_input(
        "Search", placeholder="🔍  Search algorithms…",
        label_visibility="collapsed", key="search_box",
    ).strip().lower()

    for category, data in PAGES.items():
        items = [(a, ic, s) for a, ic, s in data["items"]
                 if not search or search in a.lower() or search in s.lower()]
        if not items:
            continue
        _html(f'<div class="cat-label"><span class="ic">{data["icon"]}</span>{category}</div>')
        for algo, icon, _sub in items:
            is_active = st.session_state["page"] == algo
            wrapper_class = "nav-active" if is_active else ""
            _html(f'<div class="{wrapper_class}">')
            label = f"{icon}   {algo}"
            if st.button(label, key=f"nav_{algo}", use_container_width=True):
                st.session_state["page"] = algo
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

page = st.session_state["page"]
category = CATEGORY_OF.get(page, "")
cat_icon = PAGES.get(category, {}).get("icon", "🔐")
subtitle = SUBTITLE_OF.get(page, "")

_html(f"""
    <div class="hero">
      <div class="eyebrow"><span class="dot"></span>{cat_icon}  {category}</div>
      <h1>{page}</h1>
      <p class="tagline">{subtitle}. Interactive playground — try it, break it, understand it.</p>
      <div class="badge-row">
        <span class="badge accent">Interactive</span>
        <span class="badge cyan">Step-by-step</span>
        <span class="badge">Educational</span>
      </div>
    </div>
    """)

# ─────────────────────────────────────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def howto(steps):
    items = "".join(f"<li>{s}</li>" for s in steps)
    _html(f'<div class="howto"><div class="title">How to use</div><ol>{items}</ol></div>')

def theory(title, content):
    _html(f'<div class="theory-box"><div class="title">{title}</div>{content}</div>')

def answer_note(title, content):
    _html(f'<div class="answer-box"><div class="title">{title}</div>{content}</div>')

def section(title):
    _html(f'<div class="section">{title}</div>')

def result(label, value, lang=None):
    _html(f'<div class="result-label">{label}</div>')
    st.code(value, language=lang)

def step_indicator(steps, current):
    chips = ""
    for i, s in enumerate(steps, 1):
        cls = "done" if i <= current else ("current" if i == current + 1 else "")
        chips += f'<div class="step-chip {cls}"><div class="num">{i}</div>{s}</div>'
    _html(f'<div class="step-row">{chips}</div>')


# ═════════════════════════════════════════════════════════════════════════════
#  TP 1 — CLASSICAL CIPHERS
# ═════════════════════════════════════════════════════════════════════════════

if page == "Caesar":
    theory("Formula", "<b>Encrypt:</b> C = (P + k) mod 26 &nbsp;|&nbsp; <b>Decrypt:</b> P = (C − k) mod 26<br>Letters only; spaces and punctuation are preserved. k=0 means no shift (identity).")
    howto([
        "Type any plaintext or ciphertext in the text box.",
        "Pick a shift key <b>k</b> between 0 and 25.",
        "Click <b>Encrypt</b> or <b>Decrypt</b>.",
        "Use <b>Brute Force</b> to see all 26 possible decryptions — useful for cryptanalysis.",
    ])
    text = st.text_area("Text", height=120, placeholder="e.g.  HELLO WORLD")
    key = st.slider("Shift key k", 0, 25, 3)
    c1, c2, c3 = st.columns(3)
    enc_clicked = c1.button("🔒  Encrypt", use_container_width=True)
    dec_clicked = c2.button("🔓  Decrypt", use_container_width=True)
    bf_clicked  = c3.button("🔍  Brute Force (all 26)", use_container_width=True)

    if enc_clicked and text:
        r = Caesar.encrypt(text, key)
        result("Ciphertext", r)
        answer_note("What happened?", f"Each letter shifted +{key} positions. &nbsp; <code>{text[:20]}</code> → <code>{r[:20]}</code>")
    if dec_clicked and text:
        r = Caesar.decrypt(text, key)
        result("Plaintext", r)
        answer_note("What happened?", f"Each letter shifted −{key} positions (reverse of encryption).")
    if bf_clicked and text:
        section("All 26 candidate decryptions — k=0 to k=25")
        rows = [{"k": k, "Decryption": v} for k, v in Caesar.brute_force(text)]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        answer_note("Brute-force attack", "Caesar has only 26 possible keys — trivially broken by trying all shifts and picking the one that looks like readable French/English text (use frequency analysis: IC ≈ 0.074 for French).")

    section("Index of Coincidence Crack")
    if st.button("🧮  Auto-crack by IC", use_container_width=True) and text:
        k_found, decrypted = Caesar.crack_by_ic(text)
        result(f"Best key (IC method): k = {k_found}", decrypted)
        answer_note("IC method", f"Compared IC of each decryption to French IC≈0.074. Best match: k={k_found}.")


elif page == "Affine":
    theory("Formula", "<b>Encrypt:</b> C = (a·P + b) mod 26 &nbsp;|&nbsp; <b>Decrypt:</b> P = a⁻¹·(C − b) mod 26<br><b>Constraint:</b> gcd(a, 26) = 1 (a must be invertible mod 26). Valid values of a: 1,3,5,7,9,11,15,17,19,21,23,25.")
    howto([
        "Choose a valid <b>a</b> from the dropdown (all satisfy gcd(a,26)=1).",
        "Choose any <b>b</b> between 0 and 25.",
        "Enter text and click <b>Encrypt</b> or <b>Decrypt</b>.",
    ])
    text = st.text_area("Text", height=120, placeholder="e.g.  HELLO")
    valid_a = [a for a in range(1, 26) if gcd(a, 26) == 1]
    c1, c2 = st.columns(2)
    a = c1.selectbox("a — must be coprime with 26", valid_a, index=valid_a.index(7))
    b = c2.slider("b (shift)", 0, 25, 3)
    cc1, cc2 = st.columns(2)
    if cc1.button("🔒  Encrypt", use_container_width=True) and text:
        r = Affine.encrypt(text, a, b)
        result("Ciphertext", r)
        answer_note("Formula applied", f"C = ({a}·P + {b}) mod 26")
    if cc2.button("🔓  Decrypt", use_container_width=True) and text:
        from crypto_algorithms import mod_inverse
        a_inv = mod_inverse(a, 26)
        r = Affine.decrypt(text, a, b)
        result("Plaintext", r)
        answer_note("Formula applied", f"P = {a_inv}·(C − {b}) mod 26 &nbsp; (a⁻¹ = {a_inv} because {a}·{a_inv} ≡ 1 mod 26)")


elif page == "Simple Substitution":
    theory("How it works", "Each letter A-Z is mapped to a unique permutation of the alphabet. The key is a 26-letter string giving the substitution table. There are 26! ≈ 4×10²⁶ possible keys — brute-force is infeasible, but <b>frequency analysis</b> breaks it.")
    howto([
        "Click <b>Random Key</b> to generate a fresh permutation, or type your own 26-letter key.",
        "Enter text and click <b>Encrypt</b> or <b>Decrypt</b>.",
        "Scroll to <b>Frequency Analysis</b> to see letter distributions — the classic attack vector.",
    ])
    text = st.text_area("Text", height=120, placeholder="e.g.  THE QUICK BROWN FOX")
    if "sub_key" not in st.session_state:
        st.session_state["sub_key"] = SimpleSubstitution.make_key()
    c1, c2 = st.columns([3, 1])
    key = c1.text_input("Substitution key (26 unique letters)", value=st.session_state["sub_key"])
    if c2.button("🎲  Random Key", use_container_width=True):
        st.session_state["sub_key"] = SimpleSubstitution.make_key()
        st.rerun()
    cc1, cc2 = st.columns(2)
    if cc1.button("🔒  Encrypt", use_container_width=True) and text:
        r = SimpleSubstitution.encrypt(text, key)
        result("Ciphertext", r)
    if cc2.button("🔓  Decrypt", use_container_width=True) and text:
        r = SimpleSubstitution.decrypt(text, key)
        result("Plaintext", r)
    if text:
        section("Frequency Analysis — the attack tool")
        freq = SimpleSubstitution.frequency_analysis(text)
        if freq:
            df = pd.DataFrame(list(freq.items()), columns=["Letter", "Frequency (%)"])
            st.bar_chart(df.set_index("Letter"), height=250)
            answer_note("Why this matters", "In French, E≈15%, A≈8%, S≈8%… If ciphertext shows a high-frequency letter X, X likely maps to E. This breaks the cipher despite 26! keyspace.")


elif page == "Vigenere":
    theory("Formula", "<b>Encrypt:</b> Cᵢ = (Pᵢ + K[i mod |K|]) mod 26 &nbsp;|&nbsp; <b>Decrypt:</b> Pᵢ = (Cᵢ − K[i mod |K|]) mod 26<br>The key repeats cyclically. Security grows with key length. When |K|=|M|, it becomes a One-Time Pad.")
    howto([
        "Enter a keyword (e.g. SECRET). Longer keys are harder to break.",
        "Type plaintext and click <b>Encrypt</b>, or paste ciphertext and click <b>Decrypt</b>.",
        "Use <b>Kasiski Analysis</b> on a ciphertext to estimate key length — the first step of cryptanalysis.",
        "Use <b>Full Crack</b> to automatically recover the key and plaintext.",
    ])
    text = st.text_area("Text", height=120, placeholder="e.g.  ATTACKATDAWN")
    key = st.text_input("Keyword", value="SECRET")
    c1, c2 = st.columns(2)
    if c1.button("🔒  Encrypt", use_container_width=True) and text and key:
        r = Vigenere.encrypt(text, key)
        result("Ciphertext", r)
        answer_note("Key length impact", f"Key '{key}' has length {len(key)}. Short keys create repeating patterns detectable by Kasiski.")
    if c2.button("🔓  Decrypt", use_container_width=True) and text and key:
        r = Vigenere.decrypt(text, key)
        result("Plaintext", r)

    col1, col2 = st.columns(2)
    if col1.button("🔍  Kasiski Analysis", use_container_width=True) and text:
        results_k = Vigenere.kasiski(text)
        if results_k:
            section("Estimated key lengths (ranked by trigram spacing GCDs)")
            df = pd.DataFrame(results_k, columns=["Candidate length", "Supporting occurrences"])
            st.dataframe(df, hide_index=True, use_container_width=True)
            answer_note("How Kasiski works", "Repeated trigrams in ciphertext occur at distances that are multiples of the key length. GCDs of those distances reveal the most likely key length.")
        else:
            st.info("Not enough repeated sequences. Try a longer ciphertext (>100 letters).")

    if col2.button("🤖  Full Auto-Crack (IC + Freq)", use_container_width=True) and text:
        guessed_key, plaintext_guess = Vigenere.full_crack(text)
        result(f"Guessed key: {guessed_key}", plaintext_guess)
        answer_note("Auto-crack result", f"Estimated key length via IC, then recovered each key letter via frequency analysis. Key found: <b>{guessed_key}</b>")


elif page == "One-Time Pad":
    theory("True OTP (Vernam Cipher)", "Operations: <b>C = M XOR K</b> &nbsp;|&nbsp; <b>M = C XOR K</b> (XOR is self-inverse)<br>Key must be: (1) truly random, (2) at least as long as the message, (3) used exactly ONCE.<br>When all three hold, the cipher is <b>information-theoretically secure</b> (Shannon 1949).")
    howto([
        "Type a message. The key length must equal the message byte length.",
        "Click <b>Generate Key</b> to create a cryptographically random key.",
        "Click <b>Encrypt</b> (plaintext → bytes → XOR → hex). Click <b>Decrypt</b> to reverse.",
        "Try the <b>Key Reuse Attack</b> tab to see why reusing the key is catastrophic.",
        "Try <b>Crib Dragging</b> to partially recover plaintext from key-reuse XOR.",
    ])

    tab1, tab2, tab3 = st.tabs(["🔒  Encrypt / Decrypt", "⚠️  Key Reuse Vulnerability", "🎣  Crib Dragging"])

    with tab1:
        text = st.text_area("Message", height=100, placeholder="e.g.  Hello, World!")
        msg_bytes = text.encode() if text else b""
        if st.button("🔑  Generate New Key", use_container_width=True):
            st.session_state["otp_key"] = OTP.generate_key(max(len(msg_bytes), 1))
            st.session_state["otp_enc"] = None
        key_bytes = st.session_state.get("otp_key", b"")
        if key_bytes:
            st.caption(f"Key ({len(key_bytes)} bytes, hex): `{key_bytes.hex()[:60]}{'…' if len(key_bytes.hex()) > 60 else ''}`")
        c1, c2 = st.columns(2)
        if c1.button("🔒  Encrypt", use_container_width=True):
            if not key_bytes:
                st.warning("Generate a key first.")
            elif len(key_bytes) < len(msg_bytes):
                st.error(f"Key too short ({len(key_bytes)} bytes) for message ({len(msg_bytes)} bytes). Regenerate.")
            else:
                enc = OTP.encrypt(msg_bytes, key_bytes)
                st.session_state["otp_enc"] = enc
                result("Ciphertext (hex)", enc.hex())
        if c2.button("🔓  Decrypt", use_container_width=True):
            enc = st.session_state.get("otp_enc")
            if not enc or not key_bytes:
                st.warning("Encrypt something first.")
            else:
                dec = OTP.decrypt(enc, key_bytes)
                result("Decrypted message", dec.decode(errors='replace'))
                if dec == msg_bytes:
                    st.success("✓ Perfect recovery — D(E(M)) = M")

    with tab2:
        theory("Key Reuse Attack", "If the same key K is used for two messages M1 and M2:<br><b>C1 XOR C2 = M1 XOR M2</b><br>An attacker with both ciphertexts can XOR them to cancel the key.")
        col1, col2 = st.columns(2)
        m1_text = col1.text_input("Message M1", value="ATTACK AT DAWN")
        m2_text = col2.text_input("Message M2", value="DEFEND AT DUSK")
        if st.button("🧪  Demonstrate Key Reuse", use_container_width=True):
            m1b, m2b = m1_text.encode(), m2_text.encode()
            length = min(len(m1b), len(m2b))
            shared_key = OTP.generate_key(length)
            c1b = OTP.encrypt(m1b[:length], shared_key)
            c2b = OTP.encrypt(m2b[:length], shared_key)
            xor_ct = OTP.xor_ciphertexts(c1b, c2b)
            xor_pt = OTP.xor_ciphertexts(m1b[:length], m2b[:length])
            section("Results")
            cols = st.columns(3)
            with cols[0]: result("C1 (hex)", c1b.hex())
            with cols[1]: result("C2 (hex)", c2b.hex())
            with cols[2]: result("C1 XOR C2 (hex)", xor_ct.hex())
            st.success(f"C1 XOR C2 == M1 XOR M2: **{xor_ct == xor_pt}**")
            st.session_state["otp_xor_result"] = xor_ct
            answer_note("TP1.4 answer", "Attacker learns C1⊕C2=M1⊕M2. With crib-dragging, partial or full recovery is possible. OTP keys must <b>never</b> be reused.")

    with tab3:
        theory("Crib Dragging", "Slide a known word (crib) across C1⊕C2. At position i: if crib=M1[i:i+n], then XOR gives M2[i:i+n] — readable text reveals a hit.")
        xor_hex = st.text_input("C1 XOR C2 (hex)", value=st.session_state.get("otp_xor_result", b"").hex() if st.session_state.get("otp_xor_result") else "")
        crib = st.text_input("Crib (known word to drag)", value="THE")
        if st.button("🎣  Run Crib Drag", use_container_width=True) and xor_hex:
            try:
                xor_bytes = bytes.fromhex(xor_hex)
                hits = OTP.crib_drag(xor_bytes, crib)
                if hits:
                    section(f"Printable hits for crib '{crib}'")
                    rows = [{"Position": pos, "Fragment from other message": frag} for pos, frag in hits]
                    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
                    answer_note("How to use", "Each hit at position i means the other message has that text at position i. Try common words like 'the', 'and', 'attack' to recover fragments.")
                else:
                    st.info("No printable hits. Try a different crib.")
            except Exception as e:
                st.error(str(e))


elif page == "Playfair":
    theory("5×5 Matrix Cipher", "Key fills the 5×5 grid (J treated as I). Plaintext split into digrams; each pair encrypted by row/column/rectangle rules. Historically used by British military in WWI/WWII.")
    howto([
        "Choose a keyword — it fills the 5×5 matrix.",
        "Enter letters only (spaces allowed, J→I automatically).",
        "Click <b>Encrypt</b> or <b>Decrypt</b>.",
    ])
    text = st.text_area("Text (letters only)", height=120, placeholder="e.g.  HIDE THE GOLD IN THE TREE STUMP")
    key = st.text_input("Keyword", value="MONARCHY")
    c1, c2 = st.columns(2)
    if c1.button("🔒  Encrypt", use_container_width=True) and text:
        try:
            r = Playfair.encrypt(text, key)
            result("Ciphertext", r)
        except Exception as e:
            st.error(str(e))
    if c2.button("🔓  Decrypt", use_container_width=True) and text:
        try:
            r = Playfair.decrypt(text, key)
            result("Plaintext", r)
        except Exception as e:
            st.error(str(e))


elif page == "Hill":
    theory("Matrix Cipher (mod 26)", "<b>Encrypt:</b> C = K · P mod 26 &nbsp; (P = column vector of letter indices, K = key matrix)<br><b>Decrypt:</b> P = K⁻¹ · C mod 26 &nbsp; (K⁻¹ exists iff gcd(det(K), 26) = 1)<br><b>Vulnerability:</b> Known-plaintext attack recovers K by solving K = C · P⁻¹ mod 26.")
    howto([
        "Enter 4 integers for the 2×2 key matrix. The app checks invertibility automatically.",
        "Type your text (letters only; padding X added if needed).",
        "Click <b>Encrypt</b> or <b>Decrypt</b>.",
        "Use <b>Known-Plaintext Attack</b> tab to recover the key from plaintext-ciphertext pairs.",
    ])
    tab1, tab2 = st.tabs(["🔒  Encrypt / Decrypt", "🕵️  Known-Plaintext Attack"])

    with tab1:
        text = st.text_area("Text", height=120, placeholder="e.g.  HELP", key="hill_text")
        section("2×2 Key Matrix  K = [[a, b], [c, d]]")
        c1, c2 = st.columns(2)
        a = c1.number_input("a", value=3, step=1)
        b = c2.number_input("b", value=3, step=1)
        c = c1.number_input("c", value=2, step=1)
        d = c2.number_input("d", value=5, step=1)
        key_matrix = [[int(a), int(b)], [int(c), int(d)]]
        det = (int(a)*int(d) - int(b)*int(c)) % 26
        st.info(f"det(K) mod 26 = **{det}**  |  gcd({det}, 26) = **{gcd(det, 26)}**  →  {'✓ Invertible' if gcd(det,26)==1 else '✗ NOT invertible — choose different values'}")
        if gcd(det, 26) == 1:
            cc1, cc2 = st.columns(2)
            if cc1.button("🔒  Encrypt", use_container_width=True) and text:
                r = Hill.encrypt(text, key_matrix)
                st.session_state["hill_ct"] = r
                result("Ciphertext", r)
            if cc2.button("🔓  Decrypt", use_container_width=True) and text:
                r = Hill.decrypt(text, key_matrix)
                result("Plaintext", r)
            answer_note("Known-plaintext vulnerability (TP1.3)", "If an attacker knows ≥ n plaintext–ciphertext digram pairs for an n×n key, they can set up the linear system C = K·P mod 26 and solve for K directly. Even large matrices are vulnerable because the system remains linear.")

    with tab2:
        theory("Known-Plaintext Attack", "Given n² plaintext-ciphertext letter pairs, recover key K = P⁻¹ · C mod 26. Only 4 known letters (2 digrams) needed to break 2×2 Hill.")
        pt_kpa = st.text_input("Known plaintext (≥ 4 letters for 2×2)", value="HELP")
        ct_kpa = st.text_input("Corresponding ciphertext", value=st.session_state.get("hill_ct", ""))
        if st.button("🔓  Recover Key Matrix", use_container_width=True) and pt_kpa and ct_kpa:
            recovered = Hill.known_plaintext_attack(pt_kpa, ct_kpa, n=2)
            if recovered:
                result("Recovered key matrix K", str(recovered))
                st.success(f"✓ Key recovered: {recovered}")
                answer_note("Why Hill is weak", "The cipher is a linear transformation over Z₂₆. Any linear system can be solved exactly once you have enough equation pairs. Larger matrices just require more known pairs — the attack always works.")
            else:
                st.error("Could not recover key — plaintext matrix not invertible mod 26. Try different input.")


# ═════════════════════════════════════════════════════════════════════════════
#  TP 2 — MODERN SYMMETRIC
# ═════════════════════════════════════════════════════════════════════════════

elif page == "AES":
    theory("AES — Advanced Encryption Standard", "SPN (Substitution-Permutation Network). Block size = 128 bits. Keys: 128 (10 rounds), 192 (12), 256 (14).<br>Rounds: <b>SubBytes → ShiftRows → MixColumns → AddRoundKey</b> (last round skips MixColumns).<br>Modes: ECB (insecure patterns), CBC (IV chaining), CTR (stream mode, parallelisable).")
    howto([
        "Pick a key size and click <b>Generate Key</b> for a random hex key.",
        "Use tabs to switch between ECB, CBC and CTR modes.",
        "The <b>Demos</b> tab shows ECB weakness, CBC avalanche and CTR nonce-reuse.",
    ])
    key_size = st.selectbox("Key size (bits)", [128, 192, 256], index=0)
    if "aes_key" not in st.session_state:
        st.session_state["aes_key"] = AES.generate_key(128)
    c1, c2 = st.columns([3, 1])
    aes_key = c1.text_input("Key (hex)", value=st.session_state["aes_key"])
    if c2.button("🎲  New Key", use_container_width=True):
        st.session_state["aes_key"] = AES.generate_key(key_size)
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["🔲  ECB", "🔗  CBC", "🌊  CTR", "⚠️  Demos"])

    with tab1:
        theory("ECB Mode", "Each 16-byte block encrypted independently. <b>Same plaintext block → same ciphertext block</b> — leaks patterns.")
        text_ecb = st.text_area("Plaintext (ECB)", height=100, placeholder="Type any message…", key="aes_ecb_pt")
        cipher_ecb = st.text_input("Ciphertext hex (for decryption)", "", key="aes_ecb_ct")
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt ECB", use_container_width=True):
            if text_ecb:
                try:
                    ct = AES.encrypt_ecb(text_ecb, aes_key)
                    st.session_state["aes_ecb_stored"] = ct
                    result("Ciphertext (hex)", ct)
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Enter plaintext first.")
        if cc2.button("🔓  Decrypt ECB", use_container_width=True):
            ct_to_dec = cipher_ecb or st.session_state.get("aes_ecb_stored", "")
            if ct_to_dec:
                try:
                    pt = AES.decrypt_ecb(ct_to_dec, aes_key)
                    result("Plaintext", pt)
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Paste hex ciphertext or encrypt first.")

    with tab2:
        theory("CBC Mode", "Each block XORed with previous ciphertext before encryption. IV needed. <b>Recommended over ECB</b>. Bit-flip in ciphertext → predictable plaintext corruption.")
        text_cbc = st.text_area("Plaintext (CBC)", height=100, key="aes_cbc_pt", placeholder="Type any message…")
        if "aes_iv" not in st.session_state:
            st.session_state["aes_iv"] = AES.generate_iv()
        iv_col, iv_btn = st.columns([3,1])
        iv_hex = iv_col.text_input("IV (hex, 32 chars)", value=st.session_state["aes_iv"].hex(), key="aes_iv_hex")
        if iv_btn.button("🎲  New IV", use_container_width=True):
            st.session_state["aes_iv"] = AES.generate_iv()
            st.rerun()
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt CBC", use_container_width=True) and text_cbc:
            try:
                iv = bytes.fromhex(iv_hex)
                ct = AES.encrypt_cbc(text_cbc.encode(), aes_key, iv)
                st.session_state["aes_cbc_stored"] = ct.hex()
                result("Ciphertext (hex)", ct.hex())
            except Exception as e:
                st.error(str(e))
        if cc2.button("🔓  Decrypt CBC", use_container_width=True):
            stored = st.session_state.get("aes_cbc_stored", "")
            if stored:
                try:
                    iv = bytes.fromhex(iv_hex)
                    pt = AES.decrypt_cbc(bytes.fromhex(stored), aes_key, iv)
                    result("Plaintext", pt.decode(errors='replace'))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt first.")

    with tab3:
        theory("CTR Mode", "Encrypts a counter block to get keystream; XOR with plaintext. <b>No padding needed</b>, fully parallelisable. <b>Fatal flaw: never reuse nonce+key pair.</b>")
        text_ctr = st.text_area("Plaintext (CTR)", height=100, key="aes_ctr_pt", placeholder="Type any message…")
        if "aes_nonce" not in st.session_state:
            st.session_state["aes_nonce"] = AES.generate_nonce()
        n_col, n_btn = st.columns([3,1])
        nonce_hex = n_col.text_input("Nonce (hex, 16 chars)", value=st.session_state["aes_nonce"].hex(), key="aes_nonce_hex")
        if n_btn.button("🎲  New Nonce", use_container_width=True):
            st.session_state["aes_nonce"] = AES.generate_nonce()
            st.rerun()
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt CTR", use_container_width=True) and text_ctr:
            try:
                nonce = bytes.fromhex(nonce_hex)
                ct = AES.encrypt_ctr(text_ctr.encode(), aes_key, nonce)
                st.session_state["aes_ctr_stored"] = ct.hex()
                result("Ciphertext (hex)", ct.hex())
            except Exception as e:
                st.error(str(e))
        if cc2.button("🔓  Decrypt CTR", use_container_width=True):
            stored = st.session_state.get("aes_ctr_stored", "")
            if stored:
                try:
                    nonce = bytes.fromhex(nonce_hex)
                    pt = AES.decrypt_ctr(bytes.fromhex(stored), aes_key, nonce)
                    result("Plaintext", pt.decode(errors='replace'))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt first.")

    with tab4:
        section("CBC Avalanche Effect")
        av_text = st.text_area("Message for avalanche test", value="AES avalanche CBC demo message!", key="aes_av")
        if st.button("🌊  Run Avalanche (flip 1 IV bit)", use_container_width=True) and av_text:
            try:
                changed, total, pct = AES.avalanche_cbc_demo(av_text.encode(), aes_key)
                st.metric("Bits changed in ciphertext", f"{changed} / {total}", f"{pct}%")
                answer_note("CBC avalanche", f"Flipping 1 bit in the IV changed {pct}% of all output bits. CBC propagates changes through all blocks, giving a strong avalanche effect.")
            except Exception as e:
                st.error(str(e))

        section("CTR Nonce-Reuse Attack")
        m1_ctr = st.text_input("Message M1", value="ATTACK AT DAWN!", key="ctr_m1")
        m2_ctr = st.text_input("Message M2", value="DEFEND AT DUSK!", key="ctr_m2")
        if st.button("⚠️  Encrypt with Same Nonce (attack demo)", use_container_width=True):
            try:
                c1r, c2r, xor_r = AES.ctr_nonce_reuse_demo(m1_ctr.encode(), m2_ctr.encode(), aes_key)
                cols = st.columns(3)
                with cols[0]: result("C1 (hex)", c1r.hex())
                with cols[1]: result("C2 (hex)", c2r.hex())
                with cols[2]: result("C1 XOR C2 (hex)", xor_r.hex())
                answer_note("CTR nonce reuse", "C1⊕C2 = M1⊕M2 — the key cancels. An attacker XORs the ciphertexts and works on M1⊕M2 directly (same as OTP key reuse).")
            except Exception as e:
                st.error(str(e))

        section("AES Benchmark")
        if st.button("⏱️  Benchmark AES-128 / 192 / 256 (1 MB)", use_container_width=True):
            with st.spinner("Benchmarking…"):
                bench = AES.benchmark(1.0)
            cols = st.columns(3)
            for i, (bits, mbps) in enumerate(bench.items()):
                cols[i].metric(f"AES-{bits}", f"{mbps} MB/s")
            answer_note("TP2 Ex2.3 Q4", "AES-128 is fastest (10 rounds), AES-256 slowest (14 rounds). Difference is small in practice (≈40%). All three are secure — choose AES-256 for long-term security, AES-128 for performance-critical applications.")


elif page == "DES / 3DES":
    theory("DES & Triple-DES", "<b>DES:</b> 64-bit block, 56-bit key, 16 Feistel rounds. Broken by brute-force (56 bits too short) since 1997.<br><b>3DES-EDE:</b> Encrypt-Decrypt-Encrypt with 2 or 3 keys (112/168-bit effective security).<br><b>Modes:</b> ECB (each block independent — shows patterns), CBC (IV chaining — recommended).")
    howto([
        "Click <b>Generate Key + IV</b> for random DES or 3DES keys.",
        "Use the <b>DES ECB/CBC</b> tab to encrypt/decrypt with DES.",
        "Use the <b>3DES</b> tab for Triple-DES ECB.",
        "The <b>ECB Weakness</b> tab shows pattern leakage with structured data.",
    ])

    if "des_key" not in st.session_state:
        st.session_state["des_key"] = DES.generate_key()
        st.session_state["des_iv"] = DES.generate_iv()
        st.session_state["des3_key"] = TripleDES.generate_key()

    col_k, col_b = st.columns([3, 1])
    with col_k:
        des_key_hex = st.text_input("DES Key (hex, 16 chars = 8 bytes)", value=st.session_state["des_key"].hex())
        des_iv_hex  = st.text_input("DES IV (hex, 16 chars = 8 bytes)",  value=st.session_state["des_iv"].hex())
        des3_key_hex = st.text_input("3DES Key (hex, 32 chars = 16 bytes)", value=st.session_state["des3_key"].hex())
    with col_b:
        if st.button("🎲  New Keys", use_container_width=True):
            st.session_state["des_key"]  = DES.generate_key()
            st.session_state["des_iv"]   = DES.generate_iv()
            st.session_state["des3_key"] = TripleDES.generate_key()
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔒  DES ECB", "🔗  DES CBC", "🔐  3DES ECB"])

    with tab1:
        msg_ecb = st.text_area("Plaintext", height=100, key="des_ecb_pt", placeholder="Any text…")
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt DES-ECB", use_container_width=True) and msg_ecb:
            try:
                key_bytes = bytes.fromhex(des_key_hex)
                ct = DES.encrypt_ecb(msg_ecb.encode(), key_bytes)
                st.session_state["des_ecb_ct"] = ct.hex()
                result("Ciphertext (hex)", ct.hex())
            except Exception as e:
                st.error(str(e))
        if cc2.button("🔓  Decrypt DES-ECB", use_container_width=True):
            stored = st.session_state.get("des_ecb_ct", "")
            if stored:
                try:
                    key_bytes = bytes.fromhex(des_key_hex)
                    pt = DES.decrypt_ecb(bytes.fromhex(stored), key_bytes)
                    result("Plaintext", pt.decode(errors='replace'))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt something first.")
        answer_note("ECB weakness", "In ECB mode identical 8-byte plaintext blocks produce identical ciphertext blocks — structural patterns leak.")

    with tab2:
        msg_cbc = st.text_area("Plaintext", height=100, key="des_cbc_pt", placeholder="Any text…")
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt DES-CBC", use_container_width=True) and msg_cbc:
            try:
                key_bytes = bytes.fromhex(des_key_hex)
                iv_bytes  = bytes.fromhex(des_iv_hex)
                ct = DES.encrypt_cbc(msg_cbc.encode(), key_bytes, iv_bytes)
                st.session_state["des_cbc_ct"] = ct.hex()
                result("Ciphertext (hex)", ct.hex())
            except Exception as e:
                st.error(str(e))
        if cc2.button("🔓  Decrypt DES-CBC", use_container_width=True):
            stored = st.session_state.get("des_cbc_ct", "")
            if stored:
                try:
                    key_bytes = bytes.fromhex(des_key_hex)
                    iv_bytes  = bytes.fromhex(des_iv_hex)
                    pt = DES.decrypt_cbc(bytes.fromhex(stored), key_bytes, iv_bytes)
                    result("Plaintext", pt.decode(errors='replace'))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt something first.")
        answer_note("ECB vs CBC", "CBC randomises each block via XOR with the previous ciphertext (or IV). Identical plaintext blocks produce different ciphertext blocks — no pattern leakage.")

    with tab3:
        msg_3des = st.text_area("Plaintext", height=100, key="des3_pt", placeholder="Any text…")
        cc1, cc2 = st.columns(2)
        if cc1.button("🔒  Encrypt 3DES-ECB", use_container_width=True) and msg_3des:
            try:
                key3 = bytes.fromhex(des3_key_hex)
                ct = TripleDES.encrypt_ecb(msg_3des.encode(), key3)
                st.session_state["des3_ct"] = ct.hex()
                result("Ciphertext (hex)", ct.hex())
            except Exception as e:
                st.error(str(e))
        if cc2.button("🔓  Decrypt 3DES-ECB", use_container_width=True):
            stored = st.session_state.get("des3_ct", "")
            if stored:
                try:
                    key3 = bytes.fromhex(des3_key_hex)
                    pt = TripleDES.decrypt_ecb(bytes.fromhex(stored), key3)
                    result("Plaintext", pt.decode(errors='replace'))
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt something first.")

        section("Performance comparison: DES vs 3DES")
        if st.button("⏱️  Benchmark DES vs 3DES (10 KB)", use_container_width=True):
            data = secrets_mod.token_bytes(10240)
            key_bytes  = bytes.fromhex(des_key_hex)
            key3_bytes = bytes.fromhex(des3_key_hex)
            t0 = time.time(); DES.encrypt_ecb(data, key_bytes);      t_des  = time.time() - t0
            t0 = time.time(); TripleDES.encrypt_ecb(data, key3_bytes); t_3des = time.time() - t0
            c1c, c2c = st.columns(2)
            c1c.metric("DES-ECB",   f"{round(t_des*1000, 2)} ms")
            c2c.metric("3DES-ECB",  f"{round(t_3des*1000, 2)} ms", f"{round(t_3des/t_des, 1)}× slower")
            answer_note("TP2 Ex2.2 result", "3DES is approximately 3× slower than DES because it applies the DES algorithm three times. AES is 10-40× faster than 3DES. This is why 3DES was deprecated by NIST in 2019.")


elif page == "RC4":
    theory("RC4 — Stream Cipher", "Two phases: <b>KSA</b> (Key Scheduling Algorithm) initialises permutation S[0..255] from the key. <b>PRGA</b> (Pseudo-Random Generation Algorithm) outputs a keystream byte-by-byte.<br>Ciphertext = Plaintext XOR Keystream. <b>Banned in TLS 1.3</b> due to statistical biases (RC4 bias: 2nd keystream byte biased toward 0).")
    howto([
        "Enter a passphrase as the symmetric key.",
        "Type plaintext and click <b>Encrypt</b> → output is hex.",
        "To decrypt: paste the hex ciphertext and click <b>Decrypt</b>.",
        "Use <b>WEP Vulnerability</b> tab to see the IV weakness.",
        "Use <b>RC4 Bias</b> tab to visualise the statistical bias.",
    ])
    tab1, tab2, tab3 = st.tabs(["🔒  Encrypt / Decrypt", "📡  WEP Vulnerability", "📊  Statistical Bias"])

    with tab1:
        text_rc4 = st.text_area("Plaintext", height=110, placeholder="e.g.  Hello RC4!")
        cipher_hex = st.text_input("Ciphertext (hex) — for decryption", "")
        key_rc4 = st.text_input("Key (passphrase)", value="secretkey")
        c1, c2 = st.columns(2)
        if c1.button("🔒  Encrypt", use_container_width=True) and text_rc4:
            ct = RC4.encrypt(text_rc4, key_rc4)
            st.session_state["rc4_ct"] = ct
            result("Ciphertext (hex)", ct)
        if c2.button("🔓  Decrypt", use_container_width=True):
            ct_to_dec = cipher_hex or st.session_state.get("rc4_ct", "")
            if not ct_to_dec:
                st.warning("Paste hex ciphertext or encrypt something first.")
            else:
                try:
                    pt = RC4.decrypt(ct_to_dec, key_rc4)
                    result("Plaintext", pt)
                except Exception as e:
                    st.error(str(e))

    with tab2:
        theory("WEP IV Weakness", "WEP prepends a 3-byte IV to the secret key before running RC4. Weak IVs (of the form (A+3, 255, x)) create a statistical correlation between the first keystream byte and the actual key bytes. After ~40,000 packets, the full WEP key can be recovered (FMS/KoreK attack).")
        base_key = st.text_input("Base WEP key (hex, 10 chars = 5 bytes)", value="deadbeefca")
        num_ivs = st.slider("Number of IVs to test", 5, 30, 10)
        if st.button("📡  Generate IV/Keystream pairs", use_container_width=True):
            try:
                key_bytes = bytes.fromhex(base_key)
                iv_results = RC4.wep_vulnerability_demo(key_bytes, num_ivs)
                rows = [{"IV (hex)": iv, "First keystream byte": ks} for iv, ks in iv_results]
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
                answer_note("WEP attack (TP2 Ex2.1)", "Each row shows a different IV and the first byte of the resulting keystream. Statistical correlation between these and the key bytes makes the attack possible after collecting many IV-encrypted packets.")
            except Exception as e:
                st.error(str(e))

    with tab3:
        theory("RC4 Byte Bias", "The 2nd output byte of RC4 is biased toward 0 with probability 2/256 ≈ 0.78% instead of the expected 1/256 ≈ 0.39%. This is one of the biases that led to RC4 being banned in TLS 1.3.")
        n_samples = st.slider("Number of keystreams to sample", 500, 5000, 1000, step=500)
        if st.button("📊  Run Bias Analysis", use_container_width=True):
            with st.spinner(f"Generating {n_samples} keystreams…"):
                freq = RC4.rc4_bias_demo(n_samples)
            expected = n_samples / 256
            df = pd.DataFrame({
                "Byte value": list(range(256)),
                "Frequency": freq,
                "Expected": [expected] * 256,
            })
            st.bar_chart(df.set_index("Byte value")["Frequency"], height=250)
            st.metric("Byte 0 frequency", freq[0], f"{freq[0]-expected:+.1f} vs expected {expected:.1f}")
            answer_note("RC4 bias (TP2 Ex2.1)", f"With {n_samples} samples, byte 0 in position 2 appears {freq[0]} times (expected ≈{expected:.0f}). This bias is detectable and exploitable, especially in encrypted HTTP cookies (BEAST/Lucky-13 style attacks).")


elif page == "AES Finalists":
    theory("5 NIST AES Finalists (1997–2000)", "NIST received 15 candidates and selected 5 finalists. Rijndael was chosen as AES in October 2000. The 4 others remain secure alternatives used in some protocols.")
    howto([
        "Read the architecture description for each finalist.",
        "Click <b>Benchmark RC6</b> to time our pure-Python RC6 vs AES.",
        "Compare the structural descriptions side-by-side.",
    ])

    section("Architecture Overview")
    for name, desc in AESFinalists.DESCRIPTIONS.items():
        with st.expander(f"{'🏆' if name=='Rijndael' else '🔷'} {name} {'(selected as AES)' if name=='Rijndael' else ''}"):
            st.markdown(desc)

    section("RC6 — Pure Python Demo")
    theory("RC6 Reference", "RC6 uses 32-bit words, 20 rounds, 4 registers (A,B,C,D). Data-dependent rotations and integer multiplication provide diffusion. We implement the full reference spec from Rivest et al.")
    rc6_plain = st.text_input("Plaintext (16 bytes exactly, or will be padded)", value="Hello RC6 Block!")
    rc6_key_hex = st.text_input("RC6 Key (hex, 16 bytes = 32 hex chars)", value=secrets_mod.token_bytes(16).hex())
    if st.button("🔒  Encrypt with RC6", use_container_width=True):
        try:
            key_bytes = bytes.fromhex(rc6_key_hex)
            block = rc6_plain.encode()[:16].ljust(16, b'\x00')
            ct = AESFinalists.rc6_encrypt_block(block, key_bytes)
            result("RC6 Ciphertext (hex)", ct.hex())
            answer_note("RC6 note", "This is a single 128-bit block encryption following the Rivest et al. specification. RC6 was the most performance-competitive alternative to Rijndael on 32-bit processors.")
        except Exception as e:
            st.error(str(e))

    section("Benchmark: Rijndael vs RC6")
    bench_size = st.slider("Data size (KB)", 8, 128, 32)
    if st.button("⏱️  Run Benchmark", use_container_width=True):
        with st.spinner("Benchmarking…"):
            bench = AESFinalists.benchmark_all(bench_size)
        cols = st.columns(len(bench))
        for i, (name, val) in enumerate(bench.items()):
            if isinstance(val, (int, float)):
                cols[i].metric(name, f"{val} MB/s")
            else:
                cols[i].metric(name, str(val))
        answer_note("TP2 Ex2.4 Q4 — Why Rijndael won", "Serpent received the best security rating (32 rounds vs Rijndael's 10) but was significantly slower. Rijndael offered the best <b>security/performance balance</b>: efficient in hardware (AES-NI instructions), software (byte-oriented operations), and on constrained devices. NIST's primary criterion after security was practical performance across all platforms.")


# ═════════════════════════════════════════════════════════════════════════════
#  TP 3 — ASYMMETRIC
# ═════════════════════════════════════════════════════════════════════════════

elif page == "RSA":
    theory("RSA — Rivest Shamir Adleman", "<b>Key generation:</b> p,q large primes → n=pq, φ(n)=(p−1)(q−1), choose e s.t. gcd(e,φ)=1, d=e⁻¹ mod φ<br><b>Encrypt:</b> C = Mᵉ mod n &nbsp;|&nbsp; <b>Decrypt:</b> M = Cᵈ mod n<br><b>Sign:</b> S = H(M)ᵈ mod n &nbsp;|&nbsp; <b>Verify:</b> H(M) ≡ Sᵉ mod n<br>Security relies on hardness of factoring n. Standard sizes: 2048–4096 bits in production.")
    howto([
        "Click <b>Generate Key Pair</b> (512-bit for speed — use 2048 in production).",
        "In <b>Encrypt/Decrypt</b>: enter an integer smaller than n.",
        "In <b>Sign/Verify</b>: sign a text message, then verify or tamper.",
        "In <b>Hybrid</b>: encrypt a large message using AES+RSA.",
    ])
    key_bits = st.selectbox("Key size", [512, 1024], index=0)
    if st.button("🔑  Generate Key Pair", use_container_width=True):
        with st.spinner("Generating primes…"):
            st.session_state["rsa_keys"] = RSA.generate_keys(key_bits)
            st.session_state.pop("rsa_ct", None)
            st.session_state.pop("rsa_sig", None)

    if "rsa_keys" in st.session_state:
        keys = st.session_state["rsa_keys"]
        with st.expander("🔍  Key material"):
            st.code(f"n  = {hex(keys['n'])}\ne  = {keys['e']}\nd  = {hex(keys['d'])}\np  = {hex(keys['p'])}\nq  = {hex(keys['q'])}")

        tab1, tab2, tab3 = st.tabs(["🔐  Encrypt / Decrypt", "✍️  Sign / Verify", "🔀  Hybrid RSA+AES"])

        with tab1:
            st.markdown("Message must be an **integer < n** (textbook RSA, no padding).")
            msg_int = st.number_input("Message M (integer)", min_value=1, value=42, step=1)
            c1, c2 = st.columns(2)
            if c1.button("Encrypt with public key (e, n)", use_container_width=True):
                ct = RSA.encrypt(int(msg_int), keys["e"], keys["n"])
                st.session_state["rsa_ct"] = ct
                result("Ciphertext C = Mᵉ mod n", hex(ct))
            if c2.button("Decrypt with private key (d, n)", use_container_width=True):
                ct = st.session_state.get("rsa_ct")
                if ct:
                    pt = RSA.decrypt(ct, keys["d"], keys["n"])
                    result("Recovered M = Cᵈ mod n", str(pt))
                    if pt == int(msg_int):
                        st.success("✓ D(E(M)) = M — perfect recovery")
                else:
                    st.warning("Encrypt a message first.")
            answer_note("TP3 Q: Why can't RSA encrypt arbitrary-size messages?", "RSA operates mod n, so messages must be < n. For large data, use <b>hybrid encryption</b>: encrypt a random AES key with RSA, then encrypt data with AES. <b>OAEP padding</b> adds randomness to prevent chosen-plaintext attacks.")

        with tab2:
            msg_str = st.text_input("Message to sign", value="Hello RSA!")
            c1, c2 = st.columns(2)
            if c1.button("✍️  Sign with private key", use_container_width=True):
                sig = RSA.sign(msg_str, keys["d"], keys["n"])
                st.session_state["rsa_sig"] = (sig, msg_str)
                result("Signature S = H(M)ᵈ mod n", hex(sig))
            if c2.button("✓  Verify with public key", use_container_width=True):
                stored = st.session_state.get("rsa_sig")
                if stored:
                    sig, _ = stored
                    ok = RSA.verify(msg_str, sig, keys["e"], keys["n"])
                    st.success("✓ Valid — message authentic and unmodified") if ok else st.error("✗ Invalid — message tampered!")
                else:
                    st.warning("Sign a message first.")
            if st.session_state.get("rsa_sig"):
                section("Tamper Test")
                bad = st.text_input("Tampered message", value=msg_str + " [TAMPERED]")
                if st.button("🧪  Verify Tampered", use_container_width=True):
                    sig, _ = st.session_state["rsa_sig"]
                    ok = RSA.verify(bad, sig, keys["e"], keys["n"])
                    st.success("Valid (unexpected!)") if ok else st.error("✗ Rejected — tampering detected ✓")

        with tab3:
            theory("Hybrid RSA+AES", "RSA encrypts a random AES-256 key. AES-CBC encrypts the actual message. This solves RSA's size limitation and provides semantic security.")
            hybrid_msg = st.text_area("Message to encrypt (any length)", value="Secret document — too long for RSA alone!", key="hybrid_msg")
            c1, c2 = st.columns(2)
            if c1.button("🔒  Hybrid Encrypt", use_container_width=True) and hybrid_msg:
                pkg = RSA.hybrid_encrypt(hybrid_msg.encode(), keys)
                st.session_state["rsa_hybrid_pkg"] = pkg
                st.success("✓ Encrypted! AES key wrapped with RSA, message encrypted with AES-CBC.")
                result("Encrypted AES key (hex)", pkg['encrypted_key'].hex()[:64] + "…")
                result("IV (hex)", pkg['iv'].hex())
                result("Ciphertext (hex)", pkg['ciphertext'].hex()[:64] + "…")
            if c2.button("🔓  Hybrid Decrypt", use_container_width=True):
                pkg = st.session_state.get("rsa_hybrid_pkg")
                if pkg:
                    try:
                        recovered = RSA.hybrid_decrypt(pkg, keys)
                        result("Recovered message", recovered.decode(errors='replace'))
                        st.success("✓ Perfect recovery!")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Encrypt something first.")


elif page == "ElGamal":
    theory("ElGamal Cipher", "<b>Key gen:</b> p prime, g generator, x random secret, y = gˣ mod p<br><b>Encrypt(M):</b> choose random k, C = (gᵏ mod p, M·yᵏ mod p) = (c₁, c₂)<br><b>Decrypt(c₁,c₂):</b> M = c₂ · (c₁ˣ)⁻¹ mod p<br><b>Non-deterministic:</b> same M encrypted twice gives different ciphertexts (different k each time).")
    howto([
        "Click <b>Generate Keys</b>.",
        "Enter an integer M (must satisfy 1 < M < p).",
        "Click <b>Encrypt</b> to get the pair (c₁, c₂), then <b>Decrypt</b> to recover M.",
        "Use <b>Malleability</b> tab to forge Enc(2M) without knowing M or x.",
    ])
    if st.button("🔑  Generate Keys", use_container_width=True):
        with st.spinner("Generating prime p…"):
            st.session_state["eg_keys"] = ElGamal.generate_keys(128)
            st.session_state.pop("eg_ct", None)

    if "eg_keys" in st.session_state:
        k = st.session_state["eg_keys"]
        with st.expander("🔍  Key parameters"):
            st.code(f"p (prime)  = {k['p']}\ng (generator) = {k['g']}\ny (public) = {k['y']}\nx (private) = {k['x']}")

        tab1, tab2 = st.tabs(["🔒  Encrypt / Decrypt", "🔧  Malleability Demo"])

        with tab1:
            msg = st.number_input("Message M (integer)", min_value=2, value=12345, step=1)
            c1, c2, c3 = st.columns(3)
            if c1.button("🔒  Encrypt", use_container_width=True):
                if int(msg) >= k["p"]:
                    st.error(f"M must be < p = {k['p']}")
                else:
                    c1v, c2v = ElGamal.encrypt(int(msg), k["p"], k["g"], k["y"])
                    st.session_state["eg_ct"] = (c1v, c2v)
                    st.session_state["eg_msg"] = int(msg)
                    result("Ciphertext (c₁, c₂)", f"c₁ = {c1v}\nc₂ = {c2v}")
            if c2.button("🔓  Decrypt", use_container_width=True):
                ct = st.session_state.get("eg_ct")
                if ct:
                    m_dec = ElGamal.decrypt(ct[0], ct[1], k["x"], k["p"])
                    result("Decrypted M", str(m_dec))
                    st.success("✓ D(E(M)) = M") if m_dec == int(msg) else st.error(f"Got {m_dec}")
                else:
                    st.warning("Encrypt first.")
            if c3.button("🔄  Encrypt Again", use_container_width=True):
                c1v2, c2v2 = ElGamal.encrypt(int(msg), k["p"], k["g"], k["y"])
                result("New ciphertext (same M)", f"c₁ = {c1v2}\nc₂ = {c2v2}")
                st.info("Different (c₁,c₂) but both decrypt to the same M — non-determinism confirmed.")

        with tab2:
            theory("Malleability", "Given Enc(M)=(c₁,c₂), forge Enc(2M) = (c₁, 2·c₂ mod p) without knowing M or x.")
            if st.button("🔧  Forge Enc(2·M) from Enc(M)", use_container_width=True):
                ct = st.session_state.get("eg_ct")
                if not ct:
                    st.warning("Encrypt M first (in the Encrypt/Decrypt tab).")
                else:
                    c1v, c2v = ct
                    c2_forged = (2 * c2v) % k["p"]
                    m_forged = ElGamal.decrypt(c1v, c2_forged, k["x"], k["p"])
                    orig_m = st.session_state.get("eg_msg", "?")
                    result("Forged ciphertext", f"c₁ = {c1v}\nc₂ (forged) = {c2_forged}")
                    result("Decryption of forged ciphertext", str(m_forged))
                    if m_forged == (2 * orig_m) % k["p"]:
                        st.success(f"✓ Got 2·M = {m_forged} — malleability confirmed!")
                    answer_note("TP3 Ex3.3 — RSA vs ElGamal size comparison", f"RSA-2048: ciphertext = 256 bytes. ElGamal-2048: ciphertext = 512 bytes (c₁ + c₂, each 256 bytes) — <b>double the size</b>. Implication: more bandwidth required for ElGamal.")


elif page == "Diffie-Hellman":
    theory("Diffie-Hellman Key Exchange", "<b>Public params:</b> large prime p, generator g<br><b>Alice:</b> picks private a, sends A = gᵃ mod p<br><b>Bob:</b> picks private b, sends B = gᵇ mod p<br><b>Shared secret:</b> K = Bᵃ mod p = Aᵇ mod p = gᵃᵇ mod p<br>An eavesdropper sees g, p, A, B but cannot compute gᵃᵇ without solving the <b>Discrete Logarithm Problem</b>.")
    howto([
        "Click <b>Run Exchange</b> to simulate Alice & Bob over an insecure channel.",
        "Both parties must reach the <b>same shared secret</b>.",
        "Try <b>MITM Attack</b> to see what happens without authentication.",
    ])
    tab1, tab2 = st.tabs(["▶️  Key Exchange", "🕵️  MITM Attack Demo"])

    with tab1:
        if st.button("▶️  Run Exchange", use_container_width=True):
            with st.spinner("Generating prime p…"):
                p, g = DiffieHellman.generate_params(128)
                a_priv = DiffieHellman.generate_private(p)
                b_priv = DiffieHellman.generate_private(p)
                a_pub  = DiffieHellman.compute_public(g, a_priv, p)
                b_pub  = DiffieHellman.compute_public(g, b_priv, p)
                shared_a = DiffieHellman.compute_shared(b_pub, a_priv, p)
                shared_b = DiffieHellman.compute_shared(a_pub, b_priv, p)
                st.session_state["dh"] = dict(p=p, g=g, a_priv=a_priv, b_priv=b_priv, a_pub=a_pub, b_pub=b_pub, shared=shared_a, match=(shared_a == shared_b))
        if "dh" in st.session_state:
            dh = st.session_state["dh"]
            with st.expander("🌐  Public channel (visible to attacker)"):
                st.code(f"p = {dh['p']}\ng = {dh['g']}\nA = {dh['a_pub']}\nB = {dh['b_pub']}")
            c1, c2 = st.columns(2)
            with c1:
                _html(f"""<div class="party"><div class="role">Party A</div><h4>👩 Alice</h4>
                  <div class="result-label">Private a</div><code>{dh['a_priv']}</code>
                  <div class="result-label">K = Bᵃ mod p</div><code>{dh['shared']}</code></div>""")
            with c2:
                kb = DiffieHellman.compute_shared(dh['a_pub'], dh['b_priv'], dh['p'])
                _html(f"""<div class="party"><div class="role">Party B</div><h4>👨 Bob</h4>
                  <div class="result-label">Private b</div><code>{dh['b_priv']}</code>
                  <div class="result-label">K = Aᵇ mod p</div><code>{kb}</code></div>""")
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if dh["match"]:
                st.success(f"✓ Shared secret established:  K = {dh['shared']}")
            else:
                st.error("Mismatch!")

    with tab2:
        theory("Man-in-the-Middle Attack", "Without authentication, Eve intercepts A and B, substitutes her own values A′ and B′, and establishes separate sessions with Alice and Bob. She can read and re-encrypt all traffic.")
        if st.button("🕵️  Simulate MITM Attack", use_container_width=True):
            with st.spinner("…"):
                p, g = DiffieHellman.generate_params(128)
                a_priv = DiffieHellman.generate_private(p)
                b_priv = DiffieHellman.generate_private(p)
                a_pub  = DiffieHellman.compute_public(g, a_priv, p)
                b_pub  = DiffieHellman.compute_public(g, b_priv, p)
                e_priv_a = DiffieHellman.generate_private(p)
                e_priv_b = DiffieHellman.generate_private(p)
                e_pub_a  = DiffieHellman.compute_public(g, e_priv_a, p)
                e_pub_b  = DiffieHellman.compute_public(g, e_priv_b, p)
                k_alice_eve = DiffieHellman.compute_shared(e_pub_a, a_priv, p)
                k_eve_alice = DiffieHellman.compute_shared(a_pub, e_priv_a, p)
                k_bob_eve   = DiffieHellman.compute_shared(e_pub_b, b_priv, p)
                k_eve_bob   = DiffieHellman.compute_shared(b_pub, e_priv_b, p)
            st.error("⚠️ MITM ACTIVE — Eve intercepts both sessions")
            cols = st.columns(3)
            with cols[0]: _html(f'<div class="party"><div class="role">Victim A</div><h4>👩 Alice</h4><div class="result-label">Thinks shared with Bob</div><code>{k_alice_eve}</code></div>')
            with cols[1]: _html(f'<div class="party" style="border-color:rgba(248,113,113,0.4)"><div class="role" style="color:#F87171">Attacker</div><h4>😈 Eve</h4><div class="result-label">Key with Alice</div><code>{k_eve_alice}</code><div class="result-label">Key with Bob</div><code>{k_eve_bob}</code></div>')
            with cols[2]: _html(f'<div class="party"><div class="role">Victim B</div><h4>👨 Bob</h4><div class="result-label">Thinks shared with Alice</div><code>{k_bob_eve}</code></div>')
            st.success(f"Alice↔Eve match: {k_alice_eve == k_eve_alice} | Bob↔Eve match: {k_bob_eve == k_eve_bob}")
            answer_note("Counter-measure (TP3 Ex3.1)", "Authenticate the public keys: each party signs their DH value with a long-term private key (e.g. ECDSA). The other party verifies the signature with the sender's certified public key. This breaks the MITM attack — this is how TLS 1.3 works.")


elif page == "ECC":
    theory("Elliptic Curve Cryptography", "<b>Curve:</b> y² = x³ + ax + b mod p (Weierstrass form)<br><b>Group law:</b> Point addition via chord-and-tangent. Scalar mult: Q = k·P<br><b>ECDLP:</b> Given P and Q=k·P, finding k is computationally infeasible.<br><b>ECC-256 ≈ RSA-3072</b> in security (NIST SP 800-57) — much shorter keys.")
    howto([
        "Use <b>Demo Curve</b> tab to explore y²=x³+7 mod 97 point arithmetic.",
        "Use <b>ECDH P-256</b> tab to simulate a real key exchange on NIST P-256.",
        "Use <b>ECDSA</b> tab to sign and verify messages.",
    ])
    tab1, tab2, tab3 = st.tabs(["📐  Demo Curve y²=x³+7 mod 97", "🤝  ECDH P-256", "✍️  ECDSA"])

    with tab1:
        theory("Pedagogical Curve", "y² = x³ + 7 mod 97. Small prime field for manual computation. Real curves use p ≈ 2²⁵⁶.")
        if st.button("🔍  Find All Points on Curve", use_container_width=True):
            with st.spinner("Computing…"):
                curve = ECC.demo_curve()
                pts = ECC.demo_points()
                st.success(f"Found {len(pts)} points on y²=x³+7 mod 97")
                df = pd.DataFrame(pts[:30], columns=["x", "y"])
                st.dataframe(df, hide_index=True, use_container_width=True)
                if len(pts) > 30:
                    st.caption(f"…and {len(pts)-30} more points")

        section("Point Arithmetic")
        pts_for_ops = ECC.demo_points()
        if pts_for_ops:
            curve = ECC.demo_curve()
            P_idx = st.selectbox("Point P", range(min(10, len(pts_for_ops))), format_func=lambda i: str(pts_for_ops[i]))
            Q_idx = st.selectbox("Point Q", range(min(10, len(pts_for_ops))), index=1, format_func=lambda i: str(pts_for_ops[i]))
            k_scalar = st.slider("Scalar k (for k·P)", 1, 20, 5)
            P = pts_for_ops[P_idx]
            Q = pts_for_ops[Q_idx]
            col1, col2 = st.columns(2)
            if col1.button("➕  Compute P + Q", use_container_width=True):
                R = curve.point_add(P, Q)
                result(f"P = {P},  Q = {Q},  P+Q =", str(R))
                if R and curve.is_on_curve(R):
                    st.success("✓ Result is on curve")
            if col2.button(f"✖️  Compute {k_scalar}·P", use_container_width=True):
                R = curve.scalar_mul(k_scalar, P)
                result(f"{k_scalar}·{P} =", str(R))
                if R and curve.is_on_curve(R):
                    st.success("✓ Result is on curve")

    with tab2:
        theory("ECDH on NIST P-256", "Both parties generate ephemeral keypairs on P-256. They exchange public keys and compute the shared secret. The shared secret is hashed with SHA-256 to derive an AES-256 key.")
        if st.button("🤝  Run ECDH Exchange (P-256)", use_container_width=True):
            try:
                with st.spinner("Generating P-256 keypairs…"):
                    shared_a, shared_b = ECC.ecdh_p256()
                    aes_key = ECC.ecdh_derive_aes_key(shared_a)
                col1, col2 = st.columns(2)
                with col1:
                    _html(f'<div class="party"><div class="role">Party A</div><h4>👩 Alice</h4><div class="result-label">Shared secret (hex)</div><code>{shared_a.hex()[:32]}…</code></div>')
                with col2:
                    _html(f'<div class="party"><div class="role">Party B</div><h4>👨 Bob</h4><div class="result-label">Shared secret (hex)</div><code>{shared_b.hex()[:32]}…</code></div>')
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                if shared_a == shared_b:
                    st.success("✓ Both parties derived the same shared secret!")
                result("Derived AES-256 key (SHA-256 of shared secret)", aes_key)
                answer_note("TP3 Ex3.4 — ECDH + AES", "The shared secret from ECDH is put through SHA-256 to produce a uniformly random 256-bit AES key. This is the foundation of ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) used in TLS 1.3.")
            except Exception as e:
                st.error(f"Error: {e}. Ensure 'cryptography' library is installed.")

    with tab3:
        theory("ECDSA", "Sign: generate k, r=(k·G).x mod n, s=k⁻¹(H(M)+d·r) mod n → signature (r,s). Verify: w=s⁻¹, u₁=H(M)·w, u₂=r·w; check (u₁·G+u₂·Q).x mod n == r.")
        curve_name = st.selectbox("Curve", ["P-256", "P-384", "P-521"])
        if st.button("🔑  Generate ECDSA Keypair", use_container_width=True):
            try:
                priv, pub = ECDSALib.generate_keys(curve_name)
                st.session_state["ecdsa_priv"] = priv
                st.session_state["ecdsa_pub"] = pub
                st.success(f"✓ {curve_name} keypair generated")
                sizes = ECDSALib.compare_key_sizes()
                if curve_name in sizes:
                    info = sizes[curve_name]
                    st.info(f"{curve_name}: {info['security_bits']}-bit security ≈ RSA-{info['equivalent_rsa']}")
            except Exception as e:
                st.error(str(e))

        if "ecdsa_priv" in st.session_state:
            ecdsa_msg = st.text_input("Message to sign", value="ECDSA test message")
            c1, c2 = st.columns(2)
            if c1.button("✍️  Sign", use_container_width=True):
                try:
                    sig = ECDSALib.sign(ecdsa_msg.encode(), st.session_state["ecdsa_priv"])
                    st.session_state["ecdsa_sig"] = sig
                    result("Signature (DER hex)", sig.hex()[:64] + "…")
                    st.success("✓ Signed")
                except Exception as e:
                    st.error(str(e))
            if c2.button("✓  Verify", use_container_width=True):
                sig = st.session_state.get("ecdsa_sig")
                if sig:
                    try:
                        ok = ECDSALib.verify(ecdsa_msg.encode(), sig, st.session_state["ecdsa_pub"])
                        st.success("✓ Signature VALID") if ok else st.error("✗ INVALID")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Sign a message first.")

            if st.session_state.get("ecdsa_sig"):
                section("Tamper Test")
                bad_ecdsa = st.text_input("Tampered message", value=ecdsa_msg + " [BAD]")
                if st.button("🧪  Verify Tampered", use_container_width=True):
                    try:
                        ok = ECDSALib.verify(bad_ecdsa.encode(), st.session_state["ecdsa_sig"], st.session_state["ecdsa_pub"])
                        st.success("Valid (unexpected!)") if ok else st.error("✗ REJECTED — tampering detected ✓")
                    except Exception as e:
                        st.error(str(e))


# ═════════════════════════════════════════════════════════════════════════════
#  TP 4 — HASH FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "Hash Functions":
    theory("Cryptographic Hash Functions", "<b>MD5:</b> 128-bit, Merkle-Damgård, <em>broken</em> (collisions found 2004) — checksums only.<br><b>SHA-256:</b> 256-bit, 64 rounds, standard for TLS/Bitcoin/JWT.<br><b>SHA-512:</b> 512-bit, 80 rounds, faster than SHA-256 on 64-bit CPUs.<br><b>Properties:</b> pre-image resistance, 2nd pre-image resistance, collision resistance.")
    howto([
        "Type any input — all three digests are computed instantly.",
        "Click <b>Avalanche Effect</b> to see that flipping 1 bit changes ~50% of output bits.",
        "Use <b>Integrity Check</b> to verify a file hash matches a reference.",
        "Use <b>Benchmark</b> to compare MD5, SHA-256, SHA-512 throughput.",
    ])
    tab1, tab2, tab3, tab4 = st.tabs(["#️⃣  Hash & Compare", "🌊  Avalanche Effect", "✅  Integrity Check", "⏱️  Benchmark"])

    with tab1:
        text = st.text_area("Input message", height=110, value="Hello, World!", key="hash_input")
        if text:
            c1, c2, c3 = st.columns(3)
            with c1:
                result("MD5 (128 bits)", HashFunctions.md5(text))
                st.caption("⚠️ Broken — do not use for security")
            with c2:
                result("SHA-256 (256 bits)", HashFunctions.sha256(text))
                st.caption("✓ Current standard")
            with c3:
                result("SHA-512 (512 bits)", HashFunctions.sha512(text))
                st.caption("✓ Faster on 64-bit CPUs")

    with tab2:
        text2 = st.text_area("Input for avalanche test", height=80, value="CryptoLab 2026", key="aval_input")
        if text2:
            all_av = HashFunctions.avalanche_all(text2)
            for name, r in all_av.items():
                section(f"{name} Avalanche")
                m1c, m2c, m3c = st.columns(3)
                m1c.metric("Original", r['hash1'][:20] + "…")
                m2c.metric("1-bit flip", r['hash2'][:20] + "…")
                m3c.metric("Bits changed", f"{r['bits_different']} / {r['output_bits']}", f"{r['percent']}%")
            answer_note("Why ~50%?", "A cryptographic hash behaves like a random function. One input bit change propagates through all rounds, flipping on average half the output bits (ideal: 50%). MD5 shows the same effect but its collision resistance is broken.")

    with tab3:
        ref_hash = st.text_input("Reference SHA-256 (from trusted source)", placeholder="Paste the official hash here…")
        data_input = st.text_area("Content to verify", height=100, placeholder="Paste file content or message…")
        if st.button("✅  Verify Integrity", use_container_width=True) and data_input:
            computed = hashlib.sha256(data_input.encode()).hexdigest()
            result("Computed SHA-256", computed)
            if ref_hash:
                if computed.lower() == ref_hash.lower().strip():
                    st.success("✓ INTACT — hashes match")
                else:
                    st.error("✗ CORRUPTED or TAMPERED — hashes differ")

    with tab4:
        bench_mb = st.slider("Data size (MB)", 0.1, 10.0, 1.0, step=0.1)
        if st.button("⏱️  Run Hash Benchmark", use_container_width=True):
            with st.spinner(f"Hashing {bench_mb} MB…"):
                bench = HashFunctions.benchmark(bench_mb)
            cols = st.columns(3)
            for i, (name, mbps) in enumerate(bench.items()):
                cols[i].metric(name, f"{mbps} MB/s")
            answer_note("TP4 Ex4.3 — Benchmark result", "SHA-512 is often faster than SHA-256 on 64-bit CPUs because it processes 64-bit words (covering more data per operation). MD5 is fastest but insecure. For new applications, use SHA-256 or SHA-3.")


elif page == "SHA-256 Scratch":
    theory("SHA-256 From Scratch", "Full NIST FIPS 180-4 implementation in pure Python. Validated against hashlib on 10 test vectors.<br><b>Steps:</b> (1) Pad message to 512-bit multiple. (2) Expand 16 → 64 words per block. (3) 64 rounds of compression using Ch, Maj, Σ, σ functions. (4) Add to hash state.")
    howto([
        "Click <b>Run Validation</b> to test all 10 vectors against hashlib.",
        "Enter your own message and compute SHA-256 from scratch.",
        "Compare with the hashlib reference.",
    ])

    tab1, tab2 = st.tabs(["✅  Validation Suite", "🔢  Compute Hash"])

    with tab1:
        if st.button("✅  Run 10 Test Vectors", use_container_width=True):
            with st.spinner("Running SHA-256 from scratch…"):
                results_v = SHA256Scratch.validate()
            passed = sum(1 for r in results_v if r['ok'])
            if passed == len(results_v):
                st.success(f"✓ All {passed}/{len(results_v)} test vectors passed!")
            else:
                st.error(f"✗ {len(results_v) - passed} vectors FAILED")
            rows = []
            for r in results_v:
                inp = r['input']
                if isinstance(inp, bytes):
                    inp_str = inp[:20].decode(errors='replace') + ("…" if len(inp) > 20 else "")
                else:
                    inp_str = str(inp)[:20]
                rows.append({
                    "Input": inp_str,
                    "Expected": r['expected'][:16] + "…",
                    "Got":      r['actual'][:16]   + "…",
                    "✓": "✓" if r['ok'] else "✗"
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    with tab2:
        custom_msg = st.text_area("Message", value="SHA-256 from scratch!", key="sha256_custom")
        if st.button("⚙️  Compute SHA-256 (from scratch)", use_container_width=True) and custom_msg:
            scratch = SHA256Scratch.hash(custom_msg.encode())
            lib_val = hashlib.sha256(custom_msg.encode()).hexdigest()
            result("SHA-256 (from scratch)", scratch)
            result("SHA-256 (hashlib reference)", lib_val)
            if scratch == lib_val:
                st.success("✓ Match! Our implementation is correct.")
            else:
                st.error("✗ Mismatch — implementation bug!")

        section("How each step works")
        _html("""<div class="theory-box">
        <div class="title">SHA-256 Round Function</div>
        Each of 64 rounds computes:<br>
        <code>S1 = ROTR(e,6) ⊕ ROTR(e,11) ⊕ ROTR(e,25)</code><br>
        <code>Ch = (e AND f) ⊕ (~e AND g)</code><br>
        <code>temp1 = h + S1 + Ch + K[j] + W[j]</code><br>
        <code>S0 = ROTR(a,2) ⊕ ROTR(a,13) ⊕ ROTR(a,22)</code><br>
        <code>Maj = (a AND b) ⊕ (a AND c) ⊕ (b AND c)</code><br>
        <code>temp2 = S0 + Maj</code><br>
        Then rotate registers: h=g, g=f, f=e, e=d+temp1, d=c, c=b, b=a, a=temp1+temp2
        </div>""")


elif page == "HMAC":
    theory("HMAC — Hash-based Message Authentication Code (RFC 2104)", "<b>HMAC(K, M) = H((K ⊕ opad) || H((K ⊕ ipad) || M))</b><br>Provides both <b>integrity</b> (detects tampering) and <b>authenticity</b> (only key-holder can generate valid MACs).<br>Unlike a plain hash, an attacker without the key cannot forge a valid HMAC even if they know the message.")
    howto([
        "Generate or enter a secret key.",
        "Type a message and click <b>Compute HMAC</b>.",
        "Use <b>Verify</b> to check a MAC against a message.",
        "Try <b>Tamper Test</b> — change the message and verify again.",
    ])

    if "hmac_key" not in st.session_state:
        st.session_state["hmac_key"] = secrets_mod.token_bytes(32)

    k_col, k_btn = st.columns([3, 1])
    hmac_key_hex = k_col.text_input("Secret key (hex)", value=st.session_state["hmac_key"].hex())
    if k_btn.button("🎲  New Key", use_container_width=True):
        st.session_state["hmac_key"] = secrets_mod.token_bytes(32)
        st.rerun()

    algo = st.selectbox("Hash algorithm", ["sha256", "sha512", "md5"])
    message = st.text_area("Message", height=100, value="Authenticate this message!", key="hmac_msg")

    c1, c2 = st.columns(2)
    if c1.button("🔏  Compute HMAC", use_container_width=True) and message:
        try:
            key_bytes = bytes.fromhex(hmac_key_hex)
            mac = HMAC.compute(key_bytes, message.encode(), algo)
            st.session_state["hmac_mac"] = mac
            result(f"HMAC-{algo.upper()}", mac)
        except Exception as e:
            st.error(str(e))

    stored_mac = st.session_state.get("hmac_mac", "")
    mac_input = st.text_input("MAC to verify (hex)", value=stored_mac, key="hmac_mac_input")
    if c2.button("✓  Verify", use_container_width=True) and message and mac_input:
        try:
            key_bytes = bytes.fromhex(hmac_key_hex)
            ok = HMAC.verify(key_bytes, message.encode(), mac_input, algo)
            st.success("✓ MAC VALID — message authentic and unmodified") if ok else st.error("✗ MAC INVALID — tampered or wrong key!")
        except Exception as e:
            st.error(str(e))

    if st.session_state.get("hmac_mac"):
        section("Tamper Test")
        tampered = st.text_input("Tampered message", value=message + " [MODIFIED]")
        if st.button("🧪  Verify Tampered Message", use_container_width=True):
            try:
                key_bytes = bytes.fromhex(hmac_key_hex)
                ok = HMAC.verify(key_bytes, tampered.encode(), stored_mac, algo)
                st.success("Valid (unexpected!)") if ok else st.error("✗ REJECTED — HMAC protects against tampering ✓")
            except Exception as e:
                st.error(str(e))

    answer_note("HMAC vs plain hash", "A plain hash H(M) can be verified by anyone — no authentication. An attacker can substitute M with M' and compute H(M'). HMAC requires the secret key K to compute or verify. Without K, an attacker cannot forge a valid MAC for a modified message.")


# ═════════════════════════════════════════════════════════════════════════════
#  TP 5 — DIGITAL SIGNATURES
# ═════════════════════════════════════════════════════════════════════════════

elif page == "RSA Signatures":
    theory("RSA Signatures — PSS and PKCS#1 v1.5", "<b>RSA-PSS</b> (Probabilistic Signature Scheme): randomised padding — recommended for new applications. Provably secure under tight security reductions.<br><b>PKCS#1 v1.5</b>: deterministic, older standard, still widely deployed (TLS 1.2, S/MIME). Vulnerable to Bleichenbacher-style attacks if misimplemented.<br><b>Common:</b> Sign = RSA-decrypt(H(M)) with private key. Verify = RSA-encrypt(sig) with public key, compare to H(M).")
    howto([
        "Click <b>Generate 2048-bit Key Pair</b>.",
        "Use the <b>PSS</b> tab to sign and verify with the recommended scheme.",
        "Use the <b>PKCS#1 v1.5</b> tab to compare with the older scheme.",
        "Both tabs include tamper tests.",
    ])
    if st.button("🔑  Generate 2048-bit RSA Key Pair", use_container_width=True):
        with st.spinner("Generating RSA-2048 keys…"):
            priv, pub = RSA_PSS.generate_keys(2048)
            st.session_state["pss_priv"] = priv
            st.session_state["pss_pub"] = pub
            st.session_state.pop("pss_sig", None)
            st.session_state.pop("pkcs_sig", None)
        st.success("✓ RSA-2048 key pair generated")

    if "pss_priv" in st.session_state:
        tab1, tab2 = st.tabs(["🔐  RSA-PSS (Recommended)", "📄  PKCS#1 v1.5 (Legacy)"])

        with tab1:
            msg_pss = st.text_input("Message", value="Test PSS signature!", key="pss_msg")
            c1, c2 = st.columns(2)
            if c1.button("✍️  Sign (PSS)", use_container_width=True):
                try:
                    sig = RSA_PSS.sign(msg_pss.encode(), st.session_state["pss_priv"])
                    st.session_state["pss_sig"] = sig
                    result("PSS Signature (hex)", sig.hex()[:64] + "…")
                    st.success("✓ Signed with RSA-PSS")
                except Exception as e:
                    st.error(str(e))
            if c2.button("✓  Verify (PSS)", use_container_width=True):
                sig = st.session_state.get("pss_sig")
                if sig:
                    try:
                        ok = RSA_PSS.verify(msg_pss.encode(), sig, st.session_state["pss_pub"])
                        st.success("✓ PSS Signature VALID") if ok else st.error("✗ INVALID")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Sign a message first.")
            if st.session_state.get("pss_sig"):
                bad_pss = st.text_input("Tampered message", value=msg_pss + " [FAKE]", key="pss_tamper")
                if st.button("🧪  Verify Tampered (PSS)", use_container_width=True):
                    try:
                        ok = RSA_PSS.verify(bad_pss.encode(), st.session_state["pss_sig"], st.session_state["pss_pub"])
                        st.success("Valid!") if ok else st.error("✗ REJECTED ✓")
                    except Exception as e:
                        st.error(str(e))
            answer_note("PSS vs PKCS#1 v1.5", "RSA-PSS is <b>randomised</b> — signing the same message twice gives different signatures (uses a random salt). This prevents chosen-message attacks. PKCS#1 v1.5 is deterministic. Both are secure when properly implemented, but PSS has a tighter security proof.")

        with tab2:
            msg_pkcs = st.text_input("Message", value="Test PKCS#1 v1.5 signature!", key="pkcs_msg")
            c1, c2 = st.columns(2)
            if c1.button("✍️  Sign (PKCS#1 v1.5)", use_container_width=True):
                try:
                    sig = RSA_PSS.pkcs1v15_sign(msg_pkcs.encode(), st.session_state["pss_priv"])
                    st.session_state["pkcs_sig"] = sig
                    result("PKCS#1 Signature (hex)", sig.hex()[:64] + "…")
                    st.success("✓ Signed with PKCS#1 v1.5")
                except Exception as e:
                    st.error(str(e))
            if c2.button("✓  Verify (PKCS#1 v1.5)", use_container_width=True):
                sig = st.session_state.get("pkcs_sig")
                if sig:
                    try:
                        ok = RSA_PSS.pkcs1v15_verify(msg_pkcs.encode(), sig, st.session_state["pss_pub"])
                        st.success("✓ PKCS#1 Signature VALID") if ok else st.error("✗ INVALID")
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.warning("Sign a message first.")
            if st.session_state.get("pkcs_sig"):
                bad_pkcs = st.text_input("Tampered message", value=msg_pkcs + " [FAKE]", key="pkcs_tamper")
                if st.button("🧪  Verify Tampered (PKCS#1)", use_container_width=True):
                    try:
                        ok = RSA_PSS.pkcs1v15_verify(bad_pkcs.encode(), st.session_state["pkcs_sig"], st.session_state["pss_pub"])
                        st.success("Valid!") if ok else st.error("✗ REJECTED ✓")
                    except Exception as e:
                        st.error(str(e))


elif page == "ElGamal Sign":
    theory("ElGamal Signature Scheme", "<b>Sign(M):</b> choose random k with gcd(k, p−1)=1; r=gᵏ mod p; s=k⁻¹(H(M)−xr) mod (p−1) → (r, s)<br><b>Verify(M,r,s):</b> check gᴴ⁽ᴹ⁾ ≡ yʳ·rˢ mod p<br><b>Warning:</b> k must be unique per signature and secret — reusing k exposes the private key x.")
    howto([
        "Click <b>Generate Keys</b>.",
        "Enter a message and click <b>Sign</b>.",
        "Click <b>Verify</b> — should accept. Click <b>Verify Tampered</b> — should reject.",
    ])
    if st.button("🔑  Generate Keys", use_container_width=True):
        with st.spinner("Generating prime p…"):
            st.session_state["eg_sig_keys"] = ElGamal.generate_keys(128)
            st.session_state.pop("eg_sig_rs", None)

    if "eg_sig_keys" in st.session_state:
        k = st.session_state["eg_sig_keys"]
        with st.expander("🔍  Key parameters"):
            st.code(f"p = {k['p']}\ng = {k['g']}\ny (public) = {k['y']}\nx (private) = {k['x']}")

        msg_eg = st.text_input("Message to sign", value="Sign this with ElGamal!")
        c1, c2 = st.columns(2)
        if c1.button("✍️  Sign", use_container_width=True):
            try:
                r, s = ElGamal.sign(msg_eg, k['p'], k['g'], k['x'])
                st.session_state["eg_sig_rs"] = (r, s, msg_eg)
                result("Signature (r, s)", f"r = {r}\ns = {s}")
            except Exception as e:
                st.error(str(e))
        if c2.button("✓  Verify", use_container_width=True):
            stored = st.session_state.get("eg_sig_rs")
            if stored:
                r, s, _ = stored
                ok = ElGamal.verify_sig(msg_eg, r, s, k['p'], k['g'], k['y'])
                st.success("✓ Signature VALID") if ok else st.error("✗ INVALID")
            else:
                st.warning("Sign a message first.")

        if st.session_state.get("eg_sig_rs"):
            section("Tamper Test")
            bad_eg = st.text_input("Tampered message", value=msg_eg + " [FAKE]")
            if st.button("🧪  Verify Tampered", use_container_width=True):
                r, s, _ = st.session_state["eg_sig_rs"]
                ok = ElGamal.verify_sig(bad_eg, r, s, k['p'], k['g'], k['y'])
                st.success("Valid (unexpected!)") if ok else st.error("✗ REJECTED ✓")

        answer_note("TP5 Ex5.2 — Nonce k reuse attack", "If the same k is used to sign two messages M₁ and M₂ with signatures (r,s₁) and (r,s₂), then: s₁−s₂ = k⁻¹(H(M₁)−H(M₂)) mod (p−1). Solving for k: k = (H(M₁)−H(M₂))·(s₁−s₂)⁻¹ mod (p−1). Then x = (H(M)−k·r)·r⁻¹ mod (p−1). This is why k must be freshly random per signature.")


elif page == "DSA":
    theory("Digital Signature Algorithm", "<b>Params:</b> q (160–256 bit prime), p (1024-bit prime with q|(p−1)), g of order q<br><b>Sign(M):</b> k random ∈ [1,q−1]; r=(gᵏ mod p) mod q; s=k⁻¹(H(M)+xr) mod q → signature (r,s)<br><b>Verify(M,r,s):</b> w=s⁻¹ mod q; u₁=H(M)·w mod q; u₂=r·w mod q; v=(gᵘ¹·yᵘ² mod p) mod q; accept iff v=r<br><b>Security note:</b> if k is reused or predictable, x (private key) can be recovered!")
    howto([
        "Click <b>Generate Parameters</b> to create p, q, g, x, y.",
        "Type a message and click <b>Sign</b>.",
        "Click <b>Verify</b> with the same message — should say VALID.",
        "Use <b>Tamper Test</b> — modify the message after signing — should REJECT.",
    ])
    if st.button("🔑  Generate DSA Parameters (q=160, p=1024 bits)", use_container_width=True):
        with st.spinner("Generating primes…"):
            st.session_state["dsa"] = DSA.generate_params(q_bits=160, p_bits=1024)
            st.session_state.pop("dsa_sig", None)

    if "dsa" in st.session_state:
        params = st.session_state["dsa"]
        with st.expander("🔍  Parameters"):
            st.code(f"q = {params['q']} ({params['q'].bit_length()} bits)\ng = {params['g']}\ny (public) = {params['y']}")

        msg = st.text_input("Message", value="Sign this message!", key="dsa_msg")
        c1, c2 = st.columns(2)
        if c1.button("✍️  Sign", use_container_width=True):
            if msg:
                r, s = DSA.sign(msg, params["p"], params["q"], params["g"], params["x"])
                st.session_state["dsa_sig"] = (r, s, msg)
                result("Signature (r, s)", f"r = {r}\ns = {s}")
            else:
                st.warning("Enter a message first.")
        if c2.button("✓  Verify", use_container_width=True):
            stored = st.session_state.get("dsa_sig")
            if stored:
                r, s, _ = stored
                ok = DSA.verify(msg, r, s, params["p"], params["q"], params["g"], params["y"])
                st.success("✓ Signature VALID") if ok else st.error("✗ Signature INVALID")
            else:
                st.warning("Sign a message first.")

        if st.session_state.get("dsa_sig"):
            section("Tamper Test")
            bad_msg = st.text_input("Tampered message", value=msg + " [MODIFIED]")
            if st.button("🧪  Verify Tampered Message", use_container_width=True):
                r, s, _ = st.session_state["dsa_sig"]
                ok = DSA.verify(bad_msg, r, s, params["p"], params["q"], params["g"], params["y"])
                st.success("Valid (unexpected!)") if ok else st.error("✗ REJECTED — tampering detected ✓")
            answer_note("Security note (TP5 Ex5.3)", "DSA provides <b>authenticity</b> (only x-holder can sign), <b>integrity</b> (any change invalidates signature), and <b>non-repudiation</b> (signer cannot deny). Critical weakness: if nonce k is reused across two signatures, x can be solved algebraically — this broke PlayStation 3's ECDSA (same k every time).")


elif page == "ECDSA":
    theory("ECDSA — Elliptic Curve Digital Signature Algorithm", "<b>Sign:</b> pick k, r=(k·G).x mod n, s=k⁻¹(H(M)+d·r) mod n → (r,s)<br><b>Verify:</b> w=s⁻¹, u₁=H(M)·w, u₂=r·w; check (u₁·G+u₂·Q).x mod n == r<br><b>Advantage over RSA:</b> much shorter keys for same security. P-256 (256-bit) ≈ RSA-3072.<br><b>Used in:</b> TLS 1.3, Bitcoin, Ethereum, SSH, JWT.")
    howto([
        "Select a curve (P-256 recommended).",
        "Click <b>Generate Keys</b>.",
        "Sign a message, verify, then try to verify a tampered message.",
    ])
    curve_name = st.selectbox("Curve", ["P-256", "P-384", "P-521"])
    if st.button("🔑  Generate ECDSA Keys", use_container_width=True):
        try:
            priv, pub = ECDSALib.generate_keys(curve_name)
            st.session_state["ecdsa2_priv"] = priv
            st.session_state["ecdsa2_pub"]  = pub
            st.session_state.pop("ecdsa2_sig", None)
            sizes = ECDSALib.compare_key_sizes()
            info = sizes.get(curve_name, {})
            st.success(f"✓ {curve_name} keys generated — {info.get('security_bits','?')}-bit security ≈ RSA-{info.get('equivalent_rsa','?')}")
        except Exception as e:
            st.error(str(e))

    if "ecdsa2_priv" in st.session_state:
        msg_ecdsa = st.text_input("Message to sign", value="ECDSA test message")
        c1, c2 = st.columns(2)
        if c1.button("✍️  Sign", use_container_width=True):
            try:
                sig = ECDSALib.sign(msg_ecdsa.encode(), st.session_state["ecdsa2_priv"])
                st.session_state["ecdsa2_sig"] = sig
                result("Signature (DER hex)", sig.hex()[:64] + "…")
                st.success("✓ Signed")
            except Exception as e:
                st.error(str(e))
        if c2.button("✓  Verify", use_container_width=True):
            sig = st.session_state.get("ecdsa2_sig")
            if sig:
                try:
                    ok = ECDSALib.verify(msg_ecdsa.encode(), sig, st.session_state["ecdsa2_pub"])
                    st.success("✓ VALID") if ok else st.error("✗ INVALID")
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Sign first.")

        if st.session_state.get("ecdsa2_sig"):
            section("Tamper Test")
            bad_ec = st.text_input("Tampered", value=msg_ecdsa + " [BAD]", key="ecdsa2_tamper")
            if st.button("🧪  Verify Tampered", use_container_width=True):
                try:
                    ok = ECDSALib.verify(bad_ec.encode(), st.session_state["ecdsa2_sig"], st.session_state["ecdsa2_pub"])
                    st.success("Valid!") if ok else st.error("✗ REJECTED ✓")
                except Exception as e:
                    st.error(str(e))

        section("Key Size Comparison (NIST SP 800-57)")
        sizes = ECDSALib.compare_key_sizes()
        rows = [{"Curve": c, "Security bits": v["security_bits"], "Equivalent RSA": f"RSA-{v['equivalent_rsa']}"} for c, v in sizes.items()]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        answer_note("TP5 Ex5.3 — Why ECDSA over RSA?", "P-256 provides 128-bit security with a 256-bit key. RSA needs 3072-bit keys for the same security. Shorter keys mean faster computation, smaller certificates, and less bandwidth — critical for IoT and TLS.")


# ═════════════════════════════════════════════════════════════════════════════
#  SECRET SHARING
# ═════════════════════════════════════════════════════════════════════════════

elif page == "Shamir (k,n)":
    theory("Shamir Secret Sharing", "A secret S is encoded as a polynomial f(x) of degree k−1 over a prime field, with f(0)=S. n shares (i, f(i)) are distributed. Any k shares reconstruct S via <b>Lagrange interpolation</b>. Any k−1 shares reveal <b>nothing</b> (information-theoretic security).")
    howto([
        "Enter a secret integer.",
        "Set threshold <b>k</b> (minimum shares needed) and <b>n</b> (total shares).",
        "Click <b>Split Secret</b> — n shares are generated.",
        "Select ≥ k shares and click <b>Reconstruct</b>. Try with fewer than k — it will fail.",
    ])
    secret = st.number_input("Secret S (integer)", min_value=0, value=12345, step=1)
    c1, c2 = st.columns(2)
    k = c1.slider("Threshold k (min shares to reconstruct)", 2, 10, 3)
    n = c2.slider("Total shares n", k, 20, 5)
    st.info(f"Any **{k}** of {n} shares can recover the secret. Any **{k-1}** or fewer reveal nothing.")
    if st.button("✂️  Split Secret", use_container_width=True):
        shares = ShamirSecretSharing.split(int(secret), k, n)
        st.session_state["shamir_shares"] = shares
        st.session_state["shamir_k"] = k
        st.session_state["shamir_secret"] = int(secret)
    if "shamir_shares" in st.session_state:
        shares = st.session_state["shamir_shares"]
        k_need = st.session_state["shamir_k"]
        sec = st.session_state["shamir_secret"]
        section("Generated shares")
        st.dataframe(pd.DataFrame([{"Share #": i+1, "x": x, "y (share value)": y} for i, (x,y) in enumerate(shares)]), hide_index=True, use_container_width=True)
        section("Reconstruct — select which shares to use")
        selected = st.multiselect(f"Select shares (need ≥ {k_need})", options=list(range(len(shares))), format_func=lambda i: f"Share {i+1}  (x={shares[i][0]})", default=list(range(k_need)))
        if st.button("🔧  Reconstruct Secret", use_container_width=True):
            chosen = [shares[i] for i in selected]
            if len(chosen) < k_need:
                st.error(f"Need at least {k_need} shares, got {len(chosen)}.")
            else:
                res = ShamirSecretSharing.reconstruct(chosen)
                if res == sec:
                    st.success(f"✓ Reconstructed secret: **{res}** — matches original ✓")
                    st.balloons()
                else:
                    st.error(f"Got {res}, expected {sec}")
        if k_need >= 2:
            section("Threshold demo — try with k−1 shares")
            if st.button(f"🧪  Reconstruct with only {k_need-1} shares (should fail)", use_container_width=True):
                chosen_bad = [shares[i] for i in range(k_need - 1)]
                res_bad = ShamirSecretSharing.reconstruct(chosen_bad)
                st.warning(f"Result with {k_need-1} shares: {res_bad} (≠ {sec}) — wrong, as expected")
                answer_note("Why it fails", f"With only {k_need-1} shares, the polynomial is under-determined. Lagrange interpolation at x=0 gives an incorrect value — information-theoretic security.")


# ═════════════════════════════════════════════════════════════════════════════
#  HOMOMORPHIC ENCRYPTION
# ═════════════════════════════════════════════════════════════════════════════

elif page == "Paillier":
    theory("Paillier Homomorphic Encryption", "<b>Enc(m₁) × Enc(m₂) mod n² = Enc(m₁ + m₂ mod n)</b><br>Allows a server to compute the sum of votes without ever decrypting individual votes — the foundation of <b>electronic voting</b>.<br>Security: semantic security based on the Decisional Composite Residuosity problem.")
    howto([
        "Click <b>Generate Keys</b>.",
        "Use <b>Homomorphic Addition</b> tab to encrypt two numbers and add them in ciphertext space.",
        "Use <b>E-Voting Demo</b> tab to simulate an election where individual votes stay encrypted.",
    ])
    if st.button("🔑  Generate Keys", use_container_width=True):
        with st.spinner("Generating Paillier keys…"):
            st.session_state["paillier"] = Paillier.generate_keys(128)

    if "paillier" in st.session_state:
        pk = st.session_state["paillier"]
        with st.expander("🔍  Key parameters"):
            st.code(f"n  = {pk['n']}\ng  = {pk['g']}\nλ  = {pk['lam']}\nμ  = {pk['mu']}")

        tab1, tab2 = st.tabs(["➕  Homomorphic Addition", "🗳️  E-Voting Demo"])

        with tab1:
            c1, c2 = st.columns(2)
            m1 = c1.number_input("Value A", min_value=0, value=15, step=1)
            m2 = c2.number_input("Value B", min_value=0, value=27, step=1)
            if st.button("➕  Encrypt Both & Add Homomorphically", use_container_width=True):
                ct1 = Paillier.encrypt(int(m1), pk["n"], pk["g"])
                ct2 = Paillier.encrypt(int(m2), pk["n"], pk["g"])
                c_sum = Paillier.add_encrypted(ct1, ct2, pk["n"])
                res = Paillier.decrypt(c_sum, pk["n"], pk["lam"], pk["mu"])
                section("Computation trace")
                st.code(f"Enc({m1})      = {hex(ct1)[:40]}…\nEnc({m2})      = {hex(ct2)[:40]}…\nEnc(A)×Enc(B) = {hex(c_sum)[:40]}…\nDecrypt(sum)  = {res}")
                if res == int(m1) + int(m2):
                    st.success(f"✓ {m1} + {m2} = {res}  (computed entirely on ciphertexts!)")
                    st.balloons()
                else:
                    st.error(f"Got {res}, expected {int(m1)+int(m2)}")

        with tab2:
            st.markdown("Simulate **5 voters** each submitting an encrypted vote (0 = No, 1 = Yes).")
            votes_input = []
            cols = st.columns(5)
            for i, col in enumerate(cols):
                v = col.selectbox(f"Voter {i+1}", [0, 1], key=f"vote_{i}")
                votes_input.append(v)
            if st.button("🗳️  Tally Votes Homomorphically", use_container_width=True):
                enc_votes = [Paillier.encrypt(v, pk["n"], pk["g"]) for v in votes_input]
                tally_enc = enc_votes[0]
                for ev in enc_votes[1:]:
                    tally_enc = Paillier.add_encrypted(tally_enc, ev, pk["n"])
                total = Paillier.decrypt(tally_enc, pk["n"], pk["lam"], pk["mu"])
                expected = sum(votes_input)
                section("Voting result")
                st.code(f"Votes cast (shown for demo only): {votes_input}\nHomomorphic tally (decrypted once): {total}\nExpected:                           {expected}")
                if total == expected:
                    st.success(f"✓ Correct tally: {total} YES out of {len(votes_input)} votes — individual votes never revealed!")
                answer_note("TP6 Ex6.4 — Why this matters", "In a real e-voting system, each voter encrypts their vote with the election authority's public key. All ciphertexts are multiplied homomorphically, then only the final sum is decrypted. No individual vote is ever exposed — yet the tally is verifiable.")


# ═════════════════════════════════════════════════════════════════════════════
#  IDENTIFICATION PROTOCOLS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "Schnorr ZKP":
    theory("Schnorr Zero-Knowledge Proof", "<b>Goal:</b> Alice proves she knows secret s (where h=gˢ mod p) to Bob, without revealing s.<br><b>Protocol:</b> (1) Alice commits: r←Zq, x=gʳ mod p → sends x. (2) Bob challenges: c←Zq → sends c. (3) Alice responds: y=r+sc mod q → sends y. (4) Bob verifies: gʸ ≡ x·hᶜ mod p.")
    howto([
        "Click <b>Setup</b> to generate parameters and Alice's secret.",
        "Follow steps 1–4 in order — each button simulates one protocol message.",
        "Step 4 reveals whether the verifier (Bob) accepts the proof.",
    ])
    if "schnorr" not in st.session_state:
        st.session_state["schnorr"] = {}
    state = st.session_state["schnorr"]
    current_step = state.get("step", 0)
    step_indicator(["Setup", "Alice commits", "Bob challenges", "Alice responds", "Bob verifies"], current_step)

    if st.button("⚙️  Setup — Generate Params & Alice's Secret", use_container_width=True):
        with st.spinner("Generating…"):
            params = Schnorr.generate_params(64)
            s, h = Schnorr.generate_keys(params["p"], params["q"], params["g"])
            state.clear()
            state.update(params=params, s=s, h=h, step=1)
            st.session_state["schnorr"] = state; st.rerun()

    if state.get("step", 0) >= 1:
        st.info(f"**Alice's secret s** = `{state['s']}`  _(private — never sent)_\n\n**Public key h** = gˢ mod p = `{state['h']}`")
        if st.button("Step 1 · Alice commits  →  x = gʳ mod p", use_container_width=True):
            r, x = Schnorr.prover_commit(state["params"]["p"], state["params"]["q"], state["params"]["g"])
            state.update(r=r, x=x, step=2); st.session_state["schnorr"] = state; st.rerun()

    if state.get("step", 0) >= 2:
        st.success(f"Alice → Bob:  **x** = `{state['x']}`")
        if st.button("Step 2 · Bob sends random challenge  →  c", use_container_width=True):
            c = Schnorr.generate_challenge(state["params"]["q"])
            state.update(c=c, step=3); st.session_state["schnorr"] = state; st.rerun()

    if state.get("step", 0) >= 3:
        st.success(f"Bob → Alice:  **c** = `{state['c']}`")
        if st.button("Step 3 · Alice responds  →  y = r + s·c mod q", use_container_width=True):
            y = Schnorr.prover_respond(state["r"], state["s"], state["c"], state["params"]["q"])
            state.update(y=y, step=4); st.session_state["schnorr"] = state; st.rerun()

    if state.get("step", 0) >= 4:
        st.success(f"Alice → Bob:  **y** = `{state['y']}`")
        if st.button("Step 4 · Bob verifies  →  gʸ ≡ x·hᶜ mod p ?", use_container_width=True):
            p_params = state["params"]
            ok = Schnorr.verify(p_params["g"], state["h"], state["x"], state["c"], state["y"], p_params["p"])
            if ok:
                st.success("✓ PROOF ACCEPTED — Bob is convinced Alice knows s, without learning s.")
            else:
                st.error("✗ Proof rejected")
            answer_note("Zero-knowledge property", "Bob only sees (x, c, y). He learns nothing about s because for any response y′, one can simulate a valid transcript without knowing s. The protocol is honest-verifier zero-knowledge.")
            state["step"] = 0; st.session_state["schnorr"] = state


elif page == "Feige-Fiat-Shamir":
    theory("Feige-Fiat-Shamir Identification", "<b>Setup:</b> n=p·q (RSA modulus), public v_i = s_i² mod n (or its inverse), private s_i.<br><b>Protocol:</b> (1) Prover picks r, sends x=r² mod n. (2) Verifier sends binary challenge b=[b₁…bk]. (3) Prover sends y=r·∏sᵢᵇⁱ mod n. (4) Verifier checks y²≡x·∏vᵢᵇⁱ mod n.<br>Security: based on hardness of computing square roots mod n (equivalent to factoring).")
    howto([
        "Click <b>Generate Parameters</b>.",
        "Follow steps 1–4 in order.",
        "Step 4 verifies whether identification succeeds.",
    ])
    K = 3
    if "ffs" not in st.session_state:
        st.session_state["ffs"] = {}
    state = st.session_state["ffs"]
    step_indicator(["Setup", "Prover commits", "Verifier challenges", "Prover responds", "Verifier checks"], state.get("step", 0))

    if st.button("⚙️  Generate FFS Parameters", use_container_width=True):
        with st.spinner("Generating RSA-like modulus…"):
            n = FeigeFiatShamir.generate_params(64)
            v, s = FeigeFiatShamir.generate_keys(n, K)
            state.clear()
            state.update(n=n, v=v, s=s, step=1); st.session_state["ffs"] = state; st.rerun()

    if state.get("step", 0) >= 1:
        st.info(f"**n** = {state['n']}")
        st.code("\n".join(f"s{i+1} = {state['s'][i]}   (private)   v{i+1} = {state['v'][i]}   (public = s{i+1}² mod n)" for i in range(K)))
        if st.button("Step 1 · Prover commits  →  x = r² mod n", use_container_width=True):
            r, x = FeigeFiatShamir.prover_commit(state["n"])
            state.update(r=r, x=x, step=2); st.session_state["ffs"] = state; st.rerun()

    if state.get("step", 0) >= 2:
        st.success(f"Prover → Verifier:  **x** = r² mod n = `{state['x']}`")
        if st.button("Step 2 · Verifier sends challenge bits  [b₁, b₂, b₃]", use_container_width=True):
            challenge = FeigeFiatShamir.generate_challenge(K)
            state.update(challenge=challenge, step=3); st.session_state["ffs"] = state; st.rerun()

    if state.get("step", 0) >= 3:
        st.success(f"Verifier → Prover:  challenge = `{state['challenge']}`")
        if st.button("Step 3 · Prover responds  →  y = r · ∏sᵢᵇⁱ mod n", use_container_width=True):
            y = FeigeFiatShamir.prover_respond(state["r"], state["s"], state["challenge"], state["n"])
            state.update(y=y, step=4); st.session_state["ffs"] = state; st.rerun()

    if state.get("step", 0) >= 4:
        st.success(f"Prover → Verifier:  **y** = `{state['y']}`")
        if st.button("Step 4 · Verifier checks  →  y² ≡ x · ∏vᵢᵇⁱ mod n ?", use_container_width=True):
            ok = FeigeFiatShamir.verify(state["x"], state["y"], state["v"], state["challenge"], state["n"])
            if ok:
                st.success("✓ Identification ACCEPTED")
            else:
                st.error("✗ Identification REJECTED")
            answer_note("Why it works", "y² = (r·∏sᵢ)² = r²·∏sᵢ² = x·∏vᵢ mod n (for bᵢ=1 positions). A cheating prover who doesn't know sᵢ cannot compute the correct y with high probability.")
            state["step"] = 0; st.session_state["ffs"] = state


# ═════════════════════════════════════════════════════════════════════════════
#  TP 6 — SECURE APPLICATIONS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "Secure TCP":
    theory("Secure TCP Socket Protocol (TP6 Ex6.1)", "Protocol: (1) Server sends RSA public key. (2) Client encrypts a random AES-256 session key with RSA, sends it. (3) All subsequent messages are encrypted with AES-CBC and authenticated with HMAC-SHA256.<br>Guarantees: <b>Confidentiality</b> (AES), <b>Authenticity</b> (HMAC), <b>Key exchange</b> (RSA).")
    howto([
        "Click <b>Run Demo</b> to start a local server, connect a client, send a message, and verify receipt.",
        "The demo runs a full TCP handshake on 127.0.0.1:19999.",
        "Inspect each phase of the protocol in the output.",
    ])

    theory("Protocol Flow", """
    <b>Step 1:</b> Server generates RSA-1024 key pair → sends (n, e) to client<br>
    <b>Step 2:</b> Client generates AES-256 session key → encrypts with RSA → sends to server<br>
    <b>Step 3:</b> Client sends message: IV(16B) + HMAC(32B) + AES-CBC(ciphertext)<br>
    <b>Step 4:</b> Server decrypts AES-CBC → verifies HMAC → outputs plaintext
    """)

    if st.button("▶️  Run Secure TCP Demo", use_container_width=True):
        with st.spinner("Starting server → connecting client → sending message…"):
            import time
            try:
                msgs = []
                server = SecureTCPServer(port=19999)
                server.start(on_message=lambda m: msgs.append(m))
                time.sleep(0.4)

                client = SecureTCPClient(port=19999)
                client.connect()
                test_msg = "Hello, secure TCP world! 🔐"
                client.send(test_msg)
                client.close()
                time.sleep(0.4)

                section("Protocol execution trace")
                st.code(f"""Phase 1: Server RSA-1024 key pair generated
Phase 2: Client generated AES-256 session key
         Session key sent encrypted with RSA public key
Phase 3: Client encrypted message with AES-CBC + HMAC-SHA256
         Sent: IV(16B) + HMAC(32B) + ciphertext
Phase 4: Server decrypted AES-CBC + verified HMAC
         Received: {msgs[0] if msgs else '(timeout — try again)'}""")
                if msgs:
                    st.success(f"✓ Secure message received: '{msgs[0]}'")
                    if msgs[0] == test_msg:
                        st.success("✓ Message integrity verified — exact match!")
                else:
                    st.warning("No messages received. The demo uses local sockets — try running again.")
            except Exception as e:
                st.error(f"TCP demo error: {e}")

    section("Manual Protocol Inspection")
    theory("What each layer does", """
    <b>RSA layer:</b> Key exchange only — never used to encrypt data directly (too slow, size-limited).<br>
    <b>AES-CBC layer:</b> Fast symmetric encryption of the actual payload with the session key.<br>
    <b>HMAC layer:</b> Ensures no byte of the ciphertext was modified in transit.<br>
    <b>Combined:</b> This is essentially TLS 1.2's handshake + record layer in simplified form.
    """)

    if st.button("🔍  Simulate Protocol Steps Manually", use_container_width=True):
        with st.spinner("Simulating…"):
            # Step 1: Server RSA keys
            rsa_keys = RSA.generate_keys(1024)
            st.write("**Step 1 — Server RSA public key:**")
            st.code(f"n = {hex(rsa_keys['n'])[:40]}…\ne = {rsa_keys['e']}")

            # Step 2: Client generates session key, encrypts it
            session_key_hex = AES.generate_key(256)
            session_key_bytes = bytes.fromhex(session_key_hex)
            enc_session_key = RSA.encrypt_bytes(session_key_bytes, rsa_keys['e'], rsa_keys['n'])
            st.write("**Step 2 — Client encrypts AES-256 session key with RSA:**")
            st.code(f"Session key (hex) = {session_key_hex}\nEncrypted with RSA: {enc_session_key.hex()[:40]}…")

            # Step 3: Server decrypts session key
            dec_key = RSA.decrypt_bytes(enc_session_key, rsa_keys['d'], rsa_keys['n'])
            st.write("**Step 3 — Server decrypts session key:**")
            match = dec_key.hex() == session_key_hex
            st.code(f"Decrypted key: {dec_key.hex()}\nMatch: {match}")

            # Step 4: Encrypted + authenticated message
            msg = b"Hello, secure world!"
            iv = AES.generate_iv()
            mac = HMAC.compute(session_key_bytes, msg)
            ct = AES.encrypt_cbc(msg, session_key_hex, iv)
            payload = iv + bytes.fromhex(mac) + ct
            st.write("**Step 4 — Client sends AES-CBC + HMAC message:**")
            st.code(f"IV:         {iv.hex()}\nHMAC:       {mac[:32]}…\nCiphertext: {ct.hex()[:40]}…\nTotal payload: {len(payload)} bytes")

            # Step 5: Server verifies and decrypts
            recv_iv = payload[:16]
            recv_mac = payload[16:48].hex()
            recv_ct = payload[48:]
            plaintext = AES.decrypt_cbc(recv_ct, session_key_hex, recv_iv)
            mac_valid = HMAC.verify(session_key_bytes, plaintext, recv_mac)
            st.write("**Step 5 — Server verifies HMAC and decrypts:**")
            st.code(f"HMAC valid: {mac_valid}\nDecrypted:  {plaintext.decode(errors='replace')}")
            if mac_valid and plaintext == msg:
                st.success("✓ Full protocol execution successful!")


elif page == "Secure UDP Chat":
    theory("Secure UDP Chat (TP6 Ex6.3)", "Each message is encrypted with <b>AES-CTR</b> using a fresh nonce (avoids nonce-reuse vulnerability). Authenticated with <b>HMAC-SHA256</b> over the ciphertext.<br>Packet format: nonce(8B) + HMAC(64 hex chars = 32B) + ciphertext<br>UDP is connectionless — each packet must be self-authenticating.")
    howto([
        "Generate a shared session key (both parties would share this out-of-band or via DH).",
        "Type a message and click <b>Pack Message</b> to encrypt + authenticate it.",
        "Click <b>Unpack Message</b> to verify HMAC and decrypt.",
        "Try <b>Tamper Test</b> — modify the packet and watch HMAC fail.",
    ])

    if "udp_key" not in st.session_state:
        st.session_state["udp_key"] = AES.generate_key(256)

    k_col, k_btn = st.columns([3, 1])
    udp_key_hex = k_col.text_input("Shared session key (hex)", value=st.session_state["udp_key"])
    if k_btn.button("🎲  New Key", use_container_width=True):
        st.session_state["udp_key"] = AES.generate_key(256)
        st.rerun()

    chat = SecureUDPChat(udp_key_hex)

    message = st.text_input("Message to send", value="Bonjour via UDP sécurisé!")
    c1, c2 = st.columns(2)
    if c1.button("📦  Pack Message (Encrypt + Auth)", use_container_width=True) and message:
        try:
            packet = chat.pack_message(message)
            st.session_state["udp_packet"] = packet
            section("UDP Packet Structure")
            nonce = packet[:8]
            mac_part = packet[8:72]
            ct = packet[72:]
            st.code(f"Nonce (8B):   {nonce.hex()}\nHMAC (32B):   {mac_part.decode()}\nCiphertext:   {ct.hex()}\nTotal size:   {len(packet)} bytes")
            st.success(f"✓ Packet ready for transmission ({len(packet)} bytes)")
        except Exception as e:
            st.error(str(e))

    if c2.button("📬  Unpack Message (Verify + Decrypt)", use_container_width=True):
        packet = st.session_state.get("udp_packet")
        if packet:
            try:
                recovered = chat.unpack_message(packet)
                result("Decrypted message", recovered)
                st.success("✓ HMAC verified — message authentic and unmodified!")
            except ValueError as e:
                st.error(f"✗ {e}")
            except Exception as e:
                st.error(str(e))
        else:
            st.warning("Pack a message first.")

    if st.session_state.get("udp_packet"):
        section("Tamper Test — modify the packet")
        packet = st.session_state["udp_packet"]
        st.info(f"Current packet hex: {packet.hex()[:60]}…")
        if st.button("🔨  Flip 1 bit in ciphertext", use_container_width=True):
            tampered = bytearray(packet)
            tampered[72] ^= 0x01  # Flip a bit in the ciphertext
            try:
                chat.unpack_message(bytes(tampered))
                st.error("Verification passed — unexpected!")
            except ValueError as e:
                st.error(f"✗ {e} — HMAC caught the tampering! ✓")
            answer_note("Why this matters", "HMAC is computed over the ciphertext. Any modification to any byte of the ciphertext (even 1 bit) produces a completely different HMAC — mismatch detected. This prevents both accidental corruption and malicious modification.")


elif page == "PGP Hybrid":
    theory("PGP-Style Hybrid Encryption (TP6)", "<b>Step 1:</b> Generate random AES-256 session key.<br><b>Step 2:</b> Encrypt message with AES-CBC using session key.<br><b>Step 3:</b> Encrypt session key with recipient's RSA public key.<br><b>Step 4:</b> Sender signs H(ciphertext) with their RSA private key.<br>Guarantees: <b>Confidentiality</b> (AES), <b>Key exchange</b> (RSA), <b>Authenticity + Non-repudiation</b> (RSA signature).")
    howto([
        "Click <b>Generate Keys</b> to create RSA keypairs for Alice (sender) and Bob (recipient).",
        "Type a message and click <b>Encrypt + Sign</b>.",
        "Click <b>Decrypt + Verify</b> to recover the message and check the signature.",
        "Try modifying the ciphertext — the signature check will fail.",
    ])

    if st.button("🔑  Generate RSA Keys for Alice & Bob", use_container_width=True):
        with st.spinner("Generating RSA-512 keypairs for Alice and Bob…"):
            st.session_state["pgp_alice"] = RSA.generate_keys(512)
            st.session_state["pgp_bob"]   = RSA.generate_keys(512)
            st.session_state.pop("pgp_pkg", None)
        st.success("✓ Keys generated for Alice (sender) and Bob (recipient)")

    if "pgp_alice" in st.session_state and "pgp_bob" in st.session_state:
        alice = st.session_state["pgp_alice"]
        bob   = st.session_state["pgp_bob"]

        with st.expander("🔍  Key summary"):
            col1, col2 = st.columns(2)
            with col1:
                _html('<div class="party"><div class="role">Sender</div><h4>👩 Alice</h4></div>')
                st.code(f"Public key n = {hex(alice['n'])[:30]}…\ne = {alice['e']}")
            with col2:
                _html('<div class="party"><div class="role">Recipient</div><h4>👨 Bob</h4></div>')
                st.code(f"Public key n = {hex(bob['n'])[:30]}…\ne = {bob['e']}")

        msg_pgp = st.text_area("Message from Alice to Bob", value="PGP message: Eyes only for Bob!", height=100)

        c1, c2 = st.columns(2)
        if c1.button("🔒✍️  Encrypt + Sign (Alice → Bob)", use_container_width=True) and msg_pgp:
            try:
                pkg = PGPHybrid.encrypt_and_sign(msg_pgp.encode(), bob, alice)
                st.session_state["pgp_pkg"] = pkg
                section("Encrypted package contents")
                st.code(f"Encrypted AES key (RSA):  {pkg['enc_key'].hex()[:40]}…\nIV (AES-CBC):             {pkg['iv'].hex()}\nCiphertext:               {pkg['ciphertext'].hex()[:40]}…\nRSA Signature:            {hex(pkg['signature'])[:40]}…")
                st.success("✓ Message encrypted with AES-CBC + session key wrapped with Bob's RSA public key + signed by Alice")
            except Exception as e:
                st.error(str(e))

        if c2.button("🔓✓  Decrypt + Verify (Bob receives)", use_container_width=True):
            pkg = st.session_state.get("pgp_pkg")
            if pkg:
                try:
                    recovered, sig_valid = PGPHybrid.decrypt_and_verify(pkg, bob, alice)
                    result("Recovered message", recovered.decode(errors='replace'))
                    if sig_valid:
                        st.success("✓ Signature VALID — message is from Alice, unmodified")
                    else:
                        st.error("✗ Signature INVALID — message tampered or not from Alice!")
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Encrypt something first.")

        answer_note("PGP protocol properties", """
        <b>Confidentiality:</b> Only Bob can decrypt (only Bob has the private key to unwrap the AES key).<br>
        <b>Authenticity:</b> Only Alice could have signed (only Alice has her private signing key).<br>
        <b>Integrity:</b> The signature covers H(ciphertext) — any modification breaks the signature.<br>
        <b>Non-repudiation:</b> Alice cannot later deny sending the message — her signature is unforgeable.
        """)


# ─────────────────────────────────────────────────────────────────────────────
# TP6 — LIVE SECURE CHAT  (real bidirectional network chat)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Live Secure Chat":

    import socket as _sock, struct as _struct, json as _json

    # ── helpers (inline, no import issues in Streamlit) ──────────────────────
    def _exact(s, n):
        buf = b''
        while len(buf) < n:
            c = s.recv(n - len(buf))
            if not c: return b''
            buf += c
        return buf

    def _send_pkt(s, data: bytes):
        s.sendall(_struct.pack('>I', len(data)) + data)

    def _recv_pkt(s) -> bytes:
        h = _exact(s, 4)
        return _exact(s, _struct.unpack('>I', h)[0]) if h else b''

    def _pack(text: str, key_hex: str) -> bytes:
        import hashlib, hmac as _h
        data = text.encode()
        iv   = AES.generate_iv()
        mac  = _h.new(bytes.fromhex(key_hex), data, hashlib.sha256).hexdigest()
        ct   = AES.encrypt_cbc(data, key_hex, iv)
        return iv + mac.encode() + ct

    def _unpack(payload: bytes, key_hex: str):
        import hashlib, hmac as _h
        iv  = payload[:16]
        mac = payload[16:80].decode()
        ct  = payload[80:]
        pt  = AES.decrypt_cbc(ct, key_hex, iv)
        exp = _h.new(bytes.fromhex(key_hex), pt, hashlib.sha256).hexdigest()
        if not _h.compare_digest(mac, exp):
            raise ValueError("HMAC FAILED")
        return pt.decode(), iv.hex(), mac, ct.hex()

    def _do_handshake(ip, port, key_hex, name):
        """Connect, exchange RSA/AES keys, send name, wait for HANDSHAKE_OK."""
        s = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
        s.settimeout(8)
        s.connect((ip, int(port)))
        # receive RSA public key
        pub  = _recv_pkt(s)
        nh, eh = pub.decode().split('|')
        n, e = int(nh, 16), int(eh, 16)
        # send AES session key encrypted with RSA
        kb  = bytes.fromhex(key_hex)
        enc = RSA.encrypt_bytes(kb, e, n)
        _send_pkt(s, enc)
        # send our name
        _send_pkt(s, name.encode())
        # receive HANDSHAKE_OK
        ack_raw = _recv_pkt(s)
        ack, _, _, _ = _unpack(ack_raw, key_hex)
        if ack != "HANDSHAKE_OK":
            s.close()
            raise ValueError(f"Unexpected ACK: {ack}")
        return s   # keep socket open!

    def _poll_http(ip, http_port, since):
        """Poll HTTP API for new messages (non-blocking)."""
        try:
            import urllib.request
            url = f"http://{ip}:{http_port}/messages?since={since}"
            with urllib.request.urlopen(url, timeout=3) as r:
                return _json.loads(r.read())
        except Exception:
            return []

    # ── init session state ────────────────────────────────────────────────────
    for _k, _v in [
        ("lsc_connected", False), ("lsc_key", None), ("lsc_name", "PC"),
        ("lsc_ip", "127.0.0.1"), ("lsc_port", 9999),
        ("lsc_sock", None), ("lsc_log", []), ("lsc_last_id", 0),
    ]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    # ── page header ───────────────────────────────────────────────────────────
    theory("Live Secure Chat — TP6 Ex6.1",
        """Real bidirectional encrypted chat between two devices on the same Wi-Fi.<br>
        <b>Protocol:</b> RSA-1024 key exchange → AES-256-CBC + HMAC-SHA256 per message.<br>
        <b>Broadcast:</b> Server forwards every message to all other connected clients,
        re-encrypted with <i>their</i> session key. No plaintext ever leaves a device.
        """)

    howto([
        "Run <code>python chat_server.py</code> on your PC (terminal).",
        "Find your PC local IP: <b>Windows</b> → <code>ipconfig</code> | <b>Linux</b> → <code>hostname -I</code>",
        "Open CryptoLab on <b>both devices</b> (PC browser + phone browser at <code>http://&lt;PC-IP&gt;:8501</code>).",
        "Enter the same server IP on both devices → give each device a name → Connect → Chat!",
    ])

    # ── setup box ─────────────────────────────────────────────────────────────
    _html("""<div style="background:linear-gradient(135deg,rgba(0,255,156,.07),rgba(0,180,255,.04));
        border:1px solid rgba(0,255,156,.3);border-radius:14px;padding:16px 20px;margin:0 0 18px;
        font-size:13px;color:#D6DEEC;line-height:1.9;">
      <b style="color:#00FF9C;font-size:13.5px;">⚙️ One-time setup on your PC</b><br>
      <code style="background:rgba(0,0,0,.4);border-radius:6px;padding:2px 8px;color:#00FF9C;">
        python chat_server.py</code>
      &nbsp; then open this page on your <b>phone</b> at
      <code style="color:#06B6D4">http://&lt;your-PC-IP&gt;:8501</code><br>
      <span style="color:#9CA3B8;font-size:12px;">
        ⚠ Both devices must be on the <b style="color:#E6EDF3">same Wi-Fi</b>.
        Server uses TCP port <b>9999</b> + HTTP port <b>10000</b>.
      </span></div>""")

    # ── connection form ───────────────────────────────────────────────────────
    section("Connection")
    ca, cb, cc = st.columns([2, 1, 1])
    ip_in   = ca.text_input("Server IP", value=st.session_state["lsc_ip"],
                             placeholder="e.g. 192.168.1.42")
    pt_in   = cb.number_input("TCP Port", 1024, 65535,
                               value=int(st.session_state["lsc_port"]))
    nm_in   = cc.text_input("Your name", value=st.session_state["lsc_name"],
                             placeholder="PC  /  Phone  /  Alice…")

    connected = st.session_state["lsc_connected"]
    ba, bb = st.columns(2)
    do_connect    = ba.button("🔌  Connect", use_container_width=True, disabled=connected)
    do_disconnect = bb.button("⛔  Disconnect", use_container_width=True, disabled=not connected)

    if do_disconnect:
        try:
            old_sock = st.session_state.get("lsc_sock")
            if old_sock: old_sock.close()
        except Exception: pass
        for k in ["lsc_connected","lsc_key","lsc_sock","lsc_log","lsc_last_id"]:
            st.session_state[k] = False if k=="lsc_connected" else (None if k in ("lsc_key","lsc_sock") else ([] if k=="lsc_log" else 0))
        st.rerun()

    if do_connect:
        try:
            st.session_state["lsc_ip"]   = ip_in
            st.session_state["lsc_port"] = pt_in
            st.session_state["lsc_name"] = nm_in or "user"
            key_hex = AES.generate_key(256)
            with st.spinner(f"Connecting to {ip_in}:{pt_in} …"):
                sock = _do_handshake(ip_in, pt_in, key_hex, nm_in or "user")
            st.session_state["lsc_key"]       = key_hex
            st.session_state["lsc_sock"]      = sock
            st.session_state["lsc_connected"] = True
            st.session_state["lsc_log"] = [{
                "from": "System", "text": f"✓ Connected as '{nm_in}' — AES-256 channel ready.",
                "ts": "", "iv": "", "ct": "", "mine": False, "system": True
            }]
            st.rerun()
        except Exception as ex:
            st.error(f"Connection failed: {ex} — Make sure chat_server.py is running on {ip_in}.")

    # ── status badge ──────────────────────────────────────────────────────────
    connected = st.session_state["lsc_connected"]
    key_hex   = st.session_state.get("lsc_key")

    if connected and key_hex:
        _html(f"""<div style="display:flex;align-items:center;gap:10px;
            background:rgba(0,255,156,.06);border:1px solid rgba(0,255,156,.3);
            border-radius:10px;padding:10px 16px;margin:10px 0;font-size:13px;">
          <div style="width:9px;height:9px;border-radius:50%;background:#00FF9C;
                      box-shadow:0 0 0 4px rgba(0,255,156,.2);flex-shrink:0"></div>
          <div><b style="color:#00FF9C">Connected</b> as
            <b style="color:#E6EDF3">{st.session_state["lsc_name"]}</b> —
            session key: <code style="color:#9CA3B8">{key_hex[:16]}…</code>
          </div></div>""")
    else:
        _html("""<div style="display:flex;align-items:center;gap:10px;
            background:rgba(248,113,113,.06);border:1px solid rgba(248,113,113,.3);
            border-radius:10px;padding:10px 16px;margin:10px 0;font-size:13px;">
          <div style="width:9px;height:9px;border-radius:50%;background:#F87171;flex-shrink:0"></div>
          <div><b style="color:#F87171">Not connected</b> —
            start <code>chat_server.py</code> then click Connect.</div></div>""")

    # ── send + receive panel ──────────────────────────────────────────────────
    if connected and key_hex:

        # ── Poll for new messages from server HTTP API ─────────────────────
        http_port    = int(st.session_state["lsc_port"]) + 1
        since_id     = st.session_state["lsc_last_id"]
        new_messages = _poll_http(st.session_state["lsc_ip"], http_port, since_id)
        my_name      = st.session_state["lsc_name"]

        for msg in new_messages:
            if msg["from"] == "SERVER":
                continue  # skip internal join/leave notices shown inline
            # Only add messages from OTHERS (our own are logged on send)
            if msg["from"] != my_name:
                st.session_state["lsc_log"].append({
                    "from":   msg["from"],
                    "text":   msg["text"],
                    "ts":     msg.get("ts",""),
                    "iv":     msg.get("iv",""),
                    "ct":     msg.get("ct",""),
                    "mine":   False,
                    "system": False,
                })
            if msg["id"] >= st.session_state["lsc_last_id"]:
                st.session_state["lsc_last_id"] = msg["id"] + 1

        # ── Send form ──────────────────────────────────────────────────────
        section("Send Message")
        msg_text = st.text_input("Message", placeholder="Type and press Enter or click Send…",
                                 key="lsc_msg")
        s1, s2, s3 = st.columns([3, 1, 1])
        do_send    = s1.button("📤  Encrypt & Send", use_container_width=True,
                               disabled=not msg_text)
        do_refresh = s2.button("🔄  Refresh", use_container_width=True)
        do_clear   = s3.button("🗑️  Clear", use_container_width=True)

        if do_clear:
            st.session_state["lsc_log"] = []
            st.rerun()

        if do_refresh:
            st.rerun()

        if do_send and msg_text:
            try:
                payload = _pack(msg_text, key_hex)
                iv_hex  = payload[:16].hex()
                mac_hex = payload[16:80].decode()
                ct_hex  = payload[80:].hex()

                sock = st.session_state.get("lsc_sock")
                if sock is None:
                    st.error("Socket lost — please Disconnect and reconnect.")
                else:
                    with st.spinner("Sending…"):
                        _send_pkt(sock, payload)
                        # receive ACK from server
                        ack_raw = _recv_pkt(sock)
                        ack_txt = "(no ack)"
                        if ack_raw:
                            try:
                                ack_txt, _, _, _ = _unpack(ack_raw, key_hex)
                            except Exception:
                                pass

                    st.session_state["lsc_log"].append({
                        "from":   f"📤 {my_name} (you)",
                        "text":   msg_text,
                        "ts":     "",
                        "iv":     iv_hex,
                        "ct":     ct_hex,
                        "mac":    mac_hex,
                        "ack":    ack_txt,
                        "mine":   True,
                        "system": False,
                    })
                    st.rerun()
            except Exception as ex:
                st.error(f"Send error: {ex}. Try Disconnect → Reconnect.")

        # ── Chat log ───────────────────────────────────────────────────────
        section("Chat — Live")
        log = st.session_state["lsc_log"]

        if not log:
            st.info("No messages yet — send something or wait for the other device to write.")
        else:
            for entry in reversed(log):
                is_mine  = entry.get("mine", False)
                is_sys   = entry.get("system", False)
                sender   = entry["from"]
                text     = entry["text"]
                iv_h     = entry.get("iv","")
                ct_h     = entry.get("ct","")
                mac_h    = entry.get("mac","")
                ack      = entry.get("ack","")
                ts       = entry.get("ts","")

                if is_sys:
                    _html(f"""<div style="text-align:center;color:#6B7390;
                        font-size:12px;padding:6px 0;margin:4px 0;">
                        ℹ️ {text}</div>""")
                    continue

                align  = "flex-end"   if is_mine else "flex-start"
                bubble = "rgba(139,92,246,0.18)" if is_mine else "rgba(6,182,212,0.10)"
                border = "rgba(139,92,246,0.4)"  if is_mine else "rgba(6,182,212,0.3)"
                label  = "You" if is_mine else sender
                ts_str = f" · {ts}" if ts else ""

                # Show ciphertext (what actually went over the network)
                ct_preview = (ct_h[:48] + "…") if len(ct_h) > 48 else ct_h
                iv_preview = iv_h[:32] if iv_h else "—"
                mac_preview = (mac_h[:32] + "…") if mac_h else "—"

                _html(f"""
                <div style="display:flex;justify-content:{align};margin:0 0 14px;">
                  <div style="max-width:82%;min-width:220px;
                      background:{bubble};border:1px solid {border};
                      border-radius:14px;padding:12px 16px;">

                    <div style="display:flex;justify-content:space-between;
                        margin-bottom:8px;align-items:baseline;">
                      <span style="font-weight:700;color:#E6EDF3;font-size:13px;">{label}</span>
                      <span style="font-size:10.5px;color:#6B7390;">{ts_str}</span>
                    </div>

                    <!-- Plaintext -->
                    <div style="font-size:16px;color:#FFFFFF;
                        font-weight:500;margin-bottom:10px;
                        padding:8px 12px;background:rgba(255,255,255,0.05);
                        border-radius:8px;">{text}</div>

                    <!-- Ciphertext wire data -->
                    <div style="font-size:10.5px;color:#6B7390;margin-bottom:3px;
                        text-transform:uppercase;letter-spacing:.08em;">
                      🔒 Encrypted (what travels on network)</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:10.5px;
                        color:#F472B6;background:rgba(0,0,0,.35);border-radius:6px;
                        padding:6px 10px;word-break:break-all;margin-bottom:6px;">
                      {ct_preview if ct_preview else "—"}</div>

                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;
                        font-size:10px;color:#6B7390;">
                      <div>IV: <span style="color:#06B6D4;font-family:monospace">
                        {iv_preview}</span></div>
                      <div>HMAC: <span style="color:#8B5CF6;font-family:monospace">
                        {mac_preview}</span></div>
                    </div>
                    {f'<div style="font-size:10.5px;color:#34D399;margin-top:6px;">✓ {ack}</div>' if ack else ""}
                  </div>
                </div>""")

        # ── auto-refresh hint ──────────────────────────────────────────────
        _html("""<div style="text-align:center;color:#6B7390;font-size:12px;
            padding:10px 0;">
            Click <b style="color:#E6EDF3">🔄 Refresh</b> to load new messages
            from the other device.</div>""")

        answer_note("How messages are delivered", """
        <b>Send:</b> Your message is encrypted AES-256-CBC with a fresh IV → HMAC-SHA256 →
        sent over TCP to the server.<br>
        <b>Broadcast:</b> The server decrypts it, logs it, then <i>re-encrypts</i> it with
        each recipient's own session key and pushes it over their persistent TCP connection.<br>
        <b>Receive:</b> The Streamlit app polls the server's HTTP API (port 10000) for new
        messages and shows them with their ciphertext so you can see the encrypted form.<br>
        <b>Zero plaintext on the wire:</b> every byte that crosses the network is ciphertext.
        """)
