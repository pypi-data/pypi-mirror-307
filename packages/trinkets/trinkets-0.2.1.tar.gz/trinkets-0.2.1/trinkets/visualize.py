import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from trinkets.notify import send_notification


def plot_with_metrics(X, Y, title=None, x_label=None, y_label=None, metrics=None, save=True, directory=None,
                      timestamp=True, notify=False):
    """
    Creates a plot with supplied metrics listed next to plot. Optionally saves figure.

    :param X: Independent data.
    :param Y: Dependent data.
    :param title: [Optional] Plot title.
    :param x_label: [Optional] X axis label.
    :param y_label: [Optional] Y axis label.
    :param metrics: [Optional] Dictionary of metrics to include next to plot.
    :param save: [Optional] Save produced figure. Uses title as file name.
    :param directory: [Optional] Directory to save in. Will be created if necessary. If no directory specified, figure will be output to current working directory.
    :param timestamp: [Optional] Automatically append timestamp to filename.
    :param notify: [Optional] Send notification when done. See ``Notify.send_notification`` for details.
    :return: None
    """
    plt.figure()
    plt.plot(X, Y)

    if title:
        plt.title(title)
    else:
        title = 'Unnamed Figure'
        timestamp = True

    if x_label:
        plt.xlabel(x_label)

    if y_label:
        plt.ylabel(y_label)

    if metrics:
        label = ''
        for key in metrics:
            label += f'{key}: {metrics[key]}\n'

        plt.figtext(0.95, 0.5, label[:-1], bbox=dict(boxstyle="round", fc="0.8"))

    if save:
        directory = Path(directory) if directory is not None else Path()
        directory.mkdir(parents=True, exist_ok=True)

        filename = title

        for char in '<>:"/\|?* ':
            filename = filename.replace(char, '_')

        if timestamp:
            filename += '_' + datetime.now().strftime('%H-%M-%S-%f')

        filename = Path.with_suffix(Path(filename), '.png')

        plt.savefig(Path(directory, filename), bbox_inches='tight')

    if notify:
        under_size_limit = Path(directory, filename).stat().st_size < 5242880 if save else False
        send_notification(f'Plot saved: {title}',
                          image_path=Path(directory, filename) if save and under_size_limit else None)
