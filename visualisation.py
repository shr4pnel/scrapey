import matplotlib.pyplot as plt


def get_bar_graph(x_plot, y_plot, title):
    plt.figure(figsize=(3, 3))
    plt.bar(x_plot, y_plot)
    plt.suptitle(title)
    return plt
