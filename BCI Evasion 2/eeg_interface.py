from live_advance import LiveAdvance
import threading
from datetime import datetime


class EEGInterface:
    def __init__(self, headset_id, profile_name):
        your_app_client_id = 'BN6wnwY8b9ZKYAQmTUCJLHBx0UVQ1VE52QN4I9Ha'
        your_app_client_secret = 'WSdbaAxrMqkNvqRvMYW8ZsLXWNuNb3XJGk4cnxXebQb3A43bl7L21AEvr7aiQqOepIo01K74ixfDSKPb1QBhUPPX9EOewegV4kYZCJceDiGBZFfAKrSN5MIpTQroOhg6'
        your_app_license = 'd5b584b8-883e-421f-8bf5-cbe4bcb0ac72'
        self.headset_id = headset_id
        self.profile_name = profile_name


        # Init live advance
        self.liveAdvance = LiveAdvance(your_app_client_id, your_app_client_secret, license=your_app_license)
        threadName = "EEGThread:-{:%Y%m%d%H%M%S}".format(datetime.utcnow())
        self.eeg_thread = threading.Thread(target=self.beginStream, name=threadName)
        self.eeg_thread.daemon = True
        self.eeg_thread.start()


    def beginStream(self):
        self.liveAdvance.start(self.profile_name, self.headset_id)


    # opens and runs session
    def streamLineData(self):
        # collect each line of stdout from live_advance.py
        '''data: dictionary
             the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}'''
        output = self.liveAdvance.data
        if output:
            # determines / executes action
            return output['action'], output['power']
        return 'neutral'

    # disconnects headset and closes session
    def close(self):
        self.liveAdvance.c.close_session()
        self.eeg_thread.join()


