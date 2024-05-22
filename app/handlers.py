from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboard as kb

global initial_payment, cost_real_estate, percent, term, sum_credit
initial_payment, cost_real_estate, percent, term, sum_credit = 0,0,0,0,0

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_full_name = message.from_user.full_name
    await message.answer(f"Добрый день, {user_full_name}!\nКак вас проконсультировать по ипотеке? :)", reply_markup=kb.general_menu)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи, соболезнуем')

@router.message(F.text == 'Вывести ипотечные программы')
async def catalog(message: Message):
    await message.answer('Выберите интересующую категорию:', reply_markup=kb.program_classification)

@router.message(F.text == 'Вывести ключевую процентную ставку ЦБ')
async def catalog(message: Message):
    await message.answer('Ключевая ставка Банка России на сегодня составляет - 16,00')


#РАСЧЕТ ИПОТЕКИ

@router.message(F.text == 'Рассчитать ежемесячный платеж по ипотеке') #ежемесячный платеж по ипотеки
async def monthly_payment(message: Message):
    global initial_payment, cost_real_estate, percent, term, sum_credit
    initial_payment, cost_real_estate, percent, term = 0,0,0,0
    await message.answer('Вы решили посчитать ежемесячный платеж', show_alert=True)
    await message.reply('Введите стоимость недвижимости')
    await monthly_payment_1()

@router.message(F.text)
async def monthly_payment_1(message: Message):    
    global initial_payment, cost_real_estate, percent, term, sum_credit

    if message.text == 'Отмена':
        await message.answer('Вы остановили процесс рассчета')
    elif cost_real_estate == 0:
        cost_real_estate = message.text
        try:
            cost_real_estate = float(cost_real_estate)
            await message.answer('Введите первоначальный взнос по ипотеке')
        except:
            await message.answer('Значение не корректно :(')
            cost_real_estate = 0
            await message.answer('Введите стоимость недвижимости')
        
    elif initial_payment == 0:
            
            initial_payment = message.text
            try:
                initial_payment = float(initial_payment)
                sum_credit = cost_real_estate - initial_payment
                if sum_credit <= 0:
                    await message.answer(f'Сумма кредита {sum_credit}, мы так посчитать не сможем :(\nПридется начинать сначала')
                    cost_real_estate = 0
                    initial_payment = 0
                else:
                    await message.reply(f'Сумма по кредиту: {sum_credit}')
                    await message.answer('Введите процент по ипотеке (годовой, без знака процента)')
            except:
                await message.answer('Значение не корректно :(')
                initial_payment = 0
                await message.answer('Введите первоначальный взнос по ипотеке')

    elif percent == 0:
        percent = message.text
        try:
            percent = float(percent)
            percent = percent/12/100
            await message.answer('Введите срок ипотеки (в годах)')
        except:
            await message.answer('Значение не корректно :(')
            percent = 0
            await message.answer('Введите процент по ипотеке (годовой, без знака процента)')
            
    elif term == 0:
        term = message.text
        try:
            term = float(term)
            term = term * 12
        except:
            await message.answer('Значение не корректно :(')
            term = 0
            await message.answer('Введите срок ипотеки (в годах)')
            
        x = round((sum_credit * percent * (1+percent)**term)/(((1+percent)**term)-1), 3)
        await message.answer(f'Ежемесячный платеж получается: {round(x, 5)}')
        await message.answer(f'Переплата составит: {round((sum_credit*((1+percent)**term))-sum_credit, 5)}')
    else:
        await message.answer('Ой-ой, я Вас не понимаю :(')


#ИПОТЕЧНЫЕ ПРОГРАММЫ

