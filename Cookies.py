import telebot
from telebot import types
import os
import logging
import json
from datetime import datetime
import random
import glob

TOKEN = "8297620545:AAG-xyRqEw7y6fI7ju5JYTnpIJoSMTSAlq4"
bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Файлы для хранения данных
USERS_FILE = "users_data.json"
ADMIN_LOG_FILE = "admin_logs.json"

# Админские пароли
ADMIN_PASSWORDS = {
    "mower123": "mmm111999abzo",
    "HGF_MOZT": "sina3488ar21"
}

# Состояния для админ-панели
ADMIN_STATES = {}
# Состояния для покупки куки
PURCHASE_STATES = {}

# Структура папок для куки
COOKIE_FOLDERS = {
    "donate": "Донатки",
    "voice": "Voice chat",
    "premium": "Premium",
    "adopt_me": "Adopt Me",
    "grow_garden": "Grow a Garden",
    "steal_brainrot": "Steal a Brainrot",
    "blox_fruits_3sea": "Blox Fruits [3 Sea]",
    "mm2_100lvl": "MM2 [100 LVL]"
}

# Соответствие текста кнопок и ключей папок
BUTTON_TO_FOLDER = {
    '💰 Донатки': 'donate',
    '🎤 Voice chat': 'voice',
    '👑 Premium': 'premium',
    '🦊 Adopt Me': 'adopt_me',
    '🌱 Grow a Garden': 'grow_garden',
    '🧠 Steal a Brainrot': 'steal_brainrot',
    '⚔️ Blox Fruits [3 Sea]': 'blox_fruits_3sea',
    '🔪 MM2 [100 LVL]': 'mm2_100lvl'
}

# Цены для куки
COOKIE_PRICES = {
    "Донатки": 15,
    "Voice chat": 40,
    "Premium": 50,
    "Adopt Me": 30,
    "Grow a Garden": 35,
    "Steal a Brainrot": 40,
    "Blox Fruits [3 Sea]": 45,
    "MM2 [100 LVL]": 35
}

# Создаем структуру папок
def create_cookie_folders():
    """Создает папки для хранения куки файлов"""
    base_folder = "Cookies"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    for folder in COOKIE_FOLDERS.keys():
        folder_path = os.path.join(base_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Создана папка для куки: {folder}")
    
    # Создаем README файл в каждой папке для информации
    for folder_key, display_name in COOKIE_FOLDERS.items():
        folder_path = os.path.join(base_folder, folder_key)
        readme_file = os.path.join(folder_path, "README.txt")
        if not os.path.exists(readme_file):
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(f"Папка для хранения куки: {display_name}\n")
                f.write(f"Цена: {COOKIE_PRICES.get(display_name, 0)} Stars\n")
                f.write(f"Добавляйте файлы .txt с куками в эту папку.\n")
                f.write(f"Каждый файл должен содержать один куки.\n")
                f.write(f"Файлы автоматически удаляются после отправки покупателю.\n")

# Получаем количество файлов в папке
def get_cookie_count(cookie_type):
    """Возвращает количество доступных куки определенного типа"""
    if cookie_type not in COOKIE_FOLDERS:
        return 0
    
    folder_path = os.path.join("Cookies", cookie_type)
    if os.path.exists(folder_path):
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        # Исключаем README.txt из подсчета
        txt_files = [f for f in txt_files if not f.endswith("README.txt")]
        return len(txt_files)
    return 0

# Получаем случайный файл куки
def get_random_cookie_file(cookie_type):
    """Возвращает случайный файл куки из указанной папки"""
    if cookie_type not in COOKIE_FOLDERS:
        return None
    
    folder_path = os.path.join("Cookies", cookie_type)
    if os.path.exists(folder_path):
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        # Исключаем README.txt из выбора
        txt_files = [f for f in txt_files if not f.endswith("README.txt")]
        if txt_files:
            return random.choice(txt_files)
    return None

# Удаляем файл куки после отправки
def delete_cookie_file(file_path):
    """Удаляет файл куки после отправки пользователю"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Файл удален: {file_path}")
            return True
    except Exception as e:
        logger.error(f"Ошибка удаления файла {file_path}: {e}")
    return False

# ===== ФУНКЦИИ ДЛЯ РАБОТЫ С ДАННЫМИ =====

def load_users_data():
    """Загружает данные пользователей"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
    return {}

def save_users_data(users_data):
    """Сохраняет данные пользователей"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения данных: {e}")

def load_admin_logs():
    """Загружает логи администраторов"""
    try:
        if os.path.exists(ADMIN_LOG_FILE):
            with open(ADMIN_LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки логов админов: {e}")
    return []

def save_admin_logs(logs):
    """Сохраняет логи администраторов"""
    try:
        with open(ADMIN_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения логов админов: {e}")

def add_admin_log(admin_name, action, target_username, amount, notes=""):
    """Добавляет запись в логи администраторов"""
    logs = load_admin_logs()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "admin": admin_name,
        "action": action,
        "target_username": target_username,
        "amount": amount,
        "notes": notes
    }
    
    logs.append(log_entry)
    save_admin_logs(logs)
    logger.info(f"Лог админа: {admin_name} {action} {amount} Stars пользователю {target_username}")

def get_user_data(user_id):
    """Получает данные пользователя"""
    users_data = load_users_data()
    user_id_str = str(user_id)
    
    if user_id_str not in users_data:
        users_data[user_id_str] = {
            "username": "",
            "usdt_balance": 0,
            "stars_balance": 0,
            "total_spent": 0,
            "transactions": [],
            "cookies_purchased": [],
            "registration_date": datetime.now().isoformat()
        }
        save_users_data(users_data)
    
    return users_data[user_id_str]

def update_user_data(user_id, data_update):
    """Обновляет данные пользователя"""
    users_data = load_users_data()
    user_id_str = str(user_id)
    
    if user_id_str not in users_data:
        users_data[user_id_str] = {}
    
    users_data[user_id_str].update(data_update)
    save_users_data(users_data)

def get_user_by_username(username):
    """Получает пользователя по username"""
    if not username:
        return None, None
    
    users_data = load_users_data()
    for user_id, user_data in users_data.items():
        user_username = user_data.get("username", "")
        if user_username and user_username.lower() == username.lower():
            return user_id, user_data
    return None, None

def add_transaction(user_id, amount, status="completed", transaction_type="stars_purchase", cookie_name=None):
    """Добавляет транзакцию"""
    user_data = get_user_data(user_id)
    
    transaction = {
        "date": datetime.now().isoformat(),
        "amount": amount,
        "status": status,
        "type": transaction_type,
        "cookie_name": cookie_name
    }
    
    if "transactions" not in user_data:
        user_data["transactions"] = []
    
    user_data["transactions"].append(transaction)
    
    # Обновляем баланс
    if status == "completed":
        user_data["stars_balance"] = user_data.get("stars_balance", 0) + amount
        if amount > 0:
            user_data["total_spent"] = user_data.get("total_spent", 0) + amount
    
    update_user_data(user_id, user_data)

# ===== МЕНЮ И КЛАВИАТУРЫ =====

def main_menu(user_id=None):
    """Главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton('📦 Магазин')
    btn2 = types.KeyboardButton('👤 Профиль')
    btn3 = types.KeyboardButton('🆘 Помощь')
    btn4 = types.KeyboardButton('📋 Команды')
    btn5 = types.KeyboardButton('ℹ️ Информация о боте')
    btn6 = types.KeyboardButton('📄 Информация')
    btn7 = types.KeyboardButton('🧪 Тест')
    btn8 = types.KeyboardButton('📞 Контакты')
    
    # Добавляем кнопку админ-панели только для авторизованных админов
    if user_id and user_id in ADMIN_STATES and ADMIN_STATES[user_id].get("authorized"):
        btn_admin = types.KeyboardButton('👑 Admin Panel')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn_admin)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    return markup

