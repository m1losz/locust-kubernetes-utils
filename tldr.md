1. Generate manifests files
```
python3 locust-deploy.py -n sfportal \
	-r git@github.com:m1losz/CS-Structured-QA-SFPortal-LoadTest \
	-f CS-Structured-QA-SFPortal-LoadTest/main_task.py \
	-t http://a197dcbcaa43111e9985606b182dacc2-0e4bd8d2e4f0ba4b.elb.us-west-2.amazonaws.com/ \
	-s 10 \
        -S portal_example portal_portfolio 
```

2. Creating k8s resources
```
ssh-keyscan $YOUR_GIT_HOST > /tmp/known_hosts

kubectl create namespace test

kubectl -n test create secret generic sfportal-git-creds \
    --from-file=ssh=$HOME/.ssh/id_ecdsa \
    --from-file=known_hosts=/tmp/known_hosts

kubectl -n test create secret generic sfportal-git-config \
    --from-file=ssh_config=$HOME/.ssh/config
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
