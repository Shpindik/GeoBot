from frozendict import frozendict

ADMIN_DICT = frozendict({
    'admin_accept': 'Добро пожаловть в панель администратора😎',
    'admin_accept_spam': 'Введите сообщение для рассылки:',
    'admin_add_alert': '❌ Ошибка: ID должен быть целым числом.',
    'admin_add_new_admin': 'Введите ID нового администратора:',
    'admin_add_user': 'Добавить Админа',
    'admin_alert': '❌ Ошибка:',
    'admin_alert_delete_admin': '⛔ Нельзя удалить основных администраторов!',
    'admin_already_exists': 'Админ с ID {new_admin_id} уже существует.',
    'admin_answer': '📨 Ответить',
    'admin_answer_success': '✅ Ваше сообщение отправлено!',
    'admin_answer_success_to_user': '☑️ Ваше сообщение отправлено ученику ',
    'admin_back': '⬅️ Назад',
    'admin_back_to_admin': '⬅️ Вернуться в панель администратора',
    'admin_bot_reply': '📩 Ответ от бота: ',
    'admin_close': '❌ Отмена',
    'admin_close_admin': 'Выйти из админки ⚙️',
    'admin_confirm': ('Вы уверены, что хотите удалить администратора '
                      '{admin_id_to_delete}?'),
    'admin_delete': 'Удалить админа {admin_id}',
    'admin_delete_accept': '✅ Администратор {admin_id_to_delete} удален!',
    'admin_delete_list': 'Список администраторов для удаления:',
    'admin_delete_user': 'Удалить Админа',
    'admin_denied': ('🔒 У вас нет прав администратора. Воспользуйтесь '
                     'коммандой /start для перехода в основное меню.'),
    'admin_empty': 'Нет администраторов для удаления.',
    'admin_empty_users': '📭 В базе данных нет пользователей.',
    'admin_export_accept': '✅ Данные успешно экспортированы.',
    'admin_export_allert': 'Ошибка при экспорте данных:',
    'admin_export_users': '📜 Экспорт пользователей',
    'admin_length_alert': ('Длинна вводимого айди должна быть от 9 '
                           'до 10 цифр'),
    'admin_new_msg': '✉️ Новое сообщение от ученика: ',
    'admin_next': '➡️ Далее',
    'admin_not_found': '🔍 Администратор не найден!',
    'admin_ok': '✅ Подтвердить',
    'admin_reply_to_user': '📨 Ответить ученику',
    'admin_start_spam': '🚀 Рассылка сообщений 🚀',
    'admin_spam_success': '🚀 Рассылка успешно отправлена!',
    'admin_succes_add_admin': 'Админ с ID {new_admin_id} добавлен.',
    'admin_user_message': ('✍️ Задай вопрос администратору:\n'
                           'Не забудь написать номер задания, или название '
                           'темы!'),
    'admin_view_user': 'Посмотреть пользователей бота',
    'admin_view_users': '📊 Список пользователей:',

})

