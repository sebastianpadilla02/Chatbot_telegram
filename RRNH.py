from sympy.parsing.sympy_parser import parse_expr
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from sympy import latex
from decimal import Decimal, ROUND_DOWN

# Función para aproximar cada elemento de una lista a un cierto número de decimales
def approx_list(lst, precision):
    return [np.round(x, precision) for x in lst]


# Función para contar las repeticiones de cada elemento en una lista
def count_elements(lst):
    counter = {}
    for element in lst:
        if element not in counter:
            counter[element] = 1
        else:
            counter[element] += 1
    return counter


def evaluate_(expr, init):
  lst = []
  for i in range(len(init)):
    lst.append(expr.subs(n, i))
  return lst

#Función para recorrer la lista de coeficientes y modelar las funciones
def coefic(k,R,dec_g):
  coeff.reverse()
  for i in range(len(coeff)):
    llenado(coeff[i],R,i,dec_g)

  # Agregar el término constante
  coeff.reverse()
  coeff.append(1)

#Función para almacenar los términos de las funciones Homogenea y  Particular en listas.
def llenado(c,R,i,dec_g):
  if c != 0:
    h = f'{str(-c)}*f(n-{i+1})'
    funcion.append(h)
    if dec_g ==1:
      p = f'{str(-c)}*c'
      funcion_p.append(p)
    elif dec_g ==2:
      p = f'{str(-c)}*(A*(n-{i+1})+B)'
      funcion_p.append(p)
    elif dec_g == 3:
      p = f'{str(-c)}*(A*(n-{i+1})**2+B*(n-{i+1})+C)'
      funcion_p.append(p)
    elif dec_g == 4:
      p= f'{str(-c)}*c*{R}**(n-{i+1})'
      funcion_p.append(p)

#Función para modelar la función homogenea y guardarla en imagen.
def homogenea(g):
  global funcion
  #Concatenacion de la funcion homogenea:
  fun = ""
  for i in funcion:
      fun = fun + i + " + "

  #Acomodar la función que se usará y para imprimir.
  fun = fun[:-3]  # Elimina el último " + " que sobra
  func = parse_expr(fun)
  function = fun +" + "+ str(g)
  function = parse_expr(function)

  # Ajustar el tamaño de la figura según la longitud de la expresión
  longitud_expresion = len(latex(function))
  ancho_figura = longitud_expresion * 0.1
  alto_figura = 1.5

  # Crear una figura con el tamaño ajustado
  fig = plt.figure(figsize=(ancho_figura, alto_figura))

  # Agregar un texto con la función en modo LaTeX a la figura
  plt.text(0.5, 0.5, "$f(n) = " + latex(function) + "$", fontsize=16, ha='center')

  # Ocultar los ejes de la figura
  plt.axis('off')

  # Guardar la figura en formato PNG
  plt.savefig('function.png', dpi=300)

  return function

#Función para modelar la función particular y guardarla en imagen.
def particular(g,dec_g):
  #Acomodar la función que se usará para resolver la parte particular.
  fun_p=""

  for i in funcion_p:
    fun_p = fun_p + i + " + "

  fun_p = fun_p + str(g)
  par = parse_expr(fun_p)
  return par

#Función para resolver la parte homogenea en terminos de b_i y guardar la imagen
def exp_homogenea():
  coeff.reverse()
  roots = np.roots(coeff)
  approx_lst = approx_list(roots, 1)
  approx_lst = list(np.array(approx_lst, dtype = "complex_"))
  multiplicity = count_elements(approx_lst)

  # Obtener los coeficientes b_i
  b = symbols('b0:%d' % k)
  n = symbols('n')

  # Obtener la expresión de la función en términos de las raíces y sus multiplicidades
  expr = 0
  idx = 0
  ecuations = []

  for root in set(approx_lst):
      m = multiplicity.get(np.round(root, 1))
      if m == 1:
          if(root == 0):
            expr += (b[idx])
          else:
            expr += (b[idx] * root**n)
          idx += 1
          ecuations.append(expr)
      else:
          poly = b[idx:idx+m][::-1]
          poly_expr = poly[0]
          for i in range(1, m):
              poly_expr += (poly[i] * n**i)
          idx += m
          if root == 0:
            ecuations.append(poly_expr)
          else:
            ecuations.append(poly_expr * root**n)
          expr += (poly_expr * root**n)

  # Ajustar el tamaño de la figura según la longitud de la expresión
  longitud_expresion = len(latex(expr))
  ancho_figura = longitud_expresion * 0.1
  alto_figura = 1.5

  # Crear una figura con el tamaño ajustado
  fig = plt.figure(figsize=(ancho_figura, alto_figura))

  # Agregar un texto con la función en modo LaTeX a la figura
  plt.text(0.5, 0.5, "$f_{h}(n) = " + latex(expr) + "$", fontsize=16, ha='center')

  # Ocultar los ejes de la figura
  plt.axis('off')

  # Guardar la figura en formato PNG
  plt.savefig('sol_h.png', dpi=300, bbox_inches='tight')

  return expr

