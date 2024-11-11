
import time
import os
from copy import deepcopy
from pprint import pprint
import uuid
import sys
import importlib

def generate_uuid_from_string(input_string):
    # 使用命名空间 UUID（可以使用预定义的命名空间，如 NAMESPACE_DNS）
    namespace = uuid.NAMESPACE_DNS
    # 根据输入字符串和命名空间生成 UUID
    generated_uuid = uuid.uuid5(namespace, input_string)
    return str(generated_uuid)

def clear_print(content,time_sleep=0):
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
    temp=deepcopy(content)
    def backtrace_cut(dictobj):
        if isinstance(dictobj,dict):
            for k,v in dictobj.items():    
                if isinstance(v,str) and len(v)>100:
                    dictobj[k]=v[:50]+v[-50:]
                elif isinstance(v,dict):
                    backtrace_cut(v)
        return dictobj
    pprint(backtrace_cut(temp))
    time.sleep(time_sleep)
    

def import_if_not_exists(package_names):
    for package_name in package_names:
        if package_name not in sys.modules:
            importlib.import_module(package_name)
            # print(f"{package_name} was imported.")
            pass
        else:
            # print(f"{package_name} is already imported.")
            pass
        
class CustomVector:
    def __init__(self,init_value=[],x_range=None,y_range=None,dim=None):
        if init_value!=[]:
            self.vector=init_value
        elif dim == None:
            self.vector=[0]*2

    def __add__(self,other):
        return [self.vector[i]+other.vector[i] for i in range(len(self.vector))]
    
    def __sub__(self,other):
        return [self.vector[i]-other.vector[i] for i in range(len(self.vector))]
    
    def __mul__(self,scale):
        return [self.vector[i]*scale for i in range(len(self.vector))]
    
    def norm(self):
        return sum([i**2 for i in self.vector])**0.5
    
    def __truediv__(self,scale):
        return [self.vector[i]*(1/scale) for i in range(len(self.vector))]
    
    def __str__(self) -> str:
        return str(self.vector)
    
    def dot(self,other):
        return sum([self.vector[i]*other.vector[i] for i in range(len(self.vector))])
    
    #两个向量之间的欧氏距离
    def euclidean_distance(self,other):
        return sum([(self.vector[i]-other.vector[i])**2 for i in range(len(self.vector))])**0.5
    
# test=CustomVector([1,2])
# print(test)
# print(test.dot(CustomVector([1,0])))
# print(test.norm())
# print(test*2)
# print(test/2)
# print(type(test))