TEXT_DICT = frozendict({
    'accept': '✅ Все верно ✅',
    'about': ('О боте \n'
              'Этот бот создан для подготовки к ОГЭ по географии. Он поможет '
              'проверить знания, разобраться в сложных темах и отработать '
              'задания в удобном формате. В боте есть тесты, справочные '
              'материалы и полезные подсказки, которые сделают подготовку '
              'проще и эффективнее. Подходит как для самостоятельного '
              'обучения, так и для дополнительной практики перед экзаменом.'),
    'about_button': 'Подробнее о боте🧐',
    'approve_data': 'Имя: {message}\nКласс: {class_name}',
    'ask_to_admin': 'Задать вопрос по заданию 🤔',
    'allert_input_name': 'Пожалуйста, введи свои реальные имя и фамилию 😁',
    'back_task': '🔙 Вернутся к заданию 🔙',
    'back_task_list': '⏪ Назад к списку заданий ⏪',
    'back_to_main_button': '⏪ Вернуться в главное меню ⏪',
    'cancel': '❌ Исправить данные ❌',
    'chose_task': 'Выбери номер задания, которое хочешь решить 🤔',
    'chose_class': 'Выбери класс, в котором ты учишься 🎓',
    'correct_msg': '✅ Правильно! Молодец 😊!',
    'class': ['9-А', '9-Б', '9-В', '9-Г', '9-К', '9-М', '9-Р', '9-С', '9-Э'],
    'error_msg': 'Неправильно 😔 Подумай еще раз, и ответь на вопрос 🤔',
    'greet': ('Привет, {name}! Я бот – твой помощник для подготовки к ОГЭ '
              'по географии 📚✨ Помогу разобраться в картах, климате, '
              'населении и других темах. 🗺️🌎 Задавай вопросы и получай '
              'ответы – вместе разберёмся во всём! 🚀'),
    'into_task': 'Перейти к вопросам 👀',
    'main_menu': ('Рад знакомству, {name} 🤝 !\n'
                  'Теперь я буду помогать тебе подготовиться к ОГЭ по '
                  'географии 🌍📚\n'
                  'По кнопке ниже, ты можешь выбрать номер интересующего '
                  'тебя задания, а я помогу тебе с ним разобраться 🚀'),
    'next_step_class': 'Отлично! \nТеперь напиши свои Имя и Фамилию 😉',
    'tasks': ['2', '3', '5', '6', '8',
              '9', '10', '11', '15', '19',
              '22', '24', '25', '26'],
})

VIDEO_LINKS = frozendict({
    'video_2': 'https://rutube.ru/video/f8cdfddf0fa59963d92fde841bfde0fb/',
    'video_5': 'https://rutube.ru/video/854ce20ade387f87041ca1e29e002448/',
    'video_6': 'https://rutube.ru/video/854ce20ade387f87041ca1e29e002448/',
    'video_9': 'https://rutube.ru/video/854ce20ade387f87041ca1e29e002448/',
})

