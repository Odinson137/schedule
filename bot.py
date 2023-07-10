from imports import *

from slovars import cleaner, ready_message, homeworks, items, new_users, all_users, name_file, real_new_file, allCurs

from background_bot import Files

from dop_aio import Cycles

# from aiogram.client.session.aiohttp import AiohttpSession
# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=API_TOKEN)
# proxy_url = 'http://proxy.server:3128'
# session = AiohttpSession(proxy=('http://proxy.server:3128'))

# # bot = Bot(token=API_TOKEN, session=session)
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=API_TOKEN)

# bot = Bot(token=API_TOKEN, proxy='http://proxy.server:3128')

# Диспетчер
dp = Dispatcher(bot)

# указываем ключ из личного кабинета openai
messages = []

v = 0

async def ask(id):
    await bot.send_message(id, "Chat думает...")
    try:
        message=text_message[0]
        completion = openai.Completion.create(engine="text-davinci-003", prompt=message, temperature=0.5, max_tokens=1000)
        await bot.send_message(id, completion.choices[0]['text'])
    except:
        print('fail')
        messages.clear()
        await bot.send_message(id, 'fail')

async def CHAT_GPT(id):
    await bot.send_message(id, "Chat думает...")
    try:
        message=text_message[0]
        
        messages.append({"role": "user", "content": message})
        
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
        reply = chat.choices[0].message.content
        await bot.send_message(id, reply)
        messages.append({"role":"assistant", "content": reply})
    except:
        print('fail')
        messages.clear()
        await bot.send_message(id, 'fail')

async def hello(message):
    button_hi = KeyboardButton('Привет! 👋')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button_hi)
    # await message.reply('Привет!')
    await message.reply("Привет!", reply_markup=greet_kb)

async def full_hello(message):
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    text = "Выберите ваш курс из списка: "
    
    # select = " SELECT title_curs, name_curs FROM curs"
    # cur.execute(select)
    # x = cur.fetchall()
    
    for group in allCurs.keys():
 
            # await bot.send_message(message.from_user.id, f"{type}:", reply_markup=keyboard)
            # keyboard = InlineKeyboardMarkup(row_width=2)
        kb = InlineKeyboardButton(text=group, callback_data=group)
    
        keyboard.add(kb)
       
    kb = InlineKeyboardButton(text='отмена', callback_data='отмена')
    keyboard.add(kb)      
        
    # text = "Для получения информации введите команду /schedule или нажмите на нижнюю кнопку. Приятного пользования!"
    await bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    
