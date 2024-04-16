import json
import os
import datetime
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


local_path = 'F:/learn_neuro/Leverage/app/proj_bases'
static_keys = ['effectivity', 'percent_of_good', 'id', 'status', 'history', 'proj_name', 'local_path', 'avaliable', 'next_tasks']
var_dict = {'status': ['free', 'freeze', 'in_work', 'ended'], 'type': ['Project', 'Mailstone', 'Task', 'Idea']}

class Task:
    def __init__(self, proj_name='temp', local_path=local_path):
        self.id = int(datetime.datetime.now().timestamp())
        self.status = ''
        self.name = ''
        self.money = {'total': 0, 'spent': 0, 'avaliable': 0, 'effectivity': 0, 'reserv': 0}
        self.timing = {'deadline': 0, 'beginline': 0, 'percent_of_good': 0, 'hours_limit': 0, 'hours_spent': 0, 'effectivity': 0, 'reserv': 0}
        self.before_tasks = []  #list_of_ids
        self.next_tasks = []
        self.target = ''
        self.issue = ''  #что надо сделать
        self.masters = []  # list of pers_ids
        self.curator = 0
        self.history = {}  #datetime: {'action': '', task_id: 0, person_id: 0, 'comment': ''}
        self.proj_name = proj_name
        self.local_path = local_path
        self.type = ''
        self.risk_value = 0

    def print_task(self):
        print('вывод информации по проекту')
        print('id:', self.id)
        print('type:', self.type)
        print('name:', self.name)
        print('status:',self.status)
        print('money:', self.money)
        print('timing:', self.timing)
        print('target:', self.target)
        print('issue:', self.issue)
        print('masters:', self.masters)
        print('curator:', self.curator)
        print('proj_name:', self.proj_name)
        print('risk_value:', self.risk_value)

    def to_json(self):
        dict_json = {}
        dict_json['id'] = self.id
        dict_json['type'] = self.type
        dict_json['name'] = self.name
        dict_json['status'] = self.status
        dict_json['money'] = self.money
        dict_json['timing'] = self.timing
        dict_json['before_tasks'] = self.before_tasks
        dict_json['next_tasks'] = self.next_tasks
        dict_json['target'] = self.target
        dict_json['issue'] = self.issue
        dict_json['masters'] = self.masters
        dict_json['curator'] = self.curator
        dict_json['history'] = self.history
        dict_json['proj_name'] = self.proj_name
        dict_json['local_path'] = local_path
        dict_json['risk_value'] = self.risk_value

        return dict_json

    def from_json(self, dict_json):
        self.id = dict_json['id']
        self.name = dict_json['name']
        self.status = dict_json['status']
        self.type = dict_json['type']
        self.money = dict_json['money']
        self.timing = dict_json['timing']
        self.before_tasks = dict_json['before_tasks']
        self.next_tasks = dict_json['next_tasks']
        self.target = dict_json['target']
        self.issue = dict_json['issue']
        self.masters = dict_json['masters']
        self.curator = dict_json['curator']
        self.history = dict_json['history']
        self.proj_name = dict_json['proj_name']
        self.local_path = dict_json['local_path']
        self.risk_value = dict_json['risk_value']
        print('ok')

    def get_report(self):  #с если есть подзадачи, то собираем данные с них и складываем вместе.
        # если задача, то только с нее  todo нужен еще механизм, который всю систему просчитывает после изменений
        pass

    def save_task(self):
        dict_for_save = self.to_json()
        with open(f'{self.local_path}/{self.proj_name}/{self.id}.json', 'w') as temp:
            json.dump(dict_for_save, temp, ensure_ascii=False)


def change_hist(history, event_type, data, text=''):
    id_for_hist = int(datetime.datetime.now().timestamp())
    history[id_for_hist] = {}
    history[id_for_hist]['type'] = event_type
    history[id_for_hist]['data'] = data
    history[id_for_hist]['text'] = text

    return history

