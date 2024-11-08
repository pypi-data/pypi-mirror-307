class Registry:
    def __init__(self, name):
        self._name = name
        self._obj_map = {}

    def _do_register(self, name, obj):
        assert name not in self._obj_map, (
            f"An object named '{name}' was already registered "
            f"in '{self._name}' registry!"
        )
        if "RepositoryImpl" in name:
            name = name.replace("RepositoryImpl", "")
        self._obj_map[name] = obj

    def register(self, obj=None):
        if obj is None:

            def deco(func_or_class):
                name = func_or_class.__name__
                self._do_register(name, func_or_class)
                return func_or_class

            return deco
        name = obj.__name__
        self._do_register(name, obj)

    def get(self, name):
        if name in self._obj_map.keys():
            ret = self._obj_map.get(name)
        elif name + "Phase" in self._obj_map.keys():
            ret = self._obj_map.get(name + "Phase")
        else:
            raise KeyError(
                f"No object named '{name}' found in '{self._name}' registry!"
            )
        return ret

    def __contains__(self, name):
        return name in self._obj_map

    def __iter__(self):
        return iter(self._obj_map.items())

    def keys(self):
        return self._obj_map.keys()
