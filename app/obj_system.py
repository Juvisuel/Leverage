import json
import os
import datetime
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


local_path = 'F:/learn_neuro/Leverage/app/proj_bases'
static_keys = ['effectivity', 'percent_of_good', 'id', 'status', 'history', 'proj_name', 'local_path', 'avaliable', 'next_tasks', 'issue']
var_dict = {'status': ['free', 'freeze', 'in_work', 'ended', 'cutted'], 'type': ['Project', 'Mailstone', 'Task', 'Idea']}

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
        self.issue = ''
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
        print('before_tasks:', self.before_tasks)
        print('next_tasks:', self.next_tasks)

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
        print('loaded')

    def get_report(self):  #с если есть подзадачи, то собираем данные с них и складываем вместе.
        # если задача, то только с нее  todo нужен еще механизм, который всю систему просчитывает после изменений
        pass

    def save_task(self):
        dict_for_save = self.to_json()
        with open(f'{self.local_path}/{self.proj_name}/{self.id}.json', 'w') as temp:
            json.dump(dict_for_save, temp, ensure_ascii=False)


## вписываем в историю задачи таймштамп и изменение
def change_hist(history, event_type, data, text=''):
    id_for_hist = int(datetime.datetime.now().timestamp())
    history[id_for_hist] = {}
    history[id_for_hist]['type'] = event_type
    history[id_for_hist]['data'] = data
    history[id_for_hist]['text'] = text

    return history

# одно изменение в задаче. обрабатывается в зависимости от ключа
def one_change(dict_for_fill, key):
    print(key, dict_for_fill[key])
    change = input('меняем? 1 - да ')
    change_item = ''
    if change == '1':
        change_item = input('впишите новое значение ')
        print(f'старое значение = {dict_for_fill[key]}, Новое значение  = {change_item} \n')
        # change = input(
        #     f'старое значение = {dict_for_fill[key]}, Новое значение  = {change_item} \n')
        if change_item != '':
            dict_for_fill[key] = change_item
            dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}', change_item)

    return dict_for_fill

# одно заполнение с нуля, обрабатывается в зависимости от ключу
def one_input(dict_for_fill, key):
    print(key, dict_for_fill[key])
    change_item = input('впишите новое значение ')
    # print(f'старое значение = {dict_for_fill[key]}, Новое значение  = {change_item}')
    if change_item != '':
        dict_for_fill[key] = change_item
        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}', change_item)

    return dict_for_fill

# одно изменение второго уровня, обрабатывается в зависимости от ключа и ключа второго уровня
def one_change_2_level(dict_for_fill, key, key_mini):
    print(key, key_mini, dict_for_fill[key][key_mini])
    change = input('меняем? 1 - да ')
    change_item = ''
    if change == '1':
        change_item = input('впишите новое значение ')
        print(f'старое значение {key} {key_mini} = {dict_for_fill[key][key_mini]} \n'
            f'Новое значение = {change_item} \n')
        # change = input(
        #     f'старое значение {key} {key_mini} = {dict_for_fill[key][key_mini]} \n'
        #     f'Новое значение = {change_item} \n')
    if change_item != '':
        dict_for_fill[key][key_mini] = change_item
        dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', change_item)

    return dict_for_fill

# добавление задач в предыдущие или последующие
def connect_tasks(task_obj, proj_name='temp'):
    mini_change = 6
    print()
    print('вы работаете с задачей',task_obj.name )
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
                if file_name[:-5] not in task_obj.before_tasks and file_name[:-5] not in task_obj.next_tasks:
                    with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}', 'r') as temp:
                        temp_task_unchained = json.load(temp)
                        print(temp_task_unchained['id'],'*' , temp_task_unchained['name'],'*' ,
                              temp_task_unchained['target'])
            print()
            type_of_connect = input('Если связываете с предыдущей задачей, выберите 1; если с последующей - 2 ')
            id_new_task = input('впишите id задачи для связи: ')
            if type_of_connect == '1':
                task_obj.before_tasks.append(id_new_task)
                task_obj.history = change_hist(task_obj.history, 'connect_before_tasks', id_new_task)

            elif type_of_connect == '2':
                task_obj.next_tasks.append(id_new_task)
                task_obj.history = change_hist(task_obj.history, 'connect_next_tasks', id_new_task)

    print('saved')
    task_obj.save_task()

