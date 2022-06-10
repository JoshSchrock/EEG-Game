# Pursuit Evasion with EPOC Flex

## Pursuit-Evasion Game
- The purpose of the pursuit-evasion game was to have a human pursue an evading robot using the mental commands provided by EmotivBCI and transmitted through the EPOC Flex headset. For the evader, there were three simple evading algorithms implemented - exaggerating, ambiguous, and switching. This game was implemented in Python using the Pygame library and interacted with the EPOC Flex headset through Emotiv’s Cortex API.

## Requirements
- Python >= 3.7
- EPOC Flex Headset
- Emotiv License
- EmotivBCI & Emotiv Pro Software
- Saline Gel
- Window / Mac OS

## Connecting the EPOC Flex
- Before turning on the device, hydrate the sensor pads to be used  with saline. The saline typically used in the lab is Biotrue but most saline solutions will work and can be bought over the counter at any local pharmacy. 

- To turn on the EPOC flex there will be a switch on the side of the controller. Turn on this switch. If a blue light appears on the top of the controller then the device is on and ready to be paired. If the light is a different color, it may need to be charged. 

- Plug in the USB dongle and open the Emotiv App. The device should appear on-screen. Click connect. Once connected, ensure good contact quality. This part can be tricky and might require more saline being applied to certain sensors that are not in good contact with the scalp. To ensure good contact quality it often is useful to have another person assisting the subject wearing the device. 

- Once good contact quality is established make sure the EEG quality is good as well. To ensure good EEG quality it helps for the subject to remain still. Once good contact and EEG quality are established, the subject is ready to begin training.


## Training Mental Commands
- In order to train the EPOC Flex to do useful things, such as pursuing an evader, a training profile must be created on the EmotivBCI information. This profile should include a name and demographic information.
- Once a profile is created, training can begin. It helps to train the neutral command first. In the neutral state, the user should just act as they normally would and not think of anything in particular but just let random thoughts enter and exit their mind.
- Once the device has learned the user's neutral state, the user can begin to train some useful mental commands. Some commands include left, right, lift, and pull. It helps to train one command at a time, being confident with one command before moving on to the next one. Additionally, it helps to focus on something particular whether it be a sound or a memory while training each command. This will help to differentiate between the different commands trained. 
- The training of the mental commands can be quite difficult and can take a lot of time. Therefore, patience is definitely advised during this step.

## Cortex API
- The Cortex API is a useful tool provided by Emotiv that allows users to develop 3rd-party applications that interact with their headsets and software. For instance, in order for a pursuer-evader game to be played with the EPOC flex device a version of this game was created in Python and the device was continuously streamed for mental commands while the game was being played. 
 
- The necessary python files from the Cortex API repository (cortex.py and live_advance.py) are provided above. However, they provide additional files in this repository below.

  Cortex API: 
  https://github.com/Emotiv/cortex-v2-example

## Collecting Data

### Raw EEG Signals
- Emotiv allows users to record and export raw EEG signals in both .csv and .edf formats. 

### Feature Extracted Signals
- Emotiv also allows some processed signals (through fast-fourier transform and by other means) to be exported in the aforementioned forms. 

### Performance Metrics
- Emotiv also provided performance metrics which provide insight into the user’s excitement, engagement, focus, stress, etc. These performance metrics can be exported and used for further analysis with the academic and business licenses. 

### Brain Heat Map Data
- Unfortunately, Emotiv BrainViz software is not compatible with the EPOC flex device. Therefore, for brain heat mapping 3rd-party software is needed. Fortunately, there were some useful Python scripts provided on github to address this problem. The GitHub link is provided below. 

  Brain Heat Mapping with Python:
  https://github.com/ijmax/EEG-processing-python
  
- Note: The respository above does not allow you to save .gif files so I included convertPNGToGIF.py to remedy this issue.





