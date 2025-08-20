# Docker Offload - Comprehensive Guide for CAI-CERBERUS

> **IMPORTANT FOR LLMs/AGENTS**: This document provides complete Docker Offload guidance for AI agents and LLMs working with CAI-CERBERUS or similar agentic AI frameworks. Use this as your primary reference for all Docker Offload operations, configuration, and troubleshooting.

## Table of Contents

1. [About Docker Offload](#about-docker-offload)
2. [Docker Pro Setup](#docker-pro-setup)
3. [Quickstart Guide](#quickstart-guide)
4. [Configuration](#configuration)
5. [Usage and Optimization](#usage-and-optimization)
6. [Agentic AI Applications](#agentic-ai-applications)
7. [AI Models in Compose](#ai-models-in-compose)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices for AI Agents](#best-practices-for-ai-agents)

---

## About Docker Offload

Docker Offload is a fully managed service for building and running containers in the cloud using the Docker tools you already know, including Docker Desktop, the Docker CLI, and Docker Compose. It extends your local development workflow into a scalable, cloud-powered environment, so you can offload compute-heavy tasks, accelerate builds, and securely manage container workloads across the software lifecycle.

### Key Features

Docker Offload includes the following capabilities to support modern container workflows:

- **Cloud-based builds**: Execute builds on remote, fully managed BuildKit instances
- **GPU acceleration**: Use NVIDIA L4 GPU-backed environments for machine learning, media processing, and other compute-intensive workloads
- **Ephemeral cloud runners**: Automatically provision and tear down cloud environments for each container session
- **Shared build cache**: Speed up build times across machines and teammates with a smart, shared cache layer
- **Hybrid workflows**: Seamlessly transition between local and remote execution using Docker Desktop or CLI
- **Secure communication**: Use encrypted tunnels between Docker Desktop and cloud environments with support for secure secrets and image pulling
- **Port forwarding and bind mounts**: Retain a local development experience even when running containers in the cloud
- **VDI-friendly**: Use Docker Offload in virtual desktop environments or systems that don't support nested virtualization

### Why Use Docker Offload?

Docker Offload is designed to support modern development teams working across local and cloud environments. It helps you:

- Offload heavy builds and runs to fast, scalable infrastructure
- Accelerate feedback loops in development and testing
- Run containers that require more resources than your local setup can provide
- Build and run AI apps with instant access to GPU-powered environments
- Use Docker Compose to manage complex, multi-service apps that need cloud resources
- Maintain consistent environments without managing custom infrastructure
- Develop efficiently in restricted or low-powered environments like VDIs

Docker Offload is ideal for high-velocity development workflows that need the flexibility of the cloud without sacrificing the simplicity of local tools.

### How Docker Offload Works

Docker Offload replaces the need to build or run containers locally by connecting Docker Desktop to secure, dedicated cloud resources.

#### Building with Docker Offload

When you use Docker Offload for builds, the `docker buildx build` command sends the build request to a remote BuildKit instance in the cloud, instead of executing it locally. Your workflow stays the same, only the execution environment changes.

The build runs on infrastructure provisioned and managed by Docker:

- Each cloud builder is an isolated Amazon EC2 instance with its own EBS volume
- Remote builders use a shared cache to speed up builds across machines and teammates
- Build results are encrypted in transit and sent to your specified destination (such as a registry or local image store)

Docker Offload manages the lifecycle of builders automatically. There's no need to provision or maintain infrastructure.

> **Note**: Docker Offload builders are currently hosted in the United States East region. Users in other regions may experience increased latency.

#### Running Containers with Docker Offload

When you use Docker Offload to run containers, Docker Desktop creates a secure SSH tunnel to a Docker daemon running in the cloud. Your containers are started and managed entirely in that remote environment.

Here's what happens:

1. Docker Desktop connects to the cloud and triggers container creation
2. Docker Offload pulls the required images and starts containers in the cloud
3. The connection stays open while the containers run
4. When the containers stop running, the environment shuts down and is cleaned up automatically

This setup avoids the overhead of running containers locally and enables fast, reliable containers even on low-powered machines, including machines that do not support nested virtualization. This makes Docker Offload ideal for developers using environments such as virtual desktops, cloud-hosted development machines, or older hardware.

Docker Offload also supports GPU-accelerated workloads. Containers that require GPU access can run on cloud instances provisioned with NVIDIA L4 GPUs for efficient AI inferencing, media processing, and general-purpose GPU acceleration. This enables compute-heavy workflows such as model evaluation, image processing, and hardware-accelerated CI tests to run seamlessly in the cloud.

Despite running remotely, features like bind mounts and port forwarding continue to work seamlessly, providing a local-like experience from within Docker Desktop and the CLI.

Docker Offload provisions an ephemeral cloud environment for each session. The environment remains active while you are interacting with Docker Desktop or actively using containers. If no activity is detected for about 5 minutes, the session shuts down automatically. This includes any containers, images, or volumes in that environment, which are deleted when the session ends.

---

## Docker Pro Setup

### Current Status

✅ **Docker Desktop**: Installed (v28.3.2)  
✅ **Docker Pro Account**: Active (knightprojekslancerr)  
✅ **Docker Offload Plugin**: Available (v0.4.11)  
⚠️ **Docker Offload**: Currently offline  

### Quick Setup

#### 1. Run the Setup Script

```bash
# Make executable and run
chmod +x docker-setup.sh
./docker-setup.sh
```

#### 2. Manual Docker Offload Setup

If the automatic setup doesn't work, follow these steps:

```bash
# Check your account status
docker offload accounts

# Start Docker Offload session
docker offload start --account knightprojekslancerr

# Check status
docker offload status

# If it fails, check diagnostics
docker offload diagnose
```

### Docker Pro Features Configuration

#### 1. Docker Desktop Settings

Open Docker Desktop → Settings → Resources:

- **Memory**: Set to 6-8 GB (you have 3.8GB currently allocated)
- **CPUs**: Use 6-8 cores (you have 8 available)
- **Disk**: Allocate 100GB+ for images and containers
- **Swap**: Enable with 2GB

#### 2. Enable Pro Features

In Docker Desktop → Settings → Features:

- ✅ **Docker Offload**: Enable cloud builds
- ✅ **Enhanced Container Isolation**: Better security
- ✅ **Image Access Management**: Control image access
- ✅ **Registry Access Management**: Secure registry access

#### 3. Build Acceleration

Configure BuildKit for faster builds:

```bash
# Enable BuildKit globally
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Add to your shell profile
echo 'export DOCKER_BUILDKIT=1' >> ~/.zshrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.zshrc
```

---

## Quickstart Guide

This quickstart helps you get started with Docker Offload. Docker Offload lets you build and run container images faster by offloading resource-intensive tasks to the cloud. It provides a cloud-based environment that mirrors your local Docker Desktop experience.

### Step 1: Sign up and Subscribe to Docker Offload

To access Docker Offload, you must [sign up](https://www.docker.com/products/docker-offload/) and subscribe.

### Step 2: Start Docker Offload

> **Note**: After subscribing to Docker Offload, the first time you start Docker Desktop and sign in, you may be prompted to start Docker Offload. If you start Docker Offload via this prompt, you can skip the following steps. Note that you can use the following steps to start Docker Offload at any time.

1. Start Docker Desktop and sign in
2. Open a terminal and run the following command to start Docker Offload:

   ```console
   $ docker offload start
   ```

3. When prompted, select your account to use for Docker Offload. This account will consume credits for your Docker Offload usage

4. When prompted, select whether to enable GPU support. If you choose to enable GPU support, Docker Offload will run in an instance with an NVIDIA L4 GPU, which is useful for machine learning or compute-intensive workloads

   > **Note**: Enabling GPU support consumes more budget. For more details, see Docker Offload usage section below.

When Docker Offload is started, you'll see a cloud icon in the Docker Desktop Dashboard header, and the Docker Desktop Dashboard appears purple. You can run `docker offload status` in a terminal to check the status of Docker Offload.

### Step 3: Run a Container with Docker Offload

After starting Docker Offload, Docker Desktop connects to a secure cloud environment that mirrors your local experience. When you run builds or containers, they execute remotely, but behave just like local ones.

To verify that Docker Offload is working, run a container:

```console
$ docker run --rm hello-world
```

If you enabled GPU support, you can also run a GPU-enabled container:

```console
$ docker run --rm --gpus all hello-world
```

If Docker Offload is working, you'll see `Hello from Docker!` in the terminal output.

### Step 4: Stop Docker Offload

When you're done using Docker Offload, you can stop it. When stopped, you build images and run containers locally.

```console
$ docker offload stop
```

To start Docker Offload again, run the `docker offload start` command.

---

## Configuration

To use Docker Offload, you must start it in Docker Desktop. Settings for the cloud builders in Docker Offload can be further configured, in addition to settings for an entire organization, through **Offload settings** in the Docker Offload dashboard.

> **Note**: To view usage and configure billing for Docker Offload, see the Usage section below.

### Offload Settings

The **Offload settings** page in Docker Home lets you configure disk allocation, private resource access, and firewall settings for your cloud builders in your organization.

To view the **Offload settings** page:

1. Go to [Docker Home](https://app.docker.com/)
2. Select the account for which you want to manage Docker Offload
3. Select **Offload** > **Offload settings**

#### Disk Allocation

The **Disk allocation** setting lets you control how much of the available storage is dedicated to the build cache. A lower allocation increases storage available for active builds.

Adjust the **Disk allocation** slider to specify the percentage of storage used for build caching.

Any changes take effect immediately.

> **Tip**: If you build very large images, consider allocating less storage for caching.

#### Build Cache Space

Your subscription includes the following Build cache space:

| Subscription | Build cache space |
| ------------ | ----------------- |
| Personal     | N/A               |
| Pro          | 50GB              |
| Team         | 100GB             |
| Business     | 200GB             |

To get more Build cache space, upgrade your subscription.

#### Private Resource Access

Private resource access lets cloud builders pull images and packages from private resources. This feature is useful when builds rely on self-hosted artifact repositories or private OCI registries.

For example, if your organization hosts a private [PyPI](https://pypi.org/) repository on a private network, Docker Build Cloud would not be able to access it by default, since the cloud builder is not connected to your private network.

To enable your cloud builders to access your private resources, enter the host name and port of your private resource and then select **Add**.

##### Authentication

If your internal artifacts require authentication, make sure that you authenticate with the repository either before or during the build. For internal package repositories for npm or PyPI, use build secrets to authenticate during the build. For internal OCI registries, use `docker login` to authenticate before building.

Note that if you use a private registry that requires authentication, you will need to authenticate with `docker login` twice before building. This is because the cloud builder needs to authenticate with Docker to use the cloud builder, and then again to authenticate with the private registry.

```console
$ echo $DOCKER_PAT | docker login docker.io -u <username> --password-stdin
$ echo $REGISTRY_PASSWORD | docker login registry.example.com -u <username> --password-stdin
$ docker build --builder <cloud-builder> --tag registry.example.com/<image> --push .
```

#### Firewall

Firewall settings let you restrict cloud builder egress traffic to specific IP addresses. This helps enhance security by limiting external network egress from the builder.

1. Select **Enable firewall: Restrict cloud builder egress to specific public IP address**
2. Enter the IP address you want to allow
3. Select **Add** to apply the restriction

---

## Usage and Optimization

Docker Offload runs your builds remotely, not on the machine where you invoke the build. This means that files must be transferred from your local system to the cloud over the network.

Transferring files over the network introduces higher latency and lower bandwidth compared to local transfers. To reduce these effects, Docker Offload includes several performance optimizations:

- It uses attached storage volumes for build cache, which makes reading and writing cache fast
- When pulling build results back to your local machine, it only transfers layers that changed since the previous build

Even with these optimizations, large projects or slower network connections can lead to longer transfer times. Here are several ways to optimize your build setup for Docker Offload:

### dockerignore Files

A `.dockerignore` file lets you specify which local files should *not* be included in the build context. Files excluded by these patterns won't be uploaded to Docker Offload during a build.

Typical items to ignore:

- `.git` – avoids transferring your version history. (Note: you won't be able to run `git` commands in the build.)
- Build artifacts or locally generated binaries
- Dependency folders such as `node_modules`, if those are restored in the build process

As a rule of thumb, your `.dockerignore` should be similar to your `.gitignore`.

### Slim Base Images

Smaller base images in your `FROM` instructions can reduce final image size and improve build performance. The [`alpine`](https://hub.docker.com/_/alpine) image is a good example of a minimal base.

For fully static binaries, you can use [`scratch`](https://hub.docker.com/_/scratch), which is an empty base image.

### Multi-stage Builds

Multi-stage builds let you separate build-time and runtime environments in your Dockerfile. This not only reduces the size of the final image but also allows for parallel stage execution during the build.

Use `COPY --from` to copy files from earlier stages or external images. This approach helps minimize unnecessary layers and reduce final image size.

### Fetch Remote Files in Build

When possible, download large files from the internet during the build itself instead of bundling them in your local context. This avoids network transfer from your client to Docker Offload.

You can do this using:

- The Dockerfile `ADD` instruction
- `RUN` commands like `wget`, `curl`, or `rsync`

### Multi-threaded Tools

Some build tools, such as `make`, are single-threaded by default. If the tool supports it, configure it to run in parallel. For example, use `make --jobs=4` to run four jobs simultaneously.

Taking advantage of available CPU resources in the cloud can significantly improve build time.

---

## Agentic AI Applications

Agentic applications are transforming how software gets built. These apps don't just respond, they decide, plan, and act. They're powered by models, orchestrated by agents, and integrated with APIs, tools, and services in real time.

All these new agentic applications, no matter what they do, share a common architecture. It's a new kind of stack, built from three core components:

- **Models**: These are your GPTs, CodeLlamas, Mistrals. They're doing the reasoning, writing, and planning. They're the engine behind the intelligence
- **Agent**: This is where the logic lives. Agents take a goal, break it down, and figure out how to get it done. They orchestrate everything. They talk to the UI, the tools, the model, and the gateway
- **MCP gateway**: This is what links your agents to the outside world, including APIs, tools, and services. It provides a standard way for agents to call capabilities via the Model Context Protocol (MCP)

Docker makes this AI-powered stack simpler, faster, and more secure by unifying models, tool gateways, and cloud infrastructure into a developer-friendly workflow that uses Docker Compose.

### Docker AI Tools for Agentic Applications

This guide walks you through the core components of agentic development and shows how Docker ties them all together with the following tools:

- **Docker Model Runner** lets you run LLMs locally with simple command and OpenAI-compatible APIs
- **Docker MCP Catalog and Toolkit** helps you discover and securely run external tools, like APIs and databases, using the Model Context Protocol (MCP)
- **Docker MCP Gateway** lets you orchestrate and manage MCP servers
- **Docker Offload** provides a powerful, GPU-accelerated environment to run your AI applications with the same Compose-based workflow you use locally
- **Docker Compose** is the tool that ties it all together, letting you define and run multi-container applications with a single file

### Running Agentic AI with Docker Offload

For agentic AI applications, you'll start by running the app in Docker Offload, using the same Compose workflow you're already familiar with. Then, if your machine hardware supports it, you'll run the same app locally using the same workflow.

#### Prerequisites for AI Applications

To follow agentic AI workflows with Docker Offload, you need to:

- Install Docker Desktop 4.43 or later
- Enable Docker Model Runner
- Join Docker Offload Beta

#### Sample Agentic Application Workflow

1. **Clone the sample application**:
   ```console
   $ git clone https://github.com/docker/compose-for-agents.git
   $ cd compose-for-agents/adk/
   ```

2. **Start Docker Offload**:
   ```console
   $ docker offload start
   ```
   When prompted, choose your account and select **Yes** for GPU support.

3. **Run the application**:
   ```console
   $ docker compose up
   ```

4. **Test the application**:
   Visit http://localhost:8080 and enter facts to verify using the AI agents.

5. **Stop when done**:
   ```console
   $ docker offload stop
   ```

### Architecture for Agentic AI

The agentic AI stack with Docker Offload focuses on coordination and execution with explicit control points and safety boundaries:

```
                    ┌─────────────────────────────────────────┐
                    │              HITL Layer                 │
                    │  ┌─────────────┐    ┌─────────────┐     │
                    │  │ Approval    │    │ Override    │     │
                    │  │ Gates       │    │ Controls    │     │
                    │  └─────────────┘    └─────────────┘     │
                    └─────────────┬───────────────────────────┘
                                  │
                                  ▼
┌─────────────┐    ┌─────────────────────────────────────────┐    ┌─────────────┐
│   Memory    │◀──►│           Agent Orchestration           │◀──►│   Tracing   │
│             │    │                                         │    │             │
│ • Session   │    │  ┌───────────┐  ┌───────────┐  ┌──────┐ │    │ • Execution │
│ • Episodic  │    │  │ Patterns  │  │ Handoffs  │  │Agents│ │    │ • Metrics   │
│ • Semantic  │    │  │           │  │           │  │      │ │    │ • Audit     │
│ • Workspace │    │  │ • Hierarchy│  │ • Validate│  │• Role│ │    │ • Errors    │
└─────────────┘    │  │ • Swarm   │  │ • Transfer│  │• Cap │ │    └─────────────┘
                   │  │ • Chain   │  │ • Approve │  │• Ctx │ │
                   │  │ • Auction │  │ • Rollback│  │• Lim │ │
                   │  └───────────┘  └───────────┘  └──────┘ │
                   └─────────────┬───────────────────────────┘
                                 │
                                 ▼
                   ┌─────────────────────────────────────────┐
                   │              Tool Layer                 │
                   │                                         │
                   │ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
                   │ │   CLI   │ │  OSINT  │ │ Network │     │
                   │ │ • Exec  │ │ • Search│ │ • Scan  │     │
                   │ │ • Valid │ │ • Gather│ │ • Probe │     │
                   │ └─────────┘ └─────────┘ └─────────┘     │
                   │                                         │
                   │ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
                   │ │  Code   │ │ Custom  │ │ Agent   │     │
                   │ │ • Gen   │ │ • Adapt │ │ • Tool  │     │
                   │ │ • Exec  │ │ • Extend│ │ • Proxy │     │
                   │ └─────────┘ └─────────┘ └─────────┘     │
                   └─────────────────────────────────────────┘
```

---

### AI Models in Compose

This project now supports local GGUF models via llama-cpp-python with OpenAI-compatible endpoints, complementing cloud-based and HF-hosted options.

Key options:
- llama-cpp-python (local): Fast, Metal-accelerated serving on macOS
- WhiteRabbitNeo via LiteLLM/HF (remote): Cloud/OpenAI-compatible endpoint
- Transformers (direct): Python in-process for experimentation

Recommended patterns:
- Keep local model servers isolated (Conda env) and expose via HTTP
- Point CAI-CERBERUS to these endpoints using base_url and API mappings
- Use docker-compose for non-macOS GPU setups or when centralizing services

Docker Compose supports defining and using AI models in your applications using the `models` top-level element. This allows you to easily integrate AI models into your containerized applications.

Example: Local llama-cpp-python model (OpenAI-compatible)

```yaml
models:
  local-llama:
    type: openai-compatible
    # If you run llama-cpp-python natively on macOS (Metal), point to host.docker.internal
    url: http://host.docker.internal:8080/v1
    # Optional: If you run llama-cpp in a container, replace url with the container service name
    # url: http://llama-cpp:8080/v1
    # No API key required for local by default, but you can set one via server flags if desired
    # api_key: ${LLAMACPP_API_KEY}
```

Running llama-cpp-python inside Compose (Linux/CPU/GPU):

- For macOS with Metal, prefer native execution using make llama.setup and make llama.start
- For Linux with CUDA or CPU-only scenarios, you can run a containerized server and expose port 8080
- Make sure to mount your GGUF models into the container

Environment and networking notes:
- Use host.docker.internal to access a server running on the host from containers
- Keep the Conda env isolated for native runs; containers remain separate from host env
- Expose the base URL to CAI-CERBERUS via LLAMACPP_API_BASE and map it in your clients

### Basic Model Definition

```yaml
services:
  app:
    build: .
    models:
      my-model:
        endpoint_var: MODEL_ENDPOINT
        model_var: MODEL_NAME

models:
  my-model:
    model: ai/gemma3:4B-Q4_0
    context_size: 10000
```

### Model Configuration Options

The `models` element supports various configuration options:

- **model**: The model identifier (e.g., `ai/gemma3:4B-Q4_0`)
- **context_size**: The context window size for the model
- **endpoint_var**: Environment variable name for the model endpoint
- **model_var**: Environment variable name for the model identifier

### Integration with CAI-CERBERUS

```yaml
services:
  cerberus-agent:
    build:
      context: .
    ports:
      - "8080:8080"
    environment:
      - MCPGATEWAY_ENDPOINT=http://mcp-gateway:8811/sse
      - USE_DOCKER_OFFLOAD=true
      - GPU_REQUIRED=false
    depends_on:
      - mcp-gateway
    models:
      gemma3:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  mcp-gateway:
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      - --servers=duckduckgo,metabigor

models:
  gemma3:
    model: ai/gemma3:4B-Q4_0
    context_size: 10000  # 3.5 GB VRAM
```

---

## Troubleshooting

Docker Offload requires:

- Authentication
- An active internet connection
- No restrictive proxy or firewall blocking traffic to Docker Cloud
- Beta access to Docker Offload
- Docker Desktop 4.43 or later

Docker Desktop uses Offload to run both builds and containers in the cloud. If builds or containers are failing to run, falling back to local, or reporting session errors, use the following steps to help resolve the issue.

### Troubleshooting Steps

1. **Ensure Docker Offload is enabled in Docker Desktop**:
   1. Open Docker Desktop and sign in
   2. Go to **Settings** > **Beta features**
   3. Ensure that **Docker Offload** is checked

2. **Check connection status**:
   ```console
   $ docker offload status
   ```

3. **Get detailed diagnostics**:
   ```console
   $ docker offload diagnose
   ```

4. **Start a new session if not connected**:
   ```console
   $ docker offload start
   ```

5. **Verify authentication**:
   ```console
   $ docker login
   ```

6. **If needed, sign out and sign in again**:
   ```console
   $ docker logout
   $ docker login
   ```

7. **Verify your usage and billing** in the Docker Dashboard

### Common Issues and Solutions

#### Connection Issues
- Ensure stable internet connection
- Check firewall settings aren't blocking Docker Cloud
- Verify Docker Desktop is signed in with correct account

#### Build Failures
- Check `.dockerignore` file for excessive exclusions
- Verify base images are accessible
- Ensure private registries are properly authenticated

#### Performance Issues
- Optimize Dockerfile with multi-stage builds
- Use slim base images
- Implement proper caching strategies
- Consider disk allocation settings

#### GPU Issues
- Ensure GPU support was enabled during setup
- Verify workload actually requires GPU
- Check GPU-specific container requirements

---

## Best Practices for AI Agents

When working with Docker Offload in agentic AI frameworks like CAI-CERBERUS, follow these operational patterns:

### Agent Initialization with Docker Offload

```python
# Always initialize with clear role and constraints
agent = Agent(
    role="reconnaissance|analysis|execution|validation",
    capabilities=["tool1", "tool2"],
    constraints={
        "max_iterations": 10,
        "require_approval": True,
        "allowed_targets": ["example.com"],
        "blocked_actions": ["destructive_commands"],
        "use_offload": True,  # Enable cloud execution
        "gpu_required": False  # Set based on workload
    }
)
```

### Docker Offload Task Execution Pattern

```python
# Follow the standard execution pattern with Offload
async def execute_task_with_offload(task, context):
    # 1. Start Docker Offload if not already running
    if not await check_offload_status():
        await start_offload(gpu_support=task.requires_gpu)
    
    # 2. Validate task and permissions
    if not validate_permissions(task, context):
        return await request_approval(task)
    
    # 3. Plan execution steps
    plan = await create_execution_plan(task)
    
    # 4. Execute with checkpoints in cloud
    for step in plan:
        result = await execute_step_offload(step)
        await log_step_result(step, result)
        
        # Check for human intervention
        if requires_approval(step):
            await request_human_approval(step, result)
    
    # 5. Validate and return results
    return await validate_results(results)
```

### Docker Compose Configuration for Agents

```yaml
# CAI-CERBERUS with WhiteRabbitNeo and Docker Offload
services:
  cai-cerberus:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - USE_DOCKER_OFFLOAD=true
      - GPU_REQUIRED=false
      - TRANSFORMERS_CACHE=/app/models
      - CODE_FUNCTIONS_ENABLED=true
    volumes:
      - ./external-tools/datasets:/app/external-tools/datasets
      - ./models:/app/models
    depends_on:
      - whiterabbitneo
      - n8n
    models:
      whiterabbitneo:
        endpoint_var: WHITERABBITNEO_API_BASE
        model_var: WHITERABBITNEO_MODEL

  whiterabbitneo:
    image: huggingface/text-generation-inference:latest
    ports:
      - "8080:80"
    environment:
      - MODEL_ID=WhiteRabbitNeo/WhiteRabbitNeo-13B-v1
      - TRUST_REMOTE_CODE=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=cerberus2024

models:
  whiterabbitneo:
    model: WhiteRabbitNeo/WhiteRabbitNeo-13B-v1
    context_size: 4096
```

### Safety Protocols with Docker Offload

- **Always validate** Docker Offload status before execution
- **Monitor costs** and set appropriate limits
- **Use GPU instances** only when necessary
- **Implement timeouts** for cloud operations
- **Log all cloud executions** for audit trail
- **Handle network failures** gracefully with fallback to local
- **Secure credentials** using Docker secrets

### Performance Optimization for AI Workloads

1. **Model Caching**: Use Docker Offload's shared cache for model layers
2. **Batch Operations**: Group multiple AI tasks to minimize session overhead
3. **Resource Matching**: Use GPU instances only for compute-intensive tasks
4. **Network Optimization**: Minimize data transfer with proper .dockerignore
5. **Session Management**: Keep sessions active during multi-step workflows

### Monitoring and Observability

```python
# Monitor Docker Offload usage in agents
async def monitor_offload_usage():
    status = await get_offload_status()
    metrics = {
        "session_active": status.active,
        "gpu_enabled": status.gpu_support,
        "build_cache_usage": status.cache_usage,
        "estimated_cost": status.estimated_cost
    }
    await log_metrics("docker_offload", metrics)
    return metrics
```

### Error Handling and Fallback

```python
# Implement fallback to local execution
async def execute_with_fallback(task):
    try:
        # Try Docker Offload first
        if await is_offload_available():
            return await execute_with_offload(task)
    except OffloadError as e:
        logger.warning(f"Offload failed: {e}, falling back to local")
        
    # Fallback to local execution
    return await execute_locally(task)
```

### Integration with CAI-CERBERUS

When using Docker Offload with CAI-CERBERUS:

1. **Configure in cerberus.yaml**:
   ```yaml
   docker:
     offload:
       enabled: true
       gpu_support: false
       auto_start: true
       fallback_local: true
   ```

2. **Use in agent definitions**:
   ```python
   from caicerberus import CerberusFramework
   
   cerberus = CerberusFramework(
       model="openai/gpt-4o",
       workspace="offload-test",
       docker_offload=True,
       gpu_required=False
   )
   ```

3. **Monitor in workflows**:
   ```python
   # Check Offload status in CERBERUS workflows
   if cerberus.docker_offload_enabled:
       await cerberus.monitor_offload_usage()
   ```

### CAI-CERBERUS Docker Integration

#### Framework Initialization

```bash
# Initialize CAI-CERBERUS with integrated environment
cd CAI-CERBERUS
source cai_env/bin/activate  # Activate integrated virtual environment
cai --init                   # Initialize workspace and configuration

# Verify integration
cai --version               # Shows framework status and venv integration
echo $NMAP_PATH            # Verify tool paths are loaded
echo $NUCLEI_PATH          # All 7 security tools configured
```

#### Environment Configuration

```bash
# Docker Offload environment variables for CAI-CERBERUS
CERBERUS_DOCKER_OFFLOAD=true
CERBERUS_GPU_REQUIRED=false
CERBERUS_OFFLOAD_ACCOUNT=knightprojekslancerr
CERBERUS_FALLBACK_LOCAL=true

# WhiteRabbitNeo Configuration (Primary Model)
CERBERUS_MODEL=WhiteRabbitNeo/WhiteRabbitNeo-13B-v1
WHITERABBITNEO_MODEL=WhiteRabbitNeo/WhiteRabbitNeo-13B-v1
WHITERABBITNEO_API_BASE=http://localhost:8080
WHITERABBITNEO_GPU_MEMORY=12GB

# Integrated Virtual Environment
CERBERUS_WORKSPACE=CERBERUS
CERBERUS_WORKSPACE_DIR=./workspaces/CERBERUS
CERBERUS_VENV_PATH=./cai_env

# External Security Tools (All 7 Integrated)
NMAP_PATH=./external-tools/reconnaissance/nmap
NUCLEI_PATH=./external-tools/vulnerability/nuclei
SUBFINDER_PATH=./external-tools/reconnaissance/subfinder
AMASS_PATH=./external-tools/reconnaissance/Amass
SQLMAP_PATH=./external-tools/vulnerability/sqlmap
REDEYE_PATH=./external-tools/reconnaissance/RedEye
METABIGOR_PATH=./external-tools/reconnaissance/metabigor

# Code Functions Configuration
CODE_FUNCTIONS_ENABLED=true
CODE_FUNCTIONS_CYBER_PATH=./external-tools/datasets/Code-Functions-Level-Cyber
CODE_FUNCTIONS_GENERAL_PATH=./external-tools/datasets/Code-Functions-Level-General

# N8N Workflow Integration
N8N_WEBHOOK_URL=https://primary-production-7050.up.railway.app/webhook/cerberus
N8N_USER=knightprojeks@gmail.com
N8N_PASSWORD=Ggg123456789ggG!
```

#### Agent Operation Patterns

```python
# CAI-CERBERUS agent with integrated environment and Docker Offload
from cai_cerberus import CerberusFramework, Agent, EnvironmentBridge

# Initialize framework with integrated virtual environment
framework = CerberusFramework(workspace="CERBERUS")
framework.initialize()  # Activates cai_env and loads all configurations

# Verify integration status
venv_status = framework.get_venv_status()
print(f"Virtual Environment: {'Active' if venv_status['activated'] else 'Inactive'}")
print(f"Tool Paths Loaded: {len([k for k in framework.config.keys() if k.endswith('_PATH')])} tools")

# Create WhiteRabbitNeo agent with full tool integration
agent = Agent(
    name="whiterabbitneo_agent",
    model="WhiteRabbitNeo/WhiteRabbitNeo-13B-v1"
)

# Access integrated tool paths
nmap_path = framework.get_tool_path("nmap")
nuclei_path = framework.get_tool_path("nuclei")
metabigor_path = framework.get_tool_path("metabigor")

# Execute with Docker Offload support
class CerberusAgent(Agent):
    def __init__(self, framework, **kwargs):
        super().__init__(**kwargs)
        self.framework = framework
        self.docker_offload_enabled = framework.config.get('CERBERUS_DOCKER_OFFLOAD', 'false').lower() == 'true'
    
    async def execute_task(self, task):
        if self.docker_offload_enabled:
            return await self.execute_with_offload(task)
        else:
            return await self.execute_locally(task)
```

This comprehensive guide provides everything needed for LLMs and AI agents to effectively use Docker Offload with agentic AI frameworks, ensuring optimal performance, cost management, and reliable execution in cloud environments.