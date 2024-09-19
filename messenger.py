
import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

def generalComplaint():
	link = 'https://docs.google.com/forms/d/e/1FAIpQLSeW9-kbH8RabAyQBe9tFBidxRX-ReM7yoACJiB-46xZt028Gw/viewform'
	message = 'If you have a general complaint, please, fill in the <a href="{}">online form</a>.'.format(link)
	return message

def orderNotReceived():
	link = 'https://docs.google.com/forms/d/e/1FAIpQLSfjis1IsVRoDthM6xUtbQS98c2gVPVZ61mi6QqP4Ma5WDESbA/viewform'
	message = 'Please, search the information on the <a href="{}">delivery tracking system</a>.'.format(link)
	return message

def reDelivery(user_name):
	link = 'https://docs.google.com/forms/d/e/1FAIpQLSeW9-kbH8RabAyQBe9tFBidxRX-ReM7yoACJiB-46xZt028Gw/viewform'
	message = 'Dear {}, fill the <a href="{}">online form</a>.'.format(user_name, link)
	message += 'Ordered goods will be delivered in 5 days. Thank you for the request! We are always glad to help.'
	return message

def reFund(user_name):
	link = 'https://docs.google.com/forms/d/e/1FAIpQLSeW9-kbH8RabAyQBe9tFBidxRX-ReM7yoACJiB-46xZt028Gw/viewform'
	message = 'Dear {}, fill the <a href="{}">online form</a>.'.format(user_name, link)
	message += 'Refund will be processed according to our refund policy. Thank you for the request! Our customer support team will contact you soon.'
	return message