def shop_menu():
    """Меню магазина"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton('🛒 Печеньки')
    btn2 = types.KeyboardButton('⭐ Пополнить Stars')
    btn3 = types.KeyboardButton('🔙 Назад')
    
    markup.add(btn1, btn2, btn3)
    return markup

def cookies_menu():
    """Меню выбора куки"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton('💰 Донатки')
    btn2 = types.KeyboardButton('🎤 Voice chat')
    btn3 = types.KeyboardButton('👑 Premium')
    btn4 = types.KeyboardButton('🦊 Adopt Me')
    btn5 = types.KeyboardButton('🌱 Grow a Garden')
    btn6 = types.KeyboardButton('🧠 Steal a Brainrot')
    btn7 = types.KeyboardButton('⚔️ Blox Fruits [3 Sea]')
    btn8 = types.KeyboardButton('🔪 MM2 [100 LVL]')
    btn9 = types.KeyboardButton('🔙 Назад')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return markup

def profile_menu():
    """Меню профиля"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton('⭐ Пополнить Stars')
    btn2 = types.KeyboardButton('📊 Мои транзакции')
    btn3 = types.KeyboardButton('🍪 Мои куки')
    btn4 = types.KeyboardButton('🔙 Назад')
    
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def payment_amount_menu():
    """Меню пополнения"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    btn1 = types.KeyboardButton('25 ⭐')
    btn2 = types.KeyboardButton('50 ⭐')
    btn3 = types.KeyboardButton('75 ⭐')
    btn4 = types.KeyboardButton('100 ⭐')
    btn5 = types.KeyboardButton('150 ⭐')
    btn6 = types.KeyboardButton('200 ⭐')
    btn7 = types.KeyboardButton('🔙 Назад')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

def admin_panel_menu():
    """Меню админ-панели"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton('💰 Add Money')
    btn2 = types.KeyboardButton('📉 Withdraw Money')
    btn3 = types.KeyboardButton('📊 Users Stats')
    btn4 = types.KeyboardButton('📝 Dupe IP')
    btn5 = types.KeyboardButton('🔙 Назад')
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def inline_menu():
    """Инлайн кнопки"""
    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton('📋 Команды', callback_data='commands')
    btn2 = types.InlineKeyboardButton('ℹ️ О боте', callback_data='about')
    
    markup.add(btn1, btn2)
    return markup

# ===== ОСНОВНЫЕ КОМАНДЫ =====

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    create_cookie_folders()
    
    user = message.from_user
    user_data = {
        "username": user.username or user.first_name,
        "last_active": datetime.now().isoformat()
    }
    update_user_data(user.id, user_data)
    
    welcome_text = """
🤖 **Добро пожаловать в MonickCookies Bot!** 🍪

🎮 **Новые куки в продаже!**
⚔️ Blox Fruits [3 Sea] - 45 ⭐
🔪 MM2 [100 LVL] - 35 ⭐

Выбери действие кнопками ниже ↓
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(user.id))
    bot.send_message(message.chat.id, "Или используй быстрые кнопки:", reply_markup=inline_menu())

@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды /help"""
    help_text = """
📋 **Доступные команды:**

/start - Главное меню
/help - Помощь
/profile - Мой профиль
/balance - Мой баланс
/buy - Купить Stars
/shop - Магазин

**Или используй кнопки!** 🎛️
    """
    bot.send_message(message.chat.id, help_text, reply_markup=main_menu(message.from_user.id))

@bot.message_handler(commands=['profile'])
def profile_command(message):
    """Обработчик команды /profile"""
    show_profile(message)

@bot.message_handler(commands=['balance'])
def balance_command(message):
    """Обработчик команды /balance"""
    user_data = get_user_data(message.from_user.id)
    balance_text = f"""
💰 **Ваш баланс:**