def one_change(dict_for_fill, key):
    change = input('меняем? 1 - да ')
    change_item = ''
    while change == '1':
        change_item = input('впишите новое значение ')
        change = input(
            f'старое значение = {dict_for_fill[key]}, Новое значение  = {change_item} \n'
            f'Все ок? Если нет, нажмите 1 - поменять еще раз . Если все ок, нажмите что угодно')
    if change_item != '':
        dict_for_fill[key] = change_item
        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}', change_item)

    return dict_for_fill

def one_input(dict_for_fill, key):
    change_item = input('впишите новое значение ')
    # print(f'старое значение = {dict_for_fill[key]}, Новое значение  = {change_item}')
    if change_item != '':
        dict_for_fill[key] = change_item
        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}', change_item)

    return dict_for_fill

def one_change_2_level(dict_for_fill, key, key_mini):
    change = input('меняем? 1 - да ')
    change_item = ''
    while change == '1':
        change_item = input('впишите новое значение ')
        change = input(
            f'старое значение {key} {key_mini} = {dict_for_fill[key][key_mini]} \n'
            f'Новое значение = {change_item} \nВсе ок? 1 - поменять еще раз ')
    if change_item != '':
        dict_for_fill[key][key_mini] = change_item
        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', change_item)

    return dict_for_fill


def connect_tasks(task_obj, key='before_tasks', proj_name='temp'):
    mini_change = 6
    while int(mini_change) > 0:
        print('связанные задачи - предшественники (без них задачу не начать): ')
        for id_task in task_obj.before_tasks:
            with open(f'{task_obj.local_path}/{task_obj.proj_name}/{id_task}.json', 'r') as temp:
                temp_task_dict = json.load(temp)
                print(temp_task_dict['id'], temp_task_dict['name'])
        print()
        print('связанные задачи - наследники (ждут завершения этой задачи): ')
        for id_task in task_obj.next_tasks:
            with open(f'{task_obj.local_path}/{task_obj.proj_name}/{id_task}.json', 'r') as temp:
                temp_task_dict = json.load(temp)
                print(temp_task_dict['id'], temp_task_dict['name'])
        print()
        mini_change = input('изменить? 1 - убрать одну из задач - предшественников,\n'
                            '2 - создать новую задачу предшественника,\n'
                            '3 - создать задачу - наследника,\n'
                            '4 - связать одну из существующих задач ,\n'
                            '0 - достаточно\n ')

        if mini_change == '1':
            id_for_out = int(input('Впишите ID задачи, которую мы уберем из связки '))
            task_obj.before_tasks.remove(id_for_out)
            task_obj.history = change_hist(task_obj.history, 'remove_before_tasks', id_for_out)
            ## теперь в задаче которую убрали, нет больше бюджета и таймингов от этой связи todo нужна процедура назначения бюджета и тайминга висячим задачам

        elif mini_change == '2':
            name_task = input('введите название задачи: ')
            temp_proj = Task(proj_name=proj_name)
            temp_proj.name = name_task
            temp_proj.target = input('введите краткое описание задачи: ')
            temp_proj.next_tasks = [task_obj.id]
            temp_proj.save_task()
            task_obj.before_tasks.append(temp_proj.id)

            task_obj.history = change_hist(task_obj.history, 'append_new_before_tasks', temp_proj.id)
            ## это означает что нам нужно добавить время и деньги на предыдущую задачу из проекта todo

        elif mini_change == '3':
            name_task = input('введите название задачи: ')
            temp_proj = Task(proj_name=proj_name)
            temp_proj.name = name_task
            temp_proj.before_tasks = [task_obj.id]
            temp_proj.target = input('введите краткое описание задачи: ')
            temp_proj.save_task()
            task_obj.next_tasks.append(temp_proj.id)
            task_obj.history  = change_hist(task_obj.history, 'append_new_next_tasks', temp_proj.id)
            ## это значит что нам нужно выделить из текущей задачи часть бюджета на следующую

        elif mini_change == '4':
            print('несвязанные задачи  ')
            print()
            for file_name in os.listdir(f'{task_obj.local_path}/{task_obj.proj_name}'):
                if file_name[:-4] not in task_obj.before_tasks and file_name[:-4] not in task_obj.next_tasks:
                    with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}', 'r') as temp:
                        temp_task_unchained = json.load(temp)
                        print(temp_task_unchained['id'], temp_task_unchained['target'])
            print()
            type_of_connect = input('Если связываете с предыдущей задачей, выберите 1; если с последующей - 2 ')
            id_new_task = input('впишите id задачи для связи: ')
            if type_of_connect == '1':
                task_obj.before_tasks.append(id_new_task)
                task_obj.history = change_hist(task_obj.history, 'connect_before_tasks', id_new_task)

            elif type_of_connect == '2':
                task_obj.next_tasks.append(id_new_task)
                task_obj.history = change_hist(task_obj.history, 'connect_next_tasks', id_new_task)

    print('ok')
    task_obj.save_task()

