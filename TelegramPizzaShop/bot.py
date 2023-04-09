# Импортируем библиотеки
import sqlite3  # Библиотека для соединения с Базой данных
from datetime import datetime
import types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import *  # Библиотека для соединения с Telegram
from aiogram.types import InlineKeyboardButton, LabeledPrice, ShippingOption, ShippingQuery, Message, \
    InlineKeyboardMarkup  # Библиотеки для создания кнопок и оплаты
from aiogram.dispatcher.filters.state import State, StatesGroup

# Подсоединяем бота с помощью токена от BotFather
bot = Bot(token='5656237171:AAHstiKeRWN88t1874TtAhXRzEalLw6xrSc')
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    addres = State()
    pick_up_addres = State()
    name = State()


# Прописываем реакцию на текстовые сообщения
@dp.message_handler(content_types=['text'])
async def start(message: types.Message):
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
        # Если id пишущего /start совпадает с id администратора
        if message.from_user.id == admin:
            await bot.send_message(message.from_user.id,
                                   'Приветствуем Вас, Администратор! От меня Вы будете получать сообщения о поступивших заказах и подтверждения оплаты.')
        # Если id есть в Базе данных, приветствуем по имени и сразу предлагаем начать заказывать
        elif message.from_user.id in itog:
            cur.execute(
                f'SELECT Name FROM Customers WHERE User_id = "{message.from_user.id}";')
            name = cur.fetchone()
            cur.execute(
                f'UPDATE Customers SET Cart = NULL WHERE User_id = "{message.from_user.id}";')
            sqlite_connection.commit()
            name = name[0]
            print(datetime.now().strftime('%H:%M:%S %d.%m.%Y') + ' Зашёл пользователь ' + name + '. id- ' + str(
                message.from_user.id))
            question = 'Здравствуйте, ' + name + '! Чтобы посмотреть список пицц нажмите кнопку Пиццы.'
            keyboard = types.InlineKeyboardMarkup()  # Создание клавиатуры с кнопками
            key_listofpizzas = types.InlineKeyboardButton(text='🍕 Пиццы 🍕',
                                                          callback_data='btn_pizzas')  # кнопка «список пицц»
            keyboard.add(key_listofpizzas)  # добавляем кнопку в клавиатуру
            await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        # Если id неизвестно боту, то пользователь начинает проходить регистрацию
        else:
            await Form.name.set()
            await bot.send_message(message.from_user.id, "Здравствуйте, как Вас зовут?")
            # Перенаправление к функции добавления пользователя в Базу данных

    # Реакция на сообщение /help
    if text == '/help':
        await bot.send_message(message.from_user.id,
                               "Нашим ботом очень легко пользоваться. Как говорят в России: «Как 2"
                               " пальца…». \n\nНапишите:\n\n'/start', чтобы"
                               " посмотреть список доступных пицц. Нажмите на интересующую Вас пиццу, чтобы посмотреть информацию о ней и добавить её в корзину. После нажатия на название пиццы может быть небольшая задержка."
                               "\n\nНажмите /cart, чтобы посмотреть, что у вас выбрано, там же Вы можете оформить заказ.")


# Записывание нового пользователя в Базу данных
@dp.message_handler(state=Form.name)
async def get_name(message: types.Message, state: FSMContext):  # получаем фамилию
    await state.update_data(name=message.text)
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    # Новая запись в Базе данных
    cur.execute(
        f'INSERT INTO Customers(Name, User_id) VALUES("{message.text}", "{message.from_user.id}");')
    sqlite_connection.commit()
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_listofpizzas = types.InlineKeyboardButton(text='🍕 Пиццы 🍕', callback_data='btn_pizzas')  # кнопка «список пицц»
    keyboard.add(key_listofpizzas)  # добавляем кнопку в клавиатуру
    question = 'Очень приятно, я - ПиццаБот, и я помогу Вам заказать пиццу, нажмите кнопку Пиццы, чтобы посмотреть ассортимент'
    await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    print(
        datetime.now().strftime('%H:%M:%S %d.%m.%Y') + ' Зарегистрирован пользователь ' + message.text + '. id: ' + str(
            message.from_user.id))
    await state.finish()


