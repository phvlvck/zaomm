 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   Zain Iraq Bot v6.0 — بالإيموجيات المميزة (مُصحّح)      ║
║   حقوق التطوير: @to_ls                                   ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import re
import json
import base64
import time
import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from telegram.constants import ParseMode


# ═══════════════════════════════════════════════════════════
#                    الإعدادات
# ═══════════════════════════════════════════════════════════
BOT_TOKEN = os.getenv("BOT_TOKEN", "8649116276:AAGRor3c0juxDASZ2tJPutf31nGbXQ2NsSg")

DEVELOPER = "@to_ls"
DEV_LINK = "https://t.me/to_ls"
CHANNEL_LINK = "https://t.me/to_ls"

BASE_URL = "https://mw-mobileapp.iq.zain.com/api"

COMMON_HEADERS = {
    'User-Agent': "okhttp/4.11.0",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Skel-Accept-Language': "ar",
    'Skel-Platform': "Android",
    'Skel-OS-Version': "15",
    'Skel-Fix-Version': "6.5.0",
    'Skel-Installation-Id': "a7f6551e0ac34017fcf8c1cf7ac56bada3eb793b",
    'Content-Type': "application/json; charset=UTF-8"
}

USER_STATE = {}
CACHE = {}


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
#     🎨 الإيموجيات المميزة (تُطبق على النص فقط)
# ═══════════════════════════════════════════════════════════
_CE = {
    # ─── الرموز الملكية ───
    '👑': '<tg-emoji emoji-id="5319149831673887746">👑</tg-emoji>',
    '⭐': '<tg-emoji emoji-id="5254001839287859496">⭐</tg-emoji>',
    '💎': '<tg-emoji emoji-id="5254001839287859496">💎</tg-emoji>',
    '✨': '<tg-emoji emoji-id="5254001839287859496">✨</tg-emoji>',
    '🎉': '<tg-emoji emoji-id="5254001839287859496">🎉</tg-emoji>',
    '🎨': '<tg-emoji emoji-id="5254001839287859496">🎨</tg-emoji>',
    '🤖': '<tg-emoji emoji-id="5254001839287859496">🤖</tg-emoji>',
    '😎': '<tg-emoji emoji-id="5976308930660276596">😎</tg-emoji>',
    '👋': '<tg-emoji emoji-id="5319149831673887746">👋</tg-emoji>',
    '🧙': '<tg-emoji emoji-id="5803157577525106419">🧙</tg-emoji>',

    # ─── المال ───
    '💰': '<tg-emoji emoji-id="6037182124916740433">💰</tg-emoji>',
    '💵': '<tg-emoji emoji-id="6003691769533829755">💵</tg-emoji>',
    '💳': '<tg-emoji emoji-id="5447453226498552490">💳</tg-emoji>',
    '💲': '<tg-emoji emoji-id="6003691769533829755">💲</tg-emoji>',
    '💗': '<tg-emoji emoji-id="6043941205144771802">💗</tg-emoji>',

    # ─── المستخدم ───
    '👤': '<tg-emoji emoji-id="5373020661574826232">👤</tg-emoji>',
    '👥': '<tg-emoji emoji-id="6001388309853510348">👥</tg-emoji>',
    '👁': '<tg-emoji emoji-id="5373020661574826232">👁</tg-emoji>',
    '📱': '<tg-emoji emoji-id="5834628314731387616">📱</tg-emoji>',
    '📞': '<tg-emoji emoji-id="5373020661574826232">📞</tg-emoji>',

    # ─── الأمان ───
    '🔑': '<tg-emoji emoji-id="5785167918027250397">🔑</tg-emoji>',
    '🔒': '<tg-emoji emoji-id="5785167918027250397">🔒</tg-emoji>',
    '🔓': '<tg-emoji emoji-id="5998940732545571769">🔓</tg-emoji>',
    '🛡️': '<tg-emoji emoji-id="5920298756074379058">🛡️</tg-emoji>',
    '🚫': '<tg-emoji emoji-id="5888789252493283486">🚫</tg-emoji>',

    # ─── الحالات ───
    '✅': '<tg-emoji emoji-id="6258259403200270844">✅</tg-emoji>',
    '☑️': '<tg-emoji emoji-id="4945049066271671758">☑️</tg-emoji>',
    '❌': '<tg-emoji emoji-id="5796291784539639311">❌</tg-emoji>',
    '⚠️': '<tg-emoji emoji-id="5999278377104578246">⚠️</tg-emoji>',
    '🔄': '<tg-emoji emoji-id="5976831692604709621">🔄</tg-emoji>',
    '🔙': '<tg-emoji emoji-id="5253743295141538873">🔙</tg-emoji>',
    '🆕': '<tg-emoji emoji-id="5857339990123486296">🆕</tg-emoji>',

    # ─── الألوان ───
    '🔴': '<tg-emoji emoji-id="5999278377104578246">🔴</tg-emoji>',
    '🟢': '<tg-emoji emoji-id="4945049066271671758">🟢</tg-emoji>',
    '🔵': '<tg-emoji emoji-id="5967301267549068409">🔵</tg-emoji>',
    '🔹': '<tg-emoji emoji-id="5967301267549068409">🔹</tg-emoji>',
    '🔢': '<tg-emoji emoji-id="5965466792527666087">🔢</tg-emoji>',

    # ─── الإشعارات ───
    '📢': '<tg-emoji emoji-id="5902385465390013835">📢</tg-emoji>',
    '📣': '<tg-emoji emoji-id="5902385465390013835">📣</tg-emoji>',
    '📡': '<tg-emoji emoji-id="5836811137370297987">📡</tg-emoji>',
    '📨': '<tg-emoji emoji-id="5920415115328362511">📨</tg-emoji>',
    '📬': '<tg-emoji emoji-id="5857339990123486296">📬</tg-emoji>',
    '📤': '<tg-emoji emoji-id="5920298756074379058">📤</tg-emoji>',
    '📥': '<tg-emoji emoji-id="5920415115328362511">📥</tg-emoji>',
    '✉️': '<tg-emoji emoji-id="5314299563761222650">✉️</tg-emoji>',

    # ─── البيانات ───
    '📊': '<tg-emoji emoji-id="5935935761336505948">📊</tg-emoji>',
    '📈': '<tg-emoji emoji-id="5935935761336505948">📈</tg-emoji>',
    '📋': '<tg-emoji emoji-id="5803363345113290876">📋</tg-emoji>',
    '📦': '<tg-emoji emoji-id="5881760620117760960">📦</tg-emoji>',
    '📂': '<tg-emoji emoji-id="5881760620117760960">📂</tg-emoji>',
    '🧾': '<tg-emoji emoji-id="5881760620117760960">🧾</tg-emoji>',
    '🗂️': '<tg-emoji emoji-id="5881760620117760960">🗂️</tg-emoji>',
    '🗑️': '<tg-emoji emoji-id="5920209833071482745">🗑️</tg-emoji>',
    '📌': '<tg-emoji emoji-id="5920298756074379058">📌</tg-emoji>',

    # ─── المكافآت ───
    '🎁': '<tg-emoji emoji-id="5976317950091598658">🎁</tg-emoji>',
    '🎟️': '<tg-emoji emoji-id="5785167918027250397">🎟️</tg-emoji>',
    '🎫': '<tg-emoji emoji-id="5785167918027250397">🎫</tg-emoji>',
    '🎯': '<tg-emoji emoji-id="5965466792527666087">🎯</tg-emoji>',

    # ─── الأدوات ───
    '⚙️': '<tg-emoji emoji-id="5857054220179480029">⚙️</tg-emoji>',
    '🛠️': '<tg-emoji emoji-id="5965466792527666087">🛠️</tg-emoji>',
    '➕': '<tg-emoji emoji-id="5857339990123486296">➕</tg-emoji>',
    '➖': '<tg-emoji emoji-id="5280753674451175517">➖</tg-emoji>',
    '🔍': '<tg-emoji emoji-id="5965466792527666087">🔍</tg-emoji>',
    '🔎': '<tg-emoji emoji-id="5965466792527666087">🔎</tg-emoji>',
    'ℹ️': '<tg-emoji emoji-id="5965466792527666087">ℹ️</tg-emoji>',
    '🧹': '<tg-emoji emoji-id="5920415115328362511">🧹</tg-emoji>',

    # ─── الحركة ───
    '🚀': '<tg-emoji emoji-id="5967301267549068409">🚀</tg-emoji>',
    '🔗': '<tg-emoji emoji-id="5967301267549068409">🔗</tg-emoji>',
    '⬆️': '<tg-emoji emoji-id="5920298756074379058">⬆️</tg-emoji>',
    '⬇️': '<tg-emoji emoji-id="5922681088534124293">⬇️</tg-emoji>',

    # ─── الشبكة ───
    '🌐': '<tg-emoji emoji-id="5837128389424585193">🌐</tg-emoji>',
    '🌾': '<tg-emoji emoji-id="5981216003810400332">🌾</tg-emoji>',

    # ─── التواريخ ───
    '📅': '<tg-emoji emoji-id="5314299563761222650">📅</tg-emoji>',
    '📝': '<tg-emoji emoji-id="5314299563761222650">📝</tg-emoji>',
    '✏️': '<tg-emoji emoji-id="5314299563761222650">✏️</tg-emoji>',
    '⏳': '<tg-emoji emoji-id="5314299563761222650">⏳</tg-emoji>',
    '⏰': '<tg-emoji emoji-id="5314299563761222650">⏰</tg-emoji>',
    '💬': '<tg-emoji emoji-id="5314299563761222650">💬</tg-emoji>',

    # ─── عام ───
    '🏠': '<tg-emoji emoji-id="5881760620117760960">🏠</tg-emoji>',
    '🏦': '<tg-emoji emoji-id="5803363345113290876">🏦</tg-emoji>',
    '🏷️': '<tg-emoji emoji-id="5881760620117760960">🏷️</tg-emoji>',
    '🖨️': '<tg-emoji emoji-id="5967617875358258757">🖨️</tg-emoji>',
    '🖼️': '<tg-emoji emoji-id="5294079682365384341">🖼️</tg-emoji>',
}