## подсчет оставшегося времени
def render_t_avaliable(task):
    return float(task.timing['hours_limit']) - float(task.timing['hours_spent'])

# находим головную задачу (проект)
def find_head(task):
    finded_mailstone = 0
    list_of_next_tasks = task.next_tasks
    while finded_mailstone == 0:
        new_list_of_next_tasks = []
        for new_task_id in list_of_next_tasks:
            with open(f'{task.local_path}/{task.proj_name}/{new_task_id}.json', 'r') as temp:
                task_json = json.load(temp)
            if task_json['type'] != 'Project':
                new_list_of_next_tasks.extend(task.next_tasks)
            else:
                return task_json['id']

        list_of_next_tasks = new_list_of_next_tasks.copy()


# находим мэйлстоун, под которым лежит задача
def find_route_mailstone(task):
    finded_mailstone = 0
    list_of_next_tasks = task.next_tasks
    while finded_mailstone == 0:
        new_list_of_next_tasks = []
        for new_task_id in list_of_next_tasks:
            with open(f'{task.local_path}/{task.proj_name}/{new_task_id}.json', 'r') as temp:
                task_json = json.load(temp)
            if task_json['type'] != 'Mailstone':
                new_list_of_next_tasks.extend(task.next_tasks)
            else:
                return task_json['id']

        list_of_next_tasks = new_list_of_next_tasks.copy()

# создаем объект имеющейся  задачи из ее id, возвращаем объект
def create_task_from_id(task_id, local_path, proj_name):
    task = Task(proj_name)
    with open(f'{local_path}/{proj_name}/{task_id}.json', 'r') as temp:
        task_json = json.load(temp)
    task.from_json(task_json)
    return task


# подгружаем словарь имеющейся задачи по ее id, возвращаем словарь
def get_dict_from_id(task_id, local_path, proj_name):

    with open(f'{local_path}/{proj_name}/{task_id}.json', 'r') as temp:
        task_json = json.load(temp)

    return task_json

# забираем время для задачи с донора, возвращаем измененную задачу и измененного донора
def donor_time(recepient_task, donor_task):
    t_avaliable = render_t_avaliable(recepient_task)
    print('Доступный резерв:', recepient_task.timing['reserved'], 'перерасход времени:', t_avaliable,
          f'Уровень риска задачи: {recepient_task.risk_value}',
          f'Задача исполнена на: {recepient_task.timing["percent_of_good"]}\n')
    add_time = float(input('Добавьте время из резерва, можно ввести дробное через точку:\n'))
    if add_time > t_avaliable and add_time <= float(donor_task.timing['reserv']):
        recepient_task.timing['hours_limit'] = float(recepient_task.timing['hours_limit']) + add_time
        donor_task.timing['reserv'] = float(donor_task.timing['reserv']) - add_time + 0.1

    print('Новое доступное время задачи:', recepient_task.timing['hours_limit'], 'резерв донора', donor_task.timing['reserv'])

    return recepient_task, donor_task

## можно выбрать откуда берем время и долить в задачу
def add_reserv_time_to_task(task):
    t_avaliable = render_t_avaliable(task)
    t_reserved = task.timing['reserv']
    percent_of_good = task.timing['percent_of_good']
    risk_value = task.risk_value
    mailstone_task_id = find_route_mailstone(task)
    mailstone_task = create_task_from_id(mailstone_task_id, task.project_name)
    head_task_id = find_head(task)
    head_task = create_task_from_id(head_task_id, task.project_name)

    choice = input(f'Доступное для задачи время: {t_avaliable} ч\n'
          f'В резерве задачи {t_reserved}.\n'
          f'В резерве мэйлстоуна {mailstone_task.timing["reserv"]}\n'
          f'в резерве всего проекта {head_task.timing["reserv"]}\n'
          f'Уровень риска задачи: {risk_value}\n'
          f'Задача исполнена на: {percent_of_good}\n'
          f'Выберите действие: \n'
          f'1 - добавить времени из резерва задачи\n'
          f'2 - добавить времени из резерва мэйлстоуна \n'
          f'3 - добавить времени из резерва проекта\n'
                   f'4 - оставить как есть')

    if choice == '1':
        task, _ = donor_time(task, task)
        task.save_task()

    elif choice == '2':
        task, mailstone_task = donor_time(task, mailstone_task)
        task.save_task()
        mailstone_task.save_task()

    elif choice == '3':
        task, head_task = donor_time(task, head_task)
        task.save_task()
        head_task.save_task()

    elif choice == '4':
        pass

    return task


