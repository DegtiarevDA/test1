import math
import control.matlab as cmatlab
import control
import matplotlib.pyplot as pyplot
import sys
import sympy
from numpy import arange

## Создание структурной схемы САУ частоты вращения турбины

# Обратная связь (Апериодическая гибкая W = kp/(Tp+1))
# k=0.2 T=1..5
k1 = 10.9
T1 = 4
W1 = cmatlab.tf([k1, 0],[T1, 1])
# Генератор (W = 1 / (Tp+1)) T = 10
T2 = 10
W2 = cmatlab.tf([1],[T2, 1])
# Турбина (Гидро- W = (0.01T_1 * p+1) / (0.05T_2 * p+1))
# T_1=1 T_2=10
T3_1 = 1
T3_2 = 10
W3 = cmatlab.tf([0.01 * T3_1, 1],[0.05 * T3_2, 1])
# Усил-испол орган (W = k / (Tp+1)) k=24 T=4
k4 = 24
T4 = 4
W4 = cmatlab.tf([k4],[T4, 1])
# Сборка модели
CAY = cmatlab.feedback(W4 * W3 * W2, W1, -1)

## 1. Снятие переходной характеристики
h = cmatlab.step(CAY)
# Построение графика
pyplot.figure(1)
pyplot.grid(True)
title = 'Переходная хар-ка. '
[y, x] = h
pyplot.plot(x, y, "purple")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

## 2. Значения полюсов передаточной ф-ии замкнутой САУ
pole = cmatlab.pole(CAY)
print("Полюса:")
for polus in pole:
    print(polus)
    #print("type(polus.item())", type(polus.item()))
    #print("type(polus)", type(polus))

# Заключение об устойчивости САУ
zakluchenie = "САУ устойчива"
for polus in pole:
    if polus.item().real > 0:
        zakluchenie = "САУ неустойчива"
        break # выход из цикла
    elif polus.item().real == 0:
        zakluchenie = "САУ на границе устойчивости"
print (zakluchenie)

## 3. Разомкнутая САУ и устойчивость по критерию Найквиста
# Разомкнутая САУ
razCAY = W4 * W3 * W2
# критерий НАйквиста
pyplot.figure(2)
pyplot.grid(True)
cmatlab.nyquist(razCAY)
pyplot.title("критерий Найквиста") 
# устойчивая, если годограф не охватывает (-1, 0*j)

## 4. Снять ЛАЧХ и ЛФЧХ разомкнутой системы
pyplot.figure(3)
pyplot.grid(True)
cmatlab.bode(razCAY)
pyplot.suptitle("ЛАЧХ и ЛФЧХ разомкнутой системы", fontsize=14)
## 5. Оценить запасы
## 6. годограф Стаса
print("\nПередаточная функция САУ")
print(CAY)

omega, k =sympy.symbols('w k', real=True)
j = sympy.I
z = ( 80*(omega*j)**4+208*(omega*j)**3
      +107.6*(omega*j)**2+277.8*(omega*j)+1 )
print("Характеристический многочлен замкнутой системы:\n", z)
zr=sympy.re(z)
zm=sympy.im(z)
print("Действительная часть:\n", zr)
print("Мнимая часть:\n", zm)
x=[zr.subs({omega:w}) for w in arange(0,10,0.01)]
y=[zm.subs({omega:w}) for w in arange(0,10,0.01)]
pyplot.figure(4)
pyplot.title("критерий Михайлова")
pyplot.grid(True)
scale = 1000.0
pyplot.axis([-scale, scale, -scale, scale])
pyplot.plot(x, y)

## 7. критерий Рауса-Гурвица
import numpy.linalg as linalg
a2 = [[208, 280.1],
      [80,  107.6]]

a3 = [[208, 280.1,     0],
      [80 , 107.6,     1],
      [0  , 208  , 280.1]]

a4 = [[208, 280.1,     0,  0],
      [80 , 107.6,     1,  0],
      [0  , 208  , 280.1,  0],
      [0  , 80   , 107.6,  1]]
det2 = linalg.det(a2)
det3 = linalg.det(a3)
det4 = linalg.det(a4)
print("Главные миноры:\n", 208, det2, det3, det4)
print("a0 по Гурвицу = 80")

## Поиск предельной устойчивости
##print("\nПередаточная функция razСАУ")
##print(razCAY)
##
##W_razCAY = (0.24*(omega)+24)/(
##    20*(omega)**3+47*(omega)**2+14.5*(omega)+1)
##W_os = 0.2 * (omega) / (4*(omega) + 1)
##z2 = W_razCAY / (1 + W_os* W_razCAY)
##print("z2", z2)
##print("factor(z2)", sympy.factor(z2))
k1 = -0.688
k2 = 10.804
print("k предельный = ", k2)

## Показать графики
pyplot.show()
