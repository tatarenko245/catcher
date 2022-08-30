import json
import sqlite3

from django.shortcuts import render
from django.http import HttpResponse


from some_functions import get_project_root

root = get_project_root()
menu = ['Головна сторінка', 'Пошук повідомлень в ручному режимі']


def index(request):
    if request.method == "GET":
        return render(
            request, 'goodwin_catcher/index.html',
            {
                'title': 'Головна сторінка'
            }
        )


def manual_searching(request):
    if request.method == "GET":
        available_messages = "No messages yet..."
        query_params = request.GET
        if query_params:

            ocid = query_params['ocid']
            operation_id = query_params['operation_id']

            connection = sqlite3.connect(f"{root}/db.sqlite3")
            cursor = connection.cursor()

            if ocid != "":
                messages_list = list()
                cursor.execute(f"""SELECT message FROM goodwin_catcher_message WHERE ocid = '{ocid}';""")
                message = cursor.fetchall()
                cursor.close()

                for msg in message:
                    messages_list.append(json.loads(msg[0]))

                available_messages = messages_list

            elif operation_id != "":
                cursor.execute(f"""SELECT message FROM goodwin_catcher_message WHERE x_operation_id = 
                '{operation_id}';""")

                message = cursor.fetchall()
                cursor.close()
                print("\nСПРОБА")
                print(message)
                available_messages = json.loads(message[0][0])

        return render(
            request, 'goodwin_catcher/manual_searching.html',
            {
                'title': 'Пошук повідомлень в ручному режимі',
                'messages': json.dumps(available_messages)
            }
        )


def support(request):

    return render(
        request, 'goodwin_catcher/support.html',
        {
            'title': 'Технічна підтримка'
        }
    )


def get_by_x_oper_id(request, x_operation_id):
    if request.method == "GET":
        connection = sqlite3.connect(f"{root}/db.sqlite3")
        cursor = connection.cursor()
        cursor.execute(f"""SELECT message FROM goodwin_catcher_message WHERE x_operation_id = '{x_operation_id}';""")
        message = cursor.fetchall()
        cursor.close()

        response = json.loads(message[0][0])
        return HttpResponse(json.dumps(response))


def get_by_ocid(request, ocid):
    if request.method == "GET":
        messages_list = list()
        connection = sqlite3.connect(f"{root}/db.sqlite3")
        cursor = connection.cursor()
        cursor.execute(f"""SELECT message FROM goodwin_catcher_message WHERE ocid = '{ocid}';""")
        message = cursor.fetchall()
        cursor.close()

        for msg in message:
            messages_list.append(json.loads(msg[0]))

        return HttpResponse(json.dumps(messages_list))
