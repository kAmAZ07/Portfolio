# Импортируем библиотеки
import sqlite3 #Библиотека для соединения с Базой данных
import  datetime
from telebot import * #Библиотека для соединения с Telegram
from telebot.types import InlineKeyboardButton, LabeledPrice, ShippingOption, ShippingQuery, Message, PreCheckoutQuery, SuccessfulPayment, OrderInfo #Библиотеки для создания кнопок и оплаты

#Подсоединяем бота с помощью токена от BotFather
bot = telebot.TeleBot('5656237171:AAHstiKeRWN88t1874TtAhXRzEalLw6xrSc')
name = ''

#Прописываем реакцию на текстовые сообщения
@bot.message_handler(content_types=['text'])
def start(message):
    global msg
    text = message.text.lower()
    # Прописываем действия при получении стартового сообщения
    if text == '/start':
        # Соединяемся с Базой данных
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        # Получаем id чата администратора
        cur.execute(
            f'SELECT ID_of_chat FROM admin;')
        admin = cur.fetchone()
        admin = int(admin[0])
        # Проверяю есть ли id начинающего работу с ботом в Базе данных
        cur.execute(
            f'SELECT User_id FROM Customers;')
        itog = cur.fetchall()
        itog = [i[0] for i in itog]
        #Если id пишущего /start совпадает с id администратора
        if message.from_user.id == admin:
            bot.send_message(message.from_user.id,
                             'Приветствуем Вас, Администратор! От меня Вы будете получать сообщения о поступивших заказах и подтверждения оплаты.')
        # Если id есть в Базе данных, приветствуем по имени и сразу предлагаем начать заказывать
        elif message.from_user.id in itog:
            cur.execute(
                f'SELECT Name FROM Customers WHERE User_id = "{message.from_user.id}";')
            name = cur.fetchone()
            name = name[0]
            print('Зашёл пользователь ' + name + '. id- ' + str(message.from_user.id))
            question = 'Здравствуйте, ' + name + '! Чтобы посмотреть список пицц нажмите кнопку Пиццы..'
            keyboard = types.InlineKeyboardMarkup()  # Создание клавиатуры с кнопками
            key_listofpizzas = types.InlineKeyboardButton(text='Пиццы', callback_data='pizzas')  # кнопка «список пицц»
            keyboard.add(key_listofpizzas)  # добавляем кнопку в клавиатуру
            msg = bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
            msg = msg.id
        #Если id неизвестно боту, то пользователь начинает проходить регистрацию
        else:
            bot.send_message(message.from_user.id, "Здравствуйте, как Вас зовут?")
            #Перенаправление к функции добавления пользователя в Базу данных
            bot.register_next_step_handler(message, get_name)
            msg = 1

    # Реакция на сообщение /help
    if text == '/help':
        bot.send_message(message.from_user.id, "Нашим ботом очень легко пользоваться. Как говорят в России: «Как 2"
                                               " пальца…». \n\nНапишите:\n\n'/listofpizzas', чтобы"
                                               " посмотреть список доступных пицц. Нажмите на интересующую Вас пиццу, чтобы посмотреть информацию о ней и добавить её в корзину. После нажатия на название пиццы может быть небольшая задержка."
                                               "\n\n'/cart', чтобы посмотреть, что у вас выбрано, там же Вы можете закончить заказ.")


# Записывание нового пользователя в Базу данных
def get_name(message):  # получаем фамилию
    global name, user_id, msg
    name = message.text
    user_id = message.from_user.id
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    #Новая запись в Базе данных
    cur.execute(
        f'INSERT INTO Customers(Name, User_id) VALUES("{name}", "{user_id}");')
    sqlite_connection.commit()
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_listofpizzas = types.InlineKeyboardButton(text='Пиццы', callback_data='pizzas')  # кнопка «список пицц»
    keyboard.add(key_listofpizzas)  # добавляем кнопку в клавиатуру
    question = 'Очень приятно, я - ПиццаБот, и я помогу Вам заказать пиццу, нажмите кнопку Пиццы, чтобы посмотреть ассортимент'
    msg = bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    msg = msg.id


