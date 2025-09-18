I used source code from https://github.com/data-guru0/FLIPKART-PRODUCT-RECOMMENDER-SYSTEM and modified it based on my needs.

Create the secret, build the Docker image and deploy the application.
```bash
kubectl create namespace flipkart-recommender
kubectl create secret generic flipkart-recommender-secrets \
  --from-literal=GOOGLE_API_KEY="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  -n flipkart-recommender \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f ./k8s-yaml/app-deployment.yaml
kubectl apply -f ./k8s-yaml/ingress-config.yaml
kubectl apply -f ./k8s-yaml/prometheus-service-monitor.yaml
```

If you need to delete the deployment, use:
```bash
kubectl delete -f app-deployment.yaml
```

Check the created secret:
```bash
kubectl get secrets
```

Delete the created secret:
```bash
kubectl delete secret <secret-name> -n <namespace>
```

Check the status of your pods, services, and ingress resources:
```bash
echo "=== Pods in default namespace ==="
kubectl get pods

echo "=== Services in default namespace ==="
kubectl get svc

echo "=== Ingress resources ==="
kubectl get ingress -A
```