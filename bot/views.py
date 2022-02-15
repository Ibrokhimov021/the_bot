import logging
from turtle import back
from pkg_resources import safe_version
import telegram
from telegram import Update, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from .models import Application
from .service import get_facultet
import html2text
from .models import About, Facultet, Super
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

btn = [
    InlineKeyboardButton('📝Ariza qoldirish', callback_data='patition')
]
button=[
        ['📝Ariza qoldirish'],
        [
            '🏢Universitet haqida',
            'Fakultetlar'
        ],
        [
            '💵Superkontrakt',
            '☎️ Biz bilan aloqa'
        ]
    ]



def start(update,context):
    update.message.from_user
    user = update.message.from_user
    context.bot.delete_message(chat_id = user.id,message_id=update.message.message_id-1)
    context.bot.send_message(user.id, 'Assalomu alaykum\nProfi University rasmiy botiga xush kelibsiz😊',
                              reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))

    return 1

def ariza(update, context):
    
    state = context.user_data.get('state',0)
    user = update.message.from_user
    text = update.message.text
    if text == "🏢Universitet haqida":
        university(update,context)
    elif text == "Fakultetlar":
        fakultet(update, context)
    elif text == "☎️ Biz bilan aloqa":
        communication(update, context)
    elif text == "💵Superkontrakt":
        kontrakt(update, context)
    elif text == "📝Ariza qoldirish":
        context.user_data['state']=100
        context.bot.send_message(user.id, "Ro'yxatdan o'tish uchun ariza qoldiring.", None)
       
        context.bot.send_message(user.id, 'Ism familiya:',None)
    elif state ==100:
        context.user_data["firsname"]=text
        context.user_data['state']=101
        context.bot.send_message(user.id,'Fakultet nomi:',None)
    
    elif state == 101:
        context.user_data['yonalish']=text
        context.user_data['state']=102
        btn = [[KeyboardButton(request_contact=True,text='contact')]]
        context.bot.send_message(user.id,'Telefon raqam:', reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True,one_time_keyboard=True))
        
    elif state == 102:
        context.user_data['contact']=text
        context.user_data['state']=103
        btn = [
            ["HA","YO'Q"]
            
        ]
    
        ism ="Ism familiya: " + f"{context.user_data['firsname']}\n"
        yonalish = "Fakultet: "+f"{context.user_data['yonalish']}\n"
        number = "Telefon raqam: "+f"{context.user_data['contact']}\n\n"
        
        text = "Kiritilgan ma'lumotlar to'g'riligini tekshiring va tasdiqlash uchun HA tugmasini bosing\n \n"
        text+=ism+yonalish+number
        context.bot.send_message(user.id,text,reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True,one_time_keyboard=True))
       
    elif state == 103 and text=='HA':
        context.user_data['state']=None
        information=Application()
        information.fullname=context.user_data["firsname"]
        information.facility=context.user_data["yonalish"]
        information.phone_number=context.user_data["contact"]
        information.save()
        context.bot.send_message(user.id,'Malumotlaringiz saqlandi', reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
        
    elif text == "YO'Q" and state ==103:
        context.bot.delete_message(chat_id = user.id,message_id=update.message.message_id-1)
        context.bot.delete_message(chat_id = user.id,message_id=update.message.message_id)
        context.bot.send_message(user.id, "Ma'lumotlaringiz saqlanmadi", reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
        
    else:
        start(update, context)




def contact(update, context):
    user = update.message.from_user
    context.user_data['contact']=update.message.contact['phone_number']
    context.user_data['state']=103
    btn = [
        ["HA","YO'Q"]

        ]
    ism ="Ism-familiyangiz: " + f"{context.user_data['firsname']}\n"
    yonalish = "Fakultet: "+f"{context.user_data['yonalish']}\n"
    number = "Telefon raqam: "+f"{context.user_data['contact']}\n\n"
    text = "Kiritilgan ma'lumotlar to'g'riligini tekshiring va tasdiqlash uchun HA tugmasini bosing\n \n"
    text+=ism+yonalish+number
    context.bot.send_message(user.id,text,reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True,one_time_keyboard=True))

        

def callback_query(update, context):
    query = update.callback_query
    data = query.data
    son = data.split('_')
    user = update.callback_query.message.chat  
    fakultet = get_facultet()
    btn = [[InlineKeyboardButton('⬅️Ortga', callback_data='back_0')]]
    
    if son[0] == 'petintion':
        context.user_data['state']=100
        query.message.delete()
        context.bot.send_message( user.id,"Ro'yxatdan o'tish uchun ariza qoldiring.", None)
        context.bot.send_message( user.id,'Ism familiya:',None)
    elif son[0] == 'fakultet':    
        for i in fakultet:
            if i['id']==int(son[1]):
                info = html2text.html2text(i['about'])
                query.message.delete()
                context.bot.send_message(user.id, info,reply_markup=InlineKeyboardMarkup(btn))
    elif son[0] == 'back': 
        if int(son[1])==0:
            fakultet = get_facultet()
            btn = []
            btn_1 = [[InlineKeyboardButton("Batafsil", url='https://profiuniversity.uz/')],
                    ]
            for i in fakultet:
                btn.append(InlineKeyboardButton(f"{i['name']}",callback_data=f"fakultet_{i['id']}"))
                if len(btn)==2:
                    btn_1.append(btn)
                    btn = []
            if  btn:
                btn_1.append(btn)
            btn_1.append([InlineKeyboardButton('📝Ariza qoldirish', callback_data='petintion_0')])
                
        
            query.message.delete()
            context.bot.send_message(user.id,"Fakultetlar haqida ma'lumot",
                                reply_markup = InlineKeyboardMarkup(btn_1, resize_keyboard=True,one_time_keyboard=True))
            context.bot.send_message(user.id, None, reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
        elif int(son[1])==1:
            query.message.delete()
            context.bot.send_message(user.id, None,reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
    else:
        query.message.delete()
        context.bot.send_message(user.id, None, reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
def university(update, context):
    user = update.message.from_user
    obj = About.objects.all().first()
    info = obj.about
    res = html2text.html2text(info)
    
    btn = [ 
        [InlineKeyboardButton("Batafsil", url='https://profiuniversity.uz/')],
        [InlineKeyboardButton('📝Ariza qoldirish', callback_data='petintion_1')]
        ]

    context.bot.send_message(user.id, res,
                            reply_markup = InlineKeyboardMarkup(btn, resize_keyboard=True,one_time_keyboard=True))
    context.bot.send_message(user.id, None, reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
   
def fakultet(update, context):
    user = update.message.from_user
    fakultet = get_facultet()
    print(fakultet)
    btn = []
    btn_1 = [[InlineKeyboardButton("Batafsil", url='https://profiuniversity.uz/')],
            ]
    for i in fakultet:
        btn.append(InlineKeyboardButton(f"{i['name']}",callback_data=f"fakultet_{i['id']}"))
        if len(btn)==2:
            btn_1.append(btn)
            btn = []
    if  btn:
        btn_1.append(btn)
    btn_1.append([InlineKeyboardButton('📝Ariza qoldirish', callback_data='petintion_0')])
            
    # try:
    context.bot.send_message(user.id,"Fakultetlar haqida ma'lumot",
                            reply_markup = InlineKeyboardMarkup(btn_1, resize_keyboard=True,one_time_keyboard=True))
    context.bot.send_message(user.id, None, reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
    # except Exception as e:
    #     print('error>>>>>>', e)
def communication(update, context):
    user = update.message.from_user
    context.bot.send_message(user.id,"<b>Biz bilan aloqa:</b>\n \n📞+998 78 777 11 11\n📩info@proifuniversity.uz\n\n<i>Bizni ijtimoiy tarmoqlarda kuzatib boring:</i>\n \n<a href='https://www.instagram.com/profiuniversity/'>Instagram</a>|<a href='https://www.facebook.com/profiuniversity/'>Facebook</a>|<a href='https://t.me/profiuniversity'>Telagram</a>" ,
                             reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True) ,parse_mode='HTML')
#  <-- Bizni ijtimoiy tarmoqlarda kuzatib boring\n \n &&&<a href='https://t.me/profiuniversity'>Telagram</a>|<a href='https://www.instagram.com/profiuniversity/'>Instagram</a>|<a href='https://www.facebook.com/profiuniversity/'>Facebook</a> -- >
    
def kontrakt(update,context):
    super = Super.objects.all().first()
    text ='Super Kontrakt: '
    text += f"{super['price']}"
    user = update.message.from_user
    context.bot.delete_message(chat_id = user.id,message_id=update.message.message_id-1)
    context.bot.delete_message(chat_id = user.id,message_id=update.message.message_id)
    context.bot.send_message(user.id, text,reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True,one_time_keyboard=True))