# Реакция на получение адреса от пользователя
def get_address(message):
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'SELECT ID_of_chat FROM admin;')
    admin = cur.fetchone()
    admin = int(admin[0])
    cur.execute(
        f'SELECT Name FROM Customers WHERE User_id="{message.chat.id}";')
    Name = cur.fetchone()
    Name = Name[0]
    cur.execute(
        f'SELECT Phone FROM admin;')
    phone = cur.fetchone()
    phone = phone[0]
    #Информирование администратора
    bot.send_message(admin, 'Оплачен заказ от ' + Name + ', номер заказа: ' + str(message.chat.id) + '.\nАдрес: ' + message.text + '\nВремя: ' + datetime.now().strftime('%H:%M:%S %d.%m.%Y'))
    # Ответ пользователю
    bot.send_message(message.chat.id,
                     'Ваш заказ, номер ' + str(message.chat.id) + ', в пути. В случае возникновения вопросов по поводу Вашего заказа звоните в службу поддержки\nНомер: ' + phone + '\nНомер Вашего заказа: ' + str(message.chat.id) + '\nЧтобы сделать новый заказ напишите заново команду /start.')


# Реакция на выбор пользователем адреса для самовывоза
def get_pick_up(message):
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'SELECT ID_of_chat FROM admin;')
    admin = cur.fetchone()
    admin = int(admin[0])
    cur.execute(
        f'SELECT Name FROM Customers WHERE User_id="{message.chat.id}";')
    Name = cur.fetchone()
    Name = Name[0]
    cur.execute(
        f'SELECT Phone FROM admin;')
    phone = cur.fetchone()
    phone = phone[0]
    # Информирование администратора
    bot.send_message(admin, 'Оплачен заказ от ' + Name + ', номер: ' + str(message.chat.id) + '.\nСамовывоз по адресу: ' + message.text + '\nВремя: ' + datetime.now().strftime('%H:%M:%S %d.%m.%Y'))
    # Ответ пользователю
    bot.send_message(message.chat.id,
                     'Ваш заказ, номер ' + str(message.chat.id) + ', будет Вас ждать в выбранном Вами ресторане. В случае возникновения вопросов по поводу Вашего заказа звоните в службу поддержки\nНомер: ' + phone + '\nЧтобы сделать новый заказ напишите заново команду /start.')


