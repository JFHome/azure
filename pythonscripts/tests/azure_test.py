from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
import json

cl = get_client_from_cli_profile(ResourceManagementClient)

#type(cl)
#dir(cl)
#help(cl.resoure_groups)
rgl = []

for i in cl.resource_groups.list():
	#print(i.name)
    rgl.append(i.name)

rgl[0]

rl = []

for i in cl.resources.list_by_resource_group(rgl[0]):
	rl.append(i)

d = json.dumps(rl[0], default=lambda o: o.__dict__)
