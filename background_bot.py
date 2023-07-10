from imports import *

from slovars import schedule_sl, cleaner, name_file, real_new_file

class Files():

    def __init__(self):  
        pass

    def download_file(self):
        """Скачивание файла"""
        url = 'https://www.mrk-bsuir.by/ru'
        try:
            
            # proxies = {
            #     'http' : "proxy.server:3128",
            #     'https' : "proxy.server:3128"
            # }
            
            response = requests.get(url)
        except:
            bot.reply('сайт не работает!!!')
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        a = soup.find(id='rasp')
        
        red_a = a.text.split("\xa0на")
        name = ''
        for i in red_a:
            name += i + " "
        
        url = a.get('href')
        urllib.request.urlretrieve(url, 'Расписание занятий.pdf')

        return name


    def after_second(self):
        doc = fitz.open('Расписание занятий.pdf')
        for page in doc:
        # write_to_csw_from_pdf()
            
            Check_File().new_read(page)
        return False

    def after_download(self):
        text = self.download_file()
        # text = "Расписание занятий.pdf"
        # """Проверка, есть ли файл в памяти"""
        if text in name_file:
            return True
        else:
            cleaner()
            
            name_file.append(text)
            
            if text not in real_new_file:
                real_new_file.append(text)
            
            self.convert_pdf2img()
            value = self.after_second()
            return value

    def convert_pdf2img(self):
        """Преобразует PDF в изображение и создает файл одной страницы в форматие png"""
        doc = fitz.open('Расписание занятий.pdf')
        
        a = 0
        for page in doc:            
            pix = page.get_pixmap()    
            pix.save("Расписание занятий_"+ str(a) +".png")
            a += 1

        

# 
# def reading_csv():
#     results = []
#     with open('output.csv', encoding='utf-8') as file:
#         reader = csv.reader(file, delimiter=',')
#         for row in reader:
#             results.append(row)
#     return results

# def delete_musor(element):
#     for i in range(len(element)):
#         if 'Физ' in element[i] and 'зд' in element[i]:
#             element[i] = "Физра"
#     return element

# def to_masivs(row):
#     mas = []
#     for i in row:
#         elemnt = i.split('\n')
        
#         delete_musor(elemnt)
        
#         if (len(elemnt) > 3) and 'Физра' not in elemnt:
#             elemnt[0] += " " + elemnt[1]
#             del elemnt[1]
#         mas.append(elemnt)
#     return mas

# def red_text():
#     results = reading_csv()
#     last = ''
#     for row in results[2:]:
#         new_row = []
#         for i in row:
#             if len(i) < 2 or 'Замена' == i:
#                 pass
#             else:
#                 new_row.append(i)

#         if ('К' == new_row[0][1]):
#             schedule_sl.update({new_row[0]: []})
#             last = new_row[0]
#             schedule_sl[last] += to_masivs(new_row[1:])
#         else:
#             schedule_sl[last] += to_masivs(new_row)



# def write_to_csw_from_pdf():
#     i = 0
#     doc = fitz.open('Расписание занятий.pdf')
#     a = 1
#     for page in doc:
#         pix = page.get_pixmap()
#         pix.save("Расписание занятий_"+ str(i) +".png")
#         i += 1
#         tabula.convert_into('Расписание занятий.pdf', "output.csv", output_format="csv", pages=a)
#         # schedule_sl.update()
#         red_text()

#         a += 1

all_dict = {}


