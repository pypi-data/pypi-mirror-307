"""Define firebase cron jobs."""

import datetime as dt
from firebase_admin import firestore  # type: ignore
from firebase_functions import scheduler_fn, tasks_fn, logger, options
from gembatch import configs, models, gemini, utils
from google.cloud import firestore as fs  # type: ignore

POLL_INTERVAL = str(configs.GEMBATCH_HEALTH_CHECK_POLL_INTERVAL.value)


@scheduler_fn.on_schedule(
    schedule="*/" + POLL_INTERVAL + " * * * *",
    region=configs.GEMBATCH_REGION.value,
    max_instances=1,
    concurrency=1,
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
    timeout_sec=1800,
)
def gembatch_health_check(_):
    """Health check for gembatch."""
    db = firestore.client()
    docs = (
        db.collection(configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value)
        .where(filter=fs.FieldFilter("status", "==", models.StatusEnum.RUNNING))
        .stream()
    )
    for doc in docs:
        job = gemini.GeminiBatchJob.from_doc(doc)
        _check_running_job_health(job)


def _check_running_job_health(job: gemini.GeminiBatchJob):
    handle_failure = utils.CloudRunQueue.open("handleGemBatchJobFailure")
    state = job.poll_job_state()
    if state == models.StatusEnum.RUNNING:
        return
    elif state == models.StatusEnum.COMPLETED:
        now = dt.datetime.now(dt.timezone.utc)
        if now - job.created_at > dt.timedelta(
            seconds=configs.GEMBATCH_BATCH_JOB_POST_PROCESSING_TIMEOUT.value
        ):
            handle_failure.run(job_id=job.uuid)
    elif state == models.StatusEnum.FAILED:
        handle_failure.run(job_id=job.uuid)
    else:
        logger.warn(f"Unknown job state: {state}")


@tasks_fn.on_task_dispatched(
    retry_config=options.RetryConfig(
        max_attempts=2, max_backoff_seconds=300, min_backoff_seconds=10
    ),
    rate_limits=options.RateLimits(max_concurrent_dispatches=10),
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
    max_instances=10,
    concurrency=1,
    region=configs.GEMBATCH_REGION.value,
    timeout_sec=1800,
)
def handleGemBatchJobFailure(req: tasks_fn.CallableRequest):
    """Handle the failure of a gembatch job."""
    job_id = req.data["job_id"]
    db = firestore.client()
    doc_ref = db.collection(
        configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value
    ).document(job_id)
    doc = doc_ref.get()
    if not doc.exists:
        logger.warn(f"Document {job_id} not found")
        return
    mark_all_jobs_in_batch_as_failed(db, job_id)
    job = gemini.GeminiBatchJob.from_doc(doc)
    job.mark_as_done(success=False)


def mark_all_jobs_in_batch_as_failed(db: fs.Client, batch_job_id: str):
    """Mark all jobs in a batch as failed."""
    docs = (
        db.collection(configs.GEMBATCH_FIRESTORE_JOB_QUEUE_COLLECTION.value)
        .where(filter=fs.FieldFilter("batch_job_id", "==", batch_job_id))
        .stream()
    )
    batch = db.batch()
    doc: fs.DocumentSnapshot
    for doc in docs:
        job = models.Job.from_dict(doc.to_dict())
        job.status = models.StatusEnum.FAILED
        batch.update(doc.reference, job.asdict())
    batch.commit()
