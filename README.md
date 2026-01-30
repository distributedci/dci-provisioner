# DCI Provisioner

**A flexible provisioning system using Redis, RQ (Redis Queue), and Ansible.**

The dci-provisioner is used my the DCI RHEL agent to manage the provisioning of client test systems.  This project implements an asynchronous provisioning pipeline. It utilizes a Python API to receive provisioning requests, queues them via Redis, and processes them using RQ workers that execute Ansible playbooks to configure target infrastructure.

## Architecture Overview

This system is composed of several key components working together to automate infrastructure provisioning:

1.  **API Layer (api/)**: A Python-based interface that accepts incoming provisioning requests, validates the payloads, and enqueues jobs into Redis.
2.  **Task Queue (Redis & RQ)**: Acts as the broker and worker system. The API pushes jobs to Redis, and detached workers (running `run_worker.sh`) pull these jobs to execute them asynchronously.
3.  **Provisioning Logic**: The core execution logic is handled by Ansible playbooks. These playbooks interact with the target nodes to perform configuration management and deployment tasks.
4.  **Provisioner Container**: A specialized container acting as the controller node. It typically hosts necessary network boot services (like `hooktftp`) to handle PXE booting and Kickstart file delivery for provisioning bare-metal or virtual machines.
5.  **Process Management**: Inside the containers, `supervisord` is used to manage the API, workers, and other background processes, ensuring they remain active and restart if they fail.

## Basic Operation

### 1. Building and Running Containers
The repository relies on containerization for consistent execution. A `Makefile` is provided to simplify building and running the components.

* **Build Images**: Use the build targets in the `Makefile` (e.g., `make build`) to generate the container images defined in `Containerfiles/`.
* **Start Services**: The `entrypoint.sh` script handles the startup sequence. This script detects the environment and initializes the necessary processes (RQ worker or API service) via `supervisord`.

### 2. Workflow Lifecycle
When a provisioning request is triggered (via the API):

1.  **Request**: The API receives the JSON payload and performs initial validation.
2.  **Queue**: A job is created based on the request and pushed to the Redis `default` queue.
3.  **Execution**: An idle RQ worker picks up the job from the queue.
4.  **Action**: The worker executes the designated Ansible playbooks or generates Kickstart configurations using templates found in `templates/`.
5.  **Completion**: The worker updates the job status (Success/Failure) and logs the output for review.

## Repository Structure

* **api/**: Python API source code.
* **configs/**: Configuration files (supervisord, etc.).
* **Containerfiles/**: Docker/Podman container definitions.
* **templates/**: Kickstart and configuration templates used during provisioning.
* **run_worker.sh**: Script to launch the RQ worker process.
* **Makefile**: Automation for building and deploying the project.