### резервирование времени - операция которая задает резерв или меняет его вручную
def operate_t_reserv(task):
    t_all = float(task.timing['hours_limit'])
    t_avaliable = render_t_avaliable(task)
    t_reserved = float(task.timing['reserv'])
    risk_value = int(task.risk_value)
    percent_of_good = float(task.timing['percent_of_good'])
    ## резерв времени должен рассчитываться от риска, и только если резерв вообще не задан
    ## если время исчерпано, то новое время отнимается от резерва

    if t_avaliable <= 0:
        task = add_reserv_time_to_task(task)

    else:
        if risk_value > 0 and t_reserved == 0:  #задача рискованная, но резерв не отложен
            if percent_of_good < 5: ## самое начало
                ## мы резервируем соразмерный риску тайм из доступного
                task.timing['reserv'] = t_avaliable/100*risk_value
                task.timing['hours_limit'] = t_all-task.timing['reserv']
            else:  ## по мере исполнения риск может снижаться
                task.timing['reserv'] = t_avaliable / 100 * risk_value * (100-percent_of_good) / 100
                task.timing['hours_limit'] = t_all - task.timing['reserv']
                t_avaliable = render_t_avaliable(task)

        print('новый резерв задачи', task.timing['reserv'], 'Новое доступное время', t_avaliable)

    return task

## просто показывает все задачи
def show_me_tasks(local_path, proj_name):
    for task_name in os.listdir(f'{local_path}/{proj_name}'):
        with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
            temp_task_dict = json.load(temp)
            print(temp_task_dict['id'],'*' , temp_task_dict['type'],'*' , temp_task_dict['name'])

def show_me_in_work_tasks(local_path, proj_name):
    for task_name in os.listdir(f'{local_path}/{proj_name}'):
        with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
            temp_task_dict = json.load(temp)
            if temp_task_dict['status'] == 'in_work':
                print(temp_task_dict['id'],'*' , temp_task_dict['type'],'*' , temp_task_dict['name'])


def show_me_free_tasks(local_path, proj_name):
    print('свободные задачи')
    for task_name in os.listdir(f'{local_path}/{proj_name}'):

        with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
            temp_task_dict = json.load(temp)
            if temp_task_dict['status'] == 'free':
                print(temp_task_dict['id'],'*' , temp_task_dict['type'],'*' , temp_task_dict['name'])


## ввод времени, сделано без обработчика на ошибки ввода
def input_time(dict_for_fill, key, key_mini):
    time = input('Введите дату в формате YYYY MM DD ')
    time = time.split()
    date = int(datetime.datetime(int(time[0]), int(time[1]), int(time[2])).timestamp())
    dict_for_fill[key][key_mini] = date
    dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', date)
    return dict_for_fill