def ce(text: str) -> str:
    """تطبيق الإيموجيات المميزة — للنصوص فقط"""
    if not text:
        return text
    for ch, rep in _CE.items():
        text = text.replace(ch, rep)
    return text


# ═══════════════════════════════════════════════════════════
#                    أدوات مساعدة
# ═══════════════════════════════════════════════════════════
def normalize_msisdn(msisdn):
    d = re.sub(r'\D', '', str(msisdn))
    if d.startswith("964"):
        d = d[3:]
    if d.startswith("0"):
        d = d[1:]
    return d


def validate_msisdn(msisdn):
    d = normalize_msisdn(msisdn)
    return len(d) == 10 and d.startswith(("77", "78"))


def decode_jwt(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        pad = lambda s: s + "=" * (-len(s) % 4)
        return {
            "header": json.loads(base64.urlsafe_b64decode(pad(parts[0]))),
            "payload": json.loads(base64.urlsafe_b64decode(pad(parts[1]))),
        }
    except Exception:
        return None


def identify_token_type(token):
    d = decode_jwt(token)
    if not d:
        return "invalid"
    if d["payload"].get("data", {}).get("grant_type") == "refresh":
        return "refresh"
    return "access"


def get_msisdn_from_token(token):
    d = decode_jwt(token)
    if not d:
        return None
    return d["payload"].get("data", {}).get("msisdn")


def get_expiry_from_token(token):
    d = decode_jwt(token)
    if not d:
        return None
    return d["payload"].get("expires") or d["payload"].get("exp")


def fmt_ts(ts):
    if not ts:
        return "—"
    try:
        if isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts.replace("Z", "")).strftime("%Y-%m-%d %H:%M")
            except Exception:
                ts = float(ts)
        if ts > 1e11:
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ts)[:19]


