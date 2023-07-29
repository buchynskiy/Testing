from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.chataction import ChatAction
from dotenv import load_dotenv
import pyshorteners
import os

load_dotenv()
PORT = int(os.environ.get('PORT', 5000))
APIKEY = os.environ.get('APIKEY')
TOKEN = APIKEY

# Needed variables
actualInsert = 0
listInsert = []
isInserting = False

def shorten(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    listInsert.clear()
    resetActualInsert()
    isInsertingSetTrue()
    
    update.message.reply_text('''Please, choose a url shortener:\n
1. Bitly
2. Isgd
3. Clckru

Send only the number from above list \U00002757''')

def expand(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    listInsert.clear()
    resetActualInsert()
    isInsertingSetTrue()
    
    update.message.reply_text('''Please, choose a url expander:\n
4. Bitly 
5. Isgd
6. Clckru

Send only the number from above list \U00002757''')

def insertLink(update: Update, context: CallbackContext) -> None:
    #If the flag is false it means that there are no previous '/command' 
    #so no number has to be kept
    if isInserting:
        #message inserted by the user
        listInsert.append(update.message.text)
        message = ""
        
        #depending on the actualInsert, a different message is sent
        if actualInsert == 0:
            shorten_list = ['1','2','3']
            expanding_list = ['4','5','6']
            if listInsert[0] in shorten_list:
                message = 'You can now provide a link for shortening process'
            elif listInsert[0] in expanding_list:
                message = 'You can now provide a link for expanding process'
            else:
                message = 'You can now provide a link now'
        elif actualInsert == 1:
            if listInsert[0] == '1':
                url = listInsert[1]
                tool = pyshorteners.Shortener(api_key='50695f0ac88061f08c249be89ab091106e0f09ea')
                result = tool.bitly.short(f'{url}')
                update.message.reply_text(f'Your shortened link is:\n{result}')
            elif listInsert[0] == '2':
                url = listInsert[1]
                tool = pyshorteners.Shortener()
                result = tool.isgd.short(f'{url}')
                update.message.reply_text(f'Your shortened link is:\n{result}')
            elif listInsert[0] == '3':
                url = listInsert[1]
                tool = pyshorteners.Shortener()
                result = tool.clckru.short(f'{url}')
                update.message.reply_text(f'Your shortened link is:\n{result}')
            elif listInsert[0] == '4':
                url_test = 'https://bit.ly/'
                real_url = listInsert[1]
                if real_url[0:15] == url_test:
                    url = listInsert[1]
                    tool = pyshorteners.Shortener(api_key='50695f0ac88061f08c249be89ab091106e0f09ea')
                    result = tool.bitly.expand(f'{url}')
                    update.message.reply_text(f'Your expanded link is:\n{result}')
                else:
                    update.message.reply_text('Use only bitly links.\nPlease start again /expand')
            elif listInsert[0] == '5':
                url_test = 'https://is.gd/'
                real_url = listInsert[1]
                if real_url[0:14] == url_test:
                    url = listInsert[1]
                    tool = pyshorteners.Shortener()
                    result = tool.isgd.expand(f'{url}')
                    update.message.reply_text(f'Your expanded link is:\n{result}')
                else:
                    update.message.reply_text('Use only Isgd links.\nPlease start again /expand')
            elif listInsert[0] == '6':
                url_test = 'https://clck.ru/'
                real_url = listInsert[1]
                if real_url[0:16] == url_test:
                    url = listInsert[1]
                    tool = pyshorteners.Shortener()
                    result = tool.clckru.expand(f'{url}')
                    update.message.reply_text(f'Your expanded link is:\n{result}')
                else:
                    update.message.reply_text('Use only Clckru links.\nPlease start again /expand')
            else:
                update.message.reply_text('An error occurred, please start again /start')

        increaseActualInsert()
        update.message.reply_text(message)

def resetActualInsert():
    global actualInsert 
    actualInsert = 0

def increaseActualInsert():
    global actualInsert
    actualInsert = actualInsert + 1

def isInsertingSetTrue():
    global isInserting
    isInserting = True

def isInsertingSetFalse():
    global isInserting
    isInserting = False


def main() -> None:

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, insertLink))
    dp.add_handler(CommandHandler('shorten', shorten))
    dp.add_handler(CommandHandler('expand', expand))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://urlshortenbot.herokuapp.com/' + TOKEN)


if __name__ == '__main__':
    main()