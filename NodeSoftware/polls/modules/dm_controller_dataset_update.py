"""
Module Name      : dm_controller_dataset_update
Module Purpose   : Return call to dm_controller(‘dataset’, ’update’, dataset)
Parameters       : (dataset <dataset>)
Returns          : 

Module Author    : Lirui Yang
Start Date       : 25/02/2020
End Date         : 25/02/2020
Hours Spent      : 0.1
"""

from dmcontroller import dm_controller

def dm_controller_dataset_update(dataset):
    try:
        dm_controller("dataset", "update", dataset)
        return True
    except:
        return False