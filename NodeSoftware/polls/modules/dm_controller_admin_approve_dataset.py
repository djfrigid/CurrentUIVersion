"""
    Module Name : DM Controller Admin Approve Dataset
    Module Purpose : Tells DM Controller to mark a dataset as approved
    Status : Complete
    Parameters : (data)
    Returns : sucess_check

    Creator : Izabele
    Start Date : 17/3/20
    End Date : 17/3/20
    Time Taken : 1

"""
import dmcontroller

def admin_approve_dataset(data):

    data['is_approved'] = True
    
    try:
        dm_controller("dataset","update", data)
        return True
    except:
        return False
        print:("dm_controller_admin_approve_dataset Error")