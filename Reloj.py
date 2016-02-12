from datetime import datetime

#################################################################################
class Reloj():
    def __init__(self):
        # make it private

        self.update()
        # clock hands
        #self._update_id = GObject.timeout_add(200, self.update)
    def update(self):
        # update the time
        self._time = datetime.now()
        return True # keep running this event
    # public access to the time member
    def _get_time(self):
        return self._time
    def _set_time(self, datetime):
        self._time = datetime
    def _get_time_formated(self):
        tiempo = self._time.now().strftime("%H:%M:%S")
        return tiempo
    def get_segundos(self):
        return self._time.now().second
    def get_minutos(self):
        return self._time.now().minute
    def get_horas(self):
        return self._time.now().hour
    def get_dia_semana(self):
        return  self._time.now().weekday() #0 Lunes 6 Domingo
    def _get_date_formated(self):
        data = self._time.now().strftime("%A, %d-%m-%Y")
        return data


class cronometro():
    def __init__(self):
        # make it private
        self.estado = 1
        self.hora_inicio = datetime.now()
        self.update()

    def update(self):
        # update the time
        self._time = datetime.now()

        if (self.estado == 1):
            return True # keep running this event
        else:
            return False
    # public access to the time member
    def stop(self):
        self.estado = 0
    def _get_time(self):
        tiempo = self._time - self.hora_inicio
        return tiempo
    def get_time_now(self):
        return self._time
    def _set_time(self, datetime):
        self.hora_inicio = datetime

    def _get_time_formated(self):
        tiempo = self._time - self.hora_inicio
        return tiempo