def days_from_now(ts_str):
    if not ts_str:
        return None
    try:
        d = datetime.fromisoformat(ts_str.replace("Z", ""))
        return (d - datetime.now()).days
    except Exception:
        return None


def api_get(path, token, **params):
    headers = {**COMMON_HEADERS, "Authorization": f"Bearer {token}"}
    try:
        r = requests.get(f"{BASE_URL}{path}", headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"status": "error", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def esc(t):
    if t is None:
        return "—"
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def login_zain(msisdn, password):
    try:
        r = requests.post(
            f"{BASE_URL}/user/login",
            data=json.dumps({"msisdn": msisdn, "password": password}),
            headers=COMMON_HEADERS,
            timeout=15
        )
        data = r.json()
        if data.get("status") != "success":
            err = data.get("error", {})
            return None, err.get("message", "فشل تسجيل الدخول")
        return data["data"]["access_token"], None
    except Exception as e:
        return None, str(e)


# ═══════════════════════════════════════════════════════════
#     🎨 أزرار (بدون tg-emoji — إيموجي عادي فقط)
# ═══════════════════════════════════════════════════════════
def make_button(text, callback_data=None, url=None, color=None):
    """زر بإيموجي عادي — متوافق مع كل النسخ"""
    button = {"text": text}   # ✅ بدون ce()
    if url:
        button["url"] = url
    else:
        button["callback_data"] = callback_data or "noop"
    if color in ("primary", "success", "danger"):
        button["style"] = color
    return button


def send_colored_keyboard(chat_id, text, keyboard_rows):
    """إرسال رسالة — النص فقط يُطبَّق عليه ce()"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": ce(text),   # ✅ ce على النص فقط
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard_rows},
        "disable_web_page_preview": True,
    }
    try:
        return requests.post(url, json=payload, timeout=15).json()
    except Exception as e:
        logger.error(f"send_colored_keyboard error: {e}")
        return None


def edit_colored_keyboard(chat_id, message_id, text, keyboard_rows):
    """تعديل رسالة — النص فقط يُطبَّق عليه ce()"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": ce(text),   # ✅ ce على النص فقط
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard_rows},
        "disable_web_page_preview": True,
    }
    try:
        return requests.post(url, json=payload, timeout=15).json()
    except Exception as e:
        logger.error(f"edit_colored_keyboard error: {e}")
        return None


