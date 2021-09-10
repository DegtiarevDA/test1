import math
import mpmath 
import control.matlab as cmatlab
import control
import matplotlib.pyplot as pyplot
import sys
import sympy
from numpy import arange
import pylab
import matplotlib.path
import scipy as sp
import numpy as np


mpmath.mp.dps = 15
mpmath.mp.pretty = True
## Создание структурной схемы САУ частоты вращения турбины

def step_info(t, yout): # for step responce
    global OS, RTime, x_STime, y_STime
    OS = (yout.max() / yout[-1] - 1) * 100
    RTime = (t[next(i for i in range(0, len(yout) - 1) if yout[i] > yout[-1] * .90)] - t[0])
    STimeMax = t[next(len(yout) - i for i in range(2, len(yout) - 1) if abs(yout[-i] / yout[-1]) > 1.05)] - t[0]
    STimeMin = t[next(len(yout) - i for i in range(2, len(yout) - 1) if abs(yout[-i] / yout[-1]) < 0.95)] - t[0]
    if STimeMax>STimeMin:
        x_STime=STimeMax
    else:
        x_STime=STimeMin
    for i in range(0,len(t)):
        if t[i] == x_STime:
            n=i
            break
    y_STime=yout[n]
'''
def ach_info(t, yout,a):     #for bode
    global ACH_x,ACH_y
    n=0
    ACH_x = t[next(len(yout) - i for i in range(2, len(yout) - 1) \
                   if abs(yout[-i] / yout[0]) > 1)] - t[0]
    for i in range(0,len(t)):
        if t[i] == ACH_x:
            print("777777")
            n=i
            break
    ACH_y=yout[n]
'''
Timeline = []
for i in range (0, 100000):
        Timeline.append(i/10000)
# Обратная связь
Wobr = cmatlab.tf([1],[1])

# Генератор (W = 1 / (Tp+1)) T = 10
T1 = 10
W1 = cmatlab.tf([1],[T1, 1])
# Турбина (Гидро- W = (0.01T_1 * p+1) / (0.05T_2 * p+1))
# T_1=1 T_2=10
T2_1 = 1
T2_2 = 10
W2 = cmatlab.tf([0.01 * T2_1, 1],[0.05 * T2_2, 1])
# Усил-испол орган (W = k / (Tp+1)) k=24 T=4
k3 = 24
T3 = 4
W3 = cmatlab.tf([k3],[T3, 1])
# regulato
k4 = 0.17
W4 = cmatlab.tf([k4],[1])
k51 = 0.5
k52 = 0.03
k53 = 0.5
T53 = 0.3
W51 = cmatlab.tf([k51],[1])
W52 = cmatlab.tf([k52],[1, 0])
W53 = cmatlab.tf([k53, 0],[T53,1])
W5 = W51 + W52 + W53
# Сборка модели

CAYbezRegulatora = cmatlab.feedback(W3 * W2 * W1, Wobr, -1)
CAY4 = cmatlab.feedback(W4 * W3 * W2 * W1, Wobr, -1)
CAY5 = cmatlab.feedback(W5 * W3 * W2 * W1, Wobr, -1)

print("САУ без регулятора")
print(CAYbezRegulatora)

#print(W3 * W2 * W1)

print("САУ c П регулятором")
print(CAY4)
print("САУ с ПИД р-ом")
print(CAY5)

from sympy.abc import x
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function

# Wi = Ui/Vi
# W321
U321 = implemented_function('U321', lambda x: \
    (0.24*x+24))
V321 = implemented_function('V321', lambda x: \
    (20*x*x*x+47*x*x+14.5*x+1))

W321 = implemented_function('W321', lambda x: \
    U321(x)/(U321(x) + V321(x)))

# W4321
U4321 = implemented_function('U4321', lambda x: \
    (0.24*x+24)*k4)
V4321 = implemented_function('V4321', lambda x: \
    (20*x*x*x+47*x*x+14.5*x+1))

W4321 = implemented_function('W4321', lambda x: \
    U4321(x)/(U4321(x) + V4321(x)))


lam_W321 = lambdify(x, W321(x))
lam_W4321 = lambdify(x, W4321(x))
t = [0.001, 0.01, .1, 1, 10]

