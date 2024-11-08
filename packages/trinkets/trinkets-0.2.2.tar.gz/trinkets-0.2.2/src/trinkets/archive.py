from pickle import dump, load
from pathlib import Path
from datetime import datetime
from trinkets.notify import send_notification
from yaml import safe_load, safe_dump


def pickle_save(variable, filename, directory=None, notify=False, timestamp=False):
    """
    Saves a given variable to a pickle file. 
    
    :param variable: Variable to save.
    :param filename: Filename. Will automatically save as a ``.pkl`` file regardless of (lack of) extension in supplied filename.
    :param directory: [Optional] Directory to save in. Will be created if necessary. If no directory specified, pickle file will be output to current working directory.
    :param notify: [Optional] Send notification when done. See ``Notify.send_notification`` for details.
    :param timestamp: [Optional] Automatically append timestamp to filename.
    :return: None
    """
    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(Path(filename).stem + '_' + datetime.now().strftime('%H-%M-%S')),
                                '.pkl') if timestamp else Path.with_suffix(Path(filename), '.pkl')

    try:
        with Path(directory, filename).open('wb') as file:
            dump(variable, file)

    except Exception as e:
        if notify:
            send_notification(f'Error saving {filename}: {e}')
        return

    if notify:
        send_notification(f'Saved {filename}')


def pickle_load(filename, directory=None, notify=False):
    """
    Loads a pickle file.
    
    :param filename: Filename.
    :param directory: [Optional] Directory where file is stored. If no directory specified, will load from current working directory. 
    :param notify: [Optional] Send notification when done. See ``Notify.send_notification`` for details.
    :return: Loaded variable.
    """
    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(filename), '.pkl')

    if Path(directory, filename).exists():
        try:
            with Path(directory, filename).open('rb') as file:
                variable = load(file)

        except Exception as e:
            if notify:
                send_notification(f'Error loading {filename}: {e}')
            return None

        if notify:
            send_notification(f'Loaded {filename}')

    else:
        if notify:
            send_notification(f'Unable to read {filename} because it doesn\'t exist.')
        return None

    return variable


def yaml_save(variable, filename, directory=None, notify=False, timestamp=False):
    """
    Saves a dictionary of metrics to a yml file.

    :param variable: Variable to save.
    :param filename: Filename. Will automatically save as a ``.pkl`` file regardless of (lack of) extension in supplied filename.
    :param directory: [Optional] Directory to save in. Will be created if necessary. If no directory specified, pickle file will be output to current working directory.
    :param notify: [Optional] Send notification when done. See ``Notify.send_notification`` for details.
    :param timestamp: [Optional] Automatically append timestamp to filename.
    :return: None
    """
    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(Path(filename).stem + '_' + datetime.now().strftime('%H-%M-%S')),
                                '.yml') if timestamp else Path.with_suffix(Path(filename), '.yml')

    try:
        with Path(directory, filename).open('w') as file:
            safe_dump(variable, file)

    except Exception as e:
        if notify:
            send_notification(f'Error saving {filename}: {e}')
        return

    if notify:
        send_notification(f'Saved {filename}')


def yaml_load(filename, directory=None, notify=False):
    """
    Loads a yaml file.

    :param filename: Filename.
    :param directory: [Optional] Directory where file is stored. If no directory specified, will load from current working directory.
    :param notify: [Optional] Send notification when done. See ``Notify.send_notification`` for details.
    :return: Loaded variable.
    """
    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(filename), '.yml')

    if Path(directory, filename).exists():
        try:
            with Path(directory, filename).open('r') as file:
                variable = safe_load(file)

        except Exception as e:
            if notify:
                send_notification(f'Error loading {filename}: {e}')
            return None

        if notify:
            send_notification(f'Loaded {filename}')

    else:
        if notify:
            send_notification(f'Unable to read {filename} because it doesn\'t exist.')
        return None

    return variable
