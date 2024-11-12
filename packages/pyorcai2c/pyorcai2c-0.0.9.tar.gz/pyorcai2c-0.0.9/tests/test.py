import os, sys
import unittest
import random
import copy
import itertools
import shutil
import json

cwd = os.getcwd()
sys.path.insert(0, f'{cwd}')
from pyorcai2c import ftdi
import pyorcai2c.utils as u

unittest.TestLoader.sortTestMethodsUsing = None

# you need to know the serial number of the FTDI board you are using and provide it to the module
# import ftd2xx
# available_devices = ftd2xx.createDeviceInfoList()
# available_devices = ftd2xx.listDevices()
FTDI_SERIAL_NUMBER = b'DD290424A'
i2c = ftdi(FTDI_SERIAL_NUMBER)
slave = None
regmap = None

def build_random_target(regmap):
    nreg = 130
    i = 0
    target = []
    registers = list(regmap.keys())
    registers_pool = copy.copy(registers)
    fields_pool = copy.copy(registers)
    ints_pool = list(range(0,256))
    while i < nreg:
        choice = random.randrange(0,10)
        if choice in range(0, 5):
            register = random.choice(registers_pool)
            registers_pool.remove(register)
            target.append(register)
            address = regmap[register]['address']
            ints_pool.remove(address)
            i += 1
        elif choice == 5:
            field = random.choice(fields_pool)
            fields_pool.remove(field)
            target.append(field)
        else:
            address = random.choice(ints_pool)
            ints_pool.remove(address)
            target.append(address)
            i += 1
            register = u.find(lambda r: r[1]['address'] == address, regmap.items())
            if register:
                registers_pool.remove(register[0])
    target = list(set(target))
    return target

def calculate_i2c_rw_expectations(regmap, target):
    registers = list(regmap.keys())
    fields = list(map(lambda r: r[1]['fields'].keys(), regmap.items()))
    int_target = []
    for t in filter(lambda r: not isinstance(r, int), target):
        if (t in registers):
            int_target.append(regmap[t]['address'])
        elif (t in fields):
            address = u.find(lambda r: t in r[1][fields].keys(), regmap.items())
            int_target.append(address)
    int_target = list(set(int_target + list(filter(lambda r: isinstance(r, int), target))))
    int_target.sort()
    chunks = list([list(map(lambda a: a[1], g)) for _, g in itertools.groupby(enumerate(int_target), lambda i: i[1] - i[0])])
    info = dict(map(lambda c: (c[0], len(c)), chunks))
    return info

