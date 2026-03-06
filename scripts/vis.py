from google.colab import drive
drive.mount('/content/drive')

import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_PATH = "/content/drive/MyDrive/Colab Notebooks/breathing_project"
DATA_PATH = os.path.join(BASE_PATH, "Data")
VIS_PATH = os.path.join(BASE_PATH, "Visualizations")

os.makedirs(VIS_PATH, exist_ok=True)


def load_signal(file_path):
    df = pd.read_csv(
        file_path,
        sep=";",
        skiprows=7,
        header=None,
        names=["timestamp", "value"]
    )
    df["timestamp"] = df["timestamp"].str.replace(",", ".", regex=False)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d.%m.%Y %H:%M:%S.%f"
    )
    return df


def load_events(file_path):
    df = pd.read_csv(
        file_path,
        sep=";",
        skiprows=5,
        header=None,
        names=["time_range", "duration", "event_type", "sleep_stage"]
    )

    df[["start_raw", "end_raw"]] = df["time_range"].str.split("-", expand=True)

    df["start_raw"] = df["start_raw"].str.replace(",", ".", regex=False)
    df["start_time"] = pd.to_datetime(
        df["start_raw"],
        format="%d.%m.%Y %H:%M:%S.%f"
    )

    df["date"] = df["start_time"].dt.strftime("%d.%m.%Y")
    df["end_raw"] = df["end_raw"].str.replace(",", ".", regex=False)

    df["end_time"] = pd.to_datetime(
        df["date"] + " " + df["end_raw"],
        format="%d.%m.%Y %H:%M:%S.%f"
    )

    return df


for participant in sorted(os.listdir(DATA_PATH)):

    folder_path = os.path.join(DATA_PATH, participant)

    if not os.path.isdir(folder_path):
        continue

    print("Generating PDF for:", participant)

    files = os.listdir(folder_path)

    airflow_file = None
    thoracic_file = None
    spo2_file = None
    events_file = None

    for f in files:
        name = f.lower()
        if "flow events" in name:
            events_file = f
        elif "flow" in name and "event" not in name:
            airflow_file = f
        elif "thorac" in name:
            thoracic_file = f
        elif "spo2" in name:
            spo2_file = f

    if None in [airflow_file, thoracic_file, spo2_file, events_file]:
        print("Skipping (missing files):", participant)
        continue

    df_airflow = load_signal(os.path.join(folder_path, airflow_file))
    df_thoracic = load_signal(os.path.join(folder_path, thoracic_file))
    df_spo2 = load_signal(os.path.join(folder_path, spo2_file))
    df_events = load_events(os.path.join(folder_path, events_file))

    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    plt.plot(df_airflow["timestamp"], df_airflow["value"])
    plt.title("Nasal Airflow")
    for _, event in df_events.iterrows():
        plt.axvspan(event["start_time"], event["end_time"],
                    color="red", alpha=0.2)

    plt.subplot(3, 1, 2)
    plt.plot(df_thoracic["timestamp"], df_thoracic["value"])
    plt.title("Thoracic Movement")

    plt.subplot(3, 1, 3)
    plt.plot(df_spo2["timestamp"], df_spo2["value"])
    plt.title("SpO2")
    plt.xlabel("Time")

    plt.tight_layout()

    output_path = os.path.join(VIS_PATH,
                               f"{participant}_visualization.pdf")

    plt.savefig(output_path)
    plt.close()

print("\nAll PDFs generated.")
