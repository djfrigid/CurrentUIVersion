"""
    Module Name : DM Controller Admin Approve Question
    Module Purpose : Tells DM Controller to mark a question as approved
    Status : Complete
    Parameters : (data)
    Returns : sucess_check

    Creator : Izabele
    Start Date : 17/3/20
    End Date : 17/3/20
    Time Taken : 1

"""
import dmcontroller

def admin_approve_question(data):

    data['is_approved'] = True
    
    try:
        dm_controller("question","update", data)
        return True
    except:
        return False
        print:("dm_controller_admin_approve_question Error")