TASK_DICT = frozendict({
    'video_task': ('В этом задании надо будет посмотреть видео и ответить '
                   'на вопросы. \n'
                   'Внимательно ознакомся с информацией в видео '
                   '\nУдачи! 🚀'),
    'video_no_task': ('В этом задании надо будет просто посмотреть видео. '
                      'Задание простое, надеюсь у тебя не возникнет с '
                      'ним сложностей.\n'
                      'Внимательно ознакомся с информацией в видео '
                      '\nУдачи! 🚀'),
    'task_2_1': ('Вопрос 1: Напиши название пропущеной страны 🗺️ \n'
                 'Одним из пограничных субъектов РФ является Мурманская '
                 'область, которая имеет выход к Государственной границе '
                 'РФ с Финляндией и ...'),
    'task_2_2': ('Вопрос 2: Напиши название пропущеной страны 🗺️ \n'
                 'Одним из пограничных субъектов РФ является Республика '
                 'Бурятия, которая имеет выход к Государственной границе '
                 'РФ с ...'),
    'task_2_3': ('Вопрос 3: Напиши название пропущеной страны 🗺️ \n'
                 'Одним из пограничных субъектов РФ является Челябинская '
                 'область, которая имеет выход к Государственной границе '
                 'РФ с ...'),
    'task_2_4': ('Вопрос 4: Напиши название пропущеной страны 🗺️ \n'
                 'Одним из приграничных субъектов РФ является Приморский '
                 'край, который имеет выход к сухопутной Государственной '
                 'границе РФ с КНДР и ...'),
    'task_2_5': ('Вопрос 5: Напиши название пропущеной страны 🗺️ \n'
                 'Одним из пограничных субъектов РФ является Чукотский '
                 'автономный округ, который имеет выход к Государственной '
                 'границе РФ с ...'),
    'task_3': (
        '<i>Для успешного выполнения данного задания необходимо знать '
        '5 закономерностей природы нашей страны, которые описаны ниже. '
        'При выполнении задания необходимо пользоваться картой атласа '
        'за 8-9 классы «Федеративное устройство России».</i>\n\n'

        '<b>1. Плодородие почв</b> '
        'В нашей стране увеличивается с севера на юг, от зоны арктических '
        'пустынь на севере до степей на юге. Плодородие почв напрямую зависит '
        'от содержания в ней гумуса. Так, минимальное содержание гумуса — в '
        'тундрово-глеевых почвах Крайнего Севера, а максимальное — в '
        'черноземах степной зоны.\n\n'

        '<b>2. Минимальные температуры воздуха</b> '
        'В нашей стране в зимний период наблюдаются в Восточной Сибири, '
        'максимальные — на Восточно-Европейской равнине из-за согревающего '
        'влияния Атлантического океана. Чем дальше на восток (от '
        'Атлантического океана), тем холоднее. Летом закономерность широтная: '
        'чем дальше на север, тем холоднее, на юг — теплее.\n\n'

        '<b>3. Минимальное количество осадков</b> '
        'В нашей стране наблюдается в Астраханской области и Республике '
        'Калмыкия, максимальное регистрируется в районе города Сочи. Общая '
        'закономерность в распределении осадков в нашей стране сводится к '
        'тому, что чем дальше населенный пункт находится от побережья '
        'Атлантического или Тихого океана, тем меньше там осадков.\n\n'

        '<b>4. Континентальность климата</b> '
        'В нашей стране возрастает при движении с запада на восток и '
        'выражается в уменьшении годового количества осадков и увеличении '
        'годовой амплитуды температуры воздуха. Чем восточнее, тем зима '
        'холоднее, а лето жарче.\n\n'

        '<b>5. Лесистость</b> '
        '— степень облесенности территории, определяемая отношением площади '
        'покрытых лесной растительностью земель к её общей площади, '
        'выражаемая в процентах. Лесистость территории нашей страны '
        'уменьшается с севера на юг и с востока на запад.'
    ),
    'task_3_1': (
        'Вопрос 1.\nРасположите перечисленные регионы России по степени '
        'увеличения естественного плодородия почв на их территории, начиная '
        'с региона, почвы которого наименее плодородны.\n\n'
        '<b>Запишите получившуюся последовательность цифр без пробелов</b> '
        '<b>и запятых.</b> \n\n'
        '1) Республика Карелия\n'
        '2) Ямало-Ненецкий АО\n'
        '3) Ставропольский край\n'
    ),
    'task_3_2': (
        'Вопрос 2.\nРасположите перечисленные ниже города России в порядке '
        'повышения средней многолетней температуры воздуха самого холодного '
        'месяца, начиная с города с самой низкой температурой воздуха.\n\n'
        '<b>Запишите получившуюся последовательность цифр без пробелов и '
        'запятых.</b>\n\n'
        '1) Иркутск\n'
        '2) Казань\n'
        '3) Калининград\n'
    ),
    'task_3_3': (
        'Вопрос 3.\nРасположите перечисленные ниже города России в порядке '
        'увеличения среднегодового количества атмосферных осадков, выпадающих '
        'в них, начиная с города с наименьшим количеством осадков.\n\n'
        '<b>Запишите получившуюся последовательность цифр без пробелов и '
        'запятых.</b>\n\n'
        '1) Калининград\n'
        '2) Москва\n'
        '3) Элиста\n'
    ),
    'task_3_4': (
        'Вопрос 4.\nКомфортность климатических условий для жизни людей '
        'во многом определяется степенью континентальности климата. '
        'Расположите перечисленные города России в порядке увеличения '
        'степени континентальности климата в них, начиная с города с '
        'наименее континентальным климатом.\n\n'
        '<b>Запишите получившуюся последовательность цифр без пробелов '
        'и запятых.</b>\n\n'
        '1) Абакан\n'
        '2) Тюмень\n'
        '3) Казань\n'
    ),
    'task_3_5': (
        'Вопрос 5.\nРасположите регионы России по степени увеличения '
        'лесистости территории (начиная с региона с самой маленькой '
        'лесистостью).\n\n'
        '<b>Запишите получившуюся последовательность цифр без пробелов '
        'и запятых.</b>\n\n'
        '1) Оренбургская область\n'
        '2) Смоленская область\n'
        '3) Республика Коми\n'
    ),
    'task_5_1': ('Вопрос 1.\nКакой из перечисленных населённых пунктов, '
                 'показанных на карте, находится в зоне действия '
                 '<b>циклона?</b>\n\n'
                 '1) Тикси\n'
                 '2) Норильск\n'
                 '3) Петропавловск-Камчатский\n'
                 '4) Анадырь'),
    'task_5_2': ('Вопрос 2.\nКакой из перечисленных населённых пунктов, '
                 'показанных на карте, находится в зоне действия '
                 '<b>антициклона?</b>\n\n'
                 '1) Охотск\n'
                 '2) Алдан\n'
                 '3) Находка\n'
                 '4) Хатанга'),
    'task_5_3': ('Вопрос 3.\nКакой из перечисленных населённых пунктов, '
                 'показанных на карте, находится в зоне действия '
                 '<b>циклона?</b>\n\n'
                 '1) Покровск\n'
                 '2) Томмот\n'
                 '3) Туруханск\n'
                 '4) Северобайкальск'),
    'task_5_4': ('Вопрос 4.\nКакой из перечисленных населённых пунктов, '
                 'показанных на карте, находится в зоне действия '
                 '<b>антициклона?</b>\n\n'
                 '1) Приобье\n'
                 '2) Горно-Алтайск\n'
                 '3) Нижневартовск\n'
                 '4) Екатеринбург'),
    'task_5_5': ('Вопрос 5.\nКакой из перечисленных населённых пунктов, '
                 'показанных на карте, находится в зоне действия '
                 '<b>циклона?</b>\n\n'
                 '1) Красноярск\n'
                 '2) Тобольск\n'
                 '3) Горно-Алтайск\n'
                 '4) Барнаул'),
    'task_6_1': ('Вопрос 1.\nКарта погоды составлена на 7 сентября. '
                 'В каком из перечисленных населённых пунктов, '
                 'показанных на карте, на следующий день наиболее '
                 'вероятно существенное <b>потепление?</b>\n\n'
                 '1) Якутск\n'
                 '2) Благовещенск\n'
                 '3) Хабаровск\n'
                 '4) Дежнево'),
    'task_6_2': ('Вопрос 2.\nКарта погоды составлена на 19 сентября. '
                 'В каком из перечисленных городов, '
                 'показанных на карте, на следующий день наиболее '
                 'вероятно существенное <b>потепление?</b>\n\n'
                 '1) Арсеньев\n'
                 '2) Хабаровск\n'
                 '3) Красноярск\n'
                 '4) Ленск'),
    'task_6_3': ('Вопрос 3.\nКарта погоды составлена на 29 сентября. '
                 'В каком из перечисленных населённых пунктов, '
                 'показанных на карте, на следующий день наиболее '
                 'вероятно существенное <b>похолодание?</b>\n\n'
                 '1) Усть-Кут\n'
                 '2) Петропавловск-Камчатский\n'
                 '3) Светлая\n'
                 '4) Иркутск'),
    'task_6_4': ('Вопрос 4.\nКарта погоды составлена на 28 марта. '
                 'В каком из перечисленных населённых пунктов, '
                 'показанных на карте, на следующий день наиболее '
                 'вероятно существенное <b>потепление?</b>\n\n'
                 '1) Ревда\n'
                 '2) Колпашево\n'
                 '3) Новосибирск\n'
                 '4) Енисейск'),
    'task_6_5': ('Вопрос 5.\nКарта погоды составлена на 28 марта. '
                 'В каком из перечисленных населённых пунктов, '
                 'показанных на карте, на следующий день наиболее '
                 'вероятно существенное <b>похолодание?</b>\n\n'
                 '1) Колпашево\n'
                 '2) Пермь\n'
                 '3) Енисейск\n'
                 '4) Воркута'),
    'task_8': ('‼️ Для успешного выполнения данного задания необходимо '
               'знать следующую закономерность — при горизонтальном '
               'залегании пород самые древние породы залегают ↓внизу↓, '
               'самые молодые - 🔝вверху🔝.'),
    'task_8_1': ('Вопрос 1. Во время экскурсии учащиеся сделали '
                 'схематическую зарисовку залегания горных пород на '
                 'обрыве в карьере.\n'
                 'Расположите показанные на рисунке слои горных пород '
                 'в порядке увеличения их возраста (от самого молодого '
                 'до самого древнего.\n\n'
                 '<b>Запишите получившуюся последовательность цифр без '
                 'пробелов и запятых.</b>\n\n'
                 '1) Песок\n'
                 '2) Глина\n'
                 '3) Известняк'),
    'task_8_2': ('Вопрос 2. Во время экскурсии учащиеся сделали '
                 'схематическую зарисовку залегания горных пород на '
                 'обрыве в карьере.\n'
                 'Расположите показанные на рисунке слои горных пород '
                 'в порядке увеличения их возраста (от самого молодого '
                 'до самого древнего.\n\n'
                 '<b>Запишите получившуюся последовательность цифр без '
                 'пробелов и запятых.</b>\n\n'
                 '1) Глина\n'
                 '2) Песчаник\n'
                 '3) Мелкий песок'),
    'task_8_3': ('Вопрос 3. Во время экскурсии учащиеся сделали '
                 'схематическую зарисовку залегания горных пород на '
                 'обрыве в карьере.\n'
                 'Расположите показанные на рисунке слои горных пород '
                 'в порядке увеличения их возраста (от самого молодого '
                 'до самого древнего.\n\n'
                 '<b>Запишите получившуюся последовательность цифр без '
                 'пробелов и запятых.</b>\n\n'
                 '1) Суглинок с валунами\n'
                 '2) Песок\n'
                 '3) Глина'),
    'task_8_4': ('Вопрос 4. Во время экскурсии учащиеся сделали '
                 'схематическую зарисовку залегания горных пород на '
                 'обрыве в карьере.\n'
                 'Расположите показанные на рисунке слои горных пород '
                 'в порядке увеличения их возраста (от самого молодого '
                 'до самого древнего.\n\n'
                 '<b>Запишите получившуюся последовательность цифр без '
                 'пробелов и запятых.</b>\n\n'
                 '1) Серый слоистый песчаник\n'
                 '2) Известняк\n'
                 '3) Суглинок'),
    'task_8_5': ('Вопрос 5. Во время экскурсии учащиеся сделали '
                 'схематическую зарисовку залегания горных пород на '
                 'обрыве в карьере.\n'
                 'Расположите показанные на рисунке слои горных пород '
                 'в порядке увеличения их возраста (от самого молодого '
                 'до самого древнего.\n\n'
                 '<b>Запишите получившуюся последовательность цифр без '
                 'пробелов и запятых.</b>\n\n'
                 '1) Известняк\n'
                 '2) Суглинок с валунами\n'
                 '3) Кварцит'),


})

