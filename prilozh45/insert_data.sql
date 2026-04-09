-- ============================================
-- Заполнение каталога программ реальными данными
-- ============================================

-- Сначала добавим ключевые слова (Slova)
insert into public."Slova" (nazvanie) values
    ('браузер'),
    ('офис'),
    ('редактор'),
    ('мультимедиа'),
    ('графика'),
    ('архиватор'),
    ('безопасность'),
    ('коммуникации'),
    ('разработка'),
    ('наука'),
    ('образование'),
    ('игры'),
    ('утилиты'),
    ('сеть'),
    ('текст');

-- Добавим программы (prog)
insert into prog (nazvanie, opisanie, god_osnovania, img, img_data) values
    -- Браузеры
    ('Mozilla Firefox', 'Свободный веб-браузер с открытым исходным кодом. Поддерживает расширения, синхронизацию между устройствами, режим приватного просмотра.', 2002, null, null),
    ('Google Chrome', 'Веб-браузер от компании Google. Известен высокой скоростью работы, поддержкой расширений и интеграцией с сервисами Google.', 2008, null, null),
    ('Opera', 'Веб-браузер со встроенными функциями: VPN, блокировщик рекламы, мессенджеры. Подходит для экономии трафика.', 1995, null, null),
    ('Microsoft Edge', 'Браузер от Microsoft на базе Chromium. Интегрирован с Windows, поддерживает расширения Chrome.', 2015, null, null),

    -- Офисные пакеты
    ('LibreOffice', 'Мощный офисный пакет с открытым исходным кодом. Включает текстовый процессор, таблицы, презентации, базы данных.', 2010, null, null),
    ('Apache OpenOffice', 'Офисный пакет с открытым исходным кодом. Содержит Writer, Calc, Impress, Draw, Base, Math.', 2011, null, null),
    ('Microsoft Office', 'Популярный офисный пакет от Microsoft. Включает Word, Excel, PowerPoint, Outlook и другие приложения.', 1990, null, null),
    ('WPS Office', 'Бесплатный офисный пакет с поддержкой форматов Microsoft Office. Легкий и быстрый.', 2013, null, null),

    -- Графические редакторы
    ('GIMP', 'Мощный растровый графический редактор с открытым исходным кодом. Аналог Adobe Photoshop.', 1996, null, null),
    ('Inkscape', 'Профессиональный векторный графический редактор. Поддерживает SVG, подходит для иллюстраций и логотипов.', 2003, null, null),
    ('Krita', 'Программа для цифрового рисования и анимации. Популярна среди художников и концепт-артистов.', 2005, null, null),
    ('Blender', 'Профессиональный пакет для 3D-моделирования, анимации, рендеринга и видеомонтажа.', 1998, null, null),

    -- Мультимедиа
    ('VLC Media Player', 'Универсальный медиаплеер с открытым исходным кодом. Воспроизводит практически все форматы видео и аудио.', 2001, null, null),
    ('Audacity', 'Редактор аудио с открытым исходным кодом. Запись, редактирование, эффекты, конвертация.', 2000, null, null),
    ('Shotcut', 'Видеоредактор с открытым исходным кодом. Поддерживает множество форматов и эффектов.', 2011, null, null),
    ('OBS Studio', 'Программа для записи экрана и потокового вещания. Используется стримерами по всему миру.', 2012, null, null),

    -- Архиваторы
    ('7-Zip', 'Бесплатный архиватор с высокой степенью сжатия. Поддерживает форматы ZIP, 7z, RAR и другие.', 1999, null, null),
    ('WinRAR', 'Популярный архиватор для Windows. Создает и распаковывает архивы RAR и ZIP.', 1993, null, null),
    ('PeaZip', 'Бесплатный архиватор с открытым исходным кодом. Поддерживает более 180 форматов.', 2006, null, null),

    -- Безопасность
    ('Kaspersky Free', 'Бесплатный антивирус от Лаборатории Касперского. Базовая защита от вирусов и угроз.', 2016, null, null),
    ('Avast Free Antivirus', 'Популярный бесплатный антивирус. Защита в реальном времени, сканер уязвимостей.', 1988, null, null),
    ('Malwarebytes', 'Программа для удаления вредоносного ПО. Дополняет традиционные антивирусы.', 2004, null, null),

    -- Коммуникации
    ('Telegram Desktop', 'Официальный клиент Telegram для ПК. Быстрый, безопасный, с поддержкой секретных чатов.', 2013, null, null),
    ('Discord', 'Приложение для голосового, видеочата и обмена сообщениями. Популярно среди геймеров.', 2015, null, null),
    ('Skype', 'Программа для видеозвонков и обмена сообщениями. Принадлежит Microsoft.', 2003, null, null),
    ('Zoom', 'Платформа для видеоконференций. Популярна для онлайн-встреч и вебинаров.', 2011, null, null),

    -- Разработка
    ('Visual Studio Code', 'Легковесный редактор кода от Microsoft. Поддержка языков, отладка, Git, расширения.', 2015, null, null),
    ('PyCharm Community', 'IDE для разработки на Python. От JetBrains, бесплатная версия с базовыми функциями.', 2010, null, null),
    ('Git', 'Система контроля версий. Стандарт для совместной разработки программного обеспечения.', 2005, null, null),
    ('Notepad++', 'Редактор кода для Windows. Подсветка синтаксиса, плагины, работа с большими файлами.', 2003, null, null),

    -- Образование
    ('Stellarium', 'Планетарий с открытым исходным кодом. Показывает реалистичное небо в 3D.', 2000, null, null),
    ('GeoGebra', 'Математическая программа для обучения. Геометрия, алгебра, математический анализ.', 2001, null, null),
    ('Anki', 'Программа для запоминания с использованием интервальных повторений. Карточки для обучения.', 2006, null, null),
    ('Duolingo', 'Приложение для изучения языков. Игровой формат, более 40 языков.', 2011, null, null);

