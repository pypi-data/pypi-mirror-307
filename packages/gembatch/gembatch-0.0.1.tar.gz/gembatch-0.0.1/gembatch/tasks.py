"""Define firebase cloud run tasks."""

import datetime as dt
import itertools
import uuid
from typing import Iterable
import importlib

from firebase_admin import firestore  # type: ignore
from firebase_functions import firestore_fn, logger, options, tasks_fn  # type: ignore
from google.cloud import firestore as fs  # type: ignore

from gembatch import configs, gemini, models, utils, types

JOB_QUEUE_COLLECTION = configs.GEMBATCH_FIRESTORE_JOB_QUEUE_COLLECTION.value
JOBS_IN_QUEUE_FILTER = fs.Or(
    [
        fs.FieldFilter("status", "==", models.StatusEnum.NEW),
        fs.And(
            [
                fs.FieldFilter("status", "==", models.StatusEnum.FAILED),
                fs.FieldFilter("retries", "<", configs.GEMBATCH_MAX_RETRIES.value),
            ]
        ),
    ]
)


@firestore_fn.on_document_created(
    document=configs.GEMBATCH_FIRESTORE_JOB_QUEUE_COLLECTION.value + "/{job_id}",
    region=configs.GEMBATCH_REGION.value,
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
)
def on_gembatch_job_created(
    event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None],
):
    """Handle the creation of a new gem batch job."""
    if not event.data or not event.data.exists:
        raise ValueError("Document does not exist.")
    job = models.Job.from_dict(event.data.to_dict())
    q = utils.CloudRunQueue.open("consumeGemBatchJob")
    q.run(model=job.model)


@firestore_fn.on_document_updated(
    document=configs.GEMBATCH_FIRESTORE_JOB_QUEUE_COLLECTION.value + "/{job_id}",
    region=configs.GEMBATCH_REGION.value,
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
)
def on_gembatch_job_updated(
    event: firestore_fn.Event[
        firestore_fn.Change[firestore_fn.DocumentSnapshot | None]
    ],
):
    """Handle the update of a gem batch job."""
    if not event.data.after or not event.data.after.exists:
        raise ValueError("Document does not exist.")
    job = models.Job.from_dict(event.data.after.to_dict())
    if job.status == models.StatusEnum.COMPLETED:
        logger.info("Job already completed.")
        return
    elif job.status == models.StatusEnum.PENDING:
        logger.info("Job already pending for processing.")
        return
    q = utils.CloudRunQueue.open("consumeGemBatchJob")
    q.run(model=job.model)


@firestore_fn.on_document_created(
    document=configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value + "/{job_id}",
    region=configs.GEMBATCH_REGION.value,
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
)
def on_gembatch_batch_job_created(_):
    """Handle the creation of a new gem batch job."""
    q = utils.CloudRunQueue.open("runGemBatchJob")
    q.run()


@firestore_fn.on_document_updated(
    document=configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value + "/{job_id}",
    region=configs.GEMBATCH_REGION.value,
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
)
def on_gembatch_batch_job_updated(_):
    """Handle the update of a gem batch job."""
    q = utils.CloudRunQueue.open("runGemBatchJob")
    q.run()


@tasks_fn.on_task_dispatched(
    retry_config=options.RetryConfig(max_attempts=2, max_backoff_seconds=300),
    rate_limits=options.RateLimits(max_concurrent_dispatches=1),
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
    max_instances=1,
    concurrency=1,
    region=configs.GEMBATCH_REGION.value,
    timeout_sec=1800,
)
def consumeGemBatchJob(req: tasks_fn.CallableRequest):  # pylint: disable=[invalid-name]
    """
    Consume a gem batch job from the queue.
    """
    model = req.data["model"]
    db = firestore.client()
    consume_gembatch_job(db, model)


def get_job_count_for_model(db: fs.Client, model: str) -> int:
    """
    Get the number of jobs in the queue for the model.
    """
    return (
        db.collection(JOB_QUEUE_COLLECTION)
        .where(filter=JOBS_IN_QUEUE_FILTER)
        .where(filter=fs.FieldFilter("model", "==", model))
        .count()
        .get()[0][0]
        .value
    )


def iterate_pending_jobs(db: fs.Client, model: str) -> Iterable[models.Job]:
    """
    Iterate over pending jobs for the model.
    """
    docs = (
        db.collection(JOB_QUEUE_COLLECTION)
        .where(filter=JOBS_IN_QUEUE_FILTER)
        .where(filter=fs.FieldFilter("model", "==", model))
        .order_by("created_at", direction=fs.Query.ASCENDING)
        .limit(configs.GEMBATCH_MAX_REQUESTS_PER_BATCH.value)
        .stream()
    )
    for doc in docs:
        yield models.Job.from_dict(doc.to_dict())


