# Project 2: AI-Powered Air Quality Analysis

Welcome to AskVigil by SleepUnderflow. We are using a containerized Python stack. This means if it runs on your laptop in Docker, it **will** work on the Oracle server.

---

## 🛠 The Tech Stack

* **Frontend: React** — Flexible and industry-standard for building our dashboard.
* **Backend: FastAPI** — High-performance Python. It’s fast to develop and has native support for AI libraries like PyTorch.
* **AI: DistilBERT (Hugging Face)** — A "distilled" version of BERT. It gives us heavy-duty NLP capabilities while remaining light enough for our Oracle ARM instance.
* **Database: PostgreSQL + pgvector** — Reliable relational data storage. `pgvector` allows us to store AI embeddings for semantic search or similarity matching.
* **Containerization: Docker** — Wraps everything in a "bubble" to eliminate "it works on my machine" issues and library conflicts.
* **Proxy: Nginx Proxy Manager** — A GUI that handles our DuckDNS and SSL certificates so we never have to touch a raw `.conf` file again.

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
Install **Docker Desktop** and **VS Code**. 

### 2. Setup
1.  Clone the repo.
2.  Create a `.env` file in the root directory (see the lead for the template).
3.  Fire up the stack:
    ```bash
    docker-compose up --build
    ```
4.  **Verification:**
    * **App:** [http://localhost:3000](http://localhost:3000)
    * **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (FastAPI generates this automatically!)

---

## ☁️ Deployment (CI/CD)

We are using **GitHub Actions** for "Hands-Off" deployment. 
* **The Flow:** Push your code to the `main` branch → GitHub SSHes into Oracle → Docker rebuilds only what changed.
* **Note:** If you add a new Python library, add it to `backend/requirements.txt`.

---

## ⚠️ Ground Rules
1. **Never** commit the `.env` file to Git (it’s in the `.gitignore`).
2. **Never** upload large AI model files. We mount them as volumes on the server to keep the repo light.
3. **Always** test your `docker-compose up` locally before pushing to `main`.