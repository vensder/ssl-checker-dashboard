# How to run in Kubernetes

Tested in MicroK8s: <https://microk8s.io/>

```bash
sudo microk8s enable ingress
```

```bash
kubectl apply -f web-app.yml
deployment.apps/web-app created
service/web-app created
ingress.networking.k8s.io/web-app created
service/redis created
deployment.apps/redis created
deployment.apps/cron created
```

```bash
kubectl get ingress
NAME      CLASS    HOSTS              ADDRESS     PORTS   AGE
web-app   <none>   ssl-checks.local   127.0.0.1   80      47s
```

Add `ssl-checks.local` host to `/etc/hosts` file:

```bash
grep ssl-checks /etc/hosts
127.0.0.1 ssl-checks.local
```

Open in browser: <http://ssl-checks.local/>
