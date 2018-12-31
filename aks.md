# AKS

## download kubernetes

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/windows/amd64/kubectl.exe
```

connect to AKS:
```
az aks get-credentials --resource-group FXWEPOCRGP03 --name FXWEPOCAKS01
```

test connection:
```
kubectl get nodes
```