#(0.156 s^3 + 15.72 s^2 + 12.22 s + 0.72)/\
#       (6 s^5 + 34.1 s^4 + 51.51 s^3 + 30.52 s^2 + 13.22 s + 0.72)
#-yust

### Построение графика
pyplot.figure(2)
pyplot.grid(True)
title = 'Переходная хар-ка. П р-р'
t = [i/100 for i in range (20*100)]
y = [lam_W4321(i) for i in t]
[y, t] = cmatlab.step(CAY4)
pyplot.plot(t, y, "purple")
pyplot.title(title) 
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')

# Построение графика
pyplot.figure(3)
pyplot.grid(True)
title = 'Переходная хар-ка. ПИД р-р'
t = [i/100 for i in range (20*100)]
y = [lam_W4321(i) for i in t]
[y, t] = cmatlab.step(CAY5)
pyplot.plot(t, y, "purple")
pyplot.title(title)
pyplot.plot( [0,100],[y[-1]*1.05,y[-1]*1.05], '--')
pyplot.plot( [0,100],[y[-1]*0.95,y[-1]*0.95], '--')

pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время (с)')



###3.Прямые оценки качества

ymax=max(y)
for i in range (0,len(y)):
    if y[i]==ymax:
        break
tmax=t[i]
step_info(t,y)
pyplot.plot([x_STime, x_STime],[0,y[-1]*0.95],'--')
pyplot.plot([0, tmax],[ymax,ymax],'--')
pyplot.plot([tmax, tmax],[0,ymax],'--')
print("Mаксимальное значение")
print(ymax)
yust=y[-1]
print("Установившееся значение")
print(yust)
print("Время регулирования")
print(x_STime)

delta=((ymax-y[-1])/y[-1])*100
print("Перерегулирование")
print(delta,'%')


#pyplot.show()

# Корневой метод
print('-------------корневой метод--------------')

pyplot.figure(4)
pyplot.grid(True)
#title = 'Переходная хар-ка. ПИД р-р'
cmatlab.pzmap(CAY5)
#pyplot.show()
p=cmatlab.pole(CAY5)
p=list(p)           #перевод arrey в list
if sympy.im(max(p))==0:
    p.remove(max(p))
K=max(p)
print('время переходного процесса', 3/sympy.re(K), ' сек')
print('колебательность', abs(sympy.im(K)/sympy.re(K)))
print('степень колебательности',sympy.exp(-3.1415/abs(sympy.im(K)/sympy.re(K))))

#==================================================================
# Частотный метод

pyplot.figure(5)
pyplot.grid(True)
#title = 'Переходная хар-ка. ПИД р-р'
CAY = W5 * W3 * W2 * W1 
print(CAY)
cmatlab.pzmap(CAY)
#pyplot.show()


pyplot.figure(6)
pyplot.grid(True)
#title = 'Переходная хар-ка. ПИД р-р'

j = sympy.I
omega=sympy.symbols('w',real=True)
z=CAY.den
t=1
fden=0
s=[]
for i in z[0]:
    for l in i:
        k=len(i)-t
        fden=fden+l*(j*omega)**k
        t=t+1
        s.append(l)

a=CAY.num
t=1
fnum=0
s1=[]
for i in a[0]:
    for l in i:
        k=len(i)-t
        fnum=fnum+l*(j*omega)**k
        t=t+1
        s1.append(l)
w = fnum/fden
zr=sympy.re(w)
zm=sympy.im(w)

ach=pow(zr**2+zm**2,0.5)
vmin=0.0001
vmax=2.5
dv=0.0005

v_list=np.arange(vmin,vmax,dv)
f_list=[ach.subs({omega:q}) for q in v_list]

pyplot.plot(v_list,f_list)
##pyplot.axis([0,1.5,0,25])
pyplot.title('АЧХ')
pyplot.ylabel('Amplitude')
pyplot.xlabel('Omega')
pyplot.grid(True)


fmax=max(f_list)
imax=0
u0=0
vcp=1
for i in range(0,len(f_list)):
    if f_list[i]==fmax:
        imax=i
        break
f0=f_list[0]
u_list=[(ach-f0).subs({omega:q}) for q in v_list]
for k in range(imax, len(u_list)):
    if (u_list[k-1]>0) and (u_list[k+1]<0):
        u0=u_list[k]
        vcp=v_list[k]
        break
