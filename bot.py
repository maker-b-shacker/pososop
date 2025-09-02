import requests
import time

BOT_TOKEN = "8467049726:AAGeWgyesbFpr3l28X90U7tFFkiNh6phUxM"

# 🔧 لطفا آیدی کانال‌های خود را اینجا اصلاح کنید:
# آیدی کانال باید با @ شروع شود و بات باید ادمین کانال باشد
REQUIRED_CHANNELS = [
    {"id": "@Hrteam_ir", "name": "کانال اصلی HR Team", "url": "https://t.me/Hrteam_ir"},
    {"id": "@trust_hr_team", "name": "کانال اعتماد hr"" Team", "url": "https://t.me/trust_hr_team"}
]

# 📝 راهنمای اصلاح آیدی کانال:
# 1. آیدی کانال باید با @ شروع شود (مثال: @MyChannel)
# 2. بات باید در کانال ادمین باشد
# 3. لینک کانال را هم در قسمت url قرار دهید
# 4. نام کانال را به فارسی یا انگلیسی بنویسید

# ذخیره زبان کاربران در حافظه (موقت)
user_languages = {}

def send_message(chat_id, text, keyboard=None, parse_mode=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = keyboard
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        response = requests.post(url, json=payload)
        print(f"✅ پیام به {chat_id} ارسال شد")
        return response.json()
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")
        return None

def check_user_membership(user_id):
    """بررسی عضویت کاربر در کانال‌های اجباری"""
    try:
        not_joined_channels = []
        
        for channel in REQUIRED_CHANNELS:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
            payload = {
                "chat_id": channel["id"],
                "user_id": user_id
            }
            response = requests.post(url, json=payload).json()
            
            if response["ok"]:
                status = response["result"]["status"]
                if status in ["left", "kicked"]:
                    not_joined_channels.append(channel)
            else:
                print(f"❌ خطا در بررسی عضویت کانال {channel['name']}: {response.get('description', 'Unknown error')}")
                not_joined_channels.append(channel)
        
        return len(not_joined_channels) == 0, not_joined_channels
    except Exception as e:
        print(f"❌ خطا در بررسی عضویت: {e}")
        return False, REQUIRED_CHANNELS

def membership_required_keyboard(not_joined_channels):
    """کیبورد عضویت اجباری"""
    buttons = []
    for channel in not_joined_channels:
        buttons.append([{"text": f"📢 عضویت در {channel['name']}", "url": channel["url"]}])
    
    buttons.append([{"text": "🔍 بررسی مجدد عضویت", "callback_data": "check_membership"}])
    
    return {"inline_keyboard": buttons}

def language_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🇮🇷 فارسی", "callback_data": "fa"}],
            [{"text": "🇺🇸 English", "callback_data": "en"}]
        ]
    }

def menu_keyboard(lang):
    options = {
        "fa": [
            [{"text": "🎯 آموزش دیداسر", "callback_data": "ddoser"}],
            [{"text": "🌐 آموزش آیپی چکر", "callback_data": "ip_hack"}],
            [{"text": "💣 آموزش اس ام اس بمبر", "callback_data": "bomber"}]
        ],
        "en": [
            [{"text": "🎯 DDoser Tutorial", "callback_data": "ddoser"}],
            [{"text": "🌐 IP changer Tutorial", "callback_data": "ip_changer"}],
            [{"text": "💣 SMS Bomber Tutorial", "callback_data": "bomber"}]
        ]
    }
    return {"inline_keyboard": options[lang]}

def get_config_help():
    """راهنمای پیکربندی بات"""
    help_text = """
🔧 <b>راهنمای تنظیمات بات:</b>

📝 <b>برای اصلاح آیدی کانال‌ها:</b>
1. متغیر REQUIRED_CHANNELS را پیدا کنید
2. آیدی کانال خود را جایگزین @Hrteam_ir کنید
3. نام کانال خود را قرار دهید
4. لینک کانال خود را قرار دهید

📋 <b>مثال:</b>
REQUIRED_CHANNELS = [
    {"id": "@Your_Channel", "name": "نام کانال شما", "url": "https://t.me/Your_Channel"},
    {"id": "@Your_Second_Channel", "name": "کانال دوم شما", "url": "https://t.me/Your_Second_Channel"}
]

⚠️ <b>نکات مهم:</b>
- بات باید در کانال ادمین باشد
- آیدی کانال باید با @ شروع شود
- لینک کانال باید معتبر باشد
"""
    return help_text

print("🤖 ربات شروع به کار کرد...")
print("📋 کانال‌های اجباری تنظیم شده:")
for i, channel in enumerate(REQUIRED_CHANNELS, 1):
    print(f"   {i}. {channel['name']} ({channel['id']})")

print("\n🔧 اگر نیاز به اصلاح آیدی کانال دارید:")
print("   - متغیر REQUIRED_CHANNELS را در خط ۸ پیدا کنید")
print("   - آیدی کانال خود را جایگزین کنید")
print("   - بات باید در کانال ادمین باشد\n")

