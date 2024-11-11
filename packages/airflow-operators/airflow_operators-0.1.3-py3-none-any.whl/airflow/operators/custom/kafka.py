from typing import Sequence, Callable, Any

from airflow.models import BaseOperator, SkipMixin
from airflow.providers.apache.kafka.hooks.consume import KafkaConsumerHook
from airflow.utils.context import Context


class CustomConsumeFromTopicOperator(BaseOperator, SkipMixin):
    """

    """

    def __init__(
        self,
        topics: str | Sequence[str],
        kafka_config_id: str,
        apply_function_batch: Callable,
        max_messages: int | None = None,
        poll_timeout: float = 60,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.topics = topics
        self.kafka_config_id = kafka_config_id
        self.apply_function_batch = apply_function_batch
        self.max_messages = max_messages
        self.poll_timeout = poll_timeout

    def execute(self, context: Context) -> Any:
        consumer = KafkaConsumerHook(
            topics=self.topics, kafka_config_id=self.kafka_config_id
        ).get_consumer()

        messages = consumer.consume(
            num_messages=self.max_messages, timeout=self.poll_timeout
        )
        if not messages:
            self.log.info("No messages. Skipping downstream tasks...")
            if downstream_tasks := context['task'].get_flat_relatives(
                upstream=False
            ):
                self.skip(
                    context['dag_run'],
                    context['ti'].execution_date,
                    downstream_tasks,
                )
            return

        result = self.apply_function_batch(messages, context)

        if result is not None:
            self.log.info(f"Result: {result}")
            context.get('ti').xcom_push(key='return_value', value=result)

        consumer.commit()
        consumer.close()
        return result


class ConsumeMessageDataOperator(CustomConsumeFromTopicOperator):
    MESSAGES_KEY = 'messages'
    MESSAGES_COUNT_KEY = 'messages_count'

    def __init__(self, task_id: str, max_messages: int = 100, **kwargs):
        args = {
            'task_id': task_id,
            'apply_function_batch': self.messages_process,
            'poll_timeout': 3600,
            'max_messages': max_messages,
        }
        args.update(kwargs)
        super().__init__(**args)

    @classmethod
    def messages_process(cls, messages: Sequence[Any], context) -> None:
        values = [message.value().decode('utf-8') for message in messages]
        context.get('ti').xcom_push(key=cls.MESSAGES_KEY, value=values)
        context.get('ti').xcom_push(key=cls.MESSAGES_COUNT_KEY, value=len(values))
