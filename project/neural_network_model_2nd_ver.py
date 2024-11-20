import requests
import csv
from io import StringIO
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Fetch data from site
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Parse CSV data
csv_reader = csv.reader(StringIO(csv_data))
header = next(csv_reader)

# Filter data for Canada
canada_covid_data = [row for row in csv_reader if row[1] == 'Canada']

# Combine header with data
canada_covid_data_with_header = [dict(zip(header, row)) for row in canada_covid_data]

# Convert data to a format suitable for training/testing
dates = header[4:]  # Dates start from the 5th column
data_for_train = []
data_for_test = []

for row in canada_covid_data_with_header:
    if row['Province/State'] != 'British Columbia':
        for date in dates:
            data_for_train.append(float(row[date]))
    else:
        for date in dates:
            data_for_test.append(float(row[date]))

# Convert lists to NumPy arrays and reshape to (number_of_samples, number_of_features)
data_for_train = np.array(data_for_train).reshape(-1, 1)
data_for_test = np.array(data_for_test).reshape(-1, 1)


# Define a custom accuracy function
def custom_accuracy(y_true, y_pred):
    return tf.reduce_mean(tf.cast(tf.abs(y_true - y_pred) < 0.1 * tf.abs(y_true), tf.float32))


# Create a neural network
model = tf.keras.models.Sequential()

# Add an input layer
model.add(tf.keras.layers.Input(shape=(1,)))

# Add hidden layers with more units and ReLU activation
model.add(tf.keras.layers.Dense(64, activation="relu"))
model.add(tf.keras.layers.Dense(32, activation="relu"))
model.add(tf.keras.layers.Dense(16, activation="relu"))

# Add output layer with 1 unit, with linear activation
model.add(tf.keras.layers.Dense(1, activation="linear"))

# Compile the model
model.compile(
    optimizer="adam",
    loss="mean_squared_error",
    metrics=[custom_accuracy]
)

# Enable interactive mode
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the actual data
ax.plot(data_for_test, label='Actual Data', color='orange')

# Store predictions after each epoch
predictions_per_epoch = []


class PredictionCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        predictions = model.predict(data_for_test)
        predictions_per_epoch.append(predictions)
        # Clear the output and plot the predictions after each epoch
        clear_output(wait=True)
        ax.clear()
        ax.plot(data_for_test, label='Actual Data', color='orange')
        ax.plot(predictions, label='Predicted Data', color='blue')
        ax.set_title(f'Actual vs Predicted Data (Epoch {epoch + 1})')
        ax.set_xlabel('Days')
        ax.set_ylabel('Confirmed Cases')
        ax.legend()
        plt.draw()
        plt.pause(0.01)


# Train the neural network
history = model.fit(data_for_train, data_for_train, epochs=50, batch_size=32, verbose=0, callbacks=[PredictionCallback()])

# Evaluate how well the model performs
loss, accuracy = model.evaluate(data_for_test, data_for_test, verbose=2)
print(f"Mean Squared Error on test data: {loss}")
print(f"Custom Accuracy on test data: {accuracy}")

# Disable interactive mode
plt.ioff()
plt.show()
