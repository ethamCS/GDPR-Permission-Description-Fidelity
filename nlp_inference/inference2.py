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

model_path = '/home/roy/Documents/bert'

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('/home/roy/Documents/GDPR-Permission-Description-Fidelity/datatset.csv')

# Create a new DataFrame to store the results
results_df = pd.DataFrame(columns=['App_ID', 'Sentence', 'Predicted Labels', 'Probabilities'])

# Iterate over each row in the DataFrame
for idx, row in df.iterrows():
    app_id = row['App_ID']
    sentence = row['Sentence']

    text = sentence

    encoding = tokenizer(text, return_tensors="pt", max_length=256, truncation=True)
    encoding = {k: v.to(model.device) for k, v in encoding.items()}

    outputs = model(**encoding)

    logits = outputs.logits

    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())

    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1

    predicted_labels = [id2label[idx] for idx, label in enumerate(predictions) if label == 1.0]

    infered_permissions = set(predicted_labels)
    n = {k: label_to_permission[k] for k in infered_permissions if k in label_to_permission}
    n = list(n.values())
    flat_list = [item for sublist in n for item in sublist]

    if len(predicted_labels) != 0:
        # Create a new row with the results
        new_row = {
            'App_ID': [app_id],
            'Sentence': [sentence],
            'Predicted Labels': [predicted_labels],
            'Probabilities': [probs.tolist()]
        }

        
        # Append the new row to results_df using concat
        results_df = pd.concat([results_df, pd.DataFrame(new_row)], ignore_index=True)

        print(sentence)
        print(predicted_labels)
        print(probs)
        print(idx)


# Save the results DataFrame to a new CSV file
results_df.to_csv('/home/roy/Documents/GDPR-Permission-Description-Fidelity/results.csv', index=False)
