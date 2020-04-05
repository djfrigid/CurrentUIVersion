from django.shortcuts import render #This function renders HTML templates
from django.http import HttpResponseRedirect, FileResponse #HTTPResponseRedirects and FileResponses are used to either redirect the user to another page while preserving session data or to return files respectively.
from django.core.paginator import Paginator #Django Paginator Object, used for table pagination
from django.utils.text import slugify #Translates strings to URLs
from django.contrib.auth.models import User #Inbuilt part of login middleware
from secrets import token_hex #Generates a 24 character hash for use as a Mongo ObjectId
import datetime #Datetime module, the function we actually use gets the current time at UTC
from random import choice #Used to randomly select elements from lists

from .forms import * # From the other key Django files, import everything
from .models import * # Will be removed after login rework
from .utils import * # One dm_controller will be created here for views to use in the case they need non ORM based access.

from modules.dm_controller import dm_controller

def index(request):
    return render(request, 'index.html')

# +-----------+
# | ENDPOINTS |
# +-----------+

'''

d s.   d       b sss sssss d    d
S  ~O  S       S     S     S    S
S   'b S       S     S     S    S
S sSSO S       S     S     S sSSS
S    O S       S     S     S    S
S    O  S     S      S     S    S
P    P   "sss"       P     P    P

'''

# !! TODO !!: Rework to use Django Login middleware
def login(request):
    login_form = None #Variable must be initialized with a value
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            is_allowed = authenticate_user(login_form.cleaned_data['username'], login_form.cleaned_data['password'])
            if is_allowed:
                request.session['user'] = login_form.cleaned_data['username']
                return HttpResponseRedirect('node_selection/' + request.session['user'])
            else:
                pass #Something needs to get done to say the user's password was wrong
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form' : login_form})

# FINISHED
def node_selection(request, username):
    nodes = Client.objects.get(username=username).memberships
    if not nodes:
        node_list = Node.objects.all()
        node = choice(node_list)
        request.session['current_node'] = node.node_name
        request.session['is_authorized'] = True
        return HttpResponseRedirect('/polls/user')
    else:
        return render(request, 'node_selection.html', {'nodes': nodes})

# FINISHED - Unless we plan on implementing a log back in link? Even then, that will be an update to the template and not this
def logout(request):
    request.session.flush()
    return render(request, 'logout.html')

# Render the admin endpoint.
def admin(request):
    return render(request, 'admin.html')

def user_login_to_node(request, node_name):
    request.session['current_node'] = node_name
    request.session['is_authorized'] = True
    return HttpResponseRedirect('/polls/user')

'''

d    d   sSSSs   d s   sb d sss
S    S  S     S  S  S S S S
S    S S       S S   S  S S
S sSSS S       S S      S S sSSs
S    S S       S S      S S
S    S  S     S  S      S S
P    P   "sss"   P      P P sSSss

'''

# FINISHED
def user(request):
    return render(request, 'user.html')

'''

  sSSSs   d       b d sss     sss. sss sssss d   sSSSs   d s  b   sss.
 S     S  S       S S       d          S     S  S     S  S  S S d
S       S S       S S       Y          S     S S       S S   SS Y
S       S S       S S sSSs    ss.      S     S S       S S    S   ss.
S       S S       S S            b     S     S S       S S    S      b
 S   s S   S     S  S            P     S     S  S     S  S    S      P
  "sss"ss   "sss"   P sSSss ` ss'      P     P   "sss"   P    P ` ss'

'''

# Render the questions page
def questions(request):
    question_set = Question.objects.all().filter(is_approved = True)
    return render(request, 'questions.html', {'question_set' : question_set} )

#
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

#
def questions_mine(request):
    question_set = Question.objects.all()
    question_set = question_set.filter(submitting_user = request.session['user'])
    return render(request, 'questions_mine.html', {'question_set' : question_set})

#
def questions_details(request, question_name):
    question_data = Question.objects.get(title = question_name)
    spec = question_data.spec.read().decode('utf-8')
    dataset = question_data.datasets.read().decode('utf-8')
    # solution = question_data.best_solution.read().decode('utf-8') needs file associating with the field to work properly.
    return render(request, 'questions_details.html', {'question' : question_data, 'Specification' : spec, 'dataset' : dataset})

def sort_table(request, sort_by, sort_order):
    if sort_order == "descending":
        question_set = Question.objects.all().filter(is_approved = True).order_by("-"+sort_by)
    elif sort_order == "ascending":
        question_set = Question.objects.all().filter(is_approved = True).order_by(sort_by)
    request.session['current_sort'] = sort_by
    request.session['current_sort_direction'] = sort_order
    return render(request, 'questions.html', {'question_set' : question_set})

