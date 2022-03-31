from datetime import datetime, timedelta


class Clock:
    def __init__(self):
        # make it private
        self._time = None
        self.update()

    def update(self):
        # update the time
        self._time = datetime.now()
        return True # keep running this event
    # public access to the time member

    def _get_time(self):
        return self._time

    def _set_time(self, datetime):
        self._time = datetime

    def get_time_formated(self):
        time = self._time.now().strftime("%H:%M:%S")
        return time

    def get_seconds(self):
        return self._time.now().second

    def get_minutes(self):
        return self._time.now().minute

    def get_hours(self):
        return self._time.now().hour

    def get_week_day(self):
        return self._time.now().weekday()  #0 Monday 6 Sunday

    def get_date_formated(self):
        data = self._time.now().strftime("%A, %d-%m-%Y")
        return data


class Cronometer():
    def __init__(self):
        # make it private
        self.state = 1
        self.delta_time = datetime.now()
        self.start_time = datetime.now()
        self.update()

    def update(self):
        # update the time
        self._time = datetime.now()

        if self.state == 1:
            return True  # keep running this event
        else:
            return False
    # public access to the time member

    def stop(self):
        self.state = 0

    def _get_time(self):
        time = self._time - self.start_time
        return time

    def get_time_now(self):
        return self._time

    def _set_time(self, datetime):
        self.start_time = datetime

    def _get_time_formated(self):
        time = self._time - self.start_time
        return time

    def set_delta_time(self, minutes):
        minute = timedelta(minutes=1)
        self.delta_time = self.get_time_now()+(minute * minutes)

    def get_delta_time(self, ):
        if self.delta_time > self.get_time_now():
            return self.delta_time - self.get_time_now()
        else:
            return None