# ═══════════════════════════════════════════════════════════
#                    جلب البيانات
# ═══════════════════════════════════════════════════════════
def fetch_all_data(token, msisdn):
    data = {}

    r = api_get("/v2/user/profile", token)
    data["profile"] = r.get("data", {}) if r.get("status") == "success" else {}

    r = api_get("/number/wallet", token, msisdn=msisdn)
    data["wallet"] = r.get("data", {}) if r.get("status") == "success" else {}

    r = api_get("/number/subaccounts", token, msisdn=msisdn)
    data["subaccounts"] = r.get("data", []) if r.get("status") == "success" else []

    r = api_get("/loyalty/info", token)
    data["loyalty"] = r.get("data", {}) if r.get("status") == "success" else {}

    r = api_get("/number/subscriptions", token, msisdn=msisdn)
    data["subscriptions"] = r.get("data", []) if r.get("status") == "success" else []

    r = api_get("/notifications", token, offset=0, limit=10)
    data["notifications"] = r.get("data", {}) if r.get("status") == "success" else {}

    return data


def get_user_data(user_id, token, msisdn, force=False):
    now = time.time()
    cached = CACHE.get(user_id)
    if not force and cached and (now - cached.get("ts", 0)) < 60:
        return cached["data"]
    data = fetch_all_data(token, msisdn)
    CACHE[user_id] = {"data": data, "ts": now}
    return data


# ═══════════════════════════════════════════════════════════
#                    تنسيق التقارير
# ═══════════════════════════════════════════════════════════
ACCOUNT_TYPE_NAMES = {
    1000: "💵 رصيد أساسي",
    1001: "🎁 رصيد مكافآت",
    2000: "💰 رصيد مالي",
    2001: "📶 رصيد بيانات",
    2784: "📞 دقائق",
    4425: "🎁 رصيد مجاني",
    4426: "💬 رسائل",
    4427: "🌐 إنترنت",
    6083: "🎯 رصيد إضافي",
}

STATUS_NAMES = {
    "Active":    "🟢 نشط",
    "Renewing":  "🔄 قيد التجديد",
    "Expiring":  "🟡 قارب على الانتهاء",
    "Expired":   "🔴 منتهي",
    "Suspended": "⚫ موقوف",
    "Pending":   "🔵 قيد التفعيل",
}


def fmt_summary(data, msisdn):
    p = data.get("profile", {})
    w = data.get("wallet", {})
    l = data.get("loyalty", {})
    subs = data.get("subscriptions", [])

    name = p.get("name", "—")
    balance = w.get("balance", {}).get("value", 0)
    points = l.get("total_points", 0)
    tier_ar = l.get("localized_tier", {}).get("ar", "—")

    return (
        f"📱 【 الرقم 】  <code>{esc(msisdn)}</code>\n"
        f"👤 【 الاسم 】  <b>{esc(name)}</b>\n"
        f"💰 【 الرصيد 】  <b>{balance} د.ع</b>\n"
        f"🏆 【 نقاط ممنون 】  <b>{points:,}</b>\n"
        f"⭐ 【 المستوى 】  <b>{esc(tier_ar)}</b>\n"
        f"📦 【 الاشتراكات 】  <b>{len(subs)}</b>\n"
    )


def fmt_profile(data):
    p = data.get("profile", {})
    if not p:
        return "🔴 تعذّر جلب الملف الشخصي"

    billing_ar = {
        "prepaid_normal": "دفع مسبق عادي",
        "postpaid": "دفع لاحق",
        "hybrid": "مختلط",
    }.get(p.get("customer_billing_type", ""), p.get("customer_billing_type", "—"))

    flex_ar = {
        "eligible": "✅ مؤهل",
        "migrated": "🔄 تم الترحيل",
        "not_eligible": "❌ غير مؤهل",
    }.get(p.get("flex_status", ""), p.get("flex_status", "—"))

    return (
        f"<b>👤  【 الملف الشخصي 】</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👋 【 الاسم 】 {esc(p.get('name'))}\n"
        f"📱 【 الرقم 】 <code>{esc(p.get('msisdn'))}</code>\n"
        f"📅 【 التسجيل 】 {esc(fmt_ts(p.get('created_at')))}\n"
        f"💳 【 نوع الحساب 】 {esc(billing_ar)}\n"
        f"📶 【 الشريحة 】 {esc(p.get('unified_sim_status'))}\n"
        f"🌐 【 4G 】 {'✅ نعم' if p.get('is_4g_compatible') else '❌ لا'}\n"
        f"🎁 【 كفو 】 {'✅ مستلم' if p.get('is_gift_redeemed') else '❌ لم يُستلم'}\n"
        f"⚡ 【 Flex 】 {esc(flex_ar)}\n"
        f"🎫 【 الباقة 】 <code>#{esc(p.get('primary_offering_id', '—'))}</code>\n"
    )


