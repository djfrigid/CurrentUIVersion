import dmcontroller as dm_controller

def testing_dm_controller():
    
    test_question = {
            
        'id' : 'testing1',
        'submitting_user' : 'test_submitting_user',
        'title' : 'Test Title',
        'spec' : 'Tesyt Spec',
        'number_of_submissions' : 0,
        'best_solution' : 'bestsolution.py',
        'language' : 'Python',
        'datasets' : 'testdataset.txt',
        'code' : 'testcode.py',
        'tags' : [],
        'is_approved' : False
            
    }
    
    test_question_update = {
            
        'id' : 'testing1update',
        'submitting_user' : 'test_submitting_user',
        'title' : 'Test Title',
        'spec' : 'Tesyt Spec',
        'number_of_submissions' : 0,
        'best_solution' : 'bestsolution.py',
        'language' : 'Python',
        'datasets' : 'testdataset.txt',
        'code' : 'testcode.py',
        'tags' : [],
        'is_approved' : False
            
    }
    
    test_user = {
        'username' : 'Test Username 1',
        'email' : 'testemail@testdomain.com',
        'has_admin' : False
    } 
    
    test_user_update = {
        'username' : 'Update Test Username 1',
        'email' : 'testemail@testdomain.com',
        'has_admin' : False
    } 
    
    test_dataset = {
        'id' : 1,
        'submitter_name' : 'Test Username 1',
        'relevant_questions' : [],
        'actual_data' : 'path/to/dataset/file'
    }
    
    test_dataset_update = {
        'id' : 1,
        'submitter_name' : 'Update Test Username 1',
        'relevant_questions' : [],
        'actual_data' : 'path/to/dataset/file'
    }
    
    test_submission = {
        'id' : 1,
        'submitting_user' : 'Test Username 1',
        'is_for_question' : 'Test Question 1',
        'time_result' : 0.0,
        'memory_result' : 0.0,
        'tmp_files_created' : 0,
        'src_size' : 0.0,
        'overall_result' : 0.0,
        'rank' : 0
    }
    
    test_submission_update = {
        'id' : 1,
        'submitting_user' : 'Update Test Username 1',
        'is_for_question' : 'Test Question 1',
        'time_result' : 0.0,
        'memory_result' : 0.0,
        'tmp_files_created' : 0,
        'src_size' : 0.0,
        'overall_result' : 0.0,
        'rank' : 0
    }
    
    
    updating = False #Change to true to perform updates to existing records 
    
    if updating:
        question_update_result = dm_controller('question', 'update', test_question_update)
        user_update_result = dm_controller('user', 'update', test_user_update)
        dataset_update_result = dm_controller('dataset', 'update', test_dataset_update)
        submission_update_result = dm_controller('submission', 'update', test_submission_update)
        
    #These variables hold the results of the running of each function
    
    question_create_result = dm_controller('question', 'create', test_question)
    question_read_result = dm_controller('question', 'read', test_question)
    question_delete_result  = dm_controller('question', 'delete', test_question)
    user_create_result = dm_controller('user', 'create', test_user)
    user_read_result = dm_controller('user', 'read', test_user)
    user_delete_result  = dm_controller('user', 'delete', test_user)
    dataset_create_result = dm_controller('dataset', 'create', test_dataset)
    dataset_read_result = dm_controller('dataset', 'read', test_dataset)
    dataset_delete_result  = dm_controller('dataset', 'delete', test_dataset)
    submission_create_result = dm_controller('submission', 'create', test_submission)
    submission_read_result = dm_controller('submission', 'read', test_submission)
    submission_delete_result  = dm_controller('submission', 'delete', test_submission)
    
    
    
    
    