# Реакция на получение адреса от пользователя
@dp.message_handler(state=Form.addres)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'SELECT ID_of_chat FROM admin;')
    admin = cur.fetchone()
    admin = int(admin[0])
    cur.execute(
        f'SELECT Name FROM Customers WHERE User_id="{message.chat.id}";')
    name = cur.fetchone()
    name = name[0]
    cur.execute(
        f'SELECT Phone FROM admin;')
    phone = cur.fetchone()
    phone = phone[0]
    now = datetime.now()
    # Информирование администратора
    await bot.send_message(admin, 'Оплачен заказ от ' + name + ', номер заказа: ' + str(
        message.chat.id) + '.\nАдрес: ' + message.text + '\nВремя: ' + now.strftime('%H:%M:%S %d.%m.%Y'))
    # Ответ пользователю
    await bot.send_message(message.from_user.id,
                           'Ваш заказ, номер ' + str(
                               message.chat.id) + ', в пути. В случае возникновения вопросов по поводу Вашего заказа звоните в службу поддержки\nНомер: ' + phone + '\nНомер Вашего заказа: ' + str(
                               message.chat.id) + '\nЧтобы сделать новый заказ напишите заново команду /start.')
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'UPDATE Customers SET Cart = NULL WHERE User_id = "{message.chat.id}";')
    sqlite_connection.commit()
    print('Закрытие сеанса ' + now.strftime('%H:%M:%S %d.%m.%Y') + '. Пользователь ' + name + '. id: ' + str(
        message.chat.id))
    await state.finish()


# Реакция на выбор пользователем адреса для самовывоза
@dp.message_handler(state=Form.pick_up_addres)
async def get_pick_up(message: types.Message, state: FSMContext):
    await state.update_data(pick_up_address=message.text)
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'SELECT ID_of_chat FROM admin;')
    admin = cur.fetchone()
    admin = int(admin[0])
    cur.execute(
        f'SELECT Name FROM Customers WHERE User_id="{message.chat.id}";')
    name = cur.fetchone()
    name = name[0]
    cur.execute(
        f'SELECT Phone FROM admin;')
    phone = cur.fetchone()
    phone = phone[0]
    now = datetime.now()
    # Информирование администратора
    await bot.send_message(admin, 'Оплачен заказ от ' + name + ', номер: ' + str(
        message.chat.id) + '.\nСамовывоз по адресу: ' + message.text + '\nВремя: ' + now.strftime(
        '%H:%M:%S %d.%m.%Y'))
    # Ответ пользователю
    await bot.send_message(message.chat.id,
                           'Ваш заказ, номер ' + str(
                               message.chat.id) + ', будет Вас ждать в выбранном Вами ресторане. В случае возникновения вопросов по поводу Вашего заказа звоните в службу поддержки\nНомер: ' + phone + '\nЧтобы сделать новый заказ напишите заново команду /start.')
    sqlite_connection = sqlite3.connect('Customers')
    cur = sqlite_connection.cursor()
    cur.execute(
        f'UPDATE Customers SET Cart = NULL WHERE User_id = "{message.chat.id}";')
    sqlite_connection.commit()
    print('Закрытие сеанса ' + now.strftime('%H:%M:%S %d.%m.%Y') + '. Пользователь ' + name + '. id: ' + str(
        message.chat.id))
    await state.finish()