## изменение отработанного времени
def change_spent_time(task_obj):
    proj_name = task_obj.proj_name
    dict_for_fill = task_obj.to_json()
    key = 'timing'
    key_mini = 'hours_spent'
    print(key, key_mini, dict_for_fill[key][key_mini])
    print('на задачу уже потрачено', dict_for_fill[key][key_mini], 'часов')
    add_time = input('Пожалуйста впишите время + в часах\n')
    add_time = float(add_time)
    new_time = float(dict_for_fill[key][key_mini]) + add_time
    add_text = input('Пожалуйста, впишите описание проведенной работы\n')
    dict_for_fill[key][key_mini] = new_time
    dict_for_fill['history'] = change_hist(dict_for_fill['history'], f'change_{key}_{key_mini}', new_time, add_text)
    print('Новое время', new_time)
    perc = input(f'Пожалуйста впишите текущий процент готовности задачи, '
                 f'прошлый процент = {round(task_obj.timing["percent_of_good"]*100)} \n')


    dict_for_fill['timing']['percent_of_good'] = int(perc)
    if int(perc) >= 100:
        dict_for_fill['status'] = 'ended'
        task_obj.from_json(dict_for_fill)
        check_stat(proj_name)
        task_obj.save_task()


    timing_pers = float(new_time / (float(task_obj.timing['hours_limit'])+0.001) / 100) * 100
    print('планового времени выбрано ', round(timing_pers, 1), 'готовность задачи', perc)
    if timing_pers > float(perc):
        print(f'мы отстаем на {round(timing_pers/(perc/100))}%')
    elif timing_pers < float(perc):
        print('мы работаем с опережением графика')
    else:
        print('точно по плану')
    dict_for_fill['timing']['effectivity'] = round(float(perc) / (float(timing_pers) / 100),1)
    print('эффективность', dict_for_fill['timing']['effectivity'])
    print('сохранено')

    ## ставим задачи на изменение системы

    for file_name in task_obj.before_tasks:
        with open(f'{task_obj.local_path}/{task_obj.proj_name}/{file_name}.json', 'r') as temp:
            temp_task_unchained = json.load(temp)
        temp_task_unchained['issue'] = ['timing', 'hours_spent', add_time]
        temp_task_unchained_obj = Task(proj_name=proj_name)
        temp_task_unchained_obj.from_json(temp_task_unchained)
        temp_task_unchained_obj.save_task()

    task_obj.save_task()
    print('added', add_time)

## заполнение всех пропущенных моментов таска, с нуля. если заполнено - меняем
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
                            temp_proj = Task(proj_name=proj_name)
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

                        if key_mini == 'deadline' or key_mini == 'beginline':
                            print(key_mini)
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

## находим всех наследников задачи и наследников их наследников и возвращаем общий лист
def legacy(temp_task_dict):
    legacy_list = []

    id_level_work_list = temp_task_dict['before_tasks']
    id_level_next_list = []

    while True:

        for id_level in id_level_work_list:
            # print('id_level_work_list', id_level_work_list)
            # print('id_level', id_level)
            legacy_list.append(id_level)
            # print('len_legacy', len(legacy_list))
            task_dict = get_dict_from_id(id_level, temp_task_dict['local_path'], temp_task_dict['proj_name'])
            # print(task_dict)

            before_task_list = task_dict.get('before_tasks', [])
            # print(before_task_list)
            if len(before_task_list) > 0:
                id_level_next_list.extend([str(x) for x in before_task_list])
                # print('id_level_next_list', id_level_next_list)

            # print()
        id_level_work_list = id_level_next_list.copy()
        id_level_next_list = []
        # print()
        # print(123, id_level_work_list, legacy_list)
        # print()
        if len(id_level_work_list) == 0:

            return legacy_list

    return legacy_list

## на вход принимаем задачу в виде дикта, таблицу для отчета и лист со списком ключей, имеющих подуровень
def add_to_table(mini_dict, report_table, multiply_keys):
    new_index = report_table.shape[0]
    for key in mini_dict.keys():
        if key not in multiply_keys:
            report_table.loc[new_index, key] = mini_dict[key]
        elif key == 'money':
            for mini_key in mini_dict[key]:
                report_table.loc[new_index, f'm_{mini_key[:7]}'] = mini_dict[key][mini_key]
        elif key == 'timing':
            for mini_key in mini_dict[key]:
                report_table.loc[new_index, f't_{mini_key[:7]}'] = mini_dict[key][mini_key]
    return report_table