-- Связываем программы с ключевыми словами
-- Firefox (id=1)
insert into public."Slova_Programms" (id_slovo, id_programm) values (1, 1), (13, 1), (14, 1);
-- Chrome (id=2)
insert into public."Slova_Programms" (id_slovo, id_programm) values (1, 2), (13, 2), (14, 2);
-- Opera (id=3)
insert into public."Slova_Programms" (id_slovo, id_programm) values (1, 3), (13, 3), (14, 3);
-- Edge (id=4)
insert into public."Slova_Programms" (id_slovo, id_programm) values (1, 4), (13, 4), (14, 4);

-- LibreOffice (id=5)
insert into public."Slova_Programms" (id_slovo, id_programm) values (2, 5), (15, 5), (3, 5);
-- OpenOffice (id=6)
insert into public."Slova_Programms" (id_slovo, id_programm) values (2, 6), (15, 6), (3, 6);
-- Microsoft Office (id=7)
insert into public."Slova_Programms" (id_slovo, id_programm) values (2, 7), (15, 7);
-- WPS Office (id=8)
insert into public."Slova_Programms" (id_slovo, id_programm) values (2, 8), (15, 8);

-- GIMP (id=9)
insert into public."Slova_Programms" (id_slovo, id_programm) values (5, 9), (3, 9);
-- Inkscape (id=10)
insert into public."Slova_Programms" (id_slovo, id_programm) values (5, 10), (3, 10);
-- Krita (id=11)
insert into public."Slova_Programms" (id_slovo, id_programm) values (5, 11), (3, 11);
-- Blender (id=12)
insert into public."Slova_Programms" (id_slovo, id_programm) values (5, 12), (4, 12), (3, 12);

-- VLC (id=13)
insert into public."Slova_Programms" (id_slovo, id_programm) values (4, 13);
-- Audacity (id=14)
insert into public."Slova_Programms" (id_slovo, id_programm) values (4, 14), (3, 14);
-- Shotcut (id=15)
insert into public."Slova_Programms" (id_slovo, id_programm) values (4, 15), (3, 15);
-- OBS (id=16)
insert into public."Slova_Programms" (id_slovo, id_programm) values (4, 16), (13, 16);

-- 7-Zip (id=17)
insert into public."Slova_Programms" (id_slovo, id_programm) values (6, 17), (13, 17);
-- WinRAR (id=18)
insert into public."Slova_Programms" (id_slovo, id_programm) values (6, 18), (13, 18);
-- PeaZip (id=19)
insert into public."Slova_Programms" (id_slovo, id_programm) values (6, 19), (13, 19);

-- Kaspersky (id=20)
insert into public."Slova_Programms" (id_slovo, id_programm) values (7, 20), (13, 20);
-- Avast (id=21)
insert into public."Slova_Programms" (id_slovo, id_programm) values (7, 21), (13, 21);
-- Malwarebytes (id=22)
insert into public."Slova_Programms" (id_slovo, id_programm) values (7, 22), (13, 22);

-- Telegram (id=23)
insert into public."Slova_Programms" (id_slovo, id_programm) values (8, 23), (14, 23);
-- Discord (id=24)
insert into public."Slova_Programms" (id_slovo, id_programm) values (8, 24), (14, 24), (12, 24);
-- Skype (id=25)
insert into public."Slova_Programms" (id_slovo, id_programm) values (8, 25), (14, 25);
-- Zoom (id=26)
insert into public."Slova_Programms" (id_slovo, id_programm) values (8, 26), (14, 26);

-- VS Code (id=27)
insert into public."Slova_Programms" (id_slovo, id_programm) values (9, 27), (3, 27), (15, 27);
-- PyCharm (id=28)
insert into public."Slova_Programms" (id_slovo, id_programm) values (9, 28), (3, 28);
-- Git (id=29)
insert into public."Slova_Programms" (id_slovo, id_programm) values (9, 29), (13, 29);
-- Notepad++ (id=30)
insert into public."Slova_Programms" (id_slovo, id_programm) values (9, 30), (3, 30), (15, 30);

-- Stellarium (id=31)
insert into public."Slova_Programms" (id_slovo, id_programm) values (10, 31), (11, 31);
-- GeoGebra (id=32)
insert into public."Slova_Programms" (id_slovo, id_programm) values (10, 32), (11, 31);
-- Anki (id=33)
insert into public."Slova_Programms" (id_slovo, id_programm) values (11, 33), (10, 33);
-- Duolingo (id=34)
insert into public."Slova_Programms" (id_slovo, id_programm) values (11, 34), (10, 34);
