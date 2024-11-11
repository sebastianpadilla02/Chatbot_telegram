import telebot
from sympy import *
import json
from telebot import types

#token del bot
bot = telebot.TeleBot("8072127932:AAFDYSiwbe6whTvcREdsTYbN_A6JNVRzztM")
tipo_de_emergencia = 0
categoria = ""
subcategoria = ""

# Manejador del comando "/start"
@bot.message_handler(commands=["start"])
def start(message):
    global categoria
    global subcategoria
    categoria = ""
    subcategoria = ""
    bot.send_message(message.chat.id, "¡Hola! Soy tu bot de asistencia en emergencias relacionadas con inseguridad. Estoy aquí para ayudarte a actuar rápidamente en situaciones críticas. Usa /commands para ver lo que puedo hacer. Si es urgente, escribe directamente \"ayuda\" o usa el comando /emergencia.")
    enviar_foto(message.chat.id, "media/num_policia.png", "En caso de una llamada al cuadrante mas cercano vea /contactos para mas información")
    comandos(message)

# Manejador del comando "/help"
@bot.message_handler(commands=["help"])
def ayuda(message):
    ayuda = ""
    with open("help.txt", "r", encoding="utf-8") as f:
        for line in f:
            ayuda += line
    bot.reply_to(message, ayuda, parse_mode="Markdown")

# Manejador del comando "/commands"
@bot.message_handler(commands=["commands"])
def comandos(message):
    commands_list = ""
    with open("comandos.txt", "r", encoding="utf-8") as f:
        for line in f:
            commands_list += line
    bot.reply_to(message, commands_list)

# Manejador del comando "/emergencia"
@bot.message_handler(commands=["emergencia"])
def emergencia(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Cargar el JSON desde un archivo
    with open("recommendations_structured.json", "r", encoding="utf-8") as file:
        emergencies = json.load(file)

    btn = []
    cont = 0
    for key in emergencies.keys():
        cont += 1
        btn.append(types.InlineKeyboardButton(key, callback_data=f'emergencia_{cont}'))

    markup.add(*btn)

    response = "Por favor, elige la categoría de emergencia que presentas:"
    bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('emergencia_'))
def emergencia_seleccionada(call):
    global categoria
    tipo_de_emergencia = int(call.data.split('_')[1])

    with open("recommendations_structured.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    markup = types.InlineKeyboardMarkup(row_width=1)

    keys = list(data.keys())
    chosen_category = keys[tipo_de_emergencia - 1]
    categoria = chosen_category
    cont2 =0
    btns = []
    if chosen_category in data:
        # Obtener las claves internas (subcategorías)
        for key in data[chosen_category].keys():
            cont2 += 1
            btns.append(types.InlineKeyboardButton(key, callback_data=f'subcategoría_{cont2}'))
    
    markup.add(*btns)

    response = "Por favor, elige el tipo emergencia que presentas:"
    bot.send_message(call.message.chat.id, response, reply_markup=markup)

    # bot.send_message(call.message.chat.id, f"🛡️ **Emergencia seleccionada:** 🛡️\n{call.data.split('_')[1]} \nIngresa tu ubicación para poder ayudarte. 📍")
    #bot.register_next_step_handler(call.message, ubicacion)

@bot.callback_query_handler(func=lambda call: call.data.startswith('subcategoría_'))
def subcategoria_seleccionada(call):
    global categoria
    global subcategoria
    with open("recommendations_structured.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    subcategorias = list(data[categoria].keys())
    chosen_subcategory = subcategorias[int(call.data.split('_')[1]) - 1]
    subcategoria = chosen_subcategory

    ubicacion(call.message)
    #bot.send_message(call.message.chat.id, response)

# Manejador del comando "/contactos"
@bot.message_handler(commands=["contactos"])
def contactos(message):
    contacts_list = ""
    with open("contactos.txt", "r", encoding="utf-8") as f:
        for line in f:
            contacts_list += line
    bot.reply_to(message, contacts_list)

# Manejador del comando "/red de apoyo"
@bot.message_handler(commands=["red_de_apoyo"])
def red_de_apoyo(message):
    apoyo_list = ""
    with open("apoyo.txt", "r", encoding="utf-8") as f:
        for line in f:
            apoyo_list += line
    bot.reply_to(message, apoyo_list)

# Manejador del comando "/recomendaciones"
@bot.message_handler(commands=["recomendaciones"])
def recomendaciones(message):
    global categoria
    with open("recommendations_structured.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if(categoria == ""):
        response = "🛡️ **Guía General de Emergencias** 🛡️\n\n"

        for category, emergencies in data.items():
            response += f"🔷 *{category}*\n"
            for subcategory, recommendation in emergencies.items():
                response += f"  🔹 *{subcategory}:* {recommendation[0]}\n"
            response += "\n"
        
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    else:
        recomendaciones_2(message)

    bot.send_message(message.chat.id, "¿Necesitas algo más? Ingrese /commands para ver los comandos disponibles, o /start.")

def ubicacion(message):
    bot.send_message(message.chat.id, "Gracias por tu ubicación. 📍\n¿Podrías proporcionar más detalles sobre la emergencia?")
    bot.register_next_step_handler(message, detalles)

def detalles(message):
    bot.send_message(message.chat.id, "Gracias por la información. 📝\nUn agente de seguridad se dirigirá a tu ubicación lo más pronto posible. 🚓\nPor favor, mantente seguro y en un lugar visible")
    recomendaciones(message)

def recomendaciones_2(message):
    global categoria
    global subcategoria
    with open("recommendations_structured.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    response = "🛡️ *Recomendaciones* 🛡️\n\n"
    value = data[categoria][subcategoria]

    for a in value:
        response += a + "\n"

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

#Funcion para enviar fotos con un mensaje
def enviar_foto(id, src_pic, capt):
    photo = open(src_pic, 'rb')
    bot.send_photo(id, photo, caption=capt)
    photo.close()

@bot.message_handler(func=lambda message:True)
#A todo mensaje distinto de los comandos y no esperado se responde con los comandos
def mensaje(message):
    emergencia(message)

bot.polling()