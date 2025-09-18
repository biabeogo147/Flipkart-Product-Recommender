# 🛒 Flipkart Product Recommender — LLM‑powered • K8s‑native • Observable

> A production‑style demo that blends **LLM reasoning** (Gemini), **vector search** (Astra DB), and a **container‑first, Kubernetes‑native** deployment with **Ingress** and **Prometheus monitoring**.

---

## 🌟 Highlights

* ☸️ **Kubernetes, done right**: Deployments, Services, Ingress, Namespaces; clean label/selector hygiene.
* 🩺 **Health checks**: Readiness & liveness probes on `/` (port name `http`).
* 🧠 **LLM + Embeddings**: Gemini for reasoning; Sentence‑Transformers for vectorization.
* 🗄️ **Vector store**: Astra DB Collections (via token + endpoint).
* 🔐 **Secure config**: Multi‑provider secrets managed via K8s `Secret` → `envFrom`.
* 🔭 **Observability**: Prometheus Operator `ServiceMonitor` scraping `/metrics`; Grafana behind its own Ingress.
* 🐳 **Containers**: Single app container, `8000` → Service `80`.

---

## 🧰 Tech Stack

* **AI / Data**: Google **Gemini 2.5 Pro** (LLM) • Hugging Face **Sentence‑Transformers** (embeddings) • **Astra DB** (vector store)
* **Platform**: **Docker** • **Kubernetes** (Deployments, Services, Ingress, Namespaces)
* **Networking**: **NGINX Ingress Controller** (host‑based routing)
* **Observability**: **Prometheus Operator** (ServiceMonitor) • **Grafana**

**Container image**: `biabeogo147/flipkart-recommender-app:v1.0.0`
**App port**: `8000` (container, port name: `http`) → **Service** `80` (port name: `app`)

---

## 🧱 Architecture (at a glance)

```
[ Browser ] ──► [ NGINX Ingress ] (hosts: flipkart-recommender.local, grafana.local, prometheus.local)
                     │                                      
         ┌───────────┴──────────────────────────────────────┐───────────────────────────────────┐
         ▼                                                  ▼                                   ▼
 [ flipkart-recommender ]                       [ monitoring-grafana ]               [ monitoring-prometheus ]
 (Ingress: flipkart-recommender.local)        (Ingress: grafana.local)             (Ingress: prometheus.local)
         │                                                                               └─► SVC: monitoring-kube-prometheus-prometheus:9090
         │
         ▼
 [ flipkart-recommender-service ]  (ClusterIP:80 → Pod:8000 http)
         │
         ▼
 [ App Pod: LLM + Embeddings + /metrics ] ──► [ Astra DB (Vector) ]
         ▲
         └── K8s Secret: GOOGLE_API_KEY, HUGGINGFACEHUB_API_TOKEN,
                         ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT

[ Prometheus Operator ] ◄─ ServiceMonitor (interval=15s, path=/metrics, port=app) ── scrapes ── App Pod
```

---

## 🚀 Quick Start (Kubernetes)

```bash
kubectl create namespace flipkart-recommender

kubectl create secret generic flipkart-recommender-secrets \
  --from-literal=GOOGLE_API_KEY="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  -n flipkart-recommender \
  --dry-run=client -o yaml | kubectl apply -f -

# Apply core manifests
kubectl apply -f ./k8s-yaml/app-deployment.yaml
kubectl apply -f ./k8s-yaml/ingress-config.yaml
kubectl apply -f ./k8s-yaml/prometheus-service-monitor.yaml
```

**Verify runtime**

```bash
echo "=== Pods (all namespaces) ==="; kubectl get pods -A
echo "=== Services (all namespaces) ==="; kubectl get svc -A
echo "=== Ingress (all namespaces) ==="; kubectl get ingress -A
```

**Tear down**

```bash
kubectl delete -f ./k8s-yaml/app-deployment.yaml
kubectl delete secret <secret-name> -n <namespace>
```

---

## 🔎 Troubleshooting

* **Pods pending / crashloop** → `kubectl -n flipkart-recommender describe pod <pod>`; then `kubectl -n flipkart-recommender logs <pod>`
* **Ingress not routing** → ensure NGINX Ingress Controller is installed; add hosts locally:

  ```bash
  echo "node_ip flipkart-recommender.local grafana.local prometheus.local" | sudo tee -a /etc/hosts
  ```
* **Prometheus not scraping** → confirm Prometheus Operator is deployed; check Service has port name `app` and `/metrics` is reachable.

---

## 🔒 Security Notes

* Secrets are injected via `envFrom: secretRef` (`flipkart-recommender-secrets`), not baked into images.
* Namespace isolation (`flipkart-recommender`, `monitoring`).
* Resource limits protect cluster stability.

---

## 📄 Attribution

Based on: [https://github.com/data-guru0/FLIPKART-PRODUCT-RECOMMENDER-SYSTEM](https://github.com/data-guru0/FLIPKART-PRODUCT-RECOMMENDER-SYSTEM), adapted to an **LLM‑enhanced**, **K8s‑native**, **observability‑first** workflow.