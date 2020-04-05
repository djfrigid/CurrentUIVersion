"""
    Module Name : DM Controller 
    Module Purpose : Allow database access from python code, as an alternative to Django ORM based stuff
    Status : Nominally Complete
    Parameters : (field, action, data)
    Returns : success_check
    
    Creator : Mark
    Start Date : 20/2/20
    End Date : 24/03/20
    Time Taken : 5

"""

"""
    Notes:
    All of the code shares a common theme, so I've only commented the code for questions.
    When updating anything, only pass a dictionary of the fields you want to update and the id/username, otherwise it will create new fields and break all of the current migrations 
    There's probably differences in the names of the dictionary fields and what I'm using in here / in the database. We'll find and make a standard naming scheme as they appear 
    WARNING! - AS of 22/02/20 it will perform the operations regardless of what the data actually contains, MongoDB will not complain, but it will break the code. Use these functions at your own risk.
    """

from pymongo import MongoClient

def dm_controller(field, action, data, *args):
    
    """
        Parameter List;
            Field : Field is the collection you want to modify, which allows for extension of DM controller 
            Action : Which one of the CRUD actions you want to perform 
            Data : The relevant dictionary that is holding the required data for database execution
            
    """

    client = MongoClient('localhost', 27017) #This Object represents our connection to the database instance, it may need to be parameterized later. 
    db = client.JCoin #This is the actual database within the mongo instance we want to use, so make sure to call your database JCoin, or change your copy of DM Controller to reflect your database name
        
    if field == "question": #When we are dealing with questions
                
        questions = db.polls_question #This represents the questions collection in the database 
        
        valid_keys = ['question_id', 'submitting_user' ,'title', 'spec', 'number_of_submissions', 'best_solution', 'language', 'datasets', 'code', 'tags', 'is_approved'] #Database names of the fields that exist 
        
        for key in data.keys: #For every key in the user defined dictionary we received 
            if key not in valid_keys: #If the field doesn't already exist 
                return {'Success' : False, 'Reason' : "You are trying to access fields that do not exist. Check that the keys in your dictionary match the names of the database fields exactly."} #Return a success check
        
        if action == "create": #Decide on the action 
            #If we are creating a new question, this dictionary will represent each field we need to write to the database
            new_question = {
            
                'id' : data['id'],
                'submitting_user' : data['submitting_user'],
                'title' : data['title'],
                'spec' : data['spec'],
                'number_of_submissions' : 0,
                'best_solution' : data['best_solution'],
                'language' : 'Python',
                'datasets' : data['datasets'],
                'code' : data['code'],
                'tags' : data['tags'],
                'is_approved' : False
            
            }
            result = questions.insert_one(new_question) #Run an insert for the new document
        
        elif action == "read":
            result = questions.find_one({"id" : int(data['id'])}) #Read the document with ID = id
            
        elif action == "update":
            result = questions.update_one({"id" : int(data['id'])}, {"$set" : data}) #Update ALL the fields in data with the corresponding value to the key
            
        elif action == "delete":
            result = questions.delete_one({"id" : int(data['id'])}) #Delete the document with ID = id
        
        else:
            return {'Success' : False, 'Reason' : 'Invalid Action! Make sure you are using create, read, update or delete.'}
             
    #Rinse and repeat from here on out
        
    elif field == "user":
        
        users = db.polls_user
        valid_keys = ['username' ,'email', 'has_admin']
        
        for key in data.keys:
            if key not in valid_keys:
                return {'Success' : False, 'Reason' : "You are trying to access fields that do not exist"}
                
        if action == "create":
            new_user = {
                'username' : data['username'],
                'email' : data['email'],
                'has_admin' : False
            } 
            result = users.insert_one(new_user)
        elif action == "read":
            result = users.find_one( {"username" : data['username']} )
            
        elif action == "update":
            result = users.update_one({"username" : data['username']}, {'$set' : data})
            
        elif action == "delete":
            if len(args) != 1:
                return {'Success' : False , 'Reason' : 'Invalid amount of arguments, arguments should specify deletion type as fourth (the only additional) argument'}
            else:
                if args[0] == "soft":
                    result = users.delete_one({"username" : data['username']})
                elif args[0] == "hard":
                    question_collection = db.polls_question
                    submission_collection = db.polls_submission
                    dataset_collection = db.polls_dataset
                    
                    for question in question_collection.find():
                        if question['submitting_user'] == data['username']:
                            question_collection.delete_one({'title' : question['title']})
                            
                    for submission in submission_collection.find():
                        if submission['submitting_user'] == data['username']:
                            submission_collection.delete_one({'submission_id' : submission['submission_id']})
                    
                    for dataset in dataset_collection.find():
                        if dataset['submitting_user'] == data['username']:
                            dataset_collection.delete_one({'dataset_id' : dataset['dataset_id']})
                    
                    result = users.delete_one({"username" : data['username']})
                    return {'Success' : True, 'Reason' : 'None'}
                else:
                    return {'Success' : False, 'Reason' : 'Fourth argument was neither soft nor hard. These are the only valid values'}
            
            
        else:
            return {'Success' : False, 'Reason' : 'Invalid Action! Make sure you are using create, read, update or delete.'}
            
        
    elif field == "dataset":
        
        datasets = db.polls_dataset
        
        new_dataset = {
            'id' : data['id'],
            'submitter_name' : data['submitter_id'],
            'relevant_questions' : [],
            'actual_data' : data['data']
        }
        
        if action == "create":
            result = datasets.insert_one(new_dataset)
        elif action == "read":
            result = datasets.find_one({"id" : int(data['id'])})
            
        elif action == "update":
            result = datasets.update_one({"id" : int(data['id'])}, {"$set" : data})
             
        elif action == "delete":
            result = datasets.delete_one({"id" : int(data['id'])})
            
        else:
            return {'Success' : False, 'Reason' : 'Invalid Action! Make sure you are using create, read, update or delete.'}
            
        
    elif field == "solution":
        
        submissions = db.polls_submission
        
        new_submission = {
            'id' : data['id'],
            'submitting_user' : data['submitter_id'],
            'is_for_question' : data['question_id'],
            'time_result' : 0.0,
            'memory_result' : 0.0,
            'tmp_files_created' : 0,
            'src_size' : 0.0,
            'overall_result' : 0.0,
            'rank' : 0
        }
        
        if action == "create":
            result = submissions.insert_one(new_submission)
            
        elif action == "read":
            result = submissions.find_one({"id" : int(data['id'])})
            
        elif action == "update":
            result = submissions.update_one({"id" : int(data['id'])}, {'$set' , data})
            
        elif action == "delete":
            result = submissions.delete_one({"id" : int(data['id'])})
            
        else:
            return {'Success' : False, 'Reason' : 'Invalid Action! Make sure you are using create, read, update or delete.'}
            
    elif field == "utils":
        
        if action == "get_node_list":
            node_list = []
            node_collection = db.polls_node
            for node in node_collection.find():
                node_list.append(node)
            return node_list
        
        else:
            return {'Success' : False, 'Reason' : 'Invalid Action! The only utils action is get_node_list!.'}
        
    else:
        return {'Success' : False , 'Reason' : 'Invalid collection name! You may only work on : Users, Datasets, Questions and Solutions'}
    
    if result is not None:
        return {'Success' : True, 'Reason' : 'No Failure'}
    else:
        return {'Success' : False, 'Reason' : 'Generic Error Message'}


