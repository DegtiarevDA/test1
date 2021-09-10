import control.matlab as cmatlab
import control
import matplotlib.pyplot as pyplot
import sys 


## Задание параметров

k1 = 5
k2 = 3
T2 = 2
k3 = 5
k4 = 1
T4 = 0.00001
k5 = 3
T5 = 3
    
inertialessUnit = cmatlab.tf([k1], [1])
aperiodicUnit = cmatlab.tf([k2], [T2, 1])
integratingUnit = cmatlab.tf([k3], [1, 0])
idealDiffUnit = cmatlab.tf([k4, 0], [T4, 1])
RealDiffUnit = cmatlab.tf([k5, 0], [T5, 1])

inertialessUnitModified = cmatlab.tf([2*k1], [1])
aperiodicUnitModified = cmatlab.tf([2*k2], [T2/2, 1])
integratingUnitModified = cmatlab.tf([2*k3], [1, 0])
idealDiffUnitModified = cmatlab.tf([k4*2, 0], [T4/2, 1])
RealDiffUnitModified = cmatlab.tf([2*k5, 0], [T5/2, 1])

inertialessUnitName = 'Безынерционное звено'
aperiodicUnitName = 'Апериодическое звено'
integratingUnitName = 'Интегрирующее звено'
idealDiffUnitName = 'Идеальное дифференцирующее звено'
RealDiffUnitName = 'Реальное дифференцирующее звено'

## Выбор звена

userInput = input('Введите номер команды:\n'
    '1 - ' + inertialessUnitName + ';\n'
    '2 - ' + aperiodicUnitName + ';\n'
    '3 - ' + integratingUnitName + ';\n'
    '4 - ' + idealDiffUnitName + ';\n'
    '5 - ' + RealDiffUnitName + '.\n')

## Установка параметров в соответствии с выбранным звеном
if userInput.isdigit():
    userInput = int(userInput)
    if userInput == 1:
        Unit = inertialessUnit
        UnitModified = inertialessUnitModified
        UnitName = inertialessUnitName
    elif userInput == 2:
        Unit = aperiodicUnit
        UnitModified = aperiodicUnitModified
        UnitName = aperiodicUnitName
    elif userInput == 3:
        Unit = integratingUnit
        UnitModified = integratingUnitModified
        UnitName = integratingUnitName
    elif userInput == 4:
        Unit = idealDiffUnit
        UnitModified = idealDiffUnitModified
        UnitName = idealDiffUnitName
    elif userInput == 5:
        Unit = RealDiffUnit
        UnitModified = RealDiffUnitModified
        UnitName = RealDiffUnitName
    else:
        print ('Недопустимое число')
        sys.exit(0)
else:
    print ('Недопустимое значение')
    sys.exit(0)
        
ModifiedName = 'k*2, T*2'
Name = 'k, T'

###Временная шкала для графика 1
timeInSeconds = 3
Timeline = []
for i in range (0, 3000):
    Timeline.append(i / 1000)

## График 1 (Переходная и импульсная характеристики)
pyplot.figure(1, figsize = [7,6])
# общий заголовок
pyplot.suptitle(UnitName, fontsize=14)
# расстояние между графиками
pyplot.subplots_adjust(hspace = 0.5, wspace = 0.3)

pyplot.subplot(2,2,1)
pyplot.grid(True)
title = 'Переходная хар-ка. '
[y, x] = cmatlab.step(Unit,Timeline)
pyplot.plot(x, y, "purple")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

pyplot.subplot(2,2,2)
pyplot.grid(True)
title = 'Импульсная хар-ка. '
[y, x] = cmatlab.impulse(Unit,Timeline)
pyplot.plot(x, y, "green")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

pyplot.subplot(2,2,3)
pyplot.grid(True)
title = 'Переходная хар-ка. ' + ModifiedName
[y, x] = cmatlab.step(UnitModified,Timeline)
pyplot.plot(x, y, "blue")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

pyplot.subplot(2,2,4)
pyplot.grid(True)
title = 'Импульсная хар-ка. ' + ModifiedName
[y, x] = cmatlab.impulse(UnitModified,Timeline)
pyplot.plot(x, y, "lime")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

## График 2 (АЧХ и ФЧХ)
pyplot.figure(2, figsize = [7,6])
mag, phase, omega = control.bode([Unit, UnitModified])
pyplot.suptitle(UnitName, fontsize=14)
pyplot.legend([Name, ModifiedName])
## Показать графики
pyplot.show()