💎 USDT: {user_data.get('usdt_balance', 0)}
⭐ STARS: {user_data.get('stars_balance', 0)}
📈 Всего пополнено: {user_data.get('total_spent', 0)} Stars
    """
    bot.send_message(message.chat.id, balance_text)

@bot.message_handler(commands=['buy'])
def buy_command(message):
    """Обработчик команды /buy"""
    add_balance(message)

@bot.message_handler(commands=['shop'])
def shop_command(message):
    """Обработчик команды /shop"""
    show_shop(message)

@bot.message_handler(commands=['teststars'])
def teststars_command(message):
    """Скрытая команда для теста Stars"""
    user = message.from_user
    user_id = user.id
    
    logger.info(f"Скрытая команда: пользователь {user_id} ({user.username}) использует /teststars")
    
    amount = 1
    
    try:
        prices = [types.LabeledPrice(label="Пополнение Stars", amount=amount)]
        
        bot.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение STARS на 1",
            description="Покупка 1 Star для использования в боте",
            invoice_payload=f"stars_{amount}_{user_id}",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter="stars_1",
            photo_url="https://img.icons8.com/color/96/000000/star--v1.png",
            photo_width=96,
            photo_height=96,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False
        )
        
        logger.info(f"Создан скрытый счет на {amount} Star для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"Ошибка создания скрытого счета: {e}")
        bot.send_message(message.chat.id, "Попробуйте позже.")

# ===== АДМИН-ПАНЕЛЬ =====

@bot.message_handler(commands=['admin'])
def admin_command(message):
    """Секретная админ-панель"""
    user = message.from_user
    user_id = user.id
    
    logger.info(f"Секретная команда: пользователь {user_id} ({user.username}) пытается войти в админ-панель")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('mower123')
    btn2 = types.KeyboardButton('HGF_MOZT')
    btn3 = types.KeyboardButton('🔙 Назад')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, "👑 **Секретная админ-панель**\n\nВыберите администратора:", reply_markup=markup)
    
    ADMIN_STATES[user_id] = {"step": "select_admin"}

@bot.message_handler(func=lambda message: message.text in ['mower123', 'HGF_MOZT', 'makaroska'])
def handle_admin_selection(message):
    """Обработка выбора администратора"""
    user_id = message.from_user.id
    
    if user_id in ADMIN_STATES and ADMIN_STATES[user_id].get("step") == "select_admin":
        selected_admin = message.text
        
        ADMIN_STATES[user_id] = {
            "step": "enter_password",
            "selected_admin": selected_admin
        }
        
        bot.send_message(message.chat.id, f"🔐 Введите пароль для {selected_admin}:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "enter_password")
def handle_admin_password(message):
    """Обработка ввода пароля"""
    user_id = message.from_user.id
    password = message.text
    admin_data = ADMIN_STATES[user_id]
    selected_admin = admin_data["selected_admin"]
    
    if selected_admin in ADMIN_PASSWORDS and password == ADMIN_PASSWORDS[selected_admin]:
        ADMIN_STATES[user_id] = {
            "authorized": True,
            "admin_name": selected_admin,
            "step": "admin_panel"
        }
        
        logger.info(f"Успешная авторизация: {selected_admin} (ID: {user_id})")
        bot.send_message(message.chat.id, f"✅ **Авторизация успешна!**\nДобро пожаловать, {selected_admin}!",
                        reply_markup=main_menu(user_id))
    else:
        bot.send_message(message.chat.id, "❌ **Неверный пароль!**\nДоступ запрещен.", 
                        reply_markup=main_menu(user_id))
        
        if user_id in ADMIN_STATES:
            del ADMIN_STATES[user_id]

@bot.message_handler(func=lambda message: message.text == '👑 Admin Panel')
def show_admin_panel(message):
    """Показать админ-панель"""
    user_id = message.from_user.id
    
    if user_id in ADMIN_STATES and ADMIN_STATES[user_id].get("authorized"):
        admin_name = ADMIN_STATES[user_id].get("admin_name", "Admin")
        
        users_data = load_users_data()
        total_users = len(users_data)
        total_stars = sum(user.get("stars_balance", 0) for user in users_data.values())
        total_transactions = sum(len(user.get("transactions", [])) for user in users_data.values())
        
        stats_text = f"""
👑 **Админ-панель** | {admin_name}

📊 Статистика:
👥 Пользователей: {total_users}
⭐ Всего Stars: {total_stars}
📈 Транзакций: {total_transactions}

