def suma(numero1, numero2):
	return numero1 + numero2

def division(numero1, numero2):
	if numero2 != 0:
		return numero1 / numero2
	return 'No se puede dividir por 0.'

def multiplicacion(numero1, numero2):
	return numero1 * numero2

def resta(numero1, numero2):
    return numero1 - numero2

def solicitar_numero(mensaje):
    while True:
      valor = input(mensaje)
      try:
        return int(valor) 
      except ValueError:
        print("Entrada inválida. Por favor, ingrese un número.")

numero1, numero2 = solicitar_numero('Ingrese numero 1: '), solicitar_numero('Ingrese numero 2: ')
print(suma(numero1, numero2))
print(resta(numero1, numero2))
print('%.2f' % division(numero1, numero2))
print(multiplicacion(numero1, numero2))
