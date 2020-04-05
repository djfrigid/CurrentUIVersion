"""
    Module Name : DM Controller Question Delete
    Module Purpose : Tells DM Controller to delete a question and all associated datasets and submissions
    Status : complete
    Parameters : (data) question ID
    Returns : sucess_check

    Creator : Laura
    Start Date : 10/3/20
    End Date : 10/3/20
    Time Taken : 1

""""

import dmcontroller

def dm_controller_question_update(question_id):
    try:
        dm_controller("question","delete",question_id) #basic try catch exception for calling dm_controller
        return True
    except:
        return False
        print:("dm_controller_question_delete invoke Error")