Выберите действие:
"""
        bot.send_message(message.chat.id, stats_text, reply_markup=admin_panel_menu())
    else:
        bot.send_message(message.chat.id, "❌ Доступ запрещен.", reply_markup=main_menu(user_id))

@bot.message_handler(func=lambda message: message.text == '💰 Add Money' and 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("authorized"))
def handle_add_money(message):
    """Добавить деньги пользователю"""
    user_id = message.from_user.id
    ADMIN_STATES[user_id]["step"] = "add_money_username"
    bot.send_message(message.chat.id, "👤 Введите username пользователя для пополнения:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "add_money_username")
def handle_add_money_username(message):
    """Обработка username для добавления денег"""
    user_id = message.from_user.id
    target_username = message.text.strip().replace('@', '')
    
    if not target_username:
        bot.send_message(message.chat.id, "❌ Username не может быть пустым!", reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"
        return
    
    ADMIN_STATES[user_id]["step"] = "add_money_amount"
    ADMIN_STATES[user_id]["target_username"] = target_username
    
    bot.send_message(message.chat.id, f"💰 Введите сумму Stars для пополнения пользователя @{target_username}:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "add_money_amount")
def handle_add_money_amount(message):
    """Обработка суммы для добавления денег"""
    user_id = message.from_user.id
    admin_data = ADMIN_STATES[user_id]
    target_username = admin_data.get("target_username", "")
    
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!", reply_markup=admin_panel_menu())
            ADMIN_STATES[user_id]["step"] = "admin_panel"
            return
        
        target_user_id, target_user_data = get_user_by_username(target_username)
        
        if target_user_id:
            add_transaction(int(target_user_id), amount, "completed", "admin_add")
            
            add_admin_log(
                admin_name=admin_data.get('admin_name', 'Unknown'),
                action="add_money",
                target_username=target_username,
                amount=amount,
                notes=f"Пополнение баланса"
            )
            
            ADMIN_STATES[user_id]["step"] = "admin_panel"
            logger.info(f"Админ {admin_data.get('admin_name')} добавил {amount} Stars пользователю {target_username}")
            
            new_balance = get_user_data(int(target_user_id)).get("stars_balance", 0)
            bot.send_message(message.chat.id, 
                           f"✅ Успешно добавлено {amount} ⭐ пользователю @{target_username}\n"
                           f"💰 Новый баланс: {new_balance} ⭐",
                           reply_markup=admin_panel_menu())
            
            try:
                bot.send_message(int(target_user_id),
                               f"🎉 Администратор пополнил ваш баланс на {amount} ⭐!\n"
                               f"💰 Ваш баланс: {new_balance} ⭐")
            except:
                pass
        else:
            bot.send_message(message.chat.id, f"❌ Пользователь @{target_username} не найден!", 
                           reply_markup=admin_panel_menu())
            ADMIN_STATES[user_id]["step"] = "admin_panel"
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный формат суммы! Введите число.", 
                       reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"

@bot.message_handler(func=lambda message: message.text == '📉 Withdraw Money' and 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("authorized"))
def handle_withdraw_money(message):
    """Списать деньги у пользователя"""
    user_id = message.from_user.id
    ADMIN_STATES[user_id]["step"] = "withdraw_username"
    bot.send_message(message.chat.id, "👤 Введите username пользователя для списания:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "withdraw_username")
def handle_withdraw_username(message):
    """Обработка username для списания"""
    user_id = message.from_user.id
    target_username = message.text.strip().replace('@', '')
    
    if not target_username:
        bot.send_message(message.chat.id, "❌ Username не может быть пустым!", reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"
        return
    
    ADMIN_STATES[user_id]["step"] = "withdraw_amount"
    ADMIN_STATES[user_id]["target_username"] = target_username
    
    bot.send_message(message.chat.id, f"📉 Введите сумму Stars для списания у пользователя @{target_username}:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "withdraw_amount")
def handle_withdraw_amount(message):
    """Обработка суммы для списания"""
    user_id = message.from_user.id
    admin_data = ADMIN_STATES[user_id]
    target_username = admin_data.get("target_username", "")
    
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!", reply_markup=admin_panel_menu())
            ADMIN_STATES[user_id]["step"] = "admin_panel"
            return
        
        target_user_id, target_user_data = get_user_by_username(target_username)
        
        if target_user_id:
            target_user_data = get_user_data(int(target_user_id))
            current_balance = target_user_data.get("stars_balance", 0)
            
            if current_balance >= amount:
                add_transaction(int(target_user_id), -amount, "completed", "admin_withdraw")
                
                add_admin_log(
                    admin_name=admin_data.get('admin_name', 'Unknown'),
                    action="withdraw_money",
                    target_username=target_username,
                    amount=amount,
                    notes=f"Списание средств"
                )
                
                ADMIN_STATES[user_id]["step"] = "admin_panel"
                logger.info(f"Админ {admin_data.get('admin_name')} списал {amount} Stars у пользователя {target_username}")
                
                new_balance = get_user_data(int(target_user_id)).get("stars_balance", 0)
                bot.send_message(message.chat.id, 
                               f"✅ Успешно списано {amount} ⭐ у пользователя @{target_username}\n"
                               f"💰 Новый баланс: {new_balance} ⭐",
                               reply_markup=admin_panel_menu())
                
                try:
                    bot.send_message(int(target_user_id),
                                   f"⚠️ Администратор списал с вашего баланса {amount} ⭐\n"
                                   f"💰 Ваш баланс: {new_balance} ⭐")
                except:
                    pass
            else:
                bot.send_message(message.chat.id, 
                               f"❌ Недостаточно средств у пользователя!\n"
                               f"💰 Текущий баланс: {current_balance} ⭐\n"
                               f"📉 Запрошено: {amount} ⭐",
                               reply_markup=admin_panel_menu())
                ADMIN_STATES[user_id]["step"] = "admin_panel"
        else:
            bot.send_message(message.chat.id, f"❌ Пользователь @{target_username} не найден!", 
                           reply_markup=admin_panel_menu())
            ADMIN_STATES[user_id]["step"] = "admin_panel"
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный формат суммы! Введите число.", 
                       reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"

@bot.message_handler(func=lambda message: message.text == '📊 Users Stats' and 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("authorized"))
def handle_users_stats(message):
    """Статистика пользователей"""
    users_data = load_users_data()
    
    if not users_data:
        bot.send_message(message.chat.id, "📭 Нет зарегистрированных пользователей.", 
                       reply_markup=admin_panel_menu())
        return
    
    sorted_users = sorted(users_data.items(), 
                         key=lambda x: x[1].get("stars_balance", 0), 
                         reverse=True)
    
    stats_text = "📊 **Топ-10 пользователей по балансу:**\n\n"
    
    for i, (user_id, user_data) in enumerate(sorted_users[:10], 1):
        username = user_data.get("username", f"ID: {user_id}")
        balance = user_data.get("stars_balance", 0)
        total_spent = user_data.get("total_spent", 0)
        
        stats_text += f"{i}. **{username}**\n"
        stats_text += f"   ⭐ Баланс: {balance}\n"
        stats_text += f"   📈 Пополнено: {total_spent}\n"
        stats_text += f"   🆔 ID: {user_id}\n\n"
    
    stats_text += f"👥 Всего пользователей: {len(users_data)}"
    bot.send_message(message.chat.id, stats_text, reply_markup=admin_panel_menu())

@bot.message_handler(func=lambda message: message.text == '📝 Dupe IP' and 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("authorized"))
def handle_dupe_ip(message):
    """Просмотр операций пользователя"""
    user_id = message.from_user.id
    ADMIN_STATES[user_id]["step"] = "dupe_ip_username"
    bot.send_message(message.chat.id, "👤 Введите username пользователя для просмотра операций:")

@bot.message_handler(func=lambda message: 
                     message.from_user.id in ADMIN_STATES and 
                     ADMIN_STATES[message.from_user.id].get("step") == "dupe_ip_username")
def handle_dupe_ip_username(message):
    """Обработка username для просмотра операций"""
    user_id = message.from_user.id
    target_username = message.text.strip().replace('@', '')
    
    if not target_username:
        bot.send_message(message.chat.id, "❌ Username не может быть пустым!", 
                       reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"
        return
    
    target_user_id, target_user_data = get_user_by_username(target_username)
    
    if not target_user_id:
        bot.send_message(message.chat.id, f"❌ Пользователь @{target_username} не найден!", 
                       reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"
        return
    
    admin_logs = load_admin_logs()
    user_logs = [log for log in admin_logs if log.get("target_username", "").lower() == target_username.lower()]
    
    if not user_logs:
        bot.send_message(message.chat.id, 
                       f"📭 Для пользователя @{target_username} нет записей об операциях администраторов.",
                       reply_markup=admin_panel_menu())
        ADMIN_STATES[user_id]["step"] = "admin_panel"
        return
    
    report_text = f"""
📝 **Отчет по операциям администраторов**
👤 Пользователь: @{target_username}
📊 Всего операций: {len(user_logs)}

