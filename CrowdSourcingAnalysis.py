import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import fbeta_score

# Evaluation fuction from https://colab.research.google.com/drive/1Dc6rlxrsvYd0l8Bph66ydwNV05hBS-CX
def evaluation_summary(description, predictions, true_labels):
  print("Evaluation for: " + description)
  precision = precision_score(true_labels, predictions, average='macro')
  recall = recall_score(true_labels, predictions, average='macro')
  accuracy = accuracy_score(true_labels, predictions)
  f1 = fbeta_score(true_labels, predictions, 1, average='macro') #1 means f_1 measure
  print("Classifier '%s' has Acc=%0.3f P=%0.3f R=%0.3f F1=%0.3f" % (description,accuracy,precision,recall,f1))
  # Specify three digits instead of the default two.
  print(classification_report(true_labels, predictions, digits=3))
  print('\nConfusion matrix:\n',confusion_matrix(true_labels, predictions)) # Note the order here is true, predicted, odd.


cs = pd.read_csv('cs_res.csv')

predicted_label = []
true_label = []
diction = {'happy_positive_feeling': 'happy',
           'pleasant_positive_feeling': 'pleasant',
           'excitement_positive_feeling': 'excitement',
           'surprise_negative_feeling': 'surprise',
           'angry_negative_feeling': 'angry',
           'fear_negative_feeling': 'fear'}

for row in cs.iterrows():
    label = row[1]['label']
    cs_label = row[1]['which_category_best_fits_this_text_']
    true_label.append(diction[cs_label])
    predicted_label.append(label)

evaluation_summary('Crowd Sourcing', predicted_label, true_label)