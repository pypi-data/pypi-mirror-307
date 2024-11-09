import sched
from threading import Thread
from collections import defaultdict
import websocket
import logging
import time
import json

class Connection(Thread):
    def __init__(self, event_handler, url, reconnect_handler=None, log_level=None,
                 daemon=True, reconnect_interval=10, socket_kwargs=None, **thread_kwargs):
        super(Connection, self).__init__(**thread_kwargs)
        self.event_handler = event_handler
        self.url = url
        self.reconnect_handler = reconnect_handler or (lambda: None)
        self.socket = None
        self.socket_id = ""
        self.event_callbacks = defaultdict(list)
        self.disconnect_called = False
        self.needs_reconnect = False
        self.default_reconnect_interval = reconnect_interval
        self.reconnect_interval = reconnect_interval
        self.socket_kwargs = socket_kwargs or {}
        self.pong_timer = None
        self.pong_received = False
        self.pong_timeout = 30

        self.bind("pusher:connection_established", self._connect_handler)
        self.bind("pusher:connection_failed", self._failed_handler)
        self.bind("pusher:pong", self._pong_handler)
        self.bind("pusher:ping", self._ping_handler)
        self.bind("pusher:error", self._pusher_error_handler)

        self.state = "initialized"
        self.logger = logging.getLogger(self.__module__)
        if log_level:
            self.logger.setLevel(log_level)
            if log_level == logging.DEBUG:
                websocket.enableTrace(True)

        self.connection_timeout = 305
        self.connection_timer = None
        self.ping_interval = 120
        self.ping_timer = None
        self.timeout_scheduler = sched.scheduler(time.time, sleep_max_n(min([self.pong_timeout, self.connection_timeout, self.ping_interval])))
        self.timeout_scheduler_thread = None
        self.daemon = daemon
        self.name = "PysherEventLoop"

    def bind(self, event_name, callback, *args, **kwargs):
        """Bind an event to a callback."""
        self.event_callbacks[event_name].append((callback, args, kwargs))

    def disconnect(self, timeout=None):
        self.needs_reconnect = False
        self.disconnect_called = True
        if self.socket:
            self.socket.close()
        self.join(timeout)

    def reconnect(self, reconnect_interval=None):
        if reconnect_interval is None:
            reconnect_interval = self.default_reconnect_interval
        self.logger.info("Connection: Reconnect in %s" % reconnect_interval)
        self.reconnect_interval = reconnect_interval
        self.needs_reconnect = True
        if self.socket:
            self.socket.close()

    def run(self):
        self._connect()

    def _connect(self):
        self.state = "connecting"
        self.socket = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self.socket.run_forever(**self.socket_kwargs)
        while self.needs_reconnect and not self.disconnect_called:
            self.logger.info("Attempting to connect again in %s seconds." % self.reconnect_interval)
            self.state = "unavailable"
            time.sleep(self.reconnect_interval)
            self.socket.keep_running = True
            self.socket.run_forever(**self.socket_kwargs)

    def _on_open(self, *args):
        self.logger.info("Connection: Connection opened")
        self.send_ping()
        self._start_timers()

    def _on_error(self, *args):
        self.logger.info("Connection: Error - %s" % args[-1])
        self.state = "failed"
        self.needs_reconnect = True

    def _on_message(self, *args):
        message = args[-1]
        self.logger.info("Connection: Message - %s" % message)
        self._stop_timers()
        params = self._parse(message)
        if 'event' in params:
            if 'channel' not in params:
                if params['event'] in self.event_callbacks:
                    for func, args, kwargs in self.event_callbacks[params['event']]:
                        try:
                            func(params.get('data', None), *args, **kwargs)
                        except Exception:
                            self.logger.exception("Callback raised unhandled")
                else:
                    self.logger.info("Connection: Unhandled event")
            else:
                self.event_handler(params['event'], params.get('data'), params['channel'])
        self._start_timers()

    def _on_close(self, *args):
        self.logger.info("Connection: Connection closed")
        self.state = "disconnected"
        self._stop_timers()

    @staticmethod
    def _parse(message):
        return json.loads(message)

    def _stop_timers(self):
        for event in self.timeout_scheduler.queue:
            self._cancel_scheduler_event(event)

    def _start_timers(self):
        self._stop_timers()
        self.ping_timer = self.timeout_scheduler.enter(self.ping_interval, 1, self.send_ping)
        self.connection_timer = self.timeout_scheduler.enter(self.connection_timeout, 2, self._connection_timed_out)
        if not self.timeout_scheduler_thread or not self.timeout_scheduler_thread.is_alive():
            self.timeout_scheduler_thread = Thread(target=self.timeout_scheduler.run, name="PysherScheduler")
            self.timeout_scheduler_thread.start()

    def _cancel_scheduler_event(self, event):
        try:
            self.timeout_scheduler.cancel(event)
        except ValueError:
            self.logger.info('Connection: Scheduling event already cancelled')

    def send_event(self, event_name, data, channel_name=None):
        """Send an event to the Pusher server."""
        event = {'event': event_name, 'data': data}
        if channel_name:
            event['channel'] = channel_name
        self.logger.info("Connection: Sending event - %s" % event)
        try:
            self.socket.send(json.dumps(event))
        except Exception as e:
            self.logger.error("Failed send event: %s" % e)

    def send_ping(self):
        self.logger.info("Connection: ping to pusher")
        try:
            self.socket.send(json.dumps({'event': 'pusher:ping', 'data': ''}))
        except Exception as e:
            self.logger.error("Failed send ping: %s" % e)
        self.pong_timer = self.timeout_scheduler.enter(self.pong_timeout, 3, self._check_pong)

    def send_pong(self):
        self.logger.info("Connection: pong to pusher")
        try:
            self.socket.send(json.dumps({'event': 'pusher:pong', 'data': ''}))
        except Exception as e:
            self.logger.error("Failed send pong: %s" % e)

    def _check_pong(self):
        self._cancel_scheduler_event(self.pong_timer)
        if self.pong_received:
            self.pong_received = False
        else:
            self.logger.info("Did not receive pong in time.  Will attempt to reconnect.")
            self.state = "failed"
            self.reconnect()

    def _connect_handler(self, data):
        parsed = json.loads(data)
        self.socket_id = parsed['socket_id']
        self.state = "connected"
        if self.needs_reconnect:
            self.needs_reconnect = False
            self.reconnect_handler()
            self.logger.debug('Connection: Establisheds reconnection')
        else:
            self.logger.debug('Connection: Establisheds first connection')

    def _failed_handler(self, data):
        self.state = "failed"

    def _ping_handler(self, data):
        self.send_pong()
        self._start_timers()

    def _pong_handler(self, data):
        self.logger.info("Connection: pong from pusher")
        self.pong_received = True

    def _pusher_error_handler(self, data):
        if 'code' in data:
            try:
                error_code = int(data['code'])
            except:
                error_code = None
            if error_code is not None:
                self.logger.error("Connection: Received error %s" % error_code)
                if (4000 <= error_code <= 4099):
                    self.disconnect()
                elif (4100 <= error_code <= 4199):
                    self.reconnect()
                elif (4200 <= error_code <= 4299):
                    self.reconnect(0)
            else:
                self.logger.error("Connection: Unknown error code")
        else:
            self.logger.error("Connection: No error code supplied")

    def _connection_timed_out(self):
        self.logger.info("Did not receive any data in time.  Reconnecting.")
        self.state = "failed"
        self.reconnect()

def sleep_max_n(max_sleep_time):
    def sleep(time_to_sleep):
        time.sleep(min(max_sleep_time, time_to_sleep))
    return sleep
