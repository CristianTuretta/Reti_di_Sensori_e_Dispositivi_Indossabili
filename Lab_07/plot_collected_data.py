import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    recording_name = "sensor_data.csv"

    # Read the data from the file
    df = pd.read_csv(
        recording_name,
        header=None,
        names=["time", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"],
        index_col=0,
        parse_dates=True
    )

    # Define the figure and the subplots
    fig, (accelerometer_fig, gyroscope_fig) = plt.subplots(2, 1, figsize=(16, 10))

    # Plot Acc
    accelerometer_fig.plot(df["acc_x"], color="red", label="X")
    accelerometer_fig.plot(df["acc_y"], color="green", label="Y")
    accelerometer_fig.plot(df["acc_z"], color="blue", label="Z")
    accelerometer_fig.set_ylabel("Magnitude")
    accelerometer_fig.set_title("Accelerometer Data")
    accelerometer_fig.legend()

    # Plot Gyr
    gyroscope_fig.plot(df["gyro_x"], color="cyan", label="X")
    gyroscope_fig.plot(df["gyro_y"], color="magenta", label="Y")
    gyroscope_fig.plot(df["gyro_z"], color="yellow", label="Z")

    gyroscope_fig.set_xlabel("Time")
    gyroscope_fig.set_ylabel("Magnitude")
    gyroscope_fig.set_title("Gyroscope Data")
    gyroscope_fig.legend()

    fig.suptitle("Accelerometer and Gyroscope Data", fontsize=18, fontweight="bold")
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5, top=0.88)
    # plt.subplots_adjust(top=0.88)

    plt.savefig("collected_data_overview.png", dpi=300)
    plt.show()
