> 🚧 **Disclaimer**
>
> The current MCP based implementation should be treated as temporary and exploratory. It's main purpose is to enable
> integration of various agents into the platform and to explore underlying protocols, transports and possible
> multi-agent
> patterns. In Q2 2025, we expect to rebuild the SDK from the ground up.

# Agent template

This is an example template for a python agent that can be used in the beeai platform.

To get started, click **Use this template** or fork this repository.

## Pre-requisites

- Python 3.11 or higher
- UV package manager: https://docs.astral.sh/uv/

## Implementing agent

1. Install dependencies using `uv sync`

2. Modify the source code in [src/beeai_agents/server.py](src/beeai_agents/server.py) to add your agent implementation
   in any agentic framework you like. You can add as many agents as you like.

## Running agents locally

You can experiment with the agents locally by running it directly:

```sh
uv run beeai-agents
```

You'll get an output similar to:

```
INFO:     Started server process [86448]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Your agents should now be started on http://localhost:8000, you can now list agents using the beeai CLI with a few extra
parameters:

```sh
env BEEAI__HOST=http://localhost:8000 \
  BEEAI__MCP_SSE_PATH='/sse' \
  beeai list
```

And run your agent:

```sh
env BEEAI__HOST=http://localhost:8000 \
  BEEAI__MCP_SSE_PATH='/sse' \
  beeai run example-agent "Your Name"
```

## Adding agents to the beeai platform

Now you may want to add your agents to your collection in beeai. You can do that locally or from GitHub in a
managed or unmanaged way. Let's break it down.

### Locally

The easiest way to add agents to beeai is to use a local provider manifest.
It might be useful especially during rapid agent development to keep the agent code locally and iterate quickly.
You have two options:

#### Add unmanaged agent

This means that you will have to run the agent server yourself, the platform will not attempt to start, stop or
configure it. You can add it in two simple steps:

1. Start the agent server - run the command `uv run beeai-agents` from before
2. Add provider manifest:
   ```sh
   beeai provider add file://beeai-provider-unmanaged.yaml
   ```

> Note: You will need to start the agent using `uv run beeai-agents` everytime you want to interact with the agent
> through the platform.

#### Add managed agent

This means that the beeai platform will manage the agent server process
(you won't have to run `uv run beeai-agents`, the platform will do it for you). All you need to do is to add the local
provider manifest:

   ```sh
   beeai provider add file://beeai-provider-local.yaml
   ```

The platform will register the server and run it automatically from now on.
> Note: If you want to update your code in a managed provider, you need to bump package version in `pyproject.toml`
> and then re-register the provider `beeai provider remove <ID>`, `beeai provider add file://beeai-provider-local.yaml`

### From GitHub

If you want to share your agent with others using the beeai platform, the easiest way is to use a GitHub link to
your repository you created with the template:

1. Modify [beeai-provider.yaml](beeai-provider.yaml) manifest with your repository url: `vim beeai-provider.yaml`
2. Add provider manifest:
   ```sh
   beeai provider add https://github.com/i-am-bee/beeai-agent-starter-py
   ```

> Note: To manage versions properly and prevent automatic updates or breaking changes we recommend creating a tag
> (for example `agents-v0.0.1` which you then use in [beeai-provider.yaml](beeai-provider.yaml)).
>   - To release new version - create a new tag and modify `beeai-provider.yaml`
>   - To update the agent in beeai you'll need to `beeai provider remove <ID>` and add it again.

## Troubleshooting

**How do I know the status of the agent provider?**

You can use `beeai provider list` to see whether the provider is initializing / ready or in an error state.
Use `beeai provider info <ID>` to get full error message. You can also inspect the beeai server logs for further
details.

**Changes to my agent are not propagated to the platform**

Make sure to bump `pyproject.toml`, any git tags that you use (e.g. `agents-v0.0.x`) and re-register the provider
using `beeai provider remove <ID>` and `beeai provider add <MANIFEST>`.