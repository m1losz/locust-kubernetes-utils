1. Creating k8s resources (only have to run this once, unless you delete them in k8s)
```
ssh-keyscan $YOUR_GIT_HOST > /tmp/known_hosts

kubectl create namespace test

kubectl -n test create secret generic {TESTER_NAME}-git-creds \
    --from-file=ssh=$HOME/.ssh/id_ecdsa \
    --from-file=known_hosts=/tmp/known_hosts

kubectl -n test create secret generic {TESTER_NAME}-git-config \
    --from-file=ssh_config=$HOME/.ssh/config
```
2. Generate manifests files
```
// this will generate k8s manifest files in `--output` directory
python3 locust-deploy.py -c values.yml
//or pass in args from command line
python3 locust-deploy.py -c values.yml --name {TESTER_NAME} --services {space separated list of services to test against}
```

3. Spin up 
```
kubectl apply -f manifests/
```
& take down

```
kubectl delete -f manifests/
kubectl delete secret sfportal-git-creds
kubectl delete secret sfportal-git-config
```