CORRECT_ANSWERS = frozendict({
    'correct_answer_2_1': ['Норвегия', 'Норвегией'],
    'correct_answer_2_2': ['Монголией', 'Монголия'],
    'correct_answer_2_3': ['Казахстан', 'Казахстаном'],
    'correct_answer_2_4': ['Китаем', 'Китай'],
    'correct_answer_2_5': ['США'],
    'correct_answer_3_1': ['213'],
    'correct_answer_3_2': ['123'],
    'correct_answer_3_3': ['321'],
    'correct_answer_3_4': ['321'],
    'correct_answer_3_5': ['123'],
    'correct_answer_5_1': ['3'],
    'correct_answer_5_2': ['2'],
    'correct_answer_5_3': ['3'],
    'correct_answer_5_4': ['2'],
    'correct_answer_5_5': ['2'],
    'correct_answer_6_1': ['3'],
    'correct_answer_6_2': ['4'],
    'correct_answer_6_3': ['3'],
    'correct_answer_6_4': ['4'],
    'correct_answer_6_5': ['2'],
    'correct_answer_8_1': ['123'],
    'correct_answer_8_2': ['321'],
    'correct_answer_8_3': ['123'],
    'correct_answer_8_4': ['321'],
    'correct_answer_8_5': ['213'],

})
