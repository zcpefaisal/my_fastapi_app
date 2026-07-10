import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from core.config import settings
from core.exptactor_service import CVExtractorService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ai_worker")

async def start_consumer():
    consumer = None
    
    # Attempt to connect to Kafka broker with retry logic
    while True:
        try:
            logger.info("Attempting to connect to Kafka broker...")
            
            consumer = AIOKafkaConsumer(
                "cv_upload",
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id="talent_hunt_ai_worker_group",
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            # Start the consumer
            await consumer.start()
            logger.info("AI Worker Consumer started successfully. Listening for events on 'cv_upload' topic...")
            break 
            
        except (KafkaConnectionError, ConnectionRefusedError):
            logger.warning("Kafka broker is not ready yet. Retrying in 5 seconds...")
            if consumer:
                await consumer.stop()
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error during consumer startup: {e}")
            if consumer:
                await consumer.stop()
            await asyncio.sleep(5)

    # Start consuming messages
    try:
        async for msg in consumer:
            event_payload = msg.value
            logger.info(f"Received new event from Kafka: {event_payload}")

            file_path = event_payload.get("file_path")
            cv_id = event_payload.get("cv_id")

            if not file_path:
                logger.error("Missing 'file_path' in event payload. Skipping processing.")
                continue

            try:
                # Extract text from the PDF file using CVExtractorService
                extracted_text = CVExtractorService.extract_text_from_pdf(file_path)
                logger.info(f"--- Sample Extracted Text (CV ID: {cv_id}) ---\n{extracted_text[:300]}...\n-----")
                
            except Exception as e:
                logger.error(f"Failed to process CV ID {cv_id}: {e}")

    except Exception as e:
        logger.error(f"Critical error in consumer loop: {e}")
    finally:
        if consumer:
            await consumer.stop()
        logger.info("AI Worker Consumer stopped.")

if __name__ == "__main__":
    asyncio.run(start_consumer())