'''

  sss. d       b d ss.  d s   sb d   sss.   sss. d   sSSSs   d s  b   sss.
d      S       S S    b S  S S S S d      d      S  S     S  S  S S d
Y      S       S S    P S   S  S S Y      Y      S S       S S   SS Y
  ss.  S       S S sSS' S      S S   ss.    ss.  S S       S S    S   ss.
     b S       S S    b S      S S      b      b S S       S S    S      b
     P  S     S  S    P S      S S      P      P S  S     S  S    S      P
` ss'    "sss"   P `SS  P      P P ` ss'  ` ss'  P   "sss"   P    P ` ss'

'''

#
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

#
def submissions_all_my_subs(request):
    submission_set = Submission.objects.all()
    submission_set = submission_set.filter(submitting_user = request.session['user'])
    return render(request, 'submissions_all_my_subs.html', {'submission_set' : submission_set})

#
def submissions_spec_my_subs(request, for_question):
    question_details = Question.objects.get(title = for_question)
    submission_set = Submission.objects.all().filter(submitting_user = request.session['user'])
    return render(request, 'submissions_spec_my_subs.html', {'for_question' : question_details.title, 'submission_set' : submission_set })

#
def submissions_details(request, submission_id):
    submission = Submission.objects.get(submission_id = submission_id)
    return render(request, 'submissions_details.html', {'sub' : submission})

'''

d ss.  d sss     sSSSs   d   sss. sss sssss d sss   d ss.
S    b S        S     S  S d          S     S       S    b
S    P S       S         S Y          S     S       S    P
S sS'  S sSSs  S         S   ss.      S     S sSSs  S sS'
S   S  S       S    ssSb S      b     S     S       S   S
S    S S        S     S  S      P     S     S       S    S
P    P P sSSss   "sss"   P ` ss'      P     P sSSss P    P

'''

# Register a node
def register_node(request):
    register_form = None
    if request.method == "POST":
        register_form = NewNode(request.POST)
        if register_form.is_valid():
            new_node = Node(token_hex(12), register_form.cleaned_data['name'], request.session['user'])
            new_node.members[request.session['user']] = "Creator"
            new_node.save()
            return HttpResponseRedirect('index')
    else:
        register_form = NewNode()
    return render(request, 'register_node.html', {'form' : register_form})

# NEARLY FINISHED - Just needs to add a feedback message when the user inputs their passwords.

def register_client(request):

    client_form = None

    if request.method == "POST":
        client_form = NewClient(request.POST)
        if client_form.is_valid() and client_form.cleaned_data['password'] == client_form.cleaned_data['confirm_password']:
            new_id = token_hex(12)
            user_data = gen_login_data(client_form.cleaned_data['password'])
            new_client = Client(new_id, client_form.cleaned_data['name'], client_form.cleaned_data['email'], {})
            new_login = Login(new_id, client_form.cleaned_data['name'], user_data['salt'], user_data['hashed_password'])
            new_client.save()
            new_login.save()
            return HttpResponseRedirect('index')
    else:
        client_form = NewClient()

    return render(request, 'register_client.html', {'form' : client_form})

#FINISHED

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

def register(request):
    return render(request, 'register.html')

'''

d s.   d ss.  d ss.  d ss.    sSSSs   d    b d s.   d        sss.
S  ~O  S    b S    b S    b  S     S  S    S S  ~O  S      d
S   `b S    P S    P S    P S       S S    S S   `b S      Y
S sSSO S sS'  S sS'  S sS'  S       S S    S S sSSO S        ss.
S    O S      S      S   S  S       S S    S S    O S           b
S    O S      S      S    S  S     S   S   S S    O S           P
P    P P      P      P    P   "sss"     "ssS P    P P sSSs ` ss'

'''

def approvals_datasets(request):
    return render(request, 'approvals_datasets.html')

def approvals_questions(request):
    question_set = Question.objects.all()
    question_set = question_set.filter(is_approved = False)
    return render(request, 'approvals_questions.html', {'question_set' : question_set})

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

'''

  sSSs. d      d d sss   d s  b sss sssss   sss.
 S      S      S S       S  S S     S     d
S       S      S S       S   SS     S     Y
S       S      S S sSSs  S    S     S       ss.
S       S      S S       S    S     S          b
 S      S      S S       S    S     S          P
  "sss' P sSSs P P sSSss P    P     P     ` ss'

'''

#BELIVED FINISHED
def node_clients_all(request):
    client_set = Client.objects.all().filter(memberships__contains=request.session['current_node'])
    node = Node.objects.get(node_name = request.session['current_node'])
    return render(request, 'node_clients_all.html', {'client_set' : client_set, 'node' : node})

def clients_all(request):
    if request.method=="GET":
        form = SearchForm(request.GET)
        if request.GET.get('search_field'):
            client_set = Client.objects.all().filter(username__icontains=request.GET.get('search_field'))
        else:
            client_set = Client.objects.all()
    paginator = Paginator(client_set, 25) #Split the client query set into a set of "pages", each holding 25 clients
    page_num = request.GET.get('page') #Get the current page number from the current request objects GET data
    page_obj = paginator.get_page(page_num) #Get the actual page object from the paginator, this has the actual data in it
    return render(request, 'clients_all.html', {'page' : page_obj, 'form' : form})