# Реакция бота на кнопки
@dp.callback_query_handler(lambda call: 'btn' in call.data)
async def callback_worker(call: types.CallbackQuery):
    if call.data == "btn_pizzas":  # call.data это callback_data, которую мы указали при объявлении кнопки
        await call.message.delete()  # Удаляем предыдущее сообщение, чтобы они не накапливались в чате с пользователем
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT PizzaName FROM Pizza;')
        pizza = cur.fetchall()
        pizza = [i[0] for i in pizza]
        button_list = []
        for product in pizza:
            text = f'🍕 {product}'
            button_list.append(
                [InlineKeyboardButton(text, callback_data=f'btn_id_{product}')]
            )
        button_list.append(
            [InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')]
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=button_list)
        await bot.send_message(call.message.chat.id, text='Выберите пиццу:', reply_markup=keyboard)
    elif call.data == "btn_cart":
        summ = 0
        await call.message.delete()
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        crt = cur.fetchone()
        if None in crt:
            keyboard = types.InlineKeyboardMarkup()
            key_listofpizzas = types.InlineKeyboardButton(text='🍕 Пиццы 🍕',
                                                          callback_data='btn_pizzas')
            keyboard.add(key_listofpizzas)
            question = 'К сожалению, Ваша корзина пока пуста. Добавьте в неё пиццу, чтобы сделать заказ'
            await bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
        else:
            crt = list(crt)[0].split('_')[:-1]
            for i in crt:
                summ += int(i.split(' ')[-1])
            txt = ''
            button_list = []
            for i in crt:
                txt += 'Пицца ' + i + ' рублей\n'
            txt += '\nИтого к оплате: ' + str(summ) + ' рублей'
            for i in crt:
                i = ' '.join(i.split(' ')[:-1])
                text = '❌ Удалить пиццу ' + i + ' из корзины ❌'
                button_list.append(
                    [InlineKeyboardButton(text, callback_data=f'btn_del_{i}')]
                )
            button_list.append(
                [InlineKeyboardButton(text='🗑️ Очистить корзину', callback_data='btn_clear')]
            )
            button_list.append(
                [InlineKeyboardButton(text='📝 Оформить заказ', callback_data=F'btn_Order_{summ}')]
            )
            button_list.append(
                [InlineKeyboardButton(text='<- К меню пицц 🍕', callback_data='btn_pizzas')]
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=button_list)
            await bot.send_message(call.message.chat.id, text=txt, reply_markup=keyboard)
    elif 'id' in call.data:
        await call.message.delete()
        b_l = []
        product = call.data.split('_')
        product = product[2]
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
            [InlineKeyboardButton(text1, callback_data=f'btn_25_{product}')]
        )
        cur.execute(
            f'SELECT Thirty FROM Pizza WHERE PizzaName="{product}";')
        thcm = cur.fetchone()
        thcm = thcm[0]
        text2 = f'{thcm}руб  (30 см)'
        b_l.append(
            [InlineKeyboardButton(text2, callback_data=f'btn_30_{product}')]
        )
        cur.execute(
            f'SELECT ThirtyFive FROM Pizza WHERE PizzaName="{product}";')
        thfcm = cur.fetchone()
        thfcm = thfcm[0]
        text3 = f'{thfcm}руб  (35 см)'
        b_l.append(
            [InlineKeyboardButton(text3, callback_data=f'btn_35_{product}')]
        )
        text4 = '<- Назад к списку'
        b_l.append(
            [InlineKeyboardButton(text4, callback_data='btn_pizzas')]
        )
        keyboard1 = InlineKeyboardMarkup(inline_keyboard=b_l)
        await bot.send_photo(call.message.chat.id, img, caption=cap, reply_markup=keyboard1)
    elif '25' in call.data:
        await call.message.delete()
        product = call.data.split('_')
        product = product[2]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT TwentyFive FROM Pizza WHERE PizzaName="{product}";')
        tfcm = cur.fetchone()
        tfcm = int(tfcm[0])
        current = product + ' ' + str(tfcm) + '_'
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        cart1 = cur.fetchone()
        if None in cart1:
            crt = current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        else:
            crt = ' '.join(list(cart1))
            crt = crt + current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        kb = InlineKeyboardMarkup(row_width=2)
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb_cart = InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 25 см за ' + str(
            tfcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)
    elif '30' in call.data:
        await call.message.delete()
        product = call.data.split('_')
        product = product[2]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Thirty FROM Pizza WHERE PizzaName="{product}";')
        thcm = cur.fetchone()
        thcm = int(thcm[0])
        current = product + ' ' + str(thcm) + '_'
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        cart1 = cur.fetchone()
        if None in cart1:
            crt = current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        else:
            crt = ' '.join(list(cart1))
            crt = crt + current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        kb = InlineKeyboardMarkup(row_width=2)
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb_cart = InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 30 см за ' + str(
            thcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)
    elif '35' in call.data:
        await call.message.delete()
        product = call.data.split('_')
        product = product[2]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT ThirtyFive FROM Pizza WHERE PizzaName="{product}";')
        thfcm = cur.fetchone()
        thfcm = int(thfcm[0])
        current = product + ' ' + str(thfcm) + '_'
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        cart1 = cur.fetchone()
        if None in cart1:
            crt = current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        else:
            crt = ' '.join(list(cart1))
            crt = crt + current
            cur.execute(
                f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
            sqlite_connection.commit()
        kb = InlineKeyboardMarkup(row_width=2)
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb_cart = InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')
        kb.add(kb_cart, kb_bck)
        text = 'Вы успешно добавили в корзину пиццу: ' + product + ' 35 см за ' + str(
            thfcm) + ' рублей.\n Чтобы отменить это действие или оформить заказ перейдите в корзину,\n Чтобы добавить другую пиццу перейдите обратно в меню.'
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)
    elif call.data == "btn_clear":
        await call.message.delete()
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'UPDATE Customers SET Cart = NULL WHERE User_id = "{call.message.chat.id}";')
        sqlite_connection.commit()
        kb = InlineKeyboardMarkup()
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb.add(kb_bck)
        text = 'Корзина успешно очищена'
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)
    elif 'Order' in call.data:
        await call.message.delete()
        a = call.data.split('_')
        summ = a[-1]
        await bot.send_message(call.message.chat.id, 'Подождите пожалуйста. Ваш заказ обрабатывается.')
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
        button_list = [
            [InlineKeyboardButton(text='Подтвердить заказ', callback_data=f'btn_ok_{call.message.chat.id}_{summ}')], [
                InlineKeyboardButton(text='Невозможно оформить',
                                     callback_data=f'btn_wrong_{call.message.chat.id}_{summ}')],
            [InlineKeyboardButton(text='Отсутствует пицца', callback_data=f'btn_absent_{call.message.chat.id}_{summ}')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=button_list)
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        crt = list(cur.fetchone())[0].split('_')[:-1]
        await bot.send_message(admin,
                               'Получен заказ от ' + str(Name) + '. Номер заказа: ' + str(
                                   call.message.chat.id) + '\nЗаказ:\n' + '\n'.join(
                                   [str(i) for i in crt]) + '\n\nСумма заказа: ' + str(
                                   summ) + ' руб\n' + 'Время заказа: ' + datetime.now().strftime('%H:%M:%S %d.%m.%Y'),
                               reply_markup=keyboard)
    elif 'ok' in call.data:
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Pay_Token FROM Token;')
        token = cur.fetchone()
        token = token[0]
        print(str(call.message.chat.id) + ' оплата')
        a = call.data.split('_')
        cid = int(a[2])
        price = int(a[3]) * 100
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{cid}";')
        crt = list(cur.fetchone())[0].split('_')[:-1]
        a = call.data.split('_')
        cid = int(a[2])
        price = int(a[3]) * 100
        PRICES = [
            LabeledPrice(label='Ваш заказ', amount=price)
        ]
        await bot.send_invoice(cid,
                               title='Ваш заказ',
                               description='\n'.join([str(i) for i in crt]),
                               provider_token=token,
                               currency='rub',
                               need_phone_number=True,
                               prices=PRICES,
                               start_parameter='example',
                               payload='some_invoice')
    elif 'absent' in call.data:
        a = call.data.split('_')
        cid = int(a[2])
        last_message = a[-1]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT ID_of_chat FROM admin;')
        admin = cur.fetchone()
        admin = int(admin[0])
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{cid}";')
        crt = list(cur.fetchone())[0].split('_')
        button_list = []
        for i in crt:
            item = i.split(' ')
            i = item[0]
            button_list.append(
                [InlineKeyboardButton(i, callback_data=f'btn_ab_{i}_{cid}_{last_message}')]
            )
        keyboard = InlineKeyboardMarkup(inline_keyboard=button_list)
        await bot.send_message(admin, text='Выберите отсутсвующую пиццу', reply_markup=keyboard)
    elif 'wrong' in call.data:
        a = call.data.split('_')
        cid = int(a[2])
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Phone FROM admin;')
        phone = cur.fetchone()
        phone = phone[0]
        await bot.send_message(cid,
                               'К сожалению, невозможно в данный момент оформить заказ. По всем вопросам звоните: ' + phone)
    elif call.data == "btn_delivery":
        await call.message.delete()
        await Form.addres.set()
        await bot.send_message(call.message.chat.id, 'Напишите свой адрес')
    elif call.data == "btn_pick_up":
        await call.message.delete()
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Address FROM Shops;')
        shops = cur.fetchall()
        shops = [i[0] for i in shops]
        await Form.pick_up_addres.set()
        await bot.send_message(call.message.chat.id,
                               'Вот список наших магазинов, напишите адрес того, из которого хотите забрать.\n' + '\n'.join(
                                   [str(i) for i in shops]))
    elif 'ab' in call.data:
        await call.message.delete()
        a = call.data.split('_')
        cid = int(a[3])
        apizza = a[2]
        kb = InlineKeyboardMarkup(row_width=2)
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb_cart = InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')
        kb.add(kb_cart, kb_bck)
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{cid}";')
        crt = list(cur.fetchone())[0].split('_')
        for i in crt:
            if apizza in i:
                crt.remove(i)
                crt = '_'.join(crt)
                cur.execute(
                    f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{cid}";')
                sqlite_connection.commit()
                break
            else:
                continue
        await bot.send_message(cid,
                               'К сожалению, пицца ' + apizza + ' отсутсвует на данный момент. Пожалуйста выберите вместо неё другую.',
                               reply_markup=kb)
    elif 'del' in call.data:
        await call.message.delete()
        a = call.data.split('_')
        dpizza = a[2]
        sqlite_connection = sqlite3.connect('Customers')
        cur = sqlite_connection.cursor()
        cur.execute(
            f'SELECT Cart FROM Customers WHERE User_id="{call.message.chat.id}";')
        crt = list(cur.fetchone())[0].split('_')
        for i in crt:
            if dpizza in i:
                crt.remove(i)
                crt = '_'.join(crt)
                cur.execute(
                    f'UPDATE Customers SET Cart = "{crt}" WHERE User_id = "{call.message.chat.id}";')
                sqlite_connection.commit()
                break
            else:
                continue
        kb = InlineKeyboardMarkup(row_width=2)
        kb_bck = InlineKeyboardButton(text='🍕 Меню пицц', callback_data='btn_pizzas')
        kb_cart = InlineKeyboardButton(text='🛒 Ваша Корзина', callback_data='btn_cart')
        kb.add(kb_cart, kb_bck)
        await bot.send_message(call.message.chat.id, 'Успешно удалена из корзины пицца ' + dpizza, reply_markup=kb)


@dp.callback_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    Shipping_option = ShippingOption(
        id='deliver',
        title='Доставка по адресу'
    )
    Pick_up_shipping = ShippingOption(
        id='pickup',
        title='Самовывоз'
    )
    shipping_options = [Shipping_option, Pick_up_shipping]
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(str(pre_checkout_query.id), ok=True)


@dp.message_handler(content_types=['successful_payment'])
async def successful_payment(message: Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb_ok = types.InlineKeyboardButton(text='🚚 Доставка', callback_data=f'btn_delivery')
    kb_wr = types.InlineKeyboardButton(text='🏪 Самовывоз', callback_data=f'btn_pick_up')
    kb.add(kb_ok, kb_wr)
    print('Успешная оплата ' + str(message.chat.id))
    await bot.send_message(message.chat.id, 'Спасибо за заказ, выберите способ получения заказа.', reply_markup=kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
