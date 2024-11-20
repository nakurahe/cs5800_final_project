import requests
import csv
from io import StringIO
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split


# Fetch data from site
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Parse CSV data
csv_reader = csv.reader(StringIO(csv_data))
header = next(csv_reader)

# Filter data for British Columbia, Canada
bc_data = [row for row in csv_reader if row[0] == 'British Columbia' and row[1] == 'Canada']

# Combine header with data
bc_data_with_header = [dict(zip(header, row)) for row in bc_data]

# Convert data to a format suitable for training/testing
dates = header[4:]  # Assuming the first 4 columns are not dates
evidence = []
labels = []

for row in bc_data_with_header:
    for date in dates:
        if date.endswith('/23'):
            evidence.append([float(row[date])])
            labels.append(1)  # Assuming label 1 for training data
        else:
            evidence.append([float(row[date])])
            labels.append(0)  # Assuming label 0 for testing data

# Convert lists to NumPy arrays
evidence = np.array(evidence)
labels = np.array(labels)

# Separate data into training and testing groups
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network
model = tf.keras.models.Sequential()

# Add an input layer
model.add(tf.keras.layers.Input(shape=(1,)))

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, activation="relu"))

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
model.fit(X_training, y_training, epochs=20)

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=2)
