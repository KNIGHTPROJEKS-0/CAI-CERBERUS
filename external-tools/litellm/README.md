# LiteLLM Proxy Integration

LiteLLM provides a unified API gateway for 100+ LLM providers with cost tracking, rate limiting, and observability.

## Quick Setup

```bash
# Clone LiteLLM
cd external-tools/litellm
git clone https://github.com/BerriAI/litellm .

# Configure environment
echo 'LITELLM_MASTER_KEY="sk-cerberus-$(openssl rand -hex 16)"' > .env
echo 'LITELLM_SALT_KEY="$(openssl rand -hex 32)"' >> .env

# Start proxy
docker-compose up -d
```

## CAI-CERBERUS Integration

Update your `.env`:
```bash
# Use LiteLLM proxy instead of direct providers
CERBERUS_MODEL=gpt-4o
OPENAI_API_KEY=sk-cerberus-your-master-key
OPENAI_BASE_URL=http://localhost:4000

# Enable cost tracking
CERBERUS_PRICE_LIMIT=10.00
LITELLM_COST_TRACKING=true
```

## Benefits

- **Unified API**: Single interface for all providers
- **Cost Control**: Built-in budget limits and tracking
- **Rate Limiting**: Prevent API quota exhaustion
- **Caching**: Reduce costs for repeated queries
- **Load Balancing**: Distribute across multiple models
- **Observability**: Detailed usage analytics