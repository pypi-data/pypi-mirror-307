from typing import assert_never

from uncountable.integration.executors.generic_upload_executor import GenericUploadJob
from uncountable.integration.executors.script_executor import resolve_script_executor
from uncountable.integration.job import Job, JobArguments
from uncountable.types import job_definition_t


def resolve_executor(
    job_executor: job_definition_t.JobExecutor,
    profile_metadata: job_definition_t.ProfileMetadata,
) -> Job:
    match job_executor:
        case job_definition_t.JobExecutorScript():
            return resolve_script_executor(
                job_executor, profile_metadata=profile_metadata
            )
        case job_definition_t.JobExecutorGenericUpload():
            return GenericUploadJob(
                remote_directories=job_executor.remote_directories,
                upload_strategy=job_executor.upload_strategy,
                data_source=job_executor.data_source,
            )
    assert_never(job_executor)


def execute_job(
    *,
    job_definition: job_definition_t.JobDefinition,
    profile_metadata: job_definition_t.ProfileMetadata,
    args: JobArguments,
) -> job_definition_t.JobResult:
    with args.logger.push_scope(job_definition.name) as job_logger:
        job = resolve_executor(job_definition.executor, profile_metadata)

        job_logger.log_info("running job")

        try:
            result = job.run_outer(args=args)
        except Exception as e:
            job_logger.log_exception(e)
            return job_definition_t.JobResult(success=False)

        if args.batch_processor.current_queue_size() != 0:
            args.batch_processor.send()

        submitted_batch_job_ids = args.batch_processor.get_submitted_job_ids()
        job_logger.log_info(
            "completed job",
            attributes={
                "submitted_batch_job_ids": submitted_batch_job_ids,
                "success": result.success,
            },
        )

        return result
