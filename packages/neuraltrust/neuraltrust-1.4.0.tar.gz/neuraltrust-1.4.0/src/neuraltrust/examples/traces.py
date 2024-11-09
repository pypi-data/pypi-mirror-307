from .. import NeuralTrust, User, Metadata, EventType
client = NeuralTrust(
    api_key="3bc2a769-87f6-45a1-9322-f963a7aca533:4954139f39642c62ebbb46e00f8c3db7e1b8229c1c183251ff97ab0b3711e780",
    base_url="https://api-prod.neuraltrust.ai"
)

trace = client.trace(
    conversation_id="conversation_12345678", 
    session_id="session_12345678", 
    channel_id="channel_12345678", 
    user=User(id="user_12345678", name="John Doe"), 
    metadata=Metadata(id="metadata_12345678", name="John Doe"), 
    custom={"key": "value"}
)


message = trace.message(input="Hello, how are you?")

generation = message.generation(input="Hello, how are you?")
generation.end("I am fine, thank you!")

router = message.router(input="Hello, how are you?")

retrieval = router.retrieval(input="Hello, how are you?")
retrieval.end([{"chunk": "Hello, how are you?"}])

agent = retrieval.agent(input="Hello, how are you?")
agent.end("I am fine, thank you!")

message.end("I am fine, thank you!")