"""
    
    admin_stats = {}
    for log in user_logs:
        admin = log.get("admin", "Unknown")
        if admin not in admin_stats:
            admin_stats[admin] = {"add": 0, "withdraw": 0, "count": 0}
        
        action = log.get("action", "")
        amount = log.get("amount", 0)
        
        if action == "add_money":
            admin_stats[admin]["add"] += amount
        elif action == "withdraw_money":
            admin_stats[admin]["withdraw"] += amount
        
        admin_stats[admin]["count"] += 1
    
    for admin, stats in admin_stats.items():
        report_text += f"\n👑 **{admin}:**\n"
        report_text += f"   📈 Пополнений: +{stats['add']} ⭐\n"
        report_text += f"   📉 Списаний: -{stats['withdraw']} ⭐\n"
        report_text += f"   📊 Операций: {stats['count']}\n"
    
    report_text += f"\n---\n📋 **Последние операции:**\n\n"
    
    recent_logs = user_logs[-10:]
    for i, log in enumerate(reversed(recent_logs), 1):
        timestamp = datetime.fromisoformat(log.get("timestamp")).strftime("%d.%m.%Y %H:%M")
        admin = log.get("admin", "Unknown")
        action = log.get("action", "")
        amount = log.get("amount", 0)
        notes = log.get("notes", "")
        
        if action == "add_money":
            action_text = "Пополнение"
            symbol = "➕"
        elif action == "withdraw_money":
            action_text = "Списание"
            symbol = "➖"
        else:
            action_text = "Операция"
            symbol = "🔄"
        
        report_text += f"{i}. {timestamp}\n"
        report_text += f"   {symbol} {amount} ⭐ ({action_text})\n"
        report_text += f"   👑 Админ: {admin}\n"
        if notes:
            report_text += f"   📝 Примечание: {notes}\n"
        report_text += "\n"
    
    if len(user_logs) > 10:
        report_text += f"\n📈 Показано {len(recent_logs)} из {len(user_logs)} операций"
    
    user_balance = target_user_data.get("stars_balance", 0)
    total_spent = target_user_data.get("total_spent", 0)
    registration_date = datetime.fromisoformat(target_user_data.get("registration_date", datetime.now().isoformat())).strftime("%d.%m.%Y")
    
    report_text += f"\n---\n📊 **Общая информация:**\n"
    report_text += f"💰 Текущий баланс: {user_balance} ⭐\n"
    report_text += f"📈 Всего пополнено: {total_spent} ⭐\n"
    report_text += f"📅 Дата регистрации: {registration_date}\n"
    report_text += f"🆔 ID: {target_user_id}"
    
    ADMIN_STATES[user_id]["step"] = "admin_panel"
    
    try:
        bot.send_message(message.chat.id, report_text, reply_markup=admin_panel_menu())
    except:
        for i in range(0, len(report_text), 4000):
            bot.send_message(message.chat.id, report_text[i:i+4000], reply_markup=admin_panel_menu())

# ===== МАГАЗИН И ПОКУПКА КУКИ =====

@bot.message_handler(func=lambda message: message.text == '📦 Магазин')
def show_shop(message):
    """Показать магазин"""
    shop_text = """
🛒 **Магазин**

Выберите категорию:

• **🛒 Печеньки** - купить готовые печеньки
• **⭐ Пополнить Stars** - купить валюту для покупок

👇 Используйте кнопки ниже
    """
    bot.send_message(message.chat.id, shop_text, reply_markup=shop_menu())

@bot.message_handler(func=lambda message: message.text == '🛒 Печеньки')
def show_cookies_shop(message):
    """Показать меню с печеньками"""
    cookies_text = """
🍪 **Доступные печеньки:**

👇 Выберите тип печеньки:

"""
    
    for folder_key, display_name in COOKIE_FOLDERS.items():
        count = get_cookie_count(folder_key)
        price = COOKIE_PRICES.get(display_name, 0)
        
        if 'blox_fruits' in folder_key or 'mm2' in folder_key:
            emoji = "🎮"
        else:
            emoji = "🍪"
        
        cookies_text += f"• {emoji} {display_name}\n"
        if count == 0:
            cookies_text += f"    🔴 Нет в наличии\n\n"
        else:
            cookies_text += f"    💰 Цена: {price} ⭐\n"
            cookies_text += f"    📦 В наличии: {count} шт.\n\n"
    
    cookies_text += "👇 Нажмите на название печеньки для покупки"
    bot.send_message(message.chat.id, cookies_text, reply_markup=cookies_menu())

@bot.message_handler(func=lambda message: message.text in BUTTON_TO_FOLDER.keys())
def handle_cookie_selection(message):
    """Обработка выбора типа куки"""
    button_text = message.text
    user_id = message.from_user.id
    
    # Получаем ключ папки из словаря
    folder_key = BUTTON_TO_FOLDER.get(button_text)
    
    if not folder_key:
        bot.send_message(message.chat.id, "❌ Ошибка: тип печеньки не найден", reply_markup=cookies_menu())
        return
    
    # Получаем отображаемое имя
    cookie_display_name = COOKIE_FOLDERS.get(folder_key, button_text)
    
    # Проверяем наличие
    count = get_cookie_count(folder_key)
    price = COOKIE_PRICES.get(cookie_display_name, 0)
    
    if count == 0:
        bot.send_message(message.chat.id, 
                        f"❌ **{cookie_display_name}**\n\n🔴 Нет в наличии\n\nПопробуйте позже или выберите другой тип.",
                        reply_markup=cookies_menu())
        return
    
    # Проверяем баланс пользователя
    user_data = get_user_data(user_id)
    balance = user_data.get('stars_balance', 0)
    
    if balance < price:
        bot.send_message(message.chat.id,
                       f"❌ **Недостаточно средств!**\n\n"
                       f"Вы выбрали: **{cookie_display_name}**\n"
                       f"Цена: **{price} ⭐**\n"
                       f"Ваш баланс: **{balance} ⭐**\n\n"
                       f"Пополните баланс в профиле.",
                       reply_markup=cookies_menu())
        return
    
    # Сохраняем состояние покупки
    PURCHASE_STATES[user_id] = {
        "cookie_display_name": cookie_display_name,
        "cookie_folder_key": folder_key,
        "price": price,
        "step": "confirm"
    }
    
    # Запрашиваем подтверждение
    confirm_text = f"""
⚠️ **Подтверждение покупки**

Вы хотите купить: **{cookie_display_name}**
Цена: **{price} ⭐**

Ваш баланс: **{balance} ⭐**
Остаток после покупки: **{balance - price} ⭐**

