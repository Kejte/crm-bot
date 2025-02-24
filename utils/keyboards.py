from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def keyboard_bilder(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        if button['button']['resourcetype'] == 'OffersButton':
            builder.button(text=f'{button['button']['title']}', callback_data=f'offers_categories')
        else:
            builder.button(text=f'{button['button']['title']}', callback_data=f'id_{button['button']['callback_message']}')
    
    builder.adjust(1)

    return builder.as_markup()

def offers_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    try:
        for category in categories:
            builder.button(text=f'{category['name']}',callback_data=f'offers_category_{category['id']}')
    except TypeError:
        ...
    
    builder.button(text='Назад',callback_data='hello_message')

    builder.adjust(1)

    return builder.as_markup()

def offers_keyboard(offers: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for offer in offers:
        builder.button(text=f'{offer['name']}', callback_data=f'offer_{offer['id']}')
    
    builder.button(text=f'Назад', callback_data=f'offers_categories')
    
    builder.adjust(1)
    return builder.as_markup()

def offer_keyboard(offer_id: int, category_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Взять в работу', callback_data=f'apply_offer_{offer_id}')
    builder.button(text='Назад', callback_data=f'offers_category_{category_id}')

    builder.adjust(1)
    
    return builder.as_markup()

def apply_offer(category_id: int, tg_id:int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.button(text='Назад к офферам', callback_data=f'offers_category_{category_id}')
    builder.button(text='Мои офферы', callback_data=f'applyed_offers_{tg_id}')

    builder.adjust(1)

    return builder.as_markup()