#Función para resolver la parte particular y guardar la imagen, además devuelve la función en general(particular + homogenea)
def exp_particular(dec_g,expr, par):
  #Esto se supone que es la forma de resolver la parte particular.
  if dec_g ==1:
    c = symbols('c')
    equation = Eq(c,par)
    solution = solve(equation, c)
    sol_p = solution[0]
    expr = str(expr) + "+" +str(sol_p)
    expr = parse_expr(expr)
  elif dec_g == 2:
    A, B = symbols('A B')
    equation = Eq(A*n+B,par)
    solution = solve(equation, (A,B))
    value_of_A = solution[A]
    value_of_B = solution[B]
    sol_p = f'{str(value_of_A)}*n+{str(value_of_B)}'
    sol_p = parse_expr(sol_p)
    expr = str(expr) + "+" +str(sol_p)
    expr = parse_expr(expr)
  elif dec_g == 3:
    A, B, C = symbols('A B C')
    equation = Eq(A*n**2+B*n+C,par)
    solution = solve(equation, (A,B,C))
    sol_p = f'{str(solution[A])}*n**2+{str(solution[B])}*n+{str(solution[C])}'
    sol_p = parse_expr(sol_p)
    expr = str(expr) + "+" +str(sol_p)
    expr = parse_expr(expr)
  elif dec_g == 4:
    c = symbols('c')
    cons = f'c*({R}**n)'
    cons = parse_expr(cons)
    equation = Eq(cons,par)
    solution = solve(equation, c)
    sol_p = f'({R}**n)*({solution[0]})'
    expr = str(expr) + "+" +str(sol_p)
    expr = parse_expr(expr)
    
  if dec_g !=4:
    # Ajustar el tamaño de la figura según la longitud de la expresión
    longitud_expresion = len(latex(sol_p))
    ancho_figura = longitud_expresion * 0.1
    alto_figura = 1.5

    # Crear una figura con el tamaño ajustado
    fig = plt.figure(figsize=(ancho_figura, alto_figura))
    # Agregar un texto con la función en modo LaTeX a la figura
    plt.text(0.5, 0.5, "$f_{p}(n) = " + latex(sol_p) + "$", fontsize=16, ha='center')

    # Ocultar los ejes de la figura
    plt.axis('off')

    # Guardar la figura en formato PNG
    plt.savefig('sol_p.png', dpi=300, bbox_inches='tight')
  return expr

#Genera la imagen de la función en general.
def print_expr(expr):
  # Ajustar el tamaño de la figura según la longitud de la expresión
  longitud_expresion = len(latex(expr))
  ancho_figura = longitud_expresion * 0.15
  alto_figura = 1.5

  # Crear una figura con el tamaño ajustado
  fig = plt.figure(figsize=(ancho_figura, alto_figura))

  # Agregar un texto con la función en modo LaTeX a la figura
  plt.text(0.5, 0.5, "$f(n) = " + latex(expr) + "$", fontsize=16, ha='center')

  # Ocultar los ejes de la figura
  plt.axis('off')

  # Guardar la figura en formato PNG
  plt.savefig('expr.png', dpi=300, bbox_inches='tight')

#Función que resuelve la ecuacion general, encontrando las b_i y luego genera la imagen de la función final ya resuelta.
def solution(expr,init):
  #Ultima resolución para poder tener la no recurrente.
  ec = evaluate_(expr, init)
  # Crear una lista con las ecuaciones resultantes de igualar cada elemento de ec con su respectiva condición inicial
  eqs = [ec[i] - init[i] for i in range(len(init))]
  # Resolver el sistema de ecuaciones
  b = symbols('b0:%d' % k)
  sol = solve(eqs, b)
  
  for key, value in sol.items():
    val=str(value)
    if "I" in val:
      if "+" in val:
        va_str = val.split(' + ')
        va_str[1] = va_str[1].replace('*I','')
        va_str[0]= Decimal(va_str[0]).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        va_str[1]= Decimal(va_str[1]).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        va_str[1] = str(va_str[1]) + '*I'
        sol[key] = str(va_str[0]) + '+' + str(va_str[1])
      elif "-" in val:
        va_str = val.split(' - ') 
        va_str[1] = va_str[1].replace('*I','')
        va_str[0]= Decimal(va_str[0]).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        va_str[1]= Decimal(va_str[1]).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        va_str[1] = str(va_str[1]) + '*I'
        sol[key] = str(va_str[0]) + '+' + str(va_str[1])
    else:
      sol[key] = Decimal(str(value)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

  # Imprimir la solución
  ec_sol = expr.subs(sol)
  # Ajustar el tamaño de la figura según la longitud de la expresión
  longitud_expresion = len(latex(ec_sol))
  ancho_figura = longitud_expresion * 0.1
  alto_figura = 1.5

  # Crear una figura con el tamaño ajustado
  fig = plt.figure(figsize=(ancho_figura, alto_figura))

  # Agregar un texto con la función en modo LaTeX a la figura
  plt.text(0.5, 0.5, "$f(n) = " + latex(ec_sol) + "$", fontsize=16, ha='center')

  # Ocultar los ejes de la figura
  plt.axis('off')

  # Guardar la figura en formato PNG
  plt.savefig('ec_sol.png', dpi=300, bbox_inches='tight') 


#Listas necesarias
coeff = []
n = symbols('n')
funcion = []
funcion_p=[]
init = []
dec_g = 0
k = 0
g = 0
R = 0

#Función que es llamada en el bot y que llama las demas funciones.
def principal_rrnh():
  global coeff, n, funcion, funcion_p, init, dec_g, k, g, R
  coefic(k,R, dec_g)
  function = homogenea(g)   
  par = particular(g,dec_g)  
  expr = exp_homogenea()  
  expr = exp_particular(dec_g,expr,par)  
  print_expr(expr)
  solution(expr,init)  