print(u0,"!")
print(fmax)
print(f0)
M=fmax/f0
treg3=1.5*2*math.pi/vcp
print(ach)
#vcp=solve(ach,v)
print(treg3," -время регулирования")
print(M," - показатель колебательности")

#plt.show()

##
##yre=[wre.subs({omega:q}) for q in arange(0.01,10,0.1)]
##yim=[wim.subs({omega:q}) for q in arange(0.01,10,0.1)]
##y=[]
###print(yre[0])
###print(yim[0])
##for i in range(0,len(yre)):
##    y.append(math.sqrt(yre[i]**2+yim[i]**2))
##
##x=[]
##for i in arange(0.01,10,10/len(yre)):
##    x.append(i)


pyplot.figure(7)

mag, phase, omega = cmatlab.bode(CAY,Hz=False,dB=False)
# Переводим амплитуду в дБ из радиан/сек
mag_dB = [20*math.log10(x) for x in mag]
# Переводим частоту в Герцы из радиан/сек
omega_Hz = [x/3.1415/2 for x in omega]
# Переводим фазу в градусы из радиан
phase_deg = [x/3.1415*180 for x in phase]
# Переводим частоту в Герцы из радиан/сек
omega_Hz = [x/3.1415/2 for x in omega]



##pyplot.figure(7)
##pyplot.grid(True)
###pyplot.yscale('log')
##pyplot.xscale('log')
##title = '111111111111111'
##pyplot.plot(omega_Hz, mag_dB, "red")
##
##pyplot.figure(8)
##pyplot.grid(True)
###pyplot.yscale('log')
##pyplot.xscale('log')
##title = '111111111111111' 
##pyplot.plot(omega_Hz, phase_deg, "purple")

#pyplot.show()
#print(y1)

i = 0
for i in range(0,len(mag_dB)):
    if mag_dB[i] < 0:
        break
#print(i," ",mag_dB[i])
omega_Hz_0_i = i
omega_Hz_0 = omega_Hz[omega_Hz_0_i]

for i in range(0,len(phase_deg)):
    if phase_deg[i] < -180:
        break
#print(i," ",phase_deg[i-1])
#print(i," ",phase_deg[i])
omega_Hz_1_i = i
omega_Hz_1 = omega_Hz[omega_Hz_1_i]


#print(omega_Hz_0)
pyplot.figure(7)
pyplot.subplot(2,1,1)
pyplot.grid(True)
pyplot.xscale('log')
# из 0 вниз (частота среза)
pyplot.plot([omega_Hz_0,omega_Hz_0],[0,mag_dB[len(mag_dB)-1]],\
            '--',color='blue')
pyplot.plot([0,omega_Hz_0],[0,0],\
            '--',color='blue')
pyplot.plot([omega_Hz_1,omega_Hz_1],[mag_dB[omega_Hz_1_i],mag_dB[len(mag_dB)-1]],\
            '--',color='purple')
pyplot.plot(omega_Hz, mag_dB)

pyplot.subplot(2,1,2)
pyplot.grid(True)
pyplot.xscale('log')
# из 0 вниз (частота среза)
pyplot.plot([omega_Hz_0,omega_Hz_0],[phase_deg[0],phase_deg[omega_Hz_0_i]],\
            '--',color='blue')
pyplot.plot([omega_Hz_0,omega_Hz_0],[phase_deg[0],phase_deg[omega_Hz_0_i]],\
            '--',color='blue')
pyplot.plot([omega_Hz_1,omega_Hz_1],[phase_deg[0],phase_deg[omega_Hz_1_i]],\
            '--',color='purple')
pyplot.plot([0,omega_Hz_1],[phase_deg[omega_Hz_1_i],phase_deg[omega_Hz_1_i]],\
            '--',color='purple')
pyplot.plot(omega_Hz, phase_deg)


zapas_po_mag = abs(mag_dB[omega_Hz_1_i])
zapas_po_phase = abs(phase_deg[omega_Hz_0_i] + 180)

print("Запас по амплитуде:",zapas_po_mag)
print("Запас по фазе:",zapas_po_phase)

[y, t] = cmatlab.step(CAY5)
integral = 0
for i in range(1,len(t)):
    integral = integral + abs((y[i]+y[i-1])/2 - yust) *(t[i]-t[i-1])
#integral, error = sp.integrate.quad(CAY5,0,100)
print("Интеграл от ошибки:",integral)


pyplot.show()
