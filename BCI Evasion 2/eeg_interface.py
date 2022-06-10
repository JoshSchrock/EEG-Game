import subprocess
from live_advance import LiveAdvance

class EEGInterface:
    def __init__(self):
        self.process = subprocess.Popen("live_advance.py", shell=True, stdout=subprocess.PIPE)

    # opens and runs session
    def streamLineData(self):
        # collect each line of stdout from live_advance.py
        output = self.process.stdout.readline()
        if output:
            # determines / executes action
            return self.determineAction(output)

        retval = self.process.poll()
        return retval

    def determineAction(self, output):
        action = "neutral"
        desiredAction = str(output.strip())
        if "com" and "sid" and "time" in desiredAction:
            dataParse = desiredAction.split('"')
            action = dataParse[3]
        return action

    # disconnects headset and closes session
    def close(self):
        self.c.close_session

