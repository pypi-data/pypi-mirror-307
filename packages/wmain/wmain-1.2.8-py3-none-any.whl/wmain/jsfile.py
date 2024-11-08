import execjs

class JsFileModel:
    
    def __init__(self, js_file):
        with open(js_file, 'r') as f:
            self.js = execjs.compile(f.read())
    
    def call(self, func_name, *args):
        return self.js.call(func_name, *args)
        
        

if __name__ == '__main__':
    js_model = JsFileModel("des.js")
    print(js_model.call("strEnc", '1', '1', '2', '3'))