from kafka import KafkaProducer
import json
from app.core.config import settings

class EventProducer:
    def __init__(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                # Add short timeouts for MVP in case Kafka is unavailable
                request_timeout_ms=1000,
                delivery_timeout_ms=2000
            )
        except Exception as e:
            print(f"Kafka Producer connection failed: {e}")
            self.producer = None

    def emit(self, topic: str, data: dict):
        if self.producer:
            try:
                self.producer.send(topic, data)
                self.producer.flush()
            except Exception as e:
                print(f"Failed to emit event to {topic}: {e}")
        else:
            print(f"Mocking event emission to {topic}: {data}")

event_producer = EventProducer()
