import matplotlib.pyplot as plt
import numpy as np


def create_bar_chart(objects, values, y_label, title):
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def create_bar_chart_horizontal(objects, values, x_label, title):
    y_pos = np.arange(len(objects))
    plt.barh(y_pos, values, align='center', alpha=0.5)
    plt.xlabel(x_label)
    plt.yticks(y_pos, objects)
    plt.title(title)
    plt.show()
