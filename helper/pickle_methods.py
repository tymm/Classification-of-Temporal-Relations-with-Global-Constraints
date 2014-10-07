import copy_reg
import types
import pickle

def _pickle_method(method):
    # Author: Steven Bethard
    # http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods
    func_name = method.im_func.__name__
    #obj = method.im_self
    cls = method.im_class
    cls_name = ''
    if func_name.startswith('__') and not func_name.endswith('__'):
        cls_name = cls.__name__.lstrip('_')
    if cls_name:
        func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, cls)

def _unpickle_method(func_name, cls):
    # Author: Steven Bethard
    # http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(cls)

# This call to copy_reg.pickle allows you to pass methods as the first arg to
# mp.Pool methods. If you comment out this line, `pool.map(self.foo, ...)` results in
# PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup
# __builtin__.instancemethod failed

def activate():
    copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