def fmt_balance(data):
    w = data.get("wallet", {})
    bal = w.get("balance", {})
    amount = bal.get("value", 0)
    expiry = bal.get("expiry", "")

    txt = (
        f"<b>💰  【 الرصيد المالي 】</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💵 【 الرصيد 】 <b>{amount} دينار</b>\n"
    )

    if expiry:
        txt += f"📅 【 صالح لغاية 】 {esc(expiry[:10])}\n"
        days = days_from_now(expiry)
        if days is not None and days > 0:
            txt += f"⏳ 【 المتبقي 】 <b>{days} يوم</b>\n"

    if w.get("loan"):
        txt += f"💸 【 سلفة 】 {esc(str(w.get('loan')))}\n"

    subs = data.get("subaccounts", [])
    if subs:
        txt += "\n📊 【 تفصيل الرصيد 】\n"
        for s in subs:
            label = ACCOUNT_TYPE_NAMES.get(s.get("account_type"), f"نوع #{s.get('account_type')}")
            amt = s.get("amount", 0)
            line = f"  • {label}: <b>{amt:,}</b>"
            exp = s.get("expiry_date", "")
            if exp and exp != "2037-01-01T00:00:00":
                days = days_from_now(exp)
                if days is not None:
                    line += f" <i>({days} يوم)</i>"
            txt += line + "\n"

    return txt


def fmt_loyalty(data):
    l = data.get("loyalty", {})
    if not l:
        return "🔴 تعذّر جلب نقاط ممنون"

    tier_ar = l.get("localized_tier", {}).get("ar", l.get("tier", "—"))
    next_ar = l.get("localized_next_tier", {}).get("ar", l.get("next_tier", "—"))

    total = l.get("total_points", 0)
    spendable = l.get("total_spendable_points", 0)
    to_next = l.get("points_to_next_tier", 0)
    total_next = l.get("total_points_to_next_tier", 0)
    earned = total_next - to_next

    pct = (earned / total_next * 100) if total_next else 0
    filled = int(20 * pct / 100)
    bar = "█" * filled + "░" * (20 - filled)

    txt = (
        f"<b>🏆  【 نقاط ممنون 】</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ 【 المستوى الحالي 】 <b>{esc(tier_ar)}</b>\n"
        f"🥇 【 المستوى التالي 】 <b>{esc(next_ar)}</b>\n"
        f"📅 【 الانضمام 】 {esc(fmt_ts(l.get('tenure')))}\n"
        f"\n"
        f"💎 【 مجموع النقاط 】 <b>{total:,}</b>\n"
        f"💰 【 نقاط للاستبدال 】 <b>{spendable:,}</b>\n"
        f"📈 【 للترقية 】 <b>{to_next} نقطة</b>\n"
        f"\n"
        f"📊 【 التقدم 】\n"
        f"<code>[{bar}] {pct:.1f}%</code>\n"
        f"<code>{earned:,} / {total_next:,}</code>\n"
    )

    spendable_list = l.get("spendable_points", [])
    if spendable_list:
        txt += "\n🎁 【 نقاط قابلة للاستبدال 】\n"
        for p in spendable_list:
            txt += f"  • <b>{p.get('amount', 0):,}</b> نقطة <i>({p.get('validity', '')[:10]})</i>\n"

    return txt


def fmt_subs(data):
    subs = data.get("subscriptions", [])
    if not subs:
        return "<b>📦  【 الاشتراكات 】</b>\n━━━━━━━━━━━━━━━━━━━\n📭 لا توجد اشتراكات"

    txt = f"<b>📦  【 الاشتراكات ({len(subs)}) 】</b>\n━━━━━━━━━━━━━━━━━━━\n"

    for i, s in enumerate(subs, 1):
        status_str = STATUS_NAMES.get(s.get("status"), s.get("status", "—"))
        txt += (
            f"\n<b>#{i}</b> <code>{s.get('id')}</code>\n"
            f"  🔵 【 الحالة 】 {esc(status_str)}\n"
            f"  📅 【 التفعيل 】 {esc(fmt_ts(s.get('effective_time')))}\n"
            f"  📅 【 الانتهاء 】 {esc(fmt_ts(s.get('expire_time')))}\n"
        )
        days = days_from_now(s.get("expire_time"))
        if days is not None:
            txt += f"  ⏳ 【 المتبقي 】 <b>{days} يوم</b>\n"
        if s.get("is_kafoo_offer"):
            txt += "  👑 【 عرض كفو 】\n"

    return txt


def fmt_notifs(data):
    n = data.get("notifications", {})
    total = n.get("total_count", 0)
    unread = n.get("unread_count", 0)
    notifs = n.get("notifications", [])

    txt = (
        f"<b>📬  【 الإشعارات 】</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📊 【 الإجمالي 】 {total}\n"
        f"🔵 【 غير مقروء 】 {unread}\n"
    )

    if notifs:
        txt += "\n<b>آخر الإشعارات:</b>\n"
        for notif in notifs[:5]:
            icon = "🔵" if not notif.get("is_read") else "⚪"
            txt += f"  {icon} {esc(fmt_ts(notif.get('date_time')))}\n"

    return txt


