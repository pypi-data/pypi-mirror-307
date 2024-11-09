# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 20:28:10 2023

@author: Hedi
"""


from .. import *
from tabulate import tabulate
from .__disp__ import _set_color, _set_decimals
from .__colors__ import __colors__
from numpy import array,zeros

class _schema_obj:
    def __init__(self, dict_):
            self.__dict__.update(dict_)

__schema__ = json.loads(json.dumps(json.loads(fernet.decrypt(open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 schema), "r").read())),), object_hook=_schema_obj,)

def getfield(obj,field,default):
    if hasattr(obj,field):
        return getattr(obj,field)
    else:
        return default
def getvalue(val,schema=None):
    if is_number(val):
        scientific_notation = getfield(schema, "scientific_notation", False)
        decimals = getfield(schema, "decimals", 0)
        val = _set_decimals(val, str(decimals),scientific_notation)
    return val
def is_number(s):
    if s==None:
        return False
    else:
        try:
            float(s) # for int, long and float
        except ValueError:
                return False
        return True


  
        
class __obj__:
    def __init__(self,*res_class):
        class res(*res_class):
            def __init__(self,obj,parent):
                for k,v in obj.__dict__.items():
                    try:
                        setattr(self,k,v.default)
                    except:
                            pass
                self.parent=parent
            def __repr__(self):
                data=[]
                for k,v in self.parent.schema.varargout.__dict__.items():
                    lign = self.parent.repr_lign(k,v)
                    if not lign is None:
                        data.append(lign)
                return tabulate(data,numalign="left", stralign="left",tablefmt="pretty") 
            
            
        for k,v in self.schema.varargin.__dict__.items():
            setattr(self,k,v.default)
        self.res=res(self.schema.varargout, self)
    @property
    def type(self):
        return type(self).__name__
    @property
    def __enc(self):
        return self.type.encode(encoding="utf-32").hex()
    @property
    def schema(self):
        return getattr(__schema__,self.type)
    def formatted_val(self,ks,vs):
        try:
            val = getattr(self,ks)
        except:
            val = getattr(self.res,ks)  
        if  hasattr(val, '__iter__') and not isinstance(val,str):
            val=list(map(lambda x: getvalue(x,vs),val))
            if val and is_number(val[0]):
                def num(s):
                    try:
                        return int(s)
                    except ValueError:
                        return float(s)
                val = list(map(lambda x:num(x),val))
        else:
            val = getvalue(val, vs)
        if hasattr(vs,"color"):
              val = _set_color(str(val), getattr(__colors__,vs.color))
        return val
    def repr_lign(self,ks,vs):
        if vs.repr:
            lign=[ks]
            lign.append (self.formatted_val(ks,vs))
            try:
                lign.append(vs.unit)
            except:
                    pass
            try:
                lign.append(vs.desc)
            except:
                pass
            return lign
        return None

    def __repr__(self):
        data=[]
        for k,v in self.schema.varargin.__dict__.items():
            lign = self.repr_lign(k,v)
            if not lign is None:
                data.append(lign)
        return tabulate(data,numalign="left", stralign="left",tablefmt="pretty")
    def __setattr__(self, name, value):
        if  hasattr(value, '__iter__') and not isinstance(value,str):
            super().__setattr__(name, array(value))
        else:
            super().__setattr__(name, value)
    def sensitivity_analysis(self,evaluate_model,variables,bounds,N_samples=1024,integer_vars=[]):
        from SALib.sample import saltelli
        from SALib.analyze import sobol
        from tqdm import tqdm
        problem = {'num_vars': len(variables),'names': variables,
            'bounds': bounds}
        # Generate Samples
        param_values = saltelli.sample(problem, N_samples);
        Y = zeros([param_values.shape[0]])
        # run model
        X_tmp = list(map(lambda x: getattr(self,x),variables))
        print(X_tmp)
        Y = zeros([param_values.shape[0]])
        for i, X in enumerate(tqdm(param_values,desc="{} sensitivity".format(self.type),colour='#00ff00',smoothing=1)):
            for j in range(len(variables)):
                if variables[j] in integer_vars:
                    setattr(self,variables[j],round(X[j]))
                else:
                    setattr(self,variables[j],X[j])
                self.calcul()
                if hasattr(self.res, evaluate_model):
                    Y[i] = getattr(self.res,evaluate_model)
                else:
                    Y[i] = getattr(self.res,evaluate_model)
                # perform analysis
        Si = sobol.analyze(problem, Y)
        # re-establish tmp values
        for i,v in enumerate(variables):
            setattr(self,v,X_tmp[i])
        return Si
    