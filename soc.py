import json

class Loader(object):
    def __init__(self):
        # load modules path from module.json
        module_path = "./data/modules.json"
        modules = None
        with open(module_path, "r") as f:
            modules = json.load(f)
        self.modules = modules
        self.modprefix = "./data/"
    
    def load(self, soc_path):
        soc = None
        with open(soc_path, "r") as f:
            soc = json.load(f)
        # collect module names
        used_modules = set(map(lambda x:x["module"], soc["memmap"].values()))
        # load module data from json files
        modules = {}
        for m in used_modules:
            module_path = self.modprefix + self.modules[m]
            mods = None
            # load module data from json
            with open(module_path, "r") as f:
                mods = json.load(f)
            # TODO: error check
            modules.update({m : mods})
        soc.update({"modules" : modules})
        return soc