def fmt_token_info(state):
    token = state.get("token", "")
    exp = get_expiry_from_token(token)
    hours = max(0, (exp - time.time()) / 3600) if exp else 0

    return (
        f"<b>🔑  【 معلومات التوكن 】</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📱 【 الحساب 】 <code>{esc(state.get('msisdn'))}</code>\n"
        f"📅 【 ينتهي 】 {esc(fmt_ts(exp))}\n"
        f"⏳ 【 المتبقي 】 <b>{hours:.1f} ساعة</b>\n"
        f"📏 【 الطول 】 {len(token)} حرف\n"
    )


# ═══════════════════════════════════════════════════════════
#         🎨 الأزرار (إيموجي عادي فقط)
# ═══════════════════════════════════════════════════════════
def kb_main(msisdn="—"):
    return [
        [make_button(f"👑 الحساب: {msisdn} 👑", "noop", color="primary")],
        [
            make_button("👤 الملف", "profile", color="primary"),
            make_button("💰 الرصيد", "balance", color="success"),
        ],
        [
            make_button("🏆 نقاط ممنون", "loyalty", color="primary"),
            make_button("📦 الاشتراكات", "subs", color="primary"),
        ],
        [
            make_button("📬 الإشعارات", "notifs", color="primary"),
            make_button("🔑 التوكن", "token_info", color="primary"),
        ],
        [make_button("📋 تقرير شامل", "full_report", color="success")],
        [
            make_button("🔄 تحديث", "refresh", color="primary"),
            make_button("🚪 خروج", "logout", color="danger"),
        ],
        [make_button("ℹ️ معلومات البوت", "bot_info", color="primary")],
        [
            make_button("👨‍💻 المطور", url=DEV_LINK, color="primary"),
            make_button("📢 القناة", url=CHANNEL_LINK, color="primary"),
        ],
    ]


def kb_back():
    return [
        [
            make_button("🔙 رجوع", "menu", color="primary"),
            make_button("🔄 تحديث", "refresh_section", color="success"),
        ],
        [make_button("🏠 القائمة الرئيسية", "menu", color="primary")],
    ]


# ═══════════════════════════════════════════════════════════
#         إرسال رسائل بأزرار ملوّنة
# ═══════════════════════════════════════════════════════════
async def reply_colored(update_or_query, text, keyboard_rows, edit=False):
    if edit:
        chat_id = update_or_query.message.chat.id
        message_id = update_or_query.message.message_id

        result = edit_colored_keyboard(chat_id, message_id, text, keyboard_rows)

        if result and not result.get("ok"):
            desc = result.get("description", "")
            if "not modified" not in desc:
                await reply_colored(update_or_query, text, keyboard_rows, edit=False)
    else:
        chat_id = None
        if hasattr(update_or_query, "message") and update_or_query.message:
            chat_id = update_or_query.message.chat.id
        elif hasattr(update_or_query, "effective_chat"):
            chat_id = update_or_query.effective_chat.id

        if chat_id:
            send_colored_keyboard(chat_id, text, keyboard_rows)


# ═══════════════════════════════════════════════════════════
#                    أوامر البوت
# ═══════════════════════════════════════════════════════════
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    USER_STATE[user.id] = {"step": "waiting_input", "name": user.first_name}

    welcome = (
        f"👑 <b>أهلاً {esc(user.first_name)}</b>\n\n"
        f"✨ <b>بوت زين العراق</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔵 <b>كيفية الاستخدام:</b>\n\n"
        f"📱 <b>الطريقة 1 — رقم + كلمة مرور:</b>\n"
        f"  أرسل رقمك مباشرة\n"
        f"  مثال: <code>7801234567</code>\n\n"
        f"🔑 <b>الطريقة 2 — access_token:</b>\n"
        f"  أرسل التوكن مباشرة\n"
        f"  البوت سيتعرف عليه تلقائياً\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ <b>حقوق التطوير:</b> {DEVELOPER}\n"
    )

    send_colored_keyboard(update.effective_chat.id, welcome, [])


async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = USER_STATE.get(user_id, {})

    if not state.get("token"):
        send_colored_keyboard(update.effective_chat.id, "🔴 لا يوجد حساب مسجل. ابدأ بـ /start", [])
        return

    text = (
        f"🏠 <b>القائمة الرئيسية</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 الحساب: <code>{esc(state.get('msisdn'))}</code>"
    )
    send_colored_keyboard(update.effective_chat.id, text, kb_main(state.get("msisdn")))


async def cmd_dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    send_colored_keyboard(
        update.effective_chat.id,
        f"🛡️ <b>حقوق التطوير</b>\n\n"
        f"✨ المطوّر: {DEVELOPER}\n"
        f"🔥 الرابط: {DEV_LINK}",
        []
    )


