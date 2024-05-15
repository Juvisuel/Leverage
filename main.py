import json
import os
from app import obj_system

proj_name = 'news_finder'
local_path = 'F:/learn_neuro/Leverage/app/proj_bases'
static_keys = ['effectivity', 'percent_of_good', 'id', 'status', 'history', 'proj_name', 'local_path', 'avaliable', 'next_tasks']
multiply_keys = ['timing', 'money']
var_dict = {'status': ['free', 'freezed', 'in_work', 'ended', 'cutted'], 'type': ['Project', 'Mailstone', 'Task', 'Idea']}
run_mode = 100



while run_mode > 0:
	if run_mode == 100:
		run_mode = int(input('что хотите сделать?\n'
							 '1 - создать новую задачу\n'
							 '2 - изменить задачу или ее связи\n'
							 '3 - посмотреть отчет в целом\n'
							 '4 - посмотреть отчет по вашим задачам\n'
							 '5 - получить прогноз\n'
							 '6 - проверить и заполнить недостающее в задачах\n'
							 '7 - фиксируем рабочее время\n'
							 '8 - выделить время на задачу\n'
							 '9 - проверить фризы\n'
							 '0 - завершить\n'))
	if run_mode == 1:
		# name_task = input('введите название задачи: ')
		temp_proj = obj_system.Task(proj_name=proj_name)
		# temp_proj.name = name_task
		obj_system.fill_task(temp_proj, proj_name=proj_name)
		run_mode = 100

	elif run_mode == 2:
		action = input('что хотите сделать? \n1 - изменить связи задач и создать подзадачи\n'
						   '2 - изменить данные для задачи\n0 - вернуться\n')
		if action == '1':
			obj_system.show_me_tasks(local_path, proj_name)
			task_id = int(input('Выберите задачу\n'))
			## подгружаем объект

			with open(f'{local_path}/{proj_name}/{task_id}.json', 'r') as temp:
				task_json = json.load(temp)
			task_obj = obj_system.Task(proj_name=proj_name)
			task_obj.from_json(task_json)
			obj_system.connect_tasks(task_obj, proj_name=proj_name)
			action = '0'

		elif action == '2':
			obj_system.show_me_free_tasks(local_path, proj_name)
			task_id = int(input('Выберите задачу\n'))
			with open(f'{local_path}/{proj_name}/{task_id}.json', 'r') as temp:
				task_json = json.load(temp)
			task_obj = obj_system.Task(proj_name=proj_name)
			task_obj.from_json(task_json)
			change_item = ' '
			change_item_small = ' '
			while change_item != '0':
				print()
				task_obj.print_task()
				change_item = input('Что будем менять? (0 - завершить)\n')
				if change_item != '0':
					if change_item not in static_keys and change_item not in multiply_keys:
						print('старое значение:', task_json[change_item])
						if change_item in var_dict.keys():
							print('Варианты:', var_dict[change_item])
						new_value = input('Впишите новое значение \n' )
						task_json[change_item] = new_value

						task_obj.from_json(task_json)
						task_obj.save_task()
						print('сохранено')
					elif change_item in multiply_keys:
						while change_item_small != '0':
							print(task_json[change_item])
							change_item_small = input(f'Что будем менять в {change_item}? (0 - завершить)\n')
							if change_item_small != '0':
								if change_item_small not in static_keys:

									if change_item_small == 'beginline' or change_item_small == 'deadline':
										task_json = obj_system.input_time(task_json, change_item, change_item_small)

									else:
										print('старое значение:', task_json[change_item][change_item_small])
										new_value = input('Впишите новое значение \n')
										task_json[change_item][change_item_small] = new_value

									task_obj.from_json(task_json)
									task_obj.save_task()
									print('сохранено')

		elif action == '0':
			run_mode = 100

	elif run_mode == 3:
		report_rable = obj_system.common_report(local_path, proj_name=proj_name)
		run_mode = 100

	elif run_mode == 4:
		report_rable = obj_system.common_report(local_path, proj_name=proj_name, mode='my')
		run_mode = 100

	elif run_mode == 5:
		print('не готово')
		run_mode = 100

	elif run_mode == 6:
		## проверяем исполненное время и добавляем его в мэйлстоуны и проект
		obj_system.check_spent_time(local_path, proj_name)
		print('не готово')
		run_mode = 100

	elif run_mode == 7:
		obj_system.show_me_in_work_tasks(local_path, proj_name)
		task_id = int(input('Выберите задачу\n'))
		with open(f'{local_path}/{proj_name}/{task_id}.json', 'r') as temp:
			task_json = json.load(temp)
		task_obj = obj_system.Task(proj_name=proj_name)
		task_obj.from_json(task_json)
		obj_system.change_spent_time(task_obj)
		run_mode = 100

	elif run_mode == 8:
		print('не готово')
		run_mode = 100

	elif run_mode == 9:
		obj_system.check_stat(proj_name)
		run_mode = 100