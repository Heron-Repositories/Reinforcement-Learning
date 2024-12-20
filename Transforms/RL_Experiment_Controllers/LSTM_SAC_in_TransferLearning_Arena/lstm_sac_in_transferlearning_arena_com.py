import os
import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

from Heron import general_utils as gu
Exec = os.path.abspath(__file__)


BaseName = 'LSTM SAC in TransferLearning Arena'
NodeTooltip = 'This is the controller for a Reinforcement Learning experiment where the Agent is n SAC with LSTM model and the environment is a gym environment.'
NodeAttributeNames = ['Parameters', 'Observations from Env', 'Action from Agent', 'Reset Env', 'Action to Env', 'Observations to Agent']
NodeAttributeType = ['Static', 'Input', 'Input', 'Output', 'Output', 'Output']
ParameterNames = ['Visualisation', 'Train or Test', 'Path of Model', 'Path of tensorboard Log', 'Steps per Episode',
                  'Episodes per Epoch', 'Epochs', 'Updates per Epoch', 'Save every N Update']
ParameterTypes = ['bool', 'list', 'str', 'str', 'int', 'int', 'int', 'int', 'int']
ParametersDefaultValues = [False, ['Train', 'Test'], '', r'\path\to\log', 10000, 10, 100, 1, 2]
ParameterTooltips = ['Documentation not available',
                     'Sets the controller to training or testing mode.\n\nIf it is Train then the controller runs the environment / agent loop \nand at specified intervals trains the Agent.\n\nIf it is Test then  it just runs the environment / agent loop without updating the agent.',
                     'The full path to the model to be used. If empty a new model will be created.',
                     'The path to the logfile used by tensorboard',
                     'The number of steps per episode.', 'The number of episodes in an epoch.\n\nAn epoch is a number of episodes that collate their data (actions and  observations)\ninto a single buffer. At the end of every epoch the buffer is cleared.\n\nEach episode initialises its own Unity Game.\n\n',
                     'The number of epochs in an experiment.\n\nThe total size of the experiment will be Epochs * Episodes per Epoch episodes and\nEpochs * Episodes per Epoch * Steps per Episode steps.',
                     'How many updates the model will do (during training) within each epoch.\nIf the Episodes per Epoch is not divisible by this number\n then the updates will not be done every equal number\nof episodes.',
                     'The weights of the model will be save every this number of model updates.']
InOutTooltips = ["Dict['features: np.ndarray, 'pixels': np.ndarray, 'reward': int, 'ter': bool,\n         'trunc': bool, 'actions_distribution': np.ndarray]\n\nThese are the observations the environment returns after it has been asked to do a step.\n",
                 'np.ndarray[int]\n\nThis is the action the agent has chosen to take after it received the updated observations\nfrom the environment.\n\n',
                 'np.ndarray[str] (RESET OR Reset OR reset)\n\nIf the string is Reset, reset or RESET then the environment resets.',
                 'np.ndarray[int]\n\nThis is the action that the Agent has chosen to take, communicated to the Environment \nin order for it to update its state.',
                 "Dict['epoch': int, 'episode': int, 'features: list, 'pixels': list[list]\n\nThe observations sent to the Agent in order for it to decide on its next action."]
WorkerDefaultExecutable = os.path.join(os.path.dirname(Exec), 'lstm_sac_in_transferlearning_arena_worker.py')


if __name__ == '__main__':
    lstm_sac_in_transferlearning_arena_com = gu.start_the_transform_communications_process(NodeAttributeType, NodeAttributeNames)
    gu.register_exit_signals(lstm_sac_in_transferlearning_arena_com.on_kill)
    lstm_sac_in_transferlearning_arena_com.start_ioloop()