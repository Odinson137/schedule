
def cleaner():
    schedule_sl.clear()
    name_file.clear()
    ready_message.clear()
    for i, value in items.items():
        value.clear()
    homeworks.clear()

name_file = []

"""Словарь типа {название скачанного файла (Расписание занятий на...) : предметы (математика, русский и тд...)}"""
schedule_sl = {}

"""Словарь для хранения данных готового сообщения типа [ курс (1k9394): [заполненные кнопки]]"""
ready_message = {}

"""Словарь для хранения названий всех предметов и домашки от пользователей типа { математика : номера 24 256 и 157}"""
items = {'2К9191': {}, '2К9091': {}, '2К9111': {}, '1К9091': {}, '1К9191': {}, '1К9111': {}, '0К9091': {}, '0К9191': {}, '0К9111': {}, '9К9191': {}, '2К9391': {}, '2К9392': {}, '2К9393': {}, '2К9394': {}, '2К9311': {}, '1К9391': {}, '1К9392': {}, '1К9393': {}, '1К9394': {}, '1К9311': {}, '0К9391': {}, '0К9392': {}, '0К9393': {}, '0К9394': {}, '0К9311': {}, '9К9391': {}, '9К9392': {}, '9К9393': {}, '9К9394': {}, '2К9491': {}, '2К9591': {}, '2К9291': {}, '1К9491': {}, '1К9591': {}, '1К9291': {}, '0К9491': {}, '0К9591': {}, '0К9291': {}, '2К9341' : {}, '2К9342' : {}, '1К9341': {}, '0К9341':{}, '9К9341':{}}

allCurs = {'1 курс': ['2К9191', '2К9091', '2К9111', '2К9391', '2К9392', '2К9393', '2К9394', '2К9311', '2К9491', '2К9591', '2К9291', '2К9341', '2К9342'], 
           '2 курс': ['1К9091', '1К9191', '1К9111', '1К9391', '1К9392', '1К9393', '1К9394', '1К9311', '1К9491', '1К9591', '1К9291', '1К9341'], 
           '3 курс': ['0К9091', '0К9191', '0К9111', '0К9391', '0К9392', '0К9393', '0К9394', '0К9311', '0К9491', '0К9591', '0К9291', '0К9341'], 
           '4 курс': ['9К9191', '9К9391', '9К9392', '9К9393', '9К9394', '9К9341']}

mas = []
for i, v in items.items():
    mas.append("\""+i+"\"")
print(", ".join(mas))
# for i in items.keys():
#     if '2' in i[0]:
#         allCurs['1 курс'].append(i)

#     elif '1' in i[0]:
#         allCurs['2 курс'].append(i)

#     elif '0' in i[0]:
#         allCurs['3 курс'].append(i)

#     elif '9' in i[0]:
#         allCurs['4 курс'].append(i)
        

"""Словрь для хранения домашнего задания типа [ краткое сообщение (20 символов ведь больше кнопка в телеге не поддерживает): [полное дз, [id фото]] ]"""
homeworks = {}

"""Словрь для хранения id пользователей и его групыы [ id : 1k9394 ]"""
new_users = {}

all_users = {}

real_new_file = []