def reading_users():
    with open('users.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        for i in text['users']:
            all_users.update({int(i[0]): [i[1], i[2]]})

users = []
"""Обработчик всех сообщений!!!"""
# @dp.message(F.animation)
@dp.message_handler(content_types= ["text", "photo", "video", "document", "audio", "invoice", "voice"])
# @dp.message(F.text)
async def filters(message):
    print('sfds')
    
    if (len(all_users)) < 5:
        reading_users()
        
    text = message.text
    id = message.from_user.id

    print(id)
    if id in all_users.keys():
        print('Eсть')
    else:
        if id in new_users.keys():
            pass
        else:
            print("Нету")
            await full_hello(message)
            new_users.update({id: 1})
            return
        
    if id in users:
        pass
    else:
        if text ==  "Остановите бота":
            import os
            os._exit(0)
        
        users.append(id)
        
        if text == "/start" and id not in admins:
            await hello(message)
            
            await full_hello(message)
        
        elif text in ["/schedule", "Привет! 👋"]  and id not in admins:
            print('sdg')
            await hello(message)
            print('sdg')
            
            value = Files().after_download()
            
            curs = all_users[id][0]
            await new_schedule(user_id=id, value=value, curs=curs)
        
        elif text == '/homeworks'  and id not in admins:
            await all_homeworks(message)
        
        elif text == '/send_pdf'  and id not in admins:
            await get_file(message)
        
        elif text == '/all_days'  and id not in admins:
            # pass
            curs = all_users[id][0]
            # await days_from_base(message, curs)
            
        elif text == '/clear'  and id not in admins:
            cleaner()

        elif text == '/delet_user' and id not in admins:
            with open('users.json', 'r', encoding='utf-8') as f: 
                text = json.load(f)
                new_text = []
                with open('users.json', 'w', encoding='utf-8') as f:
                    for i in text['users']:
                        if (i[0] != id):
                            new_text.append(i)
                    # text['users'] += [[id, new_users[id], p[0].title()]]
                    json.dump({'users': new_text}, f, indent = 6, ensure_ascii=False)
                    
            await bot.send_message(id, f"Удалено!")
            del all_users[id]
            
        elif id in new_users.keys() and id not in admins:
            if new_users[id] != 1:
                p = text.split(' ')

                with open('users.json', 'r', encoding='utf-8') as f: 
                    text = json.load(f)
                    with open('users.json', 'w', encoding='utf-8') as f: 
                        text['users'] += [[id, new_users[id], p[0].title()]]
                        json.dump({'users': text['users']}, f, indent = 6, ensure_ascii=False)
                        
                await bot.send_message(id, f"{p[1].title()}, вы добавлены в дневник!")
                await bot.send_message(id, "/schedule")
                                
                all_users.update({id: [new_users[id], p[0].title()]})
                del new_users[id]
                
                all_users.clear()
                reading_users()
        
        else:
            keyboard = InlineKeyboardMarkup(row_width=2)
            curs = all_users[id][0]
            
            if id in admins:
                admins[id].clear()
                
                kb = InlineKeyboardButton(text='учащимся из группы!', callback_data='человеку из группы!')
                keyboard.add(kb)
                  
                kb = InlineKeyboardButton(text='определённым группам!', callback_data='определённым группам!')
                keyboard.add(kb)
                
                kb = InlineKeyboardButton(text='всем группам!', callback_data='всем группам!')
                keyboard.add(kb)
                
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена!')
                keyboard.add(kb)     
                
                await bot.send_message(id, 'Кому отправить сообщение: ', reply_markup=keyboard)
                admins[id].append(text)

            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                for item in get_items(curs):
                    
                    new_item = item
                    
                    if new_item:
                        items[curs].update({new_item: [text, message.message_id]})
                        kb = InlineKeyboardButton(text=new_item, callback_data=new_item)
                        keyboard.add(kb)
        
                text_message[0] = text
                kb = InlineKeyboardButton(text="Chat AI", callback_data="ChatGPT")
                keyboard.add(kb)
                
                kb = InlineKeyboardButton(text="Request AI", callback_data="RequestGPT")
                keyboard.add(kb)
        
                id_message = await bot.send_message(id, 'Выберите предмет: ', reply_markup=keyboard)
                delete_message.append(id_message)
                    
        users.remove(id)

def reading():
    with open('homeworks.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        for k, i in text['users'].items():
            items[k].update({i[0]: [i[1], i[2], i[3]]})

spammer = []
people_for_admin = {}

def dop_on_home(curs, item, text_mas):
    with open('homeworks.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        with open('homeworks.json', 'w', encoding='utf-8') as f: 
            text['users'][curs][item] = text_mas
            json.dump(text, f, indent = 6, ensure_ascii=False)

"""Обработчик нажатий кнопок!!!"""
# @dp.callback_query()
@dp.callback_query_handler()
async def filters_for_button_click(message):
        data = message.data
        id = message.from_user.id
        
        spammer.append(id)
        
        if id in all_users and id not in admins:
            curs = all_users[message.from_user.id][0]
            if data == "ChatGPT":
                await delete_message[-1].delete()
                await CHAT_GPT(id)
                
            elif data == "RequestGPT":
                await delete_message[-1].delete()
                await ask(id)
                
            elif data in homeworks:
                full_homework = homeworks[data]
                await bot.send_message(message.from_user.id, full_homework[0])
                if len(full_homework) > 1:
                    await bot.forward_message(chat_id=message.from_user.id, from_chat_id=full_homework[1][1],  message_id=full_homework[1][0])

            elif data in items[curs]:
                if items[curs][data][0]: 
                    await bot.send_message(message.from_user.id, f"Задание '{items[curs][data][0]}' по предмету '{data.title()}' добавлено в дневник")
                    if message.from_user.id != admin_id:
                        await bot.send_message(message.message.chat.id, f"Спасибо, {message.from_user.first_name}, что добавили домашку.")
                        await bot.send_message(admin_id, f"Мой Король, пользователь {message.from_user.first_name} осмелился отправить домашнее задание по предмету '{data.title()}':")
                        await bot.send_message(admin_id, items[curs][data][0])
                        

                    dop_on_home(curs, data, [items[curs][data][0], None, None])
                    if len(spammer) > 1:
                        pass
                    else:
                        
                       cleaner()
                    
                else:
                        await bot.forward_message(chat_id=admin_id, from_chat_id=message.from_user.id,  message_id=items[curs][data][1])
                        await bot.send_message(message.from_user.id, f"Фотография по предмету'{data.title()}' добавлено в дневник")
                        await bot.send_message(message.message.chat.id, f"Спасибо, {message.from_user.first_name})")
                        await bot.send_message(admin_id, f"Мой Король, пользователь {message.from_user.first_name} осмелился отправить фотку для предмета '{data.title()}'!")
                        
                        # await bot.send_message(admin_id, f"Мой Король, фото для предмета '{message.data.title()}' добавлено в дневник")
                        
                        dop_on_home(curs, data, ['Файл (нажмите чтоб просмотреть)', items[curs][data][1], id])
                        
                        if len(spammer) > 1:
                            pass
                        else:
                            cleaner()
                    
        elif id in admins and len(admins[id]) != 0:
            
            keyboard = InlineKeyboardMarkup(row_width=2)
            
            if data == 'отмена!':
                admins[id].clear()
                await bot.send_message(id, 'Отменено')
                people_for_admin.clear()
                
            elif data == 'человеку из группы!':
                for i in allCurs.keys():
                    kb = InlineKeyboardButton(text=i, callback_data='men' + i)
                    keyboard.add(kb)
                
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена!')
                keyboard.add(kb)    
                
                await bot.send_message(id, 'Выберите курс: ', reply_markup=keyboard)
                
            elif data[3:] in allCurs.keys():
                keyboard = InlineKeyboardMarkup(row_width=2)
                
                
                for i in allCurs[data[3:]]:
                    kb = InlineKeyboardButton(text=i, callback_data="men" + i)
                    keyboard.add(kb)
                    
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена')
                keyboard.add(kb)
                    
                await bot.send_message(id, "Выберите группу из списка: ", reply_markup=keyboard)
            
            elif 'men' in data:

                for k, v in all_users.items():
                    if v[0] == data[3:]:

                        kb = InlineKeyboardButton(text=v[1], callback_data=v[1])
                        keyboard.add(kb)
                        people_for_admin.update({v[1]: k})
                        
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена!')
                keyboard.add(kb)     
                    
                await bot.send_message(id, data[3:] + ' выберите людей: ', reply_markup=keyboard)
                # else:
                    # await bot.send_message(id, 'Список пока пуст')
            
            elif data in people_for_admin:
                await bot.send_message(people_for_admin[data], admins[id][0])
                await bot.send_message(id, f"'{admins[id][0]}' отправлено пользователю {data}", reply_markup=keyboard)
            
            
            
            elif data == 'определённым группам!':
                for i in allCurs.keys():
                    kb = InlineKeyboardButton(text=i, callback_data="group" + i)
                    keyboard.add(kb)
                     
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена!')
                keyboard.add(kb)     
                
                await bot.send_message(id, 'Выберите курс: ', reply_markup=keyboard)

            elif data[5:] in allCurs.keys():
                for i in allCurs[data[5:]]:
                     kb = InlineKeyboardButton(text=i, callback_data="group" + i)
                     keyboard.add(kb)
                     
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена!')
                keyboard.add(kb)     
                
                await bot.send_message(id, 'Выберите курс: ', reply_markup=keyboard)   
                             
            elif 'group' in data:
                if (all_users):
                        for k, v in all_users.items():
                            if v[0] == data[5:]:
                                await bot.send_message(k, admins[id][0], reply_markup=keyboard)
                        await bot.send_message(id, f"{admins[id][0]} отправлено группе {data[5:]}")

            elif data == 'всем группам!':
                for i, v in all_users.items():
                    await bot.send_message(i, admins[id][0])
                print("успешно")
                admins[id].clear()

        elif id in new_users.keys():
            if 'отмена' in data:
                new_users.remove(id)
            
            elif data in allCurs.keys():
                keyboard = InlineKeyboardMarkup(row_width=2)
                for i in allCurs[data]:

                    kb = InlineKeyboardButton(text=i, callback_data=i)
                    keyboard.add(kb)
                    
                kb = InlineKeyboardButton(text='отмена', callback_data='отмена')
                keyboard.add(kb)
                    
                await bot.send_message(id, "Выберите вашу группу: ", reply_markup=keyboard)
                    
            elif new_users[id] == 1:
                new_users[id] = data
                text = "Введите ваши фамилию и имя (Иванов Иван):"
                await bot.send_message(id, text)
        
        spammer.remove(id)
        
@dp.message_handler(commands=['start', 'schedule'])
# @dp.message(Command("start"))
# @dp.message(Command("schedule"))
async def new_schedule(message: types.Message=None, user_id=admin_id, value=False, curs='1К9394'):
    for page_number in range(0, 10):
        if curs.upper() in Groups[page_number]:
            name_png = "Расписание занятий_" + str(page_number) + ".png"
            f = open(name_png, "rb")
            await bot.send_photo(user_id, f, disable_notification=True)
            break
        else:
            pass
    
    if curs in ready_message:
        # await message.answer(name_file[0])
        await bot.send_message(user_id, name_file[0], reply_markup=ready_message[curs])
    else:
        await Cycles(bot).cycle_subject_main(user_id, curs)
        
def get_items(curs):
    mas = {}
    with open('homeworks.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        p = text['users'][curs]
        return p

@dp.message_handler(commands=['homeworks'])
# @dp.message(Command("homeworks"))
async def all_homeworks(message):
        # mas.clear()
        curs = all_users[message.from_user.id][0]
        mas = get_items(curs)
        
        for k, v in mas.items():
            # if i[2] == None:
                await bot.send_message(message.chat.id, f"{k} - {v[0]}")
            # else: 
            #     await bot.send_message(message.chat.id, f"{i[0]} - {i[1]}")
            #     await bot.forward_message(message.from_user.id, i[2], message_id=x[1])
       

# @dp.message_handler(commands=["all_days"])
# async def days_from_base(message, curs):
#         await bot.send_message(message.chat.id, f"Числитель")
#         for day in days:
#             await All_homworks_from_two_weaks(cur, conn, bot).repeate(message, day, 'числ', curs)
            
#         await bot.send_message(message.chat.id, f"Знаменатель")
#         for day in days:
#             await All_homworks_from_two_weaks(cur, conn, bot).repeate(message, day, 'знам', curs)

# @dp.message(Command("send_pdf"))

@dp.message_handler(commands=['send_pdf'])
async def get_file(message):
    try:
        f = open("Расписание занятий.pdf","rb")
    except:
        await bot.send_message(message.chat.id, 'сайт МРК не работает!!!')
        return
    await bot.send_document(message.from_user.id, f, disable_notification=True)


async def check_new():
        url = 'https://www.mrk-bsuir.by/ru'
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'lxml')
        a = soup.find('body')
        
        
        value = Files().after_download()
        if value == True:
            pass
        elif value == False:
            await bot.send_message(admin_id, "Новое расписание!!!")
            # Base_cheak(cur, conn).check_base_on_old_day()
    
    
    
    
    
    
async def check_new():

    value = Files().after_download()
    if value == True:
        pass
    # else:
    elif value == False:
        await bot.send_message(admin_id, "Новое расписание!!!")
        # await bot.send_message(1121101135, "Новое расписание!!!")
        # await bot.send_message(1129461474, "Новое расписание!!!")
        # await bot.send_message(672492540, "Новое расписание!!!")
    
async def timer():
    aioschedule.every(time_sleep).minutes.do(check_new)
    await asyncio.sleep(1)

async def scheduler():
    await timer()
    while True:
        try:
            await aioschedule.run_pending()
        except:
            await bot.send_message(admin_id, "Error")
            import os
            os._exit(0)
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

# from aiogram.client.session.aiohttp import AiohttpSession

def main(): 
    dp.start_polling(bot)
    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

main()

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

# if __name__ == '__main__':
#     dp.start_polling(bot)



# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")


# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())