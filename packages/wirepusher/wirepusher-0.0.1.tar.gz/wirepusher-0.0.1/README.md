# Wirepusher

Wirepusher is an Android push notification app, which allows sending arbitrary
push notifications (abstracting away all the fuss of Google's push
notifications). The client can be configured to handle different categories of
notification in different ways. See the Wirepusher docs
[here](https://wirepusher.com).

This is an unofficial Python library for Wirepusher. It supports all features
of upstream Wirepusher (encrypted messages, images, actions, etc).

## Basic usage

```python
import wirepusher

wp = wirepusher.Wirepusher(MY_DEVICE_ID, "Test notifications")

wp.send("Test title", "Test message.")
```

## Advanced usage

```python
import wirepusher

# initialise with an encryption key configured on the device
wp = wirepusher.Wirepusher(MY_DEVICE_ID, "Test notifications", MY_PRE_SHARED_KEY)

# send a notification which will go to a URL when clicked and store the ID
mid = wp.send(
    "Test title", "Test message.", action="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

# replace existing notification with one with an image
wp.send(
    "Test title",
    "Test message.",
    mid=mid,
    image="https://wirepusher.com/assets/images/logo.png",
)

# clear notification
wp.clear(mid)
```
