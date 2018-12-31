
az aks get-credentials --resource-group FXWEPOCRGP03 --name FXWEPOCAKS01

kubectl create secret generic poc-db-secret --from-literal=tstname=produser --from-literal=password=Y4nys7f11
kubectl delete secret poc-db-secret