update_id = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={update_id+1}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data["ok"] and data["result"]:
                for update in data["result"]:
                    update_id = update["update_id"]
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        user_id = msg["from"]["id"]
                        text = msg.get("text", "")
                        
                        if "/start" in text:
                            print(f"📨 کاربر {user_id} دستور /start را زد")
                            
                            # بررسی عضویت کاربر
                            is_member, not_joined_channels = check_user_membership(user_id)
                            
                            if is_member:
                                send_message(chat_id, "✅ شما در همه کانال‌ها عضو هستید!\n\nلطفا زبان انتخاب کنید / Please choose language:", language_keyboard())
                            else:
                                message_text = f"""
⚠️ <b>برای استفاده از ربات، باید در کانال‌های زیر عضو شوید:</b>

"""
                                for channel in not_joined_channels:
                                    message_text += f"• {channel['name']}\n"
                                
                                message_text += "\n📌 پس از عضویت، روی دکمه «بررسی مجدد عضویت» کلیک کنید."
                                send_message(chat_id, message_text, membership_required_keyboard(not_joined_channels), "HTML")
                        
                        elif "/config" in text and str(user_id) == "YOUR_ADMIN_ID":  # جایگزین با آی‌دی خود
                            send_message(chat_id, get_config_help(), None, "HTML")
                    
                    elif "callback_query" in update:
                        query = update["callback_query"]
                        data = query["data"]
                        chat_id = query["message"]["chat"]["id"]
                        user_id = query["from"]["id"]
                        print(f"🖱 کاربر {user_id} روی {data} کلیک کرد")
                        
                        if data == "check_membership":
                            # بررسی مجدد عضویت
                            is_member, not_joined_channels = check_user_membership(user_id)
                            
                            if is_member:
                                send_message(chat_id, "✅ عالی! حالا شما در همه کانال‌ها عضو هستید!\n\nلطفا زبان انتخاب کنید:", language_keyboard())
                            else:
                                message_text = f"""
❌ <b>هنوز در برخی کانال‌ها عضو نشده‌اید!</b>

"""
                                for channel in not_joined_channels:
                                    message_text += f"• {channel['name']}\n"
                                
                                message_text += "\n📌 لطفا ابتدا در کانال‌های بالا عضو شوید و سپس مجدد بررسی کنید."
                                send_message(chat_id, message_text, membership_required_keyboard(not_joined_channels), "HTML")
                        
                        elif data in ["fa", "en"]:
                            # بررسی مجدد عضویت قبل از نمایش منو
                            is_member, not_joined_channels = check_user_membership(user_id)
                            
                            if is_member:
                                user_languages[user_id] = data
                                welcome = "✅ خوش آمدید! 🙏\n\nلطفا یک گزینه انتخاب کنید:" if data == "fa" else "✅ Welcome! 🙏\n\nPlease choose an option:"
                                send_message(chat_id, welcome, menu_keyboard(data))
                            else:
                                message_text = "❌ ابتدا باید در کانال‌ها عضو شوید!" if data == "fa" else "❌ You must join the channels first!"
                                send_message(chat_id, message_text, membership_required_keyboard(not_joined_channels))
                        
                        elif data in ["ddoser", "ip_Checker", "bomber"]:
                            # بررسی مجدد عضویت قبل از ارسال لینک
                            is_member, not_joined_channels = check_user_membership(user_id)
                            
                            if is_member:
                                lang = user_languages.get(user_id, "fa")
                                links = {
                                    "ddoser": "https://t.me/Hrteam_ir/6694",
                                    "ip_Checker": "https://t.me/Hrteam_ir/6699", 
                                    "bomber": "https://t.me/Hrteam_ir/6677"
                                }
                                
                                if data in links:
                                    titles = {
                                        "ddoser": {"fa": "آموزش دیداسر", "en": "DDoser Tutorial"},
                                        "ip_hack": {"fa": "آموزش آیپی چکر", "en": "IP Checker Tutorial"},
                                        "bomber": {"fa": "آموزش اس ام اس بمبر", "en": "SMS Bomber Tutorial"}
                                    }
                                    
                                    title = titles[data][lang]
                                    message = f"📚 {title}:\n\n🔗 {links[data]}" if lang == "fa" else f"📚 {title}:\n\n🔗 {links[data]}"
                                    send_message(chat_id, message)
                                else:
                                    error_msg = "⚠️ لینک برای این گزینه یافت نشد" if lang == "fa" else "⚠️ Link not found for this option"
                                    send_message(chat_id, error_msg)
                            else:
                                lang = user_languages.get(user_id, "fa")
                                message_text = "❌ ابتدا باید در کانال‌ها عضو شوید!" if lang == "fa" else "❌ You must join the channels first!"
                                send_message(chat_id, message_text, membership_required_keyboard(not_joined_channels))
        
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        time.sleep(5)