## todo надо написать дата начала, выцепив из истории событие взятия в работу,
# текущий статус то, а также надо видимо временно сохранять эту таблицу в объект пользователя, чтоб по ней что то смотреть
## а значит нужен еще и объект рабочий для этой таблицы какой то
def common_report(local_path, proj_name='news_finder', mode='all'):
    print()
    print()
    print('*****  Отчет  ******')
    multiply_keys = ['history', 'money', 'timing', 'before_tasks', 'next_tasks', 'masters', 'local_path', 'target', 'issue']
    test_obj = Task()
    work_keys = list(test_obj.to_json().keys())
    work_keys = [x for x in work_keys if x not in multiply_keys]
    work_keys.extend([f'm_{x[:7]}' for x in list(test_obj.to_json()['money'].keys())])
    work_keys.extend([f't_{x[:7]}' for x in list(test_obj.to_json()['timing'].keys())])
    dict_of_mailstones = {}

    report_table = pd.DataFrame(columns=[x for x in work_keys])
    print(report_table)
    for task_name in os.listdir(f'{local_path}/{proj_name}'):
        if mode == 'all':
            with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
                temp_task_dict = json.load(temp)
            report_table = add_to_table(temp_task_dict, report_table, multiply_keys)
            if temp_task_dict['type'] == 'Mailstone':
                ## сбор всех наследников мэйлстоуна
                mailstone_list = legacy(temp_task_dict)
                print('returned for', temp_task_dict["name"], len(mailstone_list))
                dict_of_mailstones[f'{temp_task_dict["name"]}'] = [temp_task_dict['timing']['deadline'], mailstone_list]



        elif mode == 'my':
            with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
                temp_task_dict = json.load(temp)
            if temp_task_dict['masters'] == 'Юлия Деген':
                report_table = add_to_table(temp_task_dict, report_table, multiply_keys)

    if mode == 'all':
        print('Проект')
        # print(report_table)
        deadline = report_table.iloc[0]['t_deadlin']
        print(datetime.datetime.fromtimestamp(int(deadline)))

        print('всего задач', report_table.shape[0])
        print('готовность проекта', report_table['t_percent'].sum() / (report_table.shape[0] + 1))
        print('эффективность проекта',
              report_table['t_effecti'].sum() / (report_table.shape[0] + 1))  ## считаться должно не так,
        print('остаток планового бюджета', report_table['m_avaliab'].sum())

        in_work_table = report_table[report_table['status'] == 'in_work']
        if in_work_table.shape[0] > 0:
            print('в работе')
            print(in_work_table)
            print()

        problem_table = report_table[report_table['t_effecti'] < 100]
        problem_table = problem_table[problem_table['status'] == 'free']
        if problem_table.shape[0] > 0:
            print('проблемные свободные задачи')
            print(problem_table)
            print()

        freezed_table = report_table[report_table['status'] == 'freezed']
        if freezed_table.shape[0] > 0:
            print('заморожено')
            print(freezed_table)
            print()
        print('запас времени до дедлайна',
              datetime.datetime.fromtimestamp(int(deadline)) - datetime.datetime.now())
        print()

        print()
        print('Мэйлстоуны')
        for key, mailstone_list in dict_of_mailstones.items():
            print('mailstone', key)
            print(datetime.datetime.fromtimestamp(int(mailstone_list[0])).date())
            mini_table = report_table.drop([x for x in report_table.index if str(report_table.loc[x, 'id'])
                                            not in mailstone_list[1]], axis=0)

            print('всего задач', mini_table.shape[0])
            print('готовность мэйлстоуна', mini_table['t_percent'].sum() / (mini_table.shape[0] + 1))
            print('эффективность мэйлстоуна', mini_table['t_effecti'].sum() / (mini_table.shape[0] + 1))
            print('остаток планового бюджета', mini_table['m_avaliab'].sum())

            in_work_table = report_table[report_table['status'] == 'in_work']
            if in_work_table.shape[0] > 0:
                print('в работе')
                print(in_work_table)
                print()

            problem_table = mini_table[mini_table['t_effecti'] < 100]
            problem_table = problem_table[problem_table['status'] == 'free']
            if problem_table.shape[0] > 0:
                print('проблемные задачи')
                print(problem_table)
                print()

            freezed_table = mini_table[mini_table['status'] == 'freezed']
            if freezed_table.shape[0] > 0:
                print('заморожено')
                print(freezed_table)
                print()

            print('запас времени до дедлайна',
                  datetime.datetime.fromtimestamp(int(mailstone_list[0])) - datetime.datetime.now())
            print()

    elif mode == 'my':
        print('Проект')
        # print(report_table)
        deadline = report_table.iloc[0]['t_deadlin']
        print(datetime.datetime.fromtimestamp(int(deadline)))

        print('всего задач', report_table.shape[0])
        print('готовность в среднем', round(report_table['t_percent'].sum() / (report_table.shape[0] + 0.01),2))
        print('эффективность в среднем %',
              round(report_table['t_effecti'].sum() / (report_table.shape[0] + 0.01),2))  ## считаться должно не так,
        print('остаток планового бюджета', report_table['m_avaliab'].sum())

        problem_table = report_table[report_table['t_effecti'] < 100]
        problem_table = problem_table[problem_table['status'] == 'free']
        print()
        if problem_table.shape[0] > 0:
            print('проблемные свободные задачи:')
            for ind in problem_table.index:
                print(problem_table.loc[ind, 'name'], 'исполнено', problem_table.loc[ind, 't_percent'], 'эффективность',
                      problem_table.loc[ind, 't_effecti'], 'дедлайн', datetime.datetime.fromtimestamp(problem_table.loc[ind, 't_deadlin']).date())
            print()
        freezed_table = report_table[report_table['status'] == 'freezed']
        if freezed_table.shape[0] > 0:
            print('заморожено')
            print(freezed_table)
        print('запас времени до дедлайна',
              datetime.datetime.fromtimestamp(int(deadline)) - datetime.datetime.now())
        print()

    return report_table

