You already have a user-provided JSON configuration as below.

{ "taskGroups": [ { "taskSpec": { "runnables": [ { "script": { "text": "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks." } } ], "computeResource": { "cpuMilli": 2000, "memoryMib": 2000 }, "maxRetryCount": 1, "maxRunDuration": "3600s" }, "taskCount": 1, "parallelism": 1 } ], "allocationPolicy": { "instances": [ { "policy": { "machineType": "e2-highcpu-2" } } ] }, "logsPolicy": { "destination": "CLOUD_LOGGING" } }

This configuration describes a GCP batch job and can be used in gcloud command to create an actual GCP batch job resource. JSON is a lightweight data-interchange format that is easy for humans to read and write and for machines to parse and generate.

You will be given a natural lauguage text input which describes how the user wants to update the JSON. You need to parse the text input to understand the fields and values user wants to change, and update these fields/values in JSON accordingly.

After update, you want to provide a response which contains:
1. Show the updated json
2. Generate an JSON output with a comment starting with # on the modified field line with the updates you made.

You don't generate any response for this prompt, this is just for initialization and setting context.
