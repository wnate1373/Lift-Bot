#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import pip
pip.main(["install", "gspread"])
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import time
from typing import Dict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, Update
runCount = 0
runCount2 = 0
runCount3 = 0
runCount4 = 0
rowNum = 2

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
WEIGHT_CHOOSING, LEGCURL_SETS_INFO, LEGCURL_WEIGHT_INFO, LEGCURL_REPS_INFO, DBLUNGE_SETS_INFO, DBLUNGE_WEIGHT_INFO, DBLUNGE_REPS_INFO, LEGPRESS_SETS_INFO, LEGPRESS_WEIGHT_INFO, LEGPRESS_REPS_INFO, SQUAT_SETS_INFO, SQUAT_WEIGHT_INFO, SQUAT_REPS_INFO, DBCURL_SETS_INFO, DBCURL_WEIGHT_INFO, DBCURL_REPS_INFO, DBROW_SETS_INFO, DBROW_WEIGHT_INFO, DBROW_REPS_INFO, CABLEROW_SETS_INFO, CABLEROW_WEIGHT_INFO, CABLEROW_REPS_INFO, LATPULL_SETS_INFO, LATPULL_WEIGHT_INFO, LATPULL_REPS_INFO, INCLINEDB_SETS_INFO, INCLINEDB_WEIGHT_INFO, INCLINEDB_REPS_INFO, DUMBBELL_SETS_INFO, DUMBBELL_WEIGHT_INFO, DUMBBELL_REPS_INFO, OVERHEAD_SETS_INFO, OVERHEAD_WEIGHT_INFO, OVERHEAD_REPS_INFO, BENCH_SETS_INFO, BENCH_WEIGHT_INFO, BENCH_REPS_INFO, PUSH_CHOOSING, PULL_CHOOSING, LEGS_CHOOSING, WEIGHT_INFO = range(41)


reply_keyboard = [
    ['/weight', '/pull_day'],
    ['/push_day', '/leg_day'],
    ['Exit'],
]
reply2_keyboard = [
    ['/weight', '/pull_day'],
    ['/push_day', '/leg_day'],
]

push_reply_keyboard = [
    ['Bench', 'Overhead Press'],
    ['Dumbbell Press', 'Incline DB Press'],
    ['Exit']
]
pull_reply_keyboard = [
    ['Lat Pulldowns', 'Cable Rows'],
    ['Dumbbell Rows', 'Dumbbell Curls'],
    ['Exit']
]
leg_reply_keyboard = [
    ['Barbell Squat', 'Leg Press'],
    ['Dumbbell Lunges', 'Leg Curls'],
    ['Exit']
]
weight_reply_keyboard = [
    ['Record Again'],
    ['Done']
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
pushMarkup = ReplyKeyboardMarkup(push_reply_keyboard, one_time_keyboard=True)
pullMarkup = ReplyKeyboardMarkup(pull_reply_keyboard, one_time_keyboard=True)
legMarkup = ReplyKeyboardMarkup(leg_reply_keyboard, one_time_keyboard=True)
weightMarkup = ReplyKeyboardMarkup(weight_reply_keyboard, one_time_keyboard=True)
reply2Markup = ReplyKeyboardMarkup(reply2_keyboard, one_time_keyboard=True)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('liftbot-299519-2b24d73518a9.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open('liftBotSheet').sheet1

def changeRowNum(nextEmpty):
    global rowNum
    rowNum = nextEmpty[1:]
    
    
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)
    
    
def find_empty_cell():
    alphabet = list(map(chr, range(65, 91)))
    for letter in alphabet[0:1]: #look only at column A and B
        for x in range(1, 1000):
            cell_coord = letter+ str(x)
            if wks.acell(cell_coord).value == "":
                return(cell_coord)
                
def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Hi! My name is liftBot. Welcome to your workout recording! Your data will be automatically logged into the linked spreadsheet under the correct date. What would you like to record?", reply_markup=reply2Markup)
    row1List = wks.col_values(1)
    sameDay = False
    today = date.today()
    todayFormatted = today.strftime("%d/%m/%Y")
    update.message.reply_text("today's Date: ")
    update.message.reply_text(todayFormatted)
    for cell in row1List:
        if cell == todayFormatted:
            sameDay = True
            cell1 = wks.find(todayFormatted)
            nextEmpty = cell1.address
        else:
            sameDay = False

    if sameDay == False:
        nextEmpty = find_empty_cell()
        wks.update(nextEmpty, todayFormatted)
    changeRowNum(nextEmpty)

    

def weight_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f'Great! Please enter your weight in lbs now:')
    return WEIGHT_INFO

    
    