@router.callback_query(F.data == 'preferential_mortgages_IT') #ипотеки для IT
async def mortgages_IT(callback: CallbackQuery):
    await callback.message.answer('ИТ-ипотека до 5%\n\nПрограмма позволяет работникам аккредитованных Минцифры ИТ‑компаний приобрести жильё на первичном рынке или построить собственный дом. Проверить аккредитацию компании можно на Госуслугах\n\nТребования к заёмщикам:\n\nГражданство РФ\nРабота в аккредитованной ИТ-компании\nВозраст до 50 лет включительно\nДля граждан в возрасте от 36 до 50 лет включительно средняя зарплата до вычета НДФЛ за последние 3 месяца:\n\nот 150 тыс. ₽ — для сотрудников компаний, расположенных в Москв\nот 120 тыс. ₽ — для сотрудников компаний, расположенных в городах-миллионниках, кроме Москвы\nот 70 тыс. ₽ — для сотрудников компаний, расположенных во всех городах и иных муниципальных образованиях, кроме городов-миллионников\nТребования к зарплате учитываются по месту работы. Это может быть как головной офис компании, так и её филиал\n\n\n!К заёмщикам в возрасте до 35 лет включительно требование к размеру зарплаты не предъявляется\n\nСумма кредита:\n\nДо 18 млн ₽ - Регионы-миллионники\nДо 9 млн ₽- Другие регионы\n\nИТ-ипотеку можно сложить с суммой, взятой в кредит по рыночной или другой льготной ставке. Тогда общая сумма кредита увеличится до 30 млн ₽ для регионов-миллионников и 15 млн ₽ для других регионов\n\nУсловия программы:\n\nСтавка до 5%, она может быть снижена по региональной программе или банком\nМинимальный первоначальный взнос от 20%\nПрограмма распространяется только на новое жильё\nПрограмма действует до конца 2024 г., но льготная ставка сохранится на весь срок ипотечного кредита\n\n\n Более подробная информация на https://www.gosuslugi.ru/life/details/assistance_for_the_purchase_of_housing')


@router.callback_query(F.data == 'other_preferential_mortgages') #другие льготные ипотеки
async def other_mortgages(callback: CallbackQuery):
    await callback.message.answer('Выберите интересующую программу: ', reply_markup=kb.program)


@router.callback_query(F.data == 'mortgage_state_support') #Ипотека с господдержкой
async def monthly_payment(callback: CallbackQuery):
    await callback.message.answer('Льготная ипотека под 8%\n\nПо этой программе можно купить готовое жильё у застройщика или квартиру в строящемся доме по льготной ставке 8%. Она доступна всем совершеннолетним гражданам России независимо от семейного положения и наличия детей\n\nУсловия:\nПервоначальный взнос — от 30%. Максимальная сумма кредита на льготных условиях — 6 млн ₽ для всех регионов\nС 6 января 2023 г. льготную ипотеку можно получить только один раз\nПрограмма действует до 1 июля 2024 г.\n\n\n Более подробная информация на https://www.gosuslugi.ru/life/details/assistance_for_the_purchase_of_housing')


@router.callback_query(F.data == 'family_mortgage') #Семейная ипотека
async def family_mortgage(callback: CallbackQuery):
    await callback.message.answer('Семьи с детьми могут взять ипотеку с господдержкой — под 6% на весь срок кредита. Для Дальнего Востока — под 5%. Разницу между льготной и рыночной ставкой банку компенсирует государство\n\nТребования к заёмщикам:\n\nНаличие гражданства РФ у родителя и ребёнка\nНаличие в семье ребёнка, рождённого с 1 января 2018 г. по 31 декабря 2023 г.\nВ семье двое детей, которым ещё не исполнилось 18 лет на дату заключения кредитного договора\nВ семье есть ребёнок‑инвалид, рождённый до 31 декабря 2023 г.\n\nНа что можно взять кредит:\n\nНа квартиру или дом от застройщика по договору участия в долевом строительстве, договору уступки или купли‑продажи. То есть это первичное жильё — в эксплуатации или ещё строится\nНа строительство дома по договору подряда или на покупку земельного участка с дальнейшим строительством дома\nНа вторичное жильё в сельской местности, в том числе у граждан, в регионах Дальнего Востока\nНа жильё на вторичном рынке в регионах, где нет строящихся многоквартирных домов по данным Единой информационной системы жилищного строительства (ЕИСЖС), — для семей с детьми‑инвалидами\n\nУсловия программы:\n\nИпотечный договор должен быть заключён с 1 января 2018 г. по 1 июля 2024 г. Если ребёнку установлена инвалидность, ипотеку можно взять до 31 декабря 2027 г.\nПервоначальный взнос — минимум 20%\nМаксимальная сумма кредита на льготных условиях для Москвы, Московской области, Санкт‑Петербурга и Ленинградской области — 12 млн ₽, для других регионов — 6 млн ₽\nСтавка — 5% для Дальнего Востока, 6% — для других регионов. На усмотрение банка ставка может быть снижена\n\n\n Более подробная информация на https://www.gosuslugi.ru/life/details/assistance_for_the_purchase_of_housing')
  