Напишите **ДА** чтобы подтвердить покупку.
Напишите **НЕТ** чтобы отменить.
    """
    
    bot.send_message(message.chat.id, confirm_text)

@bot.message_handler(func=lambda message: message.text.upper() in ['ДА', 'НЕТ'])
def handle_purchase_confirmation(message):
    """Обработка подтверждения покупки"""
    user_id = message.from_user.id
    
    if user_id not in PURCHASE_STATES or PURCHASE_STATES[user_id].get("step") != "confirm":
        return
    
    user_response = message.text.upper()
    
    if user_response == 'ДА':
        cookie_display_name = PURCHASE_STATES[user_id]["cookie_display_name"]
        folder_key = PURCHASE_STATES[user_id]["cookie_folder_key"]
        price = PURCHASE_STATES[user_id]["price"]
        
        # Проверяем наличие еще раз
        count = get_cookie_count(folder_key)
        if count == 0:
            bot.send_message(message.chat.id, 
                           f"❌ **{cookie_display_name}**\n\n🔴 Товар закончился!\n\nПопробуйте другой тип.",
                           reply_markup=cookies_menu())
            if user_id in PURCHASE_STATES:
                del PURCHASE_STATES[user_id]
            return
        
        # Получаем случайный файл куки
        cookie_file_path = get_random_cookie_file(folder_key)
        if not cookie_file_path:
            bot.send_message(message.chat.id, 
                           "❌ Ошибка: не удалось получить файл печеньки",
                           reply_markup=cookies_menu())
            if user_id in PURCHASE_STATES:
                del PURCHASE_STATES[user_id]
            return
        
        try:
            # Списываем баланс
            user_data = get_user_data(user_id)
            user_data["stars_balance"] = user_data.get("stars_balance", 0) - price
            update_user_data(user_id, user_data)
            
            # Добавляем транзакцию
            add_transaction(user_id, -price, "completed", "cookie_purchase", cookie_display_name)
            
            # Добавляем в историю покупок
            if "cookies_purchased" not in user_data:
                user_data["cookies_purchased"] = []
            
            user_data["cookies_purchased"].append({
                "cookie_name": cookie_display_name,
                "price": price,
                "purchase_date": datetime.now().isoformat(),
                "file_name": os.path.basename(cookie_file_path)
            })
            
            update_user_data(user_id, user_data)
            
            # Отправляем сообщение об успешной покупке
            success_text = f"✅ **Покупка успешна!**\n\n🎁 Куки: {cookie_display_name}\n💰 Списано: {price} ⭐\n💰 Новый баланс: {user_data.get('stars_balance', 0)} ⭐"
            bot.send_message(message.chat.id, success_text, parse_mode='Markdown')
            
            # Отправляем txt файл как документ
            try:
                with open(cookie_file_path, 'rb') as file:
                    file_name = os.path.basename(cookie_file_path)
                    bot.send_document(
                        message.chat.id, 
                        file, 
                        caption=f"📁 Файл: {file_name}\n🍪 Тип: {cookie_display_name}",
                        visible_file_name=file_name
                    )
                logger.info(f"Файл отправлен: {cookie_file_path}")
            except Exception as e:
                logger.error(f"Ошибка отправки файла: {e}")
                # Если не удалось отправить файл, пробуем отправить содержимое как текст
                try:
                    with open(cookie_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    bot.send_message(message.chat.id, f"📦 **Содержимое файла:**\n\n{content[:3000]}")
                except:
                    bot.send_message(message.chat.id, "❌ Не удалось отправить файл.")
            
            # Удаляем файл
            if delete_cookie_file(cookie_file_path):
                logger.info(f"Файл куки удален: {cookie_file_path}")
            else:
                logger.warning(f"Не удалось удалить файл: {cookie_file_path}")
            
            logger.info(f"Пользователь {user_id} купил куки {cookie_display_name} за {price} Stars")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке покупки: {e}")
            bot.send_message(message.chat.id, 
                           f"❌ Ошибка при обработке покупки: {str(e)}\nПопробуйте еще раз или обратитесь в поддержку.",
                           reply_markup=cookies_menu())
        
        # Очищаем состояние
        if user_id in PURCHASE_STATES:
            del PURCHASE_STATES[user_id]
            
    elif user_response == 'НЕТ':
        bot.send_message(message.chat.id, "❌ Покупка отменена.", reply_markup=cookies_menu())
        
        # Очищаем состояние
        if user_id in PURCHASE_STATES:
            del PURCHASE_STATES[user_id]

# ===== ПРОФИЛЬ И БАЛАНС =====

@bot.message_handler(func=lambda message: message.text == '👤 Профиль')
def show_profile(message):
    """Показать профиль пользователя"""
    user = message.from_user
    user_data = get_user_data(user.id)
    
    username = user_data.get('username', user.username or user.first_name)
    stars_balance = user_data.get('stars_balance', 0)
    
    all_transactions = user_data.get('transactions', [])
    regular_transactions = [t for t in all_transactions if t.get('type') != 'test_stars']
    total_spent = sum(t['amount'] for t in regular_transactions if t.get('status') == 'completed' and t['amount'] > 0)
    total_transactions = len(regular_transactions)
    
    cookies_purchased = user_data.get('cookies_purchased', [])
    total_cookies = len(cookies_purchased)
    
    last_transaction = None
    if regular_transactions:
        last_trans = regular_transactions[-1]
        last_date = datetime.fromisoformat(last_trans['date']).strftime("%d.%m.%Y %H:%M")
        last_amount = last_trans['amount']
        last_type = "➕" if last_amount > 0 else "➖"
        last_transaction = f"{last_date} - {last_type} {abs(last_amount)} ⭐"
    
    profile_text = f"""
👤 **Профиль**

📛 Имя: {username}
🆔 ID: {user.id}
⭐ STARS: {stars_balance}
📊 Транзакций: {total_transactions}
🍪 Куплено куки: {total_cookies}
📈 Пополнено: {total_spent} Stars