# common_report(local_path, mode='my')



def freeze_up_tree(task):

    list_of_next_tasks = task.next_tasks
    if len(list_of_next_tasks) > 0:
        while True:
            new_list_of_next_tasks = []
            for new_task_id in list_of_next_tasks:
                with open(f'{task.local_path}/{task.proj_name}/{new_task_id}.json', 'r') as temp:
                    task_json = json.load(temp)

                next_list = task_json.get('next_tasks', [])
                if len(next_list) > 0:
                    new_list_of_next_tasks.extend(next_list)

                if task_json['type'] != 'Project':
                    if task_json['status'] != 'freezed':
                        print('i find task to freese', task_json['name'])
                        task_json['status'] = 'freezed'
                        temp_task = Task(task.proj_name)
                        temp_task.from_json(task_json)
                        temp_task.save_task()

                else:

                    return 'ok'

            list_of_next_tasks = new_list_of_next_tasks.copy()

    else:
        return 'end'


def unfreeze_up(task):

    list_of_next_tasks = task.next_tasks
    if len(list_of_next_tasks) > 0:
        for new_task_id in list_of_next_tasks:
            with open(f'{task.local_path}/{task.proj_name}/{new_task_id}.json', 'r') as temp:
                task_json = json.load(temp)
                before_list = task_json.get('before_tasks', [])
                if len(before_list) > 0:
                    for before_task_id in before_list:
                        pass


    else:
        print('end')

