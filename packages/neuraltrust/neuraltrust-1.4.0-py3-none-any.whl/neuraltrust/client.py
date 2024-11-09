import typing
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import datetime as dt
from urllib.parse import urljoin
from .api_client import (
    NeuralTrustApi,
    TraceResponse,
    TraceTask,
    User,
    Metadata
)

OMIT = typing.cast(typing.Any, ...)

DEFAULT_BASE_URL = "https://api-prod.neuraltrust.ai"

class EventType(Enum):
    """Enum representing different types of events."""
    MESSAGE = "message"
    TOOL = "tool"
    AGENT = "agent"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    ROUTER = "router"
    SYSTEM = "system"
    CUSTOM = "event"
    FEEDBACK = "feedback"

class FeedbackTag(Enum):
    """Enum representing different types of feedback tags."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class NeuralTrust:
    base_client: NeuralTrustApi
    executor: ThreadPoolExecutor

    def __init__(
        self,
        api_key: typing.Union[str, None] = None,
        base_url: typing.Union[str, None] = None,
        sdk_version: typing.Union[str, None] = 'v1',
        timeout: typing.Union[float, None] = None,
        max_workers: typing.Union[int, None] = 5,
    ) -> None:
        
        if not api_key:
            api_key = os.environ.get("NEURALTRUST_API_KEY")
        
        if not base_url:
            base_url = os.environ.get("NEURALTRUST_BASE_URL") or DEFAULT_BASE_URL
        
        self.trace_executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Ensure the base_url is correctly formatted
        base_url = base_url.rstrip('/')
        full_url = f"{base_url}/{sdk_version}"
        
        self.base_client = NeuralTrustApi(
            api_key=api_key,
            base_url=full_url,
            timeout=timeout,
            follow_redirects=False,  # Explicitly disable following redirects
        )

    @property
    def api_key(self) -> typing.Union[str, None]:
        """Property getter for api_key."""
        return self.base_client._client_wrapper.api_key

    @api_key.setter
    def api_key(self, value: typing.Union[str, None]) -> None:
        """Property setter for api_key."""
        self.api_key = value
        if value is not None:
            self.base_client._client_wrapper.api_key = value

    @property
    def base_url(self) -> typing.Union[str, None]:
        """Property getter for base_url."""
        return self.base_client._client_wrapper._base_url

    @base_url.setter
    def base_url(self, value: typing.Union[str, None]) -> None:
        """Property setter for base_url."""
        if value is not None:
            self.base_client._client_wrapper._base_url = value

    def trace(self, trace_id: str = None, conversation_id: str = None, session_id: str = None, channel_id: str = None, user: User = None, metadata: Metadata = None, custom: dict = None):
        """
        Create a new Trace object.

        Args:
            conversation_id (str, optional): The conversation ID. If not provided, a new UUID will be generated.
            session_id (str, optional): The session ID.
            channel_id (str, optional): The channel ID.
            user (User, optional): The user associated with the trace.
            metadata (Metadata, optional): Additional metadata for the trace.
            custom (dict, optional): Custom data to include with the trace.

        Returns:
            Trace: A new Trace object.
        """
        return Trace(client=self, trace_id=trace_id, conversation_id=conversation_id, session_id=session_id, channel_id=channel_id, user=user, metadata=metadata, custom=custom)
    
    def _trace(
        self,
        *,
        type: typing.Optional[str] = OMIT,
        task: typing.Optional[TraceTask] = OMIT,
        input: typing.Optional[str] = OMIT,
        output: typing.Optional[str] = OMIT,
        feedback_tag: typing.Optional[FeedbackTag] = OMIT,
        feedback_text: typing.Optional[str] = OMIT,
        user: typing.Optional[User] = OMIT,
        metadata: typing.Optional[Metadata] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        channel_id: typing.Optional[str] = OMIT,
        conversation_id: typing.Optional[str] = OMIT,
        interaction_id: typing.Optional[str] = OMIT,
        parent_id: typing.Optional[str] = OMIT,
        trace_id: typing.Optional[str] = OMIT,
        latency: typing.Optional[int] = OMIT,
        start_timestamp: typing.Optional[int] = OMIT,
        end_timestamp: typing.Optional[int] = OMIT,
        custom: typing.Optional[str] = OMIT
    ) -> TraceResponse:
        """
        Internal method to send a trace to the API.

        Args:
            type (str, optional): The type of the trace.
            task (TraceTask, optional): The task associated with the trace.
            input (str, optional): The input data for the trace.
            output (str, optional): The output data for the trace.
            feedback_tag (FeedbackTag, optional): The feedback tag for the trace.
            feedback_text (str, optional): The feedback text for the trace.
            user (User, optional): The user associated with the trace.
            metadata (Metadata, optional): Additional metadata for the trace.
            session_id (str, optional): The session ID.
            channel_id (str, optional): The channel ID.
            conversation_id (str, optional): The conversation ID.
            interaction_id (str, optional): The interaction ID.
            parent_id (str, optional): The parent ID.
            trace_id (str, optional): The trace ID.
            latency (int, optional): The latency of the trace.
            start_timestamp (int, optional): The start timestamp of the trace.
            end_timestamp (int, optional): The end timestamp of the trace.
            custom (str, optional): Custom data to include with the trace.

        Returns:
            TraceResponse: The response from the API.

        Raises:
            ConnectionError: If there's a network connection error
            TimeoutError: If the request times out
            Exception: For other unexpected errors
        """
        try:
            return self.trace_executor.submit(
                self.base_client.trace.trace,
                type=type,
                task=task,
                input=input,
                output=output,
                feedback_tag=feedback_tag,
                feedback_text=feedback_text,
                user=user,
                metadata=metadata,
                session_id=session_id,
                channel_id=channel_id,
                conversation_id=conversation_id,
                interaction_id=interaction_id,
                parent_id=parent_id,
                trace_id=trace_id,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                latency=latency,
                custom=custom
            )
        except ConnectionError as e:
            print(f"Connection error while sending trace: {str(e)}")
            raise ConnectionError(f"Failed to connect to NeuralTrust API: {str(e)}")
        except TimeoutError as e:
            print(f"Timeout error while sending trace: {str(e)}")
            raise TimeoutError(f"Request to NeuralTrust API timed out: {str(e)}")
        except Exception as e:
            print(f"Unexpected error while sending trace: {str(e)}")
            raise Exception(f"Failed to send trace to NeuralTrust API: {str(e)}")

    def run_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.run_evaluation_set(id=id)
    
    def create_evaluation_set(self, name: str = None, description: str = None, scheduler: str = None):
        return self.base_client.evaluation_set.create_evaluation_set(name=name, description=description, scheduler=scheduler)
    
    def get_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.get_evaluation_set(id=id)
    
    def delete_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.delete_evaluation_set(id=id)
    
    def create_knowledge_base(self, type: str = None, credentials: dict = None, seed_topics: list = None):
        return self.base_client.knowledge_base.create_knowledge_base(type=type, credentials=credentials, seed_topics=seed_topics)

    def get_knowledge_base(self, id: str):
        return self.base_client.knowledge_base.get_knowledge_base(id=id)
    
    def delete_knowledge_base(self, id: str):
        return self.base_client.knowledge_base.delete_knowledge_base(id=id)
    
    def create_testset(self, name: str = None, type: str = None, evaluation_set_id: str = None, knowledge_base_id: str = None, num_questions: int = None):
        return self.base_client.testset.create_testset(name=name, type=type, evaluation_set_id=evaluation_set_id, knowledge_base_id=knowledge_base_id, num_questions=num_questions)

    def get_testset(self, id: str):
        return self.base_client.testset.get_testset(id=id)
    
    def delete_testset(self, id: str):
        return self.base_client.testset.delete_testset(id=id)


class Trace:
    """
    Represents a trace in the NeuralTrust system.
    """

    def __init__(self, client, trace_id: str = None, interaction_id: typing.Optional[str] = None, conversation_id: str = None, channel_id: str = None, 
                 session_id: str = None, user: typing.Optional[User] = None, metadata: typing.Optional[Metadata] = None, custom: typing.Optional[dict] = None):
        """
        Initialize a new Trace object.

        Args:
            interaction_id: ID that can be shared across multiple related traces
            trace_id: Unique identifier for this specific trace
        """
        self.client = client
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.session_id = session_id
        self.trace_id = trace_id
        self.interaction_id = interaction_id or str(uuid.uuid4())
        self.channel_id = channel_id
        self.user = user
        self.metadata = metadata
        self.custom = custom
        self.parent_id = None
        self.start_timestamp = None
        self.end_timestamp = None
        self.latency = None
        self.input = None
        self.output = None
        self.feedback_tag = None
        self.feedback_text = None
        self.task = None

    def message(self, input: str) -> 'Trace':
        """
        Start a message trace.

        Args:
            input (str): The input message.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.MESSAGE.value
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        return new_trace

    def tool(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Start a tool trace.

        Args:
            input (str): The input for the tool.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.TOOL.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        return new_trace

    def agent(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Start an agent trace.

        Args:
            input (str): The input for the agent.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.AGENT.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        return new_trace

    def retrieval(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Start a retrieval trace.

        Args:
            input (str): The input for the retrieval task.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.RETRIEVAL.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        return new_trace

    def generation(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Start a generation trace.

        Args:
            input (str): The input for the generation task.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.GENERATION.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        return new_trace

    def router(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Start a router trace.

        Args:
            input (str): The input for the router task.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.ROUTER.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        new_trace.end_timestamp = int(dt.datetime.now().timestamp())
        new_trace._send_trace()
        return new_trace

    def event(self, input: str, parent_id: str = None) -> 'Trace':
        """
        Record an event trace.

        Args:
            input (str): The input for the event.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = input
        new_trace.task = EventType.CUSTOM.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        new_trace.end_timestamp = int(dt.datetime.now().timestamp())
        new_trace._send_trace()
        return new_trace

    def system(self, prompt: str|object, parent_id: str = None) -> 'Trace':
        """
        Record a system trace.

        Args:
            prompt (str|object): The input for the system trace. If not a string, it will be converted to a string.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.input = str(prompt)
        new_trace.task = EventType.SYSTEM.value
        new_trace.parent_id = parent_id or self.trace_id
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        new_trace.end_timestamp = int(dt.datetime.now().timestamp())
        new_trace._send_trace()
        return new_trace
    
    def feedback(self, feedback_tag: FeedbackTag, feedback_text: str, parent_id: str = None) -> 'Trace':
        """
        Record a feedback trace.

        Args:
            feedback_tag (FeedbackTag): The type of feedback.
            feedback_text (str): The feedback text content.
            parent_id (str, optional): The ID of the parent trace.

        Returns:
            Trace: A new Trace object.
        """
        trace_id = str(uuid.uuid4())
        new_trace = Trace(
            client=self.client,
            trace_id=trace_id,
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            user=self.user,
            metadata=self.metadata,
            custom=self.custom,
            interaction_id=self.interaction_id
        )
        new_trace.feedback_tag = feedback_tag.value
        new_trace.feedback_text = feedback_text
        new_trace.task = EventType.FEEDBACK.value
        new_trace.start_timestamp = int(dt.datetime.now().timestamp())
        new_trace.end_timestamp = int(dt.datetime.now().timestamp())
        new_trace.parent_id = parent_id or self.trace_id
        new_trace._send_trace()
        return new_trace

    def end(self, output: str|object) -> 'Trace':
        """
        End the current trace and record the output.

        Args:
            output (str|object): The output of the trace. If not a string, it will be converted to a string.

        Returns:
            Trace: The current Trace object.
        """
        self.output = str(output)
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()
        return self
    
    def send(
        self,
        event_type: EventType,
        input: str,
        output: str = None,
        latency: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
        parent_id: str = None
    ) -> 'Trace':
        """
        Send an atomic event to NeuralTrust.

        Args:
            event_type (EventType): The type of the event.
            input (str): The input data for the event.
            output (str, optional): The output data for the event.
            start_timestamp (int, optional): The start timestamp of the event in milliseconds. If not provided, the current time will be used.
            end_timestamp (int, optional): The end timestamp of the event in milliseconds. If not provided, the current time will be used.
            parent_id (str, optional): The ID of the parent trace. Required for all event types except MESSAGE.

        Returns:
            Trace: The current Trace object.

        Raises:
            ValueError: If parent_id is not provided for non-MESSAGE event types
        """
        try:    
            current_time = int(dt.datetime.now().timestamp())
            if start_timestamp is None:
                start_timestamp = current_time
            if end_timestamp is None:
                end_timestamp = current_time

            # Validate parent_id requirement
            if event_type != EventType.MESSAGE and parent_id is None:
                raise ValueError(f"parent_id is required for event type {event_type.value}")

            self.trace_id = self.trace_id or str(uuid.uuid4())
            self.interaction_id = self.interaction_id or str(uuid.uuid4())
            self.task = event_type.value
            self.input = str(input)
            self.output = str(output)
            self.latency = latency
            self.start_timestamp = start_timestamp
            self.end_timestamp = end_timestamp
            self.parent_id = parent_id
            
            self._send_trace()
            return self
        except Exception as e:
            raise e
    
    def _send_trace(self):
        """
        Internal method to send the trace to the API.
        Now uses both trace_id and interaction_id.
        """
        try:
            self.client._trace(
                type="traces",
                conversation_id=self.conversation_id,
                session_id=self.session_id,
                channel_id=self.channel_id,
                interaction_id=self.interaction_id,
                trace_id=self.trace_id,
                user=self.user,
                metadata=self.metadata,
                input=self.input,
                output=self.output,
                feedback_tag=self.feedback_tag,
                feedback_text=self.feedback_text,
                task=self.task,
                latency=self.latency,
                custom=str(self.custom),
                start_timestamp=self.start_timestamp * 1000,
                end_timestamp=self.end_timestamp * 1000,
                parent_id=self.parent_id
            )
            self.input = None
            self.output = None
            self.task = None
            self.start_timestamp = None
            self.end_timestamp = None
            return self
        except Exception as e:
            raise e

