# pasir
granular-based simulation and related systems


## install
```batch
pip install pasir
```


## examples
```py
from pasir.butiran.color2 import Color2
from pasir.butiran.math.vect3 import Vect3
from pasir.butiran.grain import Grain
from pasir.butiran.force.gravitational import Gravitational

# define grain with initial position and velocity
grain = Grain(id="0002", m = 1)
grain.r = Vect3(0, 0, 0)
grain.v = Vect3(30, 40, 0)

# define gravitational field and force
g = Vect3(0, -10, 0)
gravitational = Gravitational(field=g)

import numpy as np

# define iteration
tbeg = 0
tend = 8
N = 100
dt = (tend - tbeg) / N

# define lists
data_t = []
data_x = []
data_y = []
data_vx = []
data_vy = []

# perform iteration
#print("#t x y vx vy")
print("Calculate position and velocity.")
for i in range(N + 1):
  t = i
  
  m = grain.m
  v = grain.v
  r = grain.r
  
  data_t.append(t)
  data_x.append(r.x)
  data_y.append(r.y)
  data_vx.append(v.x)
  data_vy.append(v.y)

  fg = gravitational.force(grain)
  a = fg / m
  v += a * dt
  r += v * dt
  
  grain.v = v
  grain.r = r
  
  #print(t, ' ', end='')
  #print(r.x, ' ', r.y, ' ', end='')
  #print(v.x, ' ', v.y)
  
print("Plot data.")
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

figure(figsize=(5,3.5), dpi=80)

plt.plot(data_x, data_y, c='r')
plt.xlabel('x')
plt.ylabel('y')

plt.grid()
plt.xlim([0, 240])
plt.ylim([0, 80])
plt.xticks(np.arange(0, 240+0.01, 40))
plt.yticks(np.arange(0, 80+0.01, 20))

plt.text(60, 39, "$v_x = 30$, $v_y = 40$, $m = 1$", fontsize=12)
plt.text(98, 30, "$g = -10$", fontsize=12)

print("Save figure.")
plt.savefig('parabolic_gravitational_euler.png', bbox_inches='tight')
```