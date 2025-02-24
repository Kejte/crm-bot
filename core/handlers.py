from aiogram import Bot
from aiogram.types import CallbackQuery, Message
import requests
from utils import keyboards
from aiogram.utils.markdown import hlink

async def hello_message(callback: CallbackQuery, bot: Bot):
    photo = 'https://img.goodfon.ru/original/2880x1800/e/3e/gory-vershiny-sneg-uschele.jpg'
    data = requests.get('http://app:8000/api/answers/hello_message').json()
    await bot.send_photo(callback.from_user.id,photo=photo,caption=f'{data['text']}',reply_markup=keyboards.keyboard_bilder(data['message_buttons']))

async def send_callback_message(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    photo = 'https://img.goodfon.ru/original/2880x1800/e/3e/gory-vershiny-sneg-uschele.jpg'
    message_id = callback.data.split('_')[-1]
    data = requests.get(f'http://app:8000/api/answers/retrive_message?message_id={message_id}').json()
    await bot.send_photo(callback.from_user.id,photo=photo,caption=f'{data['text']}',reply_markup=keyboards.keyboard_bilder(data['message_buttons']))

async def offers_categories(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    message = requests.get(f'http://app:8000/api/answers/offers_categories_message').json()
    categories = requests.get(f'http://app:8000/api/offers/categories?tg_id={callback.from_user.id}').json()
    if message['photo']:
        await bot.send_photo(callback.from_user.id,photo=message['photo'],caption=f'{message['text']}',reply_markup=keyboards.offers_categories_keyboard(categories=categories))
    else:
        await bot.send_message(callback.from_user.id,text=message['text'],reply_markup=keyboards.offers_categories_keyboard(categories=categories))

async def offers(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    category = callback.data.split('_')[-1]
    offers = requests.get(f'http://app:8000/api/offers/offers?category_id={category}&tg_id={callback.from_user.id}').json()
    message = requests.get(f'http://app:8000/api/answers/offer_message?category_id={category}').json()
    if message['photo']:
        await bot.send_photo(callback.from_user.id,photo=message['photo'],caption=f'{message['text']}',reply_markup=keyboards.offers_keyboard(offers))
    else:
        await bot.send_message(callback.from_user.id,text=message['text'],reply_markup=keyboards.offers_keyboard(offers))

async def offer(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    offer_id = callback.data.split('_')[-1]
    offer = requests.get(f'http://app:8000/api/offers/offer?offer_id={offer_id}').json()
    pp_url = hlink('*ТЫК*', offer['pp_url'])
    manual = hlink('*ТЫК*', offer['manual'])
    message = f'{offer['name']}\n\n{offer['description']}\n\nОплата: {offer['royalty']}₽\n\nОформить: {pp_url} \n\nМануал: {manual} '
    photo = 'https://img.goodfon.ru/original/2880x1800/e/3e/gory-vershiny-sneg-uschele.jpg'
    await bot.send_photo(callback.from_user.id,photo=photo,caption=message, parse_mode='HTML', reply_markup=keyboards.offer_keyboard(offer_id=int(offer_id), category_id=offer['category']))

async def apply_offer(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    offer_id = callback.data.split('_')[-1]
    category_id = requests.get(f'http://app:8000/api/offers/offer?offer_id={offer_id}').json()['category']
    tg_id = callback.from_user.id
    json = {
        'profile': int(tg_id),
        'offer': int(offer_id)
    }
    requests.post(f'http://app:8000/api/offers/create_aplyed_offer',json=json)
    data = requests.get(f'http://app:8000/api/answers/apply_offer_message').json()
    await bot.send_message(callback.from_user.id,text=data['text'],reply_markup=keyboards.apply_offer(category_id,callback.from_user.id))