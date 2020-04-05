"""
Module Name      : dm_controller_dataset_create
Module Purpose   : Return call tol dm_controller(‘dataset’, ‘create’, dataset)
Parameters       : (dataset <dataset>)
Returns          : 

Module Author    : Lirui Yang
Start Date       : 25/02/2020
End Date         : 25/02/2020
Hours Spent      : 0.1
"""

from dmcontroller import dm_controller

def dm_controller_dataset_create(dataset):
    

    try:
        dm_controller("dataset", "create", dataset)
        return True
    except:
        return False