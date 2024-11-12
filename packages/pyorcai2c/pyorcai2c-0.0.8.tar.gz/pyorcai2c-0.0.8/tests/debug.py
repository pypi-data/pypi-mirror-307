import os, sys

cwd = os.getcwd()
sys.path.insert(0, f'{cwd}')
from pyorcai2c.pyorcai2c import ftdi
import pyorcai2c.utils as u
import random

i2c = ftdi(b'DD290424A')
slave = 0x02
regmap_filepath = os.path.join(cwd, 'regmaps', 'pmic01.json')
regmap = i2c.load_register_map(regmap_filepath)

# res = i2c.write(slave=slave, target=0, data=[0xff, 0xff])


register = random.choice(list(i2c.regmap.keys()))
res = i2c.read(slave=slave, target=register)
print(res)


register = random.choice(list(i2c.regmap.keys()))
field = random.choice(list(i2c.regmap[register]['fields'].keys()))
res = i2c.read(slave=slave, target=field)
print(res)