from nltk.tokenize import sent_tokenize
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from transformers import AutoTokenizer
from transformers import pipeline
from setfit import SetFitModel, SetFitTrainer, sample_dataset
from transformers import AutoModelForSequenceClassification
import torch
import numpy as np
from google_play_scraper import app
from google_play_scraper import permissions
import pandas as pd
# import nltk
# nltk.download('punkt')

labels = ['STORAGE',
          'CONTACTS',
          'LOCATION',
          'CAMERA',
          'MICROPHONE',
          'SMS',
          'CALL_LOG',
          'PHONE',
          'CALENDAR',
          'SETTINGS',
          'TASKS']

label_to_permission = {
    'STORAGE': ["WRITE_EXTERNAL_STORAGE", "READ_EXTERNAL_STORAGE"],
    'CONTACTS': ["GET_ACCOUNTS", "READ_CONTACTS", "WRITE_CONTACTS"],
    'LOCATION': ["ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION"],
    'CAMERA': ["CAMERA"],
    'MICROPHONE': ["RECORD_AUDIO"],
    'SMS': ["READ_SMS", "SEND_SMS"],
    'CALL_LOG': ["READ_CALL_LOG"],
    'PHONE': ["CALL_PHONE"],
    'CALENDAR': ["READ_CALENDAR"],
    'SETTINGS': ["WRITE_SETTINGS"],
    'TASKS': ["GET_TASKS", "KILL_BACKGROUND_PROCESS"]
}

id2label = {idx: label for idx, label in enumerate(labels)}

tokenizer = AutoTokenizer.from_pretrained('etham13/permissions_bert_uncased')

model = AutoModelForSequenceClassification.from_pretrained(
    "etham13/permissions_bert_uncased")


# TODO:
# read created csv into a pandas df


count = 0
labelss = []

for token in tokens:
    text = token

    encoding = tokenizer(text, return_tensors="pt", max_length=256,
                         truncation=True)
    encoding = {k: v.to(model.device) for k, v in encoding.items()}

    outputs = model(**encoding)

    logits = outputs.logits
    logits.shape

    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())

    predictions = np.zeros(probs.shape)

    predictions[np.where(probs >= 0.5)] = 1

    # turn predicted id's into actual label names
    predicted_labels = [id2label[idx]
                        for idx, label in enumerate(predictions) if label == 1.0]

    if len(predicted_labels) != 0:
        labelss.extend(predicted_labels)
        print(token)
        print(predicted_labels)
        print(probs)
        print(count)
    count = count + 1


infered_permissions = set(labelss)
n = {k: label_to_permission[k]
     for k in infered_permissions if k in label_to_permission}
n = list(n.values())
flat_list = [item for sublist in n for item in sublist]


### AC-Net Example
# description = """Works with Gmail, Exchange, Yahoo, Outlook, iCloud, Google Apps, Office 365 and any IMAP account!
# Accolades:
# ★ "Winner of the Internet's highest honor" - The Webby Awards People's Voice. "The best mobile email app" - The Wall Street Journal.
# Feature List:
# • Connected with your favorite tools. Save emails to Wunderlist, Todoist, Evernote, OneNote, Trello, Zendesk, Salesforce.com, Asana, Instapaper, OmniFocus and many more apps.
# • Attach files from Dropbox, iCloud Drive and other file storage services.
# • Download attachments in background."""
