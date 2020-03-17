from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse
from django.core.paginator import Paginator
from django.utils.text import slugify
from secrets import token_hex
import datetime

from .forms import *
from .models import *
from .utils import *

def index(request):
    return render(request, 'index.html')

# IN PROGRESS - Just need to add the what happend when it goes wrong parts

def login(request):

    login_form = None

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            is_allowed = authenticate_user(login_form.cleaned_data['username'], login_form.cleaned_data['password'])
            if is_allowed:
                request.session['user'] = login_form.cleaned_data['username']
                request.session['is_authorized'] = True
                return HttpResponseRedirect('user')
            else:
                pass
                #Something needs to get done to say the user's password was wrong
    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'form' : login_form})

#NOT STARTED

def admin(request):
    return render(request, 'admin.html')

# PARTIALLY COMPLETE - This does work, unless you want multiple datasets. Django doesn't have support for this nicely, so we have to find a workaround (or make a new endpoint for adding datasets)

def questions_create(request):

    question_form = None

    if request.method == 'POST':
        question_form = NewQuestion(request.POST, request.FILES)
        if question_form.is_valid():
            metadata = Metadata.objects.get(getter_name = "Meta")
            next_question_id = metadata.next_question_id
            next_dataset_id = metadata.next_dataset_id
            date = datetime.datetime.now()
            new_question = Question(token_hex(12), next_question_id , request.session['user'] , question_form.cleaned_data['title'], request.FILES['spec'], 0, "", question_form.cleaned_data['language'], request.FILES['datasets'], request.FILES.get('code', default = ''), question_form.cleaned_data['tags'] , False, date)
            new_question.save()
            metadata.next_question_id += 1
            metadata.next_dataset_id += 1
            metadata.save()
            new_dataset = Dataset(token_hex(12), next_dataset_id, request.session['user'], [question_form.cleaned_data['title']], request.FILES['datasets'], False) #NOTE - This probably uses the name of the uploaded file. which isn't necessarily the same as the value stored in the question as of now
            new_dataset.save()
            return HttpResponseRedirect('/polls/user')
    else:
        question_form = NewQuestion()

    return render(request, 'questions_create.html', {'form' : question_form})

#FINISHED - Unless we plan on implementing a log back in link? Even then, that will be an update to the template and not this

def logout(request):
    session.flush()
    return render(request, 'logout.html')

#FINISHED

def submissions_all_my_subs(request):
    submission_set = Submission.objects.all()
    submission_set = submission_set.filter(submitting_user = request.session['user'])
    return render(request, 'submissions_all_my_subs.html', {'submission_set' : submission_set})

def submissions_spec_my_subs(request, for_question):
    question_details = Question.objects.get(title = for_question)
    submission_set = Submission.objects.all().filter(submitting_user = request.session['user'])
    return render(request, 'submissions_spec_my_subs.html', {'for_question' : question_details.title, 'submission_set' : submission_set })

def submissions_details(request, submission_id):
    submission = Submission.objects.get(submission_id = submission_id)
    return render(request, 'submissions_details.html', {'sub' : submission})

# NEARLY FINISHED / FINISHED
# Possible addition is to enforce that the nodes are named uniquely, but this isn't technically necessary AFAIK.

def register_node(request):

    register_form = None

    if request.method == "POST":
        register_form = NewNode(request.POST)
        if register_form.is_valid():
            new_node = Node(token_hex(12), register_form.cleaned_data['name'], register_form.cleaned_data['location'])
            new_node.save()
            return HttpResponseRedirect('index')
    else:
        register_form = NewNode()

    return render(request, 'register_node.html', {'form' : register_form})

#NOT STARTED

def questions(request):
    question_set = Question.objects.all()
    question_set = question_set.filter(is_approved = True)
    return render(request, 'questions.html', {'question_set' : question_set} )

#NOT STARTED

def submissions_new(request, for_question):

    submission_form = None

    if request.method == "POST":
        submission_form = NewSubmissionForm(request.POST, request.FILES) #Any form with files will need BOTH post data and files when checking resubmission
        if submission_form.is_valid():
            metadata_entry = Metadata.objects.get(getter_name = "Meta")
            submission_id = metadata_entry.next_submission_id
            metadata_entry.next_submission_id += 1
            metadata_entry.save()
            new_submission = Submission(token_hex(12), submission_id, request.session['user'], for_question , 0.0, 0.0, 0, 0.0, 0.0, 0, 0, request.FILES['submitted_code_file'], datetime.datetime.now())
            new_submission.save()
            question = Question.objects.get(title = for_question)
            question.number_of_submissions += 1
            question.save()
            return HttpResponseRedirect('/polls/user')
    else:
        submission_form = NewSubmissionForm()

    return render(request, 'submissions_new.html', {'form' : submission_form, 'current_question_title' : for_question})

#COMPLETE

def user(request):
    return render(request, 'user.html')

# NEARLY FINISHED - Just needs to add a feedback message when the user inputs their passwords.

