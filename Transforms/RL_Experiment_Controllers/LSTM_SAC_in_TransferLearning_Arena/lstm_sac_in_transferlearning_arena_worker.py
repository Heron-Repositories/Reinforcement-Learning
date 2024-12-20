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
from Heron.gui.visualisation_dpg import VisualisationDPG
from Heron.communication.transform_worker import TransformWorker


train_or_test: str
path_of_model: str
path_of_log: str
steps_per_episode: int
episodes_per_epoch: int
epochs: int
updates_per_epoch: int
save_every_n_update: int
vis: VisualisationDPG


def initialise(worker_object: TransformWorker) -> bool:
    global vis
    global train_or_test
    global path_of_model
    global path_of_log
    global steps_per_episode
    global episodes_per_epoch
    global epochs
    global updates_per_epoch
    global save_every_n_update

    # The args depend on what will be visualised. See Worker Templates on how to fill them in.
    #vis = VisualisationDPG(worker_object.node_name, worker_object.node_index, *args)

    try:
        parameters = worker_object.parameters
        #vis.visualisation_on = parameters[0]
        train_or_test = parameters[1]
        path_of_model = parameters[2]
        path_of_log = parameters[3]
        steps_per_episode = parameters[4]
        episodes_per_epoch = parameters[5]
        epochs = parameters[6]
        updates_per_epoch = parameters[7]
        save_every_n_update = parameters[8]
    except:
        return False

    # Add Saving the parameters every time they change if required:
    worker_object.savenodestate_create_parameters_df(visualisation=False,
                                                     path_of_model=path_of_model,
                                                     path_of_log=path_of_log,
                                                     train_or_test=train_or_test,
                                                     steps_per_episode=steps_per_episode,
                                                     episodes_per_epoch=episodes_per_epoch,
                                                     epochs=epochs,
                                                     updates_per_epoch=updates_per_epoch,
                                                     save_every_n_update=save_every_n_update)

    # DO ANY OTHER INITIALISATION HERE 

    return True


def work_function(data: List[Union[np.ndarray, dict]],
                  parameters: List,
                  savenodestate_update_substate_df: TransformWorker.savenodestate_update_substate_df) -> \
        List[Union[np.ndarray, dict]]:
    global vis
    global train_or_test
    global path_of_model
    global path_of_log
    global steps_per_episode
    global episodes_per_epoch
    global epochs
    global updates_per_epoch
    global save_every_n_update

    try:
        #  Uncomment any of the parameter updates whose values
        #  need to update as the Graph is running.
        # vis.visualisation_on = parameters[0]
        # train_or_test = parameters[1]
        # path_of_model = parameters[2]
        # path_of_log = parameters[3]
        # steps_per_episode = parameters[4]
        # episodes_per_epoch = parameters[5]
        # epochs = parameters[6]
        # updates_per_epoch = parameters[7]
        # save_every_n_update = parameters[8]
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

    # Put the data you want to visualise here.
    # Check that the way you set up the VisualiserGPD in the initialisation function is compatible.
    #vis.visualise(something_to_visualise)

    # Create the result to be pushed to the next Node
    # Here we are creating a list that pushes nothing, but you should
    # create a list of numpy arrays or dictionaries for the Node to return.
    result = [np.array([ct.IGNORE]), np.array([ct.IGNORE]), np.array([ct.IGNORE]), ]

    return result


def on_end_of_life():
    global vis
    vis.end_of_life()

    # ADD HERE ANY OTHER PROCESS TERMINATION CODE


if __name__ == '__main__':
    worker_object = gu.start_the_transform_worker_process(work_function=work_function,
                                                          end_of_life_function=on_end_of_life,
                                                          initialisation_function=initialise)
    worker_object.start_ioloop()