### проверяет статусы задач и фризит верхний уровень если что
def check_stat(project_name):

    ## находим названия проектов

    for task_id in os.listdir(f'{local_path}/{project_name}'):
        task_id = task_id[:-5]
        temp_dict = get_dict_from_id(task_id, local_path, project_name)

        ## нужно находить конечные задачи, у которых нет предшественников, смотреть их статус
        ## если статуса нет, присваивать free
        ## если статус есть, и он не завершен и не остановлен, искать ее предшественника, и если это не проект то фризить, а затем его предшест
        ## венника и фризить
        print(f'i find {temp_dict["status"]} task', temp_dict['name'])
        if len(temp_dict['before_tasks']) == 0:
            if temp_dict['status'] not in ['ended', 'cutted', 'in_work', 'free', '']:
                temp_dict['status'] = 'free'
                print('i make it free')
                task = Task(project_name)
                task.from_json(temp_dict)
                task.save_task()
                freeze_up_tree(task)

            elif temp_dict['status'] == 'free':
                if 100 > float(temp_dict['timing']['percent_of_good']) > 0:
                    print('i find in work task', temp_dict["name"])
                    temp_dict['status'] = 'in_work'
                    task = Task(project_name)
                    task.from_json(temp_dict)
                    freeze_up_tree(task)
                    task.save_task()

                elif int(temp_dict['timing']['percent_of_good']) >= 100:
                    print('i find ended task', temp_dict["name"])
                    temp_dict['status'] = 'ended'
                    task = Task(project_name)
                    task.from_json(temp_dict)
                    task.save_task()


        else:
            print('has before')
            if temp_dict['status'] == 'free' or temp_dict['status'] == '':
                ## мы должны проверить верно ли что все задачи ниже выполнены или остановлены
                before_pool = legacy(temp_dict)
                print(before_pool)
                for before_task_id in before_pool:
                    if get_dict_from_id(before_task_id, local_path, project_name)['status'] not in ['ended', 'cutted']:
                        temp_dict['status'] = 'freezed'
                        task = Task(project_name)
                        task.from_json(temp_dict)
                        task.save_task()
                        freeze_up_tree(task)

                ## мы должны проверить что задача не начата
                if 100 > float(temp_dict['timing']['percent_of_good']) > 0:
                    print('i find in work task', temp_dict["name"])
                    temp_dict['status'] = 'in_work'
                    task = Task(project_name)
                    task.from_json(temp_dict)
                    task.save_task()
                    freeze_up_tree(task)

                elif int(temp_dict['timing']['percent_of_good']) >= 100:
                    print('i find ended task', temp_dict["name"])
                    temp_dict['status'] = 'ended'
                    task = Task(project_name)
                    task.from_json(temp_dict)
                    task.save_task()
                    unfreeze_up(task)


            else:
                print(f'i find {temp_dict["status"]} task: {temp_dict["name"]}')

    print('i checked all')
    print()






    ## проверяем каждую задачу каждого проекта на то, что ее предшествующие задачи завершены.
    ### для этого выстраиваем деревья из них, и проверяем от концов веточек к началу

# check_stat('news_finder')

def check_time(local_path, proj_name):
    ## разбираем по мэйлстоунам
    dict_of_mailstones = {}

    for task_name in os.listdir(f'{local_path}/{proj_name}'):
            with open(f'{local_path}/{proj_name}/{task_name}', 'r') as temp:
                temp_task_dict = json.load(temp)
            if temp_task_dict['type'] == 'Mailstone':
                ## сбор всех наследников мэйлстоуна
                mailstone_list = legacy(temp_task_dict)
                print('returned for', temp_task_dict["name"], len(mailstone_list))
                dict_of_mailstones[f'{temp_task_dict["name"]}'] = [temp_task_dict['timing']['deadline'], mailstone_list]
    for mailstone in dict_of_mailstones.keys():
        spent_time = 0
        for task in dict_of_mailstones[mailstone]:
            spent_time += task['timing']['hours_spent']
        print(spent_time)

def check_system(project_name):
    ## здесь все задачи проекта должны быть проверены на наличие pending изменений. (какой то
    ## слот, который содержит позицию для изменения и возможно содержит данные для нее)
    ## если находится такое изменение, задача уходит на change
	pass


def change_system(project_name, task_id, key, change, mini_key=' '):
    ## здесь при любом изменении должны проверяться задачи выше и ниже уровнем. после применений
    ## изменений к задаче, нужно чтобы висящие изменения удалялись и слот для них был чистый
    ## например при добавлении времени на исполнение задачи, меняется ее бюджет, меняется время ,
    ## уже затраченное на проект. уменьшается лимит времени свободного в задаче. Словно должна быть
    ## иерархическая система, которая держит в себе именно принципы связей и регламенты . и там важно направление,
    ## получается что это типа граф.
    ## и надо понимать что мы можем уйти в бесконечный цикл изменений, если не обозначим то, что должно быть изменено и
    ## что уже нет

	pass