class Check_File():
    
    def __init__(self):  
        pass

    def create_list(self, p):
        i_ = iter(p)
        return list(itertools.zip_longest(i_, i_, i_))

    def delet_musor(self, p):
        if '2 Д О' in p:
            for i in range(len(p)):
                if '2 Д О' == p[i]:
                    del p[i]
        chars = set('1234')
        for i in range(4, len(p), 3):
            if 'Физра' not in p[i-4:i]:
                num = i-1
                if not any((c in chars) for c in p[num]):
                    # p[num-2] += " " + p[num-1]

                    num += 1
                    del p[num-1]
                else:
                    break
                    # else:
                    #     break
        return p


    def new_read(self, page):
        p = []

        page_text = page.get_text("text")
        text = page_text.split('\n')
        
        for index in range(len(text)):
            item = re.sub(r'\W+', '', text[index])
            if len(text[index]) > 4:
                if "К" in text[index][1]:
                    break
                
        all_groups.update({str(page)[5:6]: []})
        while True:
            if index >= len(text):
                break
            item = text[index]

            
            if "Замена" in item or "трансляция" in item or "подгруппа" in item and "Практика" not in item:
                pass
                
            else:
                if index >= len(text):
                    k = Check_File().create_list(p[1:])
                    schedule_sl.update({p[0]: k})
                    
                    all_groups[str(page)[5:6]].append(p[0])
                    
                    p.clear()
                    return
                    
                if len(item) > 2:
                    item = re.sub(r'\W+', ' ', item)
                    
                    if len(item) > 4:
                        item = re.sub(r'\W+', ' ', item)
                        if len(p) > 0:
                            if item[1] == "К":
                                item = re.sub(r'\W+', '', item)
                                k = Check_File().create_list(p[1:])
                                schedule_sl.update({p[0]: k})
                                all_groups[str(page)[5:6]].append(p[0])
                                p.clear()
                                
                        
            
                    if item[-1] == " ":
                        item = item[0:-1]
                        
                    if len(item) >= 2:
                        # if "Практика" in item:
                        #     if ('4' not in text[index+2]):
                        #         index += 1
                        #         item = item[0:10]
                        
                        if "Основы" in item and "подготовки" in text[index+1]:
                            if 'жизни' in text[index+3]:
                                index += 1
                            if "семейной" in text[index+1]:
                                index += 1
                            index += 1
                            item = "Семейная подготовка"
                        
                        elif "Основы" in item and "права" in text[index+1]:
                            index += 1
                            item = "Основы права"
                            
                        elif "Основы" in item and "констр" in text[index+1]:
                            index += 1
                            item = "Основы конструирования"
                            
                        elif "Подготовка к" in item:
                            if "семейной" in text[index+1]:
                                index += 1
                                
                            if "жизни" in text[index+1]:
                                index += 1
                            item = "Семейная подготовка"
                            
                        elif "Защита" in item:
                            if "населения" in text[index+1]:
                                index += 1
                            item = "Защита населения"
                            
                        elif "логические" in item:
                            if "техники" in text[index+2]:
                                index += 2
                            else:
                                index += 1
                                
                            item = "АЛОВТ"
                            
                        elif "Основы эл" in item:
                            if "микро" in text[index+1]:
                                index += 1
                            item = "ОЭМ"
                        
                        elif "ОТ" in item:
                            item = "Охрана труда"
                            
                        elif "Стандартизация" in item:
                            if "сертификация" in text[index+1]:
                                index += 1
                            item = "Стандартизация сертификация"
                        
                        elif "Основы" in item and "менедж" in text[index+1]:
                            index += 1
                            item = 'Основы менеджмента'
                        
                        elif "Нано" in item:
                            if "приборы" in text[index+1]:
                                index += 1
                                item = 'Нано электронные приборы'
                            
                        elif "'Моделирование" in item:
                            if "оптимизация" in text[index]:
                                index += 1
                                item = 'Моделирование и оптимизация'
                            
                        elif "Русск" in item:
                            if "яз" in item.lower():
                                item = "Русск яз" 
                            elif 'яз' in text[index+1].lower():
                                index += 1
                                item = "Бел яз"                         
                            
                            if "лит" in item.lower():
                                item = "Русск лит" 
                            elif 'лит' in text[index+1].lower():
                                index += 1
                                item = "Русск лит"   
                                     
                        elif "Бел" in item:
                            if "яз" in item.lower():
                                item = "Бел яз" 
                            elif 'яз' in text[index+1].lower():
                                index += 1
                                item = "Бел яз"                         
                            
                            if "лит" in item.lower():
                                item = "Бел лит" 
                            elif 'лит' in text[index+1].lower():
                                index += 1
                                item = "Бел лит"   
                                
                        elif "Технология" in item:
                            if "програм" in text[index+1]:
                                index += 1
                                item = 'Технология программирования'
                                
                        # elif "Основы" in item:
                        #     item = "Семейная подготовка"
                        #     if "жизни" in text[index+1]:
                        #         index += 1
                                
                        elif "Физика" in item and 'тела' in text[index+1]:
                            index += 1
                            item = "Физика твёрдого тела"
                            
                        elif "Компьютерные" in item:
                            if "сети" in text[index+1]:
                                index += 1
                            item = 'Компьютерные сети'
                            
                        elif "Матем" in item:
                            if "модел" in text[index+1]:
                                index += 1
                                item = "Математическое моделирование"
                                
                        elif "Общество" in item:
                            if 'Обществоведение' in item:
                                pass
                            else: index += 1
                            item = 'Общество'
                            
                        elif "Физ" in item and " к" in item:
                            if "зд" in text[index+1]:
                                index += 1
                            if " ий" in " " + text[index+2]:
                                index += 1
                            # if "ий" in text[index+2]:
                            #     index += 1
                            item = "Физ к и зд"  
                            
                        elif "Ист" in item and "Бел" in item:
                            item = "История"
                        
                        elif "Охрана" in item:
                            if "труда" in text[index+1]:
                                index += 1
                            item = "Охрана труда"
                                                
                            # p.append(item)
                            # p.append("Лобастов")
                            # p.append("Спорт зал")
                        elif "Компьют" in item:
                            if "сети" in text[index+1]:
                                index += 1
                            item = 'Компьютерные сети'
                            
                        elif "Основы комп" in item:
                            if 'графики' in text[index+1]:
                                index += 1
                            item = 'Основы комп графики'
                            
                        elif "Теория" in item:
                            if "матем" or "стат" in text[index+1]:
                                index += 1
                            item = "Теория вероятностей"
                            
                        elif "Организация" in item:
                            if "самост" in text[index+1]:
                                index += 1
                            if "работы" in text[index+1]:
                                index += 1
                            item = 'Организация сам работы'
                        
                        elif "стория" in item:
                            if 'Беларуси' in text[index+1]:
                                index += 1
                            item = "История"
                            
                        elif "Всемирная" in item:
                            if 'история' in text[index+1]:
                                index += 1
                            item = "История"
                            
                        elif "Проектирование" in item:
                            if "МЭУ" in text[index+1]:
                                index += 1
                            item = "Проектирование МЭУ"
                            
                        elif "Информац" in item and "технол" in text[index+1]:
                            index += 1
                            item = 'Информационные технологии'
                        
                        elif 'Прикладное' in item and 'обеспечение' in text[index+1]:
                            item = 'ППО'
                            index += 1


                        if "Ин" in item and "яз" in item:
                            while "4" not in text[index]:
                                index += 1
                            p.append('Англ яз')
                            p.append('Козак')
                            p.append(text[index])
                            
                        elif "Физ" in item and "зд" in item:
                            index += 1
                            index += 1
                            
                            p.append("Физра")
                            p.append("Лобастов")
                            p.append("Спорт зал")
                            p  = self.delet_musor(p)
                            
                        elif "Охрана" in item:
                            if "труда" in text[index+1]:
                                item = "Охрана труда"
                                index += 1 
                            p.append(item)
                            p.append(text[index+1])
                            index += 1
                            p.append(text[index+1])
                            index += 1

                        elif "История" in item:
                            p.append("История")
                            
                        elif "Ист" in item and "Бел" in item:
                            p.append("История")
                            
                        elif "стория" in item:
                            if 'Беларуси' in text[index+1]:
                                index += 1
                            item = "История"
                            p.append(item)
                            
                        elif "Всемирная" in item:
                            if 'история' in text[index+1]:
                                index += 1
                            item = "История" 
                            p.append(item)
                                               
                        elif "Трёхм" in item:
                            if 'моделир' in text[index+1]:
                                index += 1
                            item = 'Трёхмерное моделирование'
                            p.append(item)
                        else:    
                            p = self.delet_musor(p)
                            p.append(item)
                
            index += 1

        k = Check_File().create_list(p[1:])
        schedule_sl.update({p[0]: k})
        del p[0]
        return p
    

# doc = fitz.open('Расписание занятий.pdf')
# for page in doc:
#     p = Check_File().new_read(page)  
