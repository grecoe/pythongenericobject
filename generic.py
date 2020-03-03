import typing

class GenericObject:
    '''
        Class that breaks down a json object into a class that has attributes
        named the same as the json object so you don't have to keep using 
        dictionary indexing to get to what you are after.
    '''
    def __init__(self, properties : dict):
        
        if isinstance(properties, dict):
            parsed = GenericObject._expand_dict(properties)
            for item in parsed.keys():
                self.__setattr__(item, parsed[item])
        elif isinstance(properties, list):
            parsed = GenericObject._expand_list(properties)
            self.__setattr__("list", parsed)
        else:
            print("UNKNOWN", properties)
            raise Exception("Unknown type....")

    @staticmethod 
    def has_property(generic_object, prop_list):
        prop_available = False
        if isinstance(generic_object, GenericObject):
            stepped_object = generic_object
            for prop in prop_list:
                if isinstance(stepped_object, GenericObject) and hasattr(stepped_object, prop):
                    prop_available = True
                    stepped_object = getattr(stepped_object, prop)
                else: 
                    prop_available = False
                    break

        return prop_available

    @staticmethod
    def dumpObject(generic_object, indent = 0, optional_end = ''):
        """
            dumpObject prints out the contents of a GenericObject instance
            so that the user can see that it was built correctly. 

            generic_object = A GenericObject instance
            indent = Number of spaces to indent printed lines
            optional_end = Optional line ending

            Both indent and optional_end are used internally, if you want to add one, 
            go for it, but it's not required.
        """

        indent_string = "" 
        if indent > 0:
            indent_string = " " * indent

        if isinstance(generic_object, GenericObject):
            v = vars(generic_object)
            for k in v.keys():
                if isinstance(v[k], GenericObject):
                    print(indent_string, k, '=')
                    GenericObject.dumpObject(v[k], indent + 2, optional_end)
                elif isinstance(v[k], list):
                    any_generics = False
                    for sub_item in v[k]:
                        if isinstance(sub_item, GenericObject):
                            any_generics = True
                            break
                    
                    if any_generics:
                        print(indent_string, k, '= [')
                        for sub_item in v[k]:
                            GenericObject.dumpObject(sub_item, indent + 1, ',')
                            print(indent_string,'-------')
                        print(indent_string,']')
                    else:
                        print(indent_string, k,'=',v[k], optional_end)    

                else:
                    print(indent_string, k,'=',v[k], optional_end)    
        else:
            print(indent_string, generic_object, optional_end)

    @staticmethod
    def _expand_dict(props) -> dict:
        """
            Expands a dictionary and parses sub items in a dict or contained list
            into the correct format.
        """
        return_dict = {}
        for key in props.keys():
            if isinstance(props[key], dict):
                expanded = GenericObject(props[key])
                return_dict[key] = expanded
            elif isinstance(props[key], list):
                sub_list = []
                for sub_item in props[key]:
                    if isinstance(sub_item, dict) or isinstance(sub_item, dict):
                        sub_list.append(GenericObject(sub_item))
                    else:
                        sub_list.append(sub_item)
                return_dict[key] = sub_list
            else:
                return_dict[key] = props[key]
        return return_dict

    @staticmethod
    def _expand_list(props) -> list:
        """
            Expands a list and parses sub items in a dict or contained list
            into the correct format.
        """
        return_list = []
        for item in props:
            if isinstance(item, dict) or isinstance(item, list):
                expanded = GenericObject(item)
                if expanded:
                    return_list.append(expanded)
            else:
                return_list.append(item)
        return return_list