def weight_information(update: Update, context: CallbackContext) -> int:
    Weight = update.message.text
    update.message.reply_text("Neat! Your weight for today (*Enter Day Here*) in lbs is:")
    update.message.reply_text(Weight)
    wks.update_cell(rowNum, 2, Weight)
    update.message.reply_text("Select Record Again to overwrite the previous weight, or Done to exit!", reply_markup=weightMarkup)

    return WEIGHT_CHOOSING
        
    

def push_choice(update: Update, context: CallbackContext) -> int:
    global runCount
    if runCount == 0:
        update.message.reply_text("Please select your first push lift:", reply_markup=pushMarkup)
        runCount = runCount + 1
    else:
        update.message.reply_text("Please select another push lift, select the same lift overwrite a previous lift entry, or select exit to end the program:", reply_markup=pushMarkup)

    return PUSH_CHOOSING
    
    
    #Getting Bench Info
def benchSetsInfo(update: Update, context: CallbackContext) -> int:
    benchSets = update.message.text
    wks.update_cell(rowNum, 4, benchSets)
    benchSetsReply = "Your Bench Sets: {}".format(benchSets)
    update.message.reply_text(benchSetsReply)
    update.message.reply_text("Your Bench Press has been recorded!")

    push_choice(update, context)
    
    return PUSH_CHOOSING