"""
    
    if last_transaction:
        profile_text += f"📅 Последняя операция:\n{last_transaction}\n\n"
    
    profile_text += "💡 Используй кнопки ниже для управления профилем:"
    bot.send_message(message.chat.id, profile_text, reply_markup=profile_menu())

@bot.message_handler(func=lambda message: message.text == '📊 Мои транзакции')
def show_transactions(message):
    """Показать историю транзакций"""
    user_data = get_user_data(message.from_user.id)
    all_transactions = user_data.get('transactions', [])
    
    regular_transactions = [t for t in all_transactions if t.get('type') != 'test_stars']
    
    if not regular_transactions:
        bot.send_message(message.chat.id, "📭 У вас пока нет транзакций.")
        return
    
    recent_transactions = regular_transactions[-10:]
    trans_text = "📊 **История транзакций:**\n\n"
    
    for i, trans in enumerate(reversed(recent_transactions), 1):
        date = datetime.fromisoformat(trans['date']).strftime("%d.%m.%Y %H:%M")
        amount = trans['amount']
        trans_type = trans.get('type', 'unknown')
        cookie_name = trans.get('cookie_name')
        
        if amount > 0:
            prefix = "➕"
            operation = "Пополнение"
        elif amount < 0:
            prefix = "➖"
            if cookie_name:
                operation = f"Куки: {cookie_name}"
            elif trans_type == 'admin_withdraw':
                operation = "👑 Списание админа"
            else:
                operation = "Списание"
        else:
            prefix = "🟰"
            operation = "Операция"
        
        status = "✅" if trans.get('status') == "completed" else "⏳"
        
        if trans_type in ['admin_add', 'admin_withdraw']:
            operation = "👑 Админ" + ("+" if trans_type == 'admin_add' else "-")
        
        trans_text += f"{i}. {date}\n   {prefix} {abs(amount)} ⭐ ({operation}) {status}\n"
    
    if len(regular_transactions) > 10:
        trans_text += f"\n📈 Всего операций: {len(regular_transactions)}"
    
    bot.send_message(message.chat.id, trans_text)

@bot.message_handler(func=lambda message: message.text == '🍪 Мои куки')
def show_my_cookies(message):
    """Показать купленные куки"""
    user_data = get_user_data(message.from_user.id)
    cookies_purchased = user_data.get('cookies_purchased', [])
    
    if not cookies_purchased:
        bot.send_message(message.chat.id, "🍪 У вас пока нет купленных печенек.")
        return
    
    cookies_text = f"🍪 **Ваши куки (всего: {len(cookies_purchased)})**\n\n"
    
    cookie_stats = {}
    for cookie in cookies_purchased:
        name = cookie['cookie_name']
        if name not in cookie_stats:
            cookie_stats[name] = {"count": 0, "total_spent": 0}
        cookie_stats[name]["count"] += 1
        cookie_stats[name]["total_spent"] += cookie['price']
    
    for i, (name, stats) in enumerate(cookie_stats.items(), 1):
        if 'Blox' in name or 'MM2' in name:
            emoji = "🎮"
        else:
            emoji = "🍪"
        
        cookies_text += f"{i}. {emoji} **{name}**\n"
        cookies_text += f"   📦 Куплено: {stats['count']} раз\n"
        cookies_text += f"   💰 Потрачено: {stats['total_spent']} ⭐\n\n"
    
    cookies_text += "📅 **Последние покупки:**\n"
    recent_cookies = cookies_purchased[-10:]
    for i, cookie in enumerate(reversed(recent_cookies), 1):
        purchase_date = datetime.fromisoformat(cookie['purchase_date']).strftime("%d.%m.%Y %H:%M")
        
        if 'Blox' in cookie['cookie_name'] or 'MM2' in cookie['cookie_name']:
            emoji = "🎮"
        else:
            emoji = "🍪"
        
        cookies_text += f"{i}. {emoji} {cookie['cookie_name']} - {cookie['price']} ⭐ ({purchase_date})\n"
    
    bot.send_message(message.chat.id, cookies_text)

@bot.message_handler(func=lambda message: message.text == '⭐ Пополнить Stars')
def add_balance(message):
    """Показать меню пополнения баланса"""
    text = """
⭐ **Пополнение STARS**

На данный момент доступно пополнение только STARS ⭐

Выберите количество STARS для пополнения:
    """
    bot.send_message(message.chat.id, text, reply_markup=payment_amount_menu())

@bot.message_handler(func=lambda message: message.text in ['25 ⭐', '50 ⭐', '75 ⭐', '100 ⭐', '150 ⭐', '200 ⭐'])
def handle_payment_amount(message):
    """Обработка выбора суммы для пополнения"""
    amount_text = message.text
    amount = int(amount_text.split()[0])
    
    prices = [types.LabeledPrice(label="Пополнение Stars", amount=amount)]
    
    try:
        bot.send_invoice(
            chat_id=message.chat.id,
            title=f"Пополнение STARS на {amount}",
            description=f"Покупка {amount} Stars для использования в боте",
            invoice_payload=f"stars_{amount}_{message.from_user.id}",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter=f"stars_{amount}",
            photo_url="https://img.icons8.com/color/96/000000/star--v1.png",
            photo_width=96,
            photo_height=96,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False
        )
        
        logger.info(f"Создан счет на {amount} Stars для пользователя {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка создания счета: {e}")
        error_text = f"""
❌ **Ошибка при создании счета**

Не удалось создать счет на {amount} Stars.
Попробуйте еще раз или обратитесь в поддержку.
        """
        bot.send_message(message.chat.id, error_text, reply_markup=profile_menu())

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_query(pre_checkout_q):
    """Обработка предварительной проверки платежа"""
    try:
        if pre_checkout_q.invoice_payload.startswith('stars_'):
            bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
            logger.info(f"Pre-checkout подтвержден: {pre_checkout_q.invoice_payload}")
        else:
            bot.answer_pre_checkout_query(pre_checkout_q.id, ok=False, 
                                         error_message="Неверный идентификатор платежа")
    except Exception as e:
        logger.error(f"Ошибка pre-checkout: {e}")
        bot.answer_pre_checkout_query(pre_checkout_q.id, ok=False, 
                                     error_message="Ошибка обработки платежа")

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    """Обработка успешного платежа"""
    payment = message.successful_payment
    
    payload_parts = payment.invoice_payload.split('_')
    if len(payload_parts) >= 3:
        amount = int(payload_parts[1])
        user_id = int(payload_parts[2])
        
        add_transaction(user_id, amount, status="completed", transaction_type="stars_purchase")
        
        user_data = get_user_data(user_id)
        new_balance = user_data.get('stars_balance', 0)
        
        success_text = f"""
🎉 **Оплата успешна!** 🎉

✅ Вы успешно пополнили баланс на {amount} ⭐
💰 Теперь ваш баланс Stars: {new_balance} ⭐

Спасибо за покупку! Теперь вы можете использовать Stars для получения печенек.
        """
        
        bot.send_message(message.chat.id, success_text, reply_markup=profile_menu())
        logger.info(f"Успешный платеж: пользователь {user_id} купил {amount} Stars")
        
    else:
        logger.error(f"Неверный формат payload: {payment.invoice_payload}")
        bot.send_message(message.chat.id, "Платеж получен, но произошла ошибка обработки. Обратитесь в поддержку.")

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====

@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def back_to_main(message):
    """Возврат в главное меню"""
    user_id = message.from_user.id
    
    if user_id in PURCHASE_STATES:
        del PURCHASE_STATES[user_id]
    
    if user_id in ADMIN_STATES and ADMIN_STATES[user_id].get("step") in ["admin_panel", "add_money_username", 
                                                                       "add_money_amount", "withdraw_username", 
                                                                       "withdraw_amount", "dupe_ip_username"]:
        if ADMIN_STATES[user_id].get("authorized"):
            ADMIN_STATES[user_id] = {
                "authorized": True,
                "admin_name": ADMIN_STATES[user_id].get("admin_name", "Admin"),
                "step": "admin_panel"
            }
    
    bot.send_message(message.chat.id, "🔙 Возвращаемся в главное меню", reply_markup=main_menu(user_id))

@bot.message_handler(func=lambda message: message.text == '📄 Информация')
def show_info(message):
    """Показать информацию"""
    info_text = """
