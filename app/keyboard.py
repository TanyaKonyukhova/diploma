from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

general_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать ежемесячный платеж по ипотеке')],
                                     [KeyboardButton(text='Вывести ипотечные программы')],
                                     [KeyboardButton(text='Вывести ключевую процентную ставку ЦБ'),]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт...')


program_classification= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Льготные ипотеки для IT специалистов', callback_data='preferential_mortgages_IT')],
                                                [InlineKeyboardButton(text='Другие льготные ипотеки', callback_data='other_preferential_mortgages')],])

program = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ипотека с господдержкой', callback_data='mortgage_state_support')],
                                                [InlineKeyboardButton(text='Семейная ипотека', callback_data='family_mortgage')],
                                                [InlineKeyboardButton(text='Сельская ипотека', callback_data='rural_mortgage')],
                                                [InlineKeyboardButton(text='Дальневосточная и Арктическая ипотека', callback_data='far_eastern_arctic_mortgages')],])

