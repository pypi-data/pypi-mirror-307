from collections import defaultdict


class Channel(object):
    def __init__(self, channel_name, connection, auth=None):
        self.name = channel_name
        self.connection = connection
        self.event_callbacks = defaultdict(list)
        self.auth = auth

    def bind(self, event_name, callback, *args, **kwargs):
        """Bind an event to a callback."""
        self.event_callbacks[event_name].append((callback, args, kwargs))

    def trigger(self, event_name, data):
        """Trigger an event on this channel (for private/presence channels)."""
        if self.connection:
            if event_name.startswith("client-"):
                if self.name.startswith("private-") or self.name.startswith("presence-"):
                    self.connection.send_event(event_name, data, channel_name=self.name)

    def _handle_event(self, event_name, data):
        if event_name in self.event_callbacks:
            for callback, args, kwargs in self.event_callbacks[event_name]:
                callback(data, *args, **kwargs)