# FINISHED - Privilege level will change then reload the page to show the change
def user_change_privilege(request, username):
    current_node = Node.objects.get(node_name = request.session['current_node'])
    members = current_node.members
    if username in members.keys():
        if members[username] == "Creator":
            pass #Replace with a message saying creator cannot be unadminned, and a HttpResponseRedirect to page
        elif members[username]  == "Client":
            user_data.current_privilege = "Admin"
        else:
            user_data.current_privilege = "Client"
    else:
        pass #Replace with saying user doesn't exist and the system has errored, and a HttpResponseRedirect to page again.
    current_node.save()
    return HttpResponseRedirect('/polls/node_clients_all')

def user_remove_from_node(request, username):
    node = Node.objects.get(node = request.session['current_node'])
    node.members.remove(username)
    node.save()
    return HttpResponseRedirect('/polls/user')

def delete_my_account(request, username):
    pass

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

'''

d ss    d s.   sss sssss d s.     sss. d sss   sss sssss   sss.
S   ~o  S  ~O      S     S  ~O  d      S           S     d
S     b S   `b     S     S   `b Y      S           S     Y
S     S S sSSO     S     S sSSO   ss.  S sSSs      S       ss.
S     P S    O     S     S    O      b S           S          b
S    S  S    O     S     S    O      P S           S          P
P ss"   P    P     P     P    P ` ss'  P sSSss     P     ` ss'

'''

def datasets_details(request, dataset_id):
    dataset = Dataset.objects.get(dataset_id = dataset_id)
    content = dataset.actual_data.read().decode('utf-8')
    return render(request, 'datasets_details.html', {'dataset' : dataset, 'content' : content})

#Not yet tested
def download_dataset(request, dataset_id):
    dataset = Dataset.objects.get(dataset_id=dataset_id)
    file_name, file_extension = os.path.splitext(dataset.file.file.name)
    file_extension = file_extension[1:]
    response = FileResponse(dataset.file.file, content_type = "file/%s" % file_extension)
    response['Content-Disposition'] = 'attachment;'\
    'filename=%s.%s' %(slugify(dataset.file.name) [:100], file_extension)
    return response

'''

d    d d s.   d ss.  d ss         d ss    d sss   d      d sss   sss sssss d sss
S    S S  ~O  S    b S   ~o       S   ~o  S       S      S           S     S
S    S S   `b S    P S     b      S     b S       S      S           S     S
S sSSS S sSSO S sS'  S     S      S     S S sSSs  S      S sSSs      S     S sSSs
S    S S    O S   S  S     P      S     P S       S      S           S     S
S    S S    O S    S S    S       S    S  S       S      S           S     S
P    P P    P P    P P ss"        P ss"   P sSSss P sSSs P sSSss     P     P sSSss

'''

def user_hard_delete(request, username):
    user = Client.objects.get(username = username)
    associated_submissions = Submission.objects.all().filter(submitting_user = username)
    associated_questions = Question.objects.all().filter(submitting_user = username)
    associated_datasets = Dataset.objects.all().filter(submitter_name = username)
    return render(request, 'user_hard_delete.html', {'user' : user, 'submissions' : associated_submissions, 'questions' : associated_questions, 'datasets' : associated_datasets})

def hard_delete_question(request, question_title):
    question = Question.objects.get(title = question_title)
    question.delete()
    return HttpResponseRedirect('polls/user_hard_delete')

def hard_delete_submission(request, submission_id):
    submission = Submission.objects.get(submission_id = submission_id)
    submissiion.delete()
    return HttpResponseRedirect('polls/user_hard_delete')

def hard_delete_dataset(request, dataset_id):
    dataset = Dataset.objects.get(dataset_id = dataset_id)
    dataset.delete()
    return HttpResponseRedirect('polls/user_hard_delete')

def node_delete(request):
    pass

'''

sss sssss d sss     sss. sss sssss
    S     S       d          S
    S     S       Y          S
    S     S sSSs    ss.      S
    S     S            b     S
    S     S            P     S
    P     P sSSss ` ss'      P

'''

def test(request):
    file_form = None
    if request.method == "POST":
        file_form = TestForm(request.POST, request.FILES)
        if file_form.is_valid():
            t = request.FILES.getlist('multi_file_field')
            nd1 = Dataset(token_hex(12), 5, "Test", [], t[0], False)
            nd2 = Dataset(token_hex(12), 6, "Test", [], t[1], False)
            nd1.save()
            nd2.save()
            return HttpResponseRedirect('/polls/index')
        else:
            print(file_form.errors)
    else:
        file_form = TestForm()
    return render(request, 'test.html', {'form' : file_form})
