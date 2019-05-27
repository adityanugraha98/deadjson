import json,os,time

class Util(dict):

    def __init__(self, data,fp=False):
        self.waktu = time.time()
        if not fp:
            if type(data) == str:
                data = json.load(data)
        else:
            self.file = data.replace("/data.json","")
            if not os.path.exists(data):
                os.makedirs(data)
            if not os.path.exists(self.file):
                open(self.file,"w").write("{}")
            with open(self.file, encoding='utf-8', mode="r") as f:
                data = json.load(f)
        for a,b in data.items():
            setattr(self, a, self._make(b))

    def save(self,saves=True):
        if self.file and saves == True:
            if not self.file.endswith(".json"):
                self.file+="/data.json"
            if self.waktu and time.time() - self.waktu < 3:
                return
            with open(self.file, encoding='utf-8', mode="w") as f:
                json.dump(
                    self, f,
                    indent=4,sort_keys=True,
                    separators=(',',' : ')
                )
                if self.waktu:
                    del self.waktu
        return json.dumps(self, sort_keys=True, indent=4)

    def __repr__(self):
        return str(json.dumps(self, sort_keys=True, indent=4))

    def __setattr__(self,key,value):
        super().__setitem__(key,self._make(value))
        self.save()
    
    def __setitem__(self, key, value):
        setattr(self, key, self._make(value))
        self.save()

    def __delattr__(self,attr):
        self.__delitem__(attr)
        self.save()
    
    def __getattr__(self, attr):
        return self.get(attr, None)
    
    def __getitem__(self, attr):
        return self.get(attr, None)

    def _make(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._make(v) for v in value])
        else:
            if isinstance(value, dict):
                return Util(value)
            else:
                return value