import sys
from os import path
import numpy as np
from typing import List, Union

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

from Heron.communication.socket_for_serialization import Socket
from Heron import general_utils as gu, constants as ct
from Heron.communication.transform_worker import TransformWorker
from Heron.gui.visualisation_dpg import VisualisationDPG
from gymnasium_wrapper import GymEnvWrapperOfUnityGame


visualisation_dpg: VisualisationDPG
path_to_unity_builds: str
game_executable: str
observations_returned: str
action_space_used: str
screen_resolution: str
translation_snap: float
rotation_snap: int
reward_history = []
initialised = False
gym_env: GymEnvWrapperOfUnityGame
previous_message: str


def get_parameters(_worker_object: TransformWorker):
    global visualisation_dpg
    global path_to_unity_builds
    global game_executable
    global observations_returned
    global action_space_used
    global screen_resolution
    global translation_snap
    global rotation_snap

    try:
        parameters = _worker_object.parameters
        path_to_unity_builds = parameters[1]
        game_executable = parameters[2]
        observations_returned = parameters[3]
        action_space_used = parameters[4]
        screen_resolution = parameters[5]
        translation_snap = parameters[6]
        rotation_snap = parameters[7]
    except:
        return False

    visualisation_dpg = VisualisationDPG(_node_name=_worker_object.node_name, _node_index=_worker_object.node_index,
                                         _visualisation_type='Single Pane Plot', _buffer=100,
                                         _x_axis_label='Latest Actions',
                                         _y_axis_base_label='Cumulative Reward',
                                         _base_plot_title='Cumulative Reward over Actions')

    visualisation_dpg.visualisation_on = parameters[0]

    # Add Saving the parameters every time they change if required:
    _worker_object.savenodestate_create_parameters_df(visualisation_on=visualisation_dpg.visualisation_on,
                                                      path_to_unity_builds=path_to_unity_builds,
                                                      game_executable=game_executable,
                                                      observations_returned=observations_returned,
                                                      action_space_used=action_space_used,
                                                      screen_resolution=screen_resolution,
                                                      translation_snap=translation_snap,
                                                      rotation_snap=rotation_snap)

    return True


def visualisation_reward_buffer_append(reward):
    global reward_history
    reward = float(reward)

    if len(reward_history) > 1:
        reward_history.append(reward_history[-1] + reward)
    else:
        reward_history.append(reward)
    if len(reward_history) > 100:
        reward_history.pop(0)
    if visualisation_dpg.visualisation_on:
        visualisation_dpg.visualise(np.array(reward_history))


def initialise(_worker_object: TransformWorker) -> bool:
    global initialised
    global gym_env

    if not get_parameters(_worker_object):
        return False

    screen_res = (int(screen_resolution.split(',')[0]), int(screen_resolution.split(',')[1]))

    gym_env = GymEnvWrapperOfUnityGame(path_to_unity_builds=path_to_unity_builds,
                                       game_executable=game_executable,
                                       observation_type=observations_returned,
                                       action_space_type=action_space_used,
                                       screen_res=screen_res, move_snap=translation_snap,
                                       rotate_snap=rotation_snap)

    result_reset = gym_env.reset()

    if result_reset is None:
        return False

    initialised = True

    return True


def work_function(data: List[Union[np.ndarray, dict]],
                  parameters: List,
                  savenodestate_update_substate_df: TransformWorker.savenodestate_update_substate_df) -> \
        List[Union[np.ndarray, dict]]:
    global visualisation_dpg
    global game_executable
    global observations_returned
    global action_space_used
    global screen_resolution
    global translation_snap
    global rotation_snap
    global previous_message

    try:
        visualisation_dpg.visualisation_on = parameters[0]
        # game_executable = parameters[1]
        # observations_returned = parameters[2]
        # action_space_used = parameters[3]
        # screen_resolution = parameters[4]
        # translation_snap = parameters[5]
        # rotation_snap = parameters[6]
        pass
    except:
        pass

    result = [np.array([ct.IGNORE])]

    topic = data[0]

    message = data[1:]
    message = Socket.reconstruct_data_from_bytes_message(message)

    # For now set the action distribution to Uniform but eventually this will be a function of state and will be
    # returned by the Unity Game
    result = {'features': np.array([]), 'pixels': np.array([]), 'reward': 0, 'ter': False, 'trunc': False,
              'actions_distribution': np.array([1 / gym_env.action_space.n] * gym_env.action_space.n)}

    # If the message coming into the New Environment input asks to refresh the Unity Game,
    # delete any running instance and start a new executable
    if 'New Environment' in topic:
        if message[0] == 'reset' or message[0] == 'Reset' or message[0] == 'RESET' and previous_message != message:
            previous_message = message
            result_reset = gym_env.reset()
            if result_reset is not None:
                print(result_reset)
                obs, info = result_reset
                result['features'] = obs['features']
                result['pixels'] = obs['pixels']

    if 'Action' in topic:
        action = message[0]
        #print(action)
        obs, reward, terminated, truncated, info = gym_env.step(action)
        visualisation_reward_buffer_append(reward)
        result['features'] = obs['features']
        result['pixels'] = obs['pixels']
        result['reward'] = reward
        result['ter'] = terminated
        result['trunc'] = truncated

    # SAVE TO SUBSTATE. arguments' syntax: arg_name_in_dataframe=variable_to_save 
    #  savenodestate_update_substate_df(arg_name_in_dataframe=variable_to_save)

    return [result]


def on_end_of_life():
    try:
        gym_env.close()
    except:
        pass


if __name__ == '__main__':
    worker_object = gu.start_the_transform_worker_process(work_function=work_function,
                                                          end_of_life_function=on_end_of_life,
                                                          initialisation_function=initialise)
    worker_object.start_ioloop()
