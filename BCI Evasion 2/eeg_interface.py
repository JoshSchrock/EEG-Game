from live_advance import LiveAdvance

class EEGInterface:
    def __init__(self):
        your_app_client_id = 'XpI8mIblEqQ6ZMj2I8RBAhYZnU8VRI9ZBB47J9K2'
        your_app_client_secret = 'dBrfGYuSzaW0Ff4kMTeJiXydRwNrKNwqMi4aVNaRm3q3WdDUWFY34c3DS9BH9yX22X42gRhH2oqavHrJOsSaOSLBZyLr0k8s2PKzbfV1Y1Nwl1OVpT1ER2xcsLgIhDlB'
        your_app_license = ''

        # Init live advance
        self.liveAdvance = LiveAdvance(your_app_client_id, your_app_client_secret, license=your_app_license)

        trained_profile_name = 'Test 1'  # Please set a trained profile name here
        self.liveAdvance.start(trained_profile_name)
        self.liveAdvance.subscribe_data(['com'])

    # opens and runs session
    def streamLineData(self):
        # collect each line of stdout from live_advance.py
        '''data: dictionary
             the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}'''
        output = self.liveAdvance.data
        if output:
            # determines / executes action
            return output['action']
        return 'neutral'

    # disconnects headset and closes session
    def close(self):
        self.liveAdvance.c.close_session()