📄 **Информация**

🔒 Политика конфиденциальности - https://telegra.ph/Politika-konfidencialnosti-08-15-17

📝 Пользовательское соглашение - https://telegra.ph/Polzovatelskoe-soglashenie-08-15-10
    """
    bot.send_message(message.chat.id, info_text)

@bot.message_handler(func=lambda message: message.text == '🆘 Помощь')
def support_help(message):
    """Показать помощь"""
    help_text = """
🆘 **Если у вас появился вопрос или проблема пишите сюда:**

👨‍💼 Модератор № 1: @Durov02020
👨‍💼 Модератор № 2: @mozt_1

📞 Мы всегда готовы помочь вам!
    """
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: message.text == '📋 Команды')
def send_help(message):
    """Показать команды"""
    help_text = """
📋 **Доступные команды и функции:**

• **🍪 Печеньки** - купить cookies
• **👤 Профиль** - информация о пользователе
• **🆘 Помощь** - связаться с модераторами
• **📋 Команды** - список команд бота
• **ℹ️ Инфо** - информация о боте
• **📄 Информация** - правовые документы
• **🧪 Тест** - проверить работу бота
• **📞 Контакты** - связаться с создателем
• **⭐ Пополнить Stars** - купить Stars для использования в боте
• **📊 Мои транзакции** - история пополнений

    """
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация о боте')
def send_info(message):
    """Показать информацию о боте"""
    info_text = """
🤖 **MonickCookies Bot**
Версия: 3.1
Создатель: Mower123
Описание: Бот с печеньками и системой платежей через Telegram Stars
Статус: 🟢 Активен

🎮 **Новые типы куки:**
• Blox Fruits [3 Sea] - 45 ⭐
• MM2 [100 LVL] - 35 ⭐

Настроен на Python + pyTelegramBotAPI
Поддерживает платежи через Telegram Stars
    """
    bot.send_message(message.chat.id, info_text)

@bot.message_handler(func=lambda message: message.text == '🧪 Тест')
def test_bot(message):
    """Тест работы бота"""
    user_data = get_user_data(message.from_user.id)
    
    test_text = f"""
✅ **Тест пройден! Бот работает отлично!** 🚀

📊 Статистика:
• Ваш баланс Stars: {user_data.get('stars_balance', 0)}
• Система платежей: 🟢 Активна
• Новые куки: 🎮 Blox Fruits и MM2 доступны!

💡 Для пополнения баланса нажмите "⭐ Пополнить Stars"
    """
    bot.send_message(message.chat.id, test_text)

@bot.message_handler(func=lambda message: message.text == '📞 Контакты')
def contacts(message):
    """Показать контакты"""
    contact_text = """
📞 **Контакты:**
Создатель: @Sigma813
Бот: @MonickCookiesBot

По вопросам сотрудничества: 
✉️ Напиши в Telegram @sigma813
    """
    bot.send_message(message.chat.id, contact_text)

# ===== ИНЛАЙН КНОПКИ =====

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    """Обработка инлайн кнопок"""
    if call.data == 'cookies':
        user_data = get_user_data(call.from_user.id)
        stars_balance = user_data.get('stars_balance', 0)
        
        if stars_balance >= 1:
            add_transaction(call.from_user.id, -1, "completed", "cookies_purchase")
            bot.answer_callback_query(call.id, "Вот твои печеньки! 🍪 (списано 1 ⭐)")
            bot.send_message(call.message.chat.id, "🍪🍪🍪 Печеньки через инлайн кнопку! 🍪🍪🍪")
        else:
            bot.answer_callback_query(call.id, "❌ Недостаточно Stars! Пополните баланс.", show_alert=True)
    
    elif call.data == 'commands':
        bot.answer_callback_query(call.id, "Список команд")
        send_help(call.message)
    
    elif call.data == 'about':
        bot.answer_callback_query(call.id, "Информация о боте")
        send_info(call.message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Обработка всех остальных сообщений"""
    user_id = message.from_user.id
    
    if user_id in ADMIN_STATES and ADMIN_STATES[user_id].get("step") in ["select_admin", "enter_password", 
                                                                       "add_money_username", "add_money_amount",
                                                                       "withdraw_username", "withdraw_amount",
                                                                       "dupe_ip_username"]:
        return
    
    bot.send_message(message.chat.id, "🤖 Используй кнопки для навигации!", reply_markup=main_menu(user_id))

# ===== ЗАПУСК БОТА =====

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот MonickCookies запускается...")
    print("=" * 50)
    
    create_cookie_folders()
    
    print("🍪 Структура папок создана:")
    for folder_key, display_name in COOKIE_FOLDERS.items():
        count = get_cookie_count(folder_key)
        price = COOKIE_PRICES.get(display_name, 0)
        
        if 'blox_fruits' in folder_key or 'mm2' in folder_key:
            emoji = "🎮"
        else:
            emoji = "📁"
            
        print(f"   {emoji} Cookies/{folder_key}/ -> {display_name}")
        print(f"       💰 Цена: {price} ⭐")
        print(f"       📦 В наличии: {count} шт.")
    
    print("\n💰 Цены на куки:")
    for cookie, price in COOKIE_PRICES.items():
        if 'Blox' in cookie or 'MM2' in cookie:
            emoji = "🎮"
        else:
            emoji = "🍪"
        print(f"   {emoji} {cookie}: {price} ⭐")
    
    print("\n🔒 Скрытые команды:")
    print("   - /teststars - тестовая покупка 1 Star")
    print("   - /admin - секретная админ-панель")
    
    print("\n👑 Админы:")
    for admin in ADMIN_PASSWORDS.keys():
        print(f"   - {admin}")
    
    print("\n📊 Данные сохраняются в файлах:")
    print(f"   - {USERS_FILE} - данные пользователей")
    print(f"   - {ADMIN_LOG_FILE} - логи админов")
    
    print("\n🍪 Файлы куки удаляются автоматически после отправки")
    print("=" * 50)
    print("✅ Бот запущен и готов к работе!")
    print("=" * 50)
    
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")