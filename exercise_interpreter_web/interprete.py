import re
from calendar import monthrange

header_regex = re.compile('(\d{1,2}/(\d{1,2}/\d{2})){1}(\s\(\w*\))?(\s-\s[\w\d\s:]*)?.*')
rep_regex = re.compile('^[a-zA-Z\s]*((\d{1,2})x(\d{1,2})|\d{1,2})(\s?\+\s?(\d{1,2}))?')
pr_regex = '^.*-[\s\w]*:\s*(\d*)s?'


def lambda_handler(event, context):

	texto, day_string, pr_string, header, response = '', '', '', '', ''
	modo_busqueda, modo_day,modo_mes, modo_pr, selected_day = False, False, False, False, False
	contador_busqueda, contador_mes, rep_count = 0, 0, 0
	dicto = dict()
	
	texto = event['ejercicios']
	modo_busqueda = len(event['search'])
	modo_day = len(event['dia'])
	modo_mes = len(event['mes'])
	modo_pr = len(event['pr'])
		
	def is_header(line):
		'''Returns true if the line is a header.  '''
		return header_regex.match(line)

	def print_dict():
		'''Prints the dictionary.  '''
		nonlocal response
		for key, values in dicto.items():
			response += str(f'{key[:-1]}<br>')
			for value in values:
				response += str(f'\t{value}<br>')

	def add_value(line):
		'''Adds a value to the dictionary.  '''
		nonlocal dicto
		if header not in dicto.keys():
			dicto[header] = [line]
		else:
			dicto[header].append(line)

	def procesar_modo_busqueda(line):
		nonlocal header
		nonlocal contador_busqueda
		if is_header(line):
			header = line
		if event['search'] in line:
			contador_busqueda += 1
			add_value(line.strip())
			if event['total']:
				add_reps(line)

	def is_month(month, line):
		return month == header_regex.search(line).group(2)

	def dias_mes():
		year = '20' + re.search('\d{1,2}/(\d{2})', event['mes']).group(1)
		month = re.search('(\d{1,2})/\d{2}', event['mes']).group(1)
		return monthrange(int(year), int(month))[1]

	def procesar_modo_mes(line):
		nonlocal contador_mes
		if is_header(line) and is_month(event['mes'], line):
			contador_mes += 1

	def is_day(day, line):
		return day == header_regex.search(line).group(1)

	def procesar_modo_day(line):
		nonlocal day_string
		nonlocal selected_day
		if is_header(line):
			if is_day(event['dia'], line):
				selected_day = True
			else:
				selected_day = False
		elif selected_day and line.strip():
			day_string += ('<br>\t') + line

	def is_pr(exercise, line):
		return f'pr {exercise}' in line.lower() 

	def get_pr(line):
		if re.match(pr_regex, line):
			return re.search(pr_regex, line).group(1)

	def procesar_modo_pr(line):
		nonlocal pr_string
		if is_pr(event['pr'], line):
			pr_string += header_regex.search(line).group(1) + ': ' + get_pr(line) + '<br>'

	def add_reps(line):
		nonlocal rep_count
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

	def debug(message):
		print(f"\033[95m{message}\033[0m")
	
	for line in iter(texto.splitlines()):
		if(modo_busqueda):
			procesar_modo_busqueda(line)
		if(modo_mes):
			procesar_modo_mes(line)
		if(modo_day):
			procesar_modo_day(line)
		if(modo_pr):
			procesar_modo_pr(line)

	if modo_busqueda:
		response += str(f'<br>Mostrando ejercicio \'{event["search"]}\', se ha entrenado {contador_busqueda} veces en {len(dicto)} entrenos:<br>')
		print_dict()
		if event['total']:
			response += str(f'El número total de repeticiones de \'{event["search"]}\' es {rep_count}.<br><br>')
		else:
			response += "<br>"
	if modo_mes:
		response += str(f'Se entrenó {contador_mes} de los {dias_mes()} días del mes, un {int(contador_mes / dias_mes() * 100)}%.<br>')
	if modo_day:
		if len(day_string):
			response += str(f'<br>El día {event["dia"]} se hizo:{day_string}<br>')
		else:
			response += str(f'<br>El día {event["dia"]} no se entrenó<br>')
	if modo_pr:
		if len(pr_string):
			response += str(f'<br>Se conocen los siguientes PRs del ejercicio {event["pr"]}:<br>' + pr_string)
		else:
			response += str(f'<br>No se tienen registros de PRs de \'{event["pr"]}\'')

	return {
		'statusCode': 200,
		'body': response
	}

