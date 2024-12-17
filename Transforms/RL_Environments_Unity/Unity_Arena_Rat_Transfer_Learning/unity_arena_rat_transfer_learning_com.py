import os
import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

from Heron import general_utils as gu
Exec = os.path.abspath(__file__)


BaseName = 'Unity Arena Rat Transfer Learning'
NodeTooltip ='A set of Unity Games (Environments) that model a 3D rat arena\nused for a series of Transfer Learning experiments'
NodeAttributeNames = ['Parameters', 'Message from Agent', 'Message to Agent']
NodeAttributeType = ['Static', 'Input', 'Output']
ParameterNames = ['Game Executable', 'Observations Returned', 'Action Space Used', 'Screen Resolution', 'Translation Snap', 'Rotation Snap']
ParameterTypes = ['str', 'list', 'list', 'str', 'float', 'int']
ParametersDefaultValues = ['unity_game.exe', ['Features', 'Pixels', 'Everything'], ['Small', 'Full'], '100, 100', 0.2, 10]
ParameterTooltips = ['This is the path to the executable file that is the Unity game to be\nrun.\n',
                     "This defines the type of observations returned by the environment  \nto the agent after the action of each step is taken. \n\nIf it is Features then the environment returns only the features of \neach state.\n\nIf it is Pixels then it returns only the array (picture) captured by the\non the angent's head.\n\nIf it is Everything then it returns both the features and the pixels.\n",
                     'Defines if the Action space (the set of possible actions) is either\nSimple or Full.\n\nFull means all possible actions are allowed.\n\nSimple means that the Nothing action is not allowed.\n',
                     'The resolution of the camera that the environment uses to capture\nthe Pixels observation.\n\nThis is a comma delimited string of two numbers (X pixels, Y pixels)\nfor the horizontal and vertical dimension of the screen in pixels.\n',
                     "The discritization of the agent's translation. This is in the same units\nas the arena. The arena size in this Unity project is 8 x 8.\n\nThe value here means the size of the step the agent will take when\nmoving forwards or backwards.\n\nThe number of states in the environment is a function of this \nnumber. ",
                     "The discritization of the agent's rotation. This is in degrees.\n\nThe value here means the size of the step the agent will take when\nturning clock or counter clock wise.\n\nThe number of states in the environment is a function of this \nnumber. "]
InOutTooltips = ['The only input to the environment comes from the agent.\nThere are three possible messages:\n\n1) A message to tell the environment to refresh. This will kill any open\nUnity games, start a new one (run the Game Executable file) and\nestablish a new communication with it.\n\n2) A message to ask the environment for the sizes of the State and\nAction spaces. This will lead to an immediate return message from \nthe environment (and this Node) describing these sizes.\n\n3) A message to ask the environment to make the agent take an \naction. The environment will enact the received action and then\nimmediately produce a message with the observation of the new \nstate.\n\n\n',
                 'This is a reply message to the Agent (the RL model) given a previously\nreceived message.\n\nThere can be three possible responses:\n\n1) A response saying whether a reset request completed (or not)\nsuccessfully. A successful completion means a correct connection\nwith a new instance of the Unity game.\n\n2) A response describing the sizes of the Observation and Action \nspaces.\n\n3) A response with the observations after a state update.\n']
WorkerDefaultExecutable = os.path.join(os.path.dirname(Exec), 'unity_arena_rat_transfer_learning_worker.py')


if __name__ == '__main__':
    unityarena_rat_transferlearning_com = gu.start_the_transform_communications_process(NodeAttributeType, NodeAttributeNames)
    gu.register_exit_signals(unityarena_rat_transferlearning_com.on_kill)
    unityarena_rat_transferlearning_com.start_ioloop()