@router.callback_query(F.data == 'rural_mortgage') #Сельская ипотека
async def rural_mortgage(callback: CallbackQuery):
    await callback.message.answer('Сельская ипотека до 3%\n\nВ сельской местности и малых городах можно купить новостройку или вторичное жильё в ипотеку по льготной ставке — от 0,1 до 3%. Также можно взять кредит на строительство дома. Основное требование к заёмщикам — наличие гражданства РФ. Условий по поводу семейного положения и возраста нет\n\nУсловия программы:\nСрок кредита — до 25 лет\nПервоначальный взнос — от 20%\nМаксимальная сумма кредита — 6 млн ₽\nВ программе можно участвовать только один раз\nПрограмма не действует на территориях Москвы, Санкт‑Петербурга и административных центров регионов\n\n\n Более подробная информация на https://www.gosuslugi.ru/life/details/assistance_for_the_purchase_of_housing')

@router.callback_query(F.data == 'far_eastern_arctic_mortgages') #Дальневосточная и Арктическая ипотека
async def far_eastern_arctic_mortgages(callback: CallbackQuery):
    await callback.message.answer('Дальневосточная и арктическая ипотека под 2%\n\nЭта программа для граждан РФ позволяет приобрести жильё в любом из регионов Дальнего Востока и Арктической зоны России. Она действует до конца 2030 года\n\nКто может стать заёмщиком:\n\nСупруги в возрасте до 35 лет включительно, оформляющие регистрацию в приобретаемом жилье\nОдинокий родитель моложе 36 лет с ребёнком до 18 лет включительно\nВладелец дальневосточного или арктического гектара\nУчастники программ повышения мобильности трудовых ресурсов\nПедагоги и работники медицинских организаций со стажем от 5 лет\nВынужденные переселенцы с территорий Украины, Луганской Народной Республики и Донецкой Народной Республики\nРаботники организаций оборонно‑промышленного комплекса (ОПК) в Арктике или на Дальнем Востоке\n\nНа что можно взять кредит:\n\nНа квартиру или дом от застройщика. Можно оформить договор участия в долевом строительстве или купли‑продажи\nНа строительство дома, в том числе своими силами, без привлечения подрядчиков\nНа вторичное жильё в сельских населённых пунктах, на территориях Магаданской области и Чукотского автономного округа, а также на территории моногородов\nНа вторичное жильё на территории любого региона Дальнего Востока и Арктической зоны — вынужденным переселенцам с территорий Украины, Луганской Народной Республики и Донецкой Народной Республики\n\n\n Более подробная информация на https://www.gosuslugi.ru/life/details/assistance_for_the_purchase_of_housing\n\nУсловия программы:\n\nСрок кредита — до 242 месяцев\nПервоначальный взнос — от 20%\nМаксимальная сумма кредита — 6 млн ₽. Может быть увеличена до 9 млн ₽, если площадь жилья больше 60 кв. м. Это не распространяется на вторичное жильё\nВ программе можно участвовать только один раз')