# Реакция бота на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call, crt=[], summ=[]):
    global m, msg
    #Создаём переменную с текущим временем
    a = datetime.now().strftime('%H:%M:%S %d.%m.%Y')  # Сделано, чтобы узнать во сколько регистрируется пользователь
    if call.data == "pizzas":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.delete_message(call.message.chat.id, msg)# Удаляем предыдущее сообщение, чтобы они не накапливались в чате с пользователем
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT PizzaName FROM Pizza;')
        pizza = cur.fetchall()
        pizza = [i[0] for i in pizza]
        button_list = []
        for product in pizza:
            text = f'{product}'
            button_list.append(
                [InlineKeyboardButton(text, callback_data=f'id_{product}')]
            )
        button_list.append(
            [InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')]
        )
        keyboard = types.InlineKeyboardMarkup(button_list)
        m = bot.send_message(call.message.chat.id, text='Выберите пиццу:', reply_markup=keyboard)
        m = m.id
    elif call.data == "cart":
        txt = ''
        button_list = []
        bot.delete_message(call.message.chat.id, msg)
        for i in crt:
            txt += 'Пицца ' + i + ' рублей\n'
        s = 0
        for i in summ:
            s += int(i)
        txt += '\nИтого к оплате: ' + str(s) + ' рублей'
        for i in crt:
            i = i.split(' ')
            text = 'Удалить пиццу ' + i[0] + ' из корзины'
            button_list.append(
                [InlineKeyboardButton(text, callback_data=f'del_{i[0]}')]
            )
        button_list.append(
            [InlineKeyboardButton(text='Очистить корзину', callback_data='clear')]
        )
        button_list.append(
            [InlineKeyboardButton(text='Оформить заказ', callback_data='Order')]
        )
        button_list.append(
            [InlineKeyboardButton(text='<- К меню пицц', callback_data='pizzas')]
        )
        keyboard = types.InlineKeyboardMarkup(button_list)
        msg = bot.send_message(call.message.chat.id, text=txt, reply_markup=keyboard)
        msg = msg.id
    elif 'id' in call.data:
        bot.delete_message(call.message.chat.id, m)
        b_l = []
        product = call.data.split('_')
        product = product[1]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT image FROM Pizza WHERE PizzaName="{product}";')
        img = cur.fetchone()
        img = img[0]
        img = open(img, 'rb')
        cur.execute(
            f'SELECT caption FROM Pizza WHERE PizzaName="{product}";')
        cap = cur.fetchone()
        cap = cap[0]
        cur.execute(
            f'SELECT TwentyFive FROM Pizza WHERE PizzaName="{product}";')
        tfcm = cur.fetchone()
        tfcm = tfcm[0]
        text1 = f'{tfcm}руб  (25 см)'
        b_l.append(
            [InlineKeyboardButton(text1, callback_data=f'25_{product}')]
        )
        cur.execute(
            f'SELECT Thirty FROM Pizza WHERE PizzaName="{product}";')
        thcm = cur.fetchone()
        thcm = thcm[0]
        text2 = f'{thcm}руб  (30 см)'
        b_l.append(
            [InlineKeyboardButton(text2, callback_data=f'30_{product}')]
        )
        cur.execute(
            f'SELECT ThirtyFive FROM Pizza WHERE PizzaName="{product}";')
        thfcm = cur.fetchone()
        thfcm = thfcm[0]
        text3 = f'{thfcm}руб  (35 см)'
        b_l.append(
            [InlineKeyboardButton(text3, callback_data=f'35_{product}')]
        )
        text4 = '<- Назад к списку'
        b_l.append(
            [InlineKeyboardButton(text4, callback_data='pizzas')]
        )
        keyboard1 = types.InlineKeyboardMarkup(b_l)
        msg = bot.send_photo(call.message.chat.id, img, caption=cap, reply_markup=keyboard1)
        msg = msg.id
    elif '25' in call.data:
        bot.delete_message(call.message.chat.id, msg)
        product = call.data.split('_')
        product = product[1]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT TwentyFive FROM Pizza WHERE PizzaName="{product}";')
        tfcm = cur.fetchone()
        tfcm = int(tfcm[0])
        summ.append(str(tfcm))
        print(summ)
        current = product + ' ' + str(tfcm)
        crt.append(current)
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb_cart = types.InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 25 см за ' + str(
            tfcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        msg = bot.send_message(call.message.chat.id, text, reply_markup=kb)
        msg = msg.id
    elif '30' in call.data:
        bot.delete_message(call.message.chat.id, msg)
        product = call.data.split('_')
        product = product[1]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Thirty FROM Pizza WHERE PizzaName="{product}";')
        thcm = cur.fetchone()
        thcm = int(thcm[0])
        summ.append(str(thcm))
        current = product + ' ' + str(thcm)
        crt.append(current)
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb_cart = types.InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 30 см за ' + str(
            thcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        msg = bot.send_message(call.message.chat.id, text, reply_markup=kb)
        msg = msg.id
    elif '35' in call.data:
        bot.delete_message(call.message.chat.id, msg)
        product = call.data.split('_')
        product = product[1]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT ThirtyFive FROM Pizza WHERE PizzaName="{product}";')
        thfcm = cur.fetchone()
        thfcm = int(thfcm[0])
        summ.append(str(thfcm))
        current = product + ' ' + str(thfcm)
        crt.append(current)
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb_cart = types.InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 35 см за ' + str(
            thfcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        msg = bot.send_message(call.message.chat.id, text, reply_markup=kb)
        msg = msg.id
    elif call.data == "clear":
        bot.delete_message(call.message.chat.id, msg)
        crt = []
        summ = []
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb.add(kb_bck)
        text = 'Корзина успешно очищена'
        msg = bot.send_message(call.message.chat.id, text, reply_markup=kb)
    elif call.data == "Order":
        bot.delete_message(call.message.chat.id, msg)
        s = 0
        bot.send_message(call.message.chat.id, 'Подождите пожалуйста. Ваш заказ обрабатывается.')
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT ID_of_chat FROM admin;')
        admin = cur.fetchone()
        admin = int(admin[0])
        cur.execute(
            f'SELECT Name FROM Customers WHERE User_id="{call.message.chat.id}";')
        Name = cur.fetchone()
        Name = Name[0]
        for i in summ:
            s += int(i)
        button_list = []
        button_list.append(
            [InlineKeyboardButton(text='Подтвердить заказ', callback_data=f'ok_{call.message.chat.id}_{s}')]
        )
        button_list.append(
            [InlineKeyboardButton(text='Невозможно оформить', callback_data=f'wrong_{call.message.chat.id}_{s}')]
        )
        button_list.append(
            [InlineKeyboardButton(text='Отсутствует пицца', callback_data=f'absent_{call.message.chat.id}_{s}')]
        )
        keyboard = types.InlineKeyboardMarkup(button_list)
        bot.send_message(admin,
                         'Получен заказ от ' + str(Name) + '. Номер заказа: ' + str(
                             call.message.chat.id) + '\nЗаказ:\n' + '\n'.join(
                             [str(i) for i in crt]) + '\n\nСумма заказа: ' + str(s) + ' руб\n' + 'Время заказа: ' + a, reply_markup=keyboard)
    elif 'ok' in call.data:
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Pay_Token FROM Token;')
        token = cur.fetchone()
        token = token[0]
        print(token)
        a = call.data.split('_')
        cid = int(a[1])
        price = int(a[2]) * 100
        PRICES = [
            LabeledPrice(label='Ваш заказ', amount=price)
        ]
        bot.send_invoice(cid,
                         title='Ваш заказ',
                         description='\n'.join([str(i) for i in crt]),
                         provider_token=token,
                         currency='rub',
                         need_phone_number=True,
                         prices=PRICES,
                         start_parameter='example',
                         invoice_payload='some_invoice')
    elif 'absent' in call.data:
        a = call.data.split('_')
        cid = int(a[1])
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT ID_of_chat FROM admin;')
        admin = cur.fetchone()
        admin = int(admin[0])
        button_list = []
        for i in crt:
            item = i.split(' ')
            i = item[0]
            button_list.append(
                [InlineKeyboardButton(i, callback_data=f'ab_{i}_{cid}')]
            )
        keyboard = types.InlineKeyboardMarkup(button_list)
        bot.send_message(admin, text='Выберите отсутсвующую пиццу', reply_markup=keyboard)
    elif 'wrong' in call.data:
        a = call.data.split('_')
        cid = int(a[1])
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Phone FROM admin;')
        phone = cur.fetchone()
        phone = phone[0]
        bot.send_message(cid,
                         'К сожалению, невозможно в данный момент оформить заказ. По всем вопросам звоните: ' + phone)
    elif call.data == "delivery":
        bot.send_message(call.message.chat.id, 'Напишите свой адрес')
        bot.register_next_step_handler(call.message, get_address)
        crt = []
    elif call.data == "pick_up":
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Address FROM Shops;')
        shops = cur.fetchall()
        shops = [i[0] for i in shops]
        bot.send_message(call.message.chat.id,
                         'Вот список наших магазинов, напишите адрес того, из которого хотите забрать.\n' + '\n'.join(
                             [str(i) for i in shops]))
        bot.register_next_step_handler(call.message, get_pick_up)
        crt = []
    elif 'ab' in call.data:
        a = call.data.split('_')
        cid = int(a[2])
        apizza = a[1]
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb_cart = types.InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')
        kb.add(kb_cart, kb_bck)
        for i in crt:
            l = i.split(' ')
            try:
                s = int(l[1])
            except ValueError:
                s = l[2]
            print(summ, s, l)
            if apizza in i:
                crt.remove(i)
                summ.remove(str(s))
            else:
                continue
        msg = bot.send_message(cid,
                               'К сожалению, пицца ' + apizza + ' отсутсвует на данный момент. Пожалуйста выберите вместо неё другую.',
                               reply_markup=kb)
        msg = msg.id
    elif 'del' in call.data:
        bot.delete_message(call.message.chat.id, msg)
        a = call.data.split('_')
        dpizza = a[1]
        for i in crt:
            l = i.split(' ')
            try:
                s = int(l[1])
            except ValueError:
                s = l[2]
            if dpizza in i:
                crt.remove(i)
                summ.remove(str(s))
                break
            else:
                continue
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb_bck = types.InlineKeyboardButton(text='Меню пицц', callback_data='pizzas')
        kb_cart = types.InlineKeyboardButton(text='Ваша Корзина', callback_data='cart')
        kb.add(kb_cart, kb_bck)
        msg = bot.send_message(call.message.chat.id, 'Успешно удалена из корзины пицца ' + dpizza, reply_markup=kb)
        msg = msg.id


@bot.callback_query_handler(lambda q: True)
def shipping_process(shipping_query: ShippingQuery):
    Shipping_option = ShippingOption(
        id='deliver',
        title='Доставка по адресу'
    )
    Pick_up_shipping = ShippingOption(
        id='pickup',
        title='Самовывоз'
    )
    shipping_options = [Shipping_option, Pick_up_shipping]
    bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@bot.pre_checkout_query_handler(lambda q: True)
def checkout_process(pre_checkout_query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb_ok = types.InlineKeyboardButton(text='Доставка', callback_data=f'delivery')
    kb_wr = types.InlineKeyboardButton(text='Самовывоз', callback_data=f'pick_up')
    kb.add(kb_ok, kb_wr)
    bot.send_message(message.chat.id, 'Спасибо за заказ, выберите способ получения заказа.', reply_markup=kb)


bot.polling(none_stop=True, interval=0)
