import logging

from aiogram import *

import json

import asyncio
    
import aioschedule

import fitz

import sys

import re

import itertools

import psycopg2

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.filters.command import Command

from bs4 import BeautifulSoup


import requests

import urllib.request

# from aiogram.filters import Command
import openai

openai.api_key = "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"

delete_message = []

text_message = ["Hello"]

# API_TOKEN = "1949138034:AAFWTDe6_pr3FqWxJYouzrDxhx9BaceVchE"
API_TOKEN = "2019919570:AAHB8KVnAZXPNWJTQTPAM-UJIbk3NyM_KyA"

admin_id = 1116709501 

days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]

time_sleep = 1

all_groups = {}


# one_list = ['2к9191', '2к9091', '2к9111', '1к9091', '1к9191', '1к9111', '0к9091', '0к9191', '0к9111']

# second_list = ['9к9191', '0к9111']

# fird_list = ['2к9391', '2к9392', '2к9393', '2к9394', '2к9311', '1к9391', '1к9392', '1к9393', '1к9394']

# fourd_list = ['1к9311', '0к9391', '0к9392', '0к9393', '0к9394', '0к9311', '9к9391', '9к9392', '9к9393', '9к9394']

# fived_list = ['2к9491', '2к9591', '2к9291', '1к9491', '1к9591', '1к9291']

# sixed_list = ['0к9491', '0к9591', '0к9291', '9к9491', '9к9591', '9к9291']

Groups = [['2К9191', '2К9091', '2К9111', '1К9091', '1К9191', '1К9111', '0К9091', '0К9191'], 
    ['9К9091', '9К9191', '0К9111'], 
    ['2К9391', '2К9392', '2К9393', '2К9394', '2К9311', '1К9391', '1К9392', '1К9393', '1К9394'], 
    ['1К9311', '0К9391', '0К9392', '0К9393', '0К9394', '0К9311', '9К9391', '9К9392', '9К9393', '9К9394'],
    ['2К9491', '2К9591', '2К9291', '1К9491', '1К9591', '1К9291'], 
    ['0К9491', '0К9591', '0К9291', '9К9491', '9К9591', '9К9291'],
    ['2К9341', '2К9342', '1К9341', '0К9341', '9К9341']
]

allGroups = [
 ['2К9391', '2К9392', '2К9393', '2К9394', '2К9311', '1К9391', '1К9392', '1К9393', '1К9394'], 
 ['1К9311', '0К9391', '0К9392', '0К9393', '0К9394', '0К9311', '9К9391', '9К9392', '9К9393', '9К9394'], 
 ['2К9341', '2К9342', '0К9341', '1К9341', '9К9341']]

p = []

admins = {5406067686: [], 1068221109: []}

starosts = {1116709501: []}
#  
# all_groups = ['2к9191', '2к9091', '2к9111', '1к9091', '1к9191', '1к9111', '0к9091', '0к9191', '0к9111', '9к9191', '0к9111', '2к9391', '2к9392', '2к9393', '2к9394', '2к9311', '1к9391', '1к9392', '1к9393', '1к9394', '1к9311', '0к9391', '0к9392', '0к9393', '0к9394', '0к9311', '9к9391', '9к9392', '9к9393', '9к9394', '2к9491', '2к9591', '2к9291', '1к9491', '1к9591', '1к9291', '0к9491', '0к9591', '0к9291', '9к9491', '9к9591', '9к9291']
