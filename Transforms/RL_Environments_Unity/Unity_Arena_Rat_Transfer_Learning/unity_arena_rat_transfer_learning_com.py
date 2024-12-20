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
NodeAttributeNames = ['Parameters', 'New Environment', 'Action', 'Observations']
NodeAttributeType = ['Static', 'Input', 'input', 'Output']
ParameterNames = ['Visualisation', 'Path to Unity Games', 'Game Executable', 'Observations Returned', 'Action Space Used', 'Screen Resolution', 'Translation Snap', 'Rotation Snap']
ParameterTypes = ['bool', 'str', 'str', 'list', 'list', 'str', 'float', 'int']
ParametersDefaultValues = [False, r'path\to\Unity\build\folder', 'unity_game', ['Features', 'Pixels', 'Everything'], ['Simple', 'Full'], '100, 100', 0.2, 10]
ParameterTooltips = ['The visualisation of the cumulative reward collected up to now',
                     'This is the path to the the folder where the different Unity games are',
                     'This is the name of the Unity game executable',
                     "This defines the type of observations returned by the environment  \nto the agent after the action of each step is taken. \n\nIf it is Features then the environment returns only the features of \neach state.\n\nIf it is Pixels then it returns only the array (picture) captured by the\non the angent's head.\n\nIf it is Everything then it returns both the features and the pixels.\n",
                     'Defines if the Action space (the set of possible actions) is either\nSimple or Full.\n\nFull means all possible actions are allowed.\n\nSimple means that only the Move forwards, Backwards and Rotate\nLeft and Right (no Nothing and Paw Moves) are allowed.\n',
                     'The resolution of the camera that the environment uses to capture\nthe Pixels observation.\n\nThis is a comma delimited string of two numbers (X pixels, Y pixels)\nfor the horizontal and vertical dimension of the screen in pixels.\n',
                     "The discritization of the agent's translation. This is in the same units\nas the arena. The arena size in this Unity project is 8 x 8.\n\nThe value here means the size of the step the agent will take when\nmoving forwards or backwards.\n\nThe number of states in the environment is a function of this \nnumber. ",
                     "The discritization of the agent's rotation. This is in degrees.\n\nThe value here means the size of the step the agent will take when\nturning clock or counter clock wise.\n\nThe number of states in the environment is a function of this \nnumber. "]
InOutTooltips = ['np.ndarray[str] (RESET or Reset or reset)\n\nThis is a message to tell the environment to refresh. This will kill any open\nUnity games, start a new one (run the Game Executable file) and\nestablish a new communication with it.\n\n',
                 'np.ndarray[int]\n\nThis is the input from the agent.\n\nThe environment will enact the received action and then\nimmediately produce a message with the observation of the new \nstate.\n\n',
                 "Dict['features: list, 'pixels': list[list], 'reward': int,\n         'ter': bool, 'trunc': bool, 'actions_distribution': np.ndarray]\n\nThese are the observations of the new state after a step, together with some extra info."]
WorkerDefaultExecutable = os.path.join(os.path.dirname(Exec), 'unity_arena_rat_transfer_learning_worker.py')


if __name__ == '__main__':
    unityarena_rat_transferlearning_com = gu.start_the_transform_communications_process(NodeAttributeType, NodeAttributeNames)
    gu.register_exit_signals(unityarena_rat_transferlearning_com.on_kill)
    unityarena_rat_transferlearning_com.start_ioloop()