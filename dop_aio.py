from email import message
from imports import *

from slovars import schedule_sl, ready_message, homeworks, all_users, name_file

from background_bot import *

class Cycles():
    def __init__(self, bot):
        self.bot = bot

    async def cycle_subject_main(self, user_id, curs):

        """Создание нового сообщения с расписанием"""
        keyboard = InlineKeyboardMarkup(row_width=3)
        print('основной словарь')
        print(schedule_sl)
        for subjects in schedule_sl[curs]:

            text = f"{subjects[0]} - {subjects[-1]}"
            kb = InlineKeyboardButton(text=text, callback_data='subject')

            kb_2 = Select_subjects().select(subjects[0], all_users[user_id][0])
            keyboard.add(kb, kb_2)
            
        # info_date = Base_cheak(self.cur, self.conn).check_base_on_old_day()
        if len(schedule_sl):
            # await self.bot.send_message(f"{name_file[0]}")
            
            await self.bot.send_message(user_id, f"{name_file[0]}", reply_markup=keyboard)
            ready_message.update({ curs :keyboard})

# mas = {}
def get_items(curs):
    with open('homeworks.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        if (curs in text['users']):
            p = text['users'][curs]
        else:
            p = {}
            with open('homeworks.json', 'w', encoding='utf-8') as f:
                text['users'].update({curs: {}})
                json.dump({'users': text['users']}, f, indent = 6, ensure_ascii=False)
        
    return p

def dop_on_home(curs, item):
    with open('homeworks.json', 'r', encoding='utf-8') as f: 
        text = json.load(f)
        print('sdggdsdsggdssdg')
        print(text)
        with open('homeworks.json', 'w', encoding='utf-8') as f:
            if 'users' in text:
                if curs not in text['users']:
                    text['users'] = {curs: {}}
                print(text)
                text['users'][curs].update({item: ['Ничего', None, None]})
                json.dump({'users': text['users']}, f, indent = 6, ensure_ascii=False)
            else:
                text.update({'users': {curs: {}}})
                json.dump({'users': text['users']}, f, indent = 6, ensure_ascii=False)
                
class Select_subjects():
    def __init__(self):
        pass
    # def add_subject(self, subject, curs):
    #     print('add')


    def search_subject(self, subject, mas, curs):
        if subject in mas:
            return True
        else: dop_on_home(curs, subject)


    def search_photo_in_subject(self, subject, curs):
        # print('search_subject')
        select = " SELECT (photo, id_user_photo) FROM homework WHERE item = %s AND curs = %s"
        value = subject[0], curs
        self.cur.execute(select, value)
        photot_id = self.cur.fetchone()[0]
        photot_id = photot_id[1:-1].split(",")
        if photot_id:
            return photot_id
        else: None


    def select(self, subject, curs):
            mas = get_items(curs)
            if (subject in mas):
                sub = mas[subject]
            else: 
                sub = ['None']
            
            if len(subject) == 1:
                home = ['ничегосe']
                # kb_2 = InlineKeyboardButton(text=home[0], callback_data='ничего')

            elif self.search_subject(subject, mas, curs) == True:
                home = [sub[0]]

            else: home = ['ничегос']
        
            if len(sub) > 1 and sub[1] != None:
                homeworks.update({home[0][0:20]: [home[0], [sub[1], sub[2]]]})
            else:
                homeworks.update({home[0][0:20]: [home[0]]})
            
            kb_2 = InlineKeyboardButton(text=home[0][0:20], callback_data=home[0][0:20])
            return kb_2


# class Base_cheak():
#     def __init__(self, cur, conn):
#         self.cur = cur
#         self.conn = conn


#     def check_base_on_old_day(self):
#         for curs, value in schedule_sl.items():
#             items = []
#             for i in value:
#                 items.append(i[0]) 
#             common_date = name_file[0][22:-1].split(', ')
#             info_date = self.dop(common_date, curs)
#             if info_date:
#                 pass
#             else:
#                 self.get_in_base_new_day(common_date, items, curs)


#     def dop(self, common_date, curs):
#         select = " SELECT day, value FROM schedule_day WHERE day = %s and value = %s and curs = %s"
#         value = common_date[0], common_date[1][0:4], curs
#         self.cur.execute(select, value)
#         x = self.cur.fetchone()
#         print(x)           
#         return x


#     def get_in_base_new_day(self, d_a_v, items, curs):
#         items = list(set(items))

        
#         insert = ''
#         if len(items) == 3:
#             insert = " INSERT INTO schedule_day (day, value, curs, item_1, item_2, item_3) VALUES (%s, %s, %s, %s, %s, %s)" 
#             value = d_a_v[0], d_a_v[1][0:4], curs, items[0], items[1], items[2]
#         elif len(items) == 1:
#             insert = " INSERT INTO schedule_day (day, value, curs, item_1) VALUES (%s, %s, %s, %s)" 
#             value = d_a_v[0], d_a_v[1][0:4], curs, items[0]
#         elif len(items) == 4:
#             insert = " INSERT INTO schedule_day (day, value, curs, item_1, item_2, item_3, item_4) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
#             value = d_a_v[0], d_a_v[1][0:4], curs, items[0], items[1], items[2], items[3]
#         elif len(items) == 2:
#             insert = " INSERT INTO schedule_day (day, value, curs, item_1, item_2) VALUES (%s, %s, %s, %s, %s)" 
#             value = d_a_v[0], d_a_v[1][0:4], curs, items[0], items[1]
#         elif len(items) == 5:
#             insert = " INSERT INTO schedule_day VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
#             value = d_a_v[0], d_a_v[1][0:4], curs, items[0], items[1], items[2], items[3], items[4]
            
#         else:
#             print('return')
#             return    
#         # insert = " INSERT INTO schedule_day (day, value, item_1, item_2, item_3, item_4, item_5) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
#         # value = d_a_v[0], d_a_v[1][0:4], items[0], items[1], items[2], items[3], items[4], items[5]
#         self.cur.execute(insert, (value))
#         self.conn.commit()


all_days = {}
# class All_homworks_from_two_weaks():

#     def __init__(self, cur, conn, bot):
#         self.cur = cur
#         self.conn = conn
#         self.bot = bot


#     async def repeate(self, message, day, val, curs):
#         # print(all_days)

#         # if curs in all_days.keys():
#         #     print(all_days[curs])
#         #     print(all_days[curs][val])
#         #     if val in all_days[curs][val]:
#         #         if day in all_days[curs][val][day]:
#         #             print(all_days[curs][val][day])
#         #             await self.repeate_second(message, day, val, curs)
#         # else:
#             select = " SELECT day, value, item_1, item_2, item_3, item_4, item_5 FROM schedule_day WHERE day = %s and value = %s and curs = %s"
#             value = day.lower() , val, curs
#             self.cur.execute(select, value)
#             x = self.cur.fetchall()
#             if x:
#                 x = x[0]
 
#                 all_days.update({curs: {}})
                
#                 all_days[curs].update({'числ': {}, 'знам': {}})

#                 all_days[curs][x[1]].update({x[0]: [x[2], x[3], x[4], x[5], x[6]]})

#                 # kb = InlineKeyboardButton(text=day, callback_data='subject')
#                 await self.bot.send_message(message.chat.id, f"{x[0]}\n{x[2]}, {x[3]}, {x[4]}, {x[5]}, {x[6]}")
#             else:
#                 pass


#     async def repeate_second(self, message, day, value, curs):
#         print(all_days)
#         for day in all_days[curs][value]:
#             print(day)
#             await bot.send_message(message.chat.id, f"{day[0]}\n{day[2]}, {day[3]}, {day[4]}, {day[5]}, {day[6]}")
            
