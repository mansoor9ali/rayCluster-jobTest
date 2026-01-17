from ray.job_submission import JobSubmissionClient, JobStatus
import time


if __name__ == '__main__':
    # If using a remote cluster, replace 127.0.0.1 with the head node's IP address.
    client = JobSubmissionClient("http://127.0.0.1:8265")
    job_id = client.submit_job(
        # Entrypoint shell command to execute
        entrypoint="python script.py",
        # Path to the local directory that contains the script.py file
        # Runtime environment for the job, specifying a working directory and pip package
        runtime_env={
            "working_dir": "./",
            "pip": ["requests==2.26.0"]
        },
        # Reserve 1 GPU for the entrypoint script
        # entrypoint_num_gpus = 1
    )
    print(job_id)


    def wait_until_status(job_id, status_to_wait_for, timeout_seconds=5):
        start = time.time()
        while time.time() - start <= timeout_seconds:
            status = client.get_job_status(job_id)
            print(f"status: {status}")
            if status in status_to_wait_for:
                break
            time.sleep(1)


    wait_until_status(job_id, {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED})
    logs = client.get_job_logs(job_id)
    print(logs)