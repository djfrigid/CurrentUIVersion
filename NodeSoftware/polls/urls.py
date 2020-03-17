from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),
    path('user', views.user, name='user'),
    path('logout', views.logout, name='logout'),
    path('submissions_new/<str:for_question>', views.submissions_new, name='submissions_new'),
    path('submissions_all_my_subs', views.submissions_all_my_subs, name='submissions_all_my_subs'),
    path('submissions_spec_my_subs/<str:for_question>', views.submissions_spec_my_subs, name='submissions_spec_my_subs'),
    path('submissions_details/<int:submission_id>', views.submissions_details, name = 'submissions_details'),
    path('register_client', views.register_client, name='register_client'),
    path('register_node', views.register_node, name='register_node'),
    path('register', views.register, name = 'register'),
    path('user_invite', views.user_invite, name = 'user_invite'),
    path('questions', views.questions, name='questions'),
    path('questions_create', views.questions_create, name='questions_create'),
    path('questions_mine', views.questions_mine, name = 'questions_mine'),
    path('questions_details/<str:question_name>', views.questions_details, name = "questions_details"),
    path('questions_approve_question/<str:question_name>', views.questions_approve_question, name = "questions_approve_question"),
    path('questions_deny_question/<str:question_name>', views.questions_deny_question, name = "questions_deny_question"),
    path('datasets_approve_dataset/<int:dataset_id>', views.datasets_approve_dataset, name = "datasets_approve_dataset"),
    path('datasets_deny_dataset/<int:dataset_id>', views.datasets_deny_dataset, name = "datasets_deny_dataset"),
    path('node_clients_all', views.node_clients_all, name = 'node_clients_all'),
    path('approvals_questions', views.approvals_questions, name = 'approvals_questions'),
    path('approvals_datasets', views.approvals_datasets, name = 'approvals_datasets'),
    path('user_change_privilege/<str:username>', views.user_change_privilege, name = 'user_change_privilege'),
    path('user_change_privilege_all_clients/<str:username>', views.user_change_privilege_all_clients, name = 'user_change_privilege_all_clients'),
    path('user_remove_from_node/<str:username>', views.user_remove_from_node, name = 'user_remove_from_node'),
    path('clients_all', views.clients_all, name = 'all_clients'),
    path('download_dataset', views.download_dataset, name = 'download_dataset'),
    path('delete_content_question/<int:question_id>', views.delete_content_question, name='delete_content_question'),
    path('delete_content_submission/<int:submission_id>', views.delete_content_submission, name='delete_content_submission')
]