def benchWeightInfo(update: Update, context: CallbackContext) -> int:
    benchWeight = update.message.text
    wks.update_cell(rowNum, 5, benchWeight)
    benchWeightReply = "Your Bench Weight: {}".format(benchWeight)
    update.message.reply_text(benchWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    
    return BENCH_SETS_INFO
    
def benchRepsInfo(update: Update, context: CallbackContext) -> int:
    benchReps = update.message.text
    wks.update_cell(rowNum, 3, benchReps)
    benchRepsReply = "Your Bench Reps per Set: {}".format(benchReps)
    update.message.reply_text(benchRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return BENCH_WEIGHT_INFO

def bench_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Bench: How many reps per set?')
        
    return BENCH_REPS_INFO
        
    #End Bench Info
    
    
    
    #Getting Overhead Info
def overheadSetsInfo(update: Update, context: CallbackContext) -> int:
    overheadSets = update.message.text
    wks.update_cell(rowNum, 7, overheadSets)
    overheadSetsReply = "Your Overhead Press Sets: {}".format(overheadSets)
    update.message.reply_text(overheadSetsReply)
    update.message.reply_text("Your Overhead Press has been recorded!")

    push_choice(update, context)
    
    return PUSH_CHOOSING

def overheadWeightInfo(update: Update, context: CallbackContext) -> int:
    overheadWeight = update.message.text
    wks.update_cell(rowNum, 8, overheadWeight)
    overheadWeightReply = "Your Overhead Press Weight: {}".format(overheadWeight)
    update.message.reply_text(overheadWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    
    return OVERHEAD_SETS_INFO
    
def overheadRepsInfo(update: Update, context: CallbackContext) -> int:
    overheadReps = update.message.text
    wks.update_cell(rowNum, 6, overheadReps)
    overheadRepsReply = "Your Overhead Press Reps per Set: {}".format(overheadReps)
    update.message.reply_text(overheadRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return OVERHEAD_WEIGHT_INFO
        
def overhead_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Overhead Press: How many reps per set?')
    
    return OVERHEAD_REPS_INFO
    
    #End Overhead Info
    
    
    #Getting Dumbbell Press info
def dumbbellSetsInfo(update: Update, context: CallbackContext) -> int:
    dumbbellSets = update.message.text
    wks.update_cell(rowNum, 10, dumbbellSets)
    dumbbellSetsReply = "Your Dumbbell Press Sets: {}".format(dumbbellSets)
    update.message.reply_text(dumbbellSetsReply)
    update.message.reply_text("Your Dumbbell Press has been recorded!")

    push_choice(update, context)
    
    return PUSH_CHOOSING

def dumbbellWeightInfo(update: Update, context: CallbackContext) -> int:
    dumbbellWeight = update.message.text
    wks.update_cell(rowNum, 11, dumbbellWeight)
    dumbbellWeightReply = "Your Dumbbell Press Weight: {}".format(dumbbellWeight)
    update.message.reply_text(dumbbellWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    
    return DUMBBELL_SETS_INFO
    
def dumbbellRepsInfo(update: Update, context: CallbackContext) -> int:
    dumbbellReps = update.message.text
    wks.update_cell(rowNum, 9, dumbbellReps)
    dumbbellRepsReply = "Your Dumbbell Press Reps per Set: {}".format(dumbbellReps)
    update.message.reply_text(dumbbellRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return DUMBBELL_WEIGHT_INFO
        
def dumbbell_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Dumbbell Press: How many reps per set?')
        
    return DUMBBELL_REPS_INFO
        
    #End Dumbbell Info
    
    
    #Get Incline DB Info
def inclinedbSetsInfo(update: Update, context: CallbackContext) -> int:
    inclinedbSets = update.message.text
    wks.update_cell(rowNum, 13, inclinedbSets)
    inclinedbSetsReply = "Your Incline Dumbbell Press Sets: {}".format(inclinedbSets)
    update.message.reply_text(inclinedbSetsReply)
    update.message.reply_text("Your Incline Dumbbell Press has been recorded!")

    push_choice(update, context)
    
    return PUSH_CHOOSING

def inclinedbWeightInfo(update: Update, context: CallbackContext) -> int:
    inclinedbWeight = update.message.text
    wks.update_cell(rowNum, 14, inclinedbWeight)
    inclinedbWeightReply = "Your Incline Dumbbell Press Weight: {}".format(inclinedbWeight)
    update.message.reply_text(inclinedbWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    
    return INCLINEDB_SETS_INFO
    
def inclinedbRepsInfo(update: Update, context: CallbackContext) -> int:
    inclinedbReps = update.message.text
    wks.update_cell(rowNum, 12, inclinedbReps)
    inclinedbRepsReply = "Your Incline Dumbbell Press Reps per Set: {}".format(inclinedbReps)
    update.message.reply_text(inclinedbRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return INCLINEDB_WEIGHT_INFO
    
def inclineDB_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Incline Dumbbell Press: How many reps per set?')

    return INCLINEDB_REPS_INFO
    
    #End Incline DB Info
    
    
    #Start Pull Day functions
    
def pull_choice(update: Update, context: CallbackContext) -> int:
    global runCount2
    if runCount2 == 0:
        update.message.reply_text("Please select your first pull lift:", reply_markup=pullMarkup)
        runCount2 = runCount2 + 1
    else:
        update.message.reply_text("Please select another pull lift, select the same lift to overwrite a previous lift entry, or select exit to end the program:", reply_markup=pullMarkup)
    
    return PULL_CHOOSING
    
    
    #Start Lat Pull Functions
def latpullSetsInfo(update: Update, context: CallbackContext) -> int:
    latpullSets = update.message.text
    wks.update_cell(rowNum, 16, latpullSets)
    latpullSetsReply = "Your Lat Pull Sets: {}".format(latpullSets)
    update.message.reply_text(latpullSetsReply)
    update.message.reply_text("Your Lat Pull has been recorded!")

    pull_choice(update, context)
    
    return PULL_CHOOSING
    
def latpullWeightInfo(update: Update, context: CallbackContext) -> int:
    latpullWeight = update.message.text
    wks.update_cell(rowNum, 17, latpullWeight)
    latpullWeightReply = "Your Lat Pull Weight: {}".format(latpullWeight)
    update.message.reply_text(latpullWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return LATPULL_SETS_INFO


def latpullRepsInfo(update: Update, context: CallbackContext) -> int:
    latpullReps = update.message.text
    wks.update_cell(rowNum, 15, latpullReps)
    latpullRepsReply = "Your Lat Pull Reps per Set: {}".format(latpullReps)
    update.message.reply_text(latpullRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return LATPULL_WEIGHT_INFO

def latpull_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Lat Pulldown: How many reps per set?')

    return LATPULL_REPS_INFO
    #End Lat Pull


    #Start Cable Row
def cablerowSetsInfo(update: Update, context: CallbackContext) -> int:
    cablerowSets = update.message.text
    wks.update_cell(rowNum, 19, cablerowSets)
    cablerowSetsReply = "Your Cable Row Sets: {}".format(cablerowSets)
    update.message.reply_text(cablerowSetsReply)
    update.message.reply_text("Your Cable Row has been recorded!")

    pull_choice(update, context)
    
    return PULL_CHOOSING
    
    
def cablerowWeightInfo(update: Update, context: CallbackContext) -> int:
    cablerowWeight = update.message.text
    wks.update_cell(rowNum, 20, cablerowWeight)
    cablerowWeightReply = "Your Cable Row Weight: {}".format(cablerowWeight)
    update.message.reply_text(cablerowWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return CABLEROW_SETS_INFO
    
    
def cablerowRepsInfo(update: Update, context: CallbackContext) -> int:
    cablerowReps = update.message.text
    wks.update_cell(rowNum, 18, cablerowReps)
    cablerowRepsReply = "Your Cable Row Reps per Set: {}".format(cablerowReps)
    update.message.reply_text(cablerowRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return CABLEROW_WEIGHT_INFO
    
    
def cablerows_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Cable Rows: How many reps per set?')

    return CABLEROW_REPS_INFO
    #End Cable Row


    #Start Dumbbell Row
def dbrowSetsInfo(update: Update, context: CallbackContext) -> int:
    dbrowSets = update.message.text
    wks.update_cell(rowNum, 22, dbrowSets)
    dbrowSetsReply = "Your Dumbbell Row Sets: {}".format(dbrowSets)
    update.message.reply_text(dbrowSetsReply)
    update.message.reply_text("Your Dumbbel Row has been recorded!")

    pull_choice(update, context)
    
    return PULL_CHOOSING
    
    
def dbrowWeightInfo(update: Update, context: CallbackContext) -> int:
    dbrowWeight = update.message.text
    wks.update_cell(rowNum, 23, dbrowWeight)
    dbrowWeightReply = "Your Dumbbell Row Weight: {}".format(dbrowWeight)
    update.message.reply_text(dbrowWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return DBROW_SETS_INFO
    
    
def dbrowRepsInfo(update: Update, context: CallbackContext) -> int:
    dbrowReps = update.message.text
    wks.update_cell(rowNum, 21, dbrowReps)
    dbrowRepsReply = "Your Dumbbell Row Reps per Set: {}".format(dbrowReps)
    update.message.reply_text(dbrowRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return DBROW_WEIGHT_INFO
    
    
def dbrows_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Dumbbell Row: How many reps per set?')

    return DBROW_REPS_INFO
    #End Dumbbell Rows
    
    
    #Start Dumbbell Curls
def dbcurlSetsInfo(update: Update, context: CallbackContext) -> int:
    dbcurlSets = update.message.text
    wks.update_cell(rowNum, 25, dbcurlSets)
    dbcurlSetsReply = "Your Dumbbell Curl Sets: {}".format(dbcurlSets)
    update.message.reply_text(dbcurlSetsReply)
    update.message.reply_text("Your Dumbbel Curl has been recorded!")

    pull_choice(update, context)
    
    return PULL_CHOOSING
    
    
def dbcurlWeightInfo(update: Update, context: CallbackContext) -> int:
    dbcurlWeight = update.message.text
    wks.update_cell(rowNum, 26, dbcurlWeight)
    dbcurlWeightReply = "Your Dumbbell Curl Weight: {}".format(dbcurlWeight)
    update.message.reply_text(dbcurlWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return DBCURL_SETS_INFO
    
    
def dbcurlRepsInfo(update: Update, context: CallbackContext) -> int:
    dbcurlReps = update.message.text
    wks.update_cell(rowNum, 24, dbcurlReps)
    dbcurlRepsReply = "Your Dumbbell Curl Reps per Set: {}".format(dbcurlReps)
    update.message.reply_text(dbcurlRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return DBCURL_WEIGHT_INFO

def dbcurls_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Dumbbell Curl: How many reps per set?')

    return DBCURL_REPS_INFO
    #End Pull Day
    
    #Start Leg Day Functions
def leg_choice(update: Update, context: CallbackContext) -> int:
    global runCount3
    if runCount3 == 0:
        update.message.reply_text("Please select your first leg day lift:", reply_markup=legMarkup)
        runCount3 = runCount3 + 1
    else:
        update.message.reply_text("Please select another leg day lift, select the same lift to overwrite a previous lift entry, or select exit to end the program:", reply_markup=legMarkup)
    
    return LEGS_CHOOSING
    
    #Start Squat
def squatSetsInfo(update: Update, context: CallbackContext) -> int:
    squatSets = update.message.text
    wks.update_cell(rowNum, 28, squatSets)
    squatSetsReply = "Your Squat Sets: {}".format(squatSets)
    update.message.reply_text(squatSetsReply)
    update.message.reply_text("Your Squat has been recorded!")

    leg_choice(update, context)
    
    return LEGS_CHOOSING
    
    
def squatWeightInfo(update: Update, context: CallbackContext) -> int:
    squatWeight = update.message.text
    wks.update_cell(rowNum, 29, squatWeight)
    squatWeightReply = "Your Squat Weight: {}".format(squatWeight)
    update.message.reply_text(squatWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return SQUAT_SETS_INFO
    
    
def squatRepsInfo(update: Update, context: CallbackContext) -> int:
    squatReps = update.message.text
    wks.update_cell(rowNum, 27, squatReps)
    squatRepsReply = "Your Squat Reps per Set: {}".format(squatReps)
    update.message.reply_text(squatRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return SQUAT_WEIGHT_INFO
    
def squat_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Barbell Squat: How many reps per set?')

    return SQUAT_REPS_INFO
    #End Squat
    
    
    #Start Leg Press
def legpressSetsInfo(update: Update, context: CallbackContext) -> int:
    legpressSets = update.message.text
    wks.update_cell(rowNum, 31, legpressSets)
    legpressSetsReply = "Your Leg Press Sets: {}".format(legpressSets)
    update.message.reply_text(legpressSetsReply)
    update.message.reply_text("Your Leg Press has been recorded!")

    leg_choice(update, context)
    
    return LEGS_CHOOSING
    
    
def legpressWeightInfo(update: Update, context: CallbackContext) -> int:
    legpressWeight = update.message.text
    wks.update_cell(rowNum, 32, legpressWeight)
    legpressWeightReply = "Your Leg Press Weight: {}".format(legpressWeight)
    update.message.reply_text(legpressWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return LEGPRESS_SETS_INFO
    
    
def legpressRepsInfo(update: Update, context: CallbackContext) -> int:
    legpressReps = update.message.text
    wks.update_cell(rowNum, 30, legpressReps)
    legpressRepsReply = "Your Leg Press Reps per Set: {}".format(legpressReps)
    update.message.reply_text(legpressRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return LEGPRESS_WEIGHT_INFO
    
    
def legpress_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Leg Press: How many reps per set?')

    return LEGPRESS_REPS_INFO
    #End leg press
    
    #Start dumbbell lunge
def dblungeSetsInfo(update: Update, context: CallbackContext) -> int:
    dblungeSets = update.message.text
    wks.update_cell(rowNum, 34, dblungeSets)
    dblungeSetsReply = "Your Dumbbell Lunge Sets: {}".format(dblungeSets)
    update.message.reply_text(dblungeSetsReply)
    update.message.reply_text("Your Dumbbell Lunge has been recorded!")

    leg_choice(update, context)
    
    return LEGS_CHOOSING
    
    
def dblungeWeightInfo(update: Update, context: CallbackContext) -> int:
    dblungeWeight = update.message.text
    wks.update_cell(rowNum, 35, dblungeWeight)
    dblungeWeightReply = "Your Dumbbell Lunge Weight: {}".format(dblungeWeight)
    update.message.reply_text(dblungeWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return DBLUNGE_SETS_INFO
    
    
def dblungeRepsInfo(update: Update, context: CallbackContext) -> int:
    dblungeReps = update.message.text
    wks.update_cell(rowNum, 33, dblungeReps)
    dblungeRepsReply = "Your Dumbbell Lunge Reps per Set: {}".format(dblungeReps)
    update.message.reply_text(dblungeRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return DBLUNGE_WEIGHT_INFO
    
def dblunge_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Dumbbell Lunge: How many reps per set?')

    return DBLUNGE_REPS_INFO
    #End Dumbbell Lunge
    
    #Start leg curls
def legcurlSetsInfo(update: Update, context: CallbackContext) -> int:
    legcurlSets = update.message.text
    wks.update_cell(rowNum, 37, legcurlSets)
    legcurlSetsReply = "Your Leg Curl Sets: {}".format(legcurlSets)
    update.message.reply_text(legcurlSetsReply)
    update.message.reply_text("Your Leg Curl has been recorded!")

    leg_choice(update, context)
    
    return LEGS_CHOOSING
    
    
def legcurlWeightInfo(update: Update, context: CallbackContext) -> int:
    legcurlWeight = update.message.text
    wks.update_cell(rowNum, 38,legcurlWeight)
    legcurlWeightReply = "Your Leg Curl Weight: {}".format(legcurlWeight)
    update.message.reply_text(legcurlWeightReply)
    update.message.reply_text("Finally, please enter the number of sets:")

    return LEGCURL_SETS_INFO
    
    
def legcurlRepsInfo(update: Update, context: CallbackContext) -> int:
    legcurlReps = update.message.text
    wks.update_cell(rowNum, 36, legcurlReps)
    legcurlRepsReply = "Your Leg Curl Reps per Set: {}".format(legcurlReps)
    update.message.reply_text(legcurlRepsReply)
    update.message.reply_text("Now, please enter the weight in lbs per rep (use an average if weight varied)")
    
    return LEGCURL_WEIGHT_INFO
    
    
def legcurl_reps(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Leg Curls: How many reps per set?')

    return LEGCURL_REPS_INFO
    #End Dumbbell Lunge
    #End Leg Day
    
    

    

def done(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        f"Thank you for using liftBot! Please use /start if you need to log or overwrite something else!"
    )
    return ConversationHandler.END


def weight_done(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        f"Thank you for recording your weight! Please use the any of the commands (/weight, /push_day, /pull_day, /leg_day) if you need to log or overwrite something else!", reply_markup=reply2Markup
    )
    return ConversationHandler.END




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1471349618:AAHeKGTeeu9YMWR7aYCTbrgimO_JviLVdlc", use_context=True)
        
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Push)$'), push_choice
                ),
                MessageHandler(
                    Filters.regex('^(Pull)$'), pull_choice
                ),
                MessageHandler(
                    Filters.regex('^(Legs)$'), leg_choice
                ),
            ],
        },
        
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), done)],
    )
    
    weight_handler = ConversationHandler(
        entry_points=[CommandHandler('weight', weight_choice)],
        states={
            WEIGHT_CHOOSING: [
            MessageHandler(
                Filters.regex('(Record Again)$'), weight_choice),
            MessageHandler(
                Filters.regex('(Done)$'), weight_done),
                ],
            WEIGHT_INFO: [
                MessageHandler(Filters.text, weight_information),
            ],
        },
        
        fallbacks=[MessageHandler(Filters.regex('^nada'), done)],
    )

    push_handler = ConversationHandler(
        entry_points=[CommandHandler('push_day', push_choice)],
        states={
            PUSH_CHOOSING: [
            MessageHandler(
                Filters.regex('^(Bench)$'), bench_reps
                ),
                MessageHandler(
                    Filters.regex('^(Overhead Press)$'), overhead_reps
                ),
                MessageHandler(
                    Filters.regex('^(Dumbbell Press)$'), dumbbell_reps
               ),
                MessageHandler(
                    Filters.regex('^(Incline DB Press)$'), inclineDB_reps
                ),
            ],
            BENCH_REPS_INFO: [
                MessageHandler(Filters.text, benchRepsInfo),
            ],
            BENCH_WEIGHT_INFO: [
                MessageHandler(Filters.text, benchWeightInfo),
            ],
            BENCH_SETS_INFO: [
                MessageHandler(Filters.text, benchSetsInfo),
            ],
            OVERHEAD_REPS_INFO: [
                MessageHandler(Filters.text, overheadRepsInfo),
            ],
            OVERHEAD_WEIGHT_INFO: [
                MessageHandler(Filters.text, overheadWeightInfo),
            ],
            OVERHEAD_SETS_INFO: [
                MessageHandler(Filters.text, overheadSetsInfo),
            ],
            DUMBBELL_REPS_INFO: [
                MessageHandler(Filters.text, dumbbellRepsInfo),
            ],
            DUMBBELL_WEIGHT_INFO: [
                MessageHandler(Filters.text, dumbbellWeightInfo),
            ],
            DUMBBELL_SETS_INFO: [
                MessageHandler(Filters.text, dumbbellSetsInfo),
            ],
            INCLINEDB_REPS_INFO: [
                MessageHandler(Filters.text, inclinedbRepsInfo),
            ],
            INCLINEDB_WEIGHT_INFO: [
                MessageHandler(Filters.text, inclinedbWeightInfo),
            ],
            INCLINEDB_SETS_INFO: [
                MessageHandler(Filters.text, inclinedbSetsInfo),
            ],
        },
        
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), done)],
        )
        
    pull_handler = ConversationHandler(
        entry_points=[CommandHandler('pull_day', pull_choice)],
        states={
            PULL_CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Lat Pulldowns)$'), latpull_reps
                ),
                MessageHandler(
                    Filters.regex('^(Cable Rows)$'), cablerows_reps
                ),
                MessageHandler(
                    Filters.regex('^(Dumbbell Rows)$'), dbrows_reps
                ),
                MessageHandler(
                    Filters.regex('^(Dumbbell Curls)$'), dbcurls_reps
                ),
            ],
            LATPULL_REPS_INFO: [
                MessageHandler(Filters.text, latpullRepsInfo),
            ],
            LATPULL_WEIGHT_INFO: [
                MessageHandler(Filters.text, latpullWeightInfo),
            ],
            LATPULL_SETS_INFO: [
                MessageHandler(Filters.text, latpullSetsInfo),
            ],
            CABLEROW_REPS_INFO: [
                MessageHandler(Filters.text, cablerowRepsInfo),
            ],
            CABLEROW_WEIGHT_INFO: [
                MessageHandler(Filters.text, cablerowWeightInfo),
            ],
            CABLEROW_SETS_INFO: [
                MessageHandler(Filters.text, cablerowSetsInfo),
            ],
            DBROW_REPS_INFO: [
                MessageHandler(Filters.text, dbrowRepsInfo),
            ],
            DBROW_WEIGHT_INFO: [
                MessageHandler(Filters.text, dbrowWeightInfo),
            ],
            DBROW_SETS_INFO: [
                MessageHandler(Filters.text, dbrowSetsInfo),
            ],
            DBCURL_REPS_INFO: [
                MessageHandler(Filters.text, dbcurlRepsInfo),
            ],
            DBCURL_WEIGHT_INFO: [
                MessageHandler(Filters.text, dbcurlWeightInfo),
            ],
            DBCURL_SETS_INFO: [
                MessageHandler(Filters.text, dbcurlSetsInfo),
            ],

        },
        
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), done)],
    )
    leg_handler = ConversationHandler(
        entry_points=[CommandHandler('leg_day', leg_choice)],
        states={
            LEGS_CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Barbell Squat)$'), squat_reps
                ),
                MessageHandler(
                    Filters.regex('^(Leg Press)$'), legpress_reps
                ),
                MessageHandler(
                    Filters.regex('^(Dumbbell Lunges)$'), dblunge_reps
                ),
                MessageHandler(
                    Filters.regex('^(Leg Curls)$'), legcurl_reps
                ),
            ],
            SQUAT_REPS_INFO: [
                MessageHandler(Filters.text, squatRepsInfo),
            ],
            SQUAT_WEIGHT_INFO: [
                MessageHandler(Filters.text, squatWeightInfo),
            ],
            SQUAT_SETS_INFO: [
                MessageHandler(Filters.text, squatSetsInfo),
            ],
            LEGPRESS_REPS_INFO: [
                MessageHandler(Filters.text, legpressRepsInfo),
            ],
            LEGPRESS_WEIGHT_INFO: [
                MessageHandler(Filters.text, legpressWeightInfo),
            ],
            LEGPRESS_SETS_INFO: [
                MessageHandler(Filters.text, legpressSetsInfo),
            ],
            DBLUNGE_REPS_INFO: [
                MessageHandler(Filters.text, dblungeRepsInfo),
            ],
            DBLUNGE_WEIGHT_INFO: [
                MessageHandler(Filters.text, dblungeWeightInfo),
            ],
            DBLUNGE_SETS_INFO: [
                MessageHandler(Filters.text, dblungeSetsInfo),
            ],
            LEGCURL_REPS_INFO: [
                MessageHandler(Filters.text, legcurlRepsInfo),
            ],
            LEGCURL_WEIGHT_INFO: [
                MessageHandler(Filters.text, legcurlWeightInfo),
            ],
            LEGCURL_SETS_INFO: [
                MessageHandler(Filters.text, legcurlSetsInfo),
            ],

        },
        
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), done)],
    )
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
   # dp.add_handler(CommandHandler("record", record))
   # dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)
    dp.add_handler(push_handler)
    dp.add_handler(pull_handler)
    dp.add_handler(leg_handler)
    dp.add_handler(weight_handler)


   # dp.add_handler(MessageHandler(Filters.text, recordWeight))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