def register_client(request):

    client_form = None

    if request.method == "POST":
        client_form = NewClient(request.POST)
        if client_form.is_valid() and client_form.cleaned_data['password'] == client_form.cleaned_data['confirm_password']:
            new_id = token_hex(12)
            user_data = gen_login_data(client_form.cleaned_data['password'])
            new_client = User(new_id, client_form.cleaned_data['name'], client_form.cleaned_data['email'], False)
            new_login = Login(new_id, client_form.cleaned_data['name'], user_data['salt'], user_data['hashed_password'])
            new_client.save()
            new_login.save()
            return HttpResponseRedirect('index')
    else:
        client_form = NewClient()

    return render(request, 'register_client.html', {'form' : client_form})

#FINISHED

def register(request):
    return render(request, 'register.html')

# Functional logic, just needs to actually send the email

def user_invite(request):

    invite_form = None

    if request.method == "POST":
        invite_form = InviteForm(request.POST)
        if invite_form.is_valid():
            return HttpResponseRedirect('index') #Send email
    else:
        invite_form = InviteForm()

    return render(request, 'user_invite.html', {'form' : invite_form})

#COMPLETE

def questions_mine(request):
    question_set = Question.objects.all()
    question_set = question_set.filter(submitting_user = request.session['user'])
    return render(request, 'questions_mine.html', {'question_set' : question_set})

#Again, solid logic, but needs to actually do the right thing.

def node_clients_all(request):
    client_set = User.objects.all()
    return render(request, 'node_clients_all.html', {'client_set' : client_set})

def clients_all(request):
    client_set = User.objects.all()
    paginator = Paginator(client_set, 25) #Split the client query set into a set of "pages", each holding 25 clients
    page_num = request.GET.get('page') #Get the current page number from the current request objects GET data
    page_obj = paginator.get_page(page_num) #Get the actual page object from the paginator, this has the actual data in it
    return render(request, 'clients_all.html', {'page' : page_obj})

#Not yet started

def approvals_datasets(request):
    return render(request, 'approvals_datasets.html')

def approvals_questions(request):
    question_set = Question.objects.all()
    question_set = question_set.filter(is_approved = False)
    return render(request, 'approvals_questions.html', {'question_set' : question_set})

def questions_details(request, question_name):
    question_data = Question.objects.get(title = question_name)
    spec = question_data.spec.read().decode('utf-8')
    dataset = question_data.datasets.read().decode('utf-8')
    return render(request, 'questions_details.html', {'question' : question_data, 'Specification' : spec, 'dataset' : dataset, 'dataset_id' : dataset_id})

def questions_approve_question(request, question_name):
    question  = Question.objects.get(title = question_name)
    question.is_approved = True
    question.save()
    return HttpResponseRedirect('/polls/user')

def questions_deny_question(request, question_name):
    question  = Question.objects.get(title = question_name)
    question.delete()
    return HttpResponseRedirect('/polls/user')

def datasets_approve_dataset(request, dataset_id):
    dataset  = Dataset.objects.get(title = dataset_id)
    dataset.is_approved = True
    dataset.save()
    return HttpResponseRedirect('/polls/user')

def datasets_deny_dataset(request, dataset_id):
    dataset  = Dataset.objects.get(title = dataset_id)
    dataset.delete()
    return HttpResponseRedirect('/polls/user')

# FINISHED - Privilege level will change then reload the page to show the change

def user_change_privilege(request, username):
    user_data = User.objects.get(username = username)
    if user_data.current_privilege == "Client":
        user_data.current_privilege = "Admin"
    else:
        user_data.current_privilege = "Client"
    user_data.save()
    return HttpResponseRedirect('/polls/node_clients_all')

#Copy of above function, but for the all node clients endpoint

def user_change_privilege_all_clients(request, username):
    user_data = User.objects.get(username = username)
    if user_data.current_privilege == "Client":
        user_data.current_privilege = "Admin"
    else:
        user_data.current_privilege = "Client"
    user_data.save()
    return HttpResponseRedirect('/polls/clients_all')

def user_remove_from_node(request, username):
    node = Node.objects.get(node = request.session['current_node'])
    node.members.remove(username)
    node.save()
    return HttpResponseRedirect('/polls/user')

def delete_my_account(request, username):
    pass

#Not yet tested
def download_dataset(request, dataset_id):
    dataset = Dataset.objects.get(dataset_id=dataset_id)
    file_name, file_extension = os.path.splitext(dataset.file.file.name)
    file_extension = file_extension[1:]
    response = FileResponse(dataset.file.file, content_type = "file/%s" % file_extension)
    response['Content-Disposition'] = 'attachment;'\
    'filename=%s.%s' %(slugify(dataset.file.name) [:100], file_extension)
    return response

def delete_content_question(request, question_id):
    question = Question.objects.get(question_id = question_id)
    datasets = Dataset.objects.all().filter(relevant_questions__contains=question.question_id)
    submissions = Submission.objects.all().filter(is_for_question__contains=question.title)
    print(question)
    print(datasets)
    print(submissions)
    return HttpResponseRedirect('/polls/questions_mine')

def delete_content_submission(request, submission_id):
    submission = Submission.objects.get(submission_id = submission_id)
    submission.delete()
    return HttpResponseRedirect('/polls/submissions_all_my_subs')
