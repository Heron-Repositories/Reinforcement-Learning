import sys
from os import path
import numpy as np
import time
from typing import List, Union

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

from Heron.communication.socket_for_serialization import Socket
from Heron import general_utils as gu, constants as ct
from Heron.communication.transform_worker import TransformWorker


game_executable: str
observations_returned: list
action_space_used: list
screen_resolution: str
translation_snap: float
rotation_snap: int


def initialise(worker_object: TransformWorker) -> bool:
    global game_executable
    global observations_returned
    global action_space_used
    global screen_resolution
    global translation_snap
    global rotation_snap


    try:
        parameters = worker_object.parameters
        game_executable = parameters[0]
        observations_returned = parameters[1]
        action_space_used = parameters[2]
        screen_resolution = parameters[3]
        translation_snap = parameters[4]
        rotation_snap = parameters[5]
    except:
        return False

    # Add Saving the parameters every time they change if required:
    #  worker_object.savenodestate_create_parameters_df(game_executable=game_executable, 
    #                                                   observations_returned=observations_returned,
    #                                                   action_space_used=action_space_used,
    #                                                   screen_resolution=screen_resolution,
    #                                                   translation_snap=translation_snap,
    #                                                   rotation_snap=rotation_snap
    #                                                    )

    # DO ANY OTHER INITIALISATION HERE 

    return True


def work_function(data: List[Union[np.ndarray, dict]],
                  parameters: List,
                  savenodestate_update_substate_df: TransformWorker.savenodestate_update_substate_df) -> \
        List[Union[np.ndarray, dict]]:

    global game_executable
    global observations_returned
    global action_space_used
    global screen_resolution
    global translation_snap
    global rotation_snap

    try:
        #  Uncomment any of the parameter updates whose values
        #  need to update as the Graph is running.
        # game_executable = parameters[0]
        # observations_returned = parameters[1]
        # action_space_used = parameters[2]
        # screen_resolution = parameters[3]
        # translation_snap = parameters[4]
        # rotation_snap = parameters[5]
        pass
    except:
        pass

    topic = data[0]

    message = data[1:]
    message = Socket.reconstruct_data_from_bytes_message(message)
    # OR Socket.reconstruct_array_from_bytes_message_cv2correction(message) if the message data is an image

    # -----------------------
    # MAIN CODE GOES HERE !!
    # -----------------------

    # SAVE TO SUBSTATE. arguments' syntax: arg_name_in_dataframe=variable_to_save 
    #  savenodestate_update_substate_df(arg_name_in_dataframe=variable_to_save)

    # Create the result to be pushed to the next Node
    # Here we are creating a list that pushes nothing, but you should
    # create a list of numpy arrays or dictionaries for the Node to return.
    result = [np.array([ct.IGNORE]), ]

    return result


def on_end_of_life():

    # ADD HERE ANY OTHER PROCESS TERMINATION CODE
    pass


if __name__ == '__main__':
    worker_object = gu.start_the_transform_worker_process(work_function=work_function,
                                                          end_of_life_function=on_end_of_life,
                                                          initialisation_function=initialise)
    worker_object.start_ioloop()
