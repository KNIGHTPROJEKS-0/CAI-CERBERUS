# LiteLLM Integration for CAI-CERBERUS

LiteLLM provides a unified interface to 100+ LLM APIs with cost tracking, caching, and safety controls. This integration enables CAI-CERBERUS to use multiple model providers through a single, secure proxy.

## Features

- **Multi-Provider Support**: OpenAI, Anthropic, DeepSeek, Ollama, and 100+ providers
- **Cost Tracking**: Real-time spend monitoring and budget enforcement
- **Safety Controls**: Rate limiting, content filtering, and approval gates
- **Audit Logging**: Complete request/response logging for compliance
- **High Availability**: Automatic failover and load balancing
- **Caching**: Response caching to reduce costs and latency

## Quick Setup

### 1. Run Setup Script
```bash
cd external-tools/litellm
./setup.sh
```

This will:
- Generate secure keys and configuration
- Start LiteLLM proxy with PostgreSQL database
- Configure Prometheus monitoring
- Create audit logging structure

### 2. Add API Keys
Edit `.env` file and add your provider API keys:
```bash
# Provider API Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
DEEPSEEK_API_KEY="sk-..."
```

### 3. Test Integration
```bash
python test_integration.py
```

### 4. Configure CAI-CERBERUS
```bash
# In your main .env file
CERBERUS_MODEL="litellm/gpt-4o"
LITELLM_BASE_URL="http://localhost:4000"
LITELLM_MASTER_KEY="sk-cerberus-..."  # From setup.sh output
```

## Usage in Agents

### Basic Usage
```python
from tools.proxy.litellm_adapter import LiteLLMAdapter

async with LiteLLMAdapter(master_key="sk-cerberus-...") as adapter:
    # Check health
    health = await adapter.validate_proxy_health()
    print(f"Proxy healthy: {health['healthy']}")
    
    # Get available models
    models = await adapter.get_available_models()
    print(f"Available models: {len(models)}")
    
    # Send completion request
    response = await adapter.complete_chat(
        messages=[{"role": "user", "content": "Hello from CAI-CERBERUS"}],
        model="gpt-4o-mini"
    )
    print(response["choices"][0]["message"]["content"])
```

### With Safety Controls
```python
from tools.proxy.litellm_adapter import LiteLLMAdapter, SafetyConfig

safety_config = SafetyConfig(
    max_budget_per_request=5.0,
    max_tokens_per_request=2000,
    rate_limit_per_minute=30
)

async with LiteLLMAdapter(safety_config=safety_config) as adapter:
    # Cost estimation
    cost = await adapter.get_cost_estimate(
        messages=[{"role": "user", "content": "Complex analysis task..."}],
        model="gpt-4o"
    )
    
    if cost["estimated_cost_usd"] > 1.0:
        print(f"High cost request: ${cost['estimated_cost_usd']:.4f}")
        # Request human approval
    
    # Budget checking
    budget_check = await adapter.check_budget_limit(100.0)
    if not budget_check["within_budget"]:
        print("Budget limit exceeded!")
        return
    
    # Safe completion
    response = await adapter.complete_chat(messages, model="gpt-4o")
```

## Configuration

### Model Configuration (`config.yaml`)
```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      
  - model_name: claude-3-5-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  max_budget: 1000.0
  budget_duration: 30d
```

### Safety Configuration
```python
safety_config = SafetyConfig(
    max_budget_per_request=10.0,      # Max $10 per request
    max_tokens_per_request=4000,      # Max 4K tokens
    require_approval_over=5.0,        # Approval for >$5 requests
    rate_limit_per_minute=60,         # 60 requests/minute
    blocked_content_types=["harmful", "illegal"]
)
```

## Monitoring and Observability

### Access Points
- **LiteLLM UI**: http://localhost:4000/ui
- **Prometheus**: http://localhost:9090
- **Health Check**: http://localhost:4000/health

### Audit Logs
All requests are logged to `logs/litellm_audit.jsonl`:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "event_type": "chat_completion_success",
  "data": {
    "model": "gpt-4o-mini",
    "response_time_ms": 1250,
    "usage": {"prompt_tokens": 50, "completion_tokens": 100},
    "cost_usd": 0.0045
  }
}
```

### Cost Tracking
```python
# Get usage statistics
stats = await adapter.get_usage_stats()
print(f"Total spend: ${stats['total_spend']:.2f}")

# Check budget limits
budget = await adapter.check_budget_limit(100.0)
print(f"Remaining budget: ${budget['remaining_budget']:.2f}")
```

## Security Features

### Authentication
- Master key authentication for all requests
- Per-user API key management
- Role-based access control

### Rate Limiting
- Configurable requests per minute
- Per-user and per-key limits
- Automatic throttling and queuing

### Content Safety
- Keyword-based content filtering
- Integration with safety providers
- Human approval gates for sensitive requests

### Audit and Compliance
- Complete request/response logging
- Cost tracking and budget enforcement
- Compliance reporting capabilities

## Troubleshooting

### Common Issues

1. **Proxy not starting**
   ```bash
   docker-compose logs litellm
   # Check for API key or configuration errors
   ```

2. **Authentication errors**
   ```bash
   # Verify master key in .env file
   grep LITELLM_MASTER_KEY .env
   ```

3. **Model not available**
   ```bash
   # Check model configuration
   curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
        http://localhost:4000/v1/models
   ```

4. **High costs**
   ```bash
   # Check usage statistics
   curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
        http://localhost:4000/spend
   ```

### Health Checks
```python
# Comprehensive health check
health = await adapter.validate_proxy_health()
if not health["healthy"]:
    print(f"Proxy unhealthy: {health['error']}")
```

### Log Analysis
```bash
# View recent audit logs
tail -f logs/litellm_audit.jsonl | jq .

# Check for errors
grep "error" logs/litellm_audit.jsonl | jq .
```

## Advanced Configuration

### Custom Routing
```yaml
router_settings:
  routing_strategy: "least-busy"
  model_group_alias:
    gpt-4: ["gpt-4o", "gpt-4o-mini"]
    claude: ["claude-3-5-sonnet"]
```

### Caching
```yaml
general_settings:
  cache:
    type: "redis"
    host: "localhost"
    port: 6379
    ttl: 3600
```

### Guardrails
```yaml
guardrails:
  - guardrail_name: "cerberus_safety"
    litellm_params:
      guardrail: presidio
      mode: "during_call"
```

## Integration with CAI-CERBERUS

### Agent Configuration
```yaml
# configs/agents/litellm_agent.yaml
name: "LiteLLM Agent"
role: "model_proxy"
tools:
  - name: "litellm_adapter"
    path: "tools.proxy.litellm_adapter.LiteLLMAdapter"
constraints:
  max_budget: 50.0
  require_approval: true
```

### Environment Variables
```bash
# Main CAI-CERBERUS configuration
CERBERUS_MODEL="litellm/gpt-4o"
LITELLM_BASE_URL="http://localhost:4000"
LITELLM_MASTER_KEY="sk-cerberus-..."

# Cost controls
CERBERUS_PRICE_LIMIT="100.0"
CERBERUS_MAX_ITERATIONS="50"
```

## Support and Documentation

- **LiteLLM Docs**: https://docs.litellm.ai
- **CAI-CERBERUS Docs**: ../../../docs/
- **Issues**: Report integration issues in the main repository
- **Configuration**: See `config.yaml` and `.env.example` for all options