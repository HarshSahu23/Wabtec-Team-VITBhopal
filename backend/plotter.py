from matplotlib import pyplot as plt
import seaborn as sns
import math

class Plotter:
    def plot_bar_chart(x, y, figsize=(10, 3), xlabel="Errors", ylabel="Frequency"):
        plt.figure(figsize=figsize)
        plt.xlabel(xlabel=xlabel)
        plt.ylabel(ylabel=ylabel)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        ax = sns.barplot(x=x, y=y)

        for p in ax.patches:
            bar_height = p.get_height()
            bar_x_pos = p.get_x()
            bar_width = p.get_width()
            ax.annotate(int(bar_height), (bar_x_pos + bar_width / 2.0, bar_height),  # Position at top of bar
                        ha='center', va='bottom')  # Centered horizontally, slightly above the bar
        plt.show()

    def plot_pie_chart(labels, data, figsize=(10, 10)):
        # Calculate percentages
        total = sum(data)
        percentages = [f"{size/total*100:.1f}%" for size in data]

        # Combine labels with data and percentages
        labels_with_data = [f"{label}\n{size} ({percentage})" for label, size, percentage in zip(labels, data, percentages)]

        # Plotting a flat pie chart
        plt.figure(figsize=figsize)
        plt.pie(data, labels=None, startangle=90, counterclock=False) # Labels with indicating lines are manually added 

        for i, (dataPoint, label) in enumerate(zip(data, labels_with_data)):
            angle = 90 - (sum(data[:i]) + dataPoint / 2) / total * 360  # Calculate the angle
            x = 1.2 * math.cos(angle * math.pi / 180)
            y = 1.2 * math.sin(angle * math.pi / 180)
            plt.text(x, y, label, ha='center', va='center', fontsize=10)
            plt.plot([0, x/1.07], [0, y/1.07], linestyle='solid', linewidth=0.8)  # Line from center to text

        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle.
        plt.show()