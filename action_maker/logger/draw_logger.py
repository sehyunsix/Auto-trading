import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Sample log data
log_file_path = "example.log"
with open(log_file_path, "r") as file:
    log_data = file.read()
# Parsing the log file
info_pattern = re.compile(
    r"INFO:{'totalMoney': array\(\[([0-9.]+)\], dtype=float32\).*'timeState': datetime.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)}"
)
debug_pattern = re.compile(
    r"DEBUG:action:  {'side': '(\w+)', 'symbol': .*'time': datetime.datetime\((\d+), (\d+), (\d+), (\d+), (\d+)\)}"
)

time_states = []
total_money = []
debug_actions = []

for line in log_data.split("\n"):
    info_match = info_pattern.search(line)
    if info_match:
        total_money.append(float(info_match.group(1)))
        time_states.append(
            datetime(
                int(info_match.group(2)),
                int(info_match.group(3)),
                int(info_match.group(4)),
                int(info_match.group(5)),
                int(info_match.group(6)),
            )
        )

    debug_match = debug_pattern.search(line)
    if debug_match:
        debug_actions.append(
            {
                "side": debug_match.group(1),
                "time": datetime(
                    int(debug_match.group(2)),
                    int(debug_match.group(3)),
                    int(debug_match.group(4)),
                    int(debug_match.group(5)),
                    int(debug_match.group(6)),
                ),
            }
        )


fig, ax = plt.subplots(figsize=(12, 8))


# Formatting the x-axis to show datetime properly
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
plt.xticks(rotation=90)

# Adding labels and title
ax.set_xlabel("Time")
ax.set_ylabel("Total Money")
ax.set_title("Total Money Over Time with Buy/Sell Actions")
ax.legend()
pos = 0
slider_color = "White"
(line_total_money,) = ax.plot(
    time_states[pos : pos + 100],
    total_money[pos : pos + 100],
    label="Total Money",
    color="blue",
)

axis_position = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=slider_color)
slider_position = Slider(axis_position, "Pos", 0.1, 80.0)


def update(val):
    pos = slider_position.val
    pos = int(pos)
    # fig.axis([pos, pos + 100, -1, 1])
    ax.clear()
    # Plot totalMoney over time
    ax.set_xlabel("Time")
    ax.set_ylabel("Total Money")
    ax.set_title("Total Money Over Time with Buy/Sell Actions")
    ax.legend()

    ax.plot(
        time_states[pos : pos + 100],
        total_money[pos : pos + 100],
        label="Total Money",
        color="blue",
    )

    # Plot debug actions as dots
    for action in debug_actions[pos : pos + 100]:
        if action["side"] == "buy":
            if action["time"] in time_states[pos : pos + 100]:
                ax.plot(
                    action["time"],
                    total_money[time_states.index(action["time"])],
                    "go",
                    label=(
                        "Buy" if "Buy" not in ax.get_legend_handles_labels()[1] else ""
                    ),
                )
            else:
                print(f"{action['time']} is not in time_states")

        elif action["side"] == "sell":
            if action["time"] in time_states[pos : pos + 100]:
                ax.plot(
                    action["time"],
                    total_money[time_states.index(action["time"])],
                    "ro",
                    label=(
                        "Sell"
                        if "Sell" not in ax.get_legend_handles_labels()[1]
                        else ""
                    ),
                )
            else:
                print(f"{action['time']} is not in time_states")

    ax.canvas.draw_idle()


slider_position.on_changed(update)

# Show the plot
# plt.tight_layout()
plt.show()