def show_me_tasks(local_path, proj_name):
    for task_name in os.listdir(f'{local_path}/{proj_name}'):
        with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
            temp_task_dict = json.load(temp)
            print(temp_task_dict['id'], temp_task_dict['name'])


def input_time(dict_for_fill, key, key_mini):
    time = input('Введите дату в формате YYYY MM DD ')
    time = time.split()
    date = int(datetime.datetime(int(time[0]), int(time[1]), int(time[2])).timestamp())
    dict_for_fill[key][key_mini] = date
    dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', date)
    return dict_for_fill

def fill_task(task_obj, proj_name='temp'):
    dict_for_fill = task_obj.to_json()
    for key in dict_for_fill.keys():
        if key in static_keys:
            pass
        else:
            if type(dict_for_fill[key]) != dict:
                print(key, dict_for_fill[key])
                if key in var_dict.keys():
                    print('варианты', var_dict[key])

                if key == 'before_tasks':
                    mini_change = 6
                    while int(mini_change) > 0:
                        print('связанные задачи - предшественники (без них задачу не начать): ')
                        print()
                        for id_task in dict_for_fill[key]:
                            with open(f'{task_obj.local_path}/{task_obj.proj_name}/{id_task}.json', 'r') as temp:
                                temp_task_dict = json.load(temp)
                                print(temp_task_dict['id'], temp_task_dict['name'])
                        print('связанные задачи - наследники (ждут завершения этой задачи): ')
                        print()
                        for id_task in dict_for_fill['next_tasks']:
                            with open(f'{task_obj.local_path}/{task_obj.proj_name}/{id_task}.json', 'r') as temp:
                                temp_task_dict = json.load(temp)
                                print(temp_task_dict['id'], temp_task_dict['name'])
                        print()
                        mini_change = input('изменить? 1 - убрать одну из задач - предшественников,\n'
                                                '2 - создать новую задачу предшественника,\n'
                                                '3 - создать задачу - наследника,\n'
                                                '4 - связать одну из существующих задач ,\n'
                                                '0 - достаточно\n ')

                        if mini_change == '1':
                            id_for_out = int(input('Впишите ID задачи, которую мы уберем из связки '))
                            task_obj.before_tasks.remove(id_for_out)
                            dict_for_fill['history'] = change_hist(dict_for_fill['history'], 'remove_before_tasks', id_for_out)
                            ## теперь в задаче которую убрали, нет больше бюджета и таймингов от этой связи todo нужна процедура назначения бюджета и тайминга висячим задачам

                        elif mini_change == '2':
                            name_task = input('введите название задачи: ')
                            temp_proj = Task(proj_name=proj_name)
                            temp_proj.name = name_task
                            temp_proj.target = input('введите краткое описание задачи: ')
                            temp_proj.next_tasks = [task_obj.id]
                            temp_proj.save_task()
                            task_obj.before_tasks.append(temp_proj.id)


                            dict_for_fill['history'] = change_hist(dict_for_fill['history'], 'append_new_before_tasks', temp_proj.id)
                            ## это означает что нам нужно добавить время и деньги на предыдущую задачу из проекта todo

                        elif mini_change == '3':
                            name_task = input('введите название задачи: ')
                            temp_proj = Task( proj_name=proj_name)
                            temp_proj.name = name_task
                            temp_proj.before_tasks = [task_obj.id]
                            temp_proj.target = input('введите краткое описание задачи: ')
                            temp_proj.save_task()
                            task_obj.next_tasks.append(temp_proj.id)
                            dict_for_fill['history'] = change_hist(dict_for_fill['history'], 'append_new_next_tasks', temp_proj.id)
                            ## это значит что нам нужно выделить из текущей задачи часть бюджета на следующую

                        elif mini_change == '4':
                            print('несвязанные задачи  ')
                            print()
                            for file_name in os.listdir(f'{task_obj.local_path}/{task_obj.proj_name}'):
                                if file_name[:-4] not in dict_for_fill[key]:
                                    with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}', 'r') as temp:
                                        temp_task_unchained = json.load(temp)
                                        print(temp_task_unchained['id'], temp_task_unchained['name'])
                            print()
                            type_of_connect = input('Если связываете с предыдущей задачей, выберите 1; если с последующей - 2 ')
                            id_new_task = input('впишите id задачи для связи: ')
                            if type_of_connect == '1':
                                task_obj.before_tasks.append(id_new_task)
                                dict_for_fill['history'] = change_hist(dict_for_fill['history'], 'connect_before_tasks', id_new_task)

                            elif type_of_connect == '2':
                                task_obj.next_tasks.append(id_new_task)
                                dict_for_fill['history'] = change_hist(dict_for_fill['history'], 'connect_next_tasks', id_new_task)

                elif key == 'risk_value':
                    if task_obj.type == 'Project':
                        dict_for_fill = task_obj.one_input(dict_for_fill, key)

                    else:  ## среднее всех предшественников
                        change = int(input('задаем вручную или рассчитаем от предыдущих зазач? 1 - вручную, 2 от предыдущих '))
                        if change == 2:
                            if len(task_obj.before_tasks) > 0:
                                all_risk_values = []
                                for file_name in task_obj.before_tasks:
                                    with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}.json', 'r') as temp:
                                        temp_task_unchained = json.load(temp)
                                        all_risk_values.append(temp_task_unchained['risk_value'])
                                mean_value = sum(all_risk_values) / len(all_risk_values)
                                dict_for_fill['risk_value'] = mean_value
                        else:
                            dict_for_fill = one_input(dict_for_fill, key)

                else:
                    dict_for_fill = one_input(dict_for_fill, key)
            else:
                for key_mini in dict_for_fill[key].keys():
                    if key_mini not in static_keys:
                        print(key, key_mini, dict_for_fill[key][key_mini])
                        if key_mini == 'hours_spent' and task_obj.type == 'simple_task':
                            print('на задачу уже потрачено', dict_for_fill[key][key_mini], 'часов')
                            add_time = input('Пожалуйста впишите время + в часах')

                            try:
                                add_time = float(add_time)
                                new_time = float(dict_for_fill[key][key_mini]) + add_time
                                dict_for_fill[key][key_mini] = new_time
                                dict_for_fill['history'] = task_obj.change_hist(f'change_{key}_{key_mini}', new_time)
                                print('Новое время', new_time)
                                perc = input(f'Пожалуйста впишите текущий процент готовности задачи, '
                                             f'прошлый процент = {task_obj.timing["percent_of_good"]} ')
                                dict_for_fill['timing']['percent_of_good'] = float(perc)
                                timing_pers = float(new_time/(float(task_obj.timing['hours_limit']))/100)*100
                                print('планового времени выбрано ', timing_pers, 'готовность задачи', perc)
                                if timing_pers > float(perc):
                                    print('мы отстаем')
                                elif timing_pers < float(perc):
                                    print('мы работаем с опережением графика')
                                else:
                                    print('точно по плану')
                                dict_for_fill['timing']['effectivity'] = float(perc)/(float(timing_pers)/100)*100
                                print('эффективность', dict_for_fill['timing']['effectivity'])
                                print('сохранено')

                                ## пересчитываем затраты времени связанных наверх задач

                                for file_name in task_obj.before_tasks:
                                    with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}.json','r') as temp:
                                        temp_task_unchained = json.load(temp)
                                        print(temp_task_unchained['id'], temp_task_unchained['timing'])
                                        temp_task_unchained['timing']['hours_spent'] = float(temp_task_unchained['timing']['hours_spent']) + add_time

                            except:
                                pass

                        elif key_mini == 'deadline' or key_mini == 'beginline':
                            if dict_for_fill[key][key_mini] == 0:
                                try:
                                    choice = int(input(
                                        'Хотите ввести точную дату? 1 да \nможно не вводить, ее можно будет рассчитать впоследствии или задать только продолжительность  '))

                                    if choice == 1:
                                        time = input('Введите дату в формате YYYY MM DD ')
                                        time = time.split()
                                        date = int(datetime.datetime(int(time[0]), int(time[1]), int(time[2])).timestamp())
                                        dict_for_fill[key][key_mini] = date
                                        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', date)
                                except:
                                    pass

                        else:
                            dict_for_fill = one_change_2_level(dict_for_fill, key, key_mini)

    print()

    for key in dict_for_fill.keys():
        print(key, dict_for_fill[key])

    change = int(input('сохраняем? 1 - да '))
    if change == 1:
        task_obj.from_json(dict_for_fill)
        task_obj.save_task()
        print('готово')


