from enum import Enum
import ftd2xx
import time
import json
import itertools
from pyorcai2c.utils import find, every

MILLISECOND = 0.001

I2C_CLOCK_DIVISOR = 29
BUFFON_SCLH_SDAH = [0x80, 0xC3, 0xC3]
BUFFON_SCLH_SDAL = [0x80, 0xC1, 0xC3]
BUFFON_SCLL_SDAL = [0x80, 0xC0, 0xC3]
BUFFON_SCLL_SDAH = [0x80, 0xC2, 0xC3]
BUFOFF_SCLL_SDAL = [0x80, 0x00, 0xC0]
BUFOFF_SCLH_SDAH = [0x80, 0x03, 0xC0]
SCLL_SDAHIZ = [0x80, 0x80, 0xC1]
CLOCK_ONLY = [0x8E, 0x00]
CLOCK8 = [0x20, 0x00, 0x00]
START_BIT = BUFFON_SCLH_SDAH+BUFFON_SCLH_SDAL+BUFFON_SCLL_SDAL
STOP_BIT = BUFFON_SCLL_SDAL+BUFFON_SCLH_SDAL+BUFFON_SCLH_SDAH+BUFOFF_SCLH_SDAH

class i2c_response_attribute(Enum):
    ACKS = 'acks'
    DATA = 'data'

class regmap_info:
    def __init__(self, register_names, fields_names):
            self.register_names = register_names
            self.fields_names = fields_names
class i2c_response:
    def __init__(self, acks=None, data=None):
        self.acks = acks if acks else dict()
        self.data = data if data else dict()
    
    def __repr__(self):
        return f'acks = {self.acks}\ndata = {self.data}'
    
    def __str__(self):
        return self.__repr__()

    def flatten(self, attribute = None):
        if(attribute):
            if not isinstance(filter, i2c_response_attribute):
                raise TypeError(f'filter must be an instance of i2c_response_filter Enum\npossible alternatives are {list(map(lambda a: a.value, i2c_response_attribute))}')
            else:
                return getattr(self, attribute.value).values()
        else:
            dictionaries = list(filter(lambda a: isinstance(getattr(self, a), dict), dir(self))) 
            return map(lambda d: d.values(), dictionaries)

class modify_read_operand:
    def __init__(self, field_data, field_offset, field_size):
        self.field_data = field_data
        self.field_offset = field_offset
        self.field_size = field_size

