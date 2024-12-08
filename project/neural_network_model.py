import requests
import csv
from io import StringIO
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import clear_output

# Fetch data from site
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
response = requests.get(url)
csv_data = response.content.decode("utf-8")

# Parse CSV data
csv_reader = csv.reader(StringIO(csv_data))
header = next(csv_reader)

# Filter data for Canada
canada_covid_data = [row for row in csv_reader if row[1] == "Canada"]

# Combine header with data
canada_covid_data_with_header = [dict(zip(header, row)) for row in canada_covid_data]

# Convert data to a format suitable for training/testing
dates = header[4:]  # Dates start from the 5th column

# Separate data for each province
province_data = {}
for row in canada_covid_data_with_header:
    province = row["Province/State"]
    if province not in province_data:
        province_data[province] = []
    for date in dates:
        province_data[province].append(float(row[date]))

# Separate BC data and other provinces' data
bc_data = np.array(province_data.pop("British Columbia")).reshape(-1, 1)
other_provinces_data = list(province_data.values())
other_provinces_names = list(province_data.keys())


# Define a custom accuracy function
def custom_accuracy(y_true, y_pred):
    return tf.reduce_mean(
        tf.cast(tf.abs(y_true - y_pred) < 0.05 * tf.abs(y_true), tf.float32)
    )


# Function to create and compile a model
def create_model():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input(shape=(1,)))
    model.add(tf.keras.layers.Dense(64, activation="relu"))
    model.add(tf.keras.layers.Dense(32, activation="relu"))
    model.add(tf.keras.layers.Dense(16, activation="relu"))
    model.add(tf.keras.layers.Dense(1, activation="linear"))
    model.compile(
        optimizer="adam", loss="mean_squared_error", metrics=[custom_accuracy]
    )
    return model


# Enable interactive mode
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))


class PredictionCallback(tf.keras.callbacks.Callback):
    def __init__(self, data_for_test, ax, province_name, province_data):
        super().__init__()
        self.data_for_test = data_for_test
        self.ax = ax
        self.province_name = province_name
        self.province_data = province_data

    def on_epoch_end(self, epoch, logs=None):
        predictions = self.model.predict(self.data_for_test)
        # Clear the output and plot the predictions after each epoch
        clear_output(wait=True)
        ax.clear()
        ax.plot(
            self.province_data,
            label=f"Actual Data (Province {self.province_name})",
            color="orange",
        )
        ax.plot(
            self.data_for_test,
            label="BC Actual Data",
            color="green",
            linestyle="dashed",
            linewidth=2,
        )
        ax.plot(predictions, label="BC Predicted Data", color="blue")
        ax.set_title(f"BC Actual vs Predicted Data (Trained with {self.province_name})")
        ax.set_xlabel("Days")
        ax.set_ylabel("Confirmed Cases")
        ax.legend()
        plt.draw()
        plt.pause(0.01)


# Train and evaluate the model for each province and predict BC's condition
for i, (data_for_train, province_name) in enumerate(
    zip(other_provinces_data, other_provinces_names)
):
    print(f"Training model with data from {province_name}...")

    # Convert lists to NumPy arrays and reshape to (number_of_samples, number_of_features)
    data_for_train = np.array(data_for_train).reshape(-1, 1)

    # Create and compile the model
    model = create_model()

    # Train the neural network
    history = model.fit(
        data_for_train,
        data_for_train,
        epochs=50,
        batch_size=32,
        verbose=0,
        callbacks=[PredictionCallback(bc_data, ax, province_name, data_for_train)],
    )

    # Evaluate how well the model performs
    loss, accuracy = model.evaluate(bc_data, bc_data, verbose=2)
    print(f"Mean Squared Error on BC data: {loss}")
    print(f"Custom Accuracy on BC data: {accuracy}")

# Disable interactive mode
plt.ioff()
plt.show()
