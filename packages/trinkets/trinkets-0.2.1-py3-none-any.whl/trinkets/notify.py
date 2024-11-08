import requests
import keyring


def send_notification(message, priority=0, image_path=None):
    """
    Sends a notification via the Pushover api, with an optional image attachment.

    Usernames ``token``, ``user``, ``device`` **must** be specified in the system keyring backend, under the
    ``Pushover`` service. See https://pushover.net/api for details.

    :param message: Message to send in notification.
    :param priority: [Optional] Notification priority. See https://pushover.net/api for details.
    :param image_path: [Optional] Path to image to attach to notification.
    :return:
    """
    url = 'https://api.pushover.net/1/messages.json'
    params = {
        'token': keyring.get_password('Pushover', 'token'),
        'user': keyring.get_password('Pushover', 'user'),
        'device': keyring.get_password('Pushover', 'device'),
        'message': message,
        'priority': priority
    }
    files = {
        'attachment': ('img', open(image_path, 'rb'))
    } if image_path else {}

    r = requests.post(url=url, data=params, files=files)
