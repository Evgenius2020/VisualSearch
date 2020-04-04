# VisualSearch
Based on paper 'The role of priming in conjunctive visual search.' (DOI: 10.1016/s0010-0277(02)00074-4).

VisualSearch is experimental program, when subject perform task of searching object with specific color and orientation.

Written for participation in the MARVIN contest by "Think Cognitive Think Science".

## Features
* Python3 implementation
* PyQt5 Client
* Protocol writing
* Added fixation before trials 
* Keyboard bindings randomization
* Guaranteed counterbalance for random picks (condition, target presence, bars number)

## How to use
### Install requirements
`$ pip install -r requirements.txt`
### Run
`$ python main.py`

Experiment settings window will be presented, you can change subject name, protocol filename and turn fast mode on. 
On 'Start experiment' button pressed experiment will be started form Intro page.
> Fast mode - runs experiment with lower trials number.
### Examine protocol
Protocol file saved automatically as .csv file. Default file is './subject.csv'.

## Changing configuration
In configuration.py you can change experiments parameters such as:
* blocks/condition, trials/block number
* fixation and feedback durations
* keyboard keys
* intro, feedback text (localization)

