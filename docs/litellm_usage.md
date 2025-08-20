# CAI-CERBERUS + LiteLLM Usage Guide

## Quick Start

1. **Start LiteLLM services:**
   ```bash
   make litellm-start
   ```

2. **Add your API keys to external-tools/litellm/.env:**
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Test the integration:**
   ```bash
   python examples/model_providers/cerberus_litellm_example.py
   ```

4. **Use with CAI-CERBERUS:**
   ```bash
   export CERBERUS_MODEL=litellm/gpt-4o-mini
   python -m cai.cli interactive
   ```

## Available Commands

- `make litellm-start` - Start LiteLLM services
- `make litellm-stop` - Stop LiteLLM services  
- `make litellm-logs` - View LiteLLM logs
- `make litellm-test` - Test integration

## Access URLs

- LiteLLM Proxy: http://localhost:4000
- LiteLLM UI: http://localhost:4000/ui
- Prometheus: http://localhost:9091

## Configuration

LiteLLM configuration is in `external-tools/litellm/config.yaml`
Environment variables are in `external-tools/litellm/.env`

## Troubleshooting

1. **Port conflicts:** Change ports in docker-compose.yml
2. **API key errors:** Add keys to .env file
3. **Container issues:** Run `docker-compose logs litellm`
