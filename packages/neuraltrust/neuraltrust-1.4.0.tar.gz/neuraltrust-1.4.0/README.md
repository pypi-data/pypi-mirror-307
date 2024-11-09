# NeuralTrust Python SDK

The NeuralTrust Python SDK provides a convenient way to interact with the NeuralTrust API for tracing, evaluation sets, knowledge bases, and testsets.

## Installation

You can install the NeuralTrust Python SDK using pip:

```bash
pip install neuraltrust
```

## Usage

To use the NeuralTrust Python SDK, you need to initialize the client with your API key:

```python
from neuraltrust import NeuralTrust

# Initialize the client with your API key
client = NeuralTrust(api_key="your_api_key_here")

# Optionally, you can specify a custom base URL and SDK version
client = NeuralTrust(api_key="your_api_key_here", base_url="https://custom.api.url", sdk_version="v2")
```

### Basic Trace Usage

The SDK supports various types of events that can be sent during tracing. Here are the different event types and their usage:

### Traces

The SDK supports various event types:
- MESSAGE
- TOOL
- AGENT
- RETRIEVAL
- GENERATION
- ROUTER
- SYSTEM
- CUSTOM (event)
- FEEDBACK

All event types except MESSAGE require a parent_id.

### Creating Traces

The SDK supports both nested and non-nested trace creation:

#### Nested Approach (Recommended)
```python
from neuraltrust import EventType, FeedbackTag

# Initialize client
client = NeuralTrust(api_key="your-api-key")

# Create a root trace and message
trace = client.trace(
    conversation_id="conversation_12345678", 
    session_id="session_12345678", 
    channel_id="channel_12345678", 
    user=User(id="user_12345678", name="John Doe"), 
    metadata=Metadata(id="metadata_12345678", name="John Doe"), 
    custom={"key": "value"}
)
message = trace.message("User input: Hello!")

# Create nested traces (parent_id is handled automatically)
tool = message.tool("Processing request...")
tool.end("Request processed")

# Create deeper nested traces
agent = tool.agent("Agent working...")
agent.end("Task completed")

# Example of a complete conversation flow
trace = client.trace()
message = trace.message("What's the weather?")
router = message.router("Routing to weather service")
retrieval = router.retrieval("Fetching weather data")
retrieval.end("Found current weather")
generation = retrieval.generation("Generating response")
generation.end("It's sunny and 75°F")
message.end("The weather is sunny and 75°F")
```

#### Non-nested Approach (Using explicit parent_id)
```python
# Create a root trace
trace = client.trace(
    conversation_id="conversation_12345678", 
    session_id="session_12345678", 
    channel_id="channel_12345678", 
    user=User(id="user_12345678", name="John Doe"), 
    metadata=Metadata(id="metadata_12345678", name="John Doe"), 
    custom={"key": "value"}
)

# Create a message trace
message = trace.message("User input: Hello!")
message.end("Assistant: Hi there!")

# Create child traces with explicit parent_id
tool_trace = trace.tool("Processing request...", parent_id=message.trace_id)
tool_trace.end("Request processed")

# Create another child trace referencing the tool trace
agent_trace = trace.agent("Agent working...", parent_id=tool_trace.trace_id)
agent_trace.end("Task completed")

# Example of a complete flow with explicit parent_id
message = trace.message("What's the weather?")
router = trace.router("Routing to weather service", parent_id=message.trace_id)
retrieval = trace.retrieval("Fetching weather data", parent_id=router.trace_id)
retrieval.end("Found current weather")
generation = trace.generation("Generating response", parent_id=retrieval.trace_id)
generation.end("It's sunny and 75°F")
message.end("The weather is sunny and 75°F")

# Add feedback with explicit parent_id
feedback = trace.feedback(
    feedback_tag=FeedbackTag.POSITIVE,
    feedback_text="Accurate weather report",
    parent_id=message.trace_id
)
```

Each trace method automatically generates a unique trace_id that can be used as parent_id for child traces. While both approaches are valid, the nested approach is recommended for better readability and maintainability.

### Using the Send Method

The send method provides a more direct way to create traces:

```python
trace = client.trace(
    conversation_id="conversation_12345678", 
    session_id="session_12345678", 
    channel_id="channel_12345678", 
    user=User(id="user_12345678", name="John Doe"), 
    metadata=Metadata(id="metadata_12345678", name="John Doe"), 
    custom={"key": "value"}
)
# Message trace (no parent required)
message = trace.send(
    event_type=EventType.MESSAGE,
    input="Hello",
    output="Hi there"
)

# Other event types (require parent_id)
tool = trace.send(
    event_type=EventType.TOOL,
    input="Processing",
    output="Done",
    parent_id=message.trace_id
)
```

### Trace Properties

Each trace has the following properties:
- `trace_id`: Unique identifier for the trace
- `interaction_id`: ID that can be shared across related traces
- `parent_id`: ID of the parent trace (required for all types except MESSAGE)
- `conversation_id`: ID for grouping traces in a conversation
- `session_id`: Optional session identifier
- `channel_id`: Optional channel identifier


### Evaluation Sets

```python
# Run evaluation set
eval_set = client.run_evaluation_set(id="eval_set_id")

# Create an evaluation set
eval_set = client.create_evaluation_set(name="My Eval Set", description="A test evaluation set")

# Get an evaluation set
eval_set = client.get_evaluation_set(id="eval_set_id")

# Delete an evaluation set
client.delete_evaluation_set(id="eval_set_id")
```

### Knowledge Bases

```python
# Create a knowledge base
kb = client.create_knowledge_base(type="upstash", credentials={"api_key": "your_doc_api_key"})

# Get a knowledge base
kb = client.get_knowledge_base(id="kb_id")

# Delete a knowledge base
client.delete_knowledge_base(id="kb_id")
```

### Testsets

```python
# Create a testset
testset = client.create_testset(name="My Testset", type="adversarial", evaluation_set_id="eval_set_id", knowledge_base_id="kb_id", num_questions=10)

# Get a testset
testset = client.get_testset(id="testset_id")

# Delete a testset
client.delete_testset(id="testset_id")
```

## Configuration

You can configure the SDK using environment variables:

- `NEURALTRUST_API_KEY`: Your NeuralTrust API key
- `NEURALTRUST_BASE_URL`: Custom base URL for the API (optional)

## Advanced Usage

### Custom Metadata and User Information

```python
from neuraltrust import User, Metadata

user = User(id="user123", name="John Doe")
metadata = Metadata(app_version="1.0.0", platform="web")

trace = client.trace(user=user, metadata=metadata)
```

### Asynchronous Tracing

The SDK uses a `ThreadPoolExecutor` for asynchronous tracing. You can adjust the number of workers:

```python
client = NeuralTrust(api_key="your_api_key_here", max_workers=10)
```

## Error Handling

The SDK will raise exceptions for API errors. Make sure to handle these appropriately in your application.

## Contributing

Contributions to the NeuralTrust Python SDK are welcome! Please refer to the contribution guidelines for more information.

## License

This SDK is distributed under the [MIT License](LICENSE).