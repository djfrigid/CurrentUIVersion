from djongo import models

class Question(models.Model):
    _id = models.ObjectIdField(default = None)
    question_id = models.IntegerField(default = None)
    submitting_user = models.CharField(max_length = 64, default = "")
    title = models.CharField(max_length = 64) #char fields are directly translated to MongoDB Strings
    spec = models.FileField(upload_to='uploads')
    number_of_submissions = models.IntegerField() #Integer Fields will be translated to one of the MongoDB Integer types (I don't actually know which one, I think int32)
    best_solution = models.FileField()
    language = models.CharField(max_length = 64)
    datasets = models.FileField(upload_to='uploads')
    code = models.FileField(upload_to='uploads')
    tags = models.ListField() #List fields are the Array BSON type and allow us to store compound data along with DictFields, making us unormalized, but this is standard for NoSQL pattern databases.
    is_approved = models.BooleanField(default = False)
    creation_date = models.DateTimeField(default = None)

    objects = models.DjongoManager()

class Submission(models.Model):
    _id = models.ObjectIdField(default = None)
    submission_id = models.IntegerField(default = 0)
    submitting_user = models.CharField(max_length = 64)
    is_for_question = models.CharField(max_length = 64) #This might end up needing to be another ObjectID field, currently under consideration
    time_result = models.FloatField(default = 0.0) #FloatFields will be stored as Mongo decimals, precision may need consideration
    memory_result = models.FloatField(default = 0.0)
    tmp_files_created = models.IntegerField(default = 0)
    src_size = models.FloatField(default = 0.0)
    overall_result = models.FloatField(default = 0.0)
    rank = models.IntegerField() #This is going to have to either be recomputed on the DB end every time a new document is added, or have to be computed at runtime when queried, both are going to impact performance somewhat
    number_of_confirmations = models.IntegerField(default = 0)
    src_file = models.FileField(upload_to='uploads', default = "")
    creation_date = models.DateTimeField(default=None)
    pass_status = models.CharField(max_length = 4, default = "Fail")

    objects = models.DjongoManager()

class Node(models.Model):
    _id = models.ObjectIdField(default = None)
    node_name = models.CharField(max_length = 64)
    creators_name = models.CharField(max_length = 128, default = "")
    members = models.DictField(default = {})
    current_ip_address=models.CharField(max_length = 24, default = '0.0.0.0')

    objects = models.DjongoManager()

class Login(models.Model):
    _id = models.ObjectIdField(default = None)
    username = models.CharField(max_length = 64)
    salt = models.CharField(max_length = 64) #Salt will be added programmatically, possibly as part of the Django middleware
    hashed_password = models.CharField(max_length = 64) #This is the only form of the password we will be storing

    objects = models.DjongoManager()

class Client(models.Model):
    _id = models.ObjectIdField(default = None)
    username = models.CharField(max_length = 64)
    email = models.CharField(max_length = 200, default = "")
    memberships = models.DictField(default = {})

    objects = models.DjongoManager()

class Tags(models.Model):
    #No Mongo object ID is needed here, as the name of the tag will be able to serve as the primary key (which nicely prevents two people creating different tags for the same thing, though machine_learning, machinelearning, machine-learning, machineLearning and MachineLearing would all be able to )
    # be stored unless we use some sanitization on tag creation, say enforce lowercase and no punctutation, or select from set (which uses a different backend method)
    name = models.DictField(default = {})
    objects = models.DjongoManager()

class Dataset(models.Model):
    _id = models.ObjectIdField()
    dataset_id = models.IntegerField()
    submitter_name = models.CharField(max_length = 64)
    relevant_questions = models.ListField()
    actual_data = models.FileField()
    is_approved = models.BooleanField(default = False)

    objects = models.DjongoManager()

class Metadata(models.Model):
    _id = models.ObjectIdField()
    getter_name = models.CharField(default = "Meta", max_length = 4)
    next_question_id = models.IntegerField()
    next_submission_id = models.IntegerField()
    next_dataset_id = models.IntegerField()

    objects = models.DjongoManager()

class Test(models.Model):
    file = models.FileField(upload_to='uploads')
