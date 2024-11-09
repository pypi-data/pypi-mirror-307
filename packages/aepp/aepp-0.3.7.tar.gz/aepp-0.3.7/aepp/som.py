class Som:
    """
    The Som is a class that will help you to handle to create data in a dictionary format, or JSON.\
    Creating the capability to build XDM payload directly via a simple dot notation path.
    This class is inspired by the SOM project from the JS framework built.
    """
    import re

    def __init__(self,data:Union[dict,str]=None,options:dict=None)->None:
        """
        Instantiate the Som Object.
        Arguments:
        data : OPTIONAL : An existing dictionary representation (dict or stringify) that you want to use as template.
        options : OPTIONAL : A dictionary that contains some keys for additional settings:
            defaultValue : OPTIONAL : The default value to be returned when using the get method and no match is found. Default is None.
            deepcopy : OPTIONAL : Boolean to define if you want to deepcopy the data passed (default True).
            stack : OPTIONAL : If you want to create a stack to track your call.

        Example of options value: 
            {
            "defaultValue" : "my value fallback",
            "deepcopy" : True,
            "stack" : False
            }
        """
        self.__data__:dict = {}
        if data is not None:
            if type(data) == str:
                self.__data__ = json.loads(data)
            elif type(data) == dict:
                if options.get("deepcopy",True):
                    self.__data__ = deepcopy(data)
                else:
                    self.__data__ = data
        self.__defaultValue__ = options.get('defaultValue',None)
        if options.get('stack',False):
            self.stack = []
        else:
            self.stack = None

    def setDefaultValue(self,value:Union[str,int,float,bool])->None:
        """
        Set the default value returned as fallback from the get method.
        """
        self.__defaultValue__ = deepcopy(value)

    def __recurseSearch__(self,keys:list,data:dict)->Union[str,int,bool,float,dict]:
        """
        recursive search for the path
        Arguments:
            key : list of keys to search
            data : the dictionary traverse 
        """
        if len(keys) == 1:
            if type(data) == dict:
                if keys[0] in data.keys():
                    return data[keys[0]]
            elif type(data) == set:
                if key[0] in data:
                    return True
                else:
                    return False
            elif type(data) == list:
                if keys[0].isnumeric():
                    if abs(int(keys[0])) < len(data):
                        return data[int[keys[0]]]
                    else:
                        return data[len(data)-1]
        else:
            if type(data) == dict:
                if keys[0] in data.keys():
                    return self.__recurseSearch__(keys[1:],data[keys[0]])
            elif type(data) == set:
                if keys[0] in data:
                    return self.__recurseSearch__(keys[1:],data[keys[0]])
            elif type(data) == list:
                if keys[0].isnumeric():
                    if abs(int(keys[0])) < len(data):
                        return self.__recurseSearch__(keys[1:],data[keys[0]])
            else:
                return None

    def get(self,path:Union[str,list,set]=None,fallback:Union[str,int,float,bool]=None,params:dict=None)->Union[str,list,set,bool,dict]:
        """
        Retrieve the data based on the dot notation passed. 
        If you want to return everything, use it without any parameter.
        Arguments:
            path : OPTIONAL : The dot notation path that you want to return. You can pass a list of path and the first match is returned.
            fallback : OPTIONAL : Temporary fallback if the dot notation path is not matched and you do not want to get the defaultValue
        """
        if type(self.stack) == list:
            self.stack.append({'method' : 'get', 'path':path})
        if path is None:
            return self.__data__
        if type(path) == str:
            paths = [path]
        elif type(path) == set:
            paths = list(path)
        elif type(path) == list:
            paths = list(set(path))
        results = {}
        data = deepcopy(self.__data__)
        for p in paths:
            l_path:list = p.split('.')
            results[p] = self.__recurseSearch__(l_path,deepcopy(data))
            if results[p] is not None:
                return results[p]
        if fallback:
            return fallback
        else:
            return self.__defaultValue__
    

    def assign(self,path:str=None,value:Union[dict,list,str,int,float,set]=None,fallback:Union[dict,list,str,int,float,set]=None,params:dict=None)->None:
        """
        Assign a value to a path via dot notation, creating the path if the path does not already exist.
        Arguments:
            path : REQUIRED : The path where to place the value. In case you want to set at a specific array index of a list, use the "[]" notation, such as "my.path.[1].foo"
            value : REQUIRED : The value to assign, if value is dynamic and return None, you can decide to override it with the fallback value
            fallback : OPTIONAL : Value to be assigned. It would replace the None value if your assignement is dynamic and you want to avoid None.
            params: OPTIONAL : dictionary that can cast the change of an object type or override existing value.
                Example of keys in params:
                type : the type you want to cast your assignement to. Default None.
                override : if you want to override the existing value. By default primitive will be overriden, but not list. Default False.
                    An assignement of a value to a list will append that value, the same for Set.
                    An assignment of an dictionary to a list or a Set or a primitive will override that value.
                    By overriding, the value assign to a set or a list will take the place as the unique value of that elements.
        """
        override = params.get('override',False)
        type = params.get('type',None)
        data = self.__data__
        if type(self.stack) == list:
            self.stack.append({'method':'assign','path':path})
        list_nodes = path.split('.')
        for node in list_nodes:
            if node.startswith('[') and node.endswith(']'):
                node = node[1:-1]
                nodeInt = int(node)