# -*- coding: utf-8 -*-
import os
import sys

from cryptography.fernet import Fernet
import telebot as telebot
from requests import ReadTimeout
from random import randrange

from aes_cipher import AESCipher

cipher_key = 'APM1JDVgT8WDGOWBgQv6EIhvxl4vDYvUnVdg-Vjdt0o='
cipher_key_1 = 'NGWWUJqkriPUgapSWzEaxLetztK2oifQ--y3CJghE10='
cipher_key_2 = '6CZZQ4YRWMIUcoWm36W_7sXmxMgvXZNHgns-kBfCnZc='

cipher = Fernet(cipher_key)
cipher_1 = Fernet(cipher_key_1)
cipher_2 = Fernet(cipher_key_2)

bot = telebot.TeleBot('6297351245:AAHdCO6fKhMHKR7xaK0EUPLRELSdRn1WPn8')
allow_ids = [262007822, 123]


def is_allow(_id):
    return _id in allow_ids


@bot.message_handler(commands=["start"])
def send_welcome(message, res=False):
    if is_allow(message.chat.id):
        bot.send_message(message.chat.id, "Let's go")


@bot.message_handler(commands=["encode"])
def send_encode(message):
    if is_allow(message.chat.id):
        msg = bot.send_message(message.chat.id, "Enter text to encode:")
        bot.register_next_step_handler(msg, encode_handler)


@bot.message_handler(commands=["encodelight"])
def send_encode_light(message):
    if is_allow(message.chat.id):
        msg = bot.send_message(message.chat.id, "Enter text to encode:")
        bot.register_next_step_handler(msg, light_encode_handler)


@bot.message_handler(commands=["decode"])
def send_decode(message):
    if is_allow(message.chat.id):
        msg = bot.send_message(message.chat.id, "Enter text to decode:")
        bot.register_next_step_handler(msg, decode_handler)


@bot.message_handler(commands=["decodelight"])
def send_decode(message):
    if is_allow(message.chat.id):
        msg = bot.send_message(message.chat.id, "Enter text to decode:")
        bot.register_next_step_handler(msg, light_decode_handler)


def light_encode_handler(message):
    init_text = message.text

    cipher_light = AESCipher(cipher_key)
    ciphertext = cipher_light.encrypt(init_text)

    encoded = ciphertext#ciphertext.decode('utf8')
    ans = ''
    for c in encoded:
        ans += shift(c, 3)
    encoded = ans

    ans = ''
    for c in encoded:
        ans += shift(c, 17)
    encoded = ans

    ans = ''
    for c in encoded:
        ans += shift(c, 7)
    encoded = ans

    bot.send_message(message.chat.id, f"{encoded}")


def encode_handler(message):
    init_text = message.text

    encoded = init_text
    encoded = cipher.encrypt(str.encode(encoded)).decode()
    encoded = cipher_1.encrypt(str.encode(encoded)).decode()
    encoded = cipher_2.encrypt(str.encode(encoded)).decode()

    ans = ''
    for c in encoded:
        ans += shift(c, 3)
    encoded = ans

    ans = ''
    for c in encoded:
        ans += shift(c, 17)
    encoded = ans

    ans = ''
    for c in encoded:
        ans += shift(c, 7)
    encoded = ans

    bot.send_message(message.chat.id, f"{encoded}")


def decode_handler(message):
    init_text = message.text

    decoded = init_text

    ans = ''
    for c in decoded:
        ans += back_shift(c, 7)
    decoded = ans

    ans = ''
    for c in decoded:
        ans += back_shift(c, 17)
    decoded = ans

    ans = ''
    for c in decoded:
        ans += back_shift(c, 3)
    decoded = ans

    decoded = cipher_2.decrypt(str.encode(decoded)).decode()
    decoded = cipher_1.decrypt(str.encode(decoded)).decode()
    decoded = cipher.decrypt(str.encode(decoded)).decode()
    # return decoded
    bot.send_message(message.chat.id, f"{decoded}")


def light_decode_handler(message):
    init_text = message.text

    decoded = init_text

    ans = ''
    for c in decoded:
        ans += back_shift(c, 7)
    decoded = ans

    ans = ''
    for c in decoded:
        ans += back_shift(c, 17)
    decoded = ans

    ans = ''
    for c in decoded:
        ans += back_shift(c, 3)
    decoded = ans

    cipher = AESCipher(cipher_key)
    ciphertext = cipher.decrypt(decoded)
    decoded = ciphertext
    # return decoded
    bot.send_message(message.chat.id, f"{decoded}")


s = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_abcdefghijklmnopqrstuvwxyz{|}~'


def shift(text, n):
    index = s.find(text)
    if index + n < len(s):
        return s[index + n]
    else:
        return s[(index + n) % len(s)]


def back_shift(text, n):
    index = s.find(text)
    if index - n >= 0:
        return s[index - n]
    else:
        return s[(index - n) % len(s)]


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
