import subprocess
import shlex
import string
from random import randint, choice

cmd = "kubectl get secrets"
args = shlex.split(cmd)
p = subprocess.run(args, capture_output=True)
p.stdout

x = p.stdout.splitlines

chars = string.ascii_letters + string.digits + string.punctuation.replace("'","")


pw = "".join(choice(chars) for x in range(randint(12,16)))


#kubernetes client
from kubernetes import client, config
import base64
import pprint

config.load_kube_config()

v1 = client.CoreV1Api()
#help(v1)

#list secrets
v1.list_secret_for_all_namespaces()
secrets = v1.list_namespaced_secret(namespace="default")
secrets.items[0].metadata.name

#data
db = 'DB761'
ht = 'oak4ap0qih.database.windows.net'
dben = (base64.b64encode(db.encode('utf-8'))).decode('utf-8')
hten = (base64.b64encode(ht.encode('utf-8'))).decode('utf-8')

#create a secret
namespace = 'default'
name = 'db761-sql-test1'
metadata = {'name': 'db761-sql-test1', 'namespace': 'default'}
data=  {'sql-host': hten, 'sql-db': dben}
api_version = 'v1'
#kind = 'none'
body = client.V1Secret(api_version, data, metadata=metadata)

api_response = v1.create_namespaced_secret(namespace, body)
pprint.pprint(api_response)

body = client.V1DeleteOptions()
v1.delete_namespaced_secret(name, namespace, body)