# ═══════════════════════════════════════════════════════════
#                    معالجة الرسائل
# ═══════════════════════════════════════════════════════════
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not text:
        return

    state = USER_STATE.get(user_id, {})

    # ─── 1. كلمة المرور ───
    if state.get("step") == "waiting_password":
        msisdn = state["msisdn"]
        password = text

        msg = await update.message.reply_text(ce("🔄 <i>جاري تسجيل الدخول...</i>"), parse_mode=ParseMode.HTML)

        token, error = login_zain(msisdn, password)

        if error:
            await msg.edit_text(
                ce(f"🔴 <b>فشل تسجيل الدخول</b>\n\nالسبب: {esc(error)}\n\nحاول مرة أخرى أو اكتب /start"),
                parse_mode=ParseMode.HTML
            )
            USER_STATE[user_id] = {"step": "waiting_input"}
            return

        try:
            await update.message.delete()
        except Exception:
            pass

        USER_STATE[user_id] = {
            "step": "logged_in",
            "token": token,
            "msisdn": msisdn,
            "name": state.get("name", ""),
        }

        await msg.edit_text(ce("🔄 <i>جاري جلب البيانات...</i>"), parse_mode=ParseMode.HTML)
        data = get_user_data(user_id, token, msisdn, force=True)
        summary = fmt_summary(data, msisdn)

        try:
            await msg.delete()
        except Exception:
            pass

        welcome_text = (
            f"🟢 <b>تم تسجيل الدخول بنجاح</b>\n\n"
            f"✨ <b>الملخص السريع</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{summary}\n"
            f"✨ <b>اختر من القائمة:</b>"
        )
        send_colored_keyboard(update.effective_chat.id, welcome_text, kb_main(msisdn))
        return

    # ─── 2. JWT token ───
    if text.startswith("eyJ") and text.count(".") == 2:
        token_type = identify_token_type(text)

        if token_type == "refresh":
            send_colored_keyboard(
                update.effective_chat.id,
                f"⚠️ <b>هذا refresh_token وليس access_token</b>\n\n"
                f"refresh_token لا يعمل مع الـ endpoints.\n"
                f"استخدم access_token بدلاً منه.\n\n"
                f"🔵 سجّل دخول برقم + كلمة مرور للحصول على access_token.",
                []
            )
            return

        if token_type == "invalid":
            send_colored_keyboard(update.effective_chat.id, "🔴 التوكن غير صالح", [])
            return

        msisdn = get_msisdn_from_token(text)
        exp = get_expiry_from_token(text)

        if exp and time.time() >= exp:
            send_colored_keyboard(
                update.effective_chat.id,
                f"🔴 <b>التوكن منتهي الصلاحية</b>\n\nانتهى في: {esc(fmt_ts(exp))}",
                []
            )
            return

        USER_STATE[user_id] = {
            "step": "logged_in",
            "token": text,
            "msisdn": msisdn,
        }

        msg = await update.message.reply_text(ce("🔄 <i>جاري جلب البيانات...</i>"), parse_mode=ParseMode.HTML)
        data = get_user_data(user_id, text, msisdn, force=True)
        summary = fmt_summary(data, msisdn)

        hours = max(0, (exp - time.time()) / 3600) if exp else 0

        try:
            await msg.delete()
        except Exception:
            pass

        welcome_text = (
            f"🟢 <b>تم التعرف على التوكن</b>\n\n"
            f"✨ <b>الملخص السريع</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{summary}\n"
            f"⏳ <b>صلاحية التوكن:</b> {hours:.1f} ساعة\n\n"
            f"✨ <b>اختر من القائمة:</b>"
        )
        send_colored_keyboard(update.effective_chat.id, welcome_text, kb_main(msisdn))
        return

    # ─── 3. رقم ───
    if re.match(r'^[+]?[\d\s\-]{9,}$', text):
        msisdn = normalize_msisdn(text)

        if not validate_msisdn(msisdn):
            send_colored_keyboard(
                update.effective_chat.id,
                "🔴 <b>رقم غير صالح</b>\n\nيجب أن يبدأ بـ 077 أو 078 ويتكون من 10 أرقام",
                []
            )
            return

        USER_STATE[user_id] = {
            "step": "waiting_password",
            "msisdn": msisdn,
            "name": state.get("name", ""),
        }

        send_colored_keyboard(
            update.effective_chat.id,
            f"📱 <b>الرقم:</b> <code>{esc(msisdn)}</code>\n\n"
            f"🔑 <b>أرسل كلمة المرور الآن</b>\n"
            f"<i>(سيتم حذف رسالة كلمة المرور تلقائياً للأمان)</i>",
            []
        )
        return

    # ─── 4. غير معروف ───
    send_colored_keyboard(
        update.effective_chat.id,
        f"⚠️ <b>لم أفهم المدخل</b>\n\n"
        f"أرسل:\n"
        f"  📱 رقم الهاتف (مثل: 07801234567)\n"
        f"  🔑 أو access_token",
        []
    )


