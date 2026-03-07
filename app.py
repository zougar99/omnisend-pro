"""
OmniSend Pro v6.0
Professional Multi-Channel Bulk Messaging Platform
Email + WhatsApp + SMS + Telegram
"""

APP_VERSION = "6.0"
UPDATE_URL = "https://raw.githubusercontent.com/zougar99/omnisend-pro/main/version.json"

import os, re, csv, json, time, random, smtplib, socket, threading, uuid, base64, webbrowser, tempfile, ssl
import sys, subprocess, shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import URLError

try:
    import socks; HAS_SOCKS = True
except ImportError: HAS_SOCKS = False
try:
    import dns.resolver; HAS_DNS = True
except ImportError: HAS_DNS = False
try:
    import requests; HAS_REQ = True
except ImportError: HAS_REQ = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    HAS_SELENIUM = True
except ImportError: HAS_SELENIUM = False
try:
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_WDM = True
except ImportError: HAS_WDM = False
try:
    from telethon.sync import TelegramClient as _TelethonClient
    from telethon.errors import SessionPasswordNeededError as _TelethonPwdErr
    HAS_TELETHON = True
except ImportError: HAS_TELETHON = False

import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
TPL_DIRS = {}
for _ch in ("email","whatsapp","sms","telegram"):
    TPL_DIRS[_ch] = os.path.join(DATA_DIR, "templates", _ch)
    os.makedirs(TPL_DIRS[_ch], exist_ok=True)

# ═══════════════════════════════════════════════════════════════
#  THEME — OmniSend Pro Premium Dark
# ═══════════════════════════════════════════════════════════════
THEMES = {
    "Dark Blue (Default)": {
        "bg":"#0f1219","sidebar":"#131720","sidebar_sel":"#1e2433","sidebar_hover":"#1a1f2d",
        "surface":"#171c27","surface2":"#1a1f2a",
        "card":"#1c2231","card_h":"#232a3c","card_sel":"#283148",
        "input_bg":"#141924","input_bd":"#2c3448","input_fc":"#3b82f6",
        "border":"#262d3e","border_l":"#333d54","border_glow":"#3b82f620",
        "t1":"#e8ecf4","t2":"#8e99b0","t3":"#586580","t4":"#3c4762",
        "accent":"#3b82f6","accent_h":"#2563eb","accent_s":"#1a2d54","accent_l":"#60a5fa",
    },
    "Midnight Purple": {
        "bg":"#0e0b1a","sidebar":"#12101f","sidebar_sel":"#201d35","sidebar_hover":"#1a1730",
        "surface":"#161329","surface2":"#1a172c",
        "card":"#1e1a33","card_h":"#28234a","card_sel":"#302a55",
        "input_bg":"#120f22","input_bd":"#2f2850","input_fc":"#8b5cf6",
        "border":"#2a2545","border_l":"#3d3660","border_glow":"#8b5cf620",
        "t1":"#ece8f8","t2":"#9e94c0","t3":"#6a5e90","t4":"#483c6a",
        "accent":"#8b5cf6","accent_h":"#7c3aed","accent_s":"#251550","accent_l":"#a78bfa",
    },
    "Emerald Dark": {
        "bg":"#0a1410","sidebar":"#0e1a14","sidebar_sel":"#1a2e22","sidebar_hover":"#152618",
        "surface":"#122018","surface2":"#15241c",
        "card":"#1a2e22","card_h":"#213a2c","card_sel":"#284838",
        "input_bg":"#0e1a14","input_bd":"#2a4035","input_fc":"#22c55e",
        "border":"#243830","border_l":"#305040","border_glow":"#22c55e20",
        "t1":"#e4f4ea","t2":"#8cb8a0","t3":"#5a8870","t4":"#3c6050",
        "accent":"#22c55e","accent_h":"#16a34a","accent_s":"#0f2a1a","accent_l":"#4ade80",
    },
    "Crimson Night": {
        "bg":"#140a0e","sidebar":"#1a0e14","sidebar_sel":"#301822","sidebar_hover":"#261018",
        "surface":"#1e1218","surface2":"#22151c",
        "card":"#2c1822","card_h":"#3a2030","card_sel":"#482838",
        "input_bg":"#1a0e14","input_bd":"#402a35","input_fc":"#ef4444",
        "border":"#382030","border_l":"#503040","border_glow":"#ef444420",
        "t1":"#f4e4e8","t2":"#b88c9e","t3":"#885a70","t4":"#603c50",
        "accent":"#ef4444","accent_h":"#dc2626","accent_s":"#2c1418","accent_l":"#f87171",
    },
    "Ocean Cyan": {
        "bg":"#0a1218","sidebar":"#0e161e","sidebar_sel":"#182a36","sidebar_hover":"#14222c",
        "surface":"#121e28","surface2":"#15222e",
        "card":"#1a2a38","card_h":"#213648","card_sel":"#284458",
        "input_bg":"#0e1a24","input_bd":"#2a3e50","input_fc":"#06b6d4",
        "border":"#243846","border_l":"#305060","border_glow":"#06b6d420",
        "t1":"#e4f0f8","t2":"#8cb4c8","t3":"#5a8898","t4":"#3c6070",
        "accent":"#06b6d4","accent_h":"#0891b2","accent_s":"#0e2430","accent_l":"#22d3ee",
    },
    "Sunset Orange": {
        "bg":"#161008","sidebar":"#1c1410","sidebar_sel":"#332218","sidebar_hover":"#2a1c12",
        "surface":"#221a12","surface2":"#281e14",
        "card":"#302218","card_h":"#402e20","card_sel":"#503c28",
        "input_bg":"#1c1610","input_bd":"#483620","input_fc":"#f59e0b",
        "border":"#3e3020","border_l":"#584430","border_glow":"#f59e0b20",
        "t1":"#f8f0e4","t2":"#c8a880","t3":"#988060","t4":"#6a5840",
        "accent":"#f59e0b","accent_h":"#d97706","accent_s":"#2a1f0a","accent_l":"#fbbf24",
    },
    "Rose Pink": {
        "bg":"#140a12","sidebar":"#1a0e18","sidebar_sel":"#301828","sidebar_hover":"#261020",
        "surface":"#1e1220","surface2":"#221524",
        "card":"#2c1828","card_h":"#3a2038","card_sel":"#482848",
        "input_bg":"#1a0e18","input_bd":"#402a40","input_fc":"#ec4899",
        "border":"#382038","border_l":"#503048","border_glow":"#ec489920",
        "t1":"#f4e4f0","t2":"#b88cb0","t3":"#885a80","t4":"#603c58",
        "accent":"#ec4899","accent_h":"#db2777","accent_s":"#2a0a20","accent_l":"#f472b6",
    },
    "Slate Gray": {
        "bg":"#111214","sidebar":"#161718","sidebar_sel":"#252728","sidebar_hover":"#1e2022",
        "surface":"#1a1c1e","surface2":"#1e2022",
        "card":"#222426","card_h":"#2c2e30","card_sel":"#363838",
        "input_bg":"#181a1c","input_bd":"#363838","input_fc":"#94a3b8",
        "border":"#303234","border_l":"#40444a","border_glow":"#94a3b820",
        "t1":"#e8eaee","t2":"#94a3b8","t3":"#64748b","t4":"#475569",
        "accent":"#94a3b8","accent_h":"#64748b","accent_s":"#1e293b","accent_l":"#cbd5e1",
    },
    "Hacker Green": {
        "bg":"#050a05","sidebar":"#081008","sidebar_sel":"#102010","sidebar_hover":"#0c180c",
        "surface":"#0a140a","surface2":"#0c180c",
        "card":"#102010","card_h":"#182818","card_sel":"#203420",
        "input_bg":"#081008","input_bd":"#1c3018","input_fc":"#00ff41",
        "border":"#162816","border_l":"#203620","border_glow":"#00ff4120",
        "t1":"#c0ffc0","t2":"#60c060","t3":"#408040","t4":"#306030",
        "accent":"#00ff41","accent_h":"#00cc33","accent_s":"#002200","accent_l":"#40ff70",
    },
}

_shared_colors = {
    "brand1":"#3b82f6","brand2":"#8b5cf6","brand3":"#ec4899",
    "purple":"#8b5cf6","purple_h":"#7c3aed","purple_s":"#251550",
    "green":"#22c55e","green_h":"#16a34a","green_bg":"#0f2a1a","green_l":"#4ade80",
    "red":"#ef4444","red_h":"#dc2626","red_bg":"#2c1418","red_l":"#f87171",
    "orange":"#f59e0b","orange_h":"#d97706","orange_bg":"#2a1f0a","orange_l":"#fbbf24",
    "cyan":"#06b6d4","cyan_h":"#0891b2","cyan_s":"#0e2430",
    "pink":"#ec4899","pink_h":"#db2777",
    "gold":"#fbbf24",
    "wa_green":"#25D366","wa_green_h":"#1da851","wa_bg":"#0f2a1a",
    "sms_blue":"#60a5fa","sms_blue_h":"#3b82f6","sms_bg":"#131e36",
    "tg_blue":"#0088cc","tg_blue_h":"#006daa","tg_bg":"#0d1f33",
}

def _load_theme():
    cfg = os.path.join(DATA_DIR, "app_settings.json")
    name = "Dark Blue (Default)"
    if os.path.exists(cfg):
        try:
            with open(cfg, "r") as f: name = json.load(f).get("theme", name)
        except: pass
    base = dict(THEMES.get(name, THEMES["Dark Blue (Default)"]))
    base.update(_shared_colors)
    return base

T = _load_theme()

LANGUAGES = {
    "English": {
        "app_title":"OmniSend Pro","email":"Email","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Log","settings":"Settings","tools":"Tools",
        "compose":"Compose","send":"START SENDING","stop":"STOP","save_campaign":"Save Campaign",
        "load_campaign":"Load Campaign","export_log":"Export Log","check_updates":"Check for Updates",
        "about":"About","recipients":"Recipients","message":"Message","subject":"Subject",
        "from_name":"From Name","from_email":"From Email","body":"Email Body","attachments":"Attachments",
        "templates":"Templates","preview":"Preview","connect":"Connect","disconnect":"Disconnect",
        "import":"Import","clear":"Clear","test":"Test Connection","sending_speed":"Sending Speed",
        "batch":"Batch Sending","retry":"Auto Retry","notifications":"Notifications",
        "search":"Search","add":"Add","remove":"Remove","save":"Save","cancel":"Cancel",
        "confirm":"Confirm","success":"Success","error":"Error","warning":"Warning",
    },
    "Francais": {
        "app_title":"OmniSend Pro","email":"Email","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Journal","settings":"Parametres","tools":"Outils",
        "compose":"Composer","send":"COMMENCER L'ENVOI","stop":"ARRETER","save_campaign":"Sauvegarder",
        "load_campaign":"Charger","export_log":"Exporter le journal","check_updates":"Verifier les MaJ",
        "about":"A propos","recipients":"Destinataires","message":"Message","subject":"Objet",
        "from_name":"Nom exp.","from_email":"Email exp.","body":"Corps de l'email","attachments":"Pieces jointes",
        "templates":"Modeles","preview":"Apercu","connect":"Connecter","disconnect":"Deconnecter",
        "import":"Importer","clear":"Effacer","test":"Tester la connexion","sending_speed":"Vitesse d'envoi",
        "batch":"Envoi par lots","retry":"Renvoi automatique","notifications":"Notifications",
        "search":"Chercher","add":"Ajouter","remove":"Supprimer","save":"Enregistrer","cancel":"Annuler",
        "confirm":"Confirmer","success":"Succes","error":"Erreur","warning":"Attention",
    },
    "Arabe (Darija)": {
        "app_title":"OmniSend Pro","email":"Email","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Sijil","settings":"I3dadat","tools":"Adawat",
        "compose":"Kteb","send":"BEDA L'IRSAL","stop":"W9EF","save_campaign":"7fed Campaign",
        "load_campaign":"7mel Campaign","export_log":"Khroj Sijil","check_updates":"Chouf Updates",
        "about":"3la l'Application","recipients":"Mostaqbilin","message":"Rissala","subject":"Mawdo3",
        "from_name":"Ism Morsil","from_email":"Email Morsil","body":"Jism l'Email","attachments":"Mourfaqat",
        "templates":"9walib","preview":"Mocha7ada","connect":"Twassl","disconnect":"F9e3 Twassl",
        "import":"Jib","clear":"Mse7","test":"Jrb Connexion","sending_speed":"Sor3at l'Irsal",
        "batch":"Irsal b Majmo3at","retry":"I3adat Tawmatikiya","notifications":"Ich3arat",
        "search":"9leb","add":"Zid","remove":"7yed","save":"7fed","cancel":"Lghi",
        "confirm":"Akked","success":"Nja7","error":"Khata2","warning":"Tan7iya",
    },
    "Espanol": {
        "app_title":"OmniSend Pro","email":"Correo","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Registro","settings":"Configuracion","tools":"Herramientas",
        "compose":"Componer","send":"INICIAR ENVIO","stop":"DETENER","save_campaign":"Guardar",
        "load_campaign":"Cargar","export_log":"Exportar Registro","check_updates":"Buscar Actualizaciones",
        "about":"Acerca de","recipients":"Destinatarios","message":"Mensaje","subject":"Asunto",
        "from_name":"Nombre rem.","from_email":"Email rem.","body":"Cuerpo","attachments":"Adjuntos",
        "templates":"Plantillas","preview":"Vista previa","connect":"Conectar","disconnect":"Desconectar",
        "import":"Importar","clear":"Limpiar","test":"Probar Conexion","sending_speed":"Velocidad de envio",
        "batch":"Envio por lotes","retry":"Reintento auto","notifications":"Notificaciones",
        "search":"Buscar","add":"Agregar","remove":"Eliminar","save":"Guardar","cancel":"Cancelar",
        "confirm":"Confirmar","success":"Exito","error":"Error","warning":"Advertencia",
    },
    "Deutsch": {
        "app_title":"OmniSend Pro","email":"E-Mail","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Protokoll","settings":"Einstellungen","tools":"Werkzeuge",
        "compose":"Verfassen","send":"SENDEN STARTEN","stop":"STOPPEN","save_campaign":"Speichern",
        "load_campaign":"Laden","export_log":"Protokoll exportieren","check_updates":"Updates prufen",
        "about":"Info","recipients":"Empfanger","message":"Nachricht","subject":"Betreff",
        "from_name":"Absendername","from_email":"Absender-Email","body":"E-Mail-Text","attachments":"Anhange",
        "templates":"Vorlagen","preview":"Vorschau","connect":"Verbinden","disconnect":"Trennen",
        "import":"Importieren","clear":"Loschen","test":"Verbindung testen","sending_speed":"Sendegeschwindigkeit",
        "batch":"Stapelversand","retry":"Automatisch wiederholen","notifications":"Benachrichtigungen",
        "search":"Suchen","add":"Hinzufugen","remove":"Entfernen","save":"Speichern","cancel":"Abbrechen",
        "confirm":"Bestatigen","success":"Erfolg","error":"Fehler","warning":"Warnung",
    },
    "Turkce": {
        "app_title":"OmniSend Pro","email":"E-posta","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Gunluk","settings":"Ayarlar","tools":"Araclar",
        "compose":"Olustur","send":"GONDERMEYE BASLA","stop":"DURDUR","save_campaign":"Kaydet",
        "load_campaign":"Yukle","export_log":"Gunlugu Aktar","check_updates":"Guncelleme Kontrol",
        "about":"Hakkinda","recipients":"Alicilar","message":"Mesaj","subject":"Konu",
        "from_name":"Gonderen Adi","from_email":"Gonderen Email","body":"E-posta Govdesi","attachments":"Ekler",
        "templates":"Sablonlar","preview":"Onizleme","connect":"Baglan","disconnect":"Baglanti Kes",
        "import":"Aktar","clear":"Temizle","test":"Baglantiyi Test Et","sending_speed":"Gonderim Hizi",
        "batch":"Toplu Gonderim","retry":"Otomatik Tekrar","notifications":"Bildirimler",
        "search":"Ara","add":"Ekle","remove":"Kaldir","save":"Kaydet","cancel":"Iptal",
        "confirm":"Onayla","success":"Basarili","error":"Hata","warning":"Uyari",
    },
    "Portugues": {
        "app_title":"OmniSend Pro","email":"Email","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Registro","settings":"Configuracoes","tools":"Ferramentas",
        "compose":"Compor","send":"INICIAR ENVIO","stop":"PARAR","save_campaign":"Salvar Campanha",
        "load_campaign":"Carregar","export_log":"Exportar Registro","check_updates":"Verificar Atualizacoes",
        "about":"Sobre","recipients":"Destinatarios","message":"Mensagem","subject":"Assunto",
        "from_name":"Nome remet.","from_email":"Email remet.","body":"Corpo do Email","attachments":"Anexos",
        "templates":"Modelos","preview":"Pre-visualizar","connect":"Conectar","disconnect":"Desconectar",
        "import":"Importar","clear":"Limpar","test":"Testar Conexao","sending_speed":"Velocidade de envio",
        "batch":"Envio em lotes","retry":"Reenvio automatico","notifications":"Notificacoes",
        "search":"Pesquisar","add":"Adicionar","remove":"Remover","save":"Salvar","cancel":"Cancelar",
        "confirm":"Confirmar","success":"Sucesso","error":"Erro","warning":"Aviso",
    },
    "Italiano": {
        "app_title":"OmniSend Pro","email":"Email","whatsapp":"WhatsApp","sms":"SMS",
        "telegram":"Telegram","log":"Registro","settings":"Impostazioni","tools":"Strumenti",
        "compose":"Componi","send":"INIZIA INVIO","stop":"FERMA","save_campaign":"Salva Campagna",
        "load_campaign":"Carica","export_log":"Esporta Registro","check_updates":"Controlla Aggiornamenti",
        "about":"Info","recipients":"Destinatari","message":"Messaggio","subject":"Oggetto",
        "from_name":"Nome mitt.","from_email":"Email mitt.","body":"Corpo Email","attachments":"Allegati",
        "templates":"Modelli","preview":"Anteprima","connect":"Connetti","disconnect":"Disconnetti",
        "import":"Importa","clear":"Cancella","test":"Testa Connessione","sending_speed":"Velocita di invio",
        "batch":"Invio a lotti","retry":"Ritentativo auto","notifications":"Notifiche",
        "search":"Cerca","add":"Aggiungi","remove":"Rimuovi","save":"Salva","cancel":"Annulla",
        "confirm":"Conferma","success":"Successo","error":"Errore","warning":"Avviso",
    },
}

def _load_lang():
    cfg = os.path.join(DATA_DIR, "app_settings.json")
    name = "English"
    if os.path.exists(cfg):
        try:
            with open(cfg, "r") as f: name = json.load(f).get("language", name)
        except: pass
    return name, LANGUAGES.get(name, LANGUAGES["English"])

CURRENT_LANG, L = _load_lang()

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def spin(text):
    pat = re.compile(r"\{([^{}]+)\}")
    while pat.search(text):
        text = pat.sub(lambda m: random.choice(m.group(1).split("|")), text)
    return text

def rv(text, v):
    for k, val in v.items(): text = text.replace("{{"+k+"}}", val)
    return spin(text)

def parse_emails(raw):
    out = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line: continue
        for sep in (",","\t",";"):
            if sep in line:
                p = [x.strip() for x in line.split(sep, 1)]
                email, name = p[0], p[1] if len(p)>1 else ""; break
        else: email, name = line, ""
        if re.match(r"[^@]+@[^@]+\.[^@]+", email): out.append({"email":email,"name":name})
    return out

def parse_phones(raw):
    out = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line: continue
        for sep in (",","\t",";"):
            if sep in line:
                p = [x.strip() for x in line.split(sep, 1)]
                phone, name = p[0], p[1] if len(p)>1 else ""; break
        else: phone, name = line, ""
        phone = re.sub(r"[^\d+]", "", phone)
        if len(phone) >= 8: out.append({"phone":phone,"name":name})
    return out

def is_valid_email(e):
    return bool(re.match(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$", e))

def http_post_json(url, data, headers=None):
    hdrs = {"Content-Type": "application/json"}
    if headers: hdrs.update(headers)
    body = json.dumps(data).encode("utf-8")
    req = Request(url, data=body, headers=hdrs, method="POST")
    resp = urlopen(req, timeout=30)
    return json.loads(resp.read().decode("utf-8"))

TEMPLATES = {
    "Blank":"",
    "Professional":'<div style="font-family:Arial;max-width:600px;margin:0 auto;padding:20px;"><h2 style="color:#333;">{{subject}}</h2><p>Hello {{name}},</p><p>Your content here.</p><br><p>Best regards,<br><strong>Your Name</strong></p><hr style="border:none;border-top:1px solid #eee;"><p style="font-size:12px;color:#999;">Sent to {{email}}</p></div>',
    "Newsletter":'<div style="font-family:Arial;max-width:600px;margin:0 auto;background:#f9f9f9;"><div style="background:#2563eb;padding:30px;text-align:center;"><h1 style="color:#fff;">Newsletter</h1></div><div style="padding:30px;"><h2 style="color:#1e40af;">Hello {{name}},</h2><p>Content here.</p><div style="text-align:center;margin:30px 0;"><a href="#" style="background:#2563eb;color:#fff;padding:12px 30px;border-radius:6px;text-decoration:none;">Read More</a></div></div></div>',
    "Promotion":'<div style="font-family:Arial;max-width:600px;margin:0 auto;"><div style="background:linear-gradient(135deg,#f59e0b,#ef4444);padding:40px;text-align:center;"><h1 style="color:#fff;font-size:32px;">SPECIAL OFFER</h1></div><div style="padding:30px;text-align:center;"><h2>Hi {{name}}!</h2><div style="background:#fef3c7;padding:20px;border-radius:10px;margin:20px 0;"><p style="font-size:36px;font-weight:bold;color:#f59e0b;">50% OFF</p></div></div></div>',
    "Welcome":'<div style="font-family:Arial;max-width:600px;margin:0 auto;padding:30px;"><div style="text-align:center;padding:20px;"><h1 style="color:#2563eb;">Welcome, {{name}}!</h1><p style="font-size:16px;color:#555;">We\'re excited to have you on board.</p></div><div style="background:#f0f9ff;padding:20px;border-radius:10px;margin:20px 0;"><p style="color:#333;">Your account is all set up and ready to go. Click the button below to get started.</p><div style="text-align:center;margin:20px 0;"><a href="#" style="background:#2563eb;color:#fff;padding:14px 36px;border-radius:8px;text-decoration:none;font-weight:bold;">Get Started</a></div></div><p style="font-size:12px;color:#999;text-align:center;">Sent to {{email}}</p></div>',
    "Invoice":'<div style="font-family:Arial;max-width:600px;margin:0 auto;padding:20px;"><h2 style="color:#333;border-bottom:2px solid #eee;padding-bottom:10px;">Invoice</h2><p>Hello {{name}},</p><p>Please find your invoice details below:</p><table style="width:100%;border-collapse:collapse;margin:20px 0;"><tr style="background:#f9f9f9;"><th style="padding:10px;text-align:left;border:1px solid #ddd;">Item</th><th style="padding:10px;text-align:right;border:1px solid #ddd;">Amount</th></tr><tr><td style="padding:10px;border:1px solid #ddd;">Service</td><td style="padding:10px;text-align:right;border:1px solid #ddd;">$0.00</td></tr><tr style="font-weight:bold;"><td style="padding:10px;border:1px solid #ddd;">Total</td><td style="padding:10px;text-align:right;border:1px solid #ddd;">$0.00</td></tr></table><p>Thank you for your business!</p></div>',
}

WA_TEMPLATES = {
    "Greeting": "Hello {{name}}! How are you doing today?",
    "Promotion": "Hi {{name}}! We have an exclusive offer just for you. Check it out now and save big! Reply YES for more details.",
    "Reminder": "Hi {{name}}, this is a friendly reminder about your upcoming appointment. Please confirm by replying to this message.",
    "Follow-Up": "Hello {{name}}, just following up on our previous conversation. Let me know if you have any questions!",
    "Thank You": "Hi {{name}}! Thank you for your purchase. We appreciate your business and hope to serve you again soon.",
    "Event Invite": "Hey {{name}}! You're invited to our special event on {{date}}. Don't miss it! Reply CONFIRM to reserve your spot.",
}

SMS_TEMPLATES = {
    "Verification": "Your verification code is {{random}}. Valid for 10 minutes. Do not share this code.",
    "Promotion": "Hi {{name}}! Limited time offer - save up to 50% today. Visit our store now!",
    "Reminder": "Reminder: Hi {{name}}, your appointment is scheduled for {{date}} at {{time}}.",
    "Alert": "Alert: Hi {{name}}, there is an update regarding your account. Please check your inbox.",
    "Thank You": "Thank you {{name}} for choosing us! Your order has been confirmed.",
}

TG_TEMPLATES = {
    "Welcome": "Welcome {{name}}! Thanks for joining our Telegram channel.",
    "Announcement": "Attention! Important update for all members. Check the details below.",
    "Promotion": "Hi {{name}}! Exclusive deal just for you - limited time offer. Don't miss out!",
    "Reminder": "Hi {{name}}, friendly reminder: your event is on {{date}} at {{time}}.",
    "Alert": "Alert: {{name}}, there's an important update regarding your account. Please review.",
    "Newsletter": "Hi {{name}}! Here's your weekly digest for {{date}}. Stay tuned for more!",
}

SMTP_PRESETS = {
    "── Cloud / Transactional ──": None,
    "Amazon SES (US-East-1)":        {"host":"email-smtp.us-east-1.amazonaws.com", "port":"587", "enc":"tls"},
    "Amazon SES (US-West-2)":        {"host":"email-smtp.us-west-2.amazonaws.com", "port":"587", "enc":"tls"},
    "Amazon SES (EU-West-1)":        {"host":"email-smtp.eu-west-1.amazonaws.com", "port":"587", "enc":"tls"},
    "Amazon SES (EU-Central-1)":     {"host":"email-smtp.eu-central-1.amazonaws.com", "port":"587", "enc":"tls"},
    "Amazon SES (AP-South-1)":       {"host":"email-smtp.ap-south-1.amazonaws.com", "port":"587", "enc":"tls"},
    "SendGrid":                      {"host":"smtp.sendgrid.net", "port":"587", "enc":"tls"},
    "Mailgun":                       {"host":"smtp.mailgun.org", "port":"587", "enc":"tls"},
    "Mailjet":                       {"host":"in-v3.mailjet.com", "port":"587", "enc":"tls"},
    "SparkPost":                     {"host":"smtp.sparkpostmail.com", "port":"587", "enc":"tls"},
    "Postmark":                      {"host":"smtp.postmarkapp.com", "port":"587", "enc":"tls"},
    "Elastic Email":                 {"host":"smtp.elasticemail.com", "port":"2525", "enc":"tls"},
    "SMTP2GO":                       {"host":"mail.smtp2go.com", "port":"587", "enc":"tls"},
    "Sendinblue (Brevo)":            {"host":"smtp-relay.brevo.com", "port":"587", "enc":"tls"},
    "Pepipost":                      {"host":"smtp.pepipost.com", "port":"587", "enc":"tls"},
    "SocketLabs":                    {"host":"smtp.socketlabs.com", "port":"587", "enc":"tls"},
    "Turbo-SMTP":                    {"host":"pro.turbo-smtp.com", "port":"587", "enc":"tls"},
    "SMTP.com":                      {"host":"send.smtp.com", "port":"587", "enc":"tls"},
    "Mailtrap":                      {"host":"live.smtp.mailtrap.io", "port":"587", "enc":"tls"},
    "── Free Email Providers ──": None,
    "Gmail / Google Workspace":      {"host":"smtp.gmail.com", "port":"465", "enc":"ssl"},
    "Gmail (TLS)":                   {"host":"smtp.gmail.com", "port":"587", "enc":"tls"},
    "Outlook / Hotmail":             {"host":"smtp-mail.outlook.com", "port":"587", "enc":"tls"},
    "Office 365":                    {"host":"smtp.office365.com", "port":"587", "enc":"tls"},
    "Yahoo Mail":                    {"host":"smtp.mail.yahoo.com", "port":"465", "enc":"ssl"},
    "Yahoo (TLS)":                   {"host":"smtp.mail.yahoo.com", "port":"587", "enc":"tls"},
    "iCloud / Apple":                {"host":"smtp.mail.me.com", "port":"587", "enc":"tls"},
    "AOL":                           {"host":"smtp.aol.com", "port":"465", "enc":"ssl"},
    "Zoho Mail":                     {"host":"smtp.zoho.com", "port":"465", "enc":"ssl"},
    "Zoho (TLS)":                    {"host":"smtppro.zoho.com", "port":"587", "enc":"tls"},
    "ProtonMail Bridge":             {"host":"127.0.0.1", "port":"1025", "enc":"tls"},
    "GMX Mail":                      {"host":"mail.gmx.com", "port":"465", "enc":"ssl"},
    "Mail.com":                      {"host":"smtp.mail.com", "port":"465", "enc":"ssl"},
    "Yandex Mail":                   {"host":"smtp.yandex.com", "port":"465", "enc":"ssl"},
    "── ISP SMTP ──": None,
    "Comcast / Xfinity":             {"host":"smtp.comcast.net", "port":"587", "enc":"tls"},
    "AT&T":                          {"host":"smtp.att.yahoo.com", "port":"465", "enc":"ssl"},
    "Verizon":                       {"host":"smtp.verizon.net", "port":"465", "enc":"ssl"},
    "Spectrum / Charter":            {"host":"mobile.charter.net", "port":"587", "enc":"tls"},
    "Cox":                           {"host":"smtp.cox.net", "port":"587", "enc":"tls"},
    "Frontier":                      {"host":"smtp.frontier.com", "port":"587", "enc":"tls"},
    "Earthlink":                     {"host":"smtpauth.earthlink.net", "port":"587", "enc":"tls"},
    "── Hosting / Domain SMTP ──": None,
    "cPanel (default)":              {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "cPanel (TLS)":                  {"host":"mail.yourdomain.com", "port":"587", "enc":"tls"},
    "Plesk":                         {"host":"mail.yourdomain.com", "port":"587", "enc":"tls"},
    "GoDaddy (Workspace)":           {"host":"smtpout.secureserver.net", "port":"465", "enc":"ssl"},
    "GoDaddy (O365)":                {"host":"smtp.office365.com", "port":"587", "enc":"tls"},
    "Namecheap (Private Email)":     {"host":"mail.privateemail.com", "port":"465", "enc":"ssl"},
    "Hostinger":                     {"host":"smtp.hostinger.com", "port":"465", "enc":"ssl"},
    "Bluehost":                      {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "SiteGround":                    {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "DreamHost":                     {"host":"smtp.dreamhost.com", "port":"465", "enc":"ssl"},
    "HostGator":                     {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "A2 Hosting":                    {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "InMotion Hosting":              {"host":"mail.yourdomain.com", "port":"465", "enc":"ssl"},
    "OVH":                           {"host":"ssl0.ovh.net", "port":"465", "enc":"ssl"},
    "Hetzner":                       {"host":"mail.your-server.de", "port":"587", "enc":"tls"},
    "Ionos (1&1)":                   {"host":"smtp.ionos.com", "port":"465", "enc":"ssl"},
    "Gandi":                         {"host":"mail.gandi.net", "port":"465", "enc":"ssl"},
    "Fastmail":                      {"host":"smtp.fastmail.com", "port":"465", "enc":"ssl"},
    "── Self-Hosted / Relay ──": None,
    "Postfix (localhost)":           {"host":"localhost", "port":"25", "enc":"none"},
    "Postfix (local TLS)":           {"host":"localhost", "port":"587", "enc":"tls"},
    "hMailServer (local)":           {"host":"localhost", "port":"25", "enc":"none"},
    "Mailcow":                       {"host":"mail.yourdomain.com", "port":"587", "enc":"tls"},
    "PowerMTA":                      {"host":"localhost", "port":"25", "enc":"none"},
    "Postal":                        {"host":"postal.yourdomain.com", "port":"25", "enc":"none"},
    "Mailu":                         {"host":"mail.yourdomain.com", "port":"587", "enc":"tls"},
    "iRedMail":                      {"host":"mail.yourdomain.com", "port":"587", "enc":"tls"},
    "── Custom ──": None,
    "Custom SMTP":                   {"host":"", "port":"587", "enc":"tls"},
}

# ═══════════════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OmniSend Pro")
        self.geometry("1380x860")
        self.minsize(1100, 700)
        self.configure(fg_color=T["bg"])
        self._setup_icon()

        self.smtp_servers, self.attachments = [], []
        self.sending = False
        self.sent_count = self.failed_count = 0
        self.log_data = []
        self._send_start = 0
        self.wa_driver = None
        self.wa_connected = False
        self._sender_names = []
        self._from_emails = []
        self._reply_tos = []
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build()

    def _setup_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "omnisend.ico")
        try:
            if not os.path.exists(icon_path):
                self._generate_icon(icon_path)
            self.iconbitmap(icon_path)
        except Exception:
            pass

    def _generate_icon(self, path):
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            return
        sizes = [16, 24, 32, 48, 64, 128, 256]
        images = []
        for sz in sizes:
            img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            m = sz * 0.05
            draw.rounded_rectangle(
                [m, m, sz - m, sz - m],
                radius=sz * 0.18,
                fill=(37, 99, 235, 255),
            )
            cx, cy = sz / 2, sz / 2
            s = sz * 0.32
            plane_pts = [
                (cx - s * 0.9, cy + s * 0.15),
                (cx + s * 0.95, cy - s * 0.6),
                (cx - s * 0.1, cy - s * 0.05),
                (cx - s * 0.3, cy + s * 0.7),
                (cx - s * 0.1, cy + s * 0.2),
                (cx + s * 0.95, cy - s * 0.6),
            ]
            draw.polygon(plane_pts, fill=(255, 255, 255, 245))
            tail_pts = [
                (cx - s * 0.1, cy - s * 0.05),
                (cx - s * 0.1, cy + s * 0.2),
                (cx - s * 0.55, cy + s * 0.55),
            ]
            draw.polygon(tail_pts, fill=(220, 230, 255, 200))
            images.append(img)
        images[-1].save(path, format="ICO", sizes=[(s, s) for s in sizes])

    def _on_close(self):
        try:
            if self.wa_driver: self.wa_driver.quit()
        except: pass
        self.destroy()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._build_header()
        self._build_sidebar()
        self._build_pages()
        self._build_statusbar()

    # ══════════════════════════════════════════════════════════
    #  HEADER
    # ══════════════════════════════════════════════════════════
    def _build_header(self):
        hdr = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=T["surface"],
                            border_width=0)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew"); hdr.grid_propagate(False)

        br = ctk.CTkFrame(hdr, fg_color="transparent"); br.pack(side="left", padx=18)
        logo = ctk.CTkFrame(br, width=30, height=30, corner_radius=8, fg_color=T["accent"])
        logo.pack(side="left", padx=(0,10)); logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="O", font=("Segoe UI Black",15), text_color="#fff").pack(expand=True)
        ctk.CTkLabel(br, text="OmniSend", font=("Segoe UI Semibold",17), text_color=T["t1"]).pack(side="left")
        ctk.CTkLabel(br, text="Pro", font=("Segoe UI",12), text_color=T["accent_l"]).pack(side="left", padx=(6,0), pady=(0,0))
        self.channel_lbl = ctk.CTkLabel(br, text="", font=("Segoe UI",12), text_color=T["t3"])
        self.channel_lbl.pack(side="left", padx=(14,0))

        right = ctk.CTkFrame(hdr, fg_color="transparent"); right.pack(side="right", padx=18)
        self._badges = {}
        for key, color, lbl in [("total",T["t2"],"Total"),("sent",T["green"],"Sent"),("failed",T["red"],"Fail")]:
            f = ctk.CTkFrame(right, fg_color="transparent"); f.pack(side="left", padx=10)
            ctk.CTkLabel(f, text=lbl, font=("Segoe UI",9), text_color=T["t4"]).pack()
            num = ctk.CTkLabel(f, text="0", font=("Segoe UI Bold",15), text_color=color)
            num.pack(); self._badges[key] = num

    # ══════════════════════════════════════════════════════════
    #  SIDEBAR
    # ══════════════════════════════════════════════════════════
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=T["sidebar"], border_width=0)
        sb.grid(row=1, column=0, sticky="ns"); sb.grid_propagate(False)

        self._nav = []
        nav_items = [
            ("\u2709  Email",       T["accent"]),
            ("\u260E  WhatsApp",    T["wa_green"]),
            ("\u2706  SMS",         T["sms_blue"]),
            ("\u2708  Telegram",    T["tg_blue"]),
            ("\u2630  Log",         T["accent"]),
        ]

        ctk.CTkFrame(sb, height=14, fg_color="transparent").pack()

        for i, (label, color) in enumerate(nav_items):
            if i == 4:
                ctk.CTkFrame(sb, height=1, fg_color=T["border"]).pack(fill="x", padx=16, pady=8)
            f = ctk.CTkFrame(sb, fg_color="transparent"); f.pack(fill="x", padx=6, pady=1)
            dot = ctk.CTkFrame(f, width=3, height=28, corner_radius=2, fg_color="transparent")
            dot.pack(side="left", padx=(4,4))
            btn = ctk.CTkButton(f, text=f"  {label}", height=36, anchor="w",
                                 font=("Segoe UI",12), corner_radius=8,
                                 fg_color="transparent", hover_color=T["sidebar_hover"],
                                 text_color=T["t2"], command=lambda x=i,c=color: self._go(x,c))
            btn.pack(fill="x")
            self._nav.append((btn, dot, color))

        ctk.CTkFrame(sb, height=1, fg_color=T["border"]).pack(fill="x", padx=16, pady=8)

        for text, cmd in [("\U0001F4BE  Save Campaign", self.save_campaign),
                           ("\U0001F4C2  Load Campaign", self.load_campaign),
                           ("\U0001F4CA  Export Log", self.export_log),
                           ("\u2B06  Check for Updates", self._check_for_updates),
                           ("\u2139  About", self._show_about)]:
            ctk.CTkButton(sb, text=f"  {text}", height=28, anchor="w", font=("Segoe UI",10),
                           corner_radius=6, fg_color="transparent", hover_color=T["sidebar_hover"],
                           text_color=T["t3"], command=cmd).pack(fill="x", padx=8, pady=0)

        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=12, pady=14)
        self.send_btn = ctk.CTkButton(bottom, text="\u25B6  START SENDING", height=44,
                                       font=("Segoe UI Bold",13), corner_radius=10,
                                       fg_color=T["green"], hover_color=T["green_h"],
                                       text_color="#fff", command=self.toggle_sending)
        self.send_btn.pack(fill="x")

    def _go(self, idx, color=None):
        names = ["\u2709 Email","\u260E WhatsApp","\u2706 SMS","\u2708 Telegram","\u2630 Log"]
        if idx < len(names):
            self.channel_lbl.configure(text=f"  /  {names[idx]}")

        for i, (btn, dot, c) in enumerate(self._nav):
            if i == idx:
                btn.configure(fg_color=T["sidebar_sel"], text_color=color or c)
                dot.configure(fg_color=color or c)
            else:
                btn.configure(fg_color="transparent", text_color=T["t2"])
                dot.configure(fg_color="transparent")

        if self._pages[idx] is None:
            pg = ctk.CTkFrame(self._page_container, fg_color="transparent")
            self._page_builders[idx](pg)
            self._pages[idx] = pg

        for i, pg in enumerate(self._pages):
            if pg is None: continue
            if i == idx: pg.grid(row=0, column=0, sticky="nsew")
            else: pg.grid_forget()

    def _go_email_tab(self, tab_idx):
        self._go(0, T["accent"])
        if hasattr(self, '_email_tab_sel'): self._email_tab_sel(tab_idx)

    # ══════════════════════════════════════════════════════════
    #  STATUS BAR
    # ══════════════════════════════════════════════════════════
    def _build_statusbar(self):
        bar = ctk.CTkFrame(self, height=28, corner_radius=0, fg_color=T["surface2"])
        bar.grid(row=2, column=0, columnspan=2, sticky="ew"); bar.grid_propagate(False)
        self.status_txt = ctk.CTkLabel(bar, text="  Ready",
                                        font=("Segoe UI",10), text_color=T["t3"])
        self.status_txt.pack(side="left", padx=10)
        ctk.CTkLabel(bar, text=f"OmniSend Pro v{APP_VERSION}", font=("Segoe UI",9),
                      text_color=T["t4"]).pack(side="right", padx=14)

    # ── PAGES ──────────────────────────────────────────────────
    def _build_pages(self):
        c = ctk.CTkFrame(self, fg_color="transparent")
        c.grid(row=1, column=1, sticky="nsew")
        c.grid_rowconfigure(0, weight=1); c.grid_columnconfigure(0, weight=1)
        self._page_container = c

        self._page_builders = [self._pg_email, self._pg_whatsapp, self._pg_sms, self._pg_telegram, self._pg_log]
        self._pages = [None] * len(self._page_builders)

        for i in (0, 4):
            pg = ctk.CTkFrame(c, fg_color="transparent")
            self._page_builders[i](pg)
            self._pages[i] = pg

        self._go(0, T["accent"])

    # ── TAB BAR helper ─────────────────────────────────────────
    def _tabbar(self, parent, tabs):
        bar = ctk.CTkFrame(parent, fg_color=T["surface"], height=40, corner_radius=0)
        bar.pack(fill="x"); bar.pack_propagate(False)
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)
        frames = []; btns = []
        for label, builder in tabs:
            f = ctk.CTkFrame(container, fg_color="transparent")
            builder(f)
            frames.append(f)
        def sel(idx):
            for i in range(len(tabs)):
                if i == idx:
                    btns[i].configure(fg_color=T["accent"], text_color="#fff")
                    frames[i].pack(fill="both", expand=True)
                else:
                    btns[i].configure(fg_color="transparent", text_color=T["t2"])
                    frames[i].pack_forget()
        for i, (label, _) in enumerate(tabs):
            btn = ctk.CTkButton(bar, text=label, height=30, font=("Segoe UI",11),
                                 fg_color="transparent", hover_color=T["sidebar_hover"],
                                 text_color=T["t2"], corner_radius=6,
                                 command=lambda x=i: sel(x))
            btn.pack(side="left", padx=3, pady=5)
            btns.append(btn)
        sel(0)
        return sel

    # ── Reusable collapsible-section builder ──────────────────
    def _tool_section(self, parent, title, items, color=None, expanded=False):
        if color is None: color = T["accent"]
        outer = ctk.CTkFrame(parent, fg_color=T["card"], corner_radius=8)
        outer.pack(fill="x", pady=3)
        hdr = ctk.CTkFrame(outer, fg_color="transparent", cursor="hand2")
        hdr.pack(fill="x", padx=14, pady=10)
        arrow = ctk.CTkLabel(hdr, text="+" if not expanded else "-",
                              font=("Consolas",14,"bold"), text_color=T["t3"], width=18)
        arrow.pack(side="left")
        ctk.CTkFrame(hdr, width=6, height=6, corner_radius=3, fg_color=color).pack(side="left", padx=(6,8))
        ctk.CTkLabel(hdr, text=title, font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        ctk.CTkLabel(hdr, text=f"{len(items)}", font=("Segoe UI",10), text_color=T["t4"]).pack(side="right", padx=4)
        content = ctk.CTkFrame(outer, fg_color="transparent")
        state = [expanded]
        def _build_content():
            if content.winfo_children(): return
            g = ctk.CTkFrame(content, fg_color="transparent"); g.pack(fill="x", padx=10, pady=(0,10))
            cols = 3
            for c_i in range(cols): g.grid_columnconfigure(c_i, weight=1)
            for i, (t, cmd) in enumerate(items):
                ctk.CTkButton(g, text=t, height=36, anchor="w", font=("Segoe UI",11),
                               fg_color=T["card_h"], hover_color=T["border_l"],
                               corner_radius=6, command=cmd
                               ).grid(row=i//cols, column=i%cols, padx=2, pady=2, sticky="ew")
        def toggle(e=None):
            if state[0]:
                content.pack_forget(); arrow.configure(text="+"); state[0] = False
            else:
                _build_content(); content.pack(fill="x"); arrow.configure(text="-"); state[0] = True
        hdr.bind("<Button-1>", toggle)
        for w in hdr.winfo_children(): w.bind("<Button-1>", toggle)
        if expanded: _build_content(); content.pack(fill="x")

    # ═══════════════════════════════════════════════════════════
    #  PAGE: EMAIL  (Tabbed: Compose | SMTP | Tools | Settings)
    # ═══════════════════════════════════════════════════════════
    def _pg_email(self, p):
        self._email_tab_sel = self._tabbar(p, [
            ("\u270F Compose", self._pg_email_compose),
            ("\u2699 SMTP", self._pg_smtp),
            ("\U0001F527 Tools", self._pg_email_tools),
            ("\u2638 Settings", self._pg_settings),
        ])

    def _pg_email_compose(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "Email Sender", "Compose and send bulk emails via SMTP")

        c1 = self._card(sc); self._ctitle(c1, "Sender Information")
        r1 = self._frow(c1, pad=14)
        self.from_name = self._inp(r1, "From Name", "John Doe")
        self.from_email = self._inp(r1, "From Email", "sender@example.com")
        r2 = self._frow(c1, pad=14)
        self.subject_entry = self._inp(r2, "Subject", "Your email subject...")
        self.reply_to = self._inp(r2, "Reply-To", "reply@example.com")
        r3 = self._frow(c1, pad=14)
        self.cc_field = self._inp(r3, "CC", "cc@example.com")
        self.bcc_field = self._inp(r3, "BCC", "bcc@example.com")
        ctk.CTkFrame(c1, height=6, fg_color="transparent").pack()

        c2 = self._card(sc); self._ctitle(c2, "Multiple Subjects", "Random pick per email", T["orange"])
        self.multi_subjects = ctk.CTkTextbox(c2, height=46, font=("Consolas",11),
            fg_color=T["input_bg"], border_width=1, border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        self.multi_subjects.pack(fill="x", padx=14, pady=(0,10))

        c3 = self._card(sc); self._ctitle(c3, "Personalization")
        vf = ctk.CTkFrame(c3, fg_color="transparent"); vf.pack(fill="x", padx=14, pady=(0,4))
        for v in ["{{email}}","{{name}}","{{date}}","{{time}}","{{random}}"]:
            self._tag(vf, v, lambda x=v: self._ivar(x))
        ctk.CTkLabel(c3, text="Spintax: {Hello|Hi|Hey} picks random per email",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=14, pady=(4,8))

        c4 = self._card(sc)
        self._body_card = c4

        # ── Title row with mode toggle ──
        tr = ctk.CTkFrame(c4, fg_color="transparent"); tr.pack(fill="x", padx=10, pady=(8,2))
        ctk.CTkLabel(tr, text="Email Body", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(side="left")
        self.content_type = ctk.StringVar(value="html")
        self._body_visual_mode = False
        for val, lbl in [("html","HTML"),("text","Visual (Text)")]:
            ctk.CTkRadioButton(tr, text=lbl, variable=self.content_type, value=val,
                                font=("Segoe UI",11), fg_color=T["accent"],
                                command=self._body_switch_mode).pack(side="right", padx=6)

        # helper: make a dropdown menu button
        _mcfg = {"bg": T["card"], "fg": T["t1"], "activebackground": T["accent"],
                 "activeforeground": "#fff", "font": ("Segoe UI", 10), "relief": "flat",
                 "bd": 0, "activeborderwidth": 0}
        def _menu_btn(parent, text, items):
            def _show():
                m = tk.Menu(self, tearoff=0, **_mcfg)
                for it in items:
                    if it is None: m.add_separator()
                    elif isinstance(it, tuple) and len(it) == 3:
                        m.add_command(label=it[0], command=it[1], accelerator=it[2])
                    else:
                        m.add_command(label=it[0], command=it[1])
                m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height())
            b = ctk.CTkButton(parent, text=text+" \u25BE", height=22, font=("Segoe UI",10),
                               fg_color="transparent", hover_color=T["border"], text_color=T["t2"],
                               corner_radius=3, command=_show)
            b.pack(side="left", padx=1, pady=2)
            return b

        # ═══════════ MENU BAR ═══════════
        menubar = ctk.CTkFrame(c4, fg_color=T["sidebar"], corner_radius=0, height=28)
        menubar.pack(fill="x", padx=10, pady=(0,0))

        _menu_btn(menubar, "\U0001F4C4 File", [
            ("\U0001F4C4  New (Clear)", lambda: self._ve_clear()),
            ("\U0001F4C2  Open File...", self._body_open_file),
            ("\U0001F4BE  Save File...", self._body_save_file),
            None,
            ("\U0001F4E5  Import Template...", self.open_templates),
            ("\U0001F4E7  Email Scaffold", self._body_email_scaffold),
            ("\U0001F4F1  Responsive Template", self._body_responsive_tpl),
            ("\U0001F311  Dark Mode Template", self._body_dark_mode_tpl),
        ])
        _menu_btn(menubar, "\u270F Edit", [
            ("\u21B6  Undo", lambda: self._ve("undo"), "Ctrl+Z"),
            ("\u21B7  Redo", lambda: self._ve("redo"), "Ctrl+Y"),
            None,
            ("\u2702  Cut", lambda: self._body_action("cut"), "Ctrl+X"),
            ("\U0001F4CB  Copy", lambda: self._body_action("copy"), "Ctrl+C"),
            ("\U0001F4CB  Paste", lambda: self._body_action("paste"), "Ctrl+V"),
            None,
            ("\u2610  Select All", lambda: self._body_action("selectall"), "Ctrl+A"),
            ("\U0001F5D1  Clear All", lambda: self._ve_clear()),
            None,
            ("\U0001F50D  Find...", self._body_find, "Ctrl+F"),
            ("\U0001F504  Replace...", self._body_replace, "Ctrl+H"),
        ])
        _menu_btn(menubar, "\u2795 Insert", [
            ("\U0001F517  Link...", lambda: self._ve_link()),
            ("\U0001F5BC  Image...", lambda: self._ve_image()),
            ("\u2637  Table...", self._body_ins_table),
            ("\U0001F518  Button / CTA...", self._body_ins_button),
            None,
            ("\u2022  Unordered List", lambda: self._ve("insertUnorderedList")),
            ("1.  Ordered List", lambda: self._ve("insertOrderedList")),
            None,
            ("\u25A1  Section Block", lambda: self._ve_insert_text('<div style="padding:20px;background:#f9f9f9;border-radius:8px;">\n  <h2>Section</h2>\n  <p>Content</p>\n</div>\n') if not self._body_visual_mode else self._visual_editor.insert("insert","--- Section ---\n")),
            ("\u2500  Horizontal Rule", lambda: self._ve_insert_text("<hr>\n") if not self._body_visual_mode else self._visual_editor.insert("insert","\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n")),
            ("\u21B5  Line Break", lambda: self._ve_insert_text("<br>\n") if not self._body_visual_mode else self._visual_editor.insert("insert","\n")),
            None,
            ("\u2026  Lorem Ipsum", self._body_lorem),
        ])
        _menu_btn(menubar, "\U0001F441 View", [
            ("\U0001F310  Preview in Browser", self._body_preview_browser),
            ("\U0001F4F0  Inline Preview", self._toggle_inline_preview),
            None,
            ("\U0001F522  Word / Char Count", self._body_word_count),
            ("\u2039/\u203A  View HTML Source", lambda: messagebox.showinfo("HTML Source", self._get_body_html()[:3000])),
        ])
        _menu_btn(menubar, "\u2712 Format", [
            ("B  Bold", lambda: self._ve("bold")),
            ("I  Italic", lambda: self._ve("italic")),
            ("U  Underline", lambda: self._ve("underline")),
            ("S  Strikethrough", lambda: self._body_wrap("<s>","</s>") if not self._body_visual_mode else None),
            None,
            ("H1 Heading 1", lambda: self._ve("formatBlock","<h1>")),
            ("H2 Heading 2", lambda: self._ve("formatBlock","<h2>")),
            ("H3 Heading 3", lambda: self._ve("formatBlock","<h3>")),
            ("\u00B6  Paragraph", lambda: self._ve("formatBlock","<p>")),
            None,
            ("\u2190  Align Left", lambda: self._ve("justifyLeft")),
            ("\u2194  Align Center", lambda: self._ve("justifyCenter")),
            ("\u2192  Align Right", lambda: self._ve("justifyRight")),
            ("\u2550  Justify", lambda: self._ve("justifyFull")),
            None,
            ("\U0001F3A8  Color Text...", lambda: self._ve_color()),
            ("\U0001F524  Font Size...", self._body_ins_fontsize),
            ("\U0001F7E8  Background Color...", lambda: self._ve_hilite()),
            None,
            ("\u275D  Blockquote", lambda: self._ve("formatBlock","<blockquote>")),
            ("</>  Code", lambda: self._body_wrap("<code>","</code>") if not self._body_visual_mode else None),
        ])
        _menu_btn(menubar, "\u2637 Table", [
            ("\u2637  Insert Table...", self._body_ins_table),
            None,
            ("\u2500  1x2 Table", lambda: self._body_ins_quick_table(1,2)),
            ("\u2500  2x2 Table", lambda: self._body_ins_quick_table(2,2)),
            ("\u2500  3x3 Table", lambda: self._body_ins_quick_table(3,3)),
            ("\u2500  4x4 Table", lambda: self._body_ins_quick_table(4,4)),
            ("\u2500  5x3 Table", lambda: self._body_ins_quick_table(5,3)),
        ])
        _menu_btn(menubar, "\U0001F527 Tools", [
            ("\u2728  Beautify HTML", self._body_beautify),
            ("\u26A1  Minify HTML", self._body_minify),
            ("\U0001F5D1  Strip HTML Tags", self._body_strip_tags),
            None,
            ("\U0001F510  Encode HTML Entities", self._body_encode_html),
            ("\U0001F513  Decode HTML Entities", self._body_decode_html),
            None,
            ("\U0001F4C3  Wrap in <html>", self._body_wrap_full_html),
            None,
            ("\u26A0  Spam Word Check", lambda: self._tool_spam_check() if hasattr(self,'_tool_spam_check') else None),
        ])

        # ═══════════ ICON TOOLBAR: visual buttons ═══════════
        def _ibtn(parent, label, cmd, w=28, bold=False, italic=False):
            fn = ("Segoe UI",11,"bold") if bold else ("Segoe UI",11) if italic else ("Segoe UI",10)
            return ctk.CTkButton(parent, text=label, width=w, height=26, font=fn,
                               fg_color="transparent", hover_color=T["border"], text_color=T["t1"],
                               corner_radius=3, command=cmd)
        def _isep(parent):
            return ctk.CTkFrame(parent, width=1, height=20, fg_color=T["border"])

        toolbar = ctk.CTkFrame(c4, fg_color=T["sidebar"], corner_radius=0, height=34)
        toolbar.pack(fill="x", padx=10, pady=(0,0))

        _ibtn(toolbar, "\u21B6", lambda: self._ve("undo"), w=26).pack(side="left", padx=0, pady=3)
        _ibtn(toolbar, "\u21B7", lambda: self._ve("redo"), w=26).pack(side="left", padx=0, pady=3)
        _isep(toolbar).pack(side="left", padx=3, pady=5)

        # Formats dropdown
        def _fmts_show():
            m = tk.Menu(self, tearoff=0, **_mcfg)
            for lbl, tag in [("Heading 1","h1"),("Heading 2","h2"),("Heading 3","h3"),("Heading 4","h4"),
                              ("Paragraph","p"),("Blockquote","blockquote"),("Preformatted","pre")]:
                m.add_command(label=lbl, command=lambda t=tag: self._ve("formatBlock", f"<{t}>"))
            m.tk_popup(self._fmts_btn.winfo_rootx(), self._fmts_btn.winfo_rooty() + self._fmts_btn.winfo_height())
        self._fmts_btn = ctk.CTkButton(toolbar, text="Formats \u25BE", width=70, height=26,
                                        font=("Segoe UI",10), fg_color=T["card_h"], hover_color=T["border"],
                                        text_color=T["t1"], corner_radius=3, command=_fmts_show)
        self._fmts_btn.pack(side="left", padx=2, pady=3)

        for w_ in [_isep(toolbar)]: w_.pack(side="left", padx=3, pady=5)

        btns = [
            _ibtn(toolbar, "B", lambda: self._ve("bold"), bold=True),
            _ibtn(toolbar, "I", lambda: self._ve("italic"), italic=True),
            _ibtn(toolbar, "U", lambda: self._ve("underline")),
        ]
        for b in btns: b.pack(side="left", padx=0, pady=3)
        _isep(toolbar).pack(side="left", padx=3, pady=5)

        aligns = [
            ("\u2261", "justifyLeft"), ("\u2263", "justifyCenter"),
            ("\u2262", "justifyRight"), ("\u2261", "justifyFull"),
        ]
        for sym, cmd in aligns:
            _ibtn(toolbar, sym, lambda c=cmd: self._ve(c), w=26).pack(side="left", padx=0, pady=3)
        _isep(toolbar).pack(side="left", padx=3, pady=5)

        _ibtn(toolbar, "\u2022", lambda: self._ve("insertUnorderedList"), w=26).pack(side="left", padx=0, pady=3)
        _ibtn(toolbar, "1.", lambda: self._ve("insertOrderedList"), w=26).pack(side="left", padx=0, pady=3)
        _isep(toolbar).pack(side="left", padx=3, pady=5)

        _ibtn(toolbar, "Link", lambda: self._ve_link(), w=36).pack(side="left", padx=0, pady=3)
        _ibtn(toolbar, "Img", lambda: self._ve_image(), w=32).pack(side="left", padx=0, pady=3)

        # Toolbar row 2
        toolbar2 = ctk.CTkFrame(c4, fg_color=T["sidebar"], corner_radius=0, height=34)
        toolbar2.pack(fill="x", padx=10, pady=(0,2))

        self._preview_btn = _ibtn(toolbar2, "Preview", self._toggle_inline_preview, w=58)
        self._preview_btn.pack(side="left", padx=2, pady=3)
        _ibtn(toolbar2, "Browser", self._body_preview_browser, w=56).pack(side="left", padx=2, pady=3)
        _isep(toolbar2).pack(side="left", padx=3, pady=5)
        _ibtn(toolbar2, "Color", lambda: self._ve_color(), w=40).pack(side="left", padx=0, pady=3)
        _ibtn(toolbar2, "BgCol", lambda: self._ve_hilite(), w=40).pack(side="left", padx=0, pady=3)
        _isep(toolbar2).pack(side="left", padx=3, pady=5)
        _ibtn(toolbar2, "Templates", self.open_templates, w=68).pack(side="left", padx=2, pady=3)
        _isep(toolbar2).pack(side="left", padx=3, pady=5)
        _ibtn(toolbar2, "Table", self._body_ins_table, w=42).pack(side="left", padx=2, pady=3)
        _ibtn(toolbar2, "Btn", self._body_ins_button, w=32).pack(side="left", padx=2, pady=3)
        _isep(toolbar2).pack(side="left", padx=3, pady=5)

        # Variables dropdown
        def _vars_show():
            m = tk.Menu(self, tearoff=0, **_mcfg)
            for v in ["{{email}}","{{name}}","{{domain}}","{{date}}","{{time}}",
                       "{{random}}","{{uuid}}","{{rand6}}","{{rand_name}}"]:
                m.add_command(label=v, command=lambda x=v: self._ve_insert_text(x))
            m.tk_popup(self._vars_btn.winfo_rootx(), self._vars_btn.winfo_rooty() + self._vars_btn.winfo_height())
        self._vars_btn = ctk.CTkButton(toolbar2, text="Variables \u25BE", width=76, height=26,
                                        font=("Segoe UI",10), fg_color=T["accent"], hover_color=T["accent_h"],
                                        text_color="#fff", corner_radius=3, command=_vars_show)
        self._vars_btn.pack(side="left", padx=2, pady=3)

        # ═══════════ BODY: Code editor (default) + Visual editor (WYSIWYG) ═══════════
        body_container = ctk.CTkFrame(c4, fg_color="transparent", corner_radius=0)
        body_container.pack(fill="both", expand=True, padx=10, pady=(0,0))

        # Code editor (raw HTML)
        self.body = ctk.CTkTextbox(body_container, height=400, font=("Consolas",12), fg_color=T["input_bg"],
                                    border_width=1, border_color=T["input_bd"], corner_radius=0, text_color=T["t1"],
                                    wrap="none")
        self.body.pack(fill="both", expand=True)
        try: self.body._textbox.configure(undo=True, maxundo=50)
        except: pass

        # Visual editor (WYSIWYG)
        self._visual_frame = ctk.CTkFrame(body_container, fg_color="#ffffff", corner_radius=0)
        ve_inner = tk.Frame(self._visual_frame, bg="#ffffff")
        ve_inner.pack(fill="both", expand=True, padx=2, pady=2)
        self._visual_editor = tk.Text(ve_inner, wrap="word", font=("Segoe UI",13),
                                       bg="#ffffff", fg="#222222", insertbackground="#222",
                                       relief="flat", padx=16, pady=12, undo=True,
                                       selectbackground="#3b82f6", selectforeground="#ffffff")
        self._visual_editor.pack(fill="both", expand=True)

        self._visual_editor.tag_configure("bold", font=("Segoe UI",13,"bold"))
        self._visual_editor.tag_configure("italic", font=("Segoe UI",13,"italic"))
        self._visual_editor.tag_configure("underline", underline=True)
        self._visual_editor.tag_configure("bolditalic", font=("Segoe UI",13,"bold"))
        self._visual_editor.tag_configure("h1", font=("Segoe UI",26,"bold"))
        self._visual_editor.tag_configure("h2", font=("Segoe UI",22,"bold"))
        self._visual_editor.tag_configure("h3", font=("Segoe UI",18,"bold"))
        self._visual_editor.tag_configure("center", justify="center")
        self._visual_editor.tag_configure("right", justify="right")
        self._visual_editor.tag_configure("link", foreground="#0066cc", underline=True)

        # ── Status bar ──
        body_sb = ctk.CTkFrame(c4, fg_color=T["sidebar"], corner_radius=0, height=22)
        body_sb.pack(fill="x", padx=10, pady=(0,6))
        self._body_line_lbl = ctk.CTkLabel(body_sb, text="Ln 1, Col 0", font=("Consolas",10), text_color=T["t4"])
        self._body_line_lbl.pack(side="left", padx=6)
        self._body_mode_lbl = ctk.CTkLabel(body_sb, text="Code", font=("Consolas",10,"bold"), text_color=T["accent"])
        self._body_mode_lbl.pack(side="left", padx=6)
        self._body_chars_lbl = ctk.CTkLabel(body_sb, text="0 chars", font=("Consolas",10), text_color=T["t4"])
        self._body_chars_lbl.pack(side="right", padx=6)
        self._body_words_lbl = ctk.CTkLabel(body_sb, text="0 words", font=("Consolas",10), text_color=T["t4"])
        self._body_words_lbl.pack(side="right", padx=6)
        def _upd_body_sb(e=None):
            try:
                if self._body_visual_mode:
                    pos = self._visual_editor.index("insert"); ln, col = pos.split(".")
                    self._body_line_lbl.configure(text=f"Ln {ln}, Col {col}")
                    txt = self._visual_editor.get("1.0","end-1c")
                    self._body_mode_lbl.configure(text="Visual")
                else:
                    pos = self.body.index("insert"); ln, col = pos.split(".")
                    self._body_line_lbl.configure(text=f"Ln {ln}, Col {col}")
                    txt = self.body.get("1.0","end-1c")
                    self._body_mode_lbl.configure(text="HTML")
                self._body_chars_lbl.configure(text=f"{len(txt)} chars")
                self._body_words_lbl.configure(text=f"{len(txt.split())} words")
            except: pass
        self.body.bind("<KeyRelease>", _upd_body_sb)
        self.body.bind("<ButtonRelease-1>", _upd_body_sb)
        self._visual_editor.bind("<KeyRelease>", _upd_body_sb)
        self._visual_editor.bind("<ButtonRelease-1>", _upd_body_sb)

        self._inline_preview_card = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=8)
        self._inline_preview_visible = False

        self._attachments_card = self._card(sc)
        c5 = self._attachments_card
        at = ctk.CTkFrame(c5, fg_color="transparent"); at.pack(fill="x", padx=14, pady=(10,6))
        ctk.CTkLabel(at, text="Attachments", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        ctk.CTkButton(at, text="+ Add", height=26, width=60, fg_color=T["accent"],
                       hover_color=T["accent_h"], corner_radius=6, font=("Segoe UI",10),
                       command=self.add_attachment).pack(side="right")
        self.att_frame = ctk.CTkFrame(c5, fg_color="transparent"); self.att_frame.pack(fill="x", padx=14, pady=(0,10))

        c6 = self._card(sc); self._ctitle(c6, "Recipients")
        ir = ctk.CTkFrame(c6, fg_color="transparent"); ir.pack(fill="x", padx=14, pady=(0,4))
        ctk.CTkButton(ir, text="\U0001F4E5 Import", height=28, fg_color=T["card_h"], hover_color=T["border_l"],
                       corner_radius=6, font=("Segoe UI",10),
                       command=self.import_recipients).pack(side="left")
        ctk.CTkButton(ir, text="Clear", height=28, fg_color=T["red_bg"], hover_color=T["red"],
                       text_color=T["red"], corner_radius=6, font=("Segoe UI",10),
                       command=self.clear_recipients).pack(side="right")
        self.email_count = ctk.CTkLabel(ir, text="0 recipients", font=("Segoe UI",11), text_color=T["t2"])
        self.email_count.pack(side="right", padx=10)
        self.recipients_box = ctk.CTkTextbox(c6, height=90, font=("Consolas",11), fg_color=T["input_bg"],
                                              border_width=1, border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        self.recipients_box.pack(fill="x", padx=14, pady=(0,10))
        self.recipients_box.bind("<KeyRelease>", lambda e: self._update_email_count())

    def _pg_email_tools(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "Email Tools", "Complete toolkit for email campaigns")

        self._tool_section(sc, "Email List Management", [
            ("Remove Duplicates", self._tool_dedup),
            ("Validate Emails", self._tool_validate),
            ("Sort A-Z", self._tool_sort),
            ("Shuffle List", self._tool_shuffle),
            ("Domain Statistics", self._tool_domains),
            ("Split by Domain", self._tool_split),
            ("Merge Lists", self._tool_merge_lists),
            ("Extract Emails from Text", self._tool_extract_emails),
            ("Filter by Domain", self._tool_filter_domain),
            ("Add Name Column", self._tool_add_names),
            ("Count Emails", self._tool_count_emails),
            ("Limit List Size", self._tool_limit_list),
        ], T["accent"], expanded=True)

        self._tool_section(sc, "Spam & Deliverability", [
            ("Spam Score Checker", self._tool_spam_score),
            ("Spam Word Scanner", self._tool_spam_words),
            ("Inbox Placement Test", self._tool_inbox_test),
            ("DMARC Record Checker", self._tool_dmarc_check),
            ("Email Header Analyzer", self._tool_header_analyzer),
            ("Sender Reputation Check", self._tool_reputation),
        ], T["red"], expanded=True)

        self._tool_section(sc, "Email Verification & Testing", [
            ("Send Test Email", self.test_send),
            ("Preview Email", self.preview_email),
            ("Check MX Records", self._tool_check_mx),
            ("Check SPF/DKIM", self._tool_check_spf),
            ("Blacklist Check", self._tool_blacklist_check),
            ("Email Size Calculator", self._tool_email_size),
            ("SMTP Verify Email", self._tool_smtp_verify_email),
            ("SMTP Test All", self._smtp_test_all),
            ("SMTP Pool Test", self._tool_smtp_pool_test),
        ], T["green"])

        self._tool_section(sc, "Email Composition & Content", [
            ("HTML Templates", self.open_templates),
            ("Text to HTML", self._tool_text_to_html),
            ("HTML to Text", self._tool_html_to_text),
            ("Embed Image Base64", self._tool_base64_img),
            ("Embed CID Image", self._tool_cid_images),
            ("Spintax Preview", self._tool_spintax_preview),
            ("Character Counter", self._tool_char_count),
            ("Check Links in Body", self._tool_check_links),
            ("Generate Unsubscribe", self._tool_unsub_link),
            ("Add Tracking Pixel", self._tool_tracking_pixel),
            ("Link Click Tracker", self._tool_link_tracker),
            ("Auto Text Version", self._tool_auto_text_version),
            ("Minify HTML", self._tool_minify_html),
            ("Wrap in Template", self._tool_wrap_template),
            ("Add Inline Styles", self._tool_inline_styles),
            ("HTML Validator", self._tool_html_validator),
            ("Responsive Preview", self._tool_responsive_preview),
            ("Email Signature Generator", self._tool_signature_gen),
            ("URL Shortener", self._tool_url_shortener),
            ("Dynamic Content Blocks", self._tool_dynamic_content),
        ], T["accent"])

        self._tool_section(sc, "Sender & Subject Tools", [
            ("Randomize Subjects", self._tool_random_subjects),
            ("Subject Line Generator", self._tool_subject_gen),
            ("Subject A/B Tester", self._tool_subject_ab),
            ("Random Sender Names", self._tool_random_senders),
            ("Multiple From Emails", self._tool_multi_from),
            ("Reply-To List", self._tool_reply_to_gen),
        ], T["orange"])

        self._tool_section(sc, "Advanced Sending (UltraMailer)", [
            ("Direct MX Test", self._tool_direct_mx_test),
            ("Bounce Filter", self._tool_bounce_filter),
            ("Bounce Email Parser", self._tool_bounce_parser),
            ("Retry Failed Only", self._tool_retry_failed),
            ("Send Speed Calculator", self._tool_speed_calc),
            ("Schedule Send", self._tool_schedule_send),
            ("Email Warmup Planner", self._tool_warmup_planner),
            ("Seed List Manager", self._tool_seed_list),
            ("Domain Sending Stats", self._tool_send_domain_stats),
            ("Domain Throttle Guide", self._tool_domain_throttle_cfg),
        ], T["cyan"])

        self._tool_section(sc, "Headers & Anti-Fingerprint", [
            ("Header Preview", self._tool_header_preview),
            ("Message-ID Customizer", self._tool_msgid_custom),
            ("Advanced Macros", self._tool_advanced_macros),
            ("Encoding Guide", self._tool_encoding_selector),
            ("Fingerprint Check", self._tool_email_fingerprint),
            ("Custom X-Headers Editor", self._tool_xheaders),
            ("DKIM Signature Viewer", self._tool_dkim_viewer),
            ("Return-Path Generator", self._tool_return_path),
        ], T["purple"])

        self._tool_section(sc, "Import / Export", [
            ("Save Campaign", self.save_campaign),
            ("Load Campaign", self.load_campaign),
            ("Export Send Log", self.export_log),
            ("Export Email List", self._tool_export_emails),
            ("Export Phone List", self._tool_export_phones),
            ("Import from CSV", self._tool_import_csv),
            ("Export Results to HTML Report", self._tool_export_html_report),
            ("Backup All Data", self._tool_backup_data),
        ], T["cyan"])

    # ═══════════════════════════════════════════════════════════
    #  PAGE: WHATSAPP  (Tabbed: Compose | Tools)
    # ═══════════════════════════════════════════════════════════
    def _pg_whatsapp(self, p):
        self._tabbar(p, [
            ("\u270F Compose", self._pg_wa_compose),
            ("\U0001F527 Tools", self._pg_wa_tools),
            ("\u2638 Settings", self._pg_wa_settings),
        ])

    def _pg_wa_compose(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=12, pady=8)
        self._ptitle(sc, "WhatsApp Sender", "Send bulk WhatsApp messages")

        c1 = self._card(sc); self._ctitle(c1, "Connection Mode", icon_color=T["wa_green"])

        self.wa_mode = ctk.StringVar(value="web")
        mf = ctk.CTkFrame(c1, fg_color="transparent"); mf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkRadioButton(mf, text="WhatsApp Web (QR Scan)", variable=self.wa_mode, value="web",
                            font=("Segoe UI",12,"bold"), fg_color=T["wa_green"],
                            command=self._wa_toggle).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mf, text="Business API (Meta)", variable=self.wa_mode, value="business",
                            font=("Segoe UI",12), fg_color=T["wa_green"],
                            command=self._wa_toggle).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mf, text="Custom Gateway", variable=self.wa_mode, value="custom",
                            font=("Segoe UI",12), fg_color=T["wa_green"],
                            command=self._wa_toggle).pack(side="left")

        self.wa_web_frame = ctk.CTkFrame(c1, fg_color="transparent")
        self.wa_web_frame.pack(fill="x")

        self.wa_driver = None
        self.wa_connected = False

        status_row = ctk.CTkFrame(self.wa_web_frame, fg_color="transparent")
        status_row.pack(fill="x", padx=16, pady=(8,4))
        self.wa_status_dot = ctk.CTkLabel(status_row, text="●", font=("Segoe UI",16),
                                           text_color=T["red"], width=20)
        self.wa_status_dot.pack(side="left")
        self.wa_status_lbl = ctk.CTkLabel(status_row, text="  Not connected",
                                           font=("Segoe UI",13,"bold"), text_color=T["t2"])
        self.wa_status_lbl.pack(side="left")

        btn_row = ctk.CTkFrame(self.wa_web_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(4,4))
        ctk.CTkButton(btn_row, text="\U0001F4F2  Connect WhatsApp (Open QR)", height=38,
                       fg_color=T["wa_green"], hover_color="#1B9E52", text_color="#ffffff",
                       font=("Segoe UI",13,"bold"), corner_radius=10,
                       command=self._wa_web_connect).pack(side="left", padx=(0,8))
        ctk.CTkButton(btn_row, text="\u2716  Disconnect", height=38,
                       fg_color=T["red_bg"], hover_color=T["red"], text_color=T["red"],
                       font=("Segoe UI",12), corner_radius=10,
                       command=self._wa_web_disconnect).pack(side="left")

        info_lbl = ctk.CTkLabel(self.wa_web_frame,
                      text="Click Connect > Chrome opens WhatsApp Web > Scan QR with your phone > Ready to send!",
                      font=("Segoe UI",11), text_color=T["t3"], wraplength=600, justify="left")
        info_lbl.pack(anchor="w", padx=16, pady=(4,8))

        self.wa_delay_frame = ctk.CTkFrame(self.wa_web_frame, fg_color="transparent")
        self.wa_delay_frame.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkLabel(self.wa_delay_frame, text="Delay between messages (seconds):",
                      font=("Segoe UI",12), text_color=T["t2"]).pack(side="left")
        self.wa_web_delay = ctk.CTkEntry(self.wa_delay_frame, width=60, font=("Segoe UI",12),
                                          fg_color=T["input_bg"], border_color=T["input_bd"],
                                          corner_radius=6, text_color=T["t1"])
        self.wa_web_delay.pack(side="left", padx=8)
        self.wa_web_delay.insert(0, "5")

        if not HAS_SELENIUM:
            warn = ctk.CTkLabel(self.wa_web_frame,
                      text="selenium not installed! Run: pip install selenium webdriver-manager",
                      font=("Segoe UI",12,"bold"), text_color=T["red"])
            warn.pack(anchor="w", padx=16, pady=(0,8))

        self.wa_biz_frame = ctk.CTkFrame(c1, fg_color="transparent")
        r1 = self._frow(self.wa_biz_frame, pad=16)
        self.wa_phone_id = self._inp(r1, "Phone Number ID", "1234567890")
        self.wa_token = self._inp(r1, "Access Token", "EAAxxxxxxx...", show="*")
        ctk.CTkLabel(self.wa_biz_frame, text="Get credentials from: developers.facebook.com > WhatsApp > API Setup",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        self.wa_custom_frame = ctk.CTkFrame(c1, fg_color="transparent")
        r2 = self._frow(self.wa_custom_frame, pad=16)
        self.wa_api_url = self._inp(r2, "API URL", "https://api.example.com/send")
        self.wa_api_key = self._inp(r2, "API Key / Token", "your-api-key", show="*")
        r3 = self._frow(self.wa_custom_frame, pad=16)
        self.wa_sender = self._inp(r3, "Sender Number", "+1234567890")
        self.wa_param_phone = self._inp(r3, "Phone Param Name", "phone")
        r4 = self._frow(self.wa_custom_frame, pad=16)
        self.wa_param_msg = self._inp(r4, "Message Param Name", "message")
        self.wa_param_key = self._inp(r4, "Key Param Name", "api_key")

        c2 = self._card(sc)
        wa_msg_hdr = ctk.CTkFrame(c2, fg_color="transparent"); wa_msg_hdr.pack(fill="x", padx=16, pady=(10,6))
        ctk.CTkLabel(wa_msg_hdr, text="WhatsApp Message", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        ctk.CTkButton(wa_msg_hdr, text="Templates", height=26, width=90, font=("Segoe UI",10),
                       fg_color=T["wa_green"], hover_color="#1B9E52", corner_radius=6,
                       command=self.open_wa_templates).pack(side="right")
        vf = ctk.CTkFrame(c2, fg_color="transparent"); vf.pack(fill="x", padx=16, pady=(0,6))
        for v in ["{{phone}}","{{name}}","{{date}}","{{time}}","{{random}}"]:
            self._tag(vf, v, lambda x=v: self._wa_ivar(x))
        self.wa_message = ctk.CTkTextbox(c2, height=150, font=("Consolas",13), fg_color=T["input_bg"],
                                          border_width=1, border_color=T["input_bd"], corner_radius=8, text_color=T["t1"])
        self.wa_message.pack(fill="x", padx=16, pady=(0,12))

        c2b = self._card(sc); self._ctitle(c2b, "Media (API mode only)", icon_color=T["wa_green"])
        r_media = self._frow(c2b, pad=16)
        self.wa_image_url = self._inp(r_media, "Image URL (leave empty for text only)", "https://example.com/image.jpg")
        ctk.CTkFrame(c2b, height=8, fg_color="transparent").pack()

        c3 = self._card(sc); self._ctitle(c3, "Phone Numbers", icon_color=T["wa_green"])
        ir = ctk.CTkFrame(c3, fg_color="transparent"); ir.pack(fill="x", padx=16, pady=(0,6))
        ctk.CTkButton(ir, text="\U0001F4E5 Import", height=30, fg_color=T["card_h"], hover_color=T["border"],
                       command=lambda: self._import_phones(self.wa_phones, self.wa_count)).pack(side="left")
        ctk.CTkButton(ir, text="Clear", height=30, fg_color=T["red_bg"], hover_color=T["red"],
                       text_color=T["red"],
                       command=lambda: [self.wa_phones.delete("1.0","end"), self.wa_count.configure(text="0 numbers")]).pack(side="right")
        self.wa_count = ctk.CTkLabel(ir, text="0 numbers", font=("Segoe UI",12), text_color=T["t2"])
        self.wa_count.pack(side="right", padx=12)
        self.wa_phones = ctk.CTkTextbox(c3, height=120, font=("Consolas",12), fg_color=T["input_bg"],
                                         border_width=1, border_color=T["input_bd"], corner_radius=8)
        self.wa_phones.pack(fill="x", padx=16, pady=(0,12))
        self.wa_phones.bind("<KeyRelease>", lambda e: self._count_phones(self.wa_phones, self.wa_count))
        ctk.CTkLabel(c3, text="Format: +1234567890  or  +1234567890,Name  (one per line, with country code)",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

    def _pg_wa_tools(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "WhatsApp Tools", "Tools for WhatsApp campaigns")

        self._tool_section(sc, "WhatsApp Phone Tools", [
            ("Clean Phone Numbers", self._tool_wa_clean_phones),
            ("Remove Duplicate Phones", self._tool_wa_dedup),
            ("Sort Phone Numbers", self._tool_wa_sort),
            ("Shuffle Phones", self._tool_wa_shuffle),
            ("Country Code Stats", self._tool_wa_country_stats),
            ("Split by Country", self._tool_wa_split_country),
            ("Merge Phone Lists", self._tool_wa_merge),
            ("Extract Phones from Text", self._tool_wa_extract),
            ("Message Preview", self._tool_wa_preview),
            ("Count Phones", self._tool_wa_count),
            ("Limit Phone List", self._tool_wa_limit),
            ("Format Numbers +country", self._tool_wa_format),
        ], T["wa_green"], expanded=True)

        self._tool_section(sc, "WhatsApp Message Tools", [
            ("WA Link Generator", self._tool_wa_link_gen),
            ("vCard Generator", self._tool_wa_vcard),
            ("Message Spintax Preview", self._tool_wa_spintax),
            ("Message Character Counter", self._tool_wa_msg_chars),
            ("Bulk Message Scheduler", self._tool_wa_scheduler),
            ("Auto-Reply Template", self._tool_wa_auto_reply),
        ], T["wa_green"])

        self._tool_section(sc, "WhatsApp Utilities", [
            ("Phone Number Validator", self._tool_wa_validate_phone),
            ("Generate Test Numbers", self._tool_wa_test_numbers),
            ("Export Contacts as CSV", self._tool_wa_export_csv),
            ("Import from CSV", self._tool_wa_import_csv),
            ("Broadcast List Creator", self._tool_wa_broadcast),
            ("QR Code Text Generator", self._tool_wa_qr_text),
        ], T["wa_green"])

    def _pg_wa_settings(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "WhatsApp Settings", "Configure WhatsApp sending behavior")

        c1 = self._card(sc); self._ctitle(c1, "Sending Speed", icon_color=T["wa_green"])
        r1 = self._frow(c1, pad=16)
        self.wa_delay_min = self._inp(r1, "Delay Min (s)", "3")
        self.wa_delay_max = self._inp(r1, "Delay Max (s)", "8")
        ctk.CTkLabel(c1, text="Random delay between min/max to avoid detection",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c2 = self._card(sc); self._ctitle(c2, "Batch Sending", icon_color=T["wa_green"])
        r2 = self._frow(c2, pad=16)
        self.wa_batch_size = self._inp(r2, "Messages per batch", "20")
        self.wa_batch_pause = self._inp(r2, "Pause between batches (s)", "60")
        ctk.CTkLabel(c2, text="After each batch, pause to reduce risk of ban",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c3 = self._card(sc); self._ctitle(c3, "Auto Retry", icon_color=T["wa_green"])
        self.wa_retry_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c3, text="  Auto-retry failed messages", variable=self.wa_retry_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        rf = self._frow(c3, pad=16)
        self.wa_retry_max = self._inp(rf, "Max retries", "2", w=100)
        ctk.CTkFrame(c3, height=8, fg_color="transparent").pack()

        c4 = self._card(sc); self._ctitle(c4, "Chrome / Browser", icon_color=T["wa_green"])
        self.wa_headless_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c4, text="  Headless mode (no visible browser)", variable=self.wa_headless_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.wa_save_session_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c4, text="  Save browser session (skip QR next time)", variable=self.wa_save_session_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        pr = self._frow(c4, pad=16)
        self.wa_chrome_profile = self._inp(pr, "Chrome profile path (optional)", "")
        ctk.CTkLabel(c4, text="Leave empty for default. Set a path to persist WhatsApp login.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c5 = self._card(sc); self._ctitle(c5, "Message Options", icon_color=T["wa_green"])
        self.wa_read_receipt_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Wait for read receipt before next message", variable=self.wa_read_receipt_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.wa_typing_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Simulate typing before sending", variable=self.wa_typing_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        r5 = self._frow(c5, pad=16)
        self.wa_typing_duration = self._inp(r5, "Typing duration (s)", "2", w=100)
        ctk.CTkFrame(c5, height=8, fg_color="transparent").pack()

        c6 = self._card(sc); self._ctitle(c6, "Notifications", icon_color=T["wa_green"])
        self.wa_notify_done_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c6, text="  Show notification when batch completes", variable=self.wa_notify_done_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.wa_sound_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c6, text="  Play sound on completion", variable=self.wa_sound_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["wa_green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

    # ═══════════════════════════════════════════════════════════
    #  PAGE: SMS  (Tabbed: Compose | Tools | Settings)
    # ═══════════════════════════════════════════════════════════
    def _pg_sms(self, p):
        self._tabbar(p, [
            ("\u270F Compose", self._pg_sms_compose),
            ("\U0001F527 Tools", self._pg_sms_tools),
            ("\u2638 Settings", self._pg_sms_settings),
        ])

    def _pg_sms_compose(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=12, pady=8)
        self._ptitle(sc, "SMS Sender", "Send bulk SMS via API gateway")

        c1 = self._card(sc); self._ctitle(c1, "SMS Gateway Configuration", icon_color=T["sms_blue"])

        self.sms_mode = ctk.StringVar(value="twilio")
        mf = ctk.CTkFrame(c1, fg_color="transparent"); mf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkRadioButton(mf, text="Twilio", variable=self.sms_mode, value="twilio",
                            font=("Segoe UI",12), fg_color=T["sms_blue"],
                            command=self._sms_toggle).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mf, text="Custom Gateway", variable=self.sms_mode, value="custom",
                            font=("Segoe UI",12), fg_color=T["sms_blue"],
                            command=self._sms_toggle).pack(side="left")

        self.sms_twilio_frame = ctk.CTkFrame(c1, fg_color="transparent")
        self.sms_twilio_frame.pack(fill="x")
        r1 = self._frow(self.sms_twilio_frame, pad=16)
        self.tw_sid = self._inp(r1, "Account SID", "ACxxxxxxxxxxxxxxx")
        self.tw_token = self._inp(r1, "Auth Token", "your_auth_token", show="*")
        r2 = self._frow(self.sms_twilio_frame, pad=16)
        self.tw_from = self._inp(r2, "From Number", "+1234567890")
        ctk.CTkLabel(self.sms_twilio_frame, text="Get credentials from: twilio.com/console",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        self.sms_custom_frame = ctk.CTkFrame(c1, fg_color="transparent")
        r3 = self._frow(self.sms_custom_frame, pad=16)
        self.sms_api_url = self._inp(r3, "API URL", "https://api.example.com/sms/send")
        self.sms_api_key = self._inp(r3, "API Key", "your-api-key", show="*")
        r4 = self._frow(self.sms_custom_frame, pad=16)
        self.sms_from_param = self._inp(r4, "From Param", "from")
        self.sms_to_param = self._inp(r4, "To Param", "to")
        r5 = self._frow(self.sms_custom_frame, pad=16)
        self.sms_msg_param = self._inp(r5, "Message Param", "message")
        self.sms_key_param = self._inp(r5, "Key Param", "api_key")

        c2 = self._card(sc)
        sms_msg_hdr = ctk.CTkFrame(c2, fg_color="transparent"); sms_msg_hdr.pack(fill="x", padx=16, pady=(10,6))
        ctk.CTkLabel(sms_msg_hdr, text="SMS Message", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        ctk.CTkButton(sms_msg_hdr, text="Templates", height=26, width=90, font=("Segoe UI",10),
                       fg_color=T["sms_blue"], hover_color="#0077b5", corner_radius=6,
                       command=self.open_sms_templates).pack(side="right")
        vf = ctk.CTkFrame(c2, fg_color="transparent"); vf.pack(fill="x", padx=16, pady=(0,6))
        for v in ["{{phone}}","{{name}}","{{date}}","{{time}}","{{random}}"]:
            self._tag(vf, v, lambda x=v: self._sms_ivar(x))
        self.sms_message = ctk.CTkTextbox(c2, height=120, font=("Consolas",13), fg_color=T["input_bg"],
                                           border_width=1, border_color=T["input_bd"], corner_radius=8, text_color=T["t1"])
        self.sms_message.pack(fill="x", padx=16, pady=(0,4))
        self.sms_char_count = ctk.CTkLabel(c2, text="0 / 160 chars", font=("Segoe UI",11), text_color=T["t3"])
        self.sms_char_count.pack(anchor="w", padx=16, pady=(0,12))
        self.sms_message.bind("<KeyRelease>", lambda e: self.sms_char_count.configure(
            text=f"{len(self.sms_message.get('1.0','end').strip())} / 160 chars"))

        c3 = self._card(sc); self._ctitle(c3, "Phone Numbers", icon_color=T["sms_blue"])
        ir = ctk.CTkFrame(c3, fg_color="transparent"); ir.pack(fill="x", padx=16, pady=(0,6))
        ctk.CTkButton(ir, text="\U0001F4E5 Import", height=30, fg_color=T["card_h"], hover_color=T["border"],
                       command=lambda: self._import_phones(self.sms_phones, self.sms_count)).pack(side="left")
        ctk.CTkButton(ir, text="Clear", height=30, fg_color=T["red_bg"], hover_color=T["red"],
                       text_color=T["red"],
                       command=lambda: [self.sms_phones.delete("1.0","end"), self.sms_count.configure(text="0 numbers")]).pack(side="right")
        self.sms_count = ctk.CTkLabel(ir, text="0 numbers", font=("Segoe UI",12), text_color=T["t2"])
        self.sms_count.pack(side="right", padx=12)
        self.sms_phones = ctk.CTkTextbox(c3, height=120, font=("Consolas",12), fg_color=T["input_bg"],
                                          border_width=1, border_color=T["input_bd"], corner_radius=8)
        self.sms_phones.pack(fill="x", padx=16, pady=(0,12))
        self.sms_phones.bind("<KeyRelease>", lambda e: self._count_phones(self.sms_phones, self.sms_count))
        ctk.CTkLabel(c3, text="Format: +1234567890  or  +1234567890,Name  (one per line)",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

    def _pg_sms_tools(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "SMS Tools", "Tools for SMS campaigns")

        self._tool_section(sc, "SMS Message Tools", [
            ("SMS Character Counter", self._tool_sms_char_count),
            ("SMS Parts Calculator", self._tool_sms_parts),
            ("Preview SMS", self._tool_sms_preview),
            ("SMS Encoding Detector", self._tool_sms_encoding),
            ("Short URL Generator", self._tool_sms_short_url),
            ("Opt-Out Generator", self._tool_sms_optout),
            ("SMS Spintax Preview", self._tool_sms_spintax),
        ], T["sms_blue"], expanded=True)

        self._tool_section(sc, "SMS Phone Tools", [
            ("Validate Phone Numbers", self._tool_sms_validate_phones),
            ("Remove Duplicate Phones", self._tool_sms_dedup),
            ("Sort Phone Numbers", self._tool_sms_sort),
            ("Shuffle Phones", self._tool_sms_shuffle),
            ("Format with Country Code", self._tool_sms_format_cc),
            ("Extract Phones from Text", self._tool_sms_extract),
            ("Merge Phone Lists", self._tool_sms_merge),
            ("Count Phone Numbers", self._tool_sms_count_phones),
            ("Limit Phone List", self._tool_sms_limit),
            ("Export Phone List", self._tool_sms_export),
        ], T["sms_blue"])

        self._tool_section(sc, "SMS Analytics", [
            ("SMS Cost Estimator", self._tool_sms_cost),
            ("Delivery Stats", self._tool_sms_delivery_stats),
            ("Country Code Lookup", self._tool_sms_country_lookup),
        ], T["sms_blue"])

    def _pg_sms_settings(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "SMS Settings", "Configure SMS sending behavior")

        c1 = self._card(sc); self._ctitle(c1, "Sending Speed", icon_color=T["sms_blue"])
        r1 = self._frow(c1, pad=16)
        self.sms_delay_min = self._inp(r1, "Delay Min (s)", "1")
        self.sms_delay_max = self._inp(r1, "Delay Max (s)", "3")
        r1b = self._frow(c1, pad=16)
        self.sms_rate_limit = self._inp(r1b, "Max SMS per minute", "30")
        self.sms_threads = self._inp(r1b, "Threads", "1")
        ctk.CTkFrame(c1, height=8, fg_color="transparent").pack()

        c2 = self._card(sc); self._ctitle(c2, "Batch Sending", icon_color=T["sms_blue"])
        r2 = self._frow(c2, pad=16)
        self.sms_batch_size = self._inp(r2, "Messages per batch", "50")
        self.sms_batch_pause = self._inp(r2, "Pause between batches (s)", "30")
        ctk.CTkFrame(c2, height=8, fg_color="transparent").pack()

        c3 = self._card(sc); self._ctitle(c3, "Auto Retry", icon_color=T["sms_blue"])
        self.sms_retry_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c3, text="  Auto-retry failed messages", variable=self.sms_retry_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        rf = self._frow(c3, pad=16)
        self.sms_retry_max = self._inp(rf, "Max retries", "2", w=100)
        ctk.CTkFrame(c3, height=8, fg_color="transparent").pack()

        c4 = self._card(sc); self._ctitle(c4, "Phone Number Format", icon_color=T["sms_blue"])
        r4 = self._frow(c4, pad=16)
        pf = ctk.CTkFrame(r4, fg_color="transparent"); pf.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(pf, text="Default Country Code", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        self.sms_default_cc = ctk.CTkEntry(pf, placeholder_text="+1", height=34, font=("Segoe UI",12),
                                             fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        self.sms_default_cc.pack(fill="x")
        self.sms_auto_format_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c4, text="  Auto-add country code to numbers without one", variable=self.sms_auto_format_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkFrame(c4, height=8, fg_color="transparent").pack()

        c5 = self._card(sc); self._ctitle(c5, "Message Options", icon_color=T["sms_blue"])
        self.sms_auto_split_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Auto-split long messages (>160 chars)", variable=self.sms_auto_split_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.sms_unicode_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Force Unicode encoding (UCS-2)", variable=self.sms_unicode_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.sms_delivery_report_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Request delivery reports", variable=self.sms_delivery_report_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

        c6 = self._card(sc); self._ctitle(c6, "Notifications", icon_color=T["sms_blue"])
        self.sms_notify_done_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c6, text="  Show notification when sending completes", variable=self.sms_notify_done_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.sms_sound_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c6, text="  Play sound on completion", variable=self.sms_sound_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["sms_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

    # ═══════════════════════════════════════════════════════════
    #  PAGE: TELEGRAM
    # ═══════════════════════════════════════════════════════════
    def _pg_telegram(self, p):
        self._tabbar(p, [
            ("\u270F Compose", self._pg_tg_compose),
            ("\U0001F527 Tools", self._pg_tg_tools),
            ("\u2638 Settings", self._pg_tg_settings),
        ])

    def _pg_tg_compose(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=12, pady=8)
        self._ptitle(sc, "Telegram Sender", "Send via Bot API or User Account")

        # ── Connection Mode ──
        c0 = self._card(sc); self._ctitle(c0, "Connection Mode", icon_color=T["tg_blue"])
        self.tg_mode = ctk.StringVar(value="web")
        mf = ctk.CTkFrame(c0, fg_color="transparent"); mf.pack(fill="x", padx=16, pady=(0,8))
        ctk.CTkRadioButton(mf, text="Telegram Web (QR Scan)", variable=self.tg_mode, value="web",
                            font=("Segoe UI",12,"bold"), fg_color=T["tg_blue"],
                            command=self._tg_toggle_mode).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mf, text="Bot API", variable=self.tg_mode, value="bot",
                            font=("Segoe UI",12), fg_color=T["tg_blue"],
                            command=self._tg_toggle_mode).pack(side="left", padx=(0,16))
        ctk.CTkRadioButton(mf, text="User Account", variable=self.tg_mode, value="user",
                            font=("Segoe UI",12), fg_color=T["tg_blue"],
                            command=self._tg_toggle_mode).pack(side="left")

        # ── Telegram Web (QR Scan - Selenium) frame ──
        self.tg_web_frame = ctk.CTkFrame(c0, fg_color="transparent")
        self.tg_web_frame.pack(fill="x")

        self.tg_web_driver = None
        self.tg_web_connected = False

        tg_ws = ctk.CTkFrame(self.tg_web_frame, fg_color="transparent"); tg_ws.pack(fill="x", padx=16, pady=(8,4))
        self.tg_web_status_dot = ctk.CTkLabel(tg_ws, text="●", font=("Segoe UI",18), text_color=T["red"], width=20)
        self.tg_web_status_dot.pack(side="left")
        self.tg_web_status_lbl = ctk.CTkLabel(tg_ws, text="  Not connected", font=("Segoe UI",13,"bold"), text_color=T["t2"])
        self.tg_web_status_lbl.pack(side="left")

        tg_wb = ctk.CTkFrame(self.tg_web_frame, fg_color="transparent"); tg_wb.pack(fill="x", padx=16, pady=(6,4))
        ctk.CTkButton(tg_wb, text="Connect Telegram (Open QR)", height=42,
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"], text_color="#ffffff",
                       font=("Segoe UI",14,"bold"), corner_radius=10,
                       command=self._tg_web_connect).pack(fill="x", pady=(0,6))
        ctk.CTkButton(tg_wb, text="Disconnect", height=34,
                       fg_color=T["red_bg"], hover_color=T["red"], text_color=T["red"],
                       font=("Segoe UI",12), corner_radius=8,
                       command=self._tg_web_disconnect).pack(fill="x")

        ctk.CTkLabel(self.tg_web_frame,
                      text="Click Connect > Chrome opens web.telegram.org > Scan QR with your phone > Ready to send!",
                      font=("Segoe UI",11), text_color=T["t3"], wraplength=600, justify="left").pack(anchor="w", padx=16, pady=(6,2))

        tg_wd = ctk.CTkFrame(self.tg_web_frame, fg_color="transparent"); tg_wd.pack(fill="x", padx=16, pady=(4,8))
        ctk.CTkLabel(tg_wd, text="Delay between messages (seconds):", font=("Segoe UI",12), text_color=T["t2"]).pack(side="left")
        self.tg_web_delay = ctk.CTkEntry(tg_wd, width=60, font=("Segoe UI",12),
                                          fg_color=T["input_bg"], border_color=T["input_bd"],
                                          corner_radius=6, text_color=T["t1"])
        self.tg_web_delay.pack(side="left", padx=8)
        self.tg_web_delay.insert(0, "5")

        if not HAS_SELENIUM:
            ctk.CTkLabel(self.tg_web_frame,
                          text="selenium not installed! Run: pip install selenium webdriver-manager",
                          font=("Segoe UI",12,"bold"), text_color=T["red"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Bot API frame ──
        self.tg_bot_frame = ctk.CTkFrame(c0, fg_color="transparent")
        r1 = self._frow(self.tg_bot_frame, pad=16)
        self.tg_bot_token = self._inp(r1, "Bot Token", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", show="*")
        ctk.CTkLabel(self.tg_bot_frame, text="Get your Bot Token from @BotFather on Telegram",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,4))
        btn_row = ctk.CTkFrame(self.tg_bot_frame, fg_color="transparent"); btn_row.pack(fill="x", padx=16, pady=(4,10))
        ctk.CTkButton(btn_row, text="Test Connection", height=34,
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"], text_color="#ffffff",
                       font=("Segoe UI",12,"bold"), corner_radius=8,
                       command=self._tg_test_connection).pack(side="left", padx=(0,8))
        self.tg_status_lbl = ctk.CTkLabel(btn_row, text="  Not tested", font=("Segoe UI",12), text_color=T["t3"])
        self.tg_status_lbl.pack(side="left")

        # ── User Account (Telethon) frame ──
        self.tg_user_frame = ctk.CTkFrame(c0, fg_color="transparent")
        self.tg_client = None
        self.tg_user_connected = False

        # Status
        u_status = ctk.CTkFrame(self.tg_user_frame, fg_color="transparent"); u_status.pack(fill="x", padx=16, pady=(8,4))
        self.tg_user_status_dot = ctk.CTkLabel(u_status, text="*", font=("Segoe UI",18), text_color=T["red"], width=20)
        self.tg_user_status_dot.pack(side="left")
        self.tg_user_status_lbl = ctk.CTkLabel(u_status, text="  Not connected", font=("Segoe UI",13,"bold"), text_color=T["t2"])
        self.tg_user_status_lbl.pack(side="left")

        # Phone number - simple and prominent
        ph_fr = ctk.CTkFrame(self.tg_user_frame, fg_color="transparent"); ph_fr.pack(fill="x", padx=16, pady=(6,4))
        ctk.CTkLabel(ph_fr, text="Phone Number (with country code):", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w")
        self.tg_phone = ctk.CTkEntry(ph_fr, placeholder_text="+212600000000", height=42, font=("Segoe UI",15),
                                      fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=8, text_color=T["t1"])
        self.tg_phone.pack(fill="x", pady=(2,0))

        # Big login buttons
        u_btn = ctk.CTkFrame(self.tg_user_frame, fg_color="transparent"); u_btn.pack(fill="x", padx=16, pady=(8,4))
        ctk.CTkButton(u_btn, text="Login with Phone Number", height=42,
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"], text_color="#ffffff",
                       font=("Segoe UI",14,"bold"), corner_radius=10,
                       command=self._tg_user_connect).pack(fill="x", pady=(0,6))
        ctk.CTkButton(u_btn, text="Login with QR Code (Scan from Phone)", height=42,
                       fg_color="#7c3aed", hover_color="#6d28d9", text_color="#ffffff",
                       font=("Segoe UI",14,"bold"), corner_radius=10,
                       command=self._tg_qr_login).pack(fill="x", pady=(0,6))

        u_btn2 = ctk.CTkFrame(self.tg_user_frame, fg_color="transparent"); u_btn2.pack(fill="x", padx=16, pady=(0,4))
        ctk.CTkButton(u_btn2, text="Get My Contacts", height=34,
                       fg_color=T["card_h"], hover_color=T["border"],
                       font=("Segoe UI",11), corner_radius=8,
                       command=self._tg_user_get_contacts).pack(side="left")
        ctk.CTkButton(u_btn2, text="Disconnect", height=34,
                       fg_color=T["red_bg"], hover_color=T["red"], text_color=T["red"],
                       font=("Segoe UI",11), corner_radius=8,
                       command=self._tg_user_disconnect).pack(side="right")

        ctk.CTkLabel(self.tg_user_frame,
                      text="Login with your phone or scan QR > Send to any user, contact, group, or channel",
                      font=("Segoe UI",11), text_color=T["t3"], wraplength=600, justify="left").pack(anchor="w", padx=16, pady=(6,2))

        if not HAS_TELETHON:
            ctk.CTkLabel(self.tg_user_frame,
                          text="telethon not installed! Run: pip install telethon",
                          font=("Segoe UI",12,"bold"), text_color=T["red"]).pack(anchor="w", padx=16, pady=(4,8))

        # Advanced (API ID / Hash) - hidden by default
        adv_outer = ctk.CTkFrame(self.tg_user_frame, fg_color="transparent"); adv_outer.pack(fill="x", padx=16, pady=(4,8))
        adv_content = ctk.CTkFrame(adv_outer, fg_color="transparent")
        adv_visible = [False]
        def _toggle_adv():
            if adv_visible[0]:
                adv_content.pack_forget(); adv_btn.configure(text="Advanced Settings  +"); adv_visible[0] = False
            else:
                adv_content.pack(fill="x", pady=(4,0)); adv_btn.configure(text="Advanced Settings  -"); adv_visible[0] = True
        adv_btn = ctk.CTkButton(adv_outer, text="Advanced Settings  +", height=26, anchor="w",
                                 font=("Segoe UI",10), fg_color="transparent", hover_color=T["sidebar_hover"],
                                 text_color=T["t3"], corner_radius=4, command=_toggle_adv)
        adv_btn.pack(anchor="w")
        ar1 = self._frow(adv_content, pad=0)
        self.tg_api_id = self._inp(ar1, "API ID", "12345678")
        self.tg_api_hash = self._inp(ar1, "API Hash", "0123456789abcdef...", show="*")
        ctk.CTkLabel(adv_content, text="Optional: Get from my.telegram.org. Leave empty to use defaults.",
                      font=("Segoe UI",10), text_color=T["t4"]).pack(anchor="w", pady=(2,0))

        # ── Message Options ──
        c1b = self._card(sc); self._ctitle(c1b, "Message Options", icon_color=T["tg_blue"])
        self.tg_parse_mode = ctk.StringVar(value="HTML")
        pm_row = ctk.CTkFrame(c1b, fg_color="transparent"); pm_row.pack(fill="x", padx=16, pady=(0,4))
        ctk.CTkLabel(pm_row, text="Parse Mode:", font=("Segoe UI",12), text_color=T["t2"]).pack(side="left")
        for val in ["HTML","Markdown","None"]:
            ctk.CTkRadioButton(pm_row, text=val, variable=self.tg_parse_mode, value=val,
                                font=("Segoe UI",11), fg_color=T["tg_blue"]).pack(side="left", padx=8)

        self.tg_disable_preview_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c1b, text="  Disable link preview in messages", variable=self.tg_disable_preview_var,
                        font=("Segoe UI",12), fg_color=T["border"], progress_color=T["tg_blue"],
                        button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.tg_silent_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c1b, text="  Send silently (no notification sound)", variable=self.tg_silent_var,
                        font=("Segoe UI",12), fg_color=T["border"], progress_color=T["tg_blue"],
                        button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

        # ── Message ──
        c2 = self._card(sc)
        tg_msg_hdr = ctk.CTkFrame(c2, fg_color="transparent"); tg_msg_hdr.pack(fill="x", padx=16, pady=(10,6))
        ctk.CTkLabel(tg_msg_hdr, text="Message", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        ctk.CTkButton(tg_msg_hdr, text="Templates", height=26, width=90, font=("Segoe UI",10),
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"], corner_radius=6,
                       command=self.open_tg_templates).pack(side="right")
        vf = ctk.CTkFrame(c2, fg_color="transparent"); vf.pack(fill="x", padx=16, pady=(0,6))
        for v in ["{{chat_id}}","{{name}}","{{date}}","{{time}}","{{random}}"]:
            self._tag(vf, v, lambda x=v: self._tg_ivar(x))
        self.tg_message = ctk.CTkTextbox(c2, height=160, font=("Consolas",13), fg_color=T["input_bg"],
                                          border_width=1, border_color=T["input_bd"], corner_radius=8, text_color=T["t1"])
        self.tg_message.pack(fill="x", padx=16, pady=(0,12))

        # ── Media ──
        c2b = self._card(sc); self._ctitle(c2b, "Media Attachment (optional)", icon_color=T["tg_blue"])
        self.tg_media_type = ctk.StringVar(value="none")
        mt_row = ctk.CTkFrame(c2b, fg_color="transparent"); mt_row.pack(fill="x", padx=16, pady=(0,4))
        for val, lbl in [("none","No Media"),("photo","Photo"),("document","Document"),("video","Video"),("audio","Audio")]:
            ctk.CTkRadioButton(mt_row, text=lbl, variable=self.tg_media_type, value=val,
                                font=("Segoe UI",11), fg_color=T["tg_blue"]).pack(side="left", padx=6)
        r_media = self._frow(c2b, pad=16)
        self.tg_media_url = self._inp(r_media, "Media URL or File Path", "https://example.com/image.jpg")
        ctk.CTkLabel(c2b, text="Supports URLs or local file paths. Caption = message text above.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Recipients ──
        c3 = self._card(sc); self._ctitle(c3, "Recipients", icon_color=T["tg_blue"])
        ir = ctk.CTkFrame(c3, fg_color="transparent"); ir.pack(fill="x", padx=16, pady=(0,6))
        ctk.CTkButton(ir, text="\U0001F4E5 Import", height=30, fg_color=T["card_h"], hover_color=T["border"],
                       command=lambda: self._import_tg_ids(self.tg_chat_ids, self.tg_count)).pack(side="left")
        ctk.CTkButton(ir, text="Get from Bot", height=30, fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       text_color="#fff", font=("Segoe UI",11),
                       command=self._tg_get_updates).pack(side="left", padx=6)
        ctk.CTkButton(ir, text="Clear", height=30, fg_color=T["red_bg"], hover_color=T["red"],
                       text_color=T["red"],
                       command=lambda: [self.tg_chat_ids.delete("1.0","end"), self.tg_count.configure(text="0 recipients")]).pack(side="right")
        self.tg_count = ctk.CTkLabel(ir, text="0 recipients", font=("Segoe UI",12), text_color=T["t2"])
        self.tg_count.pack(side="right", padx=12)
        self.tg_chat_ids = ctk.CTkTextbox(c3, height=120, font=("Consolas",12), fg_color=T["input_bg"],
                                            border_width=1, border_color=T["input_bd"], corner_radius=8)
        self.tg_chat_ids.pack(fill="x", padx=16, pady=(0,12))
        self.tg_chat_ids.bind("<KeyRelease>", lambda e: self._count_tg_ids())
        ctk.CTkLabel(c3, text="Chat ID, @username, or phone number (one per line). Format: target  or  target,Name",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

    def _tg_ivar(self, var):
        if hasattr(self, 'tg_message'): self.tg_message.insert("insert", var)

    def _count_tg_ids(self):
        raw = self.tg_chat_ids.get("1.0","end").strip()
        count = len([l for l in raw.splitlines() if l.strip()]) if raw else 0
        self.tg_count.configure(text=f"{count} recipients")

    def _import_tg_ids(self, textbox, count_lbl):
        path = filedialog.askopenfilename(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not path: return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip()]
        textbox.delete("1.0","end")
        textbox.insert("1.0", "\n".join(lines))
        self._count_tg_ids()
        self.log(f"Imported {len(lines)} Telegram recipients", "info")

    def _tg_test_connection(self):
        token = self.tg_bot_token.get().strip()
        if not token:
            self.tg_status_lbl.configure(text="  Enter bot token first", text_color=T["red"])
            return
        def _test():
            try:
                url = f"https://api.telegram.org/bot{token}/getMe"
                req = Request(url, method="GET")
                resp = urlopen(req, timeout=10)
                data = json.loads(resp.read().decode())
                if data.get("ok"):
                    bot_name = data["result"].get("username","Bot")
                    self.after(0, lambda: self.tg_status_lbl.configure(
                        text=f"  Connected: @{bot_name}", text_color=T["green"]))
                    self.after(0, lambda: self.log(f"Telegram bot connected: @{bot_name}", "info"))
                else:
                    self.after(0, lambda: self.tg_status_lbl.configure(
                        text="  Failed: Invalid response", text_color=T["red"]))
            except Exception as ex:
                self.after(0, lambda: self.tg_status_lbl.configure(
                    text=f"  Error: {str(ex)[:50]}", text_color=T["red"]))
        threading.Thread(target=_test, daemon=True).start()

    def _tg_toggle_mode(self):
        mode = self.tg_mode.get()
        for f in (self.tg_web_frame, self.tg_bot_frame, self.tg_user_frame):
            f.pack_forget()
        if mode == "web":
            self.tg_web_frame.pack(fill="x")
        elif mode == "bot":
            self.tg_bot_frame.pack(fill="x")
        else:
            self.tg_user_frame.pack(fill="x")

    def _tg_get_api_creds(self):
        api_id = self.tg_api_id.get().strip() if hasattr(self,'tg_api_id') else ""
        api_hash = self.tg_api_hash.get().strip() if hasattr(self,'tg_api_hash') else ""
        if not api_id or not api_hash:
            api_id = "2040"
            api_hash = "b18441a1ff607e10a989891a5462e627"
        try: api_id = int(api_id)
        except: api_id = 2040
        return api_id, api_hash

    def _tg_user_connect(self):
        if not HAS_TELETHON:
            messagebox.showerror("Missing Library", "Install telethon first:\npip install telethon"); return
        phone = self.tg_phone.get().strip()
        if not phone:
            messagebox.showwarning("","Enter your phone number (with country code, e.g. +212600000000)."); return
        if not phone.startswith("+"):
            phone = "+" + phone; self.tg_phone.delete(0,"end"); self.tg_phone.insert(0, phone)

        api_id, api_hash = self._tg_get_api_creds()
        self.tg_user_status_lbl.configure(text="  Connecting...", text_color=T["orange"])
        self.tg_user_status_dot.configure(text_color=T["orange"])

        session_dir = os.path.join(DATA_DIR, "tg_sessions")
        os.makedirs(session_dir, exist_ok=True)
        session_file = os.path.join(session_dir, f"user_{phone.replace('+','').replace(' ','')}")

        def _connect():
            try:
                client = _TelethonClient(session_file, api_id, api_hash)
                client.connect()

                if not client.is_user_authorized():
                    client.send_code_request(phone)
                    self.after(0, lambda: self._tg_ask_code(client, phone))
                else:
                    self._tg_set_connected(client)
            except Exception as ex:
                self.after(0, lambda: self.tg_user_status_lbl.configure(
                    text=f"  Error: {str(ex)[:60]}", text_color=T["red"]))
                self.after(0, lambda: self.tg_user_status_dot.configure(text_color=T["red"]))

        threading.Thread(target=_connect, daemon=True).start()

    def _tg_qr_login(self):
        if not HAS_TELETHON:
            messagebox.showerror("Missing Library", "Install telethon first:\npip install telethon"); return

        api_id, api_hash = self._tg_get_api_creds()
        self.tg_user_status_lbl.configure(text="  Generating QR code...", text_color=T["orange"])
        self.tg_user_status_dot.configure(text_color=T["orange"])

        session_dir = os.path.join(DATA_DIR, "tg_sessions")
        os.makedirs(session_dir, exist_ok=True)
        session_file = os.path.join(session_dir, "user_qr_session")

        win = ctk.CTkToplevel(self); win.title("Telegram QR Login"); win.geometry("420x520"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Scan QR Code with Telegram", font=("Segoe UI Bold",18), text_color=T["t1"]).pack(pady=(20,4))
        ctk.CTkLabel(win, text="Open Telegram on your phone:\nSettings > Devices > Link Desktop Device",
                      font=("Segoe UI",12), text_color=T["t3"], justify="center").pack(pady=(0,10))

        qr_frame = ctk.CTkFrame(win, width=260, height=260, fg_color="#ffffff", corner_radius=12)
        qr_frame.pack(pady=6); qr_frame.pack_propagate(False)
        qr_label = ctk.CTkLabel(qr_frame, text="Generating...", font=("Segoe UI",12), text_color="#333")
        qr_label.pack(expand=True)

        status_label = ctk.CTkLabel(win, text="Waiting for scan...", font=("Segoe UI",12), text_color=T["orange"])
        status_label.pack(pady=8)

        ctk.CTkLabel(win, text="The QR code refreshes automatically every 30 seconds",
                      font=("Segoe UI",10), text_color=T["t4"]).pack()

        def _qr_flow():
            try:
                client = _TelethonClient(session_file, api_id, api_hash)
                client.connect()

                if client.is_user_authorized():
                    self._tg_set_connected(client)
                    self.after(0, win.destroy)
                    return

                from telethon.tl.functions.auth import ExportLoginTokenRequest, ImportLoginTokenRequest, AcceptLoginTokenRequest
                from telethon.tl.types.auth import LoginToken, LoginTokenMigrateTo, LoginTokenSuccess
                import struct

                while not client.is_user_authorized():
                    try:
                        result = client(ExportLoginTokenRequest(
                            api_id=api_id, api_hash=api_hash, except_ids=[]))

                        if isinstance(result, LoginTokenSuccess):
                            break
                        elif isinstance(result, LoginTokenMigrateTo):
                            client._switch_dc(result.dc_id)
                            result = client(ImportLoginTokenRequest(result.token))
                            if isinstance(result, LoginTokenSuccess):
                                break

                        token = result.token
                        url = "tg://login?token=" + base64.urlsafe_b64encode(token).decode().rstrip("=")

                        try:
                            import qrcode
                            from io import BytesIO
                            from PIL import Image, ImageTk
                            qr = qrcode.QRCode(version=1, box_size=6, border=2,
                                                 error_correction=qrcode.constants.ERROR_CORRECT_L)
                            qr.add_data(url); qr.make(fit=True)
                            img = qr.make_image(fill_color="black", back_color="white")
                            buf = BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
                            pil_img = Image.open(buf).resize((240,240), Image.NEAREST)
                            def _show_qr():
                                tk_img = ImageTk.PhotoImage(pil_img)
                                qr_label.configure(image=tk_img, text="")
                                qr_label._qr_img = tk_img
                            self.after(0, _show_qr)
                        except ImportError:
                            qr_text = f"QR URL:\n{url[:50]}...\n\nInstall for image:\npip install qrcode pillow"
                            self.after(0, lambda t=qr_text: qr_label.configure(text=t, font=("Consolas",8)))

                            link_file = os.path.join(tempfile.gettempdir(), "tg_qr_login.html")
                            html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Telegram QR</title>
                            <script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js"></script>
                            </head><body style="display:flex;align-items:center;justify-content:center;min-height:100vh;background:#1a1a2e;margin:0;">
                            <div style="text-align:center;background:#fff;padding:40px;border-radius:20px;">
                            <h2 style="color:#0088cc;">Scan with Telegram</h2>
                            <div id="qr"></div>
                            <p style="color:#666;font-size:13px;">Settings > Devices > Link Desktop Device</p>
                            </div>
                            <script>var qr=qrcode(0,'L');qr.addData('{url}');qr.make();
                            document.getElementById('qr').innerHTML=qr.createSvgTag(6,0);</script>
                            </body></html>'''
                            with open(link_file,"w",encoding="utf-8") as f: f.write(html)
                            self.after(0, lambda: webbrowser.open(f"file://{link_file}"))
                            self.after(0, lambda: status_label.configure(text="QR opened in browser - scan it!"))

                        self.after(0, lambda: status_label.configure(text="Waiting for scan... (refreshes in 30s)"))
                        time.sleep(30)

                    except Exception as inner_ex:
                        err = str(inner_ex)
                        if "SESSION_PASSWORD_NEEDED" in err.upper():
                            self.after(0, lambda: self._tg_ask_2fa(client, win))
                            return
                        if "RESTART" not in err.upper():
                            self.after(0, lambda e=err: status_label.configure(text=f"Error: {e[:50]}", text_color=T["red"]))
                        break

                if client.is_user_authorized():
                    self._tg_set_connected(client)
                    self.after(0, lambda: status_label.configure(text="Logged in!", text_color=T["green"]))
                    self.after(500, win.destroy)

            except Exception as ex:
                self.after(0, lambda: status_label.configure(text=f"Error: {str(ex)[:50]}", text_color=T["red"]))
                self.after(0, lambda: self.tg_user_status_lbl.configure(text=f"  QR login error", text_color=T["red"]))
                self.after(0, lambda: self.tg_user_status_dot.configure(text_color=T["red"]))

        threading.Thread(target=_qr_flow, daemon=True).start()

    def _tg_ask_2fa(self, client, parent_win):
        if parent_win and parent_win.winfo_exists():
            try: parent_win.destroy()
            except: pass
        win = ctk.CTkToplevel(self); win.title("2FA Password"); win.geometry("380x180"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Enter 2FA Password", font=("Segoe UI Semibold",16), text_color=T["t1"]).pack(padx=20, pady=(16,4))
        ctk.CTkLabel(win, text="Your account has two-factor authentication enabled",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(padx=20)
        pwd_entry = ctk.CTkEntry(win, placeholder_text="Password", height=40, font=("Segoe UI",14),
                                  fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=8,
                                  text_color=T["t1"], show="*")
        pwd_entry.pack(padx=24, fill="x", pady=8); pwd_entry.focus_set()
        def _submit():
            pwd = pwd_entry.get().strip()
            if not pwd: return
            def _do():
                try:
                    client.sign_in(password=pwd)
                    self._tg_set_connected(client)
                    self.after(0, win.destroy)
                except Exception as ex:
                    self.after(0, lambda: messagebox.showerror("2FA Error", str(ex)))
            threading.Thread(target=_do, daemon=True).start()
        pwd_entry.bind("<Return>", lambda e: _submit())
        ctk.CTkButton(win, text="Login", height=38, font=("Segoe UI",13,"bold"),
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_submit).pack(padx=24, pady=(0,12), fill="x")

    def _tg_set_connected(self, client):
        self.tg_client = client
        self.tg_user_connected = True
        me = client.get_me()
        name = me.first_name or ""
        if me.last_name: name += " " + me.last_name
        uname = f" (@{me.username})" if me.username else ""
        self.after(0, lambda: self.tg_user_status_dot.configure(text_color=T["green"]))
        self.after(0, lambda: self.tg_user_status_lbl.configure(
            text=f"  Connected: {name}{uname}", text_color=T["green"]))
        self.after(0, lambda: self.log(f"Telegram user logged in: {name}{uname}", "tg"))

    def _tg_ask_code(self, client, phone):
        win = ctk.CTkToplevel(self); win.title("Telegram Login"); win.geometry("400x260"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Enter Verification Code", font=("Segoe UI Semibold",18), text_color=T["t1"]).pack(padx=20, pady=(20,4))
        ctk.CTkLabel(win, text=f"A code was sent to your Telegram app\n{phone}",
                      font=("Segoe UI",12), text_color=T["t3"], justify="center").pack(padx=20, pady=(0,10))
        code_entry = ctk.CTkEntry(win, placeholder_text="12345", height=48, font=("Segoe UI",22),
                                   fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=10,
                                   text_color=T["t1"], justify="center")
        code_entry.pack(padx=30, fill="x"); code_entry.focus_set()

        pwd_label = ctk.CTkLabel(win, text="", font=("Segoe UI",11), text_color=T["orange"])
        pwd_label.pack(padx=20, pady=(6,0))
        pwd_entry = ctk.CTkEntry(win, placeholder_text="2FA Password", height=38,
                                  font=("Segoe UI",13), fg_color=T["input_bg"], border_color=T["input_bd"],
                                  corner_radius=8, text_color=T["t1"], show="*")

        def _submit():
            code = code_entry.get().strip()
            if not code: return
            def _do():
                try:
                    client.sign_in(phone, code)
                except _TelethonPwdErr:
                    self.after(0, lambda: pwd_label.configure(text="2FA password required:"))
                    self.after(0, lambda: pwd_entry.pack(padx=30, fill="x", after=pwd_label))
                    return
                except Exception as ex:
                    self.after(0, lambda: messagebox.showerror("Login Error", str(ex)))
                    return
                self._tg_set_connected(client)
                self.after(0, win.destroy)
            threading.Thread(target=_do, daemon=True).start()

        def _submit_pwd():
            pwd = pwd_entry.get().strip()
            if not pwd: return
            def _do():
                try:
                    client.sign_in(password=pwd)
                    self._tg_set_connected(client)
                    self.after(0, win.destroy)
                except Exception as ex:
                    self.after(0, lambda: messagebox.showerror("2FA Error", str(ex)))
            threading.Thread(target=_do, daemon=True).start()

        pwd_entry.bind("<Return>", lambda e: _submit_pwd())
        code_entry.bind("<Return>", lambda e: _submit())
        ctk.CTkButton(win, text="Login", height=38, font=("Segoe UI",13,"bold"),
                       fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_submit).pack(padx=30, pady=(8,12), fill="x")

    def _tg_user_disconnect(self):
        if self.tg_client:
            try: self.tg_client.disconnect()
            except: pass
        self.tg_client = None; self.tg_user_connected = False
        self.tg_user_status_dot.configure(text_color=T["red"])
        self.tg_user_status_lbl.configure(text="  Disconnected", text_color=T["t2"])
        self.log("Telegram user disconnected", "info")

    def _tg_user_get_contacts(self):
        if not self.tg_user_connected or not self.tg_client:
            messagebox.showwarning("","Connect your account first."); return
        def _fetch():
            try:
                from telethon.tl.functions.contacts import GetContactsRequest
                result = self.tg_client(GetContactsRequest(hash=0))
                lines = []
                for u in result.users:
                    name = u.first_name or ""
                    if u.last_name: name += " " + u.last_name
                    target = f"@{u.username}" if u.username else str(u.id)
                    lines.append(f"{target},{name.strip()}" if name.strip() else target)
                if not lines:
                    self.after(0, lambda: messagebox.showinfo("","No contacts found.")); return
                def _insert():
                    existing = self.tg_chat_ids.get("1.0","end").strip()
                    if existing: self.tg_chat_ids.insert("end", "\n")
                    self.tg_chat_ids.insert("end", "\n".join(lines))
                    self._count_tg_ids()
                    self.log(f"Loaded {len(lines)} contacts from Telegram account", "tg")
                self.after(0, _insert)
            except Exception as ex:
                self.after(0, lambda: messagebox.showerror("Error", str(ex)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _tg_get_updates(self):
        token = self.tg_bot_token.get().strip()
        if not token:
            messagebox.showwarning("","Enter bot token first."); return
        def _fetch():
            try:
                url = f"https://api.telegram.org/bot{token}/getUpdates?limit=100"
                req = Request(url, method="GET")
                resp = urlopen(req, timeout=15)
                data = json.loads(resp.read().decode())
                if not data.get("ok"):
                    self.after(0, lambda: messagebox.showwarning("","Failed to fetch updates.")); return
                chat_ids = {}
                for upd in data.get("result",[]):
                    msg = upd.get("message") or upd.get("channel_post") or {}
                    chat = msg.get("chat",{})
                    cid = str(chat.get("id",""))
                    if not cid: continue
                    name = chat.get("title") or chat.get("first_name","")
                    if chat.get("last_name"): name += " " + chat["last_name"]
                    chat_ids[cid] = name.strip()
                if not chat_ids:
                    self.after(0, lambda: messagebox.showinfo("","No chats found. Send a message to the bot first.")); return
                lines = [f"{cid},{name}" if name else cid for cid, name in chat_ids.items()]
                def _insert():
                    existing = self.tg_chat_ids.get("1.0","end").strip()
                    if existing: self.tg_chat_ids.insert("end", "\n")
                    self.tg_chat_ids.insert("end", "\n".join(lines))
                    self._count_tg_ids()
                    self.log(f"Found {len(lines)} Telegram chats from bot updates", "info")
                self.after(0, _insert)
            except Exception as ex:
                self.after(0, lambda: messagebox.showerror("Error", str(ex)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _pg_tg_tools(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "Telegram Tools", "Tools for Telegram campaigns")

        self._tool_section(sc, "Chat ID Tools", [
            ("Clean Chat IDs", self._tool_tg_clean_ids),
            ("Remove Duplicates", self._tool_tg_dedup),
            ("Sort Chat IDs", self._tool_tg_sort),
            ("Shuffle Chat IDs", self._tool_tg_shuffle),
            ("Count Chat IDs", self._tool_tg_count),
            ("Merge ID Lists", self._tool_tg_merge),
            ("Limit ID List", self._tool_tg_limit),
            ("Export Chat IDs", self._tool_tg_export),
        ], T["tg_blue"], expanded=True)

        self._tool_section(sc, "Message Tools", [
            ("Message Spintax Preview", self._tool_tg_spintax),
            ("Character Counter", self._tool_tg_char_count),
            ("Deep Link Generator", self._tool_tg_deeplink),
            ("Bot Command List", self._tool_tg_commands),
            ("Inline Keyboard Builder", self._tool_tg_keyboard),
            ("Message Preview", self._tool_tg_msg_preview),
        ], T["tg_blue"])

        self._tool_section(sc, "Bot Management", [
            ("Get Bot Info", self._tool_tg_bot_info),
            ("Set Bot Commands", self._tool_tg_set_commands),
            ("Get Chat Members Count", self._tool_tg_member_count),
            ("Webhook Status", self._tool_tg_webhook_status),
        ], T["tg_blue"])

    # ── Telegram Chat ID Tools ──
    def _tool_tg_clean_ids(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: return
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        cleaned = []
        for l in lines:
            parts = l.split(",",1)
            cid = parts[0].strip()
            name = parts[1].strip() if len(parts)>1 else ""
            if cid.lstrip("-").isdigit() or cid.startswith("@"):
                cleaned.append(f"{cid},{name}" if name else cid)
        self.tg_chat_ids.delete("1.0","end"); self.tg_chat_ids.insert("1.0","\n".join(cleaned))
        self._count_tg_ids()
        self.log(f"Cleaned: {len(cleaned)} valid chat IDs", "info")

    def _tool_tg_dedup(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: return
        seen = set(); out = []
        for l in raw.splitlines():
            cid = l.strip().split(",")[0].strip()
            if cid and cid not in seen: seen.add(cid); out.append(l.strip())
        before = len(raw.splitlines()); after = len(out)
        self.tg_chat_ids.delete("1.0","end"); self.tg_chat_ids.insert("1.0","\n".join(out))
        self._count_tg_ids()
        self.log(f"Removed {before-after} duplicates, {after} remaining", "info")

    def _tool_tg_sort(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: return
        lines = sorted([l.strip() for l in raw.splitlines() if l.strip()])
        self.tg_chat_ids.delete("1.0","end"); self.tg_chat_ids.insert("1.0","\n".join(lines))
        self.log("Chat IDs sorted", "info")

    def _tool_tg_shuffle(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: return
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        random.shuffle(lines)
        self.tg_chat_ids.delete("1.0","end"); self.tg_chat_ids.insert("1.0","\n".join(lines))
        self.log("Chat IDs shuffled", "info")

    def _tool_tg_count(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        count = len([l for l in raw.splitlines() if l.strip()]) if raw else 0
        messagebox.showinfo("Count", f"Total chat IDs: {count}")

    def _tool_tg_merge(self):
        path = filedialog.askopenfilename(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not path: return
        with open(path,"r",encoding="utf-8",errors="ignore") as f:
            new_lines = [l.strip() for l in f if l.strip()]
        existing = self.tg_chat_ids.get("1.0","end").strip()
        if existing: self.tg_chat_ids.insert("end","\n")
        self.tg_chat_ids.insert("end","\n".join(new_lines))
        self._count_tg_ids()
        self.log(f"Merged {len(new_lines)} IDs from file", "info")

    def _tool_tg_limit(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: return
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        win = ctk.CTkToplevel(self); win.title("Limit"); win.geometry("300x120"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text=f"Current: {len(lines)} IDs. Limit to:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,4))
        inp = ctk.CTkEntry(win, placeholder_text="100", height=34, font=("Segoe UI",12),
                            fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        inp.pack(padx=16, fill="x")
        def _apply():
            try: n = int(inp.get())
            except: return
            self.tg_chat_ids.delete("1.0","end"); self.tg_chat_ids.insert("1.0","\n".join(lines[:n]))
            self._count_tg_ids(); win.destroy()
        ctk.CTkButton(win, text="Apply", fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_apply).pack(padx=16, pady=8, fill="x")

    def _tool_tg_export(self):
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: messagebox.showinfo("","No chat IDs to export."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt"),("CSV","*.csv")])
        if not path: return
        with open(path,"w",encoding="utf-8") as f: f.write(raw)
        self.log(f"Exported Telegram IDs to {path}", "info")

    # ── Telegram Message Tools ──
    def _tool_tg_spintax(self):
        if not hasattr(self,'tg_message'): return
        raw = self.tg_message.get("1.0","end").strip()
        if not raw: messagebox.showinfo("","Write a message first."); return
        results = [spin(raw) for _ in range(5)]
        win = ctk.CTkToplevel(self); win.title("Spintax Preview"); win.geometry("500x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="5 Random Variations:", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(padx=16, pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=12, pady=(0,12))
        for i,r in enumerate(results,1): tb.insert("end", f"--- Variant {i} ---\n{r}\n\n")
        tb.configure(state="disabled")

    def _tool_tg_char_count(self):
        if not hasattr(self,'tg_message'): return
        raw = self.tg_message.get("1.0","end").strip()
        chars = len(raw); words = len(raw.split())
        limit_info = "4096 chars max for text messages" if chars <= 4096 else "WARNING: Exceeds 4096 char limit!"
        messagebox.showinfo("Character Count", f"Characters: {chars}\nWords: {words}\n\n{limit_info}")

    def _tool_tg_deeplink(self):
        win = ctk.CTkToplevel(self); win.title("Deep Link Generator"); win.geometry("460x200"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Generate Telegram Deep Link", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(padx=16, pady=(12,6))
        r = ctk.CTkFrame(win, fg_color="transparent"); r.pack(fill="x", padx=16)
        ctk.CTkLabel(r, text="Bot Username:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        bot_inp = ctk.CTkEntry(r, placeholder_text="mybot", height=32, font=("Segoe UI",12),
                                fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        bot_inp.pack(side="left", fill="x", expand=True, padx=8)
        r2 = ctk.CTkFrame(win, fg_color="transparent"); r2.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(r2, text="Start Param:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        param_inp = ctk.CTkEntry(r2, placeholder_text="ref123", height=32, font=("Segoe UI",12),
                                  fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        param_inp.pack(side="left", fill="x", expand=True, padx=8)
        result_lbl = ctk.CTkLabel(win, text="", font=("Consolas",11), text_color=T["accent"])
        result_lbl.pack(padx=16, pady=4)
        def _gen():
            bot = bot_inp.get().strip().lstrip("@")
            param = param_inp.get().strip()
            link = f"https://t.me/{bot}" + (f"?start={param}" if param else "")
            result_lbl.configure(text=link)
        ctk.CTkButton(win, text="Generate", fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_gen).pack(padx=16, pady=4, fill="x")

    def _tool_tg_commands(self):
        win = ctk.CTkToplevel(self); win.title("Bot Commands"); win.geometry("450x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Bot Command List Builder", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(padx=16, pady=(12,6))
        ctk.CTkLabel(win, text="Format: command - description (one per line)", font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16)
        tb = ctk.CTkTextbox(win, height=150, font=("Consolas",11), fg_color=T["input_bg"],
                             border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=12, pady=8)
        tb.insert("1.0", "start - Start the bot\nhelp - Show help message\nsettings - Open settings\nstatus - Check your status")
        def _set():
            token = self.tg_bot_token.get().strip()
            if not token: messagebox.showwarning("","Enter bot token first."); return
            lines = [l.strip() for l in tb.get("1.0","end").strip().splitlines() if " - " in l]
            cmds = [{"command": l.split(" - ")[0].strip().lstrip("/"), "description": l.split(" - ",1)[1].strip()} for l in lines]
            try:
                data = json.dumps({"commands":cmds}).encode()
                req = Request(f"https://api.telegram.org/bot{token}/setMyCommands",
                              data=data, headers={"Content-Type":"application/json"}, method="POST")
                resp = urlopen(req, timeout=10)
                r = json.loads(resp.read().decode())
                if r.get("ok"): messagebox.showinfo("","Commands set successfully!")
                else: messagebox.showerror("","Failed: " + str(r))
            except Exception as ex: messagebox.showerror("Error", str(ex))
        ctk.CTkButton(win, text="Set Commands on Bot", fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_set).pack(padx=12, pady=(0,12), fill="x")

    def _tool_tg_keyboard(self):
        win = ctk.CTkToplevel(self); win.title("Inline Keyboard Builder"); win.geometry("500x320"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Inline Keyboard Builder", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(padx=16, pady=(12,6))
        ctk.CTkLabel(win, text="One row per line. Buttons separated by | . Format: Text=URL", font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16)
        tb = ctk.CTkTextbox(win, height=120, font=("Consolas",11), fg_color=T["input_bg"],
                             border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=12, pady=8)
        tb.insert("1.0", "Visit Site=https://example.com | Contact=https://t.me/username\nMore Info=https://example.com/info")
        result = ctk.CTkTextbox(win, height=80, font=("Consolas",10), fg_color=T["input_bg"], text_color=T["green"])
        result.pack(fill="x", padx=12, pady=(0,8))
        def _build():
            rows = [l.strip() for l in tb.get("1.0","end").strip().splitlines() if l.strip()]
            keyboard = []
            for row_str in rows:
                row_btns = []
                for btn_str in row_str.split("|"):
                    parts = btn_str.strip().split("=",1)
                    if len(parts)==2:
                        row_btns.append({"text":parts[0].strip(),"url":parts[1].strip()})
                if row_btns: keyboard.append(row_btns)
            j = json.dumps({"inline_keyboard":keyboard}, indent=2)
            result.delete("1.0","end"); result.insert("1.0", j)
        ctk.CTkButton(win, text="Build JSON", fg_color=T["tg_blue"], hover_color=T["tg_blue_h"],
                       command=_build).pack(padx=12, pady=(0,12), fill="x")

    def _tool_tg_msg_preview(self):
        if not hasattr(self,'tg_message'): return
        raw = self.tg_message.get("1.0","end").strip()
        if not raw: messagebox.showinfo("","Write a message first."); return
        v = {"chat_id":"123456789","name":"Test User","date":datetime.now().strftime("%Y-%m-%d"),
             "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
        preview = rv(raw, v)
        win = ctk.CTkToplevel(self); win.title("Message Preview"); win.geometry("460x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Preview (with test variables):", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(padx=16, pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=12, pady=(0,12))
        tb.insert("1.0", preview); tb.configure(state="disabled")

    # ── Telegram Bot Management Tools ──
    def _tool_tg_bot_info(self):
        token = self.tg_bot_token.get().strip()
        if not token: messagebox.showwarning("","Enter bot token first."); return
        def _fetch():
            try:
                req = Request(f"https://api.telegram.org/bot{token}/getMe", method="GET")
                resp = urlopen(req, timeout=10)
                data = json.loads(resp.read().decode())
                if data.get("ok"):
                    bot = data["result"]
                    info = (f"Bot ID: {bot.get('id')}\n"
                            f"Name: {bot.get('first_name','')}\n"
                            f"Username: @{bot.get('username','')}\n"
                            f"Can Join Groups: {bot.get('can_join_groups',False)}\n"
                            f"Can Read Messages: {bot.get('can_read_all_group_messages',False)}\n"
                            f"Supports Inline: {bot.get('supports_inline_queries',False)}")
                    self.after(0, lambda: messagebox.showinfo("Bot Info", info))
                else:
                    self.after(0, lambda: messagebox.showerror("Error", str(data)))
            except Exception as ex:
                self.after(0, lambda: messagebox.showerror("Error", str(ex)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _tool_tg_set_commands(self):
        self._tool_tg_commands()

    def _tool_tg_member_count(self):
        token = self.tg_bot_token.get().strip()
        if not token: messagebox.showwarning("","Enter bot token first."); return
        if not hasattr(self,'tg_chat_ids'): return
        raw = self.tg_chat_ids.get("1.0","end").strip()
        ids = [l.strip().split(",")[0].strip() for l in raw.splitlines() if l.strip()]
        if not ids: messagebox.showwarning("","Add chat IDs first."); return
        def _fetch():
            results = []
            for cid in ids[:20]:
                try:
                    req = Request(f"https://api.telegram.org/bot{token}/getChatMemberCount?chat_id={cid}", method="GET")
                    resp = urlopen(req, timeout=10)
                    data = json.loads(resp.read().decode())
                    if data.get("ok"):
                        results.append(f"{cid}: {data['result']} members")
                    else:
                        results.append(f"{cid}: Error - {data.get('description','unknown')}")
                except Exception as ex:
                    results.append(f"{cid}: Error - {str(ex)[:40]}")
            self.after(0, lambda: messagebox.showinfo("Member Counts", "\n".join(results)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _tool_tg_webhook_status(self):
        token = self.tg_bot_token.get().strip()
        if not token: messagebox.showwarning("","Enter bot token first."); return
        def _fetch():
            try:
                req = Request(f"https://api.telegram.org/bot{token}/getWebhookInfo", method="GET")
                resp = urlopen(req, timeout=10)
                data = json.loads(resp.read().decode())
                if data.get("ok"):
                    wh = data["result"]
                    info = (f"URL: {wh.get('url') or '(not set)'}\n"
                            f"Pending Updates: {wh.get('pending_update_count',0)}\n"
                            f"Last Error: {wh.get('last_error_message','None')}\n"
                            f"Max Connections: {wh.get('max_connections','N/A')}")
                    self.after(0, lambda: messagebox.showinfo("Webhook Status", info))
                else:
                    self.after(0, lambda: messagebox.showerror("Error", str(data)))
            except Exception as ex:
                self.after(0, lambda: messagebox.showerror("Error", str(ex)))
        threading.Thread(target=_fetch, daemon=True).start()

    def _pg_tg_settings(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "Telegram Settings", "Configure Telegram sending behavior")

        c1 = self._card(sc); self._ctitle(c1, "Sending Speed", icon_color=T["tg_blue"])
        r1 = self._frow(c1, pad=16)
        self.tg_delay_min = self._inp(r1, "Delay Min (s)", "1")
        self.tg_delay_max = self._inp(r1, "Delay Max (s)", "3")
        ctk.CTkLabel(c1, text="Telegram Bot API allows ~30 messages/second to different chats",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c2 = self._card(sc); self._ctitle(c2, "Batch Sending", icon_color=T["tg_blue"])
        r2 = self._frow(c2, pad=16)
        self.tg_batch_size = self._inp(r2, "Messages per batch", "25")
        self.tg_batch_pause = self._inp(r2, "Pause between batches (s)", "30")
        ctk.CTkLabel(c2, text="Pause after each batch to avoid rate limits",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c3 = self._card(sc); self._ctitle(c3, "Auto Retry", icon_color=T["tg_blue"])
        self.tg_retry_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c3, text="  Auto-retry failed messages", variable=self.tg_retry_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["tg_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        rf = self._frow(c3, pad=16)
        self.tg_retry_max = self._inp(rf, "Max retries", "3", w=100)
        ctk.CTkFrame(c3, height=8, fg_color="transparent").pack()

        c4 = self._card(sc); self._ctitle(c4, "Rate Limiting", icon_color=T["tg_blue"])
        r4 = self._frow(c4, pad=16)
        self.tg_rate_limit = self._inp(r4, "Max messages per second", "25")
        self.tg_flood_wait_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c4, text="  Auto-wait on Flood Control (429 errors)", variable=self.tg_flood_wait_var,
                        font=("Segoe UI",12), fg_color=T["border"], progress_color=T["tg_blue"],
                        button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkLabel(c4, text="If Telegram returns 429, auto-wait the retry_after duration",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        c5 = self._card(sc); self._ctitle(c5, "Message Options", icon_color=T["tg_blue"])
        self.tg_protect_content_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Protect content (prevent forwarding/saving)", variable=self.tg_protect_content_var,
                        font=("Segoe UI",12), fg_color=T["border"], progress_color=T["tg_blue"],
                        button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.tg_pin_message_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c5, text="  Pin message in chat after sending", variable=self.tg_pin_message_var,
                        font=("Segoe UI",12), fg_color=T["border"], progress_color=T["tg_blue"],
                        button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

        c6 = self._card(sc); self._ctitle(c6, "Notifications", icon_color=T["tg_blue"])
        self.tg_notify_done_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c6, text="  Show notification when batch completes", variable=self.tg_notify_done_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["tg_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.tg_sound_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c6, text="  Play sound on completion", variable=self.tg_sound_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["tg_blue"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

    def open_tg_templates(self):
        self._open_template_manager("telegram", self.tg_message)

    # ═══════════════════════════════════════════════════════════
    #  PAGE: SMTP SERVERS
    # ═══════════════════════════════════════════════════════════
    def _pg_smtp(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=12, pady=8)
        self._ptitle(sc, "SMTP Servers", "Add and manage your SMTP servers")
        tip = ctk.CTkFrame(sc, fg_color=T["card_h"], corner_radius=8, border_width=1, border_color=T["border"])
        tip.pack(fill="x", padx=2, pady=(0,8))
        ctk.CTkLabel(tip, text="Tip: 'Username / Email' is SMTP login, not recipient address.",
                     font=("Segoe UI",11), text_color=T["t2"]).pack(side="left", padx=12, pady=8)
        ctk.CTkButton(tip, text="Go to Compose", height=28, width=110, font=("Segoe UI",11),
                      fg_color=T["card"], hover_color=T["border_l"], border_width=1, border_color=T["border"],
                      command=lambda: self._go_email_tab(0)).pack(side="right", padx=10, pady=6)

        # ── Quick Add from Preset ──
        c1 = self._card(sc); self._ctitle(c1, "Quick Add — Provider Presets", icon_color=T["accent"])
        preset_row = ctk.CTkFrame(c1, fg_color="transparent"); preset_row.pack(fill="x", padx=16, pady=(0,8))
        self.smtp_preset = ctk.CTkComboBox(preset_row, values=list(SMTP_PRESETS.keys()), state="readonly",
            width=320, height=36, font=("Segoe UI",12),
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["accent"],
            dropdown_fg_color=T["card"], dropdown_text_color=T["t1"], dropdown_hover_color=T["card_h"],
            command=self._smtp_preset_changed)
        self.smtp_preset.set("── Cloud / Transactional ──")
        self.smtp_preset.pack(side="left", padx=(0,8))
        ctk.CTkButton(preset_row, text="⚡ Fill", height=36, width=70, font=("Segoe UI",12,"bold"),
                       fg_color=T["accent"], hover_color=T["accent_h"],
                       command=self._smtp_fill_preset).pack(side="left")

        # ── Manual SMTP Form ──
        c2 = self._card(sc); self._ctitle(c2, "Add Single SMTP", icon_color=T["purple"])
        r1 = self._frow(c2, pad=16)
        self.smtp_host = self._inp(r1, "SMTP Host", "smtp.example.com")
        self.smtp_port = self._inp(r1, "Port", "587", w=80)
        ef = ctk.CTkFrame(r1, fg_color="transparent"); ef.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(ef, text="Encryption", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        self.smtp_enc = ctk.CTkComboBox(ef, values=["tls","ssl","none"], state="readonly",
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"],
            dropdown_fg_color=T["card"], height=34)
        self.smtp_enc.set("tls"); self.smtp_enc.pack(fill="x")
        r2 = self._frow(c2, pad=16)
        self.smtp_user = self._inp(r2, "Username / Email", "user@example.com")
        self.smtp_pass = self._inp(r2, "Password / App Password", "password", show="*")
        r3 = self._frow(c2, pad=16)
        self.smtp_test_to = self._inp(r3, "Recipient Email (Test To)", "test@example.com")
        default_test_to = ""
        if hasattr(self, "recipients_box"):
            for ln in self.recipients_box.get("1.0", "end").splitlines():
                em = ln.strip().split(",")[0].strip()
                if is_valid_email(em):
                    default_test_to = em
                    break
        if default_test_to:
            self.smtp_test_to.delete(0, "end")
            self.smtp_test_to.insert(0, default_test_to)
        ctk.CTkLabel(c2, text="Put the email here for 'Send Test Email' (not needed for connection test).",
                     font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=20, pady=(0,4))
        btn_row = ctk.CTkFrame(c2, fg_color="transparent"); btn_row.pack(fill="x", padx=16, pady=(8,12))
        ctk.CTkButton(btn_row, text="➕ Add SMTP", height=38, font=("Segoe UI",13,"bold"),
                       fg_color=T["green"], hover_color=T["green_h"], text_color="#fff",
                       corner_radius=10, command=self._smtp_add).pack(side="left", padx=(0,8))
        ctk.CTkButton(btn_row, text="🧪 Test Connection", height=38, font=("Segoe UI",12),
                       fg_color=T["accent_s"], hover_color=T["accent"], text_color=T["accent"],
                       border_width=1, border_color=T["accent"], corner_radius=10,
                       command=self._smtp_test).pack(side="left", padx=(0,8))
        ctk.CTkButton(btn_row, text="✉ Send Test Email", height=38, font=("Segoe UI",12),
                       fg_color=T["card_h"], hover_color=T["border_l"], border_width=1, border_color=T["border"],
                       corner_radius=10, command=self._smtp_send_test_current).pack(side="left", padx=(0,8))
        self.smtp_test_lbl = ctk.CTkLabel(btn_row, text="", font=("Segoe UI",12))
        self.smtp_test_lbl.pack(side="left", padx=8)

        # ── Bulk Paste ──
        c2p = self._card(sc); self._ctitle(c2p, "Bulk Paste — Add Many SMTP At Once", icon_color=T["orange"])
        ctk.CTkLabel(c2p, text="Paste multiple SMTPs (one per line):  host|port|user|password|encryption",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,4))
        self.smtp_bulk_box = ctk.CTkTextbox(c2p, height=120, font=("Consolas",11), fg_color=T["input_bg"],
                                             border_width=1, border_color=T["input_bd"], corner_radius=8, text_color=T["t1"])
        self.smtp_bulk_box.pack(fill="x", padx=16, pady=(0,8))
        bp_row = ctk.CTkFrame(c2p, fg_color="transparent"); bp_row.pack(fill="x", padx=16, pady=(0,10))
        ctk.CTkButton(bp_row, text="➕ Add All Pasted", height=34, font=("Segoe UI",12,"bold"),
                       fg_color=T["green"], hover_color=T["green_h"], text_color="#fff", corner_radius=8,
                       command=self._smtp_bulk_add).pack(side="left", padx=(0,6))
        ctk.CTkButton(bp_row, text="📂 Import File", height=34, font=("Segoe UI",12),
                       fg_color=T["card_h"], hover_color=T["border_l"], border_width=1,
                       border_color=T["border"], corner_radius=8,
                       command=self._smtp_import_file).pack(side="left", padx=(0,6))
        lbl_sep = ctk.CTkLabel(bp_row, text="Separators: |  ,  ;  tab", font=("Segoe UI",10), text_color=T["t4"])
        lbl_sep.pack(side="left", padx=8)

        # ── Server Actions ──
        c3 = self._card(sc); self._ctitle(c3, "Server Management", icon_color=T["green"])
        self.smtp_count_lbl = ctk.CTkLabel(c3, text="0 servers configured",
                                            font=("Segoe UI",13,"bold"), text_color=T["t1"])
        self.smtp_count_lbl.pack(anchor="w", padx=16, pady=(0,6))
        act = ctk.CTkFrame(c3, fg_color="transparent"); act.pack(fill="x", padx=12, pady=(0,8))
        act.grid_columnconfigure((0,1,2,3,4), weight=1)
        for i,(txt,cmd) in enumerate([
            ("🧪 Test All", self._smtp_test_all),
            ("📤 Export List", self._smtp_export),
            ("🗑 Remove Dead", self._smtp_remove_dead),
            ("🔀 Shuffle Order", self._smtp_shuffle),
            ("🗑 Clear All", self._smtp_clear_all)]):
            ctk.CTkButton(act, text=txt, height=34, font=("Segoe UI",11), fg_color=T["card_h"],
                           hover_color=T["border_l"], border_width=1, border_color=T["border"],
                           corner_radius=8, command=cmd).grid(row=0, column=i, padx=3, pady=3, sticky="ew")
        self.smtp_test_all_lbl = ctk.CTkLabel(c3, text="", font=("Segoe UI",11))
        self.smtp_test_all_lbl.pack(anchor="w", padx=16, pady=(0,4))

        self.smtp_list_frame = ctk.CTkFrame(c3, fg_color="transparent")
        self.smtp_list_frame.pack(fill="x", padx=8, pady=(0,12))
        self._smtp_render_list()

    def _smtp_preset_changed(self, value):
        preset = SMTP_PRESETS.get(value)
        if preset is None: return
        self.smtp_host.delete(0, "end"); self.smtp_host.insert(0, preset["host"])
        self.smtp_port.delete(0, "end"); self.smtp_port.insert(0, preset["port"])
        self.smtp_enc.set(preset["enc"])

    def _smtp_fill_preset(self):
        value = self.smtp_preset.get()
        preset = SMTP_PRESETS.get(value)
        if preset is None: messagebox.showinfo("", "Select a valid provider first."); return
        self.smtp_host.delete(0, "end"); self.smtp_host.insert(0, preset["host"])
        self.smtp_port.delete(0, "end"); self.smtp_port.insert(0, preset["port"])
        self.smtp_enc.set(preset["enc"])

    def _smtp_infer_encryption(self, port):
        p = str(port).strip()
        if p == "465": return "ssl"
        if p in ("25", "587", "2525", "2587"): return "tls"
        return "tls"

    def _smtp_norm_encryption(self, enc, port):
        e = str(enc or "").strip().lower()
        p = str(port).strip()
        aliases = {
            "starttls":"tls", "tlsv1.2":"tls", "tlsv1.3":"tls",
            "smtp_ssl":"ssl", "plain":"none", "off":"none", "no":"none",
            "auto":"", "default":""
        }
        e = aliases.get(e, e)
        if e not in ("tls","ssl","none"): e = ""
        # Common mismatch auto-fix: 587/25/2525 are STARTTLS ports, 465 is SSL.
        if e == "ssl" and p in ("25", "587", "2525", "2587"):
            e = "tls"
        elif e == "tls" and p == "465":
            e = "ssl"
        return e or self._smtp_infer_encryption(port)

    def _smtp_normalize_server(self, srv):
        if not isinstance(srv, dict): return None
        host = str(srv.get("host","")).strip()
        port = str(srv.get("port","")).strip() or "587"
        if not host or not port.isdigit(): return None
        out = {
            "host": host,
            "port": port,
            "username": str(srv.get("username", srv.get("user",""))).strip(),
            "password": str(srv.get("password", srv.get("pass",""))).strip(),
            "encryption": self._smtp_norm_encryption(srv.get("encryption", srv.get("enc","")), port),
        }
        if "_status" in srv: out["_status"] = srv["_status"]
        return out

    def _smtp_normalize_servers(self, servers):
        fixed = []
        for srv in (servers or []):
            n = self._smtp_normalize_server(srv)
            if n: fixed.append(n)
        return fixed

    def _smtp_open_connection(self, srv, timeout=15, helo=None):
        cfg = self._smtp_normalize_server(srv)
        if not cfg: raise ValueError("Invalid SMTP configuration.")
        host, port, enc = cfg["host"], int(cfg["port"]), cfg["encryption"]
        ctx = ssl.create_default_context()
        s = smtplib.SMTP_SSL(host, port, timeout=timeout, context=ctx) if enc == "ssl" else smtplib.SMTP(host, port, timeout=timeout)
        if helo: s.ehlo(helo)
        else: s.ehlo()
        if enc == "tls":
            s.starttls(context=ctx)
            if helo: s.ehlo(helo)
            else: s.ehlo()
        if cfg["username"] and cfg["password"]: s.login(cfg["username"], cfg["password"])
        return s, cfg

    def _smtp_pretty_error(self, ex, cfg=None):
        raw = str(ex).strip()
        low = raw.lower()
        port = str((cfg or {}).get("port", "")).strip()
        enc = str((cfg or {}).get("encryption", "")).strip().lower()

        if "wrong version number" in low:
            if enc == "ssl":
                return "SSL/TLS mismatch: for this server, try TLS (STARTTLS). Common ports: 587 TLS, 465 SSL."
            if enc == "tls":
                return "SSL/TLS mismatch: for this server, try SSL. Common ports: 465 SSL, 587 TLS."
            return "SSL/TLS mismatch. Check encryption type (TLS vs SSL) and port."
        if "starttls extension not supported" in low:
            return "STARTTLS is not supported on this port. Try SSL on 465 or use provider recommended settings."
        if "authentication failed" in low or "5.7.8" in low or "535" in low:
            return "Authentication failed. Check username/password or use App Password."
        if "connection refused" in low or "timed out" in low:
            return "Connection failed. Check host/port and firewall."
        if "name or service not known" in low or "getaddrinfo failed" in low:
            return "SMTP host is invalid or unreachable."
        if enc == "ssl" and port == "587":
            return "Port 587 usually requires TLS, not SSL."
        if enc == "tls" and port == "465":
            return "Port 465 usually requires SSL, not TLS."
        return raw[:200] if raw else "Unknown SMTP error."

    def _smtp_add(self):
        h,po,u,pw,e = self.smtp_host.get().strip(),self.smtp_port.get().strip(),self.smtp_user.get().strip(),self.smtp_pass.get().strip(),self.smtp_enc.get()
        if not h: messagebox.showwarning("","Enter SMTP host."); return
        if not po: messagebox.showwarning("","Enter SMTP port."); return
        if not po.isdigit(): messagebox.showwarning("","SMTP port must be numeric."); return
        srv = self._smtp_normalize_server({"host":h,"port":po,"username":u,"password":pw,"encryption":e})
        if not srv: messagebox.showwarning("","Invalid SMTP settings."); return
        self.smtp_servers.append(srv)
        self._smtp_render_list()
        self.smtp_host.delete(0,"end"); self.smtp_port.delete(0,"end"); self.smtp_port.insert(0,"587")
        self.smtp_user.delete(0,"end"); self.smtp_pass.delete(0,"end"); self.smtp_enc.set("tls")

    def _smtp_parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"): return None
        for sep in ("|", ";", ",", "\t"):
            parts = line.split(sep)
            if len(parts) >= 4: break
        else: return None
        if len(parts) < 4: return None
        h, po = parts[0].strip(), parts[1].strip()
        if not h or not po: return None
        enc = parts[4].strip().lower() if len(parts) > 4 else ""
        return self._smtp_normalize_server({"host":h,"port":po,"username":parts[2].strip(),"password":parts[3].strip(),"encryption":enc})

    def _smtp_bulk_add(self):
        raw = self.smtp_bulk_box.get("1.0","end").strip()
        if not raw: messagebox.showwarning("","Paste SMTP servers first."); return
        added = 0
        for line in raw.splitlines():
            srv = self._smtp_parse_line(line)
            if srv: self.smtp_servers.append(srv); added += 1
        self._smtp_render_list()
        self.smtp_bulk_box.delete("1.0","end")
        messagebox.showinfo("Bulk Add", f"Added {added} SMTP servers.\nTotal: {len(self.smtp_servers)}")

    def _smtp_test(self):
        h,po,u,pw,e = self.smtp_host.get().strip(),self.smtp_port.get().strip(),self.smtp_user.get().strip(),self.smtp_pass.get().strip(),self.smtp_enc.get()
        if not h or not po: self.smtp_test_lbl.configure(text="Fill host & port", text_color=T["red"]); return
        if po == "587" and e == "ssl":
            self.smtp_enc.set("tls")
            self.smtp_test_lbl.configure(text="Auto-fixed: 587 works with TLS (not SSL)", text_color=T["orange"])
            e = "tls"
        elif po == "465" and e == "tls":
            self.smtp_enc.set("ssl")
            self.smtp_test_lbl.configure(text="Auto-fixed: 465 works with SSL (not TLS)", text_color=T["orange"])
            e = "ssl"
        self.smtp_test_lbl.configure(text="Testing...", text_color=T["orange"])
        def _t():
            try:
                s, cfg = self._smtp_open_connection({"host":h,"port":po,"username":u,"password":pw,"encryption":e}, timeout=15)
                s.quit()
                self.after(0, lambda: self.smtp_test_lbl.configure(text="✓ Connection OK!", text_color=T["green"]))
            except Exception as ex:
                hint = self._smtp_pretty_error(ex, {"host":h,"port":po,"username":u,"password":pw,"encryption":e})
                self.after(0, lambda e=hint[:120]: self.smtp_test_lbl.configure(text=f"✗ {e}", text_color=T["red"]))
        threading.Thread(target=_t, daemon=True).start()

    def _smtp_send_test_current(self):
        h,po,u,pw,e = self.smtp_host.get().strip(),self.smtp_port.get().strip(),self.smtp_user.get().strip(),self.smtp_pass.get().strip(),self.smtp_enc.get()
        to_addr = self.smtp_test_to.get().strip() if hasattr(self, "smtp_test_to") else ""
        if not h or not po:
            self.smtp_test_lbl.configure(text="Fill host & port", text_color=T["red"]); return
        if not is_valid_email(to_addr):
            self.smtp_test_lbl.configure(text="Enter valid test recipient email", text_color=T["red"]); return
        self.smtp_test_lbl.configure(text="Sending test email...", text_color=T["orange"])

        def _send():
            try:
                s, cfg = self._smtp_open_connection({"host":h,"port":po,"username":u,"password":pw,"encryption":e}, timeout=20)
                v = {
                    "email": to_addr, "name": "Test",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "random": str(random.randint(10000,99999)),
                    "subject": self.subject_entry.get().strip() or "SMTP Test Email",
                }
                from_addr = rv(self.from_email.get().strip() or cfg["username"] or "no-reply@local", v)
                msg = MIMEMultipart()
                msg["From"] = from_addr
                msg["To"] = to_addr
                msg["Subject"] = f"[TEST] {rv(v['subject'], v)}"
                body = self.body.get("1.0","end").strip() if hasattr(self, "body") else "SMTP test successful."
                ct = self.content_type.get() if hasattr(self, "content_type") else "plain"
                msg.attach(MIMEText(rv(body or "SMTP test successful.", v), "html" if ct == "html" else "plain", "utf-8"))
                s.sendmail(from_addr, [to_addr], msg.as_string())
                s.quit()
                self.after(0, lambda: self.smtp_test_lbl.configure(text="✓ Test email sent", text_color=T["green"]))
            except Exception as ex:
                hint = self._smtp_pretty_error(ex, {"host":h,"port":po,"username":u,"password":pw,"encryption":e})
                self.after(0, lambda e=hint[:120]: self.smtp_test_lbl.configure(text=f"✗ {e}", text_color=T["red"]))

        threading.Thread(target=_send, daemon=True).start()

    def _smtp_import_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt"),("CSV","*.csv"),("All","*.*")])
        if not path: return
        added = 0
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                srv = self._smtp_parse_line(line)
                if srv: self.smtp_servers.append(srv); added += 1
        self._smtp_render_list()
        messagebox.showinfo("Import", f"Imported {added} SMTP servers.\nTotal: {len(self.smtp_servers)}")

    def _smtp_test_all(self):
        if not self.smtp_servers: messagebox.showwarning("","No SMTP servers to test."); return
        self.smtp_servers = self._smtp_normalize_servers(self.smtp_servers)
        total = len(self.smtp_servers)
        self.smtp_test_all_lbl.configure(text=f"Testing {total} servers...", text_color=T["orange"])
        def _run():
            ok, fail, dead = 0, 0, []
            for i, srv in enumerate(self.smtp_servers):
                self.after(0, lambda n=i+1,t=total: self.smtp_test_all_lbl.configure(text=f"Testing {n}/{t}..."))
                try:
                    s, _cfg = self._smtp_open_connection(srv, timeout=10)
                    s.quit(); ok += 1; srv["_status"] = "ok"
                except:
                    fail += 1; dead.append(i); srv["_status"] = "dead"
            self._smtp_dead_indices = dead
            self.after(0, lambda: [
                self.smtp_test_all_lbl.configure(text=f"✓ {ok} OK  •  ✗ {fail} Failed  (Total: {total})",
                    text_color=T["green"] if fail==0 else T["orange"]),
                self._smtp_render_list()])
        threading.Thread(target=_run, daemon=True).start()

    def _smtp_remove_dead(self):
        dead = getattr(self, '_smtp_dead_indices', [])
        if not dead: messagebox.showinfo("","Run 'Test All' first to identify dead servers."); return
        for i in sorted(dead, reverse=True):
            if 0 <= i < len(self.smtp_servers): self.smtp_servers.pop(i)
        self._smtp_dead_indices = []
        self._smtp_render_list()
        messagebox.showinfo("Done", f"Removed {len(dead)} dead servers.\nRemaining: {len(self.smtp_servers)}")

    def _smtp_shuffle(self):
        random.shuffle(self.smtp_servers)
        self._smtp_render_list()

    def _smtp_export(self):
        if not self.smtp_servers: messagebox.showwarning("","No servers to export."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt")])
        if not path: return
        with open(path,"w") as f:
            for srv in self.smtp_servers:
                f.write(f"{srv['host']}|{srv['port']}|{srv['username']}|{srv['password']}|{srv['encryption']}\n")
        messagebox.showinfo("Export", f"Exported {len(self.smtp_servers)} servers to:\n{path}")

    def _smtp_clear_all(self):
        if not self.smtp_servers: return
        if messagebox.askyesno("Confirm", f"Remove all {len(self.smtp_servers)} SMTP servers?"):
            self.smtp_servers.clear(); self._smtp_render_list()

    def _smtp_render_list(self):
        for w in self.smtp_list_frame.winfo_children(): w.destroy()
        n = len(self.smtp_servers)
        self.smtp_count_lbl.configure(text=f"{n} server{'s' if n!=1 else ''} configured" +
            (" — ALL will be used in rotation!" if n > 1 else ""))
        if not self.smtp_servers:
            ctk.CTkLabel(self.smtp_list_frame, text="  No SMTP servers added yet.",
                          font=("Segoe UI",12), text_color=T["t3"]).pack(anchor="w", padx=8, pady=8)
            return
        for i, srv in enumerate(self.smtp_servers):
            rf = ctk.CTkFrame(self.smtp_list_frame, fg_color=T["card_h"], corner_radius=8,
                               border_width=1, border_color=T["border"])
            rf.pack(fill="x", padx=4, pady=2)
            enc_clr = {"ssl":T["green"],"tls":T["accent"],"none":T["orange"]}.get(srv["encryption"],T["t3"])
            st = srv.get("_status","")
            st_clr = T["green"] if st=="ok" else T["red"] if st=="dead" else T["t3"]

            left = ctk.CTkFrame(rf, fg_color="transparent"); left.pack(side="left", fill="x", expand=True, padx=10, pady=6)
            ctk.CTkLabel(left, text=f"#{i+1}", font=("Segoe UI",11,"bold"), text_color=T["t3"], width=30).pack(side="left")
            ctk.CTkLabel(left, text=f"{srv['host']}:{srv['port']}",
                          font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
            ctk.CTkLabel(left, text=f" [{srv['encryption'].upper()}]",
                          font=("Segoe UI",10,"bold"), text_color=enc_clr).pack(side="left", padx=2)
            if srv["username"]:
                ctk.CTkLabel(left, text=f" {srv['username']}", font=("Segoe UI",10), text_color=T["t3"]).pack(side="left")
            if st:
                ctk.CTkLabel(left, text=f"  {'✓' if st=='ok' else '✗'}", font=("Segoe UI",12,"bold"), text_color=st_clr).pack(side="left", padx=4)

            right = ctk.CTkFrame(rf, fg_color="transparent"); right.pack(side="right", padx=6, pady=4)
            ctk.CTkButton(right, text="✕", width=28, height=24, fg_color=T["red_bg"],
                           hover_color=T["red"], text_color=T["red"], font=("Segoe UI",11),
                           command=lambda x=i: self._smtp_remove(x)).pack(side="left", padx=1)

    def _smtp_remove(self, idx):
        if 0 <= idx < len(self.smtp_servers): self.smtp_servers.pop(idx); self._smtp_render_list()

    def _smtp_test_server(self, srv):
        def _t():
            try:
                s, cfg = self._smtp_open_connection(srv, timeout=15)
                s.quit()
                self.after(0, lambda: messagebox.showinfo("SMTP Test", f"✓ {srv['host']}:{srv['port']} — OK!"))
            except Exception as ex:
                hint = self._smtp_pretty_error(ex, srv)
                self.after(0, lambda e=hint: messagebox.showerror("SMTP Test", f"✗ {srv['host']}:{srv['port']}\n\n{e}"))
        threading.Thread(target=_t, daemon=True).start()

    # (Tools page removed — all tools are now inside each channel's "Tools" tab)

    def _pg_settings(self, p):
        sc = ctk.CTkScrollableFrame(p, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=10, pady=6)
        self._ptitle(sc, "Settings", "App appearance & sending configuration")

        # ═══════════════════════════════════════════
        #  APP APPEARANCE — Theme + Language
        # ═══════════════════════════════════════════
        c_app = self._card(sc); self._ctitle(c_app, "Application Appearance", icon_color=T["purple"])

        # ── Theme Selector ──
        th_row = ctk.CTkFrame(c_app, fg_color="transparent"); th_row.pack(fill="x", padx=16, pady=(0,4))
        ctk.CTkLabel(th_row, text="Color Theme", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        self._theme_var = ctk.StringVar(value=self._get_saved_setting("theme","Dark Blue (Default)"))
        theme_combo = ctk.CTkComboBox(th_row, values=list(THEMES.keys()), variable=self._theme_var,
            state="readonly", width=200, height=32, font=("Segoe UI",11),
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["accent"],
            dropdown_fg_color=T["card"], dropdown_text_color=T["t1"], dropdown_hover_color=T["card_h"],
            command=lambda v: self._apply_theme(v))
        theme_combo.pack(side="right")

        # ── Theme Preview ──
        prev_fr = ctk.CTkFrame(c_app, fg_color="transparent"); prev_fr.pack(fill="x", padx=16, pady=(4,4))
        self._theme_preview_frame = prev_fr
        self._draw_theme_previews(prev_fr)

        # ── Language Selector ──
        ln_row = ctk.CTkFrame(c_app, fg_color="transparent"); ln_row.pack(fill="x", padx=16, pady=(6,4))
        ctk.CTkLabel(ln_row, text="Language", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        self._lang_var = ctk.StringVar(value=self._get_saved_setting("language","English"))
        lang_combo = ctk.CTkComboBox(ln_row, values=list(LANGUAGES.keys()), variable=self._lang_var,
            state="readonly", width=200, height=32, font=("Segoe UI",11),
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["accent"],
            dropdown_fg_color=T["card"], dropdown_text_color=T["t1"], dropdown_hover_color=T["card_h"],
            command=lambda v: self._save_setting("language", v))
        lang_combo.pack(side="right")

        ctk.CTkLabel(c_app, text="Theme applies instantly. Language changes take effect after restart.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(2,4))

        # ── Font Size ──
        fs_row = ctk.CTkFrame(c_app, fg_color="transparent"); fs_row.pack(fill="x", padx=16, pady=(2,4))
        ctk.CTkLabel(fs_row, text="UI Font Size", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        self._fontsize_var = ctk.StringVar(value=self._get_saved_setting("font_size","Normal"))
        for val in ["Small","Normal","Large"]:
            ctk.CTkRadioButton(fs_row, text=val, variable=self._fontsize_var, value=val,
                                font=("Segoe UI",11), fg_color=T["accent"],
                                command=lambda: self._save_setting("font_size", self._fontsize_var.get())).pack(side="right", padx=8)

        # ── Window Options ──
        wo_row = ctk.CTkFrame(c_app, fg_color="transparent"); wo_row.pack(fill="x", padx=16, pady=(4,4))
        self._always_top_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(wo_row, text="  Always on top", variable=self._always_top_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"],
                        command=lambda: self.attributes("-topmost", self._always_top_var.get())).pack(side="left")
        self._confirm_exit_var = ctk.BooleanVar(value=self._get_saved_setting("confirm_exit","true")=="true")
        ctk.CTkSwitch(wo_row, text="  Confirm on exit", variable=self._confirm_exit_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"],
                        command=lambda: self._save_setting("confirm_exit", str(self._confirm_exit_var.get()).lower())).pack(side="right")

        # ── Startup ──
        su_row = ctk.CTkFrame(c_app, fg_color="transparent"); su_row.pack(fill="x", padx=16, pady=(4,10))
        self._start_minimized_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(su_row, text="  Start minimized", variable=self._start_minimized_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(side="left")
        self._restore_last_var = ctk.BooleanVar(value=self._get_saved_setting("restore_last","false")=="true")
        ctk.CTkSwitch(su_row, text="  Restore last campaign on start", variable=self._restore_last_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"],
                        command=lambda: self._save_setting("restore_last", str(self._restore_last_var.get()).lower())).pack(side="right")

        c1 = self._card(sc); self._ctitle(c1, "Sending Options")
        r1 = self._frow(c1, pad=16)
        self.delay_min = self._inp(r1, "Delay Min (s)", "0")
        self.delay_max = self._inp(r1, "Delay Max (s)", "0")
        r2 = self._frow(c1, pad=16)
        self.thread_count = self._inp(r2, "Threads", "1")
        ef = ctk.CTkFrame(r2, fg_color="transparent"); ef.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(ef, text="Encoding", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        self.header_enc = ctk.CTkComboBox(ef, values=["UTF-8","Base64","ISO-8859-1"], state="readonly",
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"], dropdown_fg_color=T["card"])
        self.header_enc.set("UTF-8"); self.header_enc.pack(fill="x")
        ctk.CTkFrame(c1, height=8, fg_color="transparent").pack()

        c2 = self._card(sc); self._ctitle(c2, "SMTP Rotation — Use ALL Servers", icon_color=T["green"])
        self.rotate_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c2, text="  Rotate across ALL SMTP servers", variable=self.rotate_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["green"], button_color=T["t1"],
                        command=self._tog_rotate).pack(padx=16, anchor="w", pady=4)
        ctk.CTkLabel(c2, text="When ON: each email uses the next SMTP server in the list (round-robin)",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,4))
        self.epp_frame = ctk.CTkFrame(c2, fg_color="transparent")
        self.epp_frame.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(self.epp_frame, text="Emails per SMTP before switching", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        self.emails_per_smtp = ctk.CTkEntry(self.epp_frame, placeholder_text="1", fg_color=T["input_bg"], border_color=T["input_bd"])
        self.emails_per_smtp.insert(0,"1"); self.emails_per_smtp.pack(fill="x")
        ctk.CTkLabel(self.epp_frame, text="Set to 1 = every email uses a different SMTP (best distribution)",
                      font=("Segoe UI",10), text_color=T["t4"]).pack(anchor="w", pady=(2,0))
        ctk.CTkFrame(c2, height=12, fg_color="transparent").pack()

        c3 = self._card(sc); self._ctitle(c3, "Auto Retry")
        self.retry_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c3, text="  Auto-retry failed", variable=self.retry_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        rf = self._frow(c3, pad=16)
        self.retry_max = self._inp(rf, "Max retries", "3", w=100)
        ctk.CTkFrame(c3, height=12, fg_color="transparent").pack()

        c4 = self._card(sc); self._ctitle(c4, "Proxy")
        self.proxy_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c4, text="  Use proxy", variable=self.proxy_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        pr = self._frow(c4, pad=16)
        ptf = ctk.CTkFrame(pr, fg_color="transparent"); ptf.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(ptf, text="Type", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        self.proxy_type = ctk.CTkComboBox(ptf, values=["SOCKS5","SOCKS4","HTTP"], state="readonly",
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"], dropdown_fg_color=T["card"])
        self.proxy_type.set("SOCKS5"); self.proxy_type.pack(fill="x")
        self.proxy_host = self._inp(pr, "Host", "127.0.0.1")
        self.proxy_port = self._inp(pr, "Port", "1080", w=80)
        pr2 = self._frow(c4, pad=16)
        self.proxy_user = self._inp(pr2, "User", ""); self.proxy_pass = self._inp(pr2, "Pass", "", show="*")
        ctk.CTkFrame(c4, height=12, fg_color="transparent").pack()

        c5 = self._card(sc); self._ctitle(c5, "Custom Email Headers")
        self.headers_box = ctk.CTkTextbox(c5, height=70, font=("Consolas",12), fg_color=T["input_bg"],
                                           border_width=1, border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        self.headers_box.pack(fill="x", padx=16, pady=(0,12))

        # ── Direct MX Sending (UltraMailer-style) ──
        c_mx = self._card(sc); self._ctitle(c_mx, "Direct MX Sending", "Send without SMTP server", T["purple"])
        self.direct_mx_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_mx, text="  Send via Direct MX (bypass SMTP)", variable=self.direct_mx_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["purple"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkLabel(c_mx, text="Sends directly to recipient mail server via MX lookup. No SMTP needed.\nRequires port 25 open. Not recommended for large volumes.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,4))
        mx_r = self._frow(c_mx, pad=16)
        self.helo_domain = self._inp(mx_r, "HELO/EHLO Domain", "mail.yourdomain.com")
        self.return_path = self._inp(mx_r, "Return-Path (Bounce)", "bounce@yourdomain.com")
        ctk.CTkFrame(c_mx, height=8, fg_color="transparent").pack()

        # ── Domain Throttle ──
        c_thr = self._card(sc); self._ctitle(c_thr, "Domain Throttle", "Limit per-domain send rate", T["orange"])
        self.domain_throttle_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_thr, text="  Enable domain-based throttle", variable=self.domain_throttle_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["orange"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        thr_r = self._frow(c_thr, pad=16)
        self.max_per_domain = self._inp(thr_r, "Max emails/domain/hour", "50")
        self.domain_pause = self._inp(thr_r, "Pause (s) after limit", "300")
        ctk.CTkLabel(c_thr, text="Prevents rate-limiting by Gmail, Outlook, Yahoo etc.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Auto Text Version ──
        c_at = self._card(sc); self._ctitle(c_at, "Auto Multipart MIME", "HTML + Plain Text", T["accent"])
        self.auto_text_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_at, text="  Auto-generate text version from HTML", variable=self.auto_text_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkLabel(c_at, text="Adds both HTML and plain-text parts. Improves deliverability.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Header Randomizer ──
        c_hr = self._card(sc); self._ctitle(c_hr, "Header Randomization", "Avoid fingerprinting", T["cyan"])
        self.rand_msgid_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_hr, text="  Randomize Message-ID domain", variable=self.rand_msgid_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["cyan"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.rand_xmailer_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_hr, text="  Randomize X-Mailer header", variable=self.rand_xmailer_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["cyan"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.rand_boundary_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_hr, text="  Randomize MIME boundary", variable=self.rand_boundary_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["cyan"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.rand_date_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_hr, text="  Add random seconds to Date header", variable=self.rand_date_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["cyan"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkFrame(c_hr, height=8, fg_color="transparent").pack()

        # ── Encoding Options ──
        c_enc = self._card(sc); self._ctitle(c_enc, "Encoding & MIME", icon_color=T["accent"])
        enc_r = self._frow(c_enc, pad=16)
        ef2 = ctk.CTkFrame(enc_r, fg_color="transparent"); ef2.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(ef2, text="Content-Transfer-Encoding", font=("Segoe UI",10), text_color=T["t2"]).pack(anchor="w")
        self.transfer_enc = ctk.CTkComboBox(ef2, values=["quoted-printable","base64","7bit","8bit"], state="readonly",
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"], dropdown_fg_color=T["card"])
        self.transfer_enc.set("quoted-printable"); self.transfer_enc.pack(fill="x")
        ef3 = ctk.CTkFrame(enc_r, fg_color="transparent"); ef3.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(ef3, text="X-Priority", font=("Segoe UI",10), text_color=T["t2"]).pack(anchor="w")
        self.x_priority = ctk.CTkComboBox(ef3, values=["None","1 (Highest)","2 (High)","3 (Normal)","4 (Low)","5 (Lowest)"], state="readonly",
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"], dropdown_fg_color=T["card"])
        self.x_priority.set("None"); self.x_priority.pack(fill="x")
        ctk.CTkFrame(c_enc, height=8, fg_color="transparent").pack()

        # ── Connection ──
        c_conn = self._card(sc); self._ctitle(c_conn, "Connection", icon_color=T["accent"])
        conn_r = self._frow(c_conn, pad=16)
        self.smtp_timeout = self._inp(conn_r, "SMTP Timeout (s)", "30")
        self.smtp_max_connections = self._inp(conn_r, "Max simultaneous connections", "5")
        conn_r2 = self._frow(c_conn, pad=16)
        self.send_rate_limit = self._inp(conn_r2, "Max emails per minute", "0")
        self.smtp_keepalive_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_conn, text="  Keep SMTP connection alive between emails", variable=self.smtp_keepalive_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkLabel(c_conn, text="Rate limit 0 = unlimited. Keep-alive reuses connection for faster sending.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Batch Sending ──
        c_batch = self._card(sc); self._ctitle(c_batch, "Batch Sending", icon_color=T["orange"])
        self.batch_enabled_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_batch, text="  Enable batch mode", variable=self.batch_enabled_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["orange"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        batch_r = self._frow(c_batch, pad=16)
        self.batch_size = self._inp(batch_r, "Emails per batch", "100")
        self.batch_pause = self._inp(batch_r, "Pause between batches (s)", "60")
        ctk.CTkLabel(c_batch, text="Pause after each batch to cool down SMTP servers.",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=16, pady=(0,8))

        # ── Auto BCC / Read Receipt ──
        c_misc = self._card(sc); self._ctitle(c_misc, "Email Options", icon_color=T["accent"])
        misc_r = self._frow(c_misc, pad=16)
        self.auto_bcc = self._inp(misc_r, "Auto BCC (always BCC to)", "")
        self.default_content_type_var = ctk.StringVar(value="html")
        dt_f = ctk.CTkFrame(misc_r, fg_color="transparent"); dt_f.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(dt_f, text="Default Content Type", font=("Segoe UI",11), text_color=T["t2"]).pack(anchor="w")
        dt_combo = ctk.CTkComboBox(dt_f, values=["html","text"], state="readonly", variable=self.default_content_type_var,
            fg_color=T["input_bg"], border_color=T["input_bd"], button_color=T["border_l"], dropdown_fg_color=T["card"], height=34)
        dt_combo.pack(fill="x")
        self.read_receipt_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_misc, text="  Request read receipt (Disposition-Notification-To)", variable=self.read_receipt_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.track_opens_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_misc, text="  Add open tracking pixel", variable=self.track_opens_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkFrame(c_misc, height=8, fg_color="transparent").pack()

        # ── Notifications ──
        c_notif = self._card(sc); self._ctitle(c_notif, "Notifications", icon_color=T["green"])
        self.email_notify_done_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(c_notif, text="  Show notification when sending completes", variable=self.email_notify_done_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.email_sound_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_notif, text="  Play sound on completion", variable=self.email_sound_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        self.auto_save_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_notif, text="  Auto-save campaign every 5 minutes", variable=self.auto_save_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["green"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=(4,10))

        # ── Log Options ──
        c_log = self._card(sc); self._ctitle(c_log, "Logging", icon_color=T["accent"])
        lf = ctk.CTkFrame(c_log, fg_color="transparent"); lf.pack(fill="x", padx=16, pady=(0,4))
        ctk.CTkLabel(lf, text="Log Level", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        self.log_level_var = ctk.StringVar(value="normal")
        for val, lbl in [("minimal","Minimal"),("normal","Normal"),("verbose","Verbose")]:
            ctk.CTkRadioButton(lf, text=lbl, variable=self.log_level_var, value=val,
                                font=("Segoe UI",11), fg_color=T["accent"]).pack(side="right", padx=8)
        self.log_to_file_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(c_log, text="  Save log to file automatically", variable=self.log_to_file_var, font=("Segoe UI",12),
                        fg_color=T["border"], progress_color=T["accent"], button_color=T["t1"]).pack(padx=16, anchor="w", pady=4)
        ctk.CTkFrame(c_log, height=8, fg_color="transparent").pack()

    # ── Settings Helpers ──
    def _get_saved_setting(self, key, default=""):
        cfg = os.path.join(DATA_DIR, "app_settings.json")
        if os.path.exists(cfg):
            try:
                with open(cfg, "r") as f: return json.load(f).get(key, default)
            except: pass
        return default

    def _save_setting(self, key, value):
        cfg = os.path.join(DATA_DIR, "app_settings.json")
        data = {}
        if os.path.exists(cfg):
            try:
                with open(cfg, "r") as f: data = json.load(f)
            except: pass
        data[key] = value
        with open(cfg, "w") as f: json.dump(data, f, indent=2)

    def _draw_theme_previews(self, parent):
        for w in parent.winfo_children(): w.destroy()
        for name, colors in THEMES.items():
            fr = ctk.CTkFrame(parent, width=50, height=28, corner_radius=6,
                               fg_color=colors["card"], border_width=2,
                               border_color=T["accent"] if name == self._theme_var.get() else colors["border"])
            fr.pack(side="left", padx=2, pady=2); fr.pack_propagate(False)
            inner = ctk.CTkFrame(fr, fg_color="transparent"); inner.pack(expand=True)
            dot = ctk.CTkFrame(inner, width=8, height=8, corner_radius=4, fg_color=colors["accent"])
            dot.pack(side="left", padx=1)
            ctk.CTkLabel(inner, text="A", font=("Segoe UI",9), text_color=colors["t1"]).pack(side="left", padx=1)
            fr.bind("<Button-1>", lambda e, n=name: [self._theme_var.set(n), self._apply_theme(n)])
            for ch in fr.winfo_children():
                ch.bind("<Button-1>", lambda e, n=name: [self._theme_var.set(n), self._apply_theme(n)])
                for ch2 in ch.winfo_children():
                    ch2.bind("<Button-1>", lambda e, n=name: [self._theme_var.set(n), self._apply_theme(n)])

    def _apply_theme(self, theme_name):
        global T
        base = dict(THEMES.get(theme_name, THEMES["Dark Blue (Default)"]))
        base.update(_shared_colors)
        T.clear(); T.update(base)
        self._save_setting("theme", theme_name)

        self.configure(fg_color=T["bg"])
        if hasattr(self, '_theme_preview_frame'):
            self._draw_theme_previews(self._theme_preview_frame)

        messagebox.showinfo("Theme Changed",
            f"Theme set to: {theme_name}\n\nRestart the app for full effect.\n(Some elements update immediately)")

    def _pg_log(self, p):
        self._ptitle(p, "Activity Log", "Real-time sending progress")
        pc = ctk.CTkFrame(p, fg_color=T["card"], corner_radius=8)
        pc.pack(fill="x", padx=10, pady=(0,6))
        self.progress_bar = ctk.CTkProgressBar(pc, height=10, corner_radius=5, fg_color=T["input_bg"], progress_color=T["accent"])
        self.progress_bar.set(0); self.progress_bar.pack(fill="x", padx=16, pady=(14,6))
        sr = ctk.CTkFrame(pc, fg_color="transparent"); sr.pack(fill="x", padx=16, pady=(0,12))
        self.prog_lbl = ctk.CTkLabel(sr, text="0 / 0  (0%)", font=("Segoe UI Semibold",12), text_color=T["t1"]); self.prog_lbl.pack(side="left")
        self.speed_lbl = ctk.CTkLabel(sr, text="Speed: --  ETA: --", font=("Segoe UI",11), text_color=T["t3"]); self.speed_lbl.pack(side="right")
        self.log_box = ctk.CTkTextbox(p, font=("Consolas",10), fg_color=T["bg"],
                                       corner_radius=6, state="disabled", text_color=T["t2"])
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0,6))
        for tag, clr in [("sent",T["green"]),("failed",T["red"]),("info",T["accent"]),("warn",T["orange"]),("retry",T["pink"]),("wa",T["wa_green"]),("sms",T["sms_blue"]),("tg",T["tg_blue"])]:
            self.log_box.tag_config(tag, foreground=clr)

    # ── UI HELPERS ───────────────────────────────────────────
    def _ptitle(self, p, t, s=""):
        ctk.CTkLabel(p, text=t, font=("Segoe UI Semibold",18), text_color=T["t1"]).pack(anchor="w", padx=4, pady=(6,0))
        if s: ctk.CTkLabel(p, text=s, font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=4, pady=(0,10))
    def _card(self, p, show=True):
        c = ctk.CTkFrame(p, fg_color=T["card"], corner_radius=8)
        if show: c.pack(fill="x", pady=3); return c
    def _ctitle(self, c, t, sub="", icon_color=None):
        f = ctk.CTkFrame(c, fg_color="transparent"); f.pack(fill="x", padx=14, pady=(10,6))
        if icon_color:
            ctk.CTkFrame(f, width=6, height=6, corner_radius=3, fg_color=icon_color).pack(side="left", padx=(0,8))
        ctk.CTkLabel(f, text=t, font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
        if sub: ctk.CTkLabel(f, text=f"  {sub}", font=("Segoe UI",10), text_color=T["t3"]).pack(side="left")
    def _frow(self, p, pad=0):
        r = ctk.CTkFrame(p, fg_color="transparent"); r.pack(fill="x", padx=pad, pady=2); return r
    def _inp(self, p, label, ph, w=None, show=None):
        f = ctk.CTkFrame(p, fg_color="transparent"); f.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(f, text=label, font=("Segoe UI",10), text_color=T["t2"]).pack(anchor="w")
        kw = {"placeholder_text":ph,"fg_color":T["input_bg"],"border_color":T["input_bd"],
              "font":("Segoe UI",12),"corner_radius":6,"height":32,"text_color":T["t1"]}
        if w: kw["width"]=w
        if show: kw["show"]=show
        e = ctk.CTkEntry(f, **kw); e.pack(fill="x"); return e
    def _tag(self, p, t, cmd):
        ctk.CTkButton(p, text=t, height=24, font=("Segoe UI",10), fg_color=T["accent_s"],
                       hover_color=T["accent"], text_color=T["accent_l"], corner_radius=10,
                       command=cmd).pack(side="left", padx=2)

    # ── Toggle helpers ───────────────────────────────────────
    def _wa_toggle(self):
        mode = self.wa_mode.get()
        self.wa_web_frame.pack_forget()
        self.wa_biz_frame.pack_forget()
        self.wa_custom_frame.pack_forget()
        if mode == "web":
            self.wa_web_frame.pack(fill="x")
        elif mode == "business":
            self.wa_biz_frame.pack(fill="x")
        else:
            self.wa_custom_frame.pack(fill="x")

    # ── WhatsApp Web: Connect / Disconnect / Sending ──

    def _wa_web_connect(self):
        if not HAS_SELENIUM:
            messagebox.showerror("Missing Library",
                "selenium is not installed.\nRun:\n  pip install selenium webdriver-manager")
            return
        if self.wa_connected and self.wa_driver:
            messagebox.showinfo("","Already connected!")
            return
        self.wa_status_lbl.configure(text="  Opening Chrome...")
        self.wa_status_dot.configure(text_color="#FFA500")
        threading.Thread(target=self._wa_web_connect_thread, daemon=True).start()

    def _wa_web_connect_thread(self):
        try:
            options = webdriver.ChromeOptions()
            wa_data_dir = os.path.join(os.path.expanduser("~"), ".omnisend_pro_wa")
            os.makedirs(wa_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={wa_data_dir}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            if HAS_WDM:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)

            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })

            driver.get("https://web.whatsapp.com")
            self.wa_driver = driver

            self.after(0, lambda: self.wa_status_lbl.configure(text="  Scan QR code with your phone..."))
            self.after(0, lambda: self.wa_status_dot.configure(text_color="#FFA500"))
            self.after(0, lambda: self.log("📱 WhatsApp Web opened — Scan the QR code now!", "wa"))

            logged_in = False
            for _ in range(240):
                try:
                    els = driver.find_elements(By.CSS_SELECTOR,
                        'div[contenteditable="true"][data-tab="3"], '
                        'div[data-testid="chat-list"], '
                        'span[data-testid="default-user"], '
                        'div[aria-label="Search input textbox"], '
                        'header span[data-icon="menu"]')
                    if els:
                        logged_in = True; break
                except: pass
                time.sleep(0.5)

            if not logged_in:
                raise Exception("QR scan timeout (2 min). Try again.")

            time.sleep(2)
            self.wa_connected = True
            self.after(0, lambda: self.wa_status_lbl.configure(text="  Connected! Ready to send"))
            self.after(0, lambda: self.wa_status_dot.configure(text_color=T["wa_green"]))
            self.after(0, lambda: self.log("✓ WhatsApp Web connected! You can send messages now.", "wa"))

        except Exception as ex:
            self.wa_connected = False
            err = str(ex)
            if "timeout" in err.lower() or "TimeoutException" in err:
                err = "QR scan timeout (2 min). Try again."
            self.after(0, lambda: self.wa_status_lbl.configure(text=f"  Connection failed"))
            self.after(0, lambda: self.wa_status_dot.configure(text_color=T["red"]))
            self.after(0, lambda e=err: self.log(f"✗ WhatsApp Web: {e}", "failed"))
            try:
                if self.wa_driver: self.wa_driver.quit()
            except: pass
            self.wa_driver = None

    def _wa_web_disconnect(self):
        try:
            if self.wa_driver: self.wa_driver.quit()
        except: pass
        self.wa_driver = None
        self.wa_connected = False
        self.wa_status_lbl.configure(text="  Disconnected")
        self.wa_status_dot.configure(text_color=T["red"])
        self.log("🔌 WhatsApp Web disconnected", "info")

    def _wa_web_send_message(self, phone, message):
        if not self.wa_driver or not self.wa_connected:
            raise Exception("WhatsApp Web not connected")

        encoded_msg = quote(message)
        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
        self.wa_driver.get(url)
        time.sleep(3)

        for _ in range(3):
            try:
                err_popup = self.wa_driver.find_elements(By.XPATH,
                    "//*[contains(text(),'Phone number shared via url is invalid')]"
                    "|//*[contains(text(),'phone number is not')]"
                    "|//*[contains(text(),'number is invalid')]"
                    "|//*[contains(text(),'numéro de téléphone')]")
                if err_popup:
                    try:
                        ok_btn = self.wa_driver.find_element(By.XPATH, "//div[@role='button' and contains(text(),'OK')]")
                        ok_btn.click(); time.sleep(0.5)
                    except: pass
                    raise Exception(f"Invalid number: {phone}")
            except Exception as ex:
                if "Invalid number" in str(ex): raise
                break

        send_btn = WebDriverWait(self.wa_driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                'span[data-icon="send"], button[aria-label="Send"], span[data-icon="msg-send"]'))
        )
        time.sleep(0.3)
        try:
            send_btn.click()
        except:
            self.wa_driver.execute_script("arguments[0].click();", send_btn)

        time.sleep(2)

        for _ in range(5):
            try:
                ticks = self.wa_driver.find_elements(By.CSS_SELECTOR,
                    'span[data-icon="msg-check"], span[data-icon="msg-dblcheck"], '
                    'span[data-icon="msg-dblcheck-ack"], span[aria-label*="Delivered"], '
                    'span[aria-label*="Read"], span[aria-label*="Sent"]')
                if ticks: break
            except: pass
            time.sleep(0.5)

    # ── Telegram Web: Connect / Disconnect / Sending (Selenium) ──

    def _tg_web_connect(self):
        if not HAS_SELENIUM:
            messagebox.showerror("Missing Library",
                "selenium is not installed.\nRun:\n  pip install selenium webdriver-manager")
            return
        if self.tg_web_connected and self.tg_web_driver:
            messagebox.showinfo("","Already connected!"); return
        self.tg_web_status_lbl.configure(text="  Opening Chrome...")
        self.tg_web_status_dot.configure(text_color="#FFA500")
        threading.Thread(target=self._tg_web_connect_thread, daemon=True).start()

    def _tg_web_connect_thread(self):
        try:
            options = webdriver.ChromeOptions()
            tg_data_dir = os.path.join(os.path.expanduser("~"), ".omnisend_pro_tg")
            os.makedirs(tg_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={tg_data_dir}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            if HAS_WDM:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)

            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })

            driver.get("https://web.telegram.org/a/")
            self.tg_web_driver = driver

            self.after(0, lambda: self.tg_web_status_lbl.configure(text="  Scan QR code with Telegram app..."))
            self.after(0, lambda: self.tg_web_status_dot.configure(text_color="#FFA500"))
            self.after(0, lambda: self.log("Telegram Web opened — Scan the QR code now!", "tg"))

            logged_in = False
            for _ in range(300):
                try:
                    els = driver.find_elements(By.CSS_SELECTOR,
                        '#search-input, '
                        'input[type="text"][placeholder*="Search"], '
                        '.chat-list, '
                        'div.ChatList, '
                        'a.chat-item, '
                        'div[class*="LeftColumn"], '
                        'button[aria-label*="Menu"], '
                        'button[aria-label*="menu"], '
                        'div[class*="ChatFolders"], '
                        'div[id="LeftColumn"]')
                    if els:
                        logged_in = True; break
                except: pass
                time.sleep(0.5)

            if not logged_in:
                raise Exception("QR scan timeout (2.5 min). Try again.")

            time.sleep(2)
            self.tg_web_connected = True
            self.after(0, lambda: self.tg_web_status_lbl.configure(text="  Connected! Ready to send"))
            self.after(0, lambda: self.tg_web_status_dot.configure(text_color=T["green"]))
            self.after(0, lambda: self.log("Telegram Web connected! You can send messages now.", "tg"))

        except Exception as ex:
            self.tg_web_connected = False
            err = str(ex)
            self.after(0, lambda: self.tg_web_status_lbl.configure(text="  Connection failed"))
            self.after(0, lambda: self.tg_web_status_dot.configure(text_color=T["red"]))
            self.after(0, lambda e=err: self.log(f"Telegram Web error: {e}", "failed"))
            try:
                if self.tg_web_driver: self.tg_web_driver.quit()
            except: pass
            self.tg_web_driver = None

    def _tg_web_disconnect(self):
        try:
            if self.tg_web_driver: self.tg_web_driver.quit()
        except: pass
        self.tg_web_driver = None
        self.tg_web_connected = False
        self.tg_web_status_lbl.configure(text="  Disconnected")
        self.tg_web_status_dot.configure(text_color=T["red"])
        self.log("Telegram Web disconnected", "info")

    def _tg_web_search_and_open_chat(self, driver, target):
        search = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                '#search-input, '
                'input[type="text"][placeholder*="Search"], '
                'input[type="text"][dir="auto"], '
                'div[contenteditable="true"][class*="input-search"]'))
        )
        search.click(); time.sleep(0.3)

        if hasattr(search, 'tag_name') and search.tag_name == 'div':
            search.send_keys(Keys.CONTROL + "a")
            search.send_keys(Keys.DELETE)
            search.send_keys(target)
        else:
            search.clear()
            search.send_keys(target)
        time.sleep(2)

        chat_selectors = [
            f'a[href*="#{target}"]',
            'div.search-result-message', 'div.ListItem', 'li.search-result',
            'a.chat-item', 'div.ChatInfo', 'div[class*="ListItem"]',
            'div.search-result', 'a.Row'
        ]
        chat = None
        for sel in chat_selectors:
            try:
                results = driver.find_elements(By.CSS_SELECTOR, sel)
                if results:
                    chat = results[0]; break
            except: pass

        if not chat:
            try:
                results = driver.find_elements(By.XPATH,
                    f'//*[contains(@class,"search")]//a | '
                    f'//*[contains(@class,"ListItem")] | '
                    f'//*[contains(@class,"chatlist")]//a')
                if results:
                    chat = results[0]
            except: pass

        if not chat:
            raise Exception(f"Chat not found: {target}")

        try:
            chat.click()
        except:
            driver.execute_script("arguments[0].click();", chat)
        time.sleep(1.5)

    def _tg_web_send_message(self, target, message):
        if not self.tg_web_driver or not self.tg_web_connected:
            raise Exception("Telegram Web not connected")

        driver = self.tg_web_driver

        self._tg_web_search_and_open_chat(driver, target)

        msg_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                'div[contenteditable="true"][class*="input-message"], '
                'div.input-message-input[contenteditable="true"], '
                'div[id="editable-message-text"], '
                'div[contenteditable="true"][dir="auto"]'))
        )
        msg_box.click(); time.sleep(0.3)

        for line in message.split("\n"):
            msg_box.send_keys(line)
            msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
        time.sleep(0.3)

        send_btn = None
        send_selectors = [
            'button.send', 'button[class*="send"]', 'button[aria-label="Send"]',
            'button[aria-label="Send Message"]', 'div.send-button',
            'button.Button.send'
        ]
        for sel in send_selectors:
            try:
                btns = driver.find_elements(By.CSS_SELECTOR, sel)
                if btns:
                    send_btn = btns[0]; break
            except: pass

        if not send_btn:
            msg_box.send_keys(Keys.ENTER)
        else:
            try: send_btn.click()
            except: driver.execute_script("arguments[0].click();", send_btn)

        time.sleep(1.5)

    def _sms_toggle(self):
        if self.sms_mode.get() == "twilio":
            self.sms_twilio_frame.pack(fill="x"); self.sms_custom_frame.pack_forget()
        else:
            self.sms_custom_frame.pack(fill="x"); self.sms_twilio_frame.pack_forget()

    def _wa_ivar(self, v): self.wa_message.insert("insert", v)
    def _sms_ivar(self, v): self.sms_message.insert("insert", v)
    def _ivar(self, v):
        f = self.focus_get()
        if isinstance(f, ctk.CTkTextbox): f.insert("insert", v)
        elif isinstance(f, ctk.CTkEntry): f.insert(tk.END, v)
        else: self.body.insert("insert", v)

    def _tog_rotate(self):
        if self.rotate_var.get(): self.epp_frame.pack(fill="x", padx=16, pady=4)
        else: self.epp_frame.pack_forget()

    def _count_phones(self, tb, lbl):
        c = len([l for l in tb.get("1.0","end").strip().splitlines() if l.strip() and len(re.sub(r"[^\d+]","",l.split(",")[0]))>=8])
        lbl.configure(text=f"{c} numbers")

    def _import_phones(self, tb, lbl):
        path = filedialog.askopenfilename(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not path: return
        with open(path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
        existing = tb.get("1.0","end").strip()
        if existing: tb.insert("end", "\n" + content.strip())
        else: tb.delete("1.0","end"); tb.insert("1.0", content.strip())
        self._count_phones(tb, lbl)

    def _update_email_count(self):
        c = len([l for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip() and "@" in l])
        self.email_count.configure(text=f"{c} recipients")

    # ═══════════════════════════════════════════════════════════
    #  SMTP / ATTACHMENTS / RECIPIENTS (email)
    # ═══════════════════════════════════════════════════════════
    def show_smtp_form(self): self._go_email_tab(1)
    def cancel_smtp(self): pass
    def add_attachment(self):
        for f in filedialog.askopenfilenames(): self.attachments.append({"filename":os.path.basename(f),"path":f})
        self._ratt()
    def _ratt(self):
        for w in self.att_frame.winfo_children(): w.destroy()
        for i,a in enumerate(self.attachments):
            r = ctk.CTkFrame(self.att_frame, fg_color=T["card_h"], corner_radius=6); r.pack(fill="x", pady=1)
            ctk.CTkLabel(r, text=f"📄 {a['filename']}", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left", padx=8, pady=5)
            ctk.CTkButton(r, text="✕", width=26, height=22, fg_color=T["red_bg"], hover_color=T["red"], text_color=T["red"],
                           command=lambda x=i:[self.attachments.pop(x),self._ratt()]).pack(side="right", padx=6, pady=5)
    def import_recipients(self):
        path = filedialog.askopenfilename(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not path: return
        with open(path,"r",encoding="utf-8",errors="ignore") as f: content = f.read()
        recs = []
        if os.path.splitext(path)[1].lower() == ".csv":
            for row in csv.reader(content.splitlines()):
                if row and re.match(r"[^@]+@[^@]+\.[^@]+", row[0].strip()):
                    recs.append(f"{row[0].strip()},{row[1].strip()}" if len(row)>1 else row[0].strip())
        else:
            for r in parse_emails(content): recs.append(f"{r['email']},{r['name']}" if r["name"] else r["email"])
        existing = self.recipients_box.get("1.0","end").strip()
        if existing: self.recipients_box.insert("end", "\n"+"\n".join(recs))
        else: self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0", "\n".join(recs))
        self._update_email_count()
    def clear_recipients(self): self.recipients_box.delete("1.0","end"); self._update_email_count()

    # ═══════════════════════════════════════════════════════════
    #  TOOLS (list)
    # ═══════════════════════════════════════════════════════════
    def _lines(self): return [l.strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip()]
    def _setl(self, lines): self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0","\n".join(lines)); self._update_email_count()
    def _tool_dedup(self):
        lines=self._lines(); seen,out=set(),[]
        for l in lines:
            k=l.split(",")[0].lower()
            if k not in seen: seen.add(k); out.append(l)
        self._setl(out); messagebox.showinfo("Done",f"Removed {len(lines)-len(out)} dupes.")
    def _tool_validate(self):
        lines=self._lines(); ok=[l for l in lines if is_valid_email(l.split(",")[0].strip())]
        self._setl(ok); messagebox.showinfo("Done",f"Removed {len(lines)-len(ok)} invalid.")
    def _tool_shuffle(self): lines=self._lines(); random.shuffle(lines); self._setl(lines)
    def _tool_sort(self): lines=self._lines(); lines.sort(key=lambda l:l.split(",")[0].lower()); self._setl(lines)
    def _tool_domains(self):
        d={}
        for l in self._lines(): e=l.split(",")[0].strip(); dom=e.split("@")[-1].lower() if "@" in e else "?"; d[dom]=d.get(dom,0)+1
        messagebox.showinfo("Domains","\n".join(f"  {k}: {v}" for k,v in sorted(d.items(), key=lambda x:-x[1])[:25]))
    def _tool_split(self):
        lines,d=self._lines(),{}
        for l in lines: e=l.split(",")[0].strip(); dom=e.split("@")[-1].lower() if "@" in e else "other"; d.setdefault(dom,[]).append(l)
        out=filedialog.askdirectory()
        if not out: return
        for dom,emails in d.items():
            with open(os.path.join(out, re.sub(r"[^\w.]","_",dom)+".txt"),"w") as f: f.write("\n".join(emails))
        messagebox.showinfo("Done",f"Split into {len(d)} files.")

    def _tool_merge_lists(self):
        paths = filedialog.askopenfilenames(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not paths: return
        merged = []
        for p in paths:
            with open(p,"r",encoding="utf-8",errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and "@" in line: merged.append(line)
        existing = self._lines()
        combined = existing + merged
        seen, out = set(), []
        for l in combined:
            k = l.split(",")[0].strip().lower()
            if k not in seen: seen.add(k); out.append(l)
        self._setl(out)
        messagebox.showinfo("Merge", f"Merged {len(paths)} files.\nAdded {len(out)-len(existing)} new emails.\nTotal: {len(out)}")

    def _tool_extract_emails(self):
        win = ctk.CTkToplevel(self); win.title("Extract Emails"); win.geometry("600x450"); win.transient(self)
        ctk.CTkLabel(win, text="📋 Paste any text — emails will be extracted", font=("Segoe UI Semibold",14)).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, height=250, font=("Consolas",12), fg_color=T["input_bg"]); tb.pack(fill="x", padx=16, pady=4)
        rl = ctk.CTkLabel(win, text="", font=("Segoe UI",12)); rl.pack(pady=4)
        def do():
            raw = tb.get("1.0","end")
            found = list(set(re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', raw)))
            if not found: rl.configure(text="No emails found.", text_color=T["red"]); return
            existing = self.recipients_box.get("1.0","end").strip()
            if existing: self.recipients_box.insert("end", "\n"+"\n".join(found))
            else: self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0","\n".join(found))
            self._update_email_count()
            rl.configure(text=f"✓ Extracted {len(found)} emails!", text_color=T["green"])
        ctk.CTkButton(win, text="Extract & Add to List", height=38, fg_color=T["green"],
                       hover_color=T["green_h"], font=("Segoe UI",13,"bold"), command=do).pack(pady=8)

    def _tool_filter_domain(self):
        win = ctk.CTkToplevel(self); win.title("Filter by Domain"); win.geometry("400x200"); win.transient(self)
        ctk.CTkLabel(win, text="Enter domain to keep (e.g. gmail.com)", font=("Segoe UI",13)).pack(pady=(16,6))
        de = ctk.CTkEntry(win, width=300, placeholder_text="gmail.com", fg_color=T["input_bg"]); de.pack()
        def do():
            dom = de.get().strip().lower()
            if not dom: return
            lines = self._lines()
            kept = [l for l in lines if l.split(",")[0].strip().lower().endswith("@"+dom)]
            self._setl(kept); win.destroy()
            messagebox.showinfo("Filter", f"Kept {len(kept)} emails from @{dom}")
        ctk.CTkButton(win, text="Filter", height=36, fg_color=T["accent"], command=do).pack(pady=12)

    def _tool_add_names(self):
        lines = self._lines()
        out = []
        for l in lines:
            if "," in l: out.append(l); continue
            email = l.strip()
            name = email.split("@")[0].replace("."," ").replace("_"," ").replace("-"," ").title()
            out.append(f"{email},{name}")
        self._setl(out)
        messagebox.showinfo("Done", f"Added name column to {len(out)} emails.")

    def _tool_count_emails(self):
        lines = self._lines()
        d = {}
        for l in lines:
            e = l.split(",")[0].strip().lower()
            dom = e.split("@")[-1] if "@" in e else "?"
            d[dom] = d.get(dom, 0) + 1
        total = len(lines)
        top = sorted(d.items(), key=lambda x:-x[1])[:15]
        msg = f"Total: {total} emails\n\nTop domains:\n" + "\n".join(f"  {k}: {v} ({v*100//max(total,1)}%)" for k,v in top)
        messagebox.showinfo("Email Count", msg)

    def _tool_limit_list(self):
        win = ctk.CTkToplevel(self); win.title("Limit List"); win.geometry("350x180"); win.transient(self)
        ctk.CTkLabel(win, text="Max number of emails to keep:", font=("Segoe UI",13)).pack(pady=(16,6))
        ne = ctk.CTkEntry(win, width=150, placeholder_text="1000", fg_color=T["input_bg"]); ne.pack()
        def do():
            try: n = int(ne.get())
            except: return
            lines = self._lines()[:n]; self._setl(lines); win.destroy()
            messagebox.showinfo("Done", f"List limited to {len(lines)} emails.")
        ctk.CTkButton(win, text="Limit", height=36, fg_color=T["accent"], command=do).pack(pady=12)

    def _tool_check_mx(self):
        if not HAS_DNS: messagebox.showwarning("","Install dnspython: pip install dnspython"); return
        lines = self._lines()
        if not lines: messagebox.showwarning("","Email list is empty."); return
        domains = set()
        for l in lines:
            e = l.split(",")[0].strip()
            if "@" in e: domains.add(e.split("@")[-1].lower())
        results = []
        for dom in sorted(domains):
            try:
                mx = dns.resolver.resolve(dom, 'MX')
                records = [str(r.exchange).rstrip('.') for r in mx]
                results.append(f"✓ {dom}: {', '.join(records[:3])}")
            except: results.append(f"✗ {dom}: No MX records")
        messagebox.showinfo("MX Records", "\n".join(results[:30]))

    def _tool_check_spf(self):
        if not HAS_DNS: messagebox.showwarning("","Install dnspython: pip install dnspython"); return
        lines = self._lines()
        domains = set()
        for l in lines:
            e = l.split(",")[0].strip()
            if "@" in e: domains.add(e.split("@")[-1].lower())
        results = []
        for dom in sorted(domains)[:20]:
            spf, dkim, dmarc = "✗", "✗", "✗"
            try:
                for r in dns.resolver.resolve(dom, 'TXT'):
                    if 'v=spf1' in str(r): spf = "✓"; break
            except: pass
            try: dns.resolver.resolve(f"_dmarc.{dom}", 'TXT'); dmarc = "✓"
            except: pass
            results.append(f"{dom}:  SPF {spf}  DMARC {dmarc}")
        messagebox.showinfo("SPF/DMARC Check", "\n".join(results) if results else "No domains found.")

    def _tool_blacklist_check(self):
        win = ctk.CTkToplevel(self); win.title("Blacklist Check"); win.geometry("500x300"); win.transient(self)
        ctk.CTkLabel(win, text="🚫 Blacklist Check", font=("Segoe UI Semibold",15)).pack(pady=(12,6))
        ctk.CTkLabel(win, text="Enter IP or domain to check:", font=("Segoe UI",12)).pack()
        ie = ctk.CTkEntry(win, width=350, placeholder_text="mail.yourdomain.com or 1.2.3.4", fg_color=T["input_bg"]); ie.pack(pady=4)
        rl = ctk.CTkTextbox(win, height=150, font=("Consolas",11), fg_color=T["input_bg"], state="disabled"); rl.pack(fill="x", padx=16, pady=8)
        def do():
            target = ie.get().strip()
            if not target: return
            rl.configure(state="normal"); rl.delete("1.0","end"); rl.insert("1.0","Checking...\n"); rl.configure(state="disabled")
            def _check():
                try: ip = socket.gethostbyname(target)
                except: ip = target
                rbls = ["zen.spamhaus.org","bl.spamcop.net","b.barracudacentral.org","dnsbl.sorbs.net",
                        "spam.dnsbl.sorbs.net","cbl.abuseat.org","dnsbl-1.uceprotect.net","psbl.surriel.com"]
                rev = ".".join(reversed(ip.split(".")))
                results = []
                for rbl in rbls:
                    try:
                        socket.gethostbyname(f"{rev}.{rbl}")
                        results.append(f"🔴 LISTED on {rbl}")
                    except: results.append(f"🟢 Clean on {rbl}")
                txt = f"IP: {ip}\n\n" + "\n".join(results)
                self.after(0, lambda: [rl.configure(state="normal"), rl.delete("1.0","end"), rl.insert("1.0",txt), rl.configure(state="disabled")])
            threading.Thread(target=_check, daemon=True).start()
        ctk.CTkButton(win, text="Check", height=36, fg_color=T["accent"], command=do).pack()

    def _tool_email_size(self):
        body = self.body.get("1.0","end").strip()
        body_size = len(body.encode("utf-8"))
        att_size = sum(os.path.getsize(a["path"]) for a in self.attachments if os.path.exists(a["path"]))
        total = body_size + att_size
        messagebox.showinfo("Email Size",
            f"Body: {body_size:,} bytes ({body_size/1024:.1f} KB)\n"
            f"Attachments: {att_size:,} bytes ({att_size/1024:.1f} KB)\n"
            f"Total: ~{total:,} bytes ({total/1024:.1f} KB)\n\n"
            f"{'⚠ Large email! Some providers limit to 25 MB.' if total > 10*1024*1024 else '✓ Size OK'}")

    def _tool_check_links(self):
        body = self.body.get("1.0","end")
        urls = re.findall(r'https?://[^\s<>"\']+', body)
        if not urls: messagebox.showinfo("Links","No links found in email body."); return
        results = []
        for u in urls[:20]:
            try:
                req = Request(u, method="HEAD", headers={"User-Agent":"Mozilla/5.0"})
                resp = urlopen(req, timeout=10)
                results.append(f"✓ {resp.status} — {u[:60]}")
            except Exception as ex:
                results.append(f"✗ {str(ex)[:30]} — {u[:60]}")
        messagebox.showinfo("Link Check", "\n".join(results))

    def _tool_base64_img(self):
        path = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.webp")])
        if not path: return
        with open(path, "rb") as f: data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(path)[1].lower().strip(".")
        if ext == "jpg": ext = "jpeg"
        tag = f'<img src="data:image/{ext};base64,{data[:20]}..." />'
        self.body.insert("insert", f'<img src="data:image/{ext};base64,{data}" style="max-width:600px;" />')
        messagebox.showinfo("Done", f"Image embedded in email body.\nSize: {len(data):,} chars")

    def _tool_html_to_text(self):
        body = self.body.get("1.0","end").strip()
        text = re.sub(r'<br\s*/?>', '\n', body)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        self.body.delete("1.0","end"); self.body.insert("1.0", text)
        self.content_type.set("text")
        messagebox.showinfo("Done","HTML converted to plain text.")

    def _tool_spintax_preview(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        win = ctk.CTkToplevel(self); win.title("Spintax Preview"); win.geometry("600x400"); win.transient(self)
        ctk.CTkLabel(win, text="📊 10 Random Spintax Variations", font=("Segoe UI Semibold",14)).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"]); tb.pack(fill="both", expand=True, padx=12, pady=8)
        for i in range(10):
            v = {"email":"test@example.com","name":"Test User","date":datetime.now().strftime("%Y-%m-%d"),
                 "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999)),"subject":"Test Subject"}
            result = rv(body, v)
            tb.insert("end", f"── Version {i+1} ──\n{result[:300]}\n\n")

    def _tool_unsub_link(self):
        link = '{{unsub_url}}'
        html = f'\n<div style="text-align:center;padding:20px;font-size:12px;color:#999;">'\
               f'<a href="{link}" style="color:#999;">Unsubscribe</a></div>'
        self.body.insert("end", html)
        messagebox.showinfo("Done","Unsubscribe footer added to email body.\nReplace {{unsub_url}} with your actual unsubscribe URL.")

    def _tool_char_count(self):
        body = self.body.get("1.0","end").strip()
        words = len(body.split())
        chars = len(body)
        lines = body.count("\n") + 1
        messagebox.showinfo("Character Count", f"Characters: {chars:,}\nWords: {words:,}\nLines: {lines:,}")

    # ── Spam Check & Deliverability ──

    SPAM_WORDS = {
        "high": [
            "act now","buy now","buy direct","click here","click below","order now",
            "free","100% free","free access","free gift","free trial","free offer",
            "winner","you won","congratulations","you have been selected",
            "urgent","limited time","expire","expires","last chance","hurry",
            "make money","earn money","earn extra cash","extra income","double your",
            "million dollars","billion","cash bonus","$$","$$$",
            "viagra","cialis","pharmacy","pills","weight loss","lose weight",
            "nigerian","prince","inheritance","lottery","sweepstakes",
            "no credit check","no fees","no cost","no obligation","no purchase",
            "risk free","risk-free","100% satisfaction","guaranteed",
            "act immediately","apply now","call now","get it now",
            "increase your","incredible deal","special promotion",
            "this is not spam","not spam","this isn't spam",
            "unsubscribe","remove me","opt out",
            "dear friend","dear sir","dear beneficiary",
        ],
        "medium": [
            "as seen on","additional income","be your own boss","financial freedom",
            "from home","work from home","home based","home-based",
            "no experience","no investment","online degree",
            "satisfaction guaranteed","money back","refund",
            "lowest price","best price","cheap","discount","save big","save money",
            "compare","offer","bargain","bonus","deal","promo","promotion",
            "credit card","debit card","wire transfer","bitcoin","crypto",
            "password","verify your account","confirm your","update your",
            "click the link","click this","open attachment","see attached",
            "invoice","receipt","payment","billing","account suspended",
            "important information","action required","immediate action",
            "re:","fwd:","fw:",
            "bulk email","mass email","email marketing","email list",
            "subscribe","opt-in","opt in","sign up now",
            "100%","50% off","70% off","80% off","90% off",
            "amazing","incredible","unbelievable","shocking",
        ],
        "low": [
            "dear customer","dear valued","hello friend",
            "please find","kindly","assist","assistance",
            "notification","alert","warning","notice",
            "opportunity","potential","exclusive","member","membership",
            "preview","sample","demo","webinar",
            "reply","respond","response needed",
            "today only","this week","this month","limited",
            "new","introducing","announcing","launch",
            "gift","reward","prize","benefit",
        ]
    }

    def _analyze_spam(self, body, subject=""):
        text = (subject + " " + body).lower()
        text_no_html = re.sub(r'<[^>]+>', ' ', text)
        text_clean = re.sub(r'\s+', ' ', text_no_html).strip()

        issues = []
        score = 0

        for word in self.SPAM_WORDS["high"]:
            if word.lower() in text_clean:
                issues.append(("🔴", f'"{word}"', "+8", "High-risk spam trigger word"))
                score += 8
        for word in self.SPAM_WORDS["medium"]:
            if word.lower() in text_clean:
                issues.append(("🟡", f'"{word}"', "+4", "Medium-risk spam word"))
                score += 4
        for word in self.SPAM_WORDS["low"]:
            if word.lower() in text_clean:
                issues.append(("🟠", f'"{word}"', "+2", "Low-risk spam word"))
                score += 2

        caps_words = re.findall(r'\b[A-Z]{3,}\b', body)
        if len(caps_words) > 3:
            issues.append(("🔴", f'{len(caps_words)} ALL-CAPS words', f"+{len(caps_words)*2}", "Excessive capitals = spam signal"))
            score += len(caps_words) * 2

        excl_count = body.count("!")
        if excl_count > 3:
            issues.append(("🟡", f'{excl_count} exclamation marks', f"+{excl_count}", "Too many ! is spammy"))
            score += excl_count

        dollar_count = body.count("$")
        if dollar_count > 2:
            issues.append(("🟡", f'{dollar_count} dollar signs', f"+{dollar_count*3}", "Money symbols trigger filters"))
            score += dollar_count * 3

        urls = re.findall(r'https?://[^\s<>"\']+', body)
        if len(urls) > 5:
            issues.append(("🟡", f'{len(urls)} links', "+5", "Too many links raises flags"))
            score += 5
        short_urls = [u for u in urls if any(s in u for s in ["bit.ly","tinyurl","goo.gl","t.co","ow.ly","is.gd","buff.ly"])]
        if short_urls:
            issues.append(("🔴", f'{len(short_urls)} shortened URLs', "+10", "URL shorteners are flagged by spam filters"))
            score += 10

        if re.search(r'color\s*:\s*#?(fff|ffffff|white)', body, re.IGNORECASE):
            issues.append(("🔴", "Hidden white text detected", "+15", "White/invisible text is a strong spam signal"))
            score += 15
        if re.search(r'font-size\s*:\s*[01]px', body, re.IGNORECASE):
            issues.append(("🔴", "Tiny font (0-1px) detected", "+15", "Hidden text via tiny font"))
            score += 15

        img_count = len(re.findall(r'<img\b', body, re.IGNORECASE))
        text_len = len(text_clean)
        if img_count > 0 and text_len < 100:
            issues.append(("🟡", "Image-heavy, low text", "+6", "Emails with mostly images go to spam"))
            score += 6

        if "unsubscribe" not in text_clean and len(text_clean) > 200:
            issues.append(("🟠", "No unsubscribe link", "+3", "Missing unsubscribe increases spam risk"))
            score += 3

        if subject:
            subj_lower = subject.lower()
            if subject == subject.upper() and len(subject) > 5:
                issues.append(("🔴", "Subject is ALL CAPS", "+10", "All-caps subject = spam"))
                score += 10
            if subject.count("!") > 1:
                issues.append(("🟡", f"Subject has {subject.count('!')} exclamation marks", "+4", "Excessive ! in subject"))
                score += 4
            if "re:" in subj_lower and "fwd:" not in subj_lower:
                issues.append(("🟡", 'Fake "Re:" in subject', "+5", 'Misleading "Re:" triggers spam filters'))
                score += 5

        return score, issues

    def _tool_spam_score(self):
        body = self.body.get("1.0","end").strip()
        subject = self.subject_entry.get().strip()
        if not body: messagebox.showwarning("","Email body is empty."); return

        score, issues = self._analyze_spam(body, subject)

        win = ctk.CTkToplevel(self); win.title("Spam Score Analysis"); win.geometry("750x650"); win.transient(self)
        win.configure(fg_color=T["bg"])

        # Header with score
        hdr = ctk.CTkFrame(win, fg_color=T["surface"], corner_radius=0, height=140)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        hdr_inner = ctk.CTkFrame(hdr, fg_color="transparent"); hdr_inner.pack(expand=True)

        if score <= 10:
            verdict, vcolor, emoji = "INBOX — Low Risk", T["green"], "✅"
            desc = "Your email looks clean! High chance of reaching inbox."
        elif score <= 30:
            verdict, vcolor, emoji = "CAUTION — Medium Risk", T["orange"], "⚠️"
            desc = "Some spam signals detected. Review the issues below."
        elif score <= 60:
            verdict, vcolor, emoji = "WARNING — High Risk", T["red"], "🚨"
            desc = "Multiple spam triggers found. Likely to hit spam folder."
        else:
            verdict, vcolor, emoji = "SPAM — Very High Risk", T["red"], "🛑"
            desc = "This email will almost certainly go to SPAM. Fix the issues!"

        ctk.CTkLabel(hdr_inner, text=f"{emoji}  Score: {score}/100+", font=("Segoe UI Bold",28), text_color=vcolor).pack()
        ctk.CTkLabel(hdr_inner, text=verdict, font=("Segoe UI Semibold",16), text_color=vcolor).pack(pady=(4,0))
        ctk.CTkLabel(hdr_inner, text=desc, font=("Segoe UI",12), text_color=T["t3"]).pack(pady=(4,0))

        # Score bar
        bar_frame = ctk.CTkFrame(win, fg_color=T["card"], height=50, corner_radius=0)
        bar_frame.pack(fill="x", padx=0, pady=0); bar_frame.pack_propagate(False)
        bar_inner = ctk.CTkFrame(bar_frame, fg_color="transparent"); bar_inner.pack(expand=True, fill="x", padx=20)
        pb = ctk.CTkProgressBar(bar_inner, height=16, corner_radius=8, fg_color=T["input_bg"],
                                 progress_color=vcolor, width=400)
        pb.set(min(score / 100, 1.0)); pb.pack(fill="x", pady=10)

        # Issues list
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent", scrollbar_button_color=T["border"])
        sc.pack(fill="both", expand=True, padx=12, pady=8)

        if issues:
            ctk.CTkLabel(sc, text=f"Found {len(issues)} issues:", font=("Segoe UI Semibold",14),
                          text_color=T["t1"]).pack(anchor="w", padx=8, pady=(4,8))
            for icon, word, pts, reason in issues:
                row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=8, border_width=1, border_color=T["border"])
                row.pack(fill="x", padx=4, pady=2)
                left = ctk.CTkFrame(row, fg_color="transparent"); left.pack(side="left", fill="x", expand=True, padx=10, pady=8)
                ctk.CTkLabel(left, text=f"{icon}  {word}", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left")
                ctk.CTkLabel(left, text=f"  —  {reason}", font=("Segoe UI",11), text_color=T["t3"]).pack(side="left")
                ctk.CTkLabel(row, text=pts, font=("Segoe UI Bold",12), text_color=T["red"],
                              width=40).pack(side="right", padx=10, pady=8)
        else:
            ctk.CTkLabel(sc, text="✅  No spam issues detected! Your email looks great.",
                          font=("Segoe UI Semibold",14), text_color=T["green"]).pack(pady=20)

        # Tips
        tips_frame = ctk.CTkFrame(sc, fg_color=T["accent_s"], corner_radius=10, border_width=1, border_color=T["accent"])
        tips_frame.pack(fill="x", padx=4, pady=(12,4))
        ctk.CTkLabel(tips_frame, text="💡  Tips to Improve Deliverability", font=("Segoe UI Semibold",13),
                      text_color=T["accent_l"]).pack(anchor="w", padx=14, pady=(10,4))
        tips = [
            "Avoid spam trigger words (free, buy now, urgent, winner...)",
            "Don't use ALL CAPS in subject or body",
            "Keep image-to-text ratio balanced (more text, fewer images)",
            "Include an unsubscribe link at the bottom",
            "Don't use URL shorteners (bit.ly, tinyurl...)",
            "Set up SPF, DKIM, and DMARC for your domain",
            "Use a consistent From name and email address",
            "Avoid excessive punctuation (!!! ???)",
            "Personalize with {{name}} — it looks less like mass mail",
        ]
        for tip in tips:
            ctk.CTkLabel(tips_frame, text=f"  •  {tip}", font=("Segoe UI",11),
                          text_color=T["t2"], anchor="w", wraplength=650).pack(anchor="w", padx=14, pady=1)
        ctk.CTkFrame(tips_frame, height=8, fg_color="transparent").pack()

    def _tool_spam_words(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return

        text = re.sub(r'<[^>]+>', ' ', body).lower()
        text = re.sub(r'\s+', ' ', text)

        found = {"high":[], "medium":[], "low":[]}
        for level in ("high","medium","low"):
            for word in self.SPAM_WORDS[level]:
                count = text.count(word.lower())
                if count > 0: found[level].append((word, count))

        win = ctk.CTkToplevel(self); win.title("Spam Word Scanner"); win.geometry("600x500"); win.transient(self)
        win.configure(fg_color=T["bg"])

        ctk.CTkLabel(win, text="🔍  Spam Word Scanner", font=("Segoe UI Bold",18), text_color=T["t1"]).pack(pady=(16,4))

        total = sum(len(v) for v in found.values())
        color = T["green"] if total == 0 else T["orange"] if total < 5 else T["red"]
        ctk.CTkLabel(win, text=f"Found {total} spam words in your email",
                      font=("Segoe UI Semibold",14), text_color=color).pack(pady=(0,12))

        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=(0,12))

        labels = {"high": ("🔴 High Risk", T["red"]), "medium": ("🟡 Medium Risk", T["orange"]), "low": ("🟠 Low Risk", T["orange_l"])}
        for level in ("high","medium","low"):
            words = found[level]
            if not words: continue
            lbl, clr = labels[level]
            ctk.CTkLabel(sc, text=f"\n{lbl} ({len(words)} words):", font=("Segoe UI Semibold",13), text_color=clr).pack(anchor="w", padx=8)
            for word, count in sorted(words, key=lambda x:-x[1]):
                row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=8, pady=1)
                ctk.CTkLabel(row, text=f'  "{word}"', font=("Consolas",12), text_color=T["t1"]).pack(side="left", padx=8, pady=4)
                if count > 1:
                    ctk.CTkLabel(row, text=f"×{count}", font=("Segoe UI Bold",11), text_color=clr).pack(side="right", padx=10)

        if total == 0:
            ctk.CTkLabel(sc, text="\n✅  No spam words found! Your email content is clean.",
                          font=("Segoe UI Semibold",14), text_color=T["green"]).pack(pady=20)

    def _tool_inbox_test(self):
        body = self.body.get("1.0","end").strip()
        subject = self.subject_entry.get().strip()
        if not body: messagebox.showwarning("","Email body is empty."); return

        score, issues = self._analyze_spam(body, subject)

        checks = []
        checks.append(("Subject line present", bool(subject), "Add a subject line"))
        checks.append(("Subject not ALL CAPS", subject != subject.upper() or len(subject) < 5, "Use normal capitalization"))
        checks.append(("From name set", bool(self.from_name.get().strip()), "Set a From name"))
        checks.append(("From email set", bool(self.from_email.get().strip()), "Set a From email"))
        checks.append(("Has text content", len(re.sub(r'<[^>]+>','',body).strip()) > 50, "Add more text content"))

        has_unsub = "unsubscribe" in body.lower()
        checks.append(("Unsubscribe link", has_unsub, "Add an unsubscribe link"))

        urls = re.findall(r'https?://[^\s<>"\']+', body)
        short_urls = [u for u in urls if any(s in u for s in ["bit.ly","tinyurl","goo.gl","t.co"])]
        checks.append(("No URL shorteners", len(short_urls) == 0, "Replace bit.ly/tinyurl with full URLs"))

        caps = re.findall(r'\b[A-Z]{4,}\b', body)
        checks.append(("No excessive CAPS", len(caps) <= 3, f"Reduce ALL-CAPS words ({len(caps)} found)"))

        checks.append(("Low spam score", score <= 15, f"Score is {score} — reduce spam trigger words"))

        has_smtp = len(self.smtp_servers) > 0
        checks.append(("SMTP configured", has_smtp, "Add SMTP servers"))

        has_att = len(self.attachments) > 0
        att_size = sum(os.path.getsize(a["path"]) for a in self.attachments if os.path.exists(a["path"]))
        checks.append(("Attachments < 10MB", att_size < 10*1024*1024, "Reduce attachment size"))

        win = ctk.CTkToplevel(self); win.title("Inbox Placement Test"); win.geometry("620x550"); win.transient(self)
        win.configure(fg_color=T["bg"])

        passed = sum(1 for _,ok,_ in checks if ok)
        total_checks = len(checks)
        pct = passed * 100 // total_checks

        hdr = ctk.CTkFrame(win, fg_color=T["surface"], height=100, corner_radius=0)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        hdr_in = ctk.CTkFrame(hdr, fg_color="transparent"); hdr_in.pack(expand=True)

        if pct >= 85:
            verdict, vclr = "INBOX Ready!", T["green"]
        elif pct >= 60:
            verdict, vclr = "Needs Improvement", T["orange"]
        else:
            verdict, vclr = "High Spam Risk", T["red"]

        ctk.CTkLabel(hdr_in, text=f"📊  {passed}/{total_checks} checks passed ({pct}%)",
                      font=("Segoe UI Bold",20), text_color=vclr).pack()
        ctk.CTkLabel(hdr_in, text=verdict, font=("Segoe UI Semibold",15), text_color=vclr).pack()

        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        for name, ok, fix in checks:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=8, border_width=1,
                                border_color=T["green"] if ok else T["red"])
            row.pack(fill="x", padx=4, pady=2)
            icon = "✅" if ok else "❌"
            ctk.CTkLabel(row, text=f" {icon}  {name}", font=("Segoe UI Semibold",12),
                          text_color=T["green"] if ok else T["red"]).pack(side="left", padx=10, pady=10)
            if not ok:
                ctk.CTkLabel(row, text=f"Fix: {fix}", font=("Segoe UI",11),
                              text_color=T["t3"]).pack(side="right", padx=10, pady=10)

    # ── Email Composition & Content Tools ──

    def _tool_text_to_html(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        lines = body.split("\n")
        html_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                html_lines.append("<br>")
            elif line.startswith("# "):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("### "):
                html_lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith("- ") or line.startswith("* "):
                html_lines.append(f"<li>{line[2:]}</li>")
            else:
                html_lines.append(f"<p>{line}</p>")
        ul_open = False
        result = []
        for h in html_lines:
            if h.startswith("<li>") and not ul_open:
                result.append("<ul>"); ul_open = True
            elif not h.startswith("<li>") and ul_open:
                result.append("</ul>"); ul_open = False
            result.append(h)
        if ul_open: result.append("</ul>")
        html = "<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'></head>\n<body style='font-family:Arial,sans-serif;line-height:1.6;color:#333;max-width:600px;margin:0 auto;padding:20px;'>\n" + "\n".join(result) + "\n</body>\n</html>"
        self.body.delete("1.0","end"); self.body.insert("1.0", html)
        self.content_type.set("html")
        messagebox.showinfo("Text → HTML", f"Converted {len(lines)} lines to HTML.")

    def _tool_tracking_pixel(self):
        win = ctk.CTkToplevel(self); win.title("Add Tracking Pixel"); win.geometry("500x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="🖼  Tracking Pixel Generator", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text="Enter your tracking URL (the server that records opens):", font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16)
        url_entry = ctk.CTkEntry(win, height=36, font=("Consolas",12), fg_color=T["input_bg"],
                                  border_color=T["input_bd"], placeholder_text="https://track.example.com/open?id={{email}}")
        url_entry.pack(fill="x", padx=20, pady=8)

        def _add():
            url = url_entry.get().strip()
            if not url: messagebox.showwarning("","Enter tracking URL."); return
            pixel = f'<img src="{url}" width="1" height="1" style="display:none;" alt="" />'
            body = self.body.get("1.0","end").strip()
            if "</body>" in body.lower():
                idx = body.lower().rfind("</body>")
                body = body[:idx] + pixel + "\n" + body[idx:]
            else:
                body += "\n" + pixel
            self.body.delete("1.0","end"); self.body.insert("1.0", body)
            messagebox.showinfo("Tracking Pixel","Pixel added to email body."); win.destroy()

        ctk.CTkButton(win, text="➕ Insert Tracking Pixel", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_add).pack(pady=12)
        ctk.CTkLabel(win, text="💡 The pixel fires an HTTP request when the email is opened.\n    Use {{email}} in URL to track per-recipient.",
                      font=("Segoe UI",11), text_color=T["t3"], justify="left").pack(padx=20)

    def _tool_minify_html(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        orig_len = len(body)
        body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
        body = re.sub(r'>\s+<', '><', body)
        body = re.sub(r'\s{2,}', ' ', body)
        body = body.strip()
        self.body.delete("1.0","end"); self.body.insert("1.0", body)
        saved = orig_len - len(body)
        pct = (saved / orig_len * 100) if orig_len else 0
        messagebox.showinfo("Minify HTML", f"Original: {orig_len:,} chars\nMinified: {len(body):,} chars\nSaved: {saved:,} chars ({pct:.1f}%)")

    def _tool_wrap_template(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        templates = {
            "Clean Modern": '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;">
<tr><td align="center" style="padding:40px 0;">
<table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
<tr><td style="padding:40px 30px;">
{CONTENT}
</td></tr>
<tr><td style="padding:20px 30px;background-color:#f8f8f8;border-top:1px solid #eee;text-align:center;font-size:12px;color:#999;">
{FOOTER}
</td></tr></table></td></tr></table></body></html>''',
            "Dark Professional": '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#1a1a2e;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#1a1a2e;">
<tr><td align="center" style="padding:40px 0;">
<table width="600" cellpadding="0" cellspacing="0" style="background-color:#16213e;border-radius:8px;">
<tr><td style="padding:40px 30px;color:#e0e0e0;">
{CONTENT}
</td></tr>
<tr><td style="padding:20px 30px;background-color:#0f3460;text-align:center;font-size:12px;color:#8899aa;">
{FOOTER}
</td></tr></table></td></tr></table></body></html>''',
            "Minimal": '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:40px 20px;font-family:Georgia,serif;color:#333;max-width:580px;margin:0 auto;">
{CONTENT}
<hr style="border:none;border-top:1px solid #ddd;margin:30px 0 15px;">
<p style="font-size:11px;color:#999;">{FOOTER}</p>
</body></html>''',
            "Corporate": '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#eef2f7;font-family:'Segoe UI',Tahoma,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#eef2f7;">
<tr><td align="center" style="padding:30px 0;">
<table width="600" cellpadding="0" cellspacing="0" style="background-color:#fff;border:1px solid #d0d7de;border-radius:6px;">
<tr><td style="padding:24px 32px;background:#0052cc;color:#fff;border-radius:6px 6px 0 0;">
<h1 style="margin:0;font-size:22px;">{{from_name}}</h1>
</td></tr>
<tr><td style="padding:32px;">
{CONTENT}
</td></tr>
<tr><td style="padding:16px 32px;background:#f6f8fa;border-top:1px solid #d0d7de;text-align:center;font-size:11px;color:#666;">
{FOOTER}
</td></tr></table></td></tr></table></body></html>''',
        }
        win = ctk.CTkToplevel(self); win.title("Wrap in Email Template"); win.geometry("480x380"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📋  Choose Email Template", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Your content will be wrapped inside the template.", font=("Segoe UI",12), text_color=T["t2"]).pack(pady=(0,12))
        sel = ctk.StringVar(value=list(templates.keys())[0])
        for name in templates:
            ctk.CTkRadioButton(win, text=name, variable=sel, value=name, font=("Segoe UI",13), fg_color=T["accent"]).pack(anchor="w", padx=30, pady=4)
        footer_entry = ctk.CTkEntry(win, height=36, font=("Segoe UI",12), fg_color=T["input_bg"],
                                     border_color=T["input_bd"], placeholder_text="Footer text (optional)")
        footer_entry.pack(fill="x", padx=24, pady=(12,6))
        def _apply():
            tpl = templates[sel.get()]
            ft = footer_entry.get().strip() or "You received this email from {{from_email}}. <a href='#'>Unsubscribe</a>"
            html = tpl.replace("{CONTENT}", body).replace("{FOOTER}", ft)
            self.body.delete("1.0","end"); self.body.insert("1.0", html)
            self.content_type.set("html")
            messagebox.showinfo("Template","Content wrapped in template."); win.destroy()
        ctk.CTkButton(win, text="✅ Apply Template", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_apply).pack(pady=14)

    def _tool_inline_styles(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        style_map = {
            "h1": "font-size:24px;font-weight:bold;color:#333;margin:0 0 16px;",
            "h2": "font-size:20px;font-weight:bold;color:#333;margin:0 0 12px;",
            "h3": "font-size:16px;font-weight:bold;color:#555;margin:0 0 10px;",
            "p": "font-size:14px;line-height:1.6;color:#555;margin:0 0 12px;",
            "a": "color:#0066cc;text-decoration:underline;",
            "ul": "padding-left:20px;margin:0 0 12px;",
            "li": "font-size:14px;line-height:1.8;color:#555;",
            "img": "max-width:100%;height:auto;display:block;",
            "table": "border-collapse:collapse;width:100%;",
            "td": "padding:8px;",
            "th": "padding:8px;font-weight:bold;background-color:#f5f5f5;",
            "hr": "border:none;border-top:1px solid #eee;margin:20px 0;",
            "blockquote": "border-left:3px solid #ddd;padding-left:16px;margin:12px 0;color:#777;font-style:italic;",
        }
        count = 0
        for tag, styles in style_map.items():
            pattern = rf'<{tag}(\s|>)'
            matches = re.findall(pattern, body, re.IGNORECASE)
            if matches:
                body = re.sub(rf'<{tag}(\s*)(>)', rf'<{tag} style="{styles}"\2', body, flags=re.IGNORECASE)
                body = re.sub(rf'<{tag}(\s+)style="([^"]*)"(\s*)((?:(?!style=)[^>])*?)style="{re.escape(styles)}"',
                              rf'<{tag}\1style="\2{styles}"\3\4', body, flags=re.IGNORECASE)
                count += len(matches)
        self.body.delete("1.0","end"); self.body.insert("1.0", body)
        messagebox.showinfo("Inline Styles", f"Added inline styles to {count} HTML tags.\nTags styled: {', '.join(style_map.keys())}")

    # ── Sender & Subject Tools ──

    def _tool_random_subjects(self):
        win = ctk.CTkToplevel(self); win.title("Randomize Subjects"); win.geometry("600x480"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="🔀  Subject Line Randomizer", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Enter subjects (one per line). Each email picks a random one.\nYou can also use spintax: {Hello|Hi|Hey}", font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=200, font=("Consolas",12), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        existing = self.multi_subjects.get("1.0","end").strip()
        if existing: txt.insert("1.0", existing)
        else:
            examples = [
                "🔥 Special Offer Just For You, {{name}}!",
                "{Hey|Hello|Hi} {{name}} — Don't Miss This",
                "Your {{date}} Update is Ready",
                "Important: Action Required for {{email}}",
                "🎁 {Exclusive|Limited|Special} {Deal|Offer|Discount} Inside",
            ]
            txt.insert("1.0", "\n".join(examples))
        def _apply():
            subjects = txt.get("1.0","end").strip()
            self.multi_subjects.delete("1.0","end"); self.multi_subjects.insert("1.0", subjects)
            lines = [l for l in subjects.splitlines() if l.strip()]
            messagebox.showinfo("Subjects Set", f"{len(lines)} subject variations saved.\nEach email will pick a random one."); win.destroy()
        ctk.CTkButton(win, text="✅ Apply Subjects", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_apply).pack(pady=12)

    def _tool_subject_gen(self):
        win = ctk.CTkToplevel(self); win.title("Subject Line Generator"); win.geometry("620x540"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📝  Subject Line Generator", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        categories = {
            "🛒 E-commerce / Sales": [
                "{{name}}, Your {Exclusive|Special|VIP} {Offer|Deal|Discount} Awaits!",
                "🎁 {Limited Time|Flash|Today Only}: {Save|Get} {20%|30%|50%} Off!",
                "Don't Miss Out — {Sale|Offer} Ends {Tonight|Tomorrow|Soon}!",
                "{{name}}, We Picked These Just For You",
                "Your Cart is Waiting — Complete Your Order Today",
                "🔥 {New Arrivals|Hot Items|Trending Now} You'll Love",
            ],
            "📰 Newsletter": [
                "📰 Your {Weekly|Monthly|Daily} Update — {{date}}",
                "What's New This {Week|Month}: Top {Stories|Updates|Tips}",
                "{{name}}, Here's What You Missed",
                "The Latest from {{from_name}} — {{date}}",
                "🗞 {Digest|Roundup|Recap}: {Best|Top} of the Week",
            ],
            "🔔 Notification": [
                "⚡ {Action Required|Update Available|Important Notice}",
                "{{name}}, Your Account {Update|Summary|Alert}",
                "🔔 {New|Important} {Message|Update|Notification} for You",
                "Security Alert: Please Verify Your {Account|Email|Identity}",
                "📋 Your {Report|Statement|Receipt} is Ready",
            ],
            "🤝 Follow-up": [
                "Following Up: {Our Conversation|Your Request|Your Inquiry}",
                "{{name}}, Just Checking In...",
                "Quick {Question|Update|Reminder} — {{from_name}}",
                "Did You Get a Chance to {Review|Check|Look at} This?",
                "Re: Our {Discussion|Meeting|Call} — Next Steps",
            ],
            "🎯 Marketing": [
                "{{name}}, {Unlock|Discover|Experience} {Something Special|The Difference|More}",
                "🚀 {Introducing|Meet|Announcing}: {Our New|The Next|A Better} Way to...",
                "How {{name}} Can {Save Time|Boost Results|Get Ahead}",
                "{Free|Instant|Easy} {Guide|Resource|Template}: {Master|Learn|Discover}...",
                "🎯 {Proven|Simple|Quick} {Tips|Strategies|Hacks} for {Success|Growth|Results}",
            ],
            "📧 Cold Outreach": [
                "Quick {Question|Idea|Thought} for {{name}}",
                "{{name}} — {Mutual Connection|Saw Your Work|Love Your Product}",
                "{Idea|Opportunity|Proposal} for {{name}}'s {Team|Business|Company}",
                "Can I {Help|Share|Send} Something {Useful|Valuable|Relevant}?",
                "{Collab|Partnership} Idea — {{from_name}} × {{name}}",
            ],
        }
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=8, pady=8)
        for cat, subjects in categories.items():
            ctk.CTkLabel(sc, text=cat, font=("Segoe UI Semibold",13), text_color=T["accent"]).pack(anchor="w", padx=8, pady=(10,2))
            for subj in subjects:
                row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=8, pady=1)
                ctk.CTkLabel(row, text=subj, font=("Consolas",11), text_color=T["t2"], wraplength=450).pack(side="left", padx=8, pady=6)
                ctk.CTkButton(row, text="Use", width=50, height=26, font=("Segoe UI",10),
                              fg_color=T["accent"], hover_color=T["accent_h"],
                              command=lambda s=subj: [self.subject_entry.delete(0,"end"), self.subject_entry.insert(0, s)]).pack(side="right", padx=6)
                ctk.CTkButton(row, text="+Multi", width=60, height=26, font=("Segoe UI",10),
                              fg_color=T["card_h"], hover_color=T["border_l"],
                              command=lambda s=subj: self.multi_subjects.insert("end", s + "\n")).pack(side="right", padx=2)

    def _tool_subject_ab(self):
        subjects = [l.strip() for l in self.multi_subjects.get("1.0","end").strip().splitlines() if l.strip()]
        if len(subjects) < 2:
            messagebox.showwarning("A/B Test","Add at least 2 subjects in 'Multiple Subjects' box."); return
        recipients = [l.strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip()]
        if not recipients:
            messagebox.showwarning("A/B Test","Add recipients first."); return
        win = ctk.CTkToplevel(self); win.title("Subject A/B Test Plan"); win.geometry("600x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📊  Subject A/B Test Plan", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        n_var = len(subjects)
        per_var = len(recipients) // n_var
        remainder = len(recipients) % n_var
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        ctk.CTkLabel(sc, text=f"📧 Total Recipients: {len(recipients):,}", font=("Segoe UI Semibold",13), text_color=T["t1"]).pack(anchor="w", padx=8, pady=(4,8))
        for i, subj in enumerate(subjects):
            cnt = per_var + (1 if i < remainder else 0)
            pct = cnt * 100 / len(recipients) if recipients else 0
            card = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=8); card.pack(fill="x", padx=4, pady=3)
            ctk.CTkLabel(card, text=f"Variant {chr(65+i)}", font=("Segoe UI Bold",12), text_color=T["accent"]).pack(anchor="w", padx=12, pady=(8,2))
            ctk.CTkLabel(card, text=subj, font=("Consolas",11), text_color=T["t2"], wraplength=500).pack(anchor="w", padx=12, pady=2)
            bar = ctk.CTkProgressBar(card, height=8, fg_color=T["bg"], progress_color=T["accent"])
            bar.pack(fill="x", padx=12, pady=(4,2)); bar.set(pct/100)
            ctk.CTkLabel(card, text=f"→ {cnt:,} recipients ({pct:.1f}%)", font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=12, pady=(0,8))
        ctk.CTkLabel(sc, text="💡 When you send, each recipient will get a randomly selected subject.\n    Check the log afterwards to see which subject performed best.",
                      font=("Segoe UI",11), text_color=T["t3"], justify="left").pack(anchor="w", padx=8, pady=8)

    def _tool_random_senders(self):
        win = ctk.CTkToplevel(self); win.title("Random Sender Names"); win.geometry("550x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="👤  Sender Name Rotation", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Enter sender names (one per line). Each email picks a random one.\nLeave empty to use the default From Name.",
                      font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=180, font=("Consolas",12), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        if not hasattr(self, '_sender_names'): self._sender_names = []
        if self._sender_names: txt.insert("1.0", "\n".join(self._sender_names))
        else:
            examples = ["Marketing Team", "Customer Support", "John from Sales", "The Newsletter", "VIP Offers"]
            txt.insert("1.0", "\n".join(examples))
        def _save():
            names = [l.strip() for l in txt.get("1.0","end").strip().splitlines() if l.strip()]
            self._sender_names = names
            messagebox.showinfo("Sender Names", f"{len(names)} sender names saved.\nWill rotate during sending."); win.destroy()
        ctk.CTkButton(win, text="✅ Save Sender Names", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_save).pack(pady=12)

    def _tool_multi_from(self):
        win = ctk.CTkToplevel(self); win.title("Multiple From Emails"); win.geometry("550x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📧  From Email Rotation", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Enter From emails (one per line). Each email picks a random one.\nMust match SMTP auth if required.",
                      font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=180, font=("Consolas",12), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        if not hasattr(self, '_from_emails'): self._from_emails = []
        if self._from_emails: txt.insert("1.0", "\n".join(self._from_emails))
        def _save():
            emails = [l.strip() for l in txt.get("1.0","end").strip().splitlines() if l.strip() and "@" in l]
            self._from_emails = emails
            messagebox.showinfo("From Emails", f"{len(emails)} from-emails saved.\nWill rotate during sending."); win.destroy()
        ctk.CTkButton(win, text="✅ Save From Emails", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_save).pack(pady=12)

    def _tool_reply_to_gen(self):
        win = ctk.CTkToplevel(self); win.title("Reply-To List"); win.geometry("550x400"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📋  Reply-To Address Manager", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Enter reply-to emails (one per line). A random one is used per email.",
                      font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=160, font=("Consolas",12), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        if not hasattr(self, '_reply_tos'): self._reply_tos = []
        if self._reply_tos: txt.insert("1.0", "\n".join(self._reply_tos))
        def _save():
            emails = [l.strip() for l in txt.get("1.0","end").strip().splitlines() if l.strip() and "@" in l]
            self._reply_tos = emails
            messagebox.showinfo("Reply-To", f"{len(emails)} reply-to addresses saved."); win.destroy()
        ctk.CTkButton(win, text="✅ Save Reply-To List", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_save).pack(pady=12)

    # ── Advanced Sending Tools ──

    def _tool_bounce_filter(self):
        log = self.log_box.get("1.0","end").strip()
        if not log: messagebox.showwarning("","Send log is empty. Send emails first."); return
        failed_emails = []
        for line in log.splitlines():
            if "✗" in line or "FAIL" in line.upper() or "ERROR" in line.upper():
                emails_in_line = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
                failed_emails.extend(emails_in_line)
        failed_emails = list(set(failed_emails))
        if not failed_emails:
            messagebox.showinfo("Bounce Filter","No failed emails found in the log."); return
        current = [l.strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip()]
        cleaned = [e for e in current if e.split(",")[0].strip() not in failed_emails]
        removed = len(current) - len(cleaned)
        self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0", "\n".join(cleaned))
        self._update_email_count()
        win = ctk.CTkToplevel(self); win.title("Bounce Filter Results"); win.geometry("500x400"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📋  Bounce Filter Results", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text=f"Removed {removed} bounced emails from recipients list.", font=("Segoe UI",13), text_color=T["green"]).pack(pady=4)
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        for em in failed_emails:
            ctk.CTkLabel(sc, text=f"  ✗  {em}", font=("Consolas",11), text_color=T["red"]).pack(anchor="w", padx=8, pady=1)

    def _tool_retry_failed(self):
        log = self.log_box.get("1.0","end").strip()
        if not log: messagebox.showwarning("","Send log is empty. Send emails first."); return
        failed_emails = []
        for line in log.splitlines():
            if "✗" in line or "FAIL" in line.upper():
                emails_in_line = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
                failed_emails.extend(emails_in_line)
        failed_emails = list(set(failed_emails))
        if not failed_emails:
            messagebox.showinfo("Retry","No failed emails found in the log."); return
        self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0", "\n".join(failed_emails))
        self._update_email_count()
        messagebox.showinfo("Retry Failed", f"Loaded {len(failed_emails)} failed recipients.\nPress START to re-send only to these.")

    def _tool_speed_calc(self):
        recipients = [l.strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip()]
        n = len(recipients)
        if n == 0: messagebox.showwarning("","No recipients loaded."); return
        try: delay = float(self.delay_min.get() or 1)
        except: delay = 1.0
        try: threads = int(self.thread_count.get() or 1)
        except: threads = 1
        n_smtp = max(len(self.smtp_servers), 1)
        emails_per_sec = threads / max(delay, 0.1)
        total_sec = n / emails_per_sec
        total_min = total_sec / 60
        total_hr = total_sec / 3600
        per_smtp = n / n_smtp
        win = ctk.CTkToplevel(self); win.title("Send Speed Calculator"); win.geometry("500x420"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📊  Send Speed Calculator", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        stats = [
            ("📧 Total Emails", f"{n:,}"),
            ("⚡ Threads", f"{threads}"),
            ("⏱ Delay per email", f"{delay}s"),
            ("🔌 SMTP Servers", f"{n_smtp}"),
            ("📨 Emails/second", f"{emails_per_sec:.1f}"),
            ("📨 Emails/minute", f"{emails_per_sec*60:.0f}"),
            ("📨 Emails/hour", f"{emails_per_sec*3600:.0f}"),
            ("⏰ Estimated Time", f"{total_min:.1f} min" if total_min < 60 else f"{total_hr:.1f} hours"),
            ("📊 Per SMTP server", f"{per_smtp:.0f} emails each"),
        ]
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        for label, val in stats:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text=label, font=("Segoe UI Semibold",12), text_color=T["t2"]).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(row, text=val, font=("Segoe UI Bold",13), text_color=T["accent"]).pack(side="right", padx=12, pady=8)
        ctk.CTkLabel(sc, text="💡 Tips:\n  • Increase threads for faster sending\n  • Add more SMTPs to distribute load\n  • Use 1-3s delay to avoid rate limits\n  • 5+ threads with 1s delay ≈ 300/min",
                      font=("Segoe UI",11), text_color=T["t3"], justify="left").pack(anchor="w", padx=8, pady=8)

    def _tool_schedule_send(self):
        win = ctk.CTkToplevel(self); win.title("Schedule Send"); win.geometry("500x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="⏰  Schedule Email Send", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text="Set a delay before sending starts.", font=("Segoe UI",12), text_color=T["t2"]).pack()
        fr = ctk.CTkFrame(win, fg_color="transparent"); fr.pack(pady=16)
        ctk.CTkLabel(fr, text="Hours:", font=("Segoe UI",12), text_color=T["t2"]).grid(row=0, column=0, padx=8)
        hr = ctk.CTkEntry(fr, width=60, font=("Segoe UI",14), fg_color=T["input_bg"], border_color=T["input_bd"])
        hr.grid(row=0, column=1, padx=4); hr.insert(0, "0")
        ctk.CTkLabel(fr, text="Minutes:", font=("Segoe UI",12), text_color=T["t2"]).grid(row=0, column=2, padx=8)
        mn = ctk.CTkEntry(fr, width=60, font=("Segoe UI",14), fg_color=T["input_bg"], border_color=T["input_bd"])
        mn.grid(row=0, column=3, padx=4); mn.insert(0, "30")
        status_lbl = ctk.CTkLabel(win, text="", font=("Segoe UI Semibold",13), text_color=T["accent"])
        status_lbl.pack(pady=8)
        def _schedule():
            try:
                total_sec = int(hr.get()) * 3600 + int(mn.get()) * 60
            except: messagebox.showwarning("","Invalid time values."); return
            if total_sec <= 0: messagebox.showwarning("","Set time > 0."); return
            import datetime as dt
            send_at = dt.datetime.now() + dt.timedelta(seconds=total_sec)
            status_lbl.configure(text=f"📅 Scheduled for: {send_at.strftime('%Y-%m-%d %H:%M:%S')}")
            def _wait():
                time.sleep(total_sec)
                self.after(0, self.toggle_sending)
            threading.Thread(target=_wait, daemon=True).start()
            messagebox.showinfo("Scheduled", f"Sending will start in {hr.get()}h {mn.get()}m\nat {send_at.strftime('%H:%M:%S')}")
            win.destroy()
        ctk.CTkButton(win, text="⏰ Schedule Now", height=40, fg_color=T["accent"], hover_color=T["accent_h"], command=_schedule).pack(pady=12)
        ctk.CTkLabel(win, text="💡 You can close this window. The app will auto-send\n    at the scheduled time. Don't close the main app.",
                      font=("Segoe UI",11), text_color=T["t3"], justify="left").pack(padx=20)

    def _tool_seed_list(self):
        win = ctk.CTkToplevel(self); win.title("Seed List Manager"); win.geometry("550x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📧  Seed List (Test Inboxes)", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,4))
        ctk.CTkLabel(win, text="Seed emails receive your campaign to test inbox placement.\nAdd your test inboxes from different providers below.",
                      font=("Segoe UI",12), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=180, font=("Consolas",12), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        defaults = [
            "# Add test emails from different providers:",
            "test@gmail.com",
            "test@outlook.com",
            "test@yahoo.com",
            "test@aol.com",
            "test@protonmail.com",
            "test@icloud.com",
            "test@zoho.com",
            "test@yourdomain.com",
        ]
        txt.insert("1.0", "\n".join(defaults))
        fr = ctk.CTkFrame(win, fg_color="transparent"); fr.pack(fill="x", padx=16, pady=8)
        def _send_seed():
            seeds = [l.strip() for l in txt.get("1.0","end").strip().splitlines() if l.strip() and not l.startswith("#") and "@" in l]
            if not seeds: messagebox.showwarning("","Add seed emails."); return
            current = self.recipients_box.get("1.0","end").strip()
            self.recipients_box.delete("1.0","end")
            self.recipients_box.insert("1.0", "\n".join(seeds))
            self._update_email_count()
            messagebox.showinfo("Seed List", f"Loaded {len(seeds)} seed emails.\nPress START to send test campaign.\n\nOriginal recipients backed up."); win.destroy()
        def _prepend():
            seeds = [l.strip() for l in txt.get("1.0","end").strip().splitlines() if l.strip() and not l.startswith("#") and "@" in l]
            if not seeds: messagebox.showwarning("","Add seed emails."); return
            current = self.recipients_box.get("1.0","end").strip()
            combined = "\n".join(seeds) + ("\n" + current if current else "")
            self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0", combined)
            self._update_email_count()
            messagebox.showinfo("Seed List", f"Added {len(seeds)} seeds to top of recipients."); win.destroy()
        ctk.CTkButton(fr, text="📧 Send to Seeds Only", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=_send_seed).pack(side="left", padx=4)
        ctk.CTkButton(fr, text="➕ Add Seeds to Recipients", height=36, fg_color=T["card_h"], hover_color=T["border_l"], command=_prepend).pack(side="left", padx=4)

    def _tool_send_domain_stats(self):
        recipients = [l.strip().split(",")[0].strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip() and "@" in l]
        if not recipients: messagebox.showwarning("","No recipients loaded."); return
        domains = {}
        for e in recipients:
            d = e.split("@")[1].lower() if "@" in e else "unknown"
            domains[d] = domains.get(d, 0) + 1
        sorted_d = sorted(domains.items(), key=lambda x: x[1], reverse=True)
        win = ctk.CTkToplevel(self); win.title("Domain Sending Stats"); win.geometry("550x500"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="📊  Domain Distribution", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text=f"Total: {len(recipients):,} emails across {len(domains)} domains",
                      font=("Segoe UI",12), text_color=T["t2"]).pack()
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        max_count = sorted_d[0][1] if sorted_d else 1
        provider_icons = {"gmail.com":"🔵","outlook.com":"🟦","yahoo.com":"🟣","hotmail.com":"🟦","aol.com":"🟡","icloud.com":"⚪","protonmail.com":"🟢"}
        for domain, cnt in sorted_d:
            pct = cnt * 100 / len(recipients)
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            icon = provider_icons.get(domain, "📧")
            ctk.CTkLabel(row, text=f" {icon} {domain}", font=("Consolas",11), text_color=T["t1"]).pack(side="left", padx=8, pady=6)
            ctk.CTkLabel(row, text=f"{cnt:,} ({pct:.1f}%)", font=("Segoe UI Bold",11), text_color=T["accent"]).pack(side="right", padx=8, pady=6)
            bar = ctk.CTkProgressBar(row, height=6, width=120, fg_color=T["bg"], progress_color=T["accent"])
            bar.pack(side="right", padx=4); bar.set(cnt / max_count)
        warn = [d for d, c in sorted_d if c > len(recipients) * 0.5]
        if warn:
            ctk.CTkLabel(sc, text=f"⚠️ High concentration on {', '.join(warn)}!\n    Consider splitting campaigns per domain to avoid rate limits.",
                          font=("Segoe UI",11), text_color=T["orange"], justify="left").pack(anchor="w", padx=8, pady=8)

    # ── UltraMailer-Style Tools ──

    def _tool_direct_mx_test(self):
        if not HAS_DNS: messagebox.showwarning("","dnspython not installed. Run: pip install dnspython"); return
        win = ctk.CTkToplevel(self); win.title("Direct MX Test"); win.geometry("550x420"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Direct MX Test", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Test if you can send directly to a domain's mail server (port 25).",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        domain_e = ctk.CTkEntry(win, height=34, font=("Segoe UI",12), fg_color=T["input_bg"],
                                 border_color=T["input_bd"], placeholder_text="gmail.com")
        domain_e.pack(fill="x", padx=20, pady=4)
        result_box = ctk.CTkTextbox(win, height=200, font=("Consolas",11), fg_color=T["input_bg"],
                                     border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        result_box.pack(fill="both", expand=True, padx=20, pady=8)
        def _test():
            d = domain_e.get().strip()
            if not d: return
            result_box.delete("1.0","end")
            result_box.insert("end", f"Testing MX for: {d}\n\n")
            try:
                answers = dns.resolver.resolve(d, 'MX')
                mx_hosts = sorted(answers, key=lambda r: r.preference)
                for mx in mx_hosts:
                    result_box.insert("end", f"MX: {mx.exchange} (priority: {mx.preference})\n")
                best = str(mx_hosts[0].exchange).rstrip('.')
                result_box.insert("end", f"\nBest MX: {best}\nTesting connection on port 25...\n")
                try:
                    s = smtplib.SMTP(best, 25, timeout=10)
                    banner = s.ehlo()
                    result_box.insert("end", f"Connected! Banner: {s.ehlo_resp.decode()[:100]}\n")
                    s.quit()
                    result_box.insert("end", "\n✓ Direct MX sending is AVAILABLE for this domain!")
                except Exception as ex:
                    result_box.insert("end", f"\n✗ Port 25 blocked: {ex}\nDirect MX may not work from your network.")
            except Exception as ex:
                result_box.insert("end", f"✗ DNS Error: {ex}")
        ctk.CTkButton(win, text="Test MX", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=lambda: threading.Thread(target=_test, daemon=True).start()).pack(pady=8)

    def _tool_smtp_verify_email(self):
        win = ctk.CTkToplevel(self); win.title("SMTP Email Verify"); win.geometry("550x420"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="SMTP Email Verification", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Verify if an email address exists via SMTP RCPT TO check.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        email_e = ctk.CTkEntry(win, height=34, font=("Segoe UI",12), fg_color=T["input_bg"],
                                border_color=T["input_bd"], placeholder_text="test@gmail.com")
        email_e.pack(fill="x", padx=20, pady=4)
        result_lbl = ctk.CTkLabel(win, text="", font=("Segoe UI",13), text_color=T["t2"])
        result_lbl.pack(pady=8)
        result_box = ctk.CTkTextbox(win, height=160, font=("Consolas",10), fg_color=T["input_bg"],
                                     border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        result_box.pack(fill="both", expand=True, padx=20, pady=(0,8))
        def _verify():
            email = email_e.get().strip()
            if not email or "@" not in email: return
            domain = email.split("@")[1]
            result_box.delete("1.0","end")
            result_lbl.configure(text="Verifying...", text_color=T["orange"])
            try:
                if not HAS_DNS: raise Exception("dnspython required")
                answers = dns.resolver.resolve(domain, 'MX')
                mx = str(sorted(answers, key=lambda r: r.preference)[0].exchange).rstrip('.')
                result_box.insert("end", f"MX: {mx}\n")
                s = smtplib.SMTP(mx, 25, timeout=15)
                s.ehlo("verify.local")
                result_box.insert("end", f"Connected to {mx}\n")
                s.mail("verify@verify.local")
                code, msg = s.rcpt(email)
                result_box.insert("end", f"RCPT TO response: {code} {msg.decode()}\n")
                s.quit()
                if code == 250:
                    result_lbl.configure(text=f"✓ {email} EXISTS", text_color=T["green"])
                elif code == 550:
                    result_lbl.configure(text=f"✗ {email} DOES NOT EXIST", text_color=T["red"])
                else:
                    result_lbl.configure(text=f"? Unknown response: {code}", text_color=T["orange"])
            except Exception as ex:
                result_lbl.configure(text="Could not verify", text_color=T["red"])
                result_box.insert("end", f"Error: {ex}\n")
        ctk.CTkButton(win, text="Verify Email", height=36, fg_color=T["accent"], hover_color=T["accent_h"],
                       command=lambda: threading.Thread(target=_verify, daemon=True).start()).pack(pady=8)

    def _tool_warmup_planner(self):
        win = ctk.CTkToplevel(self); win.title("Email Warmup Planner"); win.geometry("600x520"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Email Warmup Planner", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Plan a gradual volume increase for new SMTP/IP to build reputation.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        fr = ctk.CTkFrame(win, fg_color="transparent"); fr.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(fr, text="Total emails:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        total_e = ctk.CTkEntry(fr, width=80, font=("Segoe UI",12), fg_color=T["input_bg"], border_color=T["input_bd"])
        total_e.pack(side="left", padx=4); total_e.insert(0, "10000")
        ctk.CTkLabel(fr, text="Days:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left", padx=(12,0))
        days_e = ctk.CTkEntry(fr, width=60, font=("Segoe UI",12), fg_color=T["input_bg"], border_color=T["input_bd"])
        days_e.pack(side="left", padx=4); days_e.insert(0, "14")
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=16, pady=8)
        def _plan():
            for w in sc.winfo_children(): w.destroy()
            try: total = int(total_e.get()); days = int(days_e.get())
            except: return
            schedule = []
            remaining = total
            daily = max(10, total // (days * 4))
            for d in range(1, days+1):
                if remaining <= 0: break
                today = min(daily, remaining)
                schedule.append((d, today))
                remaining -= today
                daily = int(daily * 1.3)
            if remaining > 0: schedule.append((len(schedule)+1, remaining))
            for day, count in schedule:
                pct = count / total
                row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
                ctk.CTkLabel(row, text=f"Day {day}", font=("Segoe UI Semibold",11), text_color=T["t1"], width=60).pack(side="left", padx=8, pady=6)
                bar = ctk.CTkProgressBar(row, height=8, width=200, fg_color=T["bg"], progress_color=T["accent"])
                bar.pack(side="left", padx=4); bar.set(min(pct * 3, 1.0))
                ctk.CTkLabel(row, text=f"{count:,} emails", font=("Segoe UI Bold",11), text_color=T["accent"]).pack(side="left", padx=8)
                per_hr = max(1, count // 8)
                ctk.CTkLabel(row, text=f"~{per_hr}/hr", font=("Segoe UI",10), text_color=T["t3"]).pack(side="right", padx=8)
        ctk.CTkButton(win, text="Generate Warmup Plan", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=_plan).pack(pady=6)
        _plan()

    def _tool_link_tracker(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        win = ctk.CTkToplevel(self); win.title("Link Click Tracker"); win.geometry("600x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Link Click Tracker", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Rewrite URLs to pass through your tracking server.\nEnter your tracking redirect URL below.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        url_entry = ctk.CTkEntry(win, height=34, font=("Consolas",11), fg_color=T["input_bg"],
                                  border_color=T["input_bd"], placeholder_text="https://track.example.com/click?url=")
        url_entry.pack(fill="x", padx=20, pady=4)
        urls = re.findall(r'href=["\']([^"\']+)["\']', body)
        urls = [u for u in urls if u.startswith("http") and "unsubscribe" not in u.lower()]
        ctk.CTkLabel(win, text=f"Found {len(urls)} trackable links in email body.", font=("Segoe UI",11), text_color=T["t2"]).pack(padx=20, pady=4)
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=16, pady=4)
        for u in urls[:20]:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=1)
            ctk.CTkLabel(row, text=u[:70]+("..." if len(u)>70 else ""), font=("Consolas",10), text_color=T["t2"]).pack(side="left", padx=8, pady=4)
        def _apply():
            base = url_entry.get().strip()
            if not base: messagebox.showwarning("","Enter tracking URL."); return
            b = self.body.get("1.0","end").strip()
            count = 0
            for u in urls:
                tracked = base + quote(u, safe='')
                b = b.replace(f'href="{u}"', f'href="{tracked}"')
                b = b.replace(f"href='{u}'", f"href='{tracked}'")
                count += 1
            self.body.delete("1.0","end"); self.body.insert("1.0", b)
            messagebox.showinfo("Link Tracker", f"Rewrote {count} links for click tracking."); win.destroy()
        ctk.CTkButton(win, text="Apply Click Tracking", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=_apply).pack(pady=8)

    def _tool_cid_images(self):
        win = ctk.CTkToplevel(self); win.title("Embed CID Images"); win.geometry("550x380"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Embed Images (CID)", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Embed images as inline CID attachments instead of external URLs.\nSelect an image file to embed.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        file_lbl = ctk.CTkLabel(win, text="No file selected", font=("Segoe UI",11), text_color=T["t3"])
        file_lbl.pack(pady=4)
        cid_entry = ctk.CTkEntry(win, height=34, font=("Segoe UI",12), fg_color=T["input_bg"],
                                  border_color=T["input_bd"], placeholder_text="image001")
        cid_entry.pack(fill="x", padx=20, pady=4); cid_entry.insert(0, f"img{random.randint(100,999)}")
        file_path = [None]
        def _browse():
            f = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.gif *.webp")])
            if f: file_path[0] = f; file_lbl.configure(text=os.path.basename(f))
        ctk.CTkButton(win, text="Browse Image", height=34, fg_color=T["card_h"], hover_color=T["border_l"], command=_browse).pack(pady=4)
        def _embed():
            if not file_path[0]: messagebox.showwarning("","Select an image."); return
            cid = cid_entry.get().strip() or f"img{random.randint(100,999)}"
            ext = os.path.splitext(file_path[0])[1].lower().lstrip('.')
            if ext == "jpg": ext = "jpeg"
            with open(file_path[0], "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            img_tag = f'<img src="cid:{cid}" alt="{cid}" style="max-width:100%;" />'
            body = self.body.get("1.0","end").strip()
            if "</body>" in body.lower():
                idx = body.lower().rfind("</body>")
                body = body[:idx] + img_tag + "\n" + body[idx:]
            else:
                body += "\n" + img_tag
            self.body.delete("1.0","end"); self.body.insert("1.0", body)
            self.attachments.append({"path": file_path[0], "filename": f"{cid}.{ext}", "_cid": cid, "_mime": f"image/{ext}"})
            messagebox.showinfo("CID Image", f"Embedded as cid:{cid}\nImage tag added to body."); win.destroy()
        ctk.CTkButton(win, text="Embed Image", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=_embed).pack(pady=10)

    def _tool_bounce_parser(self):
        win = ctk.CTkToplevel(self); win.title("Bounce Email Parser"); win.geometry("600x480"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Bounce Email Parser", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Paste bounce/NDR emails to extract failed addresses.\nPaste the full bounce message text below.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, height=180, font=("Consolas",10), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        txt.pack(fill="both", expand=True, padx=16, pady=4)
        result_lbl = ctk.CTkLabel(win, text="", font=("Segoe UI",12), text_color=T["t2"])
        result_lbl.pack(pady=4)
        def _parse():
            raw = txt.get("1.0","end")
            bounce_patterns = [
                r'Final-Recipient:.*?;\s*([^\s<>]+@[^\s<>]+)',
                r'Original-Recipient:.*?;\s*([^\s<>]+@[^\s<>]+)',
                r'was not delivered to\s+([^\s<>]+@[^\s<>]+)',
                r'Delivery to .* ([^\s<>]+@[^\s<>]+) .* failed',
                r'could not be delivered to\s+([^\s<>]+@[^\s<>]+)',
                r'User unknown.*?([^\s<>]+@[^\s<>]+)',
                r'mailbox unavailable.*?([^\s<>]+@[^\s<>]+)',
                r'550.*?([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})',
                r'<([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})>.*(?:rejected|bounced|undeliverable|failed)',
            ]
            found = set()
            for pat in bounce_patterns:
                found.update(re.findall(pat, raw, re.IGNORECASE))
            extra = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', raw)
            skip = ["postmaster@","mailer-daemon@","noreply@","no-reply@"]
            for e in extra:
                if not any(e.lower().startswith(s) for s in skip): found.add(e)
            if found:
                result_lbl.configure(text=f"Found {len(found)} bounced addresses", text_color=T["green"])
                current = [l.strip() for l in self.recipients_box.get("1.0","end").strip().splitlines() if l.strip()]
                cleaned = [l for l in current if l.split(",")[0].strip().lower() not in {e.lower() for e in found}]
                removed = len(current) - len(cleaned)
                if removed > 0:
                    self.recipients_box.delete("1.0","end"); self.recipients_box.insert("1.0", "\n".join(cleaned))
                    self._update_email_count()
                    result_lbl.configure(text=f"Found {len(found)} bounced — Removed {removed} from recipients", text_color=T["green"])
            else:
                result_lbl.configure(text="No bounced addresses found", text_color=T["orange"])
        ctk.CTkButton(win, text="Parse & Remove Bounced", height=36, fg_color=T["accent"], hover_color=T["accent_h"], command=_parse).pack(pady=8)

    def _tool_advanced_macros(self):
        win = ctk.CTkToplevel(self); win.title("Advanced Macros"); win.geometry("580x520"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Advanced Macro System", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="All available variables for subject, body, and headers.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=4)
        macros = [
            ("{{email}}", "Recipient email address", "user@gmail.com"),
            ("{{name}}", "Recipient name (from list)", "John Doe"),
            ("{{domain}}", "Recipient domain", "gmail.com"),
            ("{{date}}", "Current date YYYY-MM-DD", "2026-02-21"),
            ("{{time}}", "Current time HH:MM:SS", "14:30:00"),
            ("{{subject}}", "Current subject line", "Hello World"),
            ("{{random}}", "Random 5-digit number", "48271"),
            ("{{rand6}}", "Random 6-digit number", "831054"),
            ("{{uuid}}", "Short UUID (8 chars)", "a3f8b2c1"),
            ("{{rand_name}}", "Random first name", "Alex"),
            ("{{from_name}}", "Sender name", "Marketing Team"),
            ("{{from_email}}", "Sender email", "info@company.com"),
            ("{A|B|C}", "Spintax: random pick", "B"),
            ("{Hello|Hi|Hey} {{name}}", "Combined", "Hi John Doe"),
        ]
        for var, desc, example in macros:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text=var, font=("Consolas",11), text_color=T["accent"], width=160, anchor="w").pack(side="left", padx=8, pady=6)
            ctk.CTkLabel(row, text=desc, font=("Segoe UI",10), text_color=T["t2"]).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=example, font=("Consolas",10), text_color=T["t3"]).pack(side="right", padx=8)
            ctk.CTkButton(row, text="Copy", width=44, height=22, font=("Segoe UI",9), fg_color=T["card_h"],
                           hover_color=T["border_l"], corner_radius=4,
                           command=lambda v=var: [self.clipboard_clear(), self.clipboard_append(v)]).pack(side="right", padx=2)

    def _tool_auto_text_version(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showwarning("","Email body is empty."); return
        plain = self._html_to_plain(body)
        win = ctk.CTkToplevel(self); win.title("Auto Plain Text Version"); win.geometry("600x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Auto Plain Text Version", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Preview the auto-generated text version of your HTML email.\nEnable 'Auto Multipart MIME' in Settings to include this in every email.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        txt = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        txt.pack(fill="both", expand=True, padx=16, pady=8)
        txt.insert("1.0", plain)
        ctk.CTkLabel(win, text=f"HTML: {len(body):,} chars → Plain text: {len(plain):,} chars",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(pady=(0,8))

    def _tool_msgid_custom(self):
        win = ctk.CTkToplevel(self); win.title("Message-ID Format"); win.geometry("520x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Message-ID Customizer", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Preview how Message-IDs will look.\nEnable randomization in Settings > Header Randomization.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=4)
        fe = self.from_email.get().strip() or "sender@example.com"
        for i in range(10):
            msgid = self._make_msgid_custom(fe)
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text=f"#{i+1}", font=("Segoe UI",10), text_color=T["t3"], width=28).pack(side="left", padx=6, pady=5)
            ctk.CTkLabel(row, text=msgid, font=("Consolas",10), text_color=T["t1"]).pack(side="left", padx=4)

    def _tool_header_preview(self):
        body = self.body.get("1.0","end").strip()[:100] or "Hello"
        v = {"email":"user@example.com","name":"John","date":datetime.now().strftime("%Y-%m-%d"),
             "time":datetime.now().strftime("%H:%M:%S"),"random":"48271","domain":"example.com",
             "uuid":uuid.uuid4().hex[:8],"rand6":"831054","rand_name":"Alex","subject":"Test Subject"}
        fn = rv(self.from_name.get() or "Sender", v)
        fe = rv(self.from_email.get() or "s@example.com", v)
        su = rv(self.subject_entry.get() or "Subject", v)
        rp = self.reply_to.get().strip()
        win = ctk.CTkToplevel(self); win.title("Full Header Preview"); win.geometry("650x500"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Email Header Preview", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        txt = ctk.CTkTextbox(win, font=("Consolas",10), fg_color=T["input_bg"],
                              border_width=1, border_color=T["input_bd"], text_color=T["t1"])
        txt.pack(fill="both", expand=True, padx=16, pady=8)
        lines = [
            f"From: {fn} <{fe}>",
            f"To: user@example.com",
            f"Subject: {su}",
            f"Date: {formatdate(localtime=True)}",
            f"Message-ID: {self._make_msgid_custom(fe)}",
            f"MIME-Version: 1.0",
        ]
        if rp: lines.append(f"Reply-To: {rp}")
        rpath = self.return_path.get().strip()
        if rpath: lines.append(f"Return-Path: <{rpath}>")
        xp = self.x_priority.get()
        if xp and xp != "None": lines.append(f"X-Priority: {xp[0]}")
        if self.rand_xmailer_var.get(): lines.append(f"X-Mailer: {random.choice(self._XMAILERS)}")
        hdrs = self.headers_box.get("1.0","end").strip()
        if hdrs:
            for line in hdrs.splitlines():
                if ":" in line: lines.append(rv(line.strip(), v))
        ct = "multipart/alternative" if self.auto_text_var.get() else f"text/{'html' if self.content_type.get()=='html' else 'plain'}; charset=utf-8"
        lines.append(f"Content-Type: {ct}")
        lines.append(f"Content-Transfer-Encoding: {self.transfer_enc.get()}")
        txt.insert("1.0", "\n".join(lines))

    def _tool_encoding_selector(self):
        win = ctk.CTkToplevel(self); win.title("Encoding Guide"); win.geometry("550x420"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Encoding & MIME Guide", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        items = [
            ("quoted-printable", "Best for HTML emails. Encodes special chars, keeps text readable.\nMost compatible with all email clients.", T["green"]),
            ("base64", "Encodes everything. Slightly larger size (+33%).\nGood for binary content or non-Latin charsets.", T["accent"]),
            ("7bit", "US-ASCII only. No encoding. Smallest size.\nFails with non-English characters.", T["orange"]),
            ("8bit", "Allows 8-bit chars without encoding.\nNot all servers support this.", T["orange"]),
            ("UTF-8 charset", "Standard Unicode. Supports all languages.\nAlways use with quoted-printable or base64.", T["green"]),
            ("ISO-8859-1 charset", "Latin-1. Western European languages only.\nSmaller than UTF-8 for these languages.", T["t2"]),
            ("Base64 charset", "Encode Subject/From in Base64.\nHides content from simple spam filters.", T["cyan"]),
        ]
        for title, desc, color in items:
            card = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); card.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(card, text=title, font=("Segoe UI Semibold",11), text_color=color).pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(card, text=desc, font=("Segoe UI",10), text_color=T["t3"], wraplength=460, justify="left").pack(anchor="w", padx=10, pady=(2,6))

    def _tool_domain_throttle_cfg(self):
        win = ctk.CTkToplevel(self); win.title("Domain Throttle Config"); win.geometry("550x400"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Domain Throttle Config", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Recommended limits per provider to avoid rate-limiting.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=4)
        limits = [
            ("gmail.com", "50/hour", "Strict. Use warmup."),
            ("outlook.com / hotmail.com", "100/hour", "Moderate limits."),
            ("yahoo.com", "75/hour", "Moderate. Watch bounces."),
            ("aol.com", "100/hour", "Less strict."),
            ("icloud.com", "50/hour", "Apple is strict."),
            ("zoho.com", "200/hour", "Business-friendly."),
            ("protonmail.com", "100/hour", "Privacy-focused."),
            ("Corporate domains", "200-500/hour", "Depends on server."),
            ("Custom domains", "No limit", "Your server, your rules."),
        ]
        for domain, limit, note in limits:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            ctk.CTkLabel(row, text=domain, font=("Segoe UI Semibold",11), text_color=T["t1"], width=180, anchor="w").pack(side="left", padx=8, pady=6)
            ctk.CTkLabel(row, text=limit, font=("Segoe UI Bold",11), text_color=T["accent"]).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=note, font=("Segoe UI",10), text_color=T["t3"]).pack(side="right", padx=8)

    def _tool_smtp_pool_test(self):
        if not self.smtp_servers: messagebox.showwarning("","Add SMTP servers first."); return
        win = ctk.CTkToplevel(self); win.title("SMTP Connection Pool Test"); win.geometry("600x400"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="SMTP Connection Pool Test", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Test simultaneous connections to all SMTP servers.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        def _test():
            for w in sc.winfo_children(): w.destroy()
            results = []
            def test_one(i, srv):
                start = time.time()
                try:
                    s, _cfg = self._smtp_open_connection(srv, timeout=10)
                    elapsed = time.time() - start
                    s.quit()
                    results.append((i, srv, True, elapsed, ""))
                except Exception as ex:
                    results.append((i, srv, False, time.time()-start, str(ex)[:60]))
            threads = []
            for i, srv in enumerate(self.smtp_servers):
                t = threading.Thread(target=test_one, args=(i, srv), daemon=True)
                threads.append(t); t.start()
            for t in threads: t.join(timeout=15)
            results.sort(key=lambda x: x[0])
            def _show():
                for idx, srv, ok, elapsed, err in results:
                    row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
                    status = "OK" if ok else "FAIL"
                    color = T["green"] if ok else T["red"]
                    ctk.CTkLabel(row, text=f"#{idx+1}", font=("Segoe UI",10), text_color=T["t3"], width=28).pack(side="left", padx=6, pady=5)
                    ctk.CTkLabel(row, text=f"{srv['host']}:{srv['port']}", font=("Segoe UI",11), text_color=T["t1"]).pack(side="left", padx=4)
                    ctk.CTkLabel(row, text=f"{elapsed:.1f}s", font=("Segoe UI",10), text_color=T["t3"]).pack(side="left", padx=8)
                    ctk.CTkLabel(row, text=status, font=("Segoe UI Bold",11), text_color=color).pack(side="right", padx=8)
                    if err: ctk.CTkLabel(row, text=err, font=("Segoe UI",9), text_color=T["red"]).pack(side="right", padx=4)
                ok_count = sum(1 for _,_,ok,_,_ in results if ok)
                ctk.CTkLabel(sc, text=f"Pool: {ok_count}/{len(results)} servers ready", font=("Segoe UI Semibold",12), text_color=T["accent"]).pack(pady=6)
            self.after(0, _show)
        ctk.CTkButton(win, text="Test All Connections", height=36, fg_color=T["accent"], hover_color=T["accent_h"],
                       command=lambda: threading.Thread(target=_test, daemon=True).start()).pack(pady=8)

    def _tool_email_fingerprint(self):
        win = ctk.CTkToplevel(self); win.title("Email Fingerprint Check"); win.geometry("550x450"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Email Fingerprint Check", font=("Segoe UI Bold",16), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Check if your email has unique fingerprints that could\nbe detected as bulk mail.",
                      font=("Segoe UI",11), text_color=T["t2"]).pack(padx=16, pady=(0,8))
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        body = self.body.get("1.0","end").strip()
        checks = []
        checks.append(("Spintax used", "{" in body and "|" in body and "}" in body, "Add spintax for uniqueness"))
        checks.append(("Personalization vars", "{{" in body, "Add {{name}} or {{email}} variables"))
        checks.append(("Multiple subjects", len([l for l in self.multi_subjects.get("1.0","end").strip().splitlines() if l.strip()]) > 1, "Add multiple subject lines"))
        checks.append(("Sender rotation", bool(self._sender_names), "Set up random sender names"))
        checks.append(("From email rotation", bool(self._from_emails), "Set up multiple from emails"))
        checks.append(("Message-ID randomized", self.rand_msgid_var.get(), "Enable in Settings > Header Randomization"))
        checks.append(("X-Mailer randomized", self.rand_xmailer_var.get(), "Enable in Settings > Header Randomization"))
        checks.append(("MIME boundary random", self.rand_boundary_var.get(), "Enable in Settings"))
        checks.append(("Date header varied", self.rand_date_var.get(), "Enable in Settings"))
        checks.append(("Auto text version", self.auto_text_var.get(), "Enable multipart MIME in Settings"))
        checks.append(("SMTP rotation", self.rotate_var.get() and len(self.smtp_servers) > 1, "Add multiple SMTPs"))
        passed = sum(1 for _, ok, _ in checks if ok)
        total = len(checks)
        pct = passed * 100 // total
        if pct >= 80: verdict, vclr = "Excellent anti-fingerprint", T["green"]
        elif pct >= 50: verdict, vclr = "Moderate uniqueness", T["orange"]
        else: verdict, vclr = "Easily fingerprinted", T["red"]
        ctk.CTkLabel(sc, text=f"{passed}/{total} ({pct}%) - {verdict}", font=("Segoe UI Bold",14), text_color=vclr).pack(pady=(4,8))
        for name, ok, fix in checks:
            row = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); row.pack(fill="x", padx=4, pady=2)
            icon = "✓" if ok else "✗"
            color = T["green"] if ok else T["red"]
            ctk.CTkLabel(row, text=f" {icon}  {name}", font=("Segoe UI",11), text_color=color).pack(side="left", padx=8, pady=6)
            if not ok: ctk.CTkLabel(row, text=fix, font=("Segoe UI",10), text_color=T["t3"]).pack(side="right", padx=8)

    # ── New Email Tools ──
    def _tool_dmarc_check(self):
        win = ctk.CTkToplevel(self); win.title("DMARC Record Checker"); win.geometry("500x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="DMARC Record Checker", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Enter domain to check DMARC DNS record", font=("Segoe UI",11), text_color=T["t3"]).pack()
        inp = ctk.CTkEntry(win, placeholder_text="example.com", height=36, font=("Segoe UI",12),
                            fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        inp.pack(fill="x", padx=20, pady=8)
        result = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"], text_color=T["t1"], height=120)
        result.pack(fill="both", expand=True, padx=16, pady=(0,8))
        def _check():
            domain = inp.get().strip()
            if not domain: return
            result.delete("1.0","end")
            if not HAS_DNS:
                result.insert("1.0","Install dnspython: pip install dnspython"); return
            try:
                answers = dns.resolver.resolve(f"_dmarc.{domain}","TXT")
                for rdata in answers:
                    result.insert("end", f"{rdata}\n")
            except Exception as ex: result.insert("1.0", f"Error: {str(ex)}")
        ctk.CTkButton(win, text="Check DMARC", fg_color=T["accent"], hover_color=T["accent_h"],
                       command=_check).pack(padx=20, pady=(0,12), fill="x")

    def _tool_header_analyzer(self):
        win = ctk.CTkToplevel(self); win.title("Email Header Analyzer"); win.geometry("550x400"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Email Header Analyzer", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Paste raw email headers to analyze", font=("Segoe UI",10), text_color=T["t3"]).pack()
        tb = ctk.CTkTextbox(win, height=150, font=("Consolas",10), fg_color=T["input_bg"], text_color=T["t1"])
        tb.pack(fill="x", padx=16, pady=8)
        result = ctk.CTkTextbox(win, font=("Consolas",10), fg_color=T["input_bg"], text_color=T["green"])
        result.pack(fill="both", expand=True, padx=16, pady=(0,8))
        def _analyze():
            raw = tb.get("1.0","end").strip()
            if not raw: return
            result.delete("1.0","end")
            for line in raw.splitlines():
                if ":" in line:
                    key = line.split(":")[0].strip()
                    val = line.split(":",1)[1].strip()
                    if key.lower() in ("from","to","subject","date","received","message-id","x-mailer","return-path","dkim-signature","authentication-results"):
                        result.insert("end", f"[{key}]\n  {val}\n\n")
        ctk.CTkButton(win, text="Analyze Headers", fg_color=T["accent"], hover_color=T["accent_h"],
                       command=_analyze).pack(padx=16, pady=(0,12), fill="x")

    def _tool_reputation(self):
        from_email = self.from_email.get().strip()
        domain = from_email.split("@")[1] if "@" in from_email else ""
        if not domain: messagebox.showwarning("","Enter a From Email address first."); return
        checks = []
        if HAS_DNS:
            try: dns.resolver.resolve(domain,"MX"); checks.append(("MX Record",True))
            except: checks.append(("MX Record",False))
            try: dns.resolver.resolve(domain,"TXT"); checks.append(("SPF/TXT Record",True))
            except: checks.append(("SPF/TXT Record",False))
            try: dns.resolver.resolve(f"_dmarc.{domain}","TXT"); checks.append(("DMARC Record",True))
            except: checks.append(("DMARC Record",False))
        else:
            checks.append(("DNS Check","N/A (install dnspython)"))
        passed = sum(1 for _,ok in checks if ok is True)
        total = len(checks)
        msg = f"Domain: {domain}\n\n"
        for name, ok in checks:
            icon = "OK" if ok is True else ("FAIL" if ok is False else str(ok))
            msg += f"  {icon}  {name}\n"
        msg += f"\nScore: {passed}/{total}"
        messagebox.showinfo("Sender Reputation", msg)

    def _tool_html_validator(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showinfo("","Email body is empty."); return
        issues = []
        if "<html" not in body.lower(): issues.append("Missing <html> tag")
        if "<head" not in body.lower(): issues.append("Missing <head> tag")
        if "<body" not in body.lower(): issues.append("Missing <body> tag")
        open_tags = re.findall(r'<([a-zA-Z]+)[\s>]', body)
        close_tags = re.findall(r'</([a-zA-Z]+)>', body)
        void = {"br","hr","img","input","meta","link","area","base","col","embed","source","track","wbr"}
        for tag in set(open_tags):
            if tag.lower() in void: continue
            o = open_tags.count(tag); c = close_tags.count(tag)
            if o != c: issues.append(f"<{tag}>: {o} opened, {c} closed")
        if not issues:
            messagebox.showinfo("HTML Validator","HTML looks valid! No issues found.")
        else:
            messagebox.showwarning("HTML Validator","Issues found:\n\n" + "\n".join(issues))

    def _tool_responsive_preview(self):
        body = self.body.get("1.0","end").strip()
        if not body: messagebox.showinfo("","Email body is empty."); return
        wrapper = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
        <style>body{{margin:0;padding:20px;font-family:Arial;background:#f5f5f5;}}</style></head>
        <body><div style="max-width:375px;margin:0 auto;background:#fff;padding:10px;border:2px solid #ddd;">
        <div style="text-align:center;font-size:10px;color:#999;margin-bottom:8px;">Mobile Preview (375px)</div>
        {body}</div><div style="max-width:768px;margin:20px auto;background:#fff;padding:10px;border:2px solid #ddd;">
        <div style="text-align:center;font-size:10px;color:#999;margin-bottom:8px;">Tablet Preview (768px)</div>
        {body}</div></body></html>'''
        tmp = os.path.join(tempfile.gettempdir(),"omnisend_responsive.html")
        with open(tmp,"w",encoding="utf-8") as f: f.write(wrapper)
        webbrowser.open(f"file://{tmp}")

    def _tool_signature_gen(self):
        win = ctk.CTkToplevel(self); win.title("Email Signature Generator"); win.geometry("500x380"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Email Signature Generator", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        fields = {}
        for label, placeholder in [("Full Name","John Doe"),("Title/Position","Marketing Manager"),
                                     ("Company","My Company"),("Phone","+1234567890"),
                                     ("Website","https://example.com"),("Email","john@example.com")]:
            r = ctk.CTkFrame(win, fg_color="transparent"); r.pack(fill="x", padx=20, pady=1)
            ctk.CTkLabel(r, text=label+":", font=("Segoe UI",11), text_color=T["t2"], width=90, anchor="w").pack(side="left")
            e = ctk.CTkEntry(r, placeholder_text=placeholder, height=30, font=("Segoe UI",11),
                              fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
            e.pack(side="left", fill="x", expand=True); fields[label] = e
        result = ctk.CTkTextbox(win, height=100, font=("Consolas",10), fg_color=T["input_bg"], text_color=T["t1"])
        result.pack(fill="both", expand=True, padx=16, pady=8)
        def _gen():
            n=fields["Full Name"].get() or "Name"; t=fields["Title/Position"].get()
            c=fields["Company"].get(); p=fields["Phone"].get()
            w=fields["Website"].get(); em=fields["Email"].get()
            sig = f'<table style="font-family:Arial,sans-serif;font-size:13px;color:#333;"><tr><td style="border-right:3px solid #3b82f6;padding-right:14px;">'
            sig += f'<strong style="font-size:15px;">{n}</strong><br>'
            if t: sig += f'<span style="color:#666;">{t}</span><br>'
            if c: sig += f'<strong>{c}</strong>'
            sig += f'</td><td style="padding-left:14px;">'
            if p: sig += f'Tel: {p}<br>'
            if em: sig += f'Email: <a href="mailto:{em}" style="color:#3b82f6;">{em}</a><br>'
            if w: sig += f'Web: <a href="{w}" style="color:#3b82f6;">{w}</a>'
            sig += '</td></tr></table>'
            result.delete("1.0","end"); result.insert("1.0", sig)
        def _insert():
            _gen(); body = self.body.get("1.0","end").strip()
            sig = result.get("1.0","end").strip()
            if sig: self.body.insert("end", "\n<br><br>\n" + sig); win.destroy()
        bf = ctk.CTkFrame(win, fg_color="transparent"); bf.pack(fill="x", padx=16, pady=(0,12))
        ctk.CTkButton(bf, text="Generate", fg_color=T["accent"], hover_color=T["accent_h"],
                       command=_gen).pack(side="left", fill="x", expand=True, padx=(0,4))
        ctk.CTkButton(bf, text="Insert into Body", fg_color=T["green"], hover_color=T["green_h"],
                       command=_insert).pack(side="right", fill="x", expand=True)

    def _tool_url_shortener(self):
        win = ctk.CTkToplevel(self); win.title("URL Shortener"); win.geometry("460x200"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="URL Shortener (is.gd)", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        inp = ctk.CTkEntry(win, placeholder_text="https://example.com/long-url-here", height=36, font=("Segoe UI",12),
                            fg_color=T["input_bg"], border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        inp.pack(fill="x", padx=20, pady=8)
        result_lbl = ctk.CTkLabel(win, text="", font=("Consolas",12), text_color=T["green"])
        result_lbl.pack(padx=20)
        def _shorten():
            url = inp.get().strip()
            if not url: return
            try:
                api = f"https://is.gd/create.php?format=simple&url={quote(url)}"
                resp = urlopen(Request(api, method="GET"), timeout=10)
                short = resp.read().decode().strip()
                result_lbl.configure(text=short)
            except Exception as ex: result_lbl.configure(text=f"Error: {str(ex)[:50]}", text_color=T["red"])
        ctk.CTkButton(win, text="Shorten URL", fg_color=T["accent"], hover_color=T["accent_h"],
                       command=_shorten).pack(padx=20, pady=8, fill="x")

    def _tool_dynamic_content(self):
        win = ctk.CTkToplevel(self); win.title("Dynamic Content Blocks"); win.geometry("500x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Dynamic Content Blocks", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="Generate conditional blocks. Paste result into email body.", font=("Segoe UI",10), text_color=T["t3"]).pack()
        tb = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=16, pady=8)
        blocks = ("<!-- Dynamic block: personalized greeting -->\n"
                  "{Hi {{name}}|Hello {{name}}|Dear {{name}}},\n\n"
                  "<!-- Dynamic block: CTA -->\n"
                  "{Click here to learn more|Discover our offers|Get started today}\n\n"
                  "<!-- Dynamic block: closing -->\n"
                  "{Best regards|Kind regards|Thanks|Cheers},\n"
                  "{{name}}")
        tb.insert("1.0", blocks)
        def _insert():
            content = tb.get("1.0","end").strip()
            if content: self.body.insert("end", "\n" + content); win.destroy()
        ctk.CTkButton(win, text="Insert into Body", fg_color=T["green"], hover_color=T["green_h"],
                       command=_insert).pack(padx=16, pady=(0,12), fill="x")

    def _tool_xheaders(self):
        win = ctk.CTkToplevel(self); win.title("Custom X-Headers"); win.geometry("500x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Custom X-Headers Editor", font=("Segoe UI Bold",14), text_color=T["t1"]).pack(pady=(14,4))
        ctk.CTkLabel(win, text="One per line: X-Header-Name: value", font=("Segoe UI",10), text_color=T["t3"]).pack()
        tb = ctk.CTkTextbox(win, font=("Consolas",11), fg_color=T["input_bg"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=16, pady=8)
        existing = self.custom_headers.get("1.0","end").strip() if hasattr(self,'custom_headers') else ""
        if existing: tb.insert("1.0", existing)
        else: tb.insert("1.0","X-Campaign-ID: {{random}}\nX-Mailer: OmniSend Pro\nX-Priority: 3")
        def _apply():
            if hasattr(self,'custom_headers'):
                self.custom_headers.delete("1.0","end")
                self.custom_headers.insert("1.0", tb.get("1.0","end").strip())
            win.destroy()
        ctk.CTkButton(win, text="Apply to Settings", fg_color=T["accent"], hover_color=T["accent_h"],
                       command=_apply).pack(padx=16, pady=(0,12), fill="x")

    def _tool_dkim_viewer(self):
        body = self.body.get("1.0","end").strip()[:200]
        info = ("DKIM (DomainKeys Identified Mail)\n\n"
                "DKIM must be configured on your mail server, not in the email client.\n\n"
                "To check DKIM:\n"
                "1. Send a test email to a Gmail account\n"
                "2. Open the email > Show original\n"
                "3. Look for 'DKIM: PASS' in Authentication-Results\n\n"
                "To set up DKIM:\n"
                "- Generate DKIM keys from your email provider\n"
                "- Add the DKIM TXT record to your domain's DNS\n"
                "- Most SMTP services (SendGrid, SES, etc.) handle this automatically")
        messagebox.showinfo("DKIM Signature Info", info)

    def _tool_return_path(self):
        from_email = self.from_email.get().strip()
        domain = from_email.split("@")[1] if "@" in from_email else "example.com"
        paths = [f"bounce@{domain}", f"return@{domain}", f"noreply@{domain}",
                 f"bounces+{{email}}@{domain}", f"return-{{random}}@{domain}"]
        messagebox.showinfo("Return-Path Suggestions",
            "Suggested Return-Path addresses:\n\n" + "\n".join(paths) +
            "\n\nSet this in Custom Headers:\nReturn-Path: <address>")

    def _tool_import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv"),("All","*.*")])
        if not path: return
        try:
            with open(path,"r",encoding="utf-8",errors="ignore") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header: messagebox.showwarning("","Empty CSV."); return
                email_col = -1; name_col = -1
                for i, h in enumerate(header):
                    hl = h.lower().strip()
                    if "email" in hl or "@" in hl: email_col = i
                    elif "name" in hl or "nom" in hl: name_col = i
                if email_col < 0:
                    for i, h in enumerate(header):
                        if "@" in h: email_col = i; break
                if email_col < 0: email_col = 0
                lines = []
                for row in reader:
                    if email_col < len(row):
                        email = row[email_col].strip()
                        name = row[name_col].strip() if name_col >= 0 and name_col < len(row) else ""
                        if "@" in email:
                            lines.append(f"{email},{name}" if name else email)
                existing = self.recipients_box.get("1.0","end").strip()
                if existing: self.recipients_box.insert("end","\n")
                self.recipients_box.insert("end","\n".join(lines))
                self._update_email_count()
                messagebox.showinfo("Imported", f"Imported {len(lines)} emails from CSV.")
        except Exception as ex: messagebox.showerror("Error", str(ex))

    def _tool_export_html_report(self):
        if not self.log_data: messagebox.showinfo("","No sending data yet."); return
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML","*.html")])
        if not path: return
        total = len(self.log_data)
        sent = sum(1 for e in self.log_data if e.get("status")=="sent")
        failed = total - sent
        rows = ""
        for e in self.log_data:
            clr = "#22c55e" if e.get("status")=="sent" else "#ef4444"
            rows += f'<tr><td>{e.get("time","")}</td><td>{e.get("target","")}</td><td>{e.get("channel","")}</td><td style="color:{clr}">{e.get("status","")}</td><td>{e.get("error","")}</td></tr>'
        html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>OmniSend Report</title>
        <style>body{{font-family:Arial;background:#f5f5f5;padding:30px;}}
        .card{{background:#fff;border-radius:12px;padding:24px;margin:10px 0;box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
        h1{{color:#3b82f6;}} table{{width:100%;border-collapse:collapse;}} th,td{{padding:8px;border-bottom:1px solid #eee;text-align:left;}}
        th{{background:#3b82f6;color:#fff;}} .stat{{display:inline-block;margin:0 20px;text-align:center;}}
        .stat .num{{font-size:28px;font-weight:bold;}} .green{{color:#22c55e;}} .red{{color:#ef4444;}}</style></head>
        <body><div class="card"><h1>OmniSend Pro - Send Report</h1><p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <div class="stat"><div class="num">{total}</div>Total</div>
        <div class="stat"><div class="num green">{sent}</div>Sent</div>
        <div class="stat"><div class="num red">{failed}</div>Failed</div></div>
        <div class="card"><table><tr><th>Time</th><th>Target</th><th>Channel</th><th>Status</th><th>Error</th></tr>{rows}</table></div>
        </body></html>'''
        with open(path,"w",encoding="utf-8") as f: f.write(html)
        webbrowser.open(f"file://{path}")
        messagebox.showinfo("Done", f"Report exported to {path}")

    def _tool_backup_data(self):
        import zipfile
        path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP","*.zip")],
                                             initialfile=f"omnisend_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        if not path: return
        try:
            with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(DATA_DIR):
                    for file in files:
                        fp = os.path.join(root, file)
                        arcname = os.path.relpath(fp, DATA_DIR)
                        zf.write(fp, arcname)
            messagebox.showinfo("Backup Complete", f"All data backed up to:\n{path}")
        except Exception as ex: messagebox.showerror("Error", str(ex))

    # ── WhatsApp Tools ──
    def _wa_lines(self): return [l.strip() for l in self.wa_phones.get("1.0","end").strip().splitlines() if l.strip()]
    def _wa_setl(self, lines): self.wa_phones.delete("1.0","end"); self.wa_phones.insert("1.0","\n".join(lines)); self._count_phones(self.wa_phones, self.wa_count)

    def _tool_wa_clean_phones(self):
        lines = self._wa_lines()
        out = []
        for l in lines:
            parts = l.split(",", 1)
            phone = re.sub(r'[^\d+]', '', parts[0])
            if not phone.startswith("+"): phone = "+" + phone
            if len(phone) >= 9:
                out.append(f"{phone},{parts[1].strip()}" if len(parts) > 1 else phone)
        self._wa_setl(out)
        messagebox.showinfo("Done", f"Cleaned {len(out)} phone numbers.")

    def _tool_wa_dedup(self):
        lines = self._wa_lines(); seen, out = set(), []
        for l in lines:
            k = re.sub(r'[^\d]', '', l.split(",")[0])
            if k not in seen: seen.add(k); out.append(l)
        self._wa_setl(out)
        messagebox.showinfo("Done", f"Removed {len(lines)-len(out)} duplicate phones.")

    def _tool_wa_sort(self):
        lines = self._wa_lines(); lines.sort(key=lambda l: l.split(",")[0]); self._wa_setl(lines)

    def _tool_wa_shuffle(self):
        lines = self._wa_lines(); random.shuffle(lines); self._wa_setl(lines)

    def _tool_wa_country_stats(self):
        lines = self._wa_lines()
        countries = {}
        codes = {"+1":"US/CA","+44":"UK","+33":"FR","+49":"DE","+212":"MA","+213":"DZ","+216":"TN",
                 "+20":"EG","+966":"SA","+971":"UAE","+91":"IN","+86":"CN","+81":"JP","+55":"BR",
                 "+34":"ES","+39":"IT","+31":"NL","+7":"RU","+90":"TR","+62":"ID","+60":"MY",
                 "+234":"NG","+27":"ZA","+254":"KE","+221":"SN","+225":"CI"}
        for l in lines:
            phone = l.split(",")[0].strip()
            found = False
            for code, name in sorted(codes.items(), key=lambda x:-len(x[0])):
                if phone.startswith(code): countries[f"{code} ({name})"] = countries.get(f"{code} ({name})",0)+1; found=True; break
            if not found: countries["Other"] = countries.get("Other",0)+1
        msg = "\n".join(f"  {k}: {v}" for k,v in sorted(countries.items(), key=lambda x:-x[1]))
        messagebox.showinfo("Country Stats", f"Total: {len(lines)}\n\n{msg}")

    def _tool_wa_split_country(self):
        lines = self._wa_lines()
        d = {}
        for l in lines:
            phone = l.split(",")[0].strip()
            code = re.match(r'(\+\d{1,3})', phone)
            key = code.group(1) if code else "unknown"
            d.setdefault(key, []).append(l)
        out = filedialog.askdirectory()
        if not out: return
        for code, phones in d.items():
            fn = f"phones_{code.replace('+','plus')}.txt"
            with open(os.path.join(out, fn), "w") as f: f.write("\n".join(phones))
        messagebox.showinfo("Done", f"Split into {len(d)} files by country code.")

    def _tool_wa_merge(self):
        paths = filedialog.askopenfilenames(filetypes=[("Text/CSV","*.txt *.csv"),("All","*.*")])
        if not paths: return
        merged = []
        for p in paths:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and len(re.sub(r'[^\d]','',line.split(",")[0])) >= 8: merged.append(line)
        existing = self._wa_lines()
        combined = existing + merged
        seen, out = set(), []
        for l in combined:
            k = re.sub(r'[^\d]','', l.split(",")[0])
            if k not in seen: seen.add(k); out.append(l)
        self._wa_setl(out)
        messagebox.showinfo("Merge", f"Merged {len(paths)} files.\nTotal unique: {len(out)}")

    def _tool_wa_extract(self):
        win = ctk.CTkToplevel(self); win.title("Extract Phone Numbers"); win.geometry("600x400"); win.transient(self)
        ctk.CTkLabel(win, text="Paste any text — phone numbers will be extracted", font=("Segoe UI Semibold",14)).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, height=220, font=("Consolas",12), fg_color=T["input_bg"]); tb.pack(fill="x", padx=16, pady=4)
        rl = ctk.CTkLabel(win, text="", font=("Segoe UI",12)); rl.pack(pady=4)
        def do():
            raw = tb.get("1.0","end")
            found = list(set(re.findall(r'\+?\d[\d\s\-]{7,15}\d', raw)))
            cleaned = [re.sub(r'[\s\-]','',p) for p in found if len(re.sub(r'[\s\-]','',p)) >= 8]
            if not cleaned: rl.configure(text="No phone numbers found.", text_color=T["red"]); return
            existing = self.wa_phones.get("1.0","end").strip()
            if existing: self.wa_phones.insert("end", "\n"+"\n".join(cleaned))
            else: self.wa_phones.delete("1.0","end"); self.wa_phones.insert("1.0","\n".join(cleaned))
            self._count_phones(self.wa_phones, self.wa_count)
            rl.configure(text=f"✓ Extracted {len(cleaned)} numbers!", text_color=T["green"])
        ctk.CTkButton(win, text="Extract & Add", height=38, fg_color=T["wa_green"],
                       hover_color=T["wa_green_h"], font=("Segoe UI",13,"bold"), command=do).pack(pady=8)

    def _tool_wa_preview(self):
        msg = self.wa_message.get("1.0","end").strip()
        if not msg: messagebox.showwarning("","WhatsApp message is empty."); return
        win = ctk.CTkToplevel(self); win.title("Message Preview"); win.geometry("450x350"); win.transient(self)
        ctk.CTkLabel(win, text="💬 Message Preview (5 variations)", font=("Segoe UI Semibold",14)).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"]); tb.pack(fill="both", expand=True, padx=12, pady=8)
        for i in range(5):
            v = {"phone":f"+1234567890{i}","name":f"User {i+1}","date":datetime.now().strftime("%Y-%m-%d"),
                 "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
            tb.insert("end", f"── To: {v['phone']} ──\n{rv(msg,v)}\n\n")

    def _tool_wa_count(self):
        lines = self._wa_lines()
        messagebox.showinfo("Count", f"Total phone numbers: {len(lines)}")

    def _tool_wa_limit(self):
        win = ctk.CTkToplevel(self); win.title("Limit Phone List"); win.geometry("350x180"); win.transient(self)
        ctk.CTkLabel(win, text="Max phone numbers to keep:", font=("Segoe UI",13)).pack(pady=(16,6))
        ne = ctk.CTkEntry(win, width=150, placeholder_text="500", fg_color=T["input_bg"]); ne.pack()
        def do():
            try: n = int(ne.get())
            except: return
            lines = self._wa_lines()[:n]; self._wa_setl(lines); win.destroy()
        ctk.CTkButton(win, text="Limit", height=36, fg_color=T["wa_green"], command=do).pack(pady=12)

    def _tool_wa_format(self):
        win = ctk.CTkToplevel(self); win.title("Format Numbers"); win.geometry("400x200"); win.transient(self)
        ctk.CTkLabel(win, text="Add country code prefix to all numbers:", font=("Segoe UI",13)).pack(pady=(16,6))
        ce = ctk.CTkEntry(win, width=200, placeholder_text="+212", fg_color=T["input_bg"]); ce.pack()
        def do():
            code = ce.get().strip()
            if not code: return
            if not code.startswith("+"): code = "+" + code
            lines = self._wa_lines(); out = []
            for l in lines:
                parts = l.split(",", 1); phone = parts[0].strip()
                if not phone.startswith("+"): phone = code + phone.lstrip("0")
                out.append(f"{phone},{parts[1].strip()}" if len(parts)>1 else phone)
            self._wa_setl(out); win.destroy()
            messagebox.showinfo("Done", f"Formatted {len(out)} numbers with prefix {code}")
        ctk.CTkButton(win, text="Apply", height=36, fg_color=T["wa_green"], command=do).pack(pady=12)

    # ── New WhatsApp Tools ──
    def _tool_wa_link_gen(self):
        win = ctk.CTkToplevel(self); win.title("WA Link Generator"); win.geometry("450x280"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="WhatsApp Click-to-Chat Link Generator", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text="Phone number (with country code):", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20)
        pe = ctk.CTkEntry(win, placeholder_text="+1234567890", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); pe.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(win, text="Pre-filled message (optional):", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20)
        me = ctk.CTkEntry(win, placeholder_text="Hello!", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); me.pack(fill="x", padx=20, pady=4)
        res = ctk.CTkEntry(win, fg_color=T["input_bg"], border_color=T["input_bd"], height=34, state="readonly"); res.pack(fill="x", padx=20, pady=8)
        def gen():
            phone = pe.get().strip().replace("+","").replace(" ","").replace("-","")
            msg = me.get().strip()
            url = f"https://wa.me/{phone}" + (f"?text={requests.utils.quote(msg)}" if msg else "")
            res.configure(state="normal"); res.delete(0,"end"); res.insert(0, url); res.configure(state="readonly")
        ctk.CTkButton(win, text="Generate Link", height=36, fg_color=T["wa_green"], hover_color="#1B9E52", command=gen).pack(pady=4)

    def _tool_wa_vcard(self):
        win = ctk.CTkToplevel(self); win.title("vCard Generator"); win.geometry("450x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Generate vCard from Phone List", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first.",parent=win); return
        lines = self._wa_lines()
        if not lines: messagebox.showwarning("","Phone list is empty.",parent=win); return
        path = filedialog.asksaveasfilename(defaultextension=".vcf", filetypes=[("vCard","*.vcf")], parent=win)
        if not path: return
        count = 0
        with open(path,"w",encoding="utf-8") as f:
            for l in lines:
                parts = l.split(",",1); phone = parts[0].strip(); name = parts[1].strip() if len(parts)>1 else f"Contact {count+1}"
                f.write(f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL;TYPE=CELL:{phone}\nEND:VCARD\n")
                count += 1
        messagebox.showinfo("Done", f"Generated {count} vCards to:\n{path}", parent=win); win.destroy()

    def _tool_wa_spintax(self):
        if not hasattr(self, 'wa_message'): messagebox.showwarning("","Load WhatsApp page first."); return
        msg = self.wa_message.get("1.0","end").strip()
        if not msg: messagebox.showwarning("","WhatsApp message is empty."); return
        win = ctk.CTkToplevel(self); win.title("WA Spintax Preview"); win.geometry("500x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Spintax Preview — 5 Variations", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"], text_color=T["t1"]); tb.pack(fill="both", expand=True, padx=12, pady=8)
        for i in range(5):
            v = {"phone":f"+1234567890{i}","name":f"User {i+1}","date":datetime.now().strftime("%Y-%m-%d"),
                 "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
            tb.insert("end", f"── Variation {i+1} ──\n{rv(msg,v)}\n\n")

    def _tool_wa_msg_chars(self):
        if not hasattr(self, 'wa_message'): messagebox.showwarning("","Load WhatsApp page first."); return
        msg = self.wa_message.get("1.0","end").strip()
        chars = len(msg); words = len(msg.split()); lines = msg.count("\n")+1
        messagebox.showinfo("Message Stats", f"Characters: {chars}\nWords: {words}\nLines: {lines}\n\n"
            f"WhatsApp limit: ~65,536 chars per message\n{'OK' if chars<65536 else 'Too long!'}")

    def _tool_wa_scheduler(self):
        messagebox.showinfo("Scheduler", "Bulk Message Scheduler:\n\n"
            "1. Set your messages and phone list\n"
            "2. Configure delay in WhatsApp Settings tab\n"
            "3. Set batch size and pause between batches\n"
            "4. Click START SENDING to begin\n\n"
            "The app will automatically pace your messages\n"
            "according to your settings to avoid bans.")

    def _tool_wa_auto_reply(self):
        if not hasattr(self, 'wa_message'): messagebox.showwarning("","Load WhatsApp page first."); return
        templates = [
            "Thank you for your message! We'll get back to you within 24 hours.",
            "Hi {{name}}! Thanks for reaching out. How can we help you today?",
            "Hello! We received your message. Our team will respond shortly.",
            "Thanks for contacting us, {{name}}. Your inquiry has been noted.",
        ]
        win = ctk.CTkToplevel(self); win.title("Auto-Reply Templates"); win.geometry("480x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Quick Auto-Reply Templates", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(12,6))
        for t in templates:
            f = ctk.CTkFrame(win, fg_color=T["card"], corner_radius=6); f.pack(fill="x", padx=12, pady=2)
            ctk.CTkLabel(f, text=t[:60]+"..." if len(t)>60 else t, font=("Segoe UI",11), text_color=T["t1"], wraplength=340).pack(side="left", padx=8, pady=8)
            ctk.CTkButton(f, text="Use", width=50, height=24, fg_color=T["wa_green"], hover_color="#1B9E52",
                           command=lambda m=t: [self.wa_message.delete("1.0","end"), self.wa_message.insert("1.0",m), win.destroy()]).pack(side="right", padx=8, pady=8)

    def _tool_wa_validate_phone(self):
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first."); return
        lines = self._wa_lines()
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        valid, invalid = [], []
        for l in lines:
            phone = l.split(",",1)[0].strip()
            clean = re.sub(r'[\s\-\(\)]','',phone)
            if re.match(r'^\+?\d{7,15}$', clean): valid.append(l)
            else: invalid.append(l)
        self._wa_setl(valid)
        messagebox.showinfo("Validation", f"Valid: {len(valid)}\nInvalid removed: {len(invalid)}\n\n"
            + ("Invalid numbers:\n" + "\n".join(invalid[:10]) if invalid else "All numbers are valid!"))

    def _tool_wa_test_numbers(self):
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first."); return
        nums = [f"+1555000{str(i).zfill(4)}" for i in range(1,11)]
        self.wa_phones.insert("end", "\n".join(nums) + "\n")
        self._count_phones(self.wa_phones, self.wa_count)
        messagebox.showinfo("Test Numbers", f"Added 10 test phone numbers.\nThese are fake numbers for testing only.")

    def _tool_wa_export_csv(self):
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first."); return
        lines = self._wa_lines()
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path,"w",newline="",encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["Phone","Name"])
            for l in lines:
                parts = l.split(",",1)
                w.writerow([parts[0].strip(), parts[1].strip() if len(parts)>1 else ""])
        messagebox.showinfo("Export", f"Exported {len(lines)} contacts to:\n{path}")

    def _tool_wa_import_csv(self):
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first."); return
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv"),("All","*.*")])
        if not path: return
        added = 0
        with open(path,"r",encoding="utf-8",errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if not row: continue
                phone = row[0].strip()
                name = row[1].strip() if len(row)>1 else ""
                if phone:
                    self.wa_phones.insert("end", f"{phone},{name}\n" if name else f"{phone}\n")
                    added += 1
        self._count_phones(self.wa_phones, self.wa_count)
        messagebox.showinfo("Import", f"Imported {added} contacts from CSV.")

    def _tool_wa_broadcast(self):
        if not hasattr(self, 'wa_phones'): messagebox.showwarning("","Load WhatsApp page first."); return
        lines = self._wa_lines()
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        win = ctk.CTkToplevel(self); win.title("Broadcast List Creator"); win.geometry("450x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Split into Broadcast Lists", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text="Max contacts per list (WhatsApp limit: 256):", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20)
        se = ctk.CTkEntry(win, fg_color=T["input_bg"], border_color=T["input_bd"], height=34); se.pack(fill="x", padx=20, pady=4); se.insert(0,"256")
        def split():
            try: size = int(se.get())
            except: size = 256
            chunks = [lines[i:i+size] for i in range(0,len(lines),size)]
            path = filedialog.askdirectory(parent=win)
            if not path: return
            for i, chunk in enumerate(chunks):
                with open(os.path.join(path, f"broadcast_list_{i+1}.txt"),"w",encoding="utf-8") as f:
                    f.write("\n".join(chunk))
            messagebox.showinfo("Done", f"Created {len(chunks)} broadcast lists in:\n{path}", parent=win); win.destroy()
        ctk.CTkButton(win, text="Split & Save", height=36, fg_color=T["wa_green"], command=split).pack(pady=12)

    def _tool_wa_qr_text(self):
        win = ctk.CTkToplevel(self); win.title("QR Code Text"); win.geometry("400x200"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Generate QR-ready WhatsApp Link", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        pe = ctk.CTkEntry(win, placeholder_text="+1234567890", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); pe.pack(fill="x", padx=20, pady=4)
        res = ctk.CTkEntry(win, fg_color=T["input_bg"], border_color=T["input_bd"], height=34); res.pack(fill="x", padx=20, pady=4)
        def gen():
            phone = pe.get().strip().replace("+","").replace(" ","")
            res.delete(0,"end"); res.insert(0, f"https://wa.me/{phone}")
        ctk.CTkButton(win, text="Generate", height=34, fg_color=T["wa_green"], command=gen).pack(pady=8)
        ctk.CTkLabel(win, text="Copy this link and paste into any QR code generator", font=("Segoe UI",10), text_color=T["t3"]).pack()

    # ── SMS Tools ──
    def _tool_sms_char_count(self):
        msg = self.sms_message.get("1.0","end").strip()
        chars = len(msg)
        parts = 1 if chars <= 160 else (chars + 152) // 153
        messagebox.showinfo("SMS Counter", f"Characters: {chars}\nSMS parts: {parts}\n\n"
            f"{'✓ Fits in 1 SMS' if parts == 1 else f'⚠ Will be split into {parts} SMS messages'}")

    def _tool_sms_parts(self):
        msg = self.sms_message.get("1.0","end").strip()
        has_unicode = any(ord(c) > 127 for c in msg)
        if has_unicode:
            single_limit, multi_limit = 70, 67
        else:
            single_limit, multi_limit = 160, 153
        chars = len(msg)
        parts = 1 if chars <= single_limit else (chars + multi_limit - 1) // multi_limit
        messagebox.showinfo("SMS Parts", f"Characters: {chars}\nEncoding: {'Unicode' if has_unicode else 'GSM-7'}\n"
            f"Char limit per SMS: {single_limit if parts==1 else multi_limit}\nParts: {parts}")

    def _tool_sms_preview(self):
        msg = self.sms_message.get("1.0","end").strip()
        if not msg: messagebox.showwarning("","SMS message is empty."); return
        win = ctk.CTkToplevel(self); win.title("SMS Preview"); win.geometry("400x300"); win.transient(self)
        ctk.CTkLabel(win, text="📱 SMS Preview", font=("Segoe UI Semibold",14)).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"]); tb.pack(fill="both", expand=True, padx=12, pady=8)
        for i in range(3):
            v = {"phone":f"+1234567890{i}","name":f"User {i+1}","date":datetime.now().strftime("%Y-%m-%d"),
                 "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
            tb.insert("end", f"── To: {v['phone']} ──\n{rv(msg,v)}\n\n")

    def _tool_sms_encoding(self):
        if not hasattr(self, 'sms_message'): messagebox.showwarning("","Load SMS page first."); return
        msg = self.sms_message.get("1.0","end").strip()
        if not msg: messagebox.showwarning("","SMS message is empty."); return
        has_unicode = any(ord(c) > 127 for c in msg)
        unicode_chars = [c for c in msg if ord(c) > 127]
        enc = "UCS-2 (Unicode)" if has_unicode else "GSM-7 (Standard)"
        limit = 70 if has_unicode else 160
        multi_limit = 67 if has_unicode else 153
        info = f"Encoding: {enc}\nSingle SMS limit: {limit} chars\nMultipart limit: {multi_limit} chars/part\n\nCharacters: {len(msg)}"
        if unicode_chars:
            info += f"\n\nUnicode characters found ({len(unicode_chars)}):\n" + " ".join(set(unicode_chars[:20]))
            info += "\n\nTip: Removing these characters would allow GSM-7 encoding (160 chars/SMS instead of 70)."
        messagebox.showinfo("SMS Encoding", info)

    def _tool_sms_short_url(self):
        win = ctk.CTkToplevel(self); win.title("Short URL Helper"); win.geometry("450x200"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Short URL Generator", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text="Paste your long URL:", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20)
        ue = ctk.CTkEntry(win, placeholder_text="https://example.com/very/long/url...", fg_color=T["input_bg"], border_color=T["input_bd"], height=34)
        ue.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(win, text="Use these free services to shorten URLs:\n  bit.ly  |  tinyurl.com  |  is.gd  |  v.gd",
                      font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=20, pady=8)
        def try_shorten():
            url = ue.get().strip()
            if not url: return
            try:
                r = requests.get(f"https://is.gd/create.php?format=simple&url={requests.utils.quote(url)}", timeout=10)
                if r.status_code == 200:
                    short = r.text.strip()
                    ue.delete(0,"end"); ue.insert(0, short)
                    if hasattr(self, 'sms_message'): self.sms_message.insert("end", f" {short}")
                else: messagebox.showerror("Error","Could not shorten URL. Try manually.",parent=win)
            except: messagebox.showerror("Error","Network error. Try a service manually.",parent=win)
        ctk.CTkButton(win, text="Shorten with is.gd", height=34, fg_color=T["sms_blue"], command=try_shorten).pack(pady=4)

    def _tool_sms_optout(self):
        if not hasattr(self, 'sms_message'): messagebox.showwarning("","Load SMS page first."); return
        options = [
            "\nReply STOP to unsubscribe.",
            "\nText STOP to opt out.",
            "\nReply STOP to stop receiving messages.",
            "\nTo unsubscribe, reply STOP.",
            "\nOpt-out: reply STOP to this number.",
        ]
        win = ctk.CTkToplevel(self); win.title("Opt-Out Generator"); win.geometry("450x280"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Add Opt-Out / Unsubscribe Text", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(12,6))
        for opt in options:
            f = ctk.CTkFrame(win, fg_color=T["card"], corner_radius=6); f.pack(fill="x", padx=12, pady=2)
            ctk.CTkLabel(f, text=opt.strip(), font=("Segoe UI",11), text_color=T["t1"]).pack(side="left", padx=8, pady=6)
            ctk.CTkButton(f, text="Add", width=45, height=24, fg_color=T["sms_blue"],
                           command=lambda o=opt: [self.sms_message.insert("end", o), win.destroy()]).pack(side="right", padx=8, pady=6)

    def _tool_sms_spintax(self):
        if not hasattr(self, 'sms_message'): messagebox.showwarning("","Load SMS page first."); return
        msg = self.sms_message.get("1.0","end").strip()
        if not msg: messagebox.showwarning("","SMS message is empty."); return
        win = ctk.CTkToplevel(self); win.title("SMS Spintax Preview"); win.geometry("450x300"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Spintax Preview — 5 Variations", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(12,6))
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"], text_color=T["t1"]); tb.pack(fill="both", expand=True, padx=12, pady=8)
        for i in range(5):
            v = {"phone":f"+1234567890{i}","name":f"User {i+1}","date":datetime.now().strftime("%Y-%m-%d"),
                 "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
            tb.insert("end", f"── Variation {i+1} ──\n{rv(msg,v)}\n\n")

    def _tool_sms_validate_phones(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        valid, invalid = [], []
        for l in lines:
            phone = l.split(",",1)[0].strip(); clean = re.sub(r'[\s\-\(\)]','',phone)
            if re.match(r'^\+?\d{7,15}$', clean): valid.append(l)
            else: invalid.append(l)
        self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(valid))
        self._count_phones(self.sms_phones, self.sms_count)
        messagebox.showinfo("Validation", f"Valid: {len(valid)}\nInvalid removed: {len(invalid)}")

    def _tool_sms_dedup(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        before = len(lines); seen = set(); out = []
        for l in lines:
            key = l.split(",",1)[0].strip()
            if key not in seen: seen.add(key); out.append(l)
        self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(out))
        self._count_phones(self.sms_phones, self.sms_count)
        messagebox.showinfo("Dedup", f"Before: {before}\nAfter: {len(out)}\nRemoved: {before-len(out)}")

    def _tool_sms_sort(self):
        if not hasattr(self, 'sms_phones'): return
        lines = sorted([l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()])
        self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(lines))

    def _tool_sms_shuffle(self):
        if not hasattr(self, 'sms_phones'): return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        random.shuffle(lines)
        self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(lines))

    def _tool_sms_format_cc(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        win = ctk.CTkToplevel(self); win.title("Format Country Code"); win.geometry("400x200"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Add country code prefix:", font=("Segoe UI",13), text_color=T["t1"]).pack(pady=(16,6))
        ce = ctk.CTkEntry(win, placeholder_text="+1", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); ce.pack(fill="x", padx=20, pady=4)
        def do():
            code = ce.get().strip()
            if not code: return
            if not code.startswith("+"): code = "+" + code
            lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
            out = []
            for l in lines:
                parts = l.split(",",1); phone = parts[0].strip()
                if not phone.startswith("+"): phone = code + phone.lstrip("0")
                out.append(f"{phone},{parts[1].strip()}" if len(parts)>1 else phone)
            self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(out))
            self._count_phones(self.sms_phones, self.sms_count)
            win.destroy(); messagebox.showinfo("Done", f"Formatted {len(out)} numbers")
        ctk.CTkButton(win, text="Apply", height=36, fg_color=T["sms_blue"], command=do).pack(pady=12)

    def _tool_sms_extract(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        win = ctk.CTkToplevel(self); win.title("Extract Phones"); win.geometry("450x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Paste text containing phone numbers:", font=("Segoe UI",13), text_color=T["t1"]).pack(pady=(12,4), anchor="w", padx=16)
        tb = ctk.CTkTextbox(win, height=180, font=("Consolas",12), fg_color=T["input_bg"], border_color=T["input_bd"], text_color=T["t1"])
        tb.pack(fill="both", expand=True, padx=16, pady=4)
        def do():
            text = tb.get("1.0","end")
            phones = re.findall(r'\+?\d[\d\s\-]{6,14}\d', text)
            phones = [re.sub(r'[\s\-]','',p) for p in phones]
            if phones:
                self.sms_phones.insert("end","\n".join(phones)+"\n")
                self._count_phones(self.sms_phones, self.sms_count)
                win.destroy(); messagebox.showinfo("Done", f"Extracted {len(phones)} phone numbers")
            else: messagebox.showwarning("","No phone numbers found.",parent=win)
        ctk.CTkButton(win, text="Extract & Add", height=36, fg_color=T["sms_blue"], command=do).pack(pady=8)

    def _tool_sms_merge(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        path = filedialog.askopenfilename(filetypes=[("Text","*.txt"),("CSV","*.csv"),("All","*.*")])
        if not path: return
        added = 0
        with open(path,"r",encoding="utf-8",errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line:
                    phone = re.sub(r'[\s\-\(\)]','',line.split(",")[0])
                    if re.match(r'^\+?\d{7,}$', phone):
                        self.sms_phones.insert("end", line+"\n"); added += 1
        self._count_phones(self.sms_phones, self.sms_count)
        messagebox.showinfo("Merge", f"Added {added} phone numbers from file.")

    def _tool_sms_count_phones(self):
        if not hasattr(self, 'sms_phones'): return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        messagebox.showinfo("Count", f"Total phone numbers: {len(lines)}")

    def _tool_sms_limit(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        win = ctk.CTkToplevel(self); win.title("Limit List"); win.geometry("350x160"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Max phone numbers to keep:", font=("Segoe UI",13), text_color=T["t1"]).pack(pady=(16,6))
        le = ctk.CTkEntry(win, placeholder_text="100", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); le.pack(fill="x", padx=20, pady=4)
        def do():
            try: n = int(le.get())
            except: return
            lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()][:n]
            self.sms_phones.delete("1.0","end"); self.sms_phones.insert("1.0","\n".join(lines))
            self._count_phones(self.sms_phones, self.sms_count); win.destroy()
        ctk.CTkButton(win, text="Apply", height=34, fg_color=T["sms_blue"], command=do).pack(pady=8)

    def _tool_sms_export(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt"),("CSV","*.csv")])
        if not path: return
        with open(path,"w",encoding="utf-8") as f: f.write("\n".join(lines))
        messagebox.showinfo("Export", f"Exported {len(lines)} numbers to:\n{path}")

    def _tool_sms_cost(self):
        if not hasattr(self, 'sms_phones'): messagebox.showwarning("","Load SMS page first."); return
        lines = [l.strip() for l in self.sms_phones.get("1.0","end").strip().splitlines() if l.strip()]
        msg = self.sms_message.get("1.0","end").strip() if hasattr(self, 'sms_message') else ""
        has_unicode = any(ord(c) > 127 for c in msg)
        chars = len(msg); limit = 70 if has_unicode else 160; multi = 67 if has_unicode else 153
        parts = 1 if chars <= limit else (chars + multi - 1) // multi
        total_sms = len(lines) * parts
        win = ctk.CTkToplevel(self); win.title("SMS Cost Estimator"); win.geometry("400x280"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="SMS Cost Estimator", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(16,8))
        ctk.CTkLabel(win, text=f"Recipients: {len(lines)}\nMessage parts per recipient: {parts}\n"
            f"Total SMS segments: {total_sms}", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20, pady=4)
        ctk.CTkLabel(win, text="Price per SMS segment:", font=("Segoe UI",12), text_color=T["t2"]).pack(anchor="w", padx=20)
        pe = ctk.CTkEntry(win, placeholder_text="0.01", fg_color=T["input_bg"], border_color=T["input_bd"], height=34); pe.pack(fill="x", padx=20, pady=4)
        pe.insert(0, "0.01")
        rl = ctk.CTkLabel(win, text="", font=("Segoe UI Semibold",14), text_color=T["accent"]); rl.pack(pady=8)
        def calc():
            try: price = float(pe.get())
            except: price = 0.01
            rl.configure(text=f"Estimated cost: ${total_sms * price:.2f} USD")
        ctk.CTkButton(win, text="Calculate", height=34, fg_color=T["sms_blue"], command=calc).pack()

    def _tool_sms_delivery_stats(self):
        if not self.log_data: messagebox.showinfo("","No sending data yet. Send some messages first."); return
        sms_logs = [e for e in self.log_data if e.get("channel") == "sms"]
        if not sms_logs: messagebox.showinfo("","No SMS sending data found."); return
        sent = sum(1 for e in sms_logs if e.get("status") == "sent")
        failed = sum(1 for e in sms_logs if e.get("status") == "failed")
        total = len(sms_logs)
        rate = (sent/total*100) if total else 0
        messagebox.showinfo("SMS Delivery Stats", f"Total SMS attempted: {total}\nSent: {sent}\nFailed: {failed}\n"
            f"Success rate: {rate:.1f}%")

    def _tool_sms_country_lookup(self):
        win = ctk.CTkToplevel(self); win.title("Country Code Lookup"); win.geometry("400x350"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Common Country Codes", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(pady=(12,6))
        codes = [
            ("+1","US/Canada"), ("+44","UK"), ("+33","France"), ("+49","Germany"), ("+34","Spain"),
            ("+39","Italy"), ("+81","Japan"), ("+86","China"), ("+91","India"), ("+55","Brazil"),
            ("+61","Australia"), ("+7","Russia"), ("+971","UAE"), ("+966","Saudi Arabia"), ("+212","Morocco"),
            ("+20","Egypt"), ("+234","Nigeria"), ("+27","South Africa"), ("+82","South Korea"), ("+90","Turkey"),
        ]
        sc = ctk.CTkScrollableFrame(win, fg_color="transparent"); sc.pack(fill="both", expand=True, padx=12, pady=8)
        for code, country in codes:
            f = ctk.CTkFrame(sc, fg_color=T["card"], corner_radius=6); f.pack(fill="x", pady=1)
            ctk.CTkLabel(f, text=f"  {code}", font=("Segoe UI Semibold",12), text_color=T["accent"], width=60).pack(side="left", padx=6, pady=5)
            ctk.CTkLabel(f, text=country, font=("Segoe UI",11), text_color=T["t1"]).pack(side="left")

    # ── Export Tools ──
    def _tool_export_emails(self):
        lines = self._lines()
        if not lines: messagebox.showwarning("","Email list is empty."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt"),("CSV","*.csv")])
        if not path: return
        with open(path,"w",encoding="utf-8") as f: f.write("\n".join(lines))
        messagebox.showinfo("Export", f"Exported {len(lines)} emails to:\n{path}")

    def _tool_export_phones(self):
        lines = self._wa_lines()
        if not lines: messagebox.showwarning("","Phone list is empty."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt"),("CSV","*.csv")])
        if not path: return
        with open(path,"w",encoding="utf-8") as f: f.write("\n".join(lines))
        messagebox.showinfo("Export", f"Exported {len(lines)} phone numbers to:\n{path}")

    def verify_emails(self): self._go_email_tab(1)
    def test_send(self):
        if not self.smtp_servers: messagebox.showwarning("","Configure SMTP on the SMTP page first."); return
        win = ctk.CTkToplevel(self); win.title("Test Send"); win.geometry("440x220"); win.transient(self)
        ctk.CTkLabel(win, text="📧 Test Email", font=("Segoe UI Semibold",15)).pack(pady=(16,8))
        te = ctk.CTkEntry(win, width=320, placeholder_text="test@email.com", fg_color=T["input_bg"], border_color=T["input_bd"]); te.pack()
        st = ctk.CTkLabel(win, text="", font=("Segoe UI",12)); st.pack(pady=6)
        def go():
            addr=te.get().strip()
            if not is_valid_email(addr): st.configure(text="Invalid",text_color=T["red"]); return
            st.configure(text="Sending...",text_color=T["orange"])
            cfg=self.smtp_servers[0]
            def _s():
                try:
                    v={"email":addr,"name":"Test","date":datetime.now().strftime("%Y-%m-%d"),"time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999)),"subject":self.subject_entry.get() or "Test"}
                    s, cfg = self._smtp_open_connection(cfg, timeout=15)
                    msg=MIMEMultipart(); frm=rv(self.from_email.get() or cfg["username"],v)
                    msg["From"]=frm; msg["To"]=addr; msg["Subject"]=f"[TEST] {rv(v['subject'],v)}"
                    msg.attach(MIMEText(rv(self.body.get("1.0","end").strip() or "Test.",v), "html" if self.content_type.get()=="html" else "plain","utf-8"))
                    s.sendmail(frm,addr,msg.as_string()); s.quit()
                    win.after(0, lambda: st.configure(text="Sent!",text_color=T["green"]))
                except Exception as ex:
                    err = self._smtp_pretty_error(ex, cfg if isinstance(cfg, dict) else None)
                    win.after(0, lambda e=err: st.configure(text=f"Failed: {e}",text_color=T["red"]))
            threading.Thread(target=_s, daemon=True).start()
        ctk.CTkButton(win, text="Send", width=160, command=go).pack(pady=8)

    # ═══════════════════════════════════════════════════════════
    #  EMAIL BODY TOOLBAR ACTIONS
    # ═══════════════════════════════════════════════════════════

    # ═══════════════════════════════════════════════════════════
    #  VISUAL EDITOR (WYSIWYG) HELPERS
    # ═══════════════════════════════════════════════════════════

    def _ve(self, command, value=None):
        """Execute a visual editor command (applies formatting)."""
        editor = self._visual_editor
        if self._body_visual_mode:
            try:
                sel = editor.get("sel.first", "sel.last")
                has_sel = True
            except: has_sel = False

            if command == "bold":
                if has_sel:
                    if "bold" in editor.tag_names("sel.first"):
                        editor.tag_remove("bold", "sel.first", "sel.last")
                    else:
                        editor.tag_add("bold", "sel.first", "sel.last")
            elif command == "italic":
                if has_sel:
                    if "italic" in editor.tag_names("sel.first"):
                        editor.tag_remove("italic", "sel.first", "sel.last")
                    else:
                        editor.tag_add("italic", "sel.first", "sel.last")
            elif command == "underline":
                if has_sel:
                    if "underline" in editor.tag_names("sel.first"):
                        editor.tag_remove("underline", "sel.first", "sel.last")
                    else:
                        editor.tag_add("underline", "sel.first", "sel.last")
            elif command in ("justifyCenter",):
                if has_sel:
                    editor.tag_add("center", "sel.first linestart", "sel.last lineend")
            elif command in ("justifyRight",):
                if has_sel:
                    editor.tag_add("right", "sel.first linestart", "sel.last lineend")
            elif command in ("justifyLeft", "justifyFull"):
                if has_sel:
                    for t in ("center","right"):
                        editor.tag_remove(t, "sel.first linestart", "sel.last lineend")
            elif command == "formatBlock":
                tag = value.strip("<>") if value else "p"
                if has_sel and tag in ("h1","h2","h3"):
                    for t in ("h1","h2","h3"):
                        editor.tag_remove(t, "sel.first", "sel.last")
                    editor.tag_add(tag, "sel.first", "sel.last")
            elif command == "insertUnorderedList":
                if has_sel:
                    lines = sel.split("\n")
                    editor.delete("sel.first","sel.last")
                    for ln in lines:
                        editor.insert("insert", f"  \u2022 {ln.strip()}\n")
                else:
                    editor.insert("insert", "  \u2022 ")
            elif command == "insertOrderedList":
                if has_sel:
                    lines = sel.split("\n")
                    editor.delete("sel.first","sel.last")
                    for i, ln in enumerate(lines, 1):
                        editor.insert("insert", f"  {i}. {ln.strip()}\n")
                else:
                    editor.insert("insert", "  1. ")
            elif command == "undo":
                try: editor.edit_undo()
                except: pass
            elif command == "redo":
                try: editor.edit_redo()
                except: pass
        else:
            if command == "bold": self._body_wrap("<b>","</b>")
            elif command == "italic": self._body_wrap("<i>","</i>")
            elif command == "underline": self._body_wrap("<u>","</u>")
            elif command == "justifyLeft": self._body_wrap('<div style="text-align:left;">','</div>')
            elif command == "justifyCenter": self._body_wrap('<div style="text-align:center;">','</div>')
            elif command == "justifyRight": self._body_wrap('<div style="text-align:right;">','</div>')
            elif command == "justifyFull": self._body_wrap('<div style="text-align:justify;">','</div>')
            elif command == "formatBlock":
                tag = value.strip("<>") if value else "p"
                self._body_wrap(f"<{tag}>", f"</{tag}>")
            elif command == "insertUnorderedList": self._body_ins_list("ul")
            elif command == "insertOrderedList": self._body_ins_list("ol")
            elif command == "undo": self._body_action("undo")
            elif command == "redo": self._body_action("redo")

    def _ve_link(self):
        if self._body_visual_mode:
            url = simpledialog.askstring("Insert Link", "Enter URL:", parent=self)
            if url:
                try:
                    sel = self._visual_editor.get("sel.first","sel.last")
                    self._visual_editor.delete("sel.first","sel.last")
                    pos = self._visual_editor.index("insert")
                    self._visual_editor.insert("insert", sel or url)
                    end = self._visual_editor.index("insert")
                    self._visual_editor.tag_add("link", pos, end)
                except:
                    pos = self._visual_editor.index("insert")
                    self._visual_editor.insert("insert", url)
                    end = self._visual_editor.index("insert")
                    self._visual_editor.tag_add("link", pos, end)
        else:
            self._body_ins_link()

    def _ve_image(self):
        if self._body_visual_mode:
            url = simpledialog.askstring("Insert Image", "Image URL:", parent=self)
            if url:
                self._visual_editor.insert("insert", f"[Image: {url}]")
        else:
            self._body_ins_image()

    def _ve_color(self):
        if self._body_visual_mode:
            col = simpledialog.askstring("Text Color", "Color hex (e.g. #ff0000):", parent=self)
            if col:
                try:
                    tag_name = f"fg_{col.replace('#','')}"
                    self._visual_editor.tag_configure(tag_name, foreground=col)
                    self._visual_editor.tag_add(tag_name, "sel.first", "sel.last")
                except: pass
        else:
            self._body_ins_color()

    def _ve_hilite(self):
        if self._body_visual_mode:
            col = simpledialog.askstring("Highlight", "Highlight hex (e.g. #ffff00):", parent=self)
            if col:
                try:
                    tag_name = f"bg_{col.replace('#','')}"
                    self._visual_editor.tag_configure(tag_name, background=col)
                    self._visual_editor.tag_add(tag_name, "sel.first", "sel.last")
                except: pass
        else:
            self._body_ins_bgcolor()

    def _ve_insert_text(self, text):
        if self._body_visual_mode:
            self._visual_editor.insert("insert", text)
        else:
            self.body.insert("insert", text)

    def _ve_clear(self):
        if self._body_visual_mode:
            self._visual_editor.delete("1.0","end")
        else:
            self.body.delete("1.0","end")

    def _body_set_content(self, html):
        """Set the full body content (clears and replaces) in the correct editor."""
        if self._body_visual_mode:
            self._visual_load(html)
        else:
            self.body.delete("1.0","end"); self.body.insert("1.0", html)

    def _get_body_html(self):
        """Get email body as HTML regardless of current mode."""
        if self._body_visual_mode:
            return self._visual_get_html()
        return self.body.get("1.0","end").strip()

    def _body_switch_mode(self):
        """Switch between HTML code mode and Visual (text) mode."""
        mode = self.content_type.get()
        if mode == "text" and not self._body_visual_mode:
            html = self.body.get("1.0","end-1c")
            self._visual_load(html)
            self.body.pack_forget()
            self._visual_frame.pack(fill="both", expand=True)
            self._body_visual_mode = True
            try: self._body_mode_lbl.configure(text="Visual")
            except: pass
        elif mode == "html" and self._body_visual_mode:
            html = self._visual_get_html()
            self._visual_frame.pack_forget()
            self.body.pack(fill="both", expand=True)
            self.body.delete("1.0","end"); self.body.insert("1.0", html)
            self._body_visual_mode = False
            try: self._body_mode_lbl.configure(text="HTML")
            except: pass

    def _visual_load(self, html):
        """Load HTML into the visual editor by stripping tags and showing plain text with formatting."""
        editor = self._visual_editor
        editor.delete("1.0","end")
        clean = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
        clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL|re.IGNORECASE)
        clean = re.sub(r'<br\s*/?>', '\n', clean, flags=re.IGNORECASE)
        clean = re.sub(r'</(p|div|h[1-6]|li|tr|blockquote)>', '\n', clean, flags=re.IGNORECASE)
        clean = re.sub(r'<[^>]+>', '', clean)
        clean = clean.replace("&nbsp;"," ").replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"')
        lines = [l.strip() for l in clean.split("\n")]
        text = "\n".join(l for l in lines if l or lines.index(l) == 0)
        while "\n\n\n" in text: text = text.replace("\n\n\n","\n\n")
        editor.insert("1.0", text.strip())

    def _visual_get_html(self):
        """Convert visual editor content back to HTML."""
        editor = self._visual_editor
        content = editor.get("1.0","end-1c")
        if not content.strip(): return ""

        result = []
        i = 0
        for line in content.split("\n"):
            if not line.strip():
                result.append("<br>")
                continue

            line_start = f"{i+1}.0"
            line_end = f"{i+1}.{len(line)}"
            tags_at = set()
            for pos in range(len(line)):
                tags_at.update(editor.tag_names(f"{i+1}.{pos}"))

            styled_line = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

            if "h1" in tags_at: styled_line = f"<h1>{styled_line}</h1>"
            elif "h2" in tags_at: styled_line = f"<h2>{styled_line}</h2>"
            elif "h3" in tags_at: styled_line = f"<h3>{styled_line}</h3>"
            else:
                if "bold" in tags_at: styled_line = f"<b>{styled_line}</b>"
                if "italic" in tags_at: styled_line = f"<i>{styled_line}</i>"
                if "underline" in tags_at: styled_line = f"<u>{styled_line}</u>"
                if "link" in tags_at: styled_line = f'<a href="#">{styled_line}</a>'
                if "center" in tags_at: styled_line = f'<div style="text-align:center;">{styled_line}</div>'
                elif "right" in tags_at: styled_line = f'<div style="text-align:right;">{styled_line}</div>'
                else: styled_line = f"<p>{styled_line}</p>"

            for t in tags_at:
                if t.startswith("fg_"):
                    col = "#" + t[3:]
                    styled_line = f'<span style="color:{col};">{styled_line}</span>'
                elif t.startswith("bg_"):
                    col = "#" + t[3:]
                    styled_line = f'<span style="background-color:{col};">{styled_line}</span>'

            result.append(styled_line)
            i += 1

        return "\n".join(result)

    def _body_open_file(self):
        path = filedialog.askopenfilename(filetypes=[("HTML","*.html *.htm"),("Text","*.txt"),("All","*.*")])
        if not path: return
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if self._body_visual_mode:
            self._visual_load(content)
        else:
            self.body.delete("1.0","end"); self.body.insert("1.0", content)

    def _body_save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".html",
                                             filetypes=[("HTML","*.html"),("Text","*.txt")])
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._get_body_html())
        messagebox.showinfo("Saved", f"File saved: {path}")

    def _body_ins_quick_table(self, rows, cols):
        html = '<table style="border-collapse:collapse;width:100%;">\n'
        html += '  <tr>' + ''.join(f'<th style="border:1px solid #ddd;padding:8px;background:#f2f2f2;">Header</th>' for _ in range(cols)) + '</tr>\n'
        for r in range(rows - 1):
            html += '  <tr>' + ''.join(f'<td style="border:1px solid #ddd;padding:8px;">Cell</td>' for _ in range(cols)) + '</tr>\n'
        html += '</table>\n'
        self._ve_insert_text(html)

    def _body_preview_browser(self):
        body = self._get_body_html()
        if not body: messagebox.showinfo("","Body is empty."); return
        is_html = True
        subj = self.subject_entry.get() if hasattr(self,'subject_entry') else "Preview"
        fname = self.from_name.get() if hasattr(self,'from_name') else ""
        femail = self.from_email.get() if hasattr(self,'from_email') else ""
        self._preview_open_browser(body, subj, fname, femail, is_html)

    def _body_action(self, action):
        try:
            ed = self._visual_editor if self._body_visual_mode else self.body
            if action == "undo":
                try:
                    if self._body_visual_mode: ed.edit_undo()
                    else: ed._textbox.edit_undo()
                except: pass
            elif action == "redo":
                try:
                    if self._body_visual_mode: ed.edit_redo()
                    else: ed._textbox.edit_redo()
                except: pass
            elif action == "cut":
                try:
                    sel = ed.get("sel.first","sel.last")
                    self.clipboard_clear(); self.clipboard_append(sel)
                    ed.delete("sel.first","sel.last")
                except: pass
            elif action == "copy":
                try:
                    sel = ed.get("sel.first","sel.last")
                    self.clipboard_clear(); self.clipboard_append(sel)
                except: pass
            elif action == "paste":
                try:
                    txt = self.clipboard_get()
                    try: ed.delete("sel.first","sel.last")
                    except: pass
                    ed.insert("insert", txt)
                except: pass
            elif action == "selectall":
                ed.tag_add("sel","1.0","end-1c")
        except: pass

    def _body_wrap(self, before, after):
        ed = self._visual_editor if self._body_visual_mode else self.body
        try:
            sel = ed.get("sel.first","sel.last")
            ed.delete("sel.first","sel.last")
            ed.insert("insert", before + sel + after)
        except:
            ed.insert("insert", before + after)

    def _body_find(self):
        win = ctk.CTkToplevel(self); win.title("Find"); win.geometry("380x120"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Find text:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,4), anchor="w")
        e = ctk.CTkEntry(win, height=34, font=("Segoe UI",12), fg_color=T["input_bg"],
                          border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        e.pack(fill="x", padx=16); e.focus_set()
        def _find(ev=None):
            term = e.get()
            if not term: return
            ed = self._visual_editor if self._body_visual_mode else self.body
            ed.tag_remove("found","1.0","end")
            content = ed.get("1.0","end")
            start = 0; count = 0
            while True:
                idx = content.find(term, start)
                if idx < 0: break
                line = content[:idx].count("\n") + 1
                col = idx - content.rfind("\n", 0, idx) - 1
                end_col = col + len(term)
                ed.tag_add("found", f"{line}.{col}", f"{line}.{end_col}")
                start = idx + 1; count += 1
            ed.tag_config("found", background="#fbbf24")
            win.title(f"Find - {count} matches")
        e.bind("<Return>", _find)
        ctk.CTkButton(win, text="Find All", height=30, fg_color=T["accent"], command=_find).pack(padx=16, pady=8, anchor="e")

    def _body_replace(self):
        win = ctk.CTkToplevel(self); win.title("Find & Replace"); win.geometry("400x180"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Find:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,2), anchor="w")
        e1 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        e1.pack(fill="x", padx=16); e1.focus_set()
        ctk.CTkLabel(win, text="Replace with:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(6,2), anchor="w")
        e2 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        e2.pack(fill="x", padx=16)
        def _replace():
            f = e1.get(); r = e2.get()
            if not f: return
            ed = self._visual_editor if self._body_visual_mode else self.body
            content = ed.get("1.0","end-1c")
            count = content.count(f)
            new = content.replace(f, r)
            ed.delete("1.0","end"); ed.insert("1.0", new)
            win.title(f"Replaced {count} occurrences")
        bf = ctk.CTkFrame(win, fg_color="transparent"); bf.pack(fill="x", padx=16, pady=8)
        ctk.CTkButton(bf, text="Replace All", height=30, fg_color=T["accent"], command=_replace).pack(side="right")

    def _body_word_count(self):
        ed = self._visual_editor if self._body_visual_mode else self.body
        txt = ed.get("1.0","end-1c")
        words = len(txt.split()); chars = len(txt); lines = txt.count("\n")+1
        tags = len(re.findall(r"<[^>]+>", txt)); links = len(re.findall(r"https?://[^\s<]+", txt))
        imgs = len(re.findall(r"<img[^>]*>", txt, re.I))
        messagebox.showinfo("Body Statistics",
            f"Characters: {chars:,}\nWords: {words:,}\nLines: {lines:,}\n"
            f"HTML Tags: {tags:,}\nLinks: {links:,}\nImages: {imgs:,}")

    def _body_ins_link(self):
        win = ctk.CTkToplevel(self); win.title("Insert Link"); win.geometry("400x200"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="URL:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,2), anchor="w")
        e1 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"], corner_radius=6)
        e1.pack(fill="x", padx=16); e1.insert(0,"https://"); e1.focus_set()
        ctk.CTkLabel(win, text="Text:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(6,2), anchor="w")
        e2 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"], corner_radius=6)
        e2.pack(fill="x", padx=16); e2.insert(0,"Click here")
        def _ins():
            url = e1.get(); txt = e2.get() or url
            self._ve_insert_text(f'<a href="{url}" style="color:#0066cc;text-decoration:underline;">{txt}</a>')
            win.destroy()
        ctk.CTkButton(win, text="Insert", height=32, fg_color=T["accent"], command=_ins).pack(padx=16, pady=10, anchor="e")

    def _body_ins_image(self):
        win = ctk.CTkToplevel(self); win.title("Insert Image"); win.geometry("420x220"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Image URL:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,2), anchor="w")
        e1 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"], corner_radius=6)
        e1.pack(fill="x", padx=16); e1.insert(0,"https://"); e1.focus_set()
        ctk.CTkLabel(win, text="Alt text:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(6,2), anchor="w")
        e2 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"], corner_radius=6)
        e2.pack(fill="x", padx=16); e2.insert(0,"Image")
        ctk.CTkLabel(win, text="Width:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(6,2), anchor="w")
        e3 = ctk.CTkEntry(win, height=32, width=100, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"], corner_radius=6)
        e3.pack(padx=16, anchor="w"); e3.insert(0,"600")
        def _ins():
            url = e1.get(); alt = e2.get(); w = e3.get()
            self._ve_insert_text(f'<img src="{url}" alt="{alt}" style="max-width:{w}px;display:block;" />')
            win.destroy()
        ctk.CTkButton(win, text="Insert", height=32, fg_color=T["accent"], command=_ins).pack(padx=16, pady=8, anchor="e")

    def _body_ins_table(self):
        win = ctk.CTkToplevel(self); win.title("Insert Table"); win.geometry("300x180"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        f = ctk.CTkFrame(win, fg_color="transparent"); f.pack(padx=16, pady=12)
        ctk.CTkLabel(f, text="Rows:", font=("Segoe UI",12), text_color=T["t1"]).pack(side="left")
        e1 = ctk.CTkEntry(f, width=60, height=30, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"]); e1.pack(side="left",padx=6); e1.insert(0,"3")
        ctk.CTkLabel(f, text="Cols:", font=("Segoe UI",12), text_color=T["t1"]).pack(side="left", padx=(12,0))
        e2 = ctk.CTkEntry(f, width=60, height=30, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"]); e2.pack(side="left",padx=6); e2.insert(0,"3")
        def _ins():
            rows = int(e1.get() or 3); cols = int(e2.get() or 3)
            html = '<table style="border-collapse:collapse;width:100%;">\n'
            html += '  <tr>' + ''.join(f'<th style="border:1px solid #ddd;padding:8px;background:#f2f2f2;">Header</th>' for _ in range(cols)) + '</tr>\n'
            for r in range(rows-1):
                html += '  <tr>' + ''.join(f'<td style="border:1px solid #ddd;padding:8px;">Cell</td>' for _ in range(cols)) + '</tr>\n'
            html += '</table>\n'
            self._ve_insert_text(html); win.destroy()
        ctk.CTkButton(win, text="Insert Table", height=32, fg_color=T["accent"], command=_ins).pack(padx=16, pady=10)

    def _body_ins_list(self, tag):
        html = f"<{tag}>\n  <li>Item 1</li>\n  <li>Item 2</li>\n  <li>Item 3</li>\n</{tag}>\n"
        self._ve_insert_text(html)

    def _body_ins_button(self):
        win = ctk.CTkToplevel(self); win.title("Insert Button"); win.geometry("400x200"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Button Text:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,2), anchor="w")
        e1 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"]); e1.pack(fill="x", padx=16); e1.insert(0,"Click Here")
        ctk.CTkLabel(win, text="URL:", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(6,2), anchor="w")
        e2 = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                           border_color=T["input_bd"], text_color=T["t1"]); e2.pack(fill="x", padx=16); e2.insert(0,"https://")
        colvar = ctk.StringVar(value="#0066cc")
        cf = ctk.CTkFrame(win, fg_color="transparent"); cf.pack(padx=16, pady=6, anchor="w")
        ctk.CTkLabel(cf, text="Color:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        for c in ["#0066cc","#e74c3c","#27ae60","#8e44ad","#f39c12","#333333"]:
            ctk.CTkButton(cf, text="", width=22, height=22, fg_color=c, hover_color=c, corner_radius=4,
                           command=lambda x=c: colvar.set(x)).pack(side="left", padx=2)
        def _ins():
            txt = e1.get(); url = e2.get(); col = colvar.get()
            html = (f'<a href="{url}" style="background-color:{col};color:#ffffff;padding:12px 24px;'
                    f'text-decoration:none;border-radius:6px;font-weight:bold;display:inline-block;">{txt}</a>\n')
            self._ve_insert_text(html); win.destroy()
        ctk.CTkButton(win, text="Insert", height=32, fg_color=T["accent"], command=_ins).pack(padx=16, anchor="e")

    def _body_ins_color(self):
        win = ctk.CTkToplevel(self); win.title("Color Text"); win.geometry("340x130"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Color (hex):", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,4), anchor="w")
        e = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                          border_color=T["input_bd"], text_color=T["t1"]); e.pack(fill="x", padx=16); e.insert(0,"#ff0000")
        def _ins():
            self._body_wrap(f'<span style="color:{e.get()};">', '</span>'); win.destroy()
        ctk.CTkButton(win, text="Apply", height=30, fg_color=T["accent"], command=_ins).pack(padx=16, pady=8, anchor="e")

    def _body_ins_fontsize(self):
        win = ctk.CTkToplevel(self); win.title("Font Size"); win.geometry("300x130"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="Size (px):", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,4), anchor="w")
        e = ctk.CTkEntry(win, height=32, width=80, font=("Segoe UI",12), fg_color=T["input_bg"],
                          border_color=T["input_bd"], text_color=T["t1"]); e.pack(padx=16, anchor="w"); e.insert(0,"16")
        def _ins():
            self._body_wrap(f'<span style="font-size:{e.get()}px;">', '</span>'); win.destroy()
        ctk.CTkButton(win, text="Apply", height=30, fg_color=T["accent"], command=_ins).pack(padx=16, pady=8, anchor="e")

    def _body_ins_bgcolor(self):
        win = ctk.CTkToplevel(self); win.title("Background Color"); win.geometry("340x130"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.grab_set()
        ctk.CTkLabel(win, text="BG Color (hex):", font=("Segoe UI",12), text_color=T["t1"]).pack(padx=16, pady=(12,4), anchor="w")
        e = ctk.CTkEntry(win, height=32, font=("Segoe UI",12), fg_color=T["input_bg"],
                          border_color=T["input_bd"], text_color=T["t1"]); e.pack(fill="x", padx=16); e.insert(0,"#ffff00")
        def _ins():
            self._body_wrap(f'<span style="background-color:{e.get()};">', '</span>'); win.destroy()
        ctk.CTkButton(win, text="Apply", height=30, fg_color=T["accent"], command=_ins).pack(padx=16, pady=8, anchor="e")

    def _body_ins_section(self):
        html = ('<div style="padding:20px;margin:10px 0;background:#f9f9f9;border-radius:8px;">\n'
                '  <h2>Section Title</h2>\n  <p>Your content here.</p>\n</div>\n')
        self._ve_insert_text(html)

    def _body_ins_columns(self):
        html = ('<!--[if mso]><table role="presentation" width="100%"><tr><td width="50%" valign="top"><![endif]-->\n'
                '<div style="display:inline-block;width:48%;vertical-align:top;">\n  <p>Column 1</p>\n</div>\n'
                '<div style="display:inline-block;width:48%;vertical-align:top;">\n  <p>Column 2</p>\n</div>\n'
                '<!--[if mso]></td></tr></table><![endif]-->\n')
        self._ve_insert_text(html)

    def _body_minify(self):
        if self._body_visual_mode:
            messagebox.showinfo("","Switch to HTML mode to minify."); return
        txt = self.body.get("1.0","end-1c")
        txt = re.sub(r'\s+', ' ', txt).replace("> <","><").strip()
        self.body.delete("1.0","end"); self.body.insert("1.0", txt)

    def _body_beautify(self):
        if self._body_visual_mode:
            messagebox.showinfo("","Switch to HTML mode to beautify."); return
        txt = self.body.get("1.0","end-1c")
        indent = 0; result = []
        tags = re.split(r'(<[^>]+>)', txt)
        for part in tags:
            s = part.strip()
            if not s: continue
            if s.startswith("</"):
                indent = max(0, indent - 1)
                result.append("  " * indent + s)
            elif s.startswith("<") and not s.endswith("/>") and not s.startswith("<!"):
                result.append("  " * indent + s)
                if not any(s.startswith(f"<{t}") for t in ["br","hr","img","input","meta","link"]):
                    indent += 1
            else:
                if s: result.append("  " * indent + s)
        self.body.delete("1.0","end"); self.body.insert("1.0", "\n".join(result))

    def _body_strip_tags(self):
        ed = self._visual_editor if self._body_visual_mode else self.body
        txt = ed.get("1.0","end-1c")
        clean = re.sub(r'<[^>]+>', '', txt)
        clean = re.sub(r'\s+', ' ', clean).strip()
        ed.delete("1.0","end"); ed.insert("1.0", clean)

    def _body_encode_html(self):
        if self._body_visual_mode:
            messagebox.showinfo("","Switch to HTML mode to encode."); return
        txt = self.body.get("1.0","end-1c")
        txt = txt.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        self.body.delete("1.0","end"); self.body.insert("1.0", txt)

    def _body_decode_html(self):
        if self._body_visual_mode:
            messagebox.showinfo("","Switch to HTML mode to decode."); return
        txt = self.body.get("1.0","end-1c")
        txt = txt.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"').replace("&nbsp;"," ")
        self.body.delete("1.0","end"); self.body.insert("1.0", txt)

    def _body_lorem(self):
        lorem = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore "
                 "et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
                 "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
                 "cillum dolore eu fugiat nulla pariatur.")
        self._ve_insert_text(lorem)

    def _body_wrap_full_html(self):
        if self._body_visual_mode:
            messagebox.showinfo("","Switch to HTML mode to wrap in full HTML."); return
        txt = self.body.get("1.0","end-1c")
        if txt.strip().lower().startswith(("<!doctype","<html")):
            messagebox.showinfo("","Body already contains HTML document."); return
        html = ('<!DOCTYPE html>\n<html>\n<head>\n  <meta charset="utf-8">\n'
                '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                '  <title>Email</title>\n  <style>\n    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }\n'
                '  </style>\n</head>\n<body>\n' + txt + '\n</body>\n</html>')
        self.body.delete("1.0","end"); self.body.insert("1.0", html)

    def _body_email_scaffold(self):
        html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;">
    <tr>
      <td align="center" style="padding:20px 0;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="padding:30px;background-color:#0066cc;text-align:center;">
              <h1 style="color:#ffffff;margin:0;font-size:24px;">Your Company</h1>
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td style="padding:30px;">
              <h2 style="color:#333;margin-top:0;">Hello {{name}},</h2>
              <p style="color:#555;line-height:1.6;">Your email content goes here.</p>
              <a href="#" style="background-color:#0066cc;color:#fff;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;font-weight:bold;">Call to Action</a>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:20px 30px;background-color:#f8f8f8;text-align:center;">
              <p style="color:#999;font-size:12px;margin:0;">Company Name | Address | <a href="{{unsub_url}}">Unsubscribe</a></p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''
        self._body_set_content(html)

    def _body_responsive_tpl(self):
        html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email</title>
  <style>
    @media only screen and (max-width: 600px) {
      .container { width: 100% !important; }
      .col { width: 100% !important; display: block !important; }
      .mobile-center { text-align: center !important; }
      .mobile-pad { padding: 15px !important; }
    }
  </style>
</head>
<body style="margin:0;padding:0;background:#eef2f7;font-family:'Segoe UI',Arial,sans-serif;">
  <table role="presentation" class="container" width="600" align="center" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;margin:20px auto;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <tr>
      <td style="padding:40px 30px;background:linear-gradient(135deg,#667eea,#764ba2);text-align:center;" class="mobile-pad">
        <h1 style="color:#fff;margin:0;font-size:28px;">Welcome, {{name}}!</h1>
        <p style="color:rgba(255,255,255,0.85);font-size:14px;">We're glad to have you on board.</p>
      </td>
    </tr>
    <tr>
      <td style="padding:30px;" class="mobile-pad">
        <p style="color:#444;line-height:1.7;font-size:15px;">Your responsive email content here. This template adapts to mobile screens automatically.</p>
        <table role="presentation" width="100%">
          <tr>
            <td class="col" width="48%" style="padding:10px;vertical-align:top;">
              <div style="background:#f7f8fc;padding:20px;border-radius:8px;">
                <h3 style="color:#333;margin-top:0;">Feature 1</h3>
                <p style="color:#666;font-size:13px;">Description here.</p>
              </div>
            </td>
            <td class="col" width="48%" style="padding:10px;vertical-align:top;">
              <div style="background:#f7f8fc;padding:20px;border-radius:8px;">
                <h3 style="color:#333;margin-top:0;">Feature 2</h3>
                <p style="color:#666;font-size:13px;">Description here.</p>
              </div>
            </td>
          </tr>
        </table>
        <div style="text-align:center;padding:20px 0;">
          <a href="#" style="background:#667eea;color:#fff;padding:14px 32px;text-decoration:none;border-radius:8px;font-weight:bold;font-size:15px;">Get Started</a>
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding:20px 30px;background:#f8f9fb;text-align:center;border-top:1px solid #eee;">
        <p style="color:#aaa;font-size:11px;margin:0;">&copy; 2026 Company | <a href="{{unsub_url}}" style="color:#888;">Unsubscribe</a></p>
      </td>
    </tr>
  </table>
</body>
</html>'''
        self._body_set_content(html)

    def _body_dark_mode_tpl(self):
        html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <style>
    :root { color-scheme: light dark; }
    @media (prefers-color-scheme: dark) {
      .bg-main { background-color: #1a1a2e !important; }
      .bg-card { background-color: #16213e !important; }
      .text-main { color: #e0e0e0 !important; }
      .text-sub { color: #aaa !important; }
      .text-head { color: #ffffff !important; }
    }
  </style>
</head>
<body style="margin:0;padding:0;font-family:'Segoe UI',Arial,sans-serif;">
  <table role="presentation" class="bg-main" width="100%" style="background-color:#f4f4f4;">
    <tr>
      <td align="center" style="padding:20px;">
        <table role="presentation" class="bg-card" width="600" style="background-color:#ffffff;border-radius:12px;overflow:hidden;">
          <tr>
            <td style="padding:30px;background:#0f3460;text-align:center;">
              <h1 class="text-head" style="color:#fff;margin:0;">Dark Mode Ready</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:30px;">
              <h2 class="text-main" style="color:#333;">Hello {{name}},</h2>
              <p class="text-sub" style="color:#555;line-height:1.7;">This email supports dark mode automatically. Email clients that support dark mode will show the dark version.</p>
              <a href="#" style="background:#e94560;color:#fff;padding:12px 28px;text-decoration:none;border-radius:6px;display:inline-block;font-weight:bold;">Take Action</a>
            </td>
          </tr>
          <tr>
            <td style="padding:20px;text-align:center;background:#f8f8f8;">
              <p class="text-sub" style="color:#999;font-size:11px;">&copy; 2026 | <a href="{{unsub_url}}" style="color:#888;">Unsubscribe</a></p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''
        self._body_set_content(html)

    # ── Inline HTML Preview (separate card below body) ──────────
    def _toggle_inline_preview(self):
        if self._inline_preview_visible:
            for w in self._inline_preview_card.winfo_children(): w.destroy()
            self._inline_preview_card.pack_forget()
            self._inline_preview_visible = False
            self._preview_btn.configure(text="Preview", fg_color=T["accent"])
        else:
            self._render_inline_preview()
            self._inline_preview_card.pack(fill="x", pady=3, after=self._body_card)
            self._inline_preview_visible = True
            self._preview_btn.configure(text="Hide Preview", fg_color=T["green"])

    def _render_inline_preview(self):
        for w in self._inline_preview_card.winfo_children(): w.destroy()
        body_raw = self.body.get("1.0","end").strip()

        toolbar = ctk.CTkFrame(self._inline_preview_card, fg_color=T["surface2"], corner_radius=0)
        toolbar.pack(fill="x")
        ctk.CTkLabel(toolbar, text="  HTML Preview", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(side="left", padx=8, pady=6)

        is_html = self.content_type.get() == "html"
        v = {"email":"user@example.com","name":"John Doe","date":datetime.now().strftime("%Y-%m-%d"),
             "time":datetime.now().strftime("%H:%M:%S"),"random":"48271"}

        ctk.CTkButton(toolbar, text="Refresh", height=26, width=70, font=("Segoe UI",10),
                       fg_color=T["accent"], hover_color=T["accent_h"], corner_radius=5,
                       command=self._render_inline_preview).pack(side="right", padx=4, pady=6)

        if body_raw:
            body_html = rv(body_raw, v)
            ctk.CTkButton(toolbar, text="Open in Browser", height=26, width=110, font=("Segoe UI",10),
                           fg_color=T["card_h"], hover_color=T["border_l"], corner_radius=5,
                           command=lambda bh=body_html: self._preview_open_browser(bh,
                               self.subject_entry.get() or "Preview",
                               self.from_name.get() or "Sender",
                               self.from_email.get() or "sender@email.com", is_html)).pack(side="right", padx=2, pady=6)

        if not body_raw:
            ctk.CTkLabel(self._inline_preview_card, text="  Email body is empty. Write some HTML above, then click Refresh.",
                          font=("Segoe UI",11), text_color=T["t3"]).pack(anchor="w", padx=14, pady=16)
            return

        body_html = rv(body_raw, v)
        content = ctk.CTkFrame(self._inline_preview_card, fg_color="transparent")
        content.pack(fill="both", expand=True)

        if is_html:
            is_full_doc = bool(re.search(r'<html[\s>]|<!doctype', body_html, re.IGNORECASE))
            if is_full_doc:
                wrapper = body_html
            else:
                wrapper = f'''<html><head><meta charset="utf-8">
                <style>body{{font-family:Arial,sans-serif;margin:0;padding:20px;background:#ffffff;color:#333;line-height:1.6;}}
                img{{max-width:100%;height:auto;}} a{{color:#2563eb;}} table{{border-collapse:collapse;width:100%;}}
                td,th{{padding:8px;}} *{{box-sizing:border-box;}}</style></head>
                <body>{body_html}</body></html>'''
            try:
                from tkinterweb import HtmlFrame
                frame = HtmlFrame(content, messages_enabled=False)
                frame.load_html(wrapper)
                frame.pack(fill="both", expand=True, padx=6, pady=6)
                return
            except ImportError:
                pass

            from tkinter import Text
            text_widget = Text(content, wrap="word", bg="#ffffff", fg="#333333",
                               font=("Segoe UI",12), relief="flat", padx=20, pady=20,
                               insertbackground="#333333", selectbackground="#b3d4fc",
                               height=16, borderwidth=0, highlightthickness=0)
            text_widget.pack(fill="both", expand=True, padx=8, pady=(4,8))

            clean = re.sub(r'<style[^>]*>.*?</style>', '', body_html, flags=re.DOTALL)
            clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL)
            parts = re.split(r'(<[^>]+>)', clean)
            bold_on = False; italic_on = False; size_stack = [12]; tag_counter = [0]
            link_text = None
            for part in parts:
                if part.startswith("<"):
                    tl = part.lower()
                    if re.match(r'<h[1-3][ >]', tl):
                        text_widget.insert("end","\n"); bold_on = True
                        size_stack.append(20 if "h1" in tl else 16 if "h2" in tl else 14)
                    elif re.match(r'</h[1-3]>', tl):
                        bold_on = False; text_widget.insert("end","\n\n")
                        if len(size_stack)>1: size_stack.pop()
                    elif tl.startswith("<b") or tl.startswith("<strong"): bold_on = True
                    elif tl.startswith("</b") or tl.startswith("</strong"): bold_on = False
                    elif tl.startswith("<i") or tl.startswith("<em"): italic_on = True
                    elif tl.startswith("</i") or tl.startswith("</em"): italic_on = False
                    elif tl.startswith("<br"): text_widget.insert("end","\n")
                    elif tl.startswith("<p"): text_widget.insert("end","\n")
                    elif tl.startswith("</p"): text_widget.insert("end","\n")
                    elif tl.startswith("<hr"): text_widget.insert("end","\n" + "─"*50 + "\n")
                    elif tl.startswith("<li"): text_widget.insert("end","\n  •  ")
                    elif tl.startswith("<a "): href=re.search(r'href=["\']([^"\']*)',part); link_text=href.group(1) if href else ""
                    elif tl.startswith("</a"): link_text = None
                    elif tl.startswith("<img"):
                        alt=re.search(r'alt=["\']([^"\']*)',part)
                        text_widget.insert("end",f" [Image: {alt.group(1) if alt else 'image'}] ")
                    elif tl.startswith("<div") or tl.startswith("<tr"): text_widget.insert("end","\n")
                    elif tl.startswith("<td") or tl.startswith("<th"): text_widget.insert("end","   ")
                else:
                    decoded = re.sub(r'&nbsp;',' ',part); decoded = re.sub(r'&amp;','&',decoded)
                    decoded = re.sub(r'&lt;','<',decoded); decoded = re.sub(r'&gt;','>',decoded)
                    decoded = re.sub(r'&#\d+;','',decoded); decoded = decoded.strip()
                    if not decoded: continue
                    tn = f"ip{tag_counter[0]}"; tag_counter[0] += 1
                    wt = "bold" if bold_on else "normal"
                    sl = "italic" if italic_on else "roman"
                    sz = size_stack[-1] if size_stack else 12
                    fg = "#2563eb" if link_text else "#333333"
                    text_widget.tag_configure(tn, font=("Segoe UI",sz,wt,sl), foreground=fg)
                    if link_text: text_widget.tag_configure(tn, underline=True)
                    text_widget.insert("end", decoded+" ", tn)
            text_widget.configure(state="disabled")
            ctk.CTkLabel(content, text="Tip: pip install tkinterweb for pixel-perfect HTML rendering",
                          font=("Segoe UI",9), text_color=T["t4"]).pack(anchor="w", padx=12, pady=(0,6))
        else:
            tb = ctk.CTkTextbox(content, font=("Consolas",12),
                                 fg_color="#ffffff", text_color="#333333", corner_radius=6, height=180)
            tb.pack(fill="both", expand=True, padx=8, pady=8)
            tb.insert("1.0", body_html); tb.configure(state="disabled")

    def preview_email(self):
        body_raw = self.body.get("1.0","end").strip()
        if not body_raw: messagebox.showwarning("","Email body is empty."); return
        v = {"email":"user@example.com","name":"John Doe","date":datetime.now().strftime("%Y-%m-%d"),
             "time":datetime.now().strftime("%H:%M:%S"),"random":"48271",
             "subject":self.subject_entry.get() or "Test Subject"}
        from_name = rv(self.from_name.get() or "Sender", v)
        from_email = rv(self.from_email.get() or "sender@email.com", v)
        subject = rv(v["subject"], v)
        body_html = rv(body_raw, v)
        is_html = self.content_type.get() == "html"

        win = ctk.CTkToplevel(self); win.title("Email Preview"); win.geometry("900x700"); win.transient(self)
        win.configure(fg_color=T["bg"])

        top = ctk.CTkFrame(win, fg_color=T["surface"], height=44); top.pack(fill="x")
        self._preview_mode = ctk.StringVar(value="render")
        for val, lbl in [("render","👁 Visual Preview"),("code","</> HTML Code"),("browser","🌐 Open in Browser")]:
            ctk.CTkButton(top, text=lbl, height=34, font=("Segoe UI",12),
                           fg_color=T["accent"] if val=="render" else "transparent",
                           hover_color=T["accent_h"], corner_radius=8,
                           command=lambda v=val, w=win, bh=body_html, s=subject, fn=from_name, fe=from_email, ih=is_html:
                               self._preview_switch(w, v, bh, s, fn, fe, ih)).pack(side="left", padx=4, pady=5)

        # ── Email header info ──
        hdr = ctk.CTkFrame(win, fg_color=T["surface2"], corner_radius=0); hdr.pack(fill="x")
        hdr_info = [
            ("From:", f"{from_name} <{from_email}>"),
            ("To:", "user@example.com"),
            ("Subject:", subject),
        ]
        for label, value in hdr_info:
            row = ctk.CTkFrame(hdr, fg_color="transparent"); row.pack(fill="x", padx=16, pady=1)
            ctk.CTkLabel(row, text=label, font=("Segoe UI",10,"bold"), text_color=T["t3"], width=60, anchor="e").pack(side="left")
            ctk.CTkLabel(row, text=f"  {value}", font=("Segoe UI",11), text_color=T["t1"]).pack(side="left")
        ctk.CTkFrame(hdr, height=1, fg_color=T["border"]).pack(fill="x", pady=(4,0))

        # ── Preview content area ──
        self._preview_container = ctk.CTkFrame(win, fg_color="transparent")
        self._preview_container.pack(fill="both", expand=True)
        self._preview_show_render(self._preview_container, body_html, is_html)

    def _preview_switch(self, win, mode, body_html, subject, from_name, from_email, is_html):
        for w in self._preview_container.winfo_children(): w.destroy()
        if mode == "render":
            self._preview_show_render(self._preview_container, body_html, is_html)
        elif mode == "code":
            self._preview_show_code(self._preview_container, body_html)
        elif mode == "browser":
            self._preview_open_browser(body_html, subject, from_name, from_email, is_html)

    def _preview_show_render(self, parent, body_html, is_html):
        if is_html:
            is_full_doc = bool(re.search(r'<html[\s>]|<!doctype', body_html, re.IGNORECASE))
            if is_full_doc:
                wrapper = body_html
            else:
                wrapper = f'''<html><head><meta charset="utf-8">
                <style>body{{font-family:Arial,sans-serif;margin:0;padding:20px;background:#ffffff;color:#333;}}
                img{{max-width:100%;height:auto;}} a{{color:#2563eb;}} table{{border-collapse:collapse;}}
                td,th{{padding:8px;}} *{{box-sizing:border-box;}}</style></head>
                <body>{body_html}</body></html>'''

            try:
                from tkinterweb import HtmlFrame
                frame = HtmlFrame(parent, messages_enabled=False)
                frame.load_html(wrapper)
                frame.pack(fill="both", expand=True, padx=8, pady=8)
                return
            except ImportError:
                pass

            from tkinter import Text
            text_widget = Text(parent, wrap="word", bg="#ffffff", fg="#333333",
                               font=("Segoe UI", 12), relief="flat", padx=20, pady=20,
                               insertbackground="#333333", selectbackground="#b3d4fc")
            text_widget.pack(fill="both", expand=True, padx=8, pady=8)

            clean = re.sub(r'<style[^>]*>.*?</style>', '', body_html, flags=re.DOTALL)
            clean = re.sub(r'<script[^>]*>.*?</script>', '', clean, flags=re.DOTALL)

            parts = re.split(r'(<[^>]+>)', clean)
            bold_on = False; italic_on = False; color_stack = ["#333333"]; size_stack = [12]
            link_text = None; tag_counter = [0]

            for part in parts:
                if part.startswith("<"):
                    tag_lower = part.lower()
                    if re.match(r'<h[1-3][ >]', tag_lower):
                        text_widget.insert("end", "\n")
                        bold_on = True; size_stack.append(18 if "h1" in tag_lower else 15 if "h2" in tag_lower else 13)
                    elif re.match(r'</h[1-3]>', tag_lower):
                        bold_on = False; text_widget.insert("end", "\n\n")
                        if len(size_stack) > 1: size_stack.pop()
                    elif tag_lower.startswith("<b") or tag_lower.startswith("<strong"): bold_on = True
                    elif tag_lower.startswith("</b") or tag_lower.startswith("</strong"): bold_on = False
                    elif tag_lower.startswith("<i") or tag_lower.startswith("<em"): italic_on = True
                    elif tag_lower.startswith("</i") or tag_lower.startswith("</em"): italic_on = False
                    elif tag_lower.startswith("<br"): text_widget.insert("end", "\n")
                    elif tag_lower.startswith("<p"): text_widget.insert("end", "\n")
                    elif tag_lower.startswith("</p"): text_widget.insert("end", "\n")
                    elif tag_lower.startswith("<hr"): text_widget.insert("end", "\n" + "─"*50 + "\n")
                    elif tag_lower.startswith("<li"): text_widget.insert("end", "\n  • ")
                    elif tag_lower.startswith("<a "):
                        href = re.search(r'href=["\']([^"\']*)', part)
                        link_text = href.group(1) if href else ""
                    elif tag_lower.startswith("</a"): link_text = None
                    elif tag_lower.startswith("<img"):
                        alt = re.search(r'alt=["\']([^"\']*)', part)
                        text_widget.insert("end", f"[Image: {alt.group(1) if alt else 'image'}]")
                    elif tag_lower.startswith("<div") or tag_lower.startswith("<tr"): text_widget.insert("end", "\n")
                    elif tag_lower.startswith("<td") or tag_lower.startswith("<th"): text_widget.insert("end", "  ")
                else:
                    decoded = re.sub(r'&nbsp;', ' ', part)
                    decoded = re.sub(r'&amp;', '&', decoded)
                    decoded = re.sub(r'&lt;', '<', decoded)
                    decoded = re.sub(r'&gt;', '>', decoded)
                    decoded = re.sub(r'&#\d+;', '', decoded)
                    decoded = decoded.strip()
                    if not decoded: continue

                    tag_name = f"t{tag_counter[0]}"; tag_counter[0] += 1
                    weight = "bold" if bold_on else "normal"
                    slant = "italic" if italic_on else "roman"
                    sz = size_stack[-1] if size_stack else 12
                    fg = "#2563eb" if link_text else color_stack[-1]
                    text_widget.tag_configure(tag_name, font=("Segoe UI", sz, weight, slant), foreground=fg)
                    if link_text:
                        text_widget.tag_configure(tag_name, underline=True)
                    text_widget.insert("end", decoded + " ", tag_name)

            text_widget.configure(state="disabled")

            info = ctk.CTkLabel(parent, text="💡 Install 'tkinterweb' for full HTML rendering:  pip install tkinterweb",
                                 font=("Segoe UI",11), text_color=T["t3"])
            info.pack(anchor="w", padx=12, pady=(0,6))
        else:
            tb = ctk.CTkTextbox(parent, font=("Consolas",13), fg_color="#ffffff", text_color="#333333",
                                 corner_radius=8)
            tb.pack(fill="both", expand=True, padx=8, pady=8)
            tb.insert("1.0", body_html); tb.configure(state="disabled")

    def _preview_show_code(self, parent, body_html):
        tb = ctk.CTkTextbox(parent, font=("Consolas",12), fg_color=T["input_bg"], text_color=T["t1"],
                             corner_radius=8)
        tb.pack(fill="both", expand=True, padx=8, pady=8)
        tb.insert("1.0", body_html)
        tb.configure(state="disabled")

    def _preview_open_browser(self, body_html, subject, from_name, from_email, is_html):
        is_full_doc = is_html and bool(re.search(r'<html[\s>]|<!doctype', body_html, re.IGNORECASE))
        if is_full_doc:
            full_html = body_html
        else:
            full_html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>{subject}</title>
            <style>
                body {{ font-family: -apple-system, Arial, sans-serif; margin:0; background:#f0f0f0; }}
                .omni-env {{ max-width:700px; margin:30px auto; background:#fff; border-radius:12px;
                             box-shadow:0 4px 20px rgba(0,0,0,0.1); overflow:hidden; }}
                .omni-hdr {{ background:#1c2231; color:#fff; padding:20px 30px; }}
                .omni-hdr .omni-f {{ font-size:14px; color:#aaa; }}
                .omni-hdr .omni-s {{ font-size:20px; font-weight:bold; margin-top:6px; }}
                .omni-meta {{ padding:15px 30px; background:#f8f8fc; border-bottom:1px solid #e8e8f0; font-size:13px; color:#666; }}
                .omni-meta span {{ color:#333; font-weight:600; }}
                .omni-body {{ padding:30px; }}
                .omni-body img {{ max-width:100%; height:auto; }}
            </style></head><body>
            <div class="omni-env">
                <div class="omni-hdr">
                    <div class="omni-f">From: {from_name} &lt;{from_email}&gt;</div>
                    <div class="omni-s">{subject}</div>
                </div>
                <div class="omni-meta">To: <span>user@example.com</span> &nbsp;•&nbsp; {datetime.now().strftime("%B %d, %Y at %H:%M")}</div>
                <div class="omni-body">{"" if is_html else "<pre style='white-space:pre-wrap;font-family:inherit;'>"}{body_html}{"" if is_html else "</pre>"}</div>
            </div></body></html>'''

        tmp = os.path.join(tempfile.gettempdir(), "omnisend_preview.html")
        with open(tmp, "w", encoding="utf-8") as f: f.write(full_html)
        webbrowser.open(f"file://{tmp}")
        self.log("Preview opened in browser", "info")

    def open_templates(self):
        self._open_template_manager("email", self.body, content_type_var=self.content_type)

    def open_wa_templates(self):
        self._open_template_manager("whatsapp", self.wa_message)

    def open_sms_templates(self):
        self._open_template_manager("sms", self.sms_message)

    def _tpl_list(self, channel):
        d = TPL_DIRS[channel]
        out = []
        for f in sorted(os.listdir(d)):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(d,f),"r",encoding="utf-8") as fh:
                        data = json.load(fh)
                    out.append({"file":f, "name":data.get("name",f[:-5]), "body":data.get("body",""),
                                "content_type":data.get("content_type","html")})
                except: pass
        return out

    def _tpl_save(self, channel, name, body, content_type="html"):
        safe = re.sub(r'[^\w\s-]','',name).strip().replace(' ','_')
        if not safe: return
        path = os.path.join(TPL_DIRS[channel], f"{safe}.json")
        with open(path,"w",encoding="utf-8") as f:
            json.dump({"name":name,"body":body,"content_type":content_type}, f, ensure_ascii=False, indent=2)

    def _tpl_delete(self, channel, filename):
        path = os.path.join(TPL_DIRS[channel], filename)
        if os.path.exists(path): os.remove(path)

    def _open_template_manager(self, channel, target_textbox, content_type_var=None):
        colors = {"email":T["accent"], "whatsapp":T["wa_green"], "sms":T["sms_blue"], "telegram":T["tg_blue"]}
        titles = {"email":"Email Templates", "whatsapp":"WhatsApp Templates", "sms":"SMS Templates", "telegram":"Telegram Templates"}
        accent = colors.get(channel, T["accent"])

        win = ctk.CTkToplevel(self); win.title(titles[channel]); win.geometry("620x560"); win.transient(self)
        win.configure(fg_color=T["bg"])

        hdr = ctk.CTkFrame(win, fg_color=T["surface"], corner_radius=0); hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=f"  {titles[channel]}", font=("Segoe UI Semibold",16), text_color=T["t1"]).pack(side="left", padx=12, pady=14)

        # ── Save current as template ──
        save_fr = ctk.CTkFrame(win, fg_color=T["card"], corner_radius=8); save_fr.pack(fill="x", padx=16, pady=(12,6))
        ctk.CTkLabel(save_fr, text="Save Current as Template", font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(anchor="w", padx=14, pady=(10,4))
        sf_row = ctk.CTkFrame(save_fr, fg_color="transparent"); sf_row.pack(fill="x", padx=14, pady=(0,10))
        tpl_name_entry = ctk.CTkEntry(sf_row, placeholder_text="Template name...", height=34,
                                       font=("Segoe UI",12), fg_color=T["input_bg"],
                                       border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        tpl_name_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        def _do_save():
            name = tpl_name_entry.get().strip()
            if not name: messagebox.showwarning("","Enter a template name.",parent=win); return
            body = target_textbox.get("1.0","end").strip()
            if not body: messagebox.showwarning("","Message body is empty.",parent=win); return
            ct = content_type_var.get() if content_type_var else "text"
            self._tpl_save(channel, name, body, ct)
            tpl_name_entry.delete(0,"end")
            _refresh_list()
            messagebox.showinfo("Saved", f"Template '{name}' saved!", parent=win)
        ctk.CTkButton(sf_row, text="Save", height=34, width=80, font=("Segoe UI",12,"bold"),
                       fg_color=accent, hover_color=T["accent_h"], corner_radius=6,
                       command=_do_save).pack(side="right")

        # ── Built-in templates ──
        builtin = {"email": TEMPLATES, "whatsapp": WA_TEMPLATES, "sms": SMS_TEMPLATES, "telegram": TG_TEMPLATES}.get(channel, {})
        if builtin:
            bi_fr = ctk.CTkFrame(win, fg_color=T["card"], corner_radius=8); bi_fr.pack(fill="x", padx=16, pady=(6,4))
            ctk.CTkLabel(bi_fr, text="Built-in Templates", font=("Segoe UI Semibold",11), text_color=T["t3"]).pack(anchor="w", padx=14, pady=(8,4))
            bi_inner = ctk.CTkFrame(bi_fr, fg_color="transparent"); bi_inner.pack(fill="x", padx=10, pady=(0,8))
            for bname, bbody in builtin.items():
                bf = ctk.CTkFrame(bi_inner, fg_color=T["card_h"], corner_radius=6); bf.pack(fill="x", padx=4, pady=1)
                ctk.CTkLabel(bf, text=f"  {bname}", font=("Segoe UI",11), text_color=T["t1"]).pack(side="left", padx=6, pady=6)
                ctk.CTkButton(bf, text="Use", width=50, height=24, font=("Segoe UI",10),
                               fg_color=accent, hover_color=T["accent_h"], corner_radius=5,
                               command=lambda h=bbody: [target_textbox.delete("1.0","end"), target_textbox.insert("1.0",h),
                                   content_type_var.set("html") if content_type_var else None, win.destroy()]
                               ).pack(side="right", padx=8, pady=6)

        # ── Saved templates list ──
        list_label = ctk.CTkLabel(win, text="  Your Saved Templates", font=("Segoe UI Semibold",12), text_color=T["t1"])
        list_label.pack(anchor="w", padx=16, pady=(8,2))
        list_container = ctk.CTkScrollableFrame(win, fg_color="transparent", scrollbar_button_color=T["border"])
        list_container.pack(fill="both", expand=True, padx=16, pady=(0,12))

        def _refresh_list():
            for w in list_container.winfo_children(): w.destroy()
            templates = self._tpl_list(channel)
            if not templates:
                ctk.CTkLabel(list_container, text="No saved templates yet.\nSave your first template above!",
                              font=("Segoe UI",12), text_color=T["t3"]).pack(pady=20)
                return
            for tpl in templates:
                row = ctk.CTkFrame(list_container, fg_color=T["card"], corner_radius=8,
                                    border_width=1, border_color=T["border"])
                row.pack(fill="x", pady=2)
                left = ctk.CTkFrame(row, fg_color="transparent"); left.pack(side="left", fill="x", expand=True, padx=10, pady=8)
                ctk.CTkLabel(left, text=tpl["name"], font=("Segoe UI Semibold",12), text_color=T["t1"]).pack(anchor="w")
                preview = tpl["body"][:80].replace("\n"," ")
                if len(tpl["body"])>80: preview += "..."
                ctk.CTkLabel(left, text=preview, font=("Segoe UI",10), text_color=T["t4"]).pack(anchor="w")

                btns = ctk.CTkFrame(row, fg_color="transparent"); btns.pack(side="right", padx=8, pady=8)
                ctk.CTkButton(btns, text="Use", width=50, height=26, font=("Segoe UI",10),
                               fg_color=accent, hover_color=T["accent_h"], corner_radius=5,
                               command=lambda t=tpl: [target_textbox.delete("1.0","end"), target_textbox.insert("1.0",t["body"]),
                                   content_type_var.set(t["content_type"]) if content_type_var else None, win.destroy()]
                               ).pack(side="left", padx=2)
                ctk.CTkButton(btns, text="Preview", width=60, height=26, font=("Segoe UI",10),
                               fg_color=T["card_h"], hover_color=T["border_l"], corner_radius=5,
                               command=lambda t=tpl: self._tpl_preview(t, channel)
                               ).pack(side="left", padx=2)
                ctk.CTkButton(btns, text="X", width=28, height=26, font=("Segoe UI",10),
                               fg_color=T["red_bg"], hover_color=T["red"], text_color=T["red"], corner_radius=5,
                               command=lambda t=tpl: [self._tpl_delete(channel, t["file"]), _refresh_list()]
                               ).pack(side="left", padx=2)

        _refresh_list()

    def _tpl_preview(self, tpl, channel):
        win = ctk.CTkToplevel(self); win.title(f"Preview: {tpl['name']}"); win.geometry("550x420"); win.transient(self)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text=tpl["name"], font=("Segoe UI Semibold",15), text_color=T["t1"]).pack(padx=16, pady=(12,4), anchor="w")
        if channel == "email" and tpl.get("content_type") == "html":
            wrapper = f'''<html><head><meta charset="utf-8">
            <style>body{{font-family:Arial;margin:0;padding:16px;background:#fff;color:#333;}}
            img{{max-width:100%;}} a{{color:#2563eb;}} table{{border-collapse:collapse;}}</style></head>
            <body>{tpl["body"]}</body></html>'''
            try:
                from tkinterweb import HtmlFrame
                frame = HtmlFrame(win, messages_enabled=False)
                frame.load_html(wrapper); frame.pack(fill="both", expand=True, padx=12, pady=(0,12))
                return
            except ImportError: pass
        tb = ctk.CTkTextbox(win, font=("Consolas",12), fg_color=T["input_bg"], text_color=T["t1"], corner_radius=8)
        tb.pack(fill="both", expand=True, padx=12, pady=(0,12))
        tb.insert("1.0", tpl["body"]); tb.configure(state="disabled")

    # ═══════════════════════════════════════════════════════════
    #  CAMPAIGN SAVE/LOAD
    # ═══════════════════════════════════════════════════════════
    def save_campaign(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", initialdir=DATA_DIR, filetypes=[("JSON","*.json")])
        if not path: return
        d = {"smtp":self.smtp_servers,"from_name":self.from_name.get(),"from_email":self.from_email.get(),
             "subject":self.subject_entry.get(),"reply_to":self.reply_to.get(),"cc":self.cc_field.get(),"bcc":self.bcc_field.get(),
             "body":self.body.get("1.0","end").strip(),"content_type":self.content_type.get(),
             "recipients":self.recipients_box.get("1.0","end").strip(),
             "multi_subjects":self.multi_subjects.get("1.0","end").strip(),
             "wa_phones":self.wa_phones.get("1.0","end").strip(),"wa_message":self.wa_message.get("1.0","end").strip(),
             "sms_phones":self.sms_phones.get("1.0","end").strip(),"sms_message":self.sms_message.get("1.0","end").strip(),
             "tg_chat_ids":self.tg_chat_ids.get("1.0","end").strip() if hasattr(self,'tg_chat_ids') else "",
             "tg_message":self.tg_message.get("1.0","end").strip() if hasattr(self,'tg_message') else "",
             "tg_bot_token":self.tg_bot_token.get().strip() if hasattr(self,'tg_bot_token') else "",
             "delay_min":self.delay_min.get(),"delay_max":self.delay_max.get(),"threads":self.thread_count.get()}
        with open(path,"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)
        messagebox.showinfo("Saved","Campaign saved!")

    def load_campaign(self):
        path = filedialog.askopenfilename(initialdir=DATA_DIR, filetypes=[("JSON","*.json")])
        if not path: return
        try:
            with open(path,"r",encoding="utf-8") as f: d = json.load(f)
            self.smtp_servers = self._smtp_normalize_servers(d.get("smtp",[]))
            self._smtp_render_list()
            for e,k in [(self.from_name,"from_name"),(self.from_email,"from_email"),(self.subject_entry,"subject"),
                         (self.reply_to,"reply_to"),(self.cc_field,"cc"),(self.bcc_field,"bcc"),
                         (self.delay_min,"delay_min"),(self.delay_max,"delay_max"),(self.thread_count,"threads")]:
                e.delete(0,"end"); e.insert(0,d.get(k,""))
            self.content_type.set(d.get("content_type","html"))
            tg_pairs = []
            if hasattr(self,'tg_chat_ids'): tg_pairs.append((self.tg_chat_ids,"tg_chat_ids"))
            if hasattr(self,'tg_message'): tg_pairs.append((self.tg_message,"tg_message"))
            if hasattr(self,'tg_bot_token') and d.get("tg_bot_token"):
                self.tg_bot_token.delete(0,"end"); self.tg_bot_token.insert(0,d.get("tg_bot_token",""))
            for tb,k in [(self.body,"body"),(self.recipients_box,"recipients"),(self.multi_subjects,"multi_subjects"),
                          (self.wa_phones,"wa_phones"),(self.wa_message,"wa_message"),
                          (self.sms_phones,"sms_phones"),(self.sms_message,"sms_message")] + tg_pairs:
                tb.delete("1.0","end"); tb.insert("1.0",d.get(k,""))
            self._update_email_count(); messagebox.showinfo("Loaded","Campaign loaded!")
        except Exception as e: messagebox.showerror("Error",str(e))

    def export_log(self):
        if not self.log_data: messagebox.showinfo("","No data."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path,"w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["Time","Target","Channel","Status","Error"])
            for e in self.log_data: w.writerow([e.get("time"),e.get("target"),e.get("channel"),e.get("status"),e.get("error","")])
        messagebox.showinfo("Done",f"Exported {len(self.log_data)} entries.")

    # ═══════════════════════════════════════════════════════════
    #  SENDING ENGINE
    # ═══════════════════════════════════════════════════════════
    def toggle_sending(self):
        if self.sending: self.sending = False; return

        # Detect active channel
        current = 0
        for i, (btn, dot, c) in enumerate(self._nav):
            if btn.cget("fg_color") == T["sidebar_sel"]: current = i; break

        if current == 0: self._send_email()
        elif current == 1: self._send_whatsapp()
        elif current == 2: self._send_sms()
        elif current == 3: self._send_telegram()
        else: self._send_email()

    def _pre_send(self):
        self.sending = True; self.sent_count = 0; self.failed_count = 0; self.log_data = []
        self.progress_bar.set(0)
        self.log_box.configure(state="normal"); self.log_box.delete("1.0","end"); self.log_box.configure(state="disabled")
        self._send_start = time.time()
        self.send_btn.configure(text="STOP", fg_color=T["red"], hover_color=T["red_h"])
        self.status_txt.configure(text="  Sending...")
        self._go(4)

    def _post_send(self):
        s,f = self.sent_count, self.failed_count
        msg = "Complete!" if self.sending else "Stopped."
        self.after(0, lambda: self.log(f"{msg}  Sent: {s}  Failed: {f}", "info"))
        self.after(0, lambda: self.send_btn.configure(text="START SENDING", fg_color=T["green"], hover_color=T["green_h"]))
        self.after(0, lambda: self.status_txt.configure(text="  Ready"))
        self.sending = False

    def _delay(self):
        try: d_min=float(self.delay_min.get() or 0)
        except: d_min=0
        try: d_max=float(self.delay_max.get() or 0)
        except: d_max=0
        if d_max>0: time.sleep(random.uniform(d_min, d_max))
        elif d_min>0: time.sleep(d_min)

    def _progress(self, done, total):
        elapsed = time.time()-self._send_start
        spd = done/elapsed if elapsed>0 else 0
        eta = (total-done)/spd if spd>0 else 0
        pct = done/total if total>0 else 0
        es = f"{int(eta)}s" if eta<120 else f"{int(eta/60)}m"
        self.after(0, lambda: [self.progress_bar.set(pct),
            self.prog_lbl.configure(text=f"{done}/{total} ({int(pct*100)}%)"),
            self.speed_lbl.configure(text=f"Speed: {spd:.1f}/s • ETA: {es}"),
            self._badges["sent"].configure(text=str(self.sent_count)),
            self._badges["failed"].configure(text=str(self.failed_count)),
            self._badges["total"].configure(text=str(total))])

    # ── ULTRAMAILER-STYLE HELPERS ─────────────────────────────

    _XMAILERS = ["Microsoft Outlook 16.0","Thunderbird 115.0","Apple Mail","The Bat! 11.0",
                  "Postfix","Evolution 3.48","MailMate 1.14","em Client 9.2","Claws Mail 4.2",
                  "Zimbra 8.8","Roundcube 1.6","Mutt 2.2","Alpine 2.26","KMail 23.08"]

    def _resolve_mx(self, domain):
        if not HAS_DNS: return None
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_hosts = sorted(answers, key=lambda r: r.preference)
            return str(mx_hosts[0].exchange).rstrip('.')
        except: return None

    def _send_direct_mx(self, from_addr, to_addr, msg_str, helo_domain=""):
        domain = to_addr.split("@")[1]
        mx_host = self._resolve_mx(domain)
        if not mx_host: raise Exception(f"No MX record for {domain}")
        s = smtplib.SMTP(mx_host, 25, timeout=30)
        if helo_domain: s.ehlo(helo_domain)
        s.sendmail(from_addr, [to_addr], msg_str)
        s.quit()

    def _make_msgid_custom(self, from_email):
        if self.rand_msgid_var.get():
            domains = [from_email.split("@")[1] if "@" in from_email else "mail.local",
                       "outlook.com","mail.com","send.local","mx.local"]
            d = random.choice(domains)
            return f"<{uuid.uuid4().hex[:16]}.{random.randint(1000,9999)}@{d}>"
        return make_msgid()

    def _html_to_plain(self, html):
        text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<br\s*/?>','\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>','\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</div>','\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</h[1-6]>','\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</li>','\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<li[^>]*>', '  - ', text, flags=re.IGNORECASE)
        links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, re.IGNORECASE|re.DOTALL)
        for url, label in links:
            clean_label = re.sub(r'<[^>]+>', '', label).strip()
            text = text.replace(f'<a', f'[LINK_REPLACE]{url}[/LINK_REPLACE]<a', 1)
        text = re.sub(r'<[^>]+>', '', text)
        for url, label in links:
            clean_label = re.sub(r'<[^>]+>', '', label).strip()
            text = text.replace(f'[LINK_REPLACE]{url}[/LINK_REPLACE]', f'{clean_label} ({url})', 1)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _build_email_msg(self, fn, fe, su, bd, rp, params, v, rec):
        is_html = params["ct"] == "html"
        auto_text = self.auto_text_var.get()

        if is_html and auto_text:
            msg = MIMEMultipart("alternative")
            plain = self._html_to_plain(bd)
            msg.attach(MIMEText(plain, "plain", "utf-8"))
            msg.attach(MIMEText(bd, "html", "utf-8"))
            if params["atts"]:
                outer = MIMEMultipart("mixed")
                outer.attach(msg)
                msg = outer
        else:
            msg = MIMEMultipart("mixed")
            msg.attach(MIMEText(bd, "html" if is_html else "plain", "utf-8"))

        msg["From"] = f"{fn} <{fe}>" if fn else fe
        msg["To"] = rec["email"]
        msg["Subject"] = su

        if self.rand_date_var.get():
            from email.utils import format_datetime
            import datetime as dt
            now = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=random.randint(-30, 30))
            msg["Date"] = format_datetime(now)
        else:
            msg["Date"] = formatdate(localtime=True)

        msg["Message-ID"] = self._make_msgid_custom(fe)

        if rp: msg["Reply-To"] = rp
        if params["cc"]: msg["Cc"] = ", ".join(params["cc"])

        rpath = self.return_path.get().strip()
        if rpath: msg["Return-Path"] = rv(rpath, v)

        xp = self.x_priority.get()
        if xp and xp != "None":
            msg["X-Priority"] = xp[0]
            if xp[0] in ("1","2"): msg["Importance"] = "high"

        if self.rand_xmailer_var.get():
            msg["X-Mailer"] = random.choice(self._XMAILERS)

        for k, val in params["hdrs"].items():
            msg[k] = rv(val, v)

        if not (is_html and auto_text and params["atts"]):
            for att in params["atts"]:
                if os.path.exists(att["path"]):
                    with open(att["path"], "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f'attachment; filename="{att["filename"]}"')
                        msg.attach(part)

        return msg

    # ── EMAIL SENDING (UltraMailer-enhanced) ──────────────────
    def _send_email(self):
        use_mx = self.direct_mx_var.get()
        if not use_mx:
            self.smtp_servers = self._smtp_normalize_servers(self.smtp_servers)
        if not use_mx and not self.smtp_servers:
            messagebox.showwarning("","Add SMTP servers or enable Direct MX."); return
        raw = self.recipients_box.get("1.0","end").strip()
        if not raw: messagebox.showwarning("","Add recipients."); return
        recs = parse_emails(raw)
        if not recs: messagebox.showwarning("","No valid emails."); return
        self._pre_send()

        try: thr=max(1,int(self.thread_count.get() or 1))
        except: thr=1
        msubs=[s.strip() for s in self.multi_subjects.get("1.0","end").strip().splitlines() if s.strip()]
        hdrs = {}
        for line in self.headers_box.get("1.0","end").strip().splitlines():
            if ":" in line: k,v=line.split(":",1); hdrs[k.strip()]=v.strip()

        params = {"fn":self.from_name.get(),"fe":self.from_email.get(),"subj":self.subject_entry.get(),
                  "msubs":msubs,"reply":self.reply_to.get(),"body":self._get_body_html(),
                  "ct":"html" if self._body_visual_mode else self.content_type.get(),
                  "cc":[x.strip() for x in self.cc_field.get().split(",") if x.strip()],
                  "bcc":[x.strip() for x in self.bcc_field.get().split(",") if x.strip()],
                  "atts":list(self.attachments),"hdrs":hdrs}

        do_throttle = self.domain_throttle_var.get()
        try: max_pd = int(self.max_per_domain.get() or 50)
        except: max_pd = 50
        try: pause_s = int(self.domain_pause.get() or 300)
        except: pause_s = 300
        do_retry = self.retry_var.get()
        try: max_retry = int(self.retry_max.get() or 3)
        except: max_retry = 3
        helo = self.helo_domain.get().strip()

        def worker():
            total = len(recs); lock = threading.Lock(); si=[0]; sc_count=[0]; done=[0]
            rotate=self.rotate_var.get()
            try: epp=int(self.emails_per_smtp.get() or 50)
            except: epp=50
            domain_counts = {}

            mode = "Direct MX" if use_mx else f"SMTP ({len(self.smtp_servers)} servers)"
            self.after(0, lambda: self.log(f"Email: {total} recipients, {thr} threads, {mode}", "info"))

            def get_cfg():
                if use_mx: return None
                with lock:
                    cfg=self.smtp_servers[si[0]%len(self.smtp_servers)]
                    sc_count[0]+=1
                    if rotate and epp>0 and sc_count[0]>=epp: sc_count[0]=0; si[0]+=1
                    return cfg

            def check_domain_throttle(email):
                if not do_throttle: return
                domain = email.split("@")[1].lower() if "@" in email else ""
                with lock:
                    cnt = domain_counts.get(domain, 0)
                    if cnt >= max_pd:
                        self.after(0, lambda d=domain: self.log(f"  Throttle: {d} limit reached, pausing {pause_s}s", "warn"))
                        domain_counts[domain] = 0
                        time.sleep(pause_s)
                    domain_counts[domain] = domain_counts.get(domain, 0) + 1

            def send(rec, retry_num=0):
                if not self.sending: return
                check_domain_throttle(rec["email"])
                cfg = get_cfg()
                try:
                    v={"email":rec["email"],"name":rec.get("name",""),"date":datetime.now().strftime("%Y-%m-%d"),
                       "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999)),
                       "domain":rec["email"].split("@")[1] if "@" in rec["email"] else "",
                       "uuid":uuid.uuid4().hex[:8],"rand6":str(random.randint(100000,999999)),
                       "rand_name":random.choice(["Alex","Sam","Jordan","Taylor","Morgan","Casey","Riley","Quinn"])}
                    subj=random.choice(params["msubs"]) if params["msubs"] else params["subj"]
                    v["subject"]=subj
                    base_fn = params["fn"]
                    if self._sender_names: base_fn = random.choice(self._sender_names)
                    base_fe = params["fe"] or (cfg["username"] if cfg else "sender@local")
                    if self._from_emails: base_fe = random.choice(self._from_emails)
                    fn=rv(base_fn,v); fe=rv(base_fe,v)
                    su=rv(subj,v); bd=rv(params["body"],v)
                    base_rp = params["reply"]
                    if self._reply_tos: base_rp = random.choice(self._reply_tos)
                    rp=rv(base_rp,v) if base_rp else ""

                    msg = self._build_email_msg(fn, fe, su, bd, rp, params, v, rec)

                    if use_mx:
                        self._send_direct_mx(fe, rec["email"], msg.as_string(), helo)
                    else:
                        s, cfg = self._smtp_open_connection(cfg, timeout=30, helo=helo)
                        s.sendmail(fe,[rec["email"]]+params["cc"]+params["bcc"],msg.as_string()); s.quit()

                    with lock: self.sent_count+=1; done[0]+=1; self.log_data.append({"time":datetime.now().strftime("%H:%M:%S"),"target":rec["email"],"channel":"email","status":"sent","error":""})
                    self.after(0, lambda e=rec["email"]: self.log(f"✓ {e}","sent"))
                except Exception as ex:
                    err = self._smtp_pretty_error(ex, cfg if isinstance(cfg, dict) else None)
                    if do_retry and retry_num < max_retry:
                        self.after(0, lambda e=rec["email"],r=retry_num+1: self.log(f"  Retry {r}/{max_retry}: {e}","retry"))
                        time.sleep(2)
                        if not use_mx and len(self.smtp_servers) > 1:
                            with lock: si[0] += 1
                        send(rec, retry_num + 1)
                        return
                    with lock: self.failed_count+=1; done[0]+=1; self.log_data.append({"time":datetime.now().strftime("%H:%M:%S"),"target":rec["email"],"channel":"email","status":"failed","error":err})
                    self.after(0, lambda e=rec["email"],er=err: self.log(f"✗ {e} ({er})","failed"))
                self._progress(done[0], total); self._delay()

            if thr<=1:
                for r in recs:
                    if not self.sending: break
                    send(r)
            else:
                with ThreadPoolExecutor(max_workers=thr) as ex:
                    futs=[ex.submit(send,r) for r in recs if self.sending]
                    for f in as_completed(futs):
                        if not self.sending: break
            self._post_send()

        threading.Thread(target=worker, daemon=True).start()

    # ── WHATSAPP SENDING ─────────────────────────────────────
    def _send_whatsapp(self):
        if not hasattr(self, 'wa_phones'):
            messagebox.showwarning("","Go to WhatsApp page first to set up."); return
        raw = self.wa_phones.get("1.0","end").strip()
        if not raw: messagebox.showwarning("","Add phone numbers."); return
        msg_text = self.wa_message.get("1.0","end").strip()
        if not msg_text: messagebox.showwarning("","Write a message."); return
        recs = parse_phones(raw)
        if not recs: messagebox.showwarning("","No valid numbers."); return

        mode = self.wa_mode.get()

        if mode == "web":
            if not self.wa_connected or not self.wa_driver:
                messagebox.showwarning("Not Connected",
                    "Connect to WhatsApp Web first!\nClick 'Connect WhatsApp' and scan the QR code.")
                return

        self._pre_send()
        img_url = self.wa_image_url.get().strip()

        try:
            web_delay = max(2, int(self.wa_web_delay.get() or 5))
        except:
            web_delay = 5

        def worker():
            total = len(recs); done = [0]
            self.after(0, lambda: self.log(f"💬 WhatsApp: {total} numbers ({mode})", "wa"))

            for rec in recs:
                if not self.sending: break
                phone = rec["phone"]; name = rec.get("name","")
                v = {"phone":phone,"name":name,"date":datetime.now().strftime("%Y-%m-%d"),
                     "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
                actual_msg = rv(msg_text, v)
                ts = datetime.now().strftime("%H:%M:%S")

                try:
                    if mode == "web":
                        self.after(0, lambda p=phone,d=done[0],t=total: self.log(f"→ Sending to {p}  ({d+1}/{t})...", "info"))
                        self._wa_web_send_message(phone, actual_msg)
                        self.sent_count += 1
                        self.log_data.append({"time":ts,"target":phone,"channel":"whatsapp-web","status":"sent","error":""})
                        self.after(0, lambda p=phone: self.log(f"✓ {p} — Sent!", "wa"))
                        if done[0] + 1 < total:
                            self.after(0, lambda d=web_delay: self.log(f"⏳ Waiting {d}s...", "info"))
                            time.sleep(web_delay)

                    elif mode == "business":
                        pid = self.wa_phone_id.get().strip()
                        token = self.wa_token.get().strip()
                        url = f"https://graph.facebook.com/v21.0/{pid}/messages"
                        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

                        if img_url:
                            data = {"messaging_product":"whatsapp","to":phone,"type":"image",
                                    "image":{"link": rv(img_url, v), "caption": actual_msg}}
                        else:
                            data = {"messaging_product":"whatsapp","to":phone,"type":"text",
                                    "text":{"body":actual_msg}}

                        body = json.dumps(data).encode("utf-8")
                        req = Request(url, data=body, headers=headers, method="POST")
                        resp = urlopen(req, timeout=30)
                        if resp.status < 300:
                            self.sent_count += 1
                            self.log_data.append({"time":ts,"target":phone,"channel":"whatsapp","status":"sent","error":""})
                            self.after(0, lambda p=phone: self.log(f"✓ {p}","wa"))
                        else: raise Exception(f"HTTP {resp.status}")
                    else:
                        api_url = self.wa_api_url.get().strip()
                        api_key = self.wa_api_key.get().strip()
                        phone_param = self.wa_param_phone.get().strip() or "phone"
                        msg_param = self.wa_param_msg.get().strip() or "message"
                        key_param = self.wa_param_key.get().strip() or "api_key"

                        data = {phone_param: phone, msg_param: actual_msg, key_param: api_key}
                        if self.wa_sender.get().strip():
                            data["sender"] = self.wa_sender.get().strip()

                        body = json.dumps(data).encode("utf-8")
                        req = Request(api_url, data=body, headers={"Content-Type":"application/json"}, method="POST")
                        resp = urlopen(req, timeout=30)
                        self.sent_count += 1
                        self.log_data.append({"time":ts,"target":phone,"channel":"whatsapp","status":"sent","error":""})
                        self.after(0, lambda p=phone: self.log(f"✓ {p}","wa"))

                except Exception as ex:
                    self.failed_count += 1
                    err_msg = str(ex)
                    if "invalid" in err_msg.lower() and "number" in err_msg.lower():
                        err_msg = "Invalid phone number"
                    self.log_data.append({"time":ts,"target":phone,"channel":"whatsapp","status":"failed","error":err_msg})
                    self.after(0, lambda p=phone,er=err_msg: self.log(f"✗ {p} ({er})","failed"))

                done[0] += 1; self._progress(done[0], total)
                if mode != "web": self._delay()

            self._post_send()

        threading.Thread(target=worker, daemon=True).start()

    # ── SMS SENDING ──────────────────────────────────────────
    def _send_sms(self):
        if not hasattr(self, 'sms_phones'):
            messagebox.showwarning("","Go to SMS page first to set up."); return
        raw = self.sms_phones.get("1.0","end").strip()
        if not raw: messagebox.showwarning("","Add phone numbers."); return
        msg_text = self.sms_message.get("1.0","end").strip()
        if not msg_text: messagebox.showwarning("","Write a message."); return
        recs = parse_phones(raw)
        if not recs: messagebox.showwarning("","No valid numbers."); return
        self._pre_send()

        mode = self.sms_mode.get()

        def worker():
            total = len(recs); done = [0]
            self.after(0, lambda: self.log(f"📱 SMS: {total} numbers ({mode})", "sms"))

            for rec in recs:
                if not self.sending: break
                phone = rec["phone"]; name = rec.get("name","")
                v = {"phone":phone,"name":name,"date":datetime.now().strftime("%Y-%m-%d"),
                     "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
                actual_msg = rv(msg_text, v)
                ts = datetime.now().strftime("%H:%M:%S")

                try:
                    if mode == "twilio":
                        sid = self.tw_sid.get().strip()
                        token = self.tw_token.get().strip()
                        from_num = self.tw_from.get().strip()
                        url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"

                        data = urlencode({"From":from_num,"To":phone,"Body":actual_msg}).encode("utf-8")
                        auth = base64.b64encode(f"{sid}:{token}".encode()).decode()
                        req = Request(url, data=data, headers={"Authorization":f"Basic {auth}"}, method="POST")
                        resp = urlopen(req, timeout=30)
                        result = json.loads(resp.read().decode())

                        if result.get("sid"):
                            self.sent_count += 1
                            self.log_data.append({"time":ts,"target":phone,"channel":"sms","status":"sent","error":""})
                            self.after(0, lambda p=phone: self.log(f"✓ {p}","sms"))
                        else: raise Exception(result.get("message","Unknown error"))
                    else:
                        api_url = self.sms_api_url.get().strip()
                        api_key = self.sms_api_key.get().strip()
                        to_param = self.sms_to_param.get().strip() or "to"
                        msg_param = self.sms_msg_param.get().strip() or "message"
                        key_param = self.sms_key_param.get().strip() or "api_key"
                        from_param = self.sms_from_param.get().strip() or "from"

                        data = {to_param:phone, msg_param:actual_msg, key_param:api_key}
                        if from_param: data[from_param] = self.tw_from.get().strip() if self.tw_from.get().strip() else ""

                        body = json.dumps(data).encode("utf-8")
                        req = Request(api_url, data=body, headers={"Content-Type":"application/json"}, method="POST")
                        resp = urlopen(req, timeout=30)
                        self.sent_count += 1
                        self.log_data.append({"time":ts,"target":phone,"channel":"sms","status":"sent","error":""})
                        self.after(0, lambda p=phone: self.log(f"✓ {p}","sms"))

                except Exception as ex:
                    self.failed_count += 1
                    self.log_data.append({"time":ts,"target":phone,"channel":"sms","status":"failed","error":str(ex)})
                    self.after(0, lambda p=phone,er=str(ex): self.log(f"✗ {p} ({er})","failed"))

                done[0] += 1; self._progress(done[0], total); self._delay()

            self._post_send()

        threading.Thread(target=worker, daemon=True).start()

    # ── TELEGRAM SENDING ────────────────────────────────────
    def _send_telegram(self):
        if not hasattr(self, 'tg_chat_ids'):
            messagebox.showwarning("","Go to Telegram page first to set up."); return
        mode = self.tg_mode.get()
        raw = self.tg_chat_ids.get("1.0","end").strip()
        if not raw: messagebox.showwarning("","Add recipients."); return
        msg_text = self.tg_message.get("1.0","end").strip()
        media_type = self.tg_media_type.get()
        media_url = self.tg_media_url.get().strip() if hasattr(self,'tg_media_url') else ""
        if not msg_text and media_type == "none":
            messagebox.showwarning("","Write a message or attach media."); return

        if mode == "web":
            if not self.tg_web_connected or not self.tg_web_driver:
                messagebox.showwarning("Not Connected",
                    "Connect to Telegram Web first!\nClick 'Connect Telegram (Open QR)' and scan the QR code.")
                return
        elif mode == "bot":
            token = self.tg_bot_token.get().strip()
            if not token: messagebox.showwarning("","Enter your Telegram Bot Token."); return
        else:
            if not self.tg_user_connected or not self.tg_client:
                messagebox.showwarning("Not Connected",
                    "Connect your Telegram account first!\nLogin with Phone or QR Code.")
                return

        recs = []
        for line in raw.splitlines():
            line = line.strip()
            if not line: continue
            parts = line.split(",",1)
            cid = parts[0].strip()
            name = parts[1].strip() if len(parts)>1 else ""
            if cid: recs.append({"chat_id":cid,"name":name})
        if not recs: messagebox.showwarning("","No valid recipients."); return

        self._pre_send()
        parse_mode = self.tg_parse_mode.get()
        if parse_mode == "None": parse_mode = None
        disable_preview = self.tg_disable_preview_var.get()
        silent = self.tg_silent_var.get()
        protect = self.tg_protect_content_var.get() if hasattr(self,'tg_protect_content_var') else False

        try: delay_min = max(0, float(self.tg_delay_min.get() or 1))
        except: delay_min = 1
        try: delay_max = max(delay_min, float(self.tg_delay_max.get() or 3))
        except: delay_max = 3

        if mode == "web":
            try: web_delay = max(1, float(self.tg_web_delay.get() or 5))
            except: web_delay = 5
            self._send_telegram_web(recs, msg_text, web_delay)
        elif mode == "user":
            self._send_telegram_user(recs, msg_text, media_type, media_url, parse_mode,
                                      disable_preview, silent, delay_min, delay_max)
        else:
            token = self.tg_bot_token.get().strip()
            self._send_telegram_bot(recs, msg_text, media_type, media_url, token, parse_mode,
                                     disable_preview, silent, protect, delay_min, delay_max)

    def _send_telegram_web(self, recs, msg_text, delay):
        def worker():
            total = len(recs); done = [0]
            self.after(0, lambda: self.log(f"Telegram Web: {total} recipients", "tg"))

            for rec in recs:
                if not self.sending: break
                target = rec["chat_id"]; name = rec.get("name","")
                v = {"chat_id":target,"name":name,"date":datetime.now().strftime("%Y-%m-%d"),
                     "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
                actual_msg = rv(msg_text, v) if msg_text else ""
                ts = datetime.now().strftime("%H:%M:%S")

                try:
                    self._tg_web_send_message(target, actual_msg)
                    self.sent_count += 1
                    self.log_data.append({"time":ts,"target":target,"channel":"telegram-web","status":"sent","error":""})
                    self.after(0, lambda t=target,n=name: self.log(f"-> {t}" + (f" ({n})" if n else "") + " - Sent", "tg"))
                except Exception as ex:
                    err_msg = str(ex)[:80]
                    self.failed_count += 1
                    self.log_data.append({"time":ts,"target":target,"channel":"telegram-web","status":"failed","error":err_msg})
                    self.after(0, lambda t=target,er=err_msg: self.log(f"X {t} ({er})","failed"))

                done[0] += 1; self._progress(done[0], total)
                if done[0] < total: time.sleep(delay)

            self._post_send()
        threading.Thread(target=worker, daemon=True).start()

    def _send_telegram_bot(self, recs, msg_text, media_type, media_url, token,
                            parse_mode, disable_preview, silent, protect, delay_min, delay_max):
        def worker():
            total = len(recs); done = [0]
            self.after(0, lambda: self.log(f"Telegram Bot: {total} recipients", "tg"))
            base_url = f"https://api.telegram.org/bot{token}"

            for rec in recs:
                if not self.sending: break
                chat_id = rec["chat_id"]; name = rec.get("name","")
                v = {"chat_id":chat_id,"name":name,"date":datetime.now().strftime("%Y-%m-%d"),
                     "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
                actual_msg = rv(msg_text, v) if msg_text else ""
                ts = datetime.now().strftime("%H:%M:%S")

                try:
                    if media_type != "none" and media_url:
                        actual_media = rv(media_url, v)
                        method_map = {"photo":"sendPhoto","document":"sendDocument",
                                      "video":"sendVideo","audio":"sendAudio"}
                        method = method_map.get(media_type,"sendPhoto")
                        media_key = media_type if media_type != "document" else "document"
                        payload = {"chat_id":chat_id, media_key:actual_media}
                        if actual_msg: payload["caption"] = actual_msg
                        if parse_mode: payload["parse_mode"] = parse_mode
                        if silent: payload["disable_notification"] = True
                        if protect: payload["protect_content"] = True
                    else:
                        method = "sendMessage"
                        payload = {"chat_id":chat_id, "text":actual_msg}
                        if parse_mode: payload["parse_mode"] = parse_mode
                        if disable_preview: payload["disable_web_page_preview"] = True
                        if silent: payload["disable_notification"] = True
                        if protect: payload["protect_content"] = True

                    data = json.dumps(payload).encode("utf-8")
                    req = Request(f"{base_url}/{method}", data=data,
                                  headers={"Content-Type":"application/json"}, method="POST")
                    resp = urlopen(req, timeout=30)
                    result = json.loads(resp.read().decode())

                    if result.get("ok"):
                        self.sent_count += 1
                        self.log_data.append({"time":ts,"target":chat_id,"channel":"telegram-bot","status":"sent","error":""})
                        self.after(0, lambda c=chat_id,n=name: self.log(f"-> {c}" + (f" ({n})" if n else "") + " - Sent", "tg"))
                    else:
                        desc = result.get("description","Unknown error")
                        if result.get("error_code") == 429 and hasattr(self,'tg_flood_wait_var') and self.tg_flood_wait_var.get():
                            retry_after = result.get("parameters",{}).get("retry_after",5)
                            self.after(0, lambda w=retry_after: self.log(f"Rate limited, waiting {w}s...", "info"))
                            time.sleep(retry_after)
                            resp2 = urlopen(Request(f"{base_url}/{method}", data=data,
                                           headers={"Content-Type":"application/json"}, method="POST"), timeout=30)
                            result2 = json.loads(resp2.read().decode())
                            if result2.get("ok"):
                                self.sent_count += 1
                                self.log_data.append({"time":ts,"target":chat_id,"channel":"telegram-bot","status":"sent","error":""})
                                self.after(0, lambda c=chat_id: self.log(f"-> {c} - Sent (retry)", "tg"))
                            else:
                                raise Exception(result2.get("description","Retry failed"))
                        else:
                            raise Exception(desc)

                except Exception as ex:
                    self.failed_count += 1
                    err_msg = str(ex)[:80]
                    self.log_data.append({"time":ts,"target":chat_id,"channel":"telegram-bot","status":"failed","error":err_msg})
                    self.after(0, lambda c=chat_id,er=err_msg: self.log(f"X {c} ({er})","failed"))

                done[0] += 1; self._progress(done[0], total)
                if done[0] < total: time.sleep(random.uniform(delay_min, delay_max))

            self._post_send()
        threading.Thread(target=worker, daemon=True).start()

    def _send_telegram_user(self, recs, msg_text, media_type, media_url, parse_mode,
                             disable_preview, silent, delay_min, delay_max):
        client = self.tg_client
        def worker():
            total = len(recs); done = [0]
            self.after(0, lambda: self.log(f"Telegram User Account: {total} recipients", "tg"))

            for rec in recs:
                if not self.sending: break
                target = rec["chat_id"]; name = rec.get("name","")
                v = {"chat_id":target,"name":name,"date":datetime.now().strftime("%Y-%m-%d"),
                     "time":datetime.now().strftime("%H:%M:%S"),"random":str(random.randint(10000,99999))}
                actual_msg = rv(msg_text, v) if msg_text else ""
                ts = datetime.now().strftime("%H:%M:%S")

                try:
                    entity = target
                    if target.lstrip("-").isdigit():
                        entity = int(target)

                    if media_type != "none" and media_url:
                        actual_media = rv(media_url, v)
                        file_to_send = actual_media
                        if os.path.isfile(actual_media):
                            file_to_send = actual_media
                        client.send_file(entity, file_to_send, caption=actual_msg or None,
                                          silent=silent, parse_mode="html" if parse_mode == "HTML" else
                                          "md" if parse_mode == "Markdown" else None)
                    else:
                        client.send_message(entity, actual_msg, link_preview=not disable_preview,
                                             silent=silent, parse_mode="html" if parse_mode == "HTML" else
                                             "md" if parse_mode == "Markdown" else None)

                    self.sent_count += 1
                    self.log_data.append({"time":ts,"target":target,"channel":"telegram-user","status":"sent","error":""})
                    self.after(0, lambda t=target,n=name: self.log(f"-> {t}" + (f" ({n})" if n else "") + " - Sent", "tg"))

                except Exception as ex:
                    err_msg = str(ex)[:80]
                    if "FloodWaitError" in type(ex).__name__:
                        wait = getattr(ex, 'seconds', 30)
                        self.after(0, lambda w=wait: self.log(f"Flood wait: sleeping {w}s...", "warn"))
                        time.sleep(wait)
                        try:
                            if media_type != "none" and media_url:
                                client.send_file(entity, rv(media_url, v), caption=actual_msg or None, silent=silent)
                            else:
                                client.send_message(entity, actual_msg, link_preview=not disable_preview, silent=silent)
                            self.sent_count += 1
                            self.log_data.append({"time":ts,"target":target,"channel":"telegram-user","status":"sent","error":""})
                            self.after(0, lambda t=target: self.log(f"-> {t} - Sent (retry)", "tg"))
                        except Exception as ex2:
                            self.failed_count += 1
                            self.log_data.append({"time":ts,"target":target,"channel":"telegram-user","status":"failed","error":str(ex2)[:80]})
                            self.after(0, lambda t=target,er=str(ex2)[:60]: self.log(f"X {t} ({er})","failed"))
                    else:
                        self.failed_count += 1
                        self.log_data.append({"time":ts,"target":target,"channel":"telegram-user","status":"failed","error":err_msg})
                        self.after(0, lambda t=target,er=err_msg: self.log(f"X {t} ({er})","failed"))

                done[0] += 1; self._progress(done[0], total)
                if done[0] < total: time.sleep(random.uniform(delay_min, delay_max))

            self._post_send()
        threading.Thread(target=worker, daemon=True).start()

    def log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}]  {msg}\n", tag)
        self.log_box.see("end"); self.log_box.configure(state="disabled")

    # ══════════════════════════════════════════════════════════
    #  ABOUT
    # ══════════════════════════════════════════════════════════
    # ═══════════════════════════════════════════════════════════
    #  AUTO-UPDATER
    # ═══════════════════════════════════════════════════════════
    def _check_for_updates(self):
        win = ctk.CTkToplevel(self); win.title("Update Manager"); win.geometry("520x420"); win.transient(self)
        win.configure(fg_color=T["bg"]); win.resizable(False, False)

        hdr = ctk.CTkFrame(win, fg_color=T["surface"], corner_radius=0); hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  OmniSend Pro  -  Update Manager", font=("Segoe UI Semibold",15), text_color=T["t1"]).pack(side="left", padx=12, pady=14)

        body = ctk.CTkFrame(win, fg_color="transparent"); body.pack(fill="both", expand=True, padx=20, pady=12)

        info_card = ctk.CTkFrame(body, fg_color=T["card"], corner_radius=8)
        info_card.pack(fill="x", pady=(0,10))
        ir = ctk.CTkFrame(info_card, fg_color="transparent"); ir.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(ir, text=f"Installed Version:", font=("Segoe UI",12), text_color=T["t2"]).pack(side="left")
        ctk.CTkLabel(ir, text=f"  v{APP_VERSION}", font=("Segoe UI Bold",13), text_color=T["green"]).pack(side="left")

        status_card = ctk.CTkFrame(body, fg_color=T["card"], corner_radius=8)
        status_card.pack(fill="x", pady=(0,10))
        status_lbl = ctk.CTkLabel(status_card, text="  Checking for updates...", font=("Segoe UI",12), text_color=T["orange"])
        status_lbl.pack(anchor="w", padx=16, pady=(12,4))
        detail_lbl = ctk.CTkLabel(status_card, text="", font=("Segoe UI",11), text_color=T["t3"], wraplength=440, justify="left")
        detail_lbl.pack(anchor="w", padx=16, pady=(0,12))

        progress = ctk.CTkProgressBar(body, height=6, fg_color=T["border"], progress_color=T["accent"])
        progress.pack(fill="x", pady=(0,10)); progress.set(0)

        log_card = ctk.CTkFrame(body, fg_color=T["card"], corner_radius=8)
        log_card.pack(fill="both", expand=True, pady=(0,10))
        log_tb = ctk.CTkTextbox(log_card, font=("Consolas",10), fg_color=T["input_bg"], text_color=T["t2"],
                                 corner_radius=6, height=80)
        log_tb.pack(fill="both", expand=True, padx=8, pady=8)
        log_tb.configure(state="disabled")

        btn_frame = ctk.CTkFrame(body, fg_color="transparent"); btn_frame.pack(fill="x")
        update_btn = ctk.CTkButton(btn_frame, text="Update Now", height=38, font=("Segoe UI",13,"bold"),
                                    fg_color=T["green"], hover_color=T["green_h"], corner_radius=8, state="disabled")
        update_btn.pack(side="left", fill="x", expand=True, padx=(0,4))
        ctk.CTkButton(btn_frame, text="Set Update URL", height=38, font=("Segoe UI",11),
                       fg_color=T["card_h"], hover_color=T["border"], corner_radius=8,
                       command=lambda: self._set_update_url(win)).pack(side="right", padx=(4,0))

        def _log(msg):
            log_tb.configure(state="normal"); log_tb.insert("end", msg + "\n"); log_tb.see("end"); log_tb.configure(state="disabled")

        update_info = {}

        def _check():
            url = self._get_update_url()
            self.after(0, lambda: _log(f"Checking: {url}"))
            self.after(0, lambda: progress.set(0.2))
            try:
                req = Request(url, method="GET", headers={"User-Agent":"OmniSendPro-Updater"})
                resp = urlopen(req, timeout=15)
                data = json.loads(resp.read().decode())
                self.after(0, lambda: progress.set(0.5))

                remote_ver = data.get("version","")
                changelog = data.get("changelog","No changelog provided.")
                download_url = data.get("download_url","")
                min_python = data.get("min_python","3.8")

                self.after(0, lambda: _log(f"Remote version: v{remote_ver}"))
                self.after(0, lambda: _log(f"Download URL: {download_url[:60]}..."))
                self.after(0, lambda: _log(f"Runtime mode: {'EXE' if self._is_frozen_app() else 'Python script'}"))

                update_info["version"] = remote_ver
                update_info["changelog"] = changelog
                update_info["download_url"] = download_url
                update_info["min_python"] = min_python

                if self._compare_versions(remote_ver, APP_VERSION) > 0:
                    self.after(0, lambda: status_lbl.configure(
                        text=f"  New version available: v{remote_ver}", text_color=T["green"]))
                    self.after(0, lambda: detail_lbl.configure(
                        text=f"Changelog:\n{changelog}"))
                    self.after(0, lambda: update_btn.configure(state="normal",
                        command=lambda: self._do_update(update_info, progress, status_lbl, _log, win)))
                    self.after(0, lambda: _log(f"Update available! v{APP_VERSION} -> v{remote_ver}"))
                    if self._is_frozen_app() and download_url.lower().endswith(".py"):
                        self.after(0, lambda: _log("Warning: server provides .py update, but app is running as EXE."))
                        self.after(0, lambda: detail_lbl.configure(
                            text=f"Changelog:\n{changelog}\n\nNote: You are running the EXE build. This update URL returns a Python file. Use Manual Update with a new .exe, or set an EXE download URL."))
                else:
                    self.after(0, lambda: status_lbl.configure(
                        text=f"  You're up to date! (v{APP_VERSION})", text_color=T["green"]))
                    self.after(0, lambda: detail_lbl.configure(
                        text="No updates available. You have the latest version."))
                    self.after(0, lambda: _log("Already up to date."))

                self.after(0, lambda: progress.set(1.0))

            except Exception as ex:
                self.after(0, lambda: status_lbl.configure(
                    text="  Could not check for updates", text_color=T["red"]))
                self.after(0, lambda: detail_lbl.configure(
                    text=f"Error: {str(ex)}\n\nMake sure the update URL is correct and accessible.\nYou can set a custom URL with 'Set Update URL'."))
                self.after(0, lambda: _log(f"Error: {str(ex)}"))
                self.after(0, lambda: progress.set(0))
                self.after(0, lambda: update_btn.configure(state="normal", text="Manual Update",
                    command=lambda: self._manual_update(progress, status_lbl, _log, win)))

        threading.Thread(target=_check, daemon=True).start()

    def _compare_versions(self, v1, v2):
        def _parse(v):
            return [int(x) for x in re.sub(r'[^0-9.]','', v).split('.') if x]
        p1, p2 = _parse(v1), _parse(v2)
        for a, b in zip(p1, p2):
            if a > b: return 1
            if a < b: return -1
        return len(p1) - len(p2)

    def _get_update_url(self):
        cfg_path = os.path.join(DATA_DIR, "update_config.json")
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r") as f:
                    return json.load(f).get("url", UPDATE_URL)
            except: pass
        return UPDATE_URL

    def _set_update_url(self, parent):
        win = ctk.CTkToplevel(parent); win.title("Set Update URL"); win.geometry("500x200"); win.transient(parent)
        win.configure(fg_color=T["bg"])
        ctk.CTkLabel(win, text="Custom Update URL", font=("Segoe UI Semibold",14), text_color=T["t1"]).pack(padx=20, pady=(16,4))
        ctk.CTkLabel(win, text="Point to a JSON file with: version, changelog, download_url",
                      font=("Segoe UI",10), text_color=T["t3"]).pack(anchor="w", padx=20)
        url_entry = ctk.CTkEntry(win, height=36, font=("Segoe UI",12), fg_color=T["input_bg"],
                                  border_color=T["input_bd"], corner_radius=6, text_color=T["t1"])
        url_entry.pack(fill="x", padx=20, pady=8)
        url_entry.insert(0, self._get_update_url())

        def _save():
            cfg_path = os.path.join(DATA_DIR, "update_config.json")
            with open(cfg_path, "w") as f: json.dump({"url": url_entry.get().strip()}, f)
            messagebox.showinfo("Saved", "Update URL saved!"); win.destroy()

        bf = ctk.CTkFrame(win, fg_color="transparent"); bf.pack(fill="x", padx=20, pady=(0,12))
        ctk.CTkButton(bf, text="Save", height=34, fg_color=T["green"], hover_color=T["green_h"],
                       command=_save).pack(side="left", fill="x", expand=True, padx=(0,4))
        ctk.CTkButton(bf, text="Reset Default", height=34, fg_color=T["card_h"], hover_color=T["border"],
                       command=lambda: [url_entry.delete(0,"end"), url_entry.insert(0, UPDATE_URL)]).pack(side="right")

    def _is_frozen_app(self):
        return bool(getattr(sys, "frozen", False))

    def _update_target_path(self):
        # In PyInstaller/EXE mode, the update target should be the executable.
        return os.path.abspath(sys.executable if self._is_frozen_app() else __file__)

    def _update_backup_path(self, target_path):
        root, ext = os.path.splitext(target_path)
        return f"{root}.backup{ext or '.bak'}"

    def _do_update(self, info, progress, status_lbl, log_fn, win):
        download_url = info.get("download_url","")
        if not download_url:
            messagebox.showwarning("","No download URL in update info."); return

        status_lbl.configure(text="  Downloading update...", text_color=T["orange"])
        progress.set(0.3)

        def _download():
            try:
                log_fn(f"Downloading from: {download_url[:70]}...")
                log_fn(f"Runtime mode: {'EXE' if self._is_frozen_app() else 'Python script'}")
                req = Request(download_url, method="GET", headers={"User-Agent":"OmniSendPro-Updater"})
                resp = urlopen(req, timeout=60)
                new_code = resp.read()
                self.after(0, lambda: progress.set(0.6))
                self.after(0, lambda: log_fn(f"Downloaded {len(new_code)} bytes"))

                app_path = self._update_target_path()
                backup_path = self._update_backup_path(app_path)

                self.after(0, lambda: log_fn(f"Creating backup: {os.path.basename(backup_path)}"))
                shutil.copy2(app_path, backup_path)
                self.after(0, lambda: progress.set(0.75))

                self.after(0, lambda: log_fn("Writing new version..."))
                with open(app_path, "wb") as f:
                    f.write(new_code)
                self.after(0, lambda: progress.set(0.9))

                self.after(0, lambda: log_fn("Update installed successfully!"))
                self.after(0, lambda: status_lbl.configure(
                    text=f"  Updated to v{info.get('version','?')}! Restart to apply.", text_color=T["green"]))
                self.after(0, lambda: progress.set(1.0))

                def _ask_restart():
                    if messagebox.askyesno("Update Complete",
                            f"Updated to v{info.get('version','?')}!\n\nRestart the application now?"):
                        self._restart_app()
                self.after(100, _ask_restart)

            except Exception as ex:
                self.after(0, lambda: status_lbl.configure(
                    text="  Update failed!", text_color=T["red"]))
                self.after(0, lambda: log_fn(f"Error: {str(ex)}"))
                self.after(0, lambda: progress.set(0))

                app_path = self._update_target_path()
                backup_path = self._update_backup_path(app_path)
                if os.path.exists(backup_path):
                    self.after(0, lambda: log_fn("Restoring from backup..."))
                    try:
                        shutil.copy2(backup_path, app_path)
                        self.after(0, lambda: log_fn("Backup restored."))
                    except: pass

        threading.Thread(target=_download, daemon=True).start()

    def _manual_update(self, progress, status_lbl, log_fn, win):
        path = filedialog.askopenfilename(
            title="Select update file",
            filetypes=[("Executable","*.exe"),("Python","*.py"),("All","*.*")] if self._is_frozen_app() else [("Python","*.py"),("All","*.*")])
        if not path: return

        try:
            new_ver = "unknown"
            if path.lower().endswith(".py"):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "OmniSend Pro" not in content[:200]:
                    if not messagebox.askyesno("Warning",
                            "This file doesn't look like OmniSend Pro.\nContinue anyway?"):
                        return
                ver_match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)', content)
                new_ver = ver_match.group(1) if ver_match else "unknown"

            log_fn(f"Selected file: {os.path.basename(path)}")
            log_fn(f"Detected version: v{new_ver}")
            progress.set(0.4)

            app_path = self._update_target_path()
            backup_path = self._update_backup_path(app_path)
            shutil.copy2(app_path, backup_path)
            log_fn("Backup created.")
            progress.set(0.6)

            shutil.copy2(path, app_path)
            log_fn("File replaced.")
            progress.set(1.0)

            status_lbl.configure(text=f"  Updated to v{new_ver}! Restart to apply.", text_color=T["green"])

            if messagebox.askyesno("Update Complete",
                    f"Manually updated to v{new_ver}!\n\nRestart the application now?"):
                self._restart_app()

        except Exception as ex:
            log_fn(f"Error: {str(ex)}")
            status_lbl.configure(text="  Manual update failed!", text_color=T["red"])

    def _restart_app(self):
        python = sys.executable
        script = os.path.abspath(__file__)
        self.destroy()
        if self._is_frozen_app():
            subprocess.Popen([python])
        else:
            subprocess.Popen([python, script])
        sys.exit(0)

    def _rollback_update(self):
        app_path = self._update_target_path()
        backup_path = self._update_backup_path(app_path)
        if not os.path.exists(backup_path):
            messagebox.showinfo("","No backup found. Nothing to rollback."); return
        if not messagebox.askyesno("Rollback",
                "Restore the previous version from backup?\nThe app will restart."):
            return
        try:
            shutil.copy2(backup_path, app_path)
            messagebox.showinfo("Rolled Back", "Previous version restored. Restarting...")
            self._restart_app()
        except Exception as ex:
            messagebox.showerror("Error", f"Rollback failed: {str(ex)}")

    def _show_about(self):
        win = ctk.CTkToplevel(self)
        win.title("About OmniSend Pro")
        win.geometry("460x560")
        win.transient(self)
        win.resizable(False, False)
        win.configure(fg_color=T["bg"])

        top = ctk.CTkFrame(win, fg_color=T["surface"], corner_radius=0, height=130)
        top.pack(fill="x"); top.pack_propagate(False)
        inner = ctk.CTkFrame(top, fg_color="transparent"); inner.pack(expand=True)
        logo = ctk.CTkFrame(inner, width=50, height=50, corner_radius=12, fg_color=T["accent"])
        logo.pack(pady=(0,8)); logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="O", font=("Segoe UI Black",24), text_color="#fff").pack(expand=True)
        ctk.CTkLabel(inner, text="OmniSend Pro", font=("Segoe UI Bold",20), text_color=T["t1"]).pack()
        ctk.CTkLabel(inner, text=f"v{APP_VERSION}  -  Multi-Channel Messaging", font=("Segoe UI",11), text_color=T["t3"]).pack()

        content = ctk.CTkFrame(win, fg_color="transparent"); content.pack(fill="both", expand=True, padx=20, pady=12)

        desc = ctk.CTkFrame(content, fg_color=T["card"], corner_radius=8)
        desc.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(desc, text="Professional bulk messaging tool for\nEmail, WhatsApp, SMS, and Telegram.",
                      font=("Segoe UI",12), text_color=T["t2"], justify="center").pack(padx=16, pady=12)

        feat = ctk.CTkFrame(content, fg_color=T["card"], corner_radius=8)
        feat.pack(fill="x", pady=(0,8))
        for title, info in [("Email","SMTP rotation, templates, spintax"),
                             ("WhatsApp","Web QR + Business API"),
                             ("SMS","Twilio + custom gateway"),
                             ("Telegram","Bot API + User Account (Telethon)"),
                             ("60+ SMTP","Pre-configured presets"),
                             ("80+ Tools","Lists, verification, content, export")]:
            row = ctk.CTkFrame(feat, fg_color="transparent"); row.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row, text=title, font=("Segoe UI Semibold",11), text_color=T["t1"], width=80, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=info, font=("Segoe UI",10), text_color=T["t3"]).pack(side="left", padx=(4,0))
        ctk.CTkFrame(feat, height=4, fg_color="transparent").pack()

        # ── Update button ──
        upd_fr = ctk.CTkFrame(content, fg_color=T["card"], corner_radius=8)
        upd_fr.pack(fill="x", pady=(0,8))
        upd_row = ctk.CTkFrame(upd_fr, fg_color="transparent"); upd_row.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(upd_row, text=f"Current version: v{APP_VERSION}", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        ctk.CTkButton(upd_row, text="Check for Updates", height=30, width=140, font=("Segoe UI",11),
                       fg_color=T["accent"], hover_color=T["accent_h"], corner_radius=6,
                       command=self._check_for_updates).pack(side="right")

        contact = ctk.CTkFrame(content, fg_color=T["accent_s"], corner_radius=8)
        contact.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(contact, text="Contact & Support", font=("Segoe UI Semibold",12), text_color=T["accent_l"]).pack(anchor="w", padx=14, pady=(10,4))
        tg = ctk.CTkFrame(contact, fg_color="transparent"); tg.pack(fill="x", padx=14, pady=(0,10))
        ctk.CTkLabel(tg, text="Telegram:", font=("Segoe UI",11), text_color=T["t2"]).pack(side="left")
        tg_link = ctk.CTkLabel(tg, text=" @werlist99", font=("Segoe UI Bold",12), text_color=T["cyan"], cursor="hand2")
        tg_link.pack(side="left")
        tg_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/werlist99"))

        ctk.CTkLabel(content, text="Python + CustomTkinter", font=("Segoe UI",9), text_color=T["t4"]).pack(pady=(2,0))


if __name__ == "__main__":
    App().mainloop()