class ftdi:
    def __init__(self, serial_number, clock_divisor = I2C_CLOCK_DIVISOR):
        self.com = ftd2xx.openEx(serial_number)
        # MPSSE enable
        self.com.setBitMode(0, 2) #Set bit mode = MPSSE
        time.sleep(10*MILLISECOND)
        # Clock divisor setting
        byte_high = clock_divisor // 256
        byte_low = clock_divisor % 256
        self._write([0x86, byte_low, byte_high])    
        # Init SDA and SCL pins
        # for the SDA, SCL buffered board you need to setup SDA and SCL before turning on the buffers to avoid glitches
        self._write([0x80, 0x03, 0xFB])
        self._write([0x80, 0xC3, 0xFB])
        #Disable Clock Divide by 5
        self._write([0x8A])
        #Enable Three Phase Clock
        self._write([0x8C])

    def close(self):
        self.com.close()

    def _write(self, data):
        s = bytes(data)
        return(self.com.write(s))

    def _read(self, nbytes):
        s = self.com.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)
    
    def _build_send_byte(self, data):
        prefix = [0x11, 0x00, 0x00]
        read_ack = [0x22, 0x00]
        drive_sda_anaing_with_scl_Low = [0x80, 0xC2, 0xC3]
        byte_array = prefix + [data] + SCLL_SDAHIZ + read_ack + drive_sda_anaing_with_scl_Low
        return(byte_array)   

    def _build_read_byte(self, n):   
        byte_array = []
        for i in range (n):
            if  i + 1 == n:           
                byte_array += SCLL_SDAHIZ + CLOCK8 + CLOCK_ONLY + STOP_BIT
            else:           
                byte_array += SCLL_SDAHIZ + CLOCK8+ BUFFON_SCLL_SDAL + CLOCK_ONLY
        return(byte_array)
    
    def _evaluate_ack(self, a):
        return (a % 2) == 0

    def _i2c_write(self, slave:int, register:int=None, data:int|list=None):
        byte_array = START_BIT + self._build_send_byte(slave) 
        if register or register == 0:
             byte_array += self._build_send_byte(register)
        if isinstance(data, list):
            n = len(data)
            for i in range(n):
                byte_array += self._build_send_byte(data[i])
        elif isinstance(data, int):
                byte_array += self._build_send_byte(data)
                n = 1
        else:
            n = 0
        byte_array += STOP_BIT
        self._write(byte_array)
        n_acks = 1 + (1 if register or register == 0 else 0) + n
        acks = self._read(n_acks)
        res = i2c_response()
        for i, a in enumerate(acks):
            ack = self._evaluate_ack(a)
            if i == 0:
                res.acks['slave'] = ack
            elif i == 1:
                res.acks['register'] = ack
            else:
                res.acks[f'data_{i-2}'] = ack
        return(res)

    def _i2c_read(self, slave:int, register:int, n:int):
        read_slave = slave + 1 if slave % 2 == 0 else slave
        byte_array = START_BIT + self._build_send_byte(slave) + self._build_send_byte(register) + START_BIT + self._build_send_byte(read_slave)
        byte_array += self._build_read_byte(n)
        self._write(byte_array)
        data = self._read(3 + n)
        res = i2c_response()
        for i, a in enumerate(data):
            ack = self._evaluate_ack(a)
            if i == 0:
                res.acks['slave'] = ack
            elif i == 1:
                res.acks['register'] = ack
            elif i == 2:
                res.acks[f'read_slave'] = ack
            else:
                res.data[register + i - 3] = data[i]
        return res
    
    def _retrieve_regmap_info(self):
        if(self.regmap):
            register_names = [r for r in self.regmap.keys()]
            fields_names = [f for fields in map(lambda r: r[1]['fields'].keys() , self.regmap.items()) for f in fields]
            return regmap_info(register_names=register_names, fields_names=fields_names)
        else:
            raise Exception('Error: register map is not loaded')

    
    def _generate_field_mask(self, offset, size):
        mask =''.join(map(lambda i: '1' if (i < 8 - offset) and (i > 8 - offset - size) else '0', range(8)))
        return int(f'0b{mask}', 2)
    
    def _find_register_from_field(self, field):
        register = find(lambda r: field in r['fields'].keys()  , self.regmap.values())
        return register

    def _modify_read_data(self, read_data, operand:list|modify_read_operand):
        if isinstance(operand, list) and len(operand) > 0:
            o = operand.pop()
        else:
            o = operand
        if(not (isinstance(o, modify_read_operand) or len(operand) == 0)):
            raise Exception('Error: modify_read_operand has not been setup properly')
        binaryData = bin(o.field_data)
        slicedData = binaryData[2: o.field_size + 2]
        shiftedData = int(slicedData, 2) << o.field_offset
        mask = self._generate_field_mask(offset=o.field_offset, size=o.field_size)
        fieldData = mask & shiftedData
        old_data = read_data if (isinstance(operand, modify_read_operand) or (isinstance(operand, list) and len(operand) == 0)) else self._modify_read_data(read_data, operand)
        registerData = (~mask & old_data)
        newData = fieldData + registerData
        return(newData)

    def _i2c_write_field(self, slave, field, data):
        if(not isinstance(data, int)):
            raise TypeError("data agument of _i2c_write_field must be an integer NUMBER")
        register = self._find_register_from_field(field)
        address = register['address']
        if(register['fields'][field]['size'] < 8):
            read = self._i2c_read(slave=slave, register=address, n=1)
            if every(lambda a: a, read.acks):
                modify_request = modify_read_operand(data, register['fields'][field]['offset'], register['fields'][field]['size'])
                newData = self._modify_read_data(read_data=read.data[address], operand = modify_request)
                res = self._i2c_write(slave=slave, register=address, data=newData)
            else:
                raise Exception("Internal Error: NACK on _i2c_read of READ-MODIFY_WRITE operation during an _i2c_write_field")
        else:
            res = self._i2c_write(slave=slave, register=address, data=data)
        return res
    
    def _get_field_data_from_register_data(self, data, size, offset):
        mask = self._generate_field_mask(offset, size)
        fieldData = mask & data
        zero_based_data = fieldData >> offset
        return zero_based_data
    
    def _get_register_from_address(self, address):
        register = find(lambda r: r[1]['address'] == address, self.regmap.items())
        return register
        
    
    def _i2c_read_field(self, slave, field):
        register = self._find_register_from_field(field)
        address = register['address']
        read = self._i2c_read(slave=slave, register=address, n=1)
        zero_based_data = self._get_field_data_from_register_data(list(read.data.values())[0], register['fields'][field]['size'], register['fields'][field]['offset'])
        res = i2c_response(acks=read.acks, data={field: zero_based_data})
        return res
    
    def _optimize_addresses_chunks(self, addresses:list):
        addresses.sort()
        address_chunks = [list(map(lambda a: a[1], g)) for _, g in itertools.groupby(enumerate(addresses), lambda e: e[1] - e[0])]
        return address_chunks
    
    def load_register_map(self, filepath:str):
        regmap = None
        try:            
            with open(filepath, 'r') as file:
                regmap = json.load(file)
        except Exception as error:
            print("An exception occurred:", error)
        finally:
            self.regmap = regmap
            return regmap
        
    def write(self, slave:int, target:str|int|dict=None, data:int|list=None):
        if(target is None or isinstance(target, int)):
            res = self._i2c_write(slave=slave, register=target, data=data)
        else:
            regmap_info = self._retrieve_regmap_info()
            if(isinstance(target, dict)):
                if data is not None:
                    print('Warning: write target argument was a dictiionary but data argument was also provided\nThis method expects data values to be the values part of the dictionary not to be provided otherwise\ndata argument is IGNORED')
                addresses = dict(filter(lambda t: isinstance(t[0], int), target.items()))
                registers = dict(filter(lambda t: t[0] in regmap_info.register_names, target.items()))
                fields = dict(filter(lambda t: t[0] in regmap_info.fields_names, target.items()))
                registers_addresses = {}
                if len(registers) > 0:
                    registers_addresses = dict(map(lambda r: (r[0], {'address': self.regmap[r[0]]['address'], 'value': r[1]}), registers.items()))
                    addresses = addresses | dict(map(lambda r: (r['address'], r['value']), registers_addresses.values()))
                fields_registers = {}
                if len(fields) > 0:
                    for field in fields.items():
                        register = self._find_register_from_field(field[0])
                        if register['fields'][field[0]]['size'] == 8:
                            addresses = addresses | {register['address']: field[1]}
                        else:
                            fields_registers[field[0]] = register
                    same_register_fields = dict([(a, list(map(lambda x: x[0], g))) for a, g in itertools.groupby(fields_registers.items(), lambda r: r[1]['address'])])
                    read = self.read(slave=slave, target=list(same_register_fields.keys()))
                    fields_registers_data = {}
                    for r in same_register_fields.items():
                        modify_request = list(map(lambda f: modify_read_operand(field_data=target[f], field_offset=fields_registers[f]['fields'][f]['offset'], field_size=fields_registers[f]['fields'][f]['size']), r[1]))
                        fields_registers_data[r[0]] = self._modify_read_data(read_data=read.data[r[0]], operand=modify_request)
                    addresses = addresses | fields_registers_data
                optimized_addresses = self._optimize_addresses_chunks(list(addresses.keys()))
                chunks = dict(map(lambda c: (c[0], c[1]), [(chunk[0], list(map(lambda c: addresses[c], chunk))) for chunk in optimized_addresses]))
                res = i2c_response()
                for c in chunks.items():
                    r = self._i2c_write(slave=slave, register=c[0], data=c[1])
                    res.acks[c[0]] = r.acks
            elif(target in regmap_info.register_names):
                address = self.regmap[target]['address']
                res = self._i2c_write(slave=slave, register=address, data=data)
            elif(target in regmap_info.fields_names):
                res = self._i2c_write_field(slave=slave, field=target, data=data)
            else:
                raise Exception(f'Error: attempting to read {target} but that is not found in the loaded register map')
        return res
    
    def read(self, slave:int, target:str|int|list, n:int=1):
        if(isinstance(target, int)):
            res = self._i2c_read(slave=slave, register=target, n=n)
        else:
            regmap_info = self._retrieve_regmap_info()
            if(isinstance(target, list)):
                addresses = list(filter(lambda t: isinstance(t, int), target))
                registers = list(filter(lambda t: t in regmap_info.register_names, target))
                fields = list(filter(lambda t: t in regmap_info.fields_names, target))
                registers_addresses = []
                if len(registers) > 0:
                    registers_addresses = list(map(lambda r: self.regmap[r]['address'], registers))
                    addresses += registers_addresses
                fields_registers = {}
                if len(fields) > 0:
                    for field in fields:
                        fields_registers[field] = self._find_register_from_field(field)
                    addresses += list(map(lambda f: f['address'], fields_registers.values()))
                chunks = self._optimize_addresses_chunks(addresses=list(set(addresses)))
                res = i2c_response()
                for c in chunks:
                    r = self._i2c_read(slave=slave, register=c[0], n=len(c))
                    res.acks[c[0]] = r.acks
                    res.data = res.data | r.data
                friendly_data = {} 
                if len(registers) > 0 or len(fields_registers.keys()) > 0:
                    for d in res.data.items():
                        if d[0] in registers_addresses or d[0] in list(map(lambda f: f['address'], fields_registers.values())):
                            if d[0] in registers_addresses:
                                friendly_data[self._get_register_from_address(d[0])[0]] = d[1]
                            else:
                                for register in fields_registers.items():
                                    friendly_data[register[0]] = self._get_field_data_from_register_data(d[1], register[1]['fields'][register[0]]['size'],  register[1]['fields'][register[0]]['offset'])
                                    print(d)
                        else:
                            friendly_data[d[0]] = d[1]
                    res.data = friendly_data
            elif(target in regmap_info.register_names):
                address = self.regmap[target]['address']
                res = self._i2c_read(slave=slave, register=address, n=n)
                res.data[target] = res.data[address]
            elif(target in regmap_info.fields_names):
                res = self._i2c_read_field(slave=slave, field=target)
            else:
                raise Exception(f'Error: attempting to read {target} but that is not found in the loaded register map')
        return res



