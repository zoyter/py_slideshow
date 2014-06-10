#-*-coding:utf8-*-
"""
Пример реализации простого слайдшоу с автоматической сменой изображений
(с) Zoyter 2014
"""
try:
	from Tkinter import *
except:
	print(u'Не могу найти модуль Tkinter')

try:
	import os
except:
	print(u'Не могу найти модуль os')

try:
	import sys
except:
	print(u'Не могу найти модуль sys')	
	
try:
	import pygame
except:
	print(u'Не могу найти модуль pygame')	

class App:
    """
    Основной класс приложения
    """
    def __init__(self,width=800,height=600):
        """
			Инициализация класса        
        аргументы:
        self	--	ссылка на класс
        width	--	ширина окна
        height	--	высота окна
        """
        #Ширина окна приложения
        self.width=width
        #Высота окна приложения
        self.height=height
        #Список с расширениями графических файлов
        self.imgExt=['jpg','png','gif']
        #Вызов функции для получения списка всех графических файлов в текущей папке
        self.files=self.GetListOfImages('./')
        #Индекс картинки для отображения на экране
        self.filenumber=0
        #Временной предел для слайдшоу (счетчик времени обновляется раз за 25 кадров)
        self.time_lim=20
        #Устанавливаем стартовое значение для отсчета приода времени для отображения следующего изображения в автоматическом режиме
        self.time=self.time_lim
        #По умолчанию считаем, что автоматический показ картинок отключен
        self.auto=False
        #Создаем окно
        self.root=Tk()
        #Генерируем интерфейс
        self.makeGUI()
        #Запускаем основной цикл
        self.mainloop()

    def GetListOfImages(self,directory):
        """
        Получение списка всех графических файлов в указанной папке
        аргументы:
        self	--	ссылка на класс
        directory	--	путь к каталогу с картинками        
        """
        #Пустой список для графических файлов
        files=[]
        #Заполучаем список Всех файлов в указанной папке
        files = os.listdir(directory);
        #Просто временная переменная
        tmp=''
        #Список с результатом фильтрации
        r=[]
        #Цикл по всем файлам в папке
        for i in files:
			#Отрезаем расширение имени файла и переводим в нижний регистр
            tmp=i.split('.')[1].lower()
            #Если расширение имени файла попало в список с расширениями графических файлов
            if tmp in self.imgExt:
				# то добавляем этот файл в список с резултатом фильтрации
                r.append(i)
        #Возвращаем список графических файлов
        return r

    def btnBackClick(self,event):
        """
        Прокручивание списка файлов влево(назад)
        аргументы:
        self	--	ссылка на класс
        event	--	события
        """		
        print(u'Листаем влево')
        #Уменьшаем на 1 индекс картинки, отображаемой на экране
        self.filenumber-=1
        #Если индекс стал отрицательным, то
        if self.filenumber<=0:
			#Присваиваем ему номер последней картинки в списке с графическими файлами
            self.filenumber=len(self.files)-1
        #Выводим номер картинки в консоль
        print(self.filenumber)
        #Загружаем графическое изображение
        tmp=pygame.image.load(self.files[self.filenumber]).convert()
        #Масштабируем картинку к размеру окна и приваиваем переменно в, которой хранится отображаемая на экране картинка
        self.img=pygame.transform.scale(tmp,(self.width,self.height))

    def btnForwardClick(self,event):
        """
        Прокручивание списка файлов вправо(вперед)
        аргументы:
        self	--	ссылка на класс
        event	--	события
        """				
        print(u'Листаем вправо')
        #Увеличиваем на 1 индекс картинки, отображаемой на экране
        self.filenumber+=1
        #Если индекс стал больше чем у нас картинок, то
        if self.filenumber>len(self.files)-1:
			#Присваиваем ему номер первой картинки в списке с графическими файлами
            self.filenumber=0
        #Выводим номер картинки в консоль
        print(self.filenumber)
        #Загружаем графическое изображение
        tmp=pygame.image.load(self.files[self.filenumber]).convert()
        #Масштабируем картинку к размеру окна и приваиваем переменно в, которой хранится отображаемая на экране картинка
        self.img=pygame.transform.scale(tmp,(self.width,self.height))

    def btnQuitClick(self,event):
        """
        Завершение работы приложения
        аргументы:
        self	--	ссылка на класс
        event	--	события
        """			
        #Завершаем работу приложения
        self.root.destroy()

    def chkBox1Click(self,event):
        """
        Включение и отключение автоматического просмотра
        аргументы:
        self	--	ссылка на класс
        event	--	события
        """	
        #Если включено, то выключаем и наоборот		
        self.auto=not(self.auto)

    def makeGUI(self):
        """
        Формирование интерфейса приложения
        аргументы:
        self	--	ссылка на класс        
        """			
        #Первый фрэйм для кнопок
        self.frame1 = Frame(self.root, height = 60, bg = 'gray')
        #Второй фрэйм для отображения картинок
        self.frame2 = Frame(self.root, height = self.height, width = self.width)
        #
        #Определение операционной системы
        #но и без него как то работает :-)
        '''
        if sys.platform[0]=='w':
            print('Windows')
            # The wxPython wiki says you might need the following line on Windows
            # (http://wiki.wxpython.org/IntegratingPyGame).
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        else:
            print('Linux')
            # Tell pygame's SDL window which window ID to use
        '''
        #Интеграция окна pygame во второй фрэйм нашего приложения
        #Это самый важный момент в приложении, без него просто создается два отдельных окна
        os.environ['SDL_WINDOWID'] = str(self.frame2.winfo_id())
        
        ####	Упаковка фрэймов
        #Первый фрэйм в верху
        self.frame1.pack(side = 'top', fill = 'x')
        #Второй фрэйм внизу
        self.frame2.pack(side = 'bottom', fill = 'both', expand = 1)
        
        #Кнопка Назад
        self.btnBack = Button(self.frame1, text = 'Назад')
        #Кнопка Вперед
        self.btnForward = Button(self.frame1, text = 'Вперед')
        #Кнопка Выход
        self.btnQuit = Button(self.frame1, text = 'Выход')
        #Чекбокс Авто
        self.chkBox1 = Checkbutton(self.frame1, text="Авто")
        
        #Указываем взаимное расположение кнопок
        self.btnBack.pack(side='left')
        self.btnForward.pack(side='left')
        self.btnQuit.pack(side='left')
        self.chkBox1.pack(side='left')
        
        #Привязываем обработчики событий к кнопкам
        self.btnBack.bind("<Button-1>", self.btnBackClick)
        self.btnForward.bind("<Button-1>", self.btnForwardClick)
        self.btnQuit.bind("<Button-1>", self.btnQuitClick)
        #Привязываем обработчики событий к чекбоксу
        self.chkBox1.bind("<Button-1>", self.chkBox1Click)
        
        #Обновляем окно
        self.root.update()
        
        #Инициализируем pygame
        pygame.display.init()
        #Создаем экран и задаем его параметры
        self.screen = pygame.display.set_mode((self.width,self.height))
        #Создаем "таймер"
        self.clock=pygame.time.Clock()
        #Загружаем первую картинку из списка графических файлов
        tmp=pygame.image.load(self.files[0]).convert()
        #Подгоняем размеры картинки под размеры окна
        self.img=pygame.transform.scale(tmp,(self.width,self.height))

    def mainloop(self):
		#запускаем бесконечный цикл в котором все будет рисоваться
        while 1:
            #Если включен автоматический показ
            if self.auto:
				#Уменьшаем счетчик времени на 1
                self.time-=1
                #И если время истекло, то
                if self.time<=0:
					#Устанавливаем счетчик времени на максимум
                    self.time=self.time_lim
                    #и вызываем функцию, которая срабатывает при нажатии на кнопку Вперед
                    #т.е. листаем вперед
                    self.btnForwardClick('q')
            #Выводим картинку на экран (на самом деле рисуем на surface из pygame, который вставлен в окно Tk)
            self.screen.blit(self.img,[0,0])
            # Обновляем изображение display
            pygame.display.flip()
            self.clock.tick(20)
            # Обновляем Tk экран/окно
            self.root.update()

#Создаем приложение SlideShow на базе описанного выше класса
SlideShow=App(800,600)
