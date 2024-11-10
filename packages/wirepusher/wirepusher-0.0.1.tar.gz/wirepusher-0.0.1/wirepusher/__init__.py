import base64
import hashlib
import random
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests


class WirepusherException(Exception):
    """Exception raised after failed requests.

    Includes the JSON response from the server as the `response` property.
    This should have an `'error'` key if the request was invalid, and if not
    will tell you how many deliveries failed in the `'errors'` key with details
    in the `'results'` key.
    """

    def __init__(self, msg: str, response: dict):
        super().__init__(msg)
        self.response = response


class Wirepusher:
    """Class for sending Wirepusher notifications to a device or set of devices."""

    alpha = str.maketrans({"+": "-", "/": ".", "=": "_"})

    def __init__(self, deviceid: str, messagetype: str | None, key: str | None = None):
        """Create a notifier.

        Params:

        `deviceid`: ID of device to send to, or up to five comma-separated
            device IDs.
        `messagetype`: Category of notification to send (allows configuring
            different behaviour client-side). Optional, human-readable string.
        `key`: Pre-shared encryption key. Optional, string as configured in
            client.
        """
        self.deviceid = deviceid
        if key:
            self.key = self.hash_password(key)
        else:
            self.key = None
        self.messagetype = messagetype

    def b64encode(self, val: bytes) -> str:
        return base64.b64encode(val).decode("ascii").translate(self.alpha)

    def hash_password(self, pwd: str) -> str:
        return hashlib.sha1(pwd.encode("utf8")).digest()[:16]

    def encrypt(self, msg: str, iv: bytes) -> str:
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        return self.b64encode(aes.encrypt(pad(msg.encode("utf8"), 16)))

    def encrypt_message(self, args: dict) -> None:
        iv = secrets.token_bytes(16)
        args["iv"] = iv.hex()
        args["title"] = self.encrypt(args["title"], iv)
        args["message"] = self.encrypt(args["message"], iv)

    def send(
        self,
        title: str,
        message: str,
        mid: int | None = None,
        action: str | None = None,
        image: str | None = None,
        trim: bool = False,
    ) -> int:
        """Send a notification.

        Params:

        `title`: Notification title.
        `message`: Notification body.
        `mid`: Message ID, to allow overwriting existing notifications.
            Optional, will be randomly generated if not supplied.
        `action`: URL to open when notification is clicked. Optional.
        `image`: Publicly accessible URL of image to display in notification.
            Optional. Should be about 2:1 aspect ratio for best results.
        `trim`: If set, silently truncate over-long message bodies. Otherwise,
            raise an exception (the default).

        Returns the message ID of the sent notification.
        """
        mid = mid or random.randrange(2**32)
        if len(message) > 2975:
            if trim:
                message = message[:2975]
            else:
                raise ValueError("message too long")
        args = {
            "message_id": mid,
            "title": title,
            "message": message,
            "id": self.deviceid,
        }
        if self.messagetype:
            args["mtype"] = self.messagetype
        if self.key:
            self.encrypt_message(args)
        if action:
            args["action"] = action
        if image:
            args["image_url"] = image
        res = requests.get("https://wirepusher.com/send", params=args, timeout=30)
        j = res.json()
        # There's some API inconsistency here where successful requests get
        # errors: 0 in the JSON, but failed ones get error: somemsg and *not*
        # the errors key. Make sure we handle either, just in case.
        if "error" in j:
            raise WirepusherException(f"request failed: {j['error']}", j)
        if "errors" in j and j["errors"] != 0:
            raise WirepusherException(f"request failed: {j}", j)
        return mid

    def clear(self, mid: int) -> None:
        """Clear a previously sent notification.

        Params:

        `mid`: The ID of the message to remove (returned from `send()`).
        """
        requests.get(
            "https://wirepusher.com/send",
            params={
                "id": self.deviceid,
                "type": "wirepusher_clear_notification",
                "message_id": mid,
            },
            timeout=30,
        )
