from infra.kafka import KafkaFactory
from config.enums import KafkaTopic
from schemas import VideoUploadedPayload

payload = VideoUploadedPayload.model_validate({
        "jobId": "1",
        "videoId": "1",
        "filename": "Week 0.1 - Introduction, Seetings Up IDE.mp4",
        "objectKey": "videos/1/Week 0.1 - Introduction, Seetings Up IDE.mp4"
    })

KafkaFactory.create().producer().publish(
    topic=KafkaTopic.VIDEO_UPLOADED,
    key=payload.jobId,
    value=payload.model_dump()
)