def consume_gembatch_job(db: fs.Client, model: str):
    """Consume a gem batch job from the queue."""
    count = get_job_count_for_model(db, model)

    status = models.Status.from_db(db)
    last_submit_time = status.get_last_submit_time(model)
    if last_submit_time is None:
        last_submit_time = dt.datetime.now(tz=dt.timezone.utc)
        status.last_batch_submit_time[model] = last_submit_time
        status.save(db)

    if count >= configs.GEMBATCH_MAX_REQUESTS_PER_BATCH.value:
        flush_gembatch_job_queue(db, model)
        return
    elif last_submit_time + dt.timedelta(
        seconds=configs.GEMBATCH_BATCH_INTERVAL_SECONDS.value
    ) > dt.datetime.now(tz=dt.timezone.utc):
        flush_gembatch_job_queue(db, model)
        return
    else:
        delta = dt.datetime.now(tz=dt.timezone.utc) - last_submit_time
        q = utils.CloudRunQueue.open(
            "consumeGemBatchJob",
            delay_seconds=delta.seconds + 1,
        )
        q.run(model=model)


def flush_gembatch_job_queue(db: fs.Client, model: str):
    """Flush the gem batch job queue."""
    uid = uuid.uuid4().hex
    batch_job = gemini.GeminiBatchJob(uid, model)
    for jobs in itertools.batched(iterate_pending_jobs(db, model), 50):
        queries: list[gemini.PredictionQuery] = []
        for job in jobs:
            request = job.get_request(db)
            if not request:
                continue
            queries.append(
                gemini.PredictionQuery(
                    request=request.load_as_dict(),
                    metadata=job.get_metadata(),
                    params=job.params,
                )
            )
        batch_job.write_queries(queries)
        batch = db.batch()
        for job in jobs:
            job.batch_job_id = batch_job.uuid
            job.status = models.StatusEnum.PENDING
            job.retries += 1
            batch.update(
                db.collection(JOB_QUEUE_COLLECTION).document(job.uuid),
                job.asdict(),
            )
        batch.commit()
    batch_job.submit(db)


@tasks_fn.on_task_dispatched(
    retry_config=options.RetryConfig(max_attempts=2, max_backoff_seconds=300),
    rate_limits=options.RateLimits(max_concurrent_dispatches=1),
    memory=configs.GEMBATCH_LARGE_JOB_MEMORY.value,
    max_instances=1,
    concurrency=1,
    region=configs.GEMBATCH_REGION.value,
)
def runGemBatchJob(_: tasks_fn.CallableRequest):  # pylint: disable=[invalid-name]
    """
    Run and submit a gem batch job.
    """
    db = firestore.client()
    active_jobs = gemini.count_active_prediction_jobs()
    if active_jobs >= configs.GEMBATCH_MAX_GEMINI_BATCH_JOBS.value:
        logger.info("Too many active jobs. Skipping.")
        return
    active_gembatch = count_gembatch_running_batch_jobs(db)
    if active_gembatch >= configs.GEMBATCH_MAX_GEMINI_BATCH_JOBS.value:
        logger.info("Too many active gem batch jobs. Skipping.")
        return
    docs = (
        db.collection(configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value)
        .where(
            filter=fs.Or(
                [
                    fs.FieldFilter("status", "==", models.StatusEnum.NEW),
                    fs.FieldFilter("status", "==", models.StatusEnum.PENDING),
                ]
            )
        )
        .order_by("created_at", direction=fs.Query.ASCENDING)
        .limit(1)
        .get()
    )
    if not docs:
        logger.info("No batch jobs to run.")
        return
    job = gemini.GeminiBatchJob.from_doc(docs[0])
    job.run()


def count_gembatch_running_batch_jobs(db: fs.Client) -> int:
    """
    Count the number of running gem batch jobs.
    """
    return (
        db.collection(configs.GEMBATCH_FIRESTORE_BATCH_QUEUE_COLLECTION.value)
        .where("status", "==", models.StatusEnum.RUNNING)
        .count()
        .get()[0][0]
        .value
    )


@tasks_fn.on_task_dispatched(
    retry_config=options.RetryConfig(max_attempts=2, max_backoff_seconds=300),
    memory=configs.GEMBATCH_SMALL_JOB_MEMORY.value,
    max_instances=min(50, configs.GEMBATCH_MAX_REQUESTS_PER_BATCH.value // 5),
    concurrency=5,
    region=configs.GEMBATCH_REGION.value,
)
def handleGemBatchJobComplete(
    req: tasks_fn.CallableRequest,
):  # pylint: disable=[invalid-name]
    """Handle the completion of a gembatch job."""
    job_id = req.data["job_id"]
    job = models.Job.from_db(firestore.client(), job_id)
    if job is None:
        raise ValueError(f"Job {job_id} not found.")
    if job.status != models.StatusEnum.COMPLETED:
        raise RuntimeError(f"Job {job_id} not completed.")
    meta = job.get_metadata()
    importlib.import_module(meta["handler_module"])
    handler: types.ResponseHandler = getattr(
        meta["handler_module"], meta["handler_name"]
    )
    if not callable(handler):
        raise ValueError(f"Handler {handler} is not callable.")
    db = firestore.client()
    response = job.get_response(db)
    if not response:
        raise ValueError(f"Response for job {job_id} not found.")
    handler(response.load_as_response(), **job.params)
