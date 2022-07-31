import argparse
import re
from calendar import monthrange

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='file name')
	parser.add_argument('-s', '--search', help='exercise to search for')
	parser.add_argument('-m', '--month', help='month to show, format m or m/y')
	parser.add_argument('-d', '--day', help='day to show, format d/m/y')
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

def procesar_modo_dia(line):
	pass

# main
args = parse_arguments()
header_regex = re.compile('(\d{1,2}/(\d{1,2}/\d{2})){1}(\s\(\w*\))?(\s-\s[\w\d\s:]*)?.*')
dict = dict()
header = ''
contador_busqueda = 0
contador_mes = 0
modo_busqueda = args.search is not None
modo_dia = args.day is not None
modo_mes =  args.month is not None

with open(args.file) as file:
	for line in file:
		if(modo_busqueda):
			procesar_modo_busqueda(line)
		if(modo_mes):
			procesar_modo_mes(line)
		if(modo_dia):
			procesar_modo_dia(line)
	if(modo_busqueda):
		print(f'\nMostrando ejercicio \'{args.search}\', se ha entrenado {contador_busqueda} veces en {len(dict)} entrenos:')
		print('-----------------------------------------------------------------------------')
		print_dict()
	if(modo_mes):
		print(f'Se entrenó {contador_mes} de los {dias_mes()} días del mes, un {int(contador_mes / dias_mes() * 100)}%')
