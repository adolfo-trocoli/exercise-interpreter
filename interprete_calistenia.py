import argparse
import re
from calendar import monthrange

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='file name')
	parser.add_argument('-s', '--search', help='exercise to search for')
	parser.add_argument('-m', '--month', help='month to show, format m or m/y')
	parser.add_argument('-d', '--day', help='day to show, format d/m/y')
	parser.add_argument('--pr', help='personal record of a certain exercise')
	parser.add_argument('-t', '--total', help='total reps for a given exercise, requires -s', action='store_true')
	return parser.parse_args()

def is_header(line):
	'''Returns true if the line is a header.  '''
	return header_regex.match(line)

def print_dict():
	'''Prints the dictionary.  '''
	for key, values in dict.items():
		print(f'{key[:-1]}')
		for value in values:
			print(f'\t{value}')

def add_value(line):
	'''Adds a value to the dictionary.  '''
	if header not in dict.keys():
		dict[header] = [line]
	else:
		dict[header].append(line)

def procesar_modo_busqueda(line):
	global header
	global contador_busqueda
	if is_header(line):
		header = line
	if args.search in line:
		contador_busqueda += 1
		add_value(line.strip())
		if args.total:
			add_reps(line)

def is_month(month, line):
	return month == header_regex.search(line).group(2)

def dias_mes():
	year = '20' + re.search('\d{1,2}/(\d{2})', args.month).group(1)
	month = re.search('(\d{1,2})/\d{2}', args.month).group(1)
	return monthrange(int(year), int(month))[1]

def procesar_modo_mes(line):
	global contador_mes
	if is_header(line) and is_month(args.month, line):
		contador_mes += 1

def is_day(day, line):
	return day == header_regex.search(line).group(1)

def procesar_modo_day(line):
	global day_string
	global selected_day
	if is_header(line):
		if is_day(args.day, line):
			selected_day = True
		else:
			selected_day = False
	elif selected_day and line.strip():
		day_string += ('\t') + line

def is_pr(exercise, line):
	return f'pr {exercise}' in line.lower() 

def get_pr(line):
	pr_regex = '^.*-[\s\w]*:\s*(\d*)'
	return re.search(pr_regex, line).group(1)

def procesar_modo_pr(line):
	global pr_string
	if is_pr(args.pr, line):
		pr_string += header_regex.search(line).group(1) + ': ' + get_pr(line) + '\n'

def add_reps(line):
	global rep_count
	result = rep_regex.search(line)
	if result is None:
		return
	if result.group(2) is not None:
		if result.group(5) is not None:
			rep_count += int(result.group(2)) * int(result.group(3)) + int(result.group(5))
		else:
			rep_count += int(result.group(2)) * int(result.group(3))
	elif result.group(5) is not None:
		rep_count += int(result.group(1)) + int(result.group(5))
	else:
		rep_count += int(result.group(1))
# main
args = parse_arguments()
header_regex = re.compile('(\d{1,2}/(\d{1,2}/\d{2})){1}(\s\(\w*\))?(\s-\s[\w\d\s:]*)?.*')
rep_regex = re.compile('^[a-zA-Z\s]*((\d{1,2})x(\d{1,2})|\d{1,2})(\s?\+\s?(\d{1,2}))?')

dict = dict()
header = ''
contador_busqueda = 0
contador_mes = 0
day_string = ''
selected_day = False
pr_string = ''
rep_count = 0

modo_busqueda = args.search is not None
modo_day = args.day is not None
modo_mes =  args.month is not None
modo_pr = args.pr is not None

with open(args.file) as file:

	for line in file:
		if(modo_busqueda):
			procesar_modo_busqueda(line)
		if(modo_mes):
			procesar_modo_mes(line)
		if(modo_day):
			procesar_modo_day(line)
		if(modo_pr):
			procesar_modo_pr(line)

	if modo_busqueda:
		print(f'\nMostrando ejercicio \'{args.search}\', se ha entrenado {contador_busqueda} veces en {len(dict)} entrenos:')
		print('-----------------------------------------------------------------------------')
		print_dict()
		if args.total:
			print(f'El número total de repeticiones hechas de este ejercicio es {rep_count}\n')
		else:
			print()
	if modo_mes:
		print(f'Se entrenó {contador_mes} de los {dias_mes()} días del mes, un {int(contador_mes / dias_mes() * 100)}%\n')
	if modo_day:
		if len(day_string):
			print(f'\nEl día {args.day} se hizo:\n{day_string}\n')
		else:
			print(f'\nEl día {args.day} no se entrenó\n')
	if modo_pr:
		if len(pr_string):
			print(f'\nSe conocen los siguientes PRs del ejercicio {args.pr}:\n' + pr_string)
		else:
			print(f'\nNo se tienen registros de PRs de \'{args.pr}\'')

