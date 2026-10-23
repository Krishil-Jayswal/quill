from enum import StrEnum

class KafkaBackendType(StrEnum):
    KAFKA = "kafka"

class KafkaTopic(StrEnum):
    VIDEO_UPLOADED = "quill.video.uploaded"
    MEDIA_COMPLETED = "quill.media.completed"
    TRANSCRIPTION_COMPLETED = "quill.transcription.completed"
    FRAME_REDUCTION_COMPLETED = "quill.frame-reduction.completed"
    OCR_COMPLETED = "quill.ocr.completed"
    LOGS = "quill.logs"
    EVENTS = "quill.events"

class KafkaConsumerGroup(StrEnum):
    MEDIA = "media-worker"
    TRANSCRIPTION = "transcription-worker"
    FRAME_REDUCTION = "frame-reduction-worker"
    OCR = "ocr-worker"
    NOTES = "notes-worker"

class KafkaSecurityProtocol(StrEnum):
    PLAINTEXT = "PLAINTEXT"
    SSL = "SSL"
    SASL_PLAINTEXT = "SASL_PLAINTEXT"
    SASL_SSL = "SASL_SSL"

class KafkaSaslMechanism(StrEnum):
    PLAIN = "PLAIN"
    GSSAPI = "GSSAPI"
    OAUTHBEARER = "OAUTHBEARER"
    SCRAM_SHA_256 = "SCRAM-SHA-256"
    SCRAM_SHA_512 = "SCRAM-SHA-512"
