"""
    Module Name : DM Controller Question Update
    Module Purpose : Tells DM Controller to update a question
    Status : Complete
    Parameters : (data)
    Returns : sucess_check

    Creator : Laura
    Start Date : 9/3/20
    End Date : 9/3/20
    Time Taken : 1

""""
import dmcontroller

def dm_controller_question_update(data):
    try:
        dm_controller("question","update",data) #basic try catch exception
        return True
    except:
        return False
        print:("dm_controller_question_update Error")

# was going to implement a data check however dm_controller has an already built in data Check