# ═══════════════════════════════════════════════════════════
#                    معالجة الأزرار
# ═══════════════════════════════════════════════════════════
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    state = USER_STATE.get(user_id, {})
    action = query.data

    if action == "noop":
        return

    # ─── معلومات البوت ───
    if action == "bot_info":
        text = (
            f"ℹ️ <b>معلومات البوت</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"👑 <b>الاسم:</b> بوت زين العراق\n"
            f"📌 <b>الوصف:</b> واجهة تفاعلية لحساب زين\n"
            f"🔖 <b>الإصدار:</b> v6.0\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER}\n"
            f"📢 <b>القناة:</b> {CHANNEL_LINK}\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ <b>المميزات:</b>\n"
            f"  • عرض الرصيد الكامل\n"
            f"  • نقاط ممنون والمستوى\n"
            f"  • الاشتراكات والإشعارات\n"
            f"  • تقرير شامل\n"
            f"  • إيموجيات مميزة 🎨\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        await reply_colored(query, text, kb_back(), edit=True)
        return

    if action not in ("menu",) and not state.get("token"):
        await reply_colored(query, "🔴 جلسة منتهية. ابدأ بـ /start", [], edit=True)
        return

    token = state.get("token")
    msisdn = state.get("msisdn")

    # ─── رجوع للقائمة ───
    if action == "menu":
        data = get_user_data(user_id, token, msisdn)
        summary = fmt_summary(data, msisdn)
        text = (
            f"🏠 <b>القائمة الرئيسية</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ <b>الملخص السريع</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{summary}"
        )
        await reply_colored(query, text, kb_main(msisdn), edit=True)
        return

    # ─── تحديث ───
    if action in ("refresh", "refresh_section"):
        CACHE.pop(user_id, None)
        data = get_user_data(user_id, token, msisdn, force=True)
        summary = fmt_summary(data, msisdn)
        text = (
            f"🔄 <b>تم التحديث</b>\n\n"
            f"✨ <b>الملخص السريع</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{summary}"
        )
        await reply_colored(query, text, kb_main(msisdn), edit=True)
        return

    # ─── خروج ───
    if action == "logout":
        USER_STATE.pop(user_id, None)
        CACHE.pop(user_id, None)
        await reply_colored(query, "🚪 <b>تم تسجيل الخروج بنجاح</b>\n\nللدخول مجدداً، أرسل /start", [], edit=True)
        return

    # ─── جلب البيانات ───
    data = get_user_data(user_id, token, msisdn)

    # ─── الملف الشخصي ───
    if action == "profile":
        await reply_colored(query, fmt_profile(data), kb_back(), edit=True)
        return

    # ─── الرصيد ───
    if action == "balance":
        await reply_colored(query, fmt_balance(data), kb_back(), edit=True)
        return

    # ─── نقاط ممنون ───
    if action == "loyalty":
        await reply_colored(query, fmt_loyalty(data), kb_back(), edit=True)
        return

    # ─── الاشتراكات ───
    if action == "subs":
        await reply_colored(query, fmt_subs(data), kb_back(), edit=True)
        return

    # ─── الإشعارات ───
    if action == "notifs":
        await reply_colored(query, fmt_notifs(data), kb_back(), edit=True)
        return

    # ─── التوكن ───
    if action == "token_info":
        await reply_colored(query, fmt_token_info(state), kb_back(), edit=True)
        return

    # ─── تقرير شامل ───
    if action == "full_report":
        txt = (
            f"📋 <b>التقرير الشامل</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{fmt_summary(data, msisdn)}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{fmt_profile(data)}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{fmt_balance(data)}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{fmt_loyalty(data)}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{fmt_subs(data)}\n"
        )

        if len(txt) > 4000:
            await reply_colored(query, fmt_summary(data, msisdn), kb_back(), edit=True)
            for section_txt in [fmt_profile(data), fmt_balance(data), fmt_loyalty(data), fmt_subs(data)]:
                await reply_colored(query, section_txt, [], edit=False)
        else:
            await reply_colored(query, txt, kb_back(), edit=True)
        return


# ═══════════════════════════════════════════════════════════
#                    خطأ عام
# ═══════════════════════════════════════════════════════════
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error: {context.error}")


# ═══════════════════════════════════════════════════════════
#                    التشغيل
# ═══════════════════════════════════════════════════════════
def main():
    if BOT_TOKEN == "8649116276:AAGRor3c0juxDASZ2tJPutf31nGbXQ2NsSg":
        print("🔴 ضع BOT_TOKEN أولاً!")
        return

    print("🔥 جاري تشغيل البوت...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("menu", cmd_menu))
    app.add_handler(CommandHandler("dev", cmd_dev))

    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print(f"🟢 البوت يعمل — المطوّر: {DEVELOPER}")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