## todo надо написать дата начала, выцепив из истории событие взятия в работу, текущий статус то, а также надо видимо временно сохранять эту таблицу в объект пользователя, чтоб по ней что то смотреть
## а значит нужен еще и объект рабочий для этой таблицы какой то
def common_report(local_path, proj_name='news_finder'):
    multiply_keys = ['history', 'money', 'timing', 'before_tasks', 'next_tasks', 'masters', 'local_path', 'target', 'issue']
    test_obj = Task()
    work_keys = list(test_obj.to_json().keys())
    work_keys = [x for x in work_keys if x not in multiply_keys]
    work_keys.extend([f'm_{x[:6]}' for x in list(test_obj.to_json()['money'].keys())])
    work_keys.extend([f't_{x[:6]}' for x in list(test_obj.to_json()['timing'].keys())])

    report_table = pd.DataFrame(columns=[x for x in work_keys])
    for task_name in os.listdir(f'{local_path}/{proj_name}'):
        with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
            temp_task_dict = json.load(temp)
            new_index = report_table.shape[0]
            for key in temp_task_dict.keys():
                if key not in multiply_keys:
                    report_table.loc[new_index, key] = temp_task_dict[key]
                elif key == 'money':
                    for mini_key in temp_task_dict[key]:
                        report_table.loc[new_index, f'm_{mini_key[:6]}'] = temp_task_dict[key][mini_key]
                elif key == 'timing':
                    for mini_key in temp_task_dict[key]:
                        report_table.loc[new_index, f't_{mini_key[:6]}'] = temp_task_dict[key][mini_key]

    print(report_table)
    print()
    return report_table

# common_report(local_path)


def check_system(project_name, task_id, key, change, mini_key=' '):
    ## здесь при любом изменении должна проверяться вся система. нужен какой то регламент
    ## этих изменений. например при добавлении времени на исполнение задачи, меняется ее бюджет, меняется время ,
    ## уже затраченное на проект. уменьшается лимит времени свободного в задаче. Словно должна быть
    ## иерархическая система, которая держит в себе именно принципы связей и регламенты . и там важно направление,
    ## получается что это типа граф.
    ## и надо понимать что мы можем уйти в бесконечный цикл изменений, если не обозначим то, что должно быть изменено и
    ## что уже нет

	pass