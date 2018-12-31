import sys
import json
import getpass
import pyodbc
from io import StringIO
import string
from random import randint, choice
from kubernetes import client, config
import base64
import pprint
import azure.cosmos.cosmos_client as cosmos_client

def arg_chk():
    if len(sys.argv)!=2:
        print("Please use one parameter")
        exit()
arg_chk()

#parameter file name:
pfn = sys.argv[1]

#constants:
#ppn = "C:\\projects\\azure\\params\\"
namespace = "default"
api_version = 'v1'
chars = string.ascii_letters + string.digits + string.punctuation.replace("'","")
cosmosconf = {
    'ENDPOINT': 'https://fxwepoccqa001.documents.azure.com:443/',
    'PRIMARYKEY': 'MEapTcCRjmoPzZNcltKCGNtu8BodwaJ9kCllHUzy8vstdxCxaemyzSqKbKYjEfjuTSiey5t6bimGrNrZpDY96g==',
    'DATABASE': 'PARAMETERS',
    'CONTAINER': 'secrets'
}


# Initialize the Cosmos client
print('Initialize cosmos client')
cosmos = cosmos_client.CosmosClient(url_connection=cosmosconf['ENDPOINT'], auth={
                                    'masterKey': cosmosconf['PRIMARYKEY']})
# get parameter data from cosmos db
print('query parameter json')
cnlnk = "dbs/PARAMETERS/colls/secrets"
sql = "SELECT * FROM c WHERE c.id = '{0}'".format(pfn)
options = {}
options['enableCrossPartitionQuery'] = True
options['maxItemCount'] = 1
ret = cosmos.QueryItems(cnlnk, sql, options)
for i in ret:
    j = i

#getting kubernets config and json data file
config.load_kube_config()
cc = config.list_kube_config_contexts()[0][0]["name"]
kube = client.CoreV1Api()
#fn = ppn + pfn
#f = open(fn, 'r', encoding='ascii')
#j = json.load(f)
aks = j["aks"]

if cc != aks:
    print("these data are supposed to use in {0}, not in current context ({1})".format(aks, cc))
    exit()

#password and connection string, test connection
ssrvn = j["host"]
sdbn = j["db"]
ssa = j["user"]
pw = ''
pw = getpass.getpass()
cnn = ( "DRIVER={ODBC Driver 17 for SQL Server}"
        ";SERVER=" + ssrvn +
        ";DATABASE=" + sdbn +
        ";UID=" + ssa +
        ";PWD=" + pw
)
cnxn = pyodbc.connect(cnn)
crsr = cnxn.cursor()
#crsr.execute("SELECT DB_NAME();")
#row = crsr.fetchone()
#while row:
#    print(row[0])
#    row = crsr.fetchone()


for secret in j["values"]:
    u = secret["sql-user"]
    s = secret["secret-name"]
    db = secret["sql-db"]
    ht = secret["sql-host"]
    pw = "".join(choice(chars) for x in range(randint(12,16)))
    sql="""
IF EXISTS (SELECT * FROM sys.database_principals WHERE [name] = '{0}' AND [type] = 'S')
    DROP USER [{0}];
CREATE USER [{0}] WITH PASSWORD='{1}';
ALTER ROLE db_datareader ADD MEMBER[{0}];
ALTER ROLE db_datawriter ADD MEMBER[{0}];""".format(u,pw)
    if u.endswith('_adm'):
        sql+="""
ALTER ROLE db_ddladmin ADD MEMBER[{0}];""".format(u)

    for stmnt in sql.split(';'):
        with cnxn.cursor() as crsr:
            if len(stmnt) > 2:
                #print("Statment: " + stmnt)
                crsr.execute(stmnt)
    
    print("sql statements executed.")

    fs = "metadata.name=" + s
    ret = kube.list_namespaced_secret('default', field_selector=fs) 
    if len(ret.items)>0:
        print('delete the secret')
        body = client.V1DeleteOptions()
        kube.delete_namespaced_secret(s, namespace, body)
    
    print("create base64 strings")
    dben = (base64.b64encode(db.encode('utf-8'))).decode('utf-8')
    hten = (base64.b64encode(ht.encode('utf-8'))).decode('utf-8')
    pwen = (base64.b64encode(pw.encode('utf-8'))).decode('utf-8')
    uen = (base64.b64encode(u.encode('utf-8'))).decode('utf-8')

    metadata = {'name': s, 'namespace': namespace}
    data=  {'sql-host': hten, 'sql-db': dben, 'sql-user': uen, 'sql-pw': pwen}

    body = client.V1Secret(api_version, data, metadata=metadata)

    print ('create secret')
    api_response = kube.create_namespaced_secret(namespace, body)
    #pprint.pprint(api_response)

print ('end of taks')

