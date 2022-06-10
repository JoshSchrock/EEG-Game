from cortex import Cortex
import webbrowser
import subprocess

# creates Emotiv session for Pursuit Evasion Game

class userSession():
    def __init__(self):
        user = {'client_id': '', 'client_secret' : '', 
        'license' : '', 'debit' : 100}
        self.userSession = Cortex(user)
        # runs live_advance.py file
        self.process = subprocess.Popen("live_advance.py", shell = True, stdout=subprocess.PIPE)

    # creates a session for the user
    def openSession(self):
        # request access / query headset / control device / authorize / create session
        self.userSession.do_prepare_steps()

    # open website
    def openWebsite(self, url):
        webbrowser.open(url)

    # determines the action to be taken
    def determineAction(self, output):
        action = "neutral"
        desiredAction = str(output.strip())
        if "com" and "sid" and "time" in desiredAction:
            dataParse = desiredAction.split('"')
            action = dataParse[3]
        return action

    # disconnects headset and closes session
    def close(self):
        self.terminateRecord()
        self.userSession.disconnect_headset()
        self.userSession.close_session()

    # opens and runs session
    def streamLineData(self):
        # collect each line of stdout from live_advance.py
        output = self.process.stdout.readline()
        if output:
            # determines / executes action
            return self.determineAction(output)

        retval = self.process.poll()
        return retval

    # records eeg signals during session
    def beginRecord(self):
        # record parameters
        recordName = 'Pursuit Evasion Trials'
        recordDescription = 'Pursuit Evasion Trials for Research Project'
        # start record --> stop record --> disconnect headset --> export record
        self.userSession.create_record(recordName, recordDescription)

    # stops the recording
    def terminateRecord(self):
        # stop recording
        self.userSession.stop_record()

    # exports the recording
    def exportRecord(self):
        # export parameters
        recordExportFolder = ''
        recordExportDataTypes = ['EEG', 'MOTION', 'PM', 'BP']
        recordExportFormat = 'EDF'
        recordExportVersion = 'V2'
        # export recording
        self.userSession.export_record(recordExportFolder, recordExportDataTypes, recordExportFormat, recordExportVersion, [self.userSession.record_id])

    