class TestGenericI2cComms(unittest.TestCase):

    def test_00_i2c_bus_scan(self):
        global slave
        scanned = []
        for i in range(0,256,2):
            scanned += [i2c.write(slave=i)]
        acked = u.findIndex(lambda r: r.acks['slave'], scanned)
        self.assertEqual(len(scanned), 256/2)
        self.assertTrue(acked or acked == 0)
        slave = acked*2

    def test_01_i2c_command(self): 
        res = i2c.write(slave=slave, target=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])

    def test_02_i2c_write(self):
        res = i2c.write(slave=slave, target=0x00, data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])
        res = i2c.write(slave=slave, target=random.choice(range(256)), data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])

    def test_03_i2c_burst_write(self):
        register = random.choice(range(256))
        data = list(map(lambda x: random.randrange(0, 256), list(range(register, random.randrange(register, 256)))))
        res = i2c.write(slave=slave, target=register, data=data)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        for i in range(len(data)):
            self.assertTrue(res.acks[f'data_{i}'])
    
    def test_04_i2c_read(self):
        register = random.choice(range(256))
        res = i2c.read(slave=slave, target=register, n=1)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(list(res.data.keys())[0], register)
        self.assertTrue(isinstance(list(res.data.values())[0], int))
    
    def test_05_i2c_burst_read(self):
        register = random.choice(range(256))
        n = random.randrange(register, 256) - register
        res = i2c.read(slave=slave, target=register, n=n)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), n)
        for i in range(n):
            self.assertEqual(list(res.data.keys())[i], register + i)
            self.assertTrue(isinstance(list(res.data.values())[i], int))

    def test_06_load_register_map(self):
        regmap_filepath = os.path.join(cwd, 'regmaps', 'pmic01.json')
        regmap = i2c.load_register_map(regmap_filepath)
        self.assertTrue(regmap)
        self.assertTrue(i2c.regmap)
        self.assertTrue(isinstance(regmap, dict))
        self.assertTrue(isinstance(i2c.regmap, dict))

    def test_07_i2c_regbased_write(self):
        register = random.choice(list(i2c.regmap.keys()))
        data = random.choice(range(256))
        res = i2c.write(slave=slave, target=register, data=data)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])

    def test_08_i2c_regbased_burst_write(self):
        register = random.choice(list(i2c.regmap.keys()))
        address = i2c.regmap[register]['address']
        data = list(map(lambda x: random.randrange(0, 256), list(range(address, random.randrange(address, 256)))))
        res = i2c.write(slave=slave, target=register, data=data)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        for i in range(len(data)):
            self.assertTrue(res.acks[f'data_{i}'])

    def test_09_i2c_fieldbased_write(self):
        register = random.choice(list(i2c.regmap.keys()))
        field = random.choice(list(i2c.regmap[register]['fields'].keys()))
        res = i2c.write(slave=slave, target=field, data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])

    def test_10_i2c_multi_read(self):
        target = build_random_target(regmap=i2c.regmap)
        res = i2c.read(slave=slave, target=target)
        check_acks = u.every(lambda a: a['slave'] and a['register'] and a['read_slave'], res.acks.values())
        info = calculate_i2c_rw_expectations(regmap=i2c.regmap, target=target)
        self.assertTrue(check_acks)
        self.assertTrue(len(res.acks) == len(info))
        self.assertTrue(list(map(lambda t: str(t), target)).sort() == list(map(lambda d: str(d), res.data.keys())).sort())

    def test_11_i2c_multi_write(self):
        target = dict(map(lambda a: (a, random.randrange(0,256)), build_random_target(regmap=i2c.regmap)))
        res = i2c.write(slave=slave, target=target)
        info = calculate_i2c_rw_expectations(regmap=i2c.regmap, target=target)
        self.assertTrue(len(res.acks) == len(info))
        for a in res.acks.items():
            local_acks = a[1]
            expected_acks = {'slave': True, 'register': True} | dict(map(lambda d: (f'data_{d}', True), range(info[a[0]])))
            self.assertTrue(len(a[1]) == (info[a[0]] + 2))
            self.assertTrue(local_acks == expected_acks)

    def test_12_i2c_regbased_read(self):
        register = random.choice(list(i2c.regmap.keys()))
        res = i2c.read(slave=slave, target=register)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), 2)
        self.assertTrue(True if register in list(res.data.keys()) else False)
        self.assertTrue(True if i2c.regmap[register]['address'] in list(res.data.keys()) else False)
        self.assertTrue(isinstance(list(res.data.values())[0], int))

    def test_13_i2c_fieldbased_read(self):
        register = random.choice(list(i2c.regmap.keys()))
        field = random.choice(list(i2c.regmap[register]['fields'].keys()))
        res = i2c.read(slave=slave, target=field)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(list(res.data.keys())[0], field)
        self.assertTrue(isinstance(list(res.data.values())[0], int))

    def test_14_create_destroy_recreate_dummy_memory(self):
        global i2c
        i2c.destroy_dummy_memory()
        i2c.close()
        i2c = ftdi(FTDI_SERIAL_NUMBER, dryrun_mode=True)
        self.assertTrue(os.path.isfile(i2c._dummy_part_memory))
        i2c.destroy_dummy_memory()
        self.assertTrue(not os.path.isfile(i2c._dummy_part_memory))
        dummy_memory_folder = os.path.join(cwd, 'tests_output')
        new_dummy_memory_path = os.path.join(dummy_memory_folder, 'test_dummy_memory.json')
        if os.path.exists(dummy_memory_folder):
            shutil.rmtree(dummy_memory_folder)
        i2c.create_dummy_memory(new_dummy_memory_path)
        self.assertTrue(os.path.isfile(new_dummy_memory_path))
        i2c.destroy_dummy_memory()
        self.assertTrue(not os.path.isfile(i2c._dummy_part_memory))
        i2c.set_dryrun_mode(True)
        expected_dummy_memory_path = os.path.join(os.getcwd(), 'regmaps', f'dummy_part_memory.json')
        self.assertTrue(os.path.isfile(expected_dummy_memory_path))
    
    def test_15_fillout_dummy_memory(self):
        res = i2c.fillout_dummy_memory(slave=slave)
        self.assertTrue(u.every(lambda c: u.every(lambda a: a, c.values()), res.acks.values()))        
        with open(i2c._dummy_part_memory , 'r') as openfile:
            memory_dictionary = json.load(openfile)
        self.assertTrue(len(memory_dictionary[f'{slave}']) == 256)    

    def test_16_i2c_multi_write_dryrun(self):
        regmap_filepath = os.path.join(cwd, 'regmaps', 'pmic01.json')
        i2c.load_register_map(regmap_filepath)
        target = dict(map(lambda a: (a, random.randrange(0,256)), build_random_target(regmap=i2c.regmap)))
        i2c.set_dryrun_mode(True)
        res = i2c.write(slave=slave, target=target)
        info = calculate_i2c_rw_expectations(regmap=i2c.regmap, target=target)
        self.assertTrue(len(res.acks) == len(info))
        for a in res.acks.items():
            local_acks = a[1]
            expected_acks = {'slave': True, 'register': True} | dict(map(lambda d: (f'data_{d}', True), range(info[a[0]])))
            self.assertTrue(len(a[1]) == (info[a[0]] + 2))
            self.assertTrue(local_acks == expected_acks)

    def test_17_i2c_multi_read_dryrun(self):
        target = build_random_target(regmap=i2c.regmap)
        i2c.set_dryrun_mode(True)
        res = i2c.read(slave=slave, target=target)
        check_acks = u.every(lambda a: a['slave'] and a['register'] and a['read_slave'], res.acks.values())
        info = calculate_i2c_rw_expectations(regmap=i2c.regmap, target=target)
        self.assertTrue(check_acks)
        self.assertTrue(len(res.acks) == len(info))
        self.assertTrue(list(map(lambda t: str(t), target)).sort() == list(map(lambda d: str(d), res.data.keys())).sort())
    
if __name__ == '__main__':
    unittest.main()