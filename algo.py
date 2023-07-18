import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
data_for_modal = pd.read_csv("minipro/urls.csv")
x = data_for_modal.drop(['url', 'type'], axis=1).values
y = data_for_modal['type'].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=500)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)
with open('classification.pkl', 'wb') as file:
    pickle.dump(model, file)
