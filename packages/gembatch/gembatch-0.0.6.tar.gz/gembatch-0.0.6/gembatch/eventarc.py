"""Module to handle Eventarc events."""

import itertools

import functions_framework
from cloudevents.http import event as cloud_event  # type: ignore
from firebase_admin import firestore  # type: ignore
from firebase_functions import logger  # type: ignore
from google.cloud import firestore as fs  # type: ignore

from gembatch import configs, gemini, models, utils

JOB_QUEUE_COLLECTION = configs.GEMBATCH_FIRESTORE_JOB_QUEUE_COLLECTION.value


@functions_framework.cloud_event
def on_receive_gembatch_bigquery_batch_updates(event: cloud_event.CloudEvent):
    """Handle the completion of a batch prediction job."""

    resource: str | None = event.get("resourcename")
    if not resource:
        raise ValueError(f"Need bigquery event, got {event}.")
    tokens = resource.strip("/").split("/")
    attributes = {k: v for k, v in zip(tokens[0::2], tokens[1::2])}
    table = attributes["tables"]
    logger.info(f"Received bigquery event for {table}")
    if not table.startswith(f"{gemini.BATCH_DISPLAY_NAME}-destination"):
        logger.info(f"Skipping event for {table}")
        return

    db = firestore.client()
    batch_job = gemini.GeminiBatchJob.from_bq_event(event)
    visited = set()
    for rows in itertools.batched(batch_job.list_results(), 50):
        batch = db.batch()
        for row in rows:
            job = models.Job.from_db(db, row.metadata["uuid"])
            if job is None:
                logger.warn(f"Job {row.metadata['uuid']} not found.")
                continue
            job.save_response(db, row.response)
            job.status = models.StatusEnum.COMPLETED
            batch.update(
                db.collection(JOB_QUEUE_COLLECTION).document(job.uuid),
                job.asdict(),
            )
            visited.add(job.uuid)
        batch.commit()
    batch_job.mark_as_done()

    # Trigger post-job completion tasks
    queue = utils.CloudRunQueue.open("handleGemBatchJobComplete")
    for job_id in visited:
        queue.run(job_id=job_id)

    # Clean up failed jobs
    docs = (
        db.collection(JOB_QUEUE_COLLECTION)
        .where(filter=fs.FieldFilter("batch_job_id", "==", batch_job.uuid))
        .stream()
    )
    doc: fs.DocumentSnapshot
    for doc in docs:
        job = models.Job.from_dict(doc.to_dict())
        if job.uuid in visited:
            continue
        job.status = models.StatusEnum.FAILED
        doc.reference.update(job.asdict())
