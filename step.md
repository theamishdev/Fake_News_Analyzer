# DevOps Showcase: Docker Desktop & GitHub Actions

This guide provides step-by-step instructions for showcasing the modern DevOps workflow integrated into the Smart News Analyzer project.

## 🐳 Containerization with Docker Desktop

Docker simplifies deployment by packaging the frontend, backend, and ML services into isolated containers.

### 1. Build and Launch the Stack
Run the following command in the project root to build all images and start the containers:
```bash
docker-compose up --build
```
*   **Showcase Point**: Note how Docker Orchestration manages inter-service dependencies (multi-tier architecture).

### 2. Verify Services in Docker Desktop
Open the **Docker Desktop Dashboard**:
-   **Containers**: You should see a group named `int332` containing the following services:
    -   `frontend`: Serving on [http://localhost:3000](http://localhost:3000)
    -   `backend`: Coordinating API at [http://localhost:8080](http://localhost:8080)
    -   `ml-service`: Flask processing at [http://localhost:5000](http://localhost:5000)
    -   `elasticsearch`, `logstash`, `kibana`: The ELK logging stack.
-   **Images**: Check the `Images` tab to see the custom-built images for each service.

### 3. Centralized Logging (ELK)
-   Access **Kibana**: [http://localhost:5601](http://localhost:5601)
-   **Showcase Point**: Enter a query in the frontend, then demonstrate how logs flow from the Backend and ML services into a single centralized dashboard in Kibana.

---

## 🚀 Continuous Integration with GitHub Actions

The project includes a pre-configured CI pipeline that automates testing and building.

### 1. Trigger the Pipeline
1.  Navigate to the project on GitHub.
2.  Make a small change (e.g., in `README.md` or a comment in a source file).
3.  Commit and push the change to the `main` branch.

### 2. Monitor the Workflow
1.  Click on the **Actions** tab in your GitHub repository.
2.  You will see a workflow titled **CI/CD Pipeline** currently running.
3.  Click on the workflow run to see live logs for:
    -   `Set up JDK 17` (Backend environment)
    -   `Build Backend with Maven` (Compiling and testing)
    -   `Install ML Service Dependencies` (Validating Python setup)
    -   `Build Docker Images` (Simulated container build)

### 3. Key Pipeline Benefits
-   **Automation**: No manual compilation or testing required.
-   **Consistency**: The pipeline runs in a clean GitHub-hosted environment, ensuring "it works on my machine" issues are minimized.
-   **Feedback Loop**: Immediate notification if a code push breaks the build.

---

## 📊 Summary of Integrated Tools

-   **Version Control**: GitHub
-   **CI/CD**: GitHub Actions
-   **Build Tool**: Apache Maven
-   **Containerization**: Docker
-   **Orchestration**: Docker Compose
-   **Monitoring**: ELK Stack