jsonObject = {"ejercicios":"pr muscleup\npino\ntuck lever\ndominadas con goma\n\n10/9/22\nfondos una barra 3x12\nfull planche pies apoyados 3x10s\nflexiones abiertas 3x12\nflexiones pico 3x6\nsentadillas 3x15\ntriceps 3x15\nelevaciones piernas antebrazos paralelas 3x15 (fallo en las ultimas)\n\n9/9/22\ndominadas 4x6\nfront lever raises goma 3x6\ndominadas neutro 3x8\nelevaciones piernas colgado 3x8 (fallo en las últimas)\naustralianas biceps 3x10\nelevaciones rodillas explosivas colgado 3x12\nchinups l-sit negativas 2 \nescapulas\ndeadhang\n\n7/9/22\nintentos de pino\nfondos 3x12\nflexiones bíceps 3x8\nintentos back lever\nflexiones 3x12\nelevaciones piernas oblicuas paralelas 3x8\nflexiones triceps 3x12 (fallo)\nsentadillas 2x20 (se me ha cargado el isquio derecho)\nnegativas muscle-up 2\nescapulas 3x15\ndeadhang rap lolito\n\n6/9/22\ndominadas pecho goma 3x6\nelevaciones piernas colgado 8 + 2x6 (reventao en la parte de subir la espalda)\nchinups 3x8\nfront lever raises goma 6\ntriceps goma 3x12\n\n31/8/22\ndominadas 3x10\naustralianas 3x15\nchinups negativas l-sit 3x3\n\n23/8/22\ndominadas negativas l-sit 4x3\nsentadillas 3x15\nautralianas bíceps barra 3x12\nescalera 3\ngiros cadera goma 3x16\nescapulas 2x15\ndeadhang rap lolito\n\n22/8/22\nfondos 3x14\nintentos de pino\nflexiones 3x16\nelevaciones piernas paralelas 3x10\nflexiones triceps 3x12\nplancha inclinado 3x10s\ntuck lever 3x10s\ndeadhang\n\n21/8/22\ndominadas pecho 3x4\nintentos de muscle-up\nchinups 3x10 (podía hacer más)\nelevaciones rodillas explosivas colgado 3x12\nintentos de pino\nescapulas 3x15\ndeadhang\n\n19/8/22\ndominadas 3x10\nintentos de pino\nchinups negativas en l-sit 3x3\nfront lever raises 3x6\ndominadas cerradas goma 3x10\n\n17/8/22\nfondos 3x12\nintentos de pino\nflexiones 3x15\nfondos deep una barra 3x8\nelevaciones piernas colgado 3x8\nflexiones cadera 3x8\nflexiones abiertas 3x15\n\n16/8/22 - PR DOMINADAS: 13\ndominadas 13\nintentos de pino\ndominadas pecho 4x3\naustralianas cerradas 3x15\nisométrico neutro elevaciones de piernas 3x6 (puedo hacer más por serie)\nescapulas 3x15 \n\n14/8/22 - PR ESCAPULAS: 15\ndominadas pecho 3x3 (cuestan)\ndominadas pecho goma 3x4\ndominadas inverted row 4x2\nchinups 1x6 + 8\nescapulas 3x15\naustralianas barra tres 3x15\nintentos de pino\ncirgulos colgado 3x6\ndeadhang\ntriceps goma 3x12\n\n13/8/22\nfondos 3x12\nintentos de pino\nflexiones cadera 3x10\nfront lever raises goma\n\n11/8/22 (Jueves)\ndominadas pecho goma 3x6\ncirgulos colgado 3x6\ndominadas neutras l-sit 3x8\nseparaciones pared pino 4x1\nelevaciones piernas colgado 3x6\nl-sit 1x20s + 12s (fallo)\nnegativas 4x2\n\n10/8/22 (Miércoles)\nmuscle up 1\ndominadas 3x10\ndominadas neutras 8\n\n8/8/22 (Lunes)\nintentos de pino\nflexiones palmada 3x10\nfront lever raises goma 4x5\nfondos 3x12\nelevaciones piernas paralelas 3x8\nmuscle-up 1\nflexiones diamante 3x10\nescapulas 3x12\ndeadhang\n\n7/8/22 (Sábado)\npiscina 200m\ndominadas 3x8\nescapulas 3x12\n\n6/8/22 (Viernes) - PR MUSCLE-UP: 1\nelíptica 1km en 5:16 min al 7\npiscina 100m\nmuscle-up 5x1 + 1\ndominadas pecho goma 3x6\ncirculos colgado 3x6\ncomando 4x8\nmantener piernas arriba antebrazos 3x15s\nchinups 3x8\ndeadhang\nsentadillas 20 + 10\n\n4/8/22 (Jueves)\nintentos de muscle-up 4\ndominadas explosivas goma 3x6\nmuscle-up goma 7x1\ndominadas negativas 2x3\nescapulas 3x6\n\n3/8/22 (Miércoles)\nfondos una barra explosivos 4x5\nflexiones palmada 3x8\nfondos 3x12\nflexiones pico 3x8\nelevaciones rodillas explosivas colgado 3x12\n\n1/8/22 (Lunes)\nsuperdominadas goma 2x2\ndominadas pecho 3x6\nchinups 3x8\ndominadas l-sit anillas 3x6\ndeadhang 45s + 29s + \n\n31/7/22 (Domingo)\nfondos 3x12\nflexiones 3x12\nflexiones bíceps 3x8\nflexiones tríceps 3x12\nelevaciones piernas paralelas 3x8\ncurl bíceps neutro 8.5kg 3x16\nelevaciones rodillas oblicuo paralelas 3x12\n\n29/7/22 (Viernes)\ndominadas pecho goma 3x6\ndominadas l-sit 3x6\nexplosive knee raises 3x12\nescapulas 3x12\ndominadas neutras 11\n\n28/7/22 (Jueves)\nfondos 3x10\nflexiones 3x12\nelíptica 1km en 5:53 min al 7\npiscina 200m\n\n27/7/22 (Miércoles) \ndominadas pecho 6x2 \nexplosive knee raises 4x10\ndominadas l-sit 3x6\nescapulas 3x12\n\n25/7/22 (Lunes)\nfondos 4x8\nfondos una barra 3x10\nflexiones 4x12\nelevaciones de piernas 3x8\nflexiones abiertas 3x12 \n\n24/7/22 (Domingo)\nsuperdominadas 4x2\ndominadas explosivas 4x3 (probar con una más) \ndominadas l-sit 3x6\ndominadas fallo 7\nescapulas 3x12\nelevaciones oblicuas antebrazos 3x12\nchinups 10\ndominadas neutras 10\n\n19/7/22 (Martes)\nsuperdominadas 4x2\ndominadas pecho 3x4\ndominadas l-sit explosivas 3x3\nescapulas 3x12\nchinups 8\n\n18/7/22 (Lunes)\nFondos explosivos: 4x6\nfondos una barra: 10\nl-sit: 20s\nelevaciones piernas: 4x8\n\n17/7/22 (Domingo) - PR DOMINADAS: 12\ndominadas: 12 (la forma ha sufrido al final)\nsuperdominadas: 3x2 (debería  ir primer ejercicio)\ndominadas en L: 4x3 (puedo hacer más por serie)\nescapulas 4x12 (duro)\n\n14/7/22 (Jueves)\nmixto\n\n12/7/22 (Martes)\nTirar\n\n10/7/22 (Domingo)\nEmpujar\n\n9/7/22 (Sábado)\nTirar\n\n3/7/22 (Domingo) - PR DEADHANG: 60s\nDía 20 plan 22 días\n    deadhang 60s\n    dominadas 4x5\nescapulas 4x10\nlevantamiento piernas colgado 3x5\n\n2/7/22(Sábado) feat. mama\nflexiones 4x12\nl-sit paralelas 4x12s\ntriceps 4x12\nelevaciones piernas paralelas antebrazos \n\n\n1/7/22 (Viernes) feat. mama\nDía 19 plan 22 días\n\n\n27/6/22 (Lunes)\ndominadas 6\nDía 18 plan 22 días\n    chinups 4x6\n    dominadas 4x4\n\n16/6/22 (Miércoles) - PR DOMINADAS: 10\nDía 17 plan 22 días\n    Test bloque 4: 10 maximo + 24 en 5 minutos con descanso de 2 minutos\n\n14/6/22 (Lunes)\nDía 16 plan 22 días\n    Deadhang 45s\n    dominadas 4x4 + 8\nelevaciones oblicuas colgado 4x10\n\n12/6/22 (Sábado)\nDía 15 plan 22 días\n    comando 4x6\n    dominadas 4x4\nelevaciones oblicuas colgado 3x6\naustralianas 3x10\nescapula 4x10\nchinups 4x5 (fallo en la ultima)\n\n11/6/22 (Viernes)\nfondos una barra 4x10\nflexiones diamante suelo 3x10 \nflexiones wide 3x10\nl-sit colgado 3x10s\nfondos 2x12 + 10 (fallo)\nllevar rodillas arriba colgado 4x3\nflexiones 2x15\nelevaciones rodilla colgado 3x8\ntriceps 3x12\ncolgar mano izquierda 20s\ncolgar mano derecha 27s\nelevaciones piernas antebrazos paralelas 3x8\nflexiones pies elevados 3x8\ndeadhang\n\n10/6/22 (Jueves)\nDía 14 plan 22 días\n     chinups 4x5\n     dominadas 3 + 3x4\n dominadas l-sit anillas 3x3\n escapula anillas 4x8\n australianas anillas 4x10\n llevar rodillas arriba colgado 3 + 3x2\n\n8/6/22 (Martes) - PR DOMINADAS: 9\nDía 13 plan 22 días\n     Test bloque 4: 9 maximo + 20 en 5 minutos con descanso de 2 minutos\nescapula 4x8\nnegativas 3x3\naustralianas 3x8\n\n7/6/22 (Lunes) - PR L-SIT: 16s\nfondos 4x8\nflexiones pino pies banco 6 + 4 + 6\nflexiones 4x12\nflexiones diamante 4x8\nl-sit 16s + 2x10s\nl-sit kicks 3x6\nelevaciones oblicuas rodillas en paralelas \n\n6/6/22 (Domingo)\nDía 12 plan 22 días\n     deadhang hasta fallo\n     dominadas 3x3 + 5x4\naustralianas\n\n4/6/22 (Viernes)\nFlexiones suelo 4x10\nelevaciones oblicuas espaldera 3x8\nfondos paralelos 4x8\nL-sit hold 4x5s\nfondos 4x6\ntuck planche hasta L-sit colgado 1x4\ntriceps 4x10\nl-sit kicks 3x6 (tres con cada)\nflexiones pino banco x4\n\n3/6/22 (Jueves) - PR ANTEBRAZOS PARALELAS: 18\nDía 11 plan 22 días\n    comando 4x5 (se me han hecho faciles)\n    dominadas 4x3\nescapula 4x7\naustralianas wide: 4x8\nchinups negativas 4x3\ndeadhang fallo 28s \nelevaciones antebrazos paralelas 18\n\n1/6/22 (Martes)\nFlexiones 4x15\nElevaciones de pelvis espaldera 4x5\nFondos 3x8 + fallo en la 6 (intento de 4x8)\nFlexiones progresion pino 4x8\n\n30/5/22 (Lunes)\nDía 10 plan 22 días\n    chinups 4x5\n    dominadas 4x3\nl-sit 4x4s\nescapulas 4x7\nl-sit kicks 4x6(3 con cada pierna)\ndeadhang\n\n28/5/22 (Sábado) - PRIMER L-SIT (5s)\nfondos 4x8\nintentos fracasados de diferentes flexiones (estoy cansado)\nl-sit kicks una pierna Y HE SACADO L-SIT\nElevaciones rectas oblicuas espaldera 8\n\n27/5/22 (Viernes) - PR DOMINADAS: 8\nDía 9 plan 22 días\n    Test bloque 3: 8 maximo + 18 y varios fallos en 5 minutos\n    con descanso de 2 minutos\nAustralianas 4x9\nEscapulas 4x6\n\n25/5/22 (Miércoles)\nDía 8 plan 22 días\n    deadhang hasta fallo - 42s - estaba resbaloso\n    dominadas 8x3\nchin-ups negativas 3x5\nescapula 5x4\ndeadhang\n\n23/5/22 (Lunes)\nDía 7 plan 22 días\n    20 comando (6 + 6 + 4 + 4)\n    dominadas 4x3\nFlexiones pino 3x10\nFondos una barra  4x7\nFlexiones normales 4x12\nKicks 4x6\nTriceps paralelas 4x10\n\n21/5/22(Sábado)\nDía 6 plan 22 días\n    chinups 3x5 + 4 (no he tirado la quinta para no fallar)\n    dominadas 4x3\nMedios kicks - 4x5\nFlexiones progresion pino - 3x10\nElevaciones pelvis espaldera 4x6\nElevaciones rectas oblicuas espaldera 4x6\ntuck planche paralelas 25s + 18s (los dos fallo)\nflexiones 6x8 (descanso 30s)\nfondos 4x6\n\n\n19/5/22 (Jueves) - PR DOMINADAS: 7\nDía 5 plan 22 días\n    Test bloque 2: 7 maximo + 18 en 5 minutos\n    con descanso de 2 minutos\nTuck planche paralelas 2x 20s\nAustralianas 3x10\nNegativas chin up 2x5\nEscapula 7\nDeadhang 2x30s \nfondos 4x6\n\n17/5/22 (Martes) - PR DEADHANG: 50s\nDía 4 plan 22 días\n    deadhang hasta fallo - 50s max\n    dominadas 7x3\nFondos una barra 3x10 (demasiadas repes)\nFlexiones diamante 4x5\nFlexiones EN SUELO 4x10\nTriceps 4x10\nFlexiones profundas 5x6 (tengo que hacer mas repes por serie)\nbiceps australiana 4x6 (me salen fáciles)\n\n15/5/22 (Domingo)\nDía 3 plan 22 días\n    20 comando (6 + 6 + 4 + 4)\n    9 dominadas rest/pause (1min descanso 3x3)\nElevaciones de pelvis en espaldera 3x6\nFondos 4x5\nFlexiones barra 4x15\nDeadhang 4x30s\nAustralianas 4x10\nFondos una barra 4x5\nElevaciones de rodillas en paralelas 4x8\nIsométrico de dominadas arriba con manos en neutro\n\n13/5/22 (Viernes) - PR FONDOS: 16\nFondos 16\nDía 2 plan 22 días:\n    20 chin-ups rest/pause\n    9 dominadas rest/pause\nElevaciones de pelvis en espaldera 10(máximo por fuerza de agarre) + 3x4\nElevaciones rodillas en paralelas 10 (prueba, muy facil, más difícil en brazos que en core)\nIntento de tuck planche colgado (bastante lejos)\nFloating crunches 2x10\nFlexiones - rutina 9 min buff academy hasta el fall\nBiceps australiana 8\n\n11/5/22 (Miércoles) - PRIMERA VEZ QUE CONSIGO HACER FONDOS DE UNA SOLA BARRA\nDía 1 plan 22 días:\n    Test bloque 1: 6 maximo + 15 en 5 minutos\n    con descanso de 2 minutos\nMolinete con las piernas colgado: 2x6\nLevantar rodillas colgado 2x10\nflexiones barra baja: 3x15\nflexiones hacia abajo (levantando el culo) 4x4\nfondos 4x5\nhe conocido a una madre italiana \nbiceps rollo australiana 4x6\nfondos una barra 4x4\n\n9/5/22 (Lunes)\ndeadhang 2x15s\nflexiones 4x15\nfondos 4x5\n\n8/5/22 (Domingo) - PR DOMINADAS: 6\ndominadas 6\ndominadas negativas 3x5\nretraccion escapular 3x6\ndeadhang 3x15s\ntriceps paralelas bajas 5x10\n2x((plancha(5s) + 3 elevaciones)x3sindescanso)\naustralianas 4x8\nelevaciones en barra una a cada lado 3x8\n\n7/5/22 (Sábado)\n(Dominadasx1 +fondosx2)x10 (sin descanso)\nflexiones profundas en paralelas (3x5)\n\n5/5/22 (Jueves) - PR FONDOS: 13\nfondos: (13) + (4x4)\nflexiones profundas:3x6\nflexiones barra baja 4x8\ndeadhang (4x15s) + 1x15s\nTriceps en barras paralelas bajas 4x12\ntocar delante en el suelo 4x10\ndeadhang sosteniendo rodillas arriba 3x10s\nabdominales inferiores 4x10\n\n4/5/22 (Miercoles) - PR DOMINADAS: 5\ndominadas 5+4\ndominadas negativo 3x5\ndeadhang 3x15\n\n2/5/22 (Lunes)\nlevantamiento rodillas 2x10\nlevantar piernas rectas en tumbona inclinada 3x8\nlevantamiento rodillas cambiando de lado 3x8\n\n1/5/22 (Domingo)\nFlexiones profundas (4x6)\nChin-ups (6 + 4 + dos en negativo + 4 y fallo)\nAbdominales colgado x10\nTriceps en barras paralelas bajas (4x10)\nEjercicio general de abdonminales inferiores x2\n\n30/4/22 (Sábado) \n(Dominadasx1 +fondosx2)x10 (sin descanso)\n\n28/4/22 (Jueves) \nvarias cosas pero no me acuerdo\n\n26/4/22 (Martes) \nDominadas: 1-2-3-3-2-1 + 3 negativas (con dos paradas)\nFlexiones en barras paralelas bajas 4x6\nFondos 4x4\nSemidominadas: 4x10 (4 series de 10)\nEjercicio general de abdominales inferioresx2\nFlexiones 4x10\ndominadas neutro 3","search":"dominadas","mes":"7/22","dia":"17/7/22","pr":"deadhang","total": True}

print(lambda_handler(jsonObject, "hola"))

