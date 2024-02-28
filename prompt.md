You are going to take a user-provided intent which describes their batch job requirement, and convert it to JSON which can be used to create a GCP batch resource. JSON is a lightweight data-interchange format that is easy for humans to read and write and for machines to parse and generate.

You will be given a natural lauguage text input which describes the intent of user. Some examples are provided below but you can also use the GCP batch config json examples you already have.

Description of intent: a basic job which runs a very simple test script, it requires minimal compute resources

{
    "taskGroups": [
        {
            "taskSpec": {
                "runnables": [
                    {
                        "script": {
                            "text": "echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks."
                        }
                    }
                ],
                "computeResource": {
                    "cpuMilli": 2000,
                    "memoryMib": 2000
                },
                "maxRetryCount": 1,
                "maxRunDuration": "3600s"
            },
            "taskCount": 1,
            "parallelism": 1
        }
    ],
    "allocationPolicy": {
        "instances": [
            {
                "policy": { "machineType": "e2-highcpu-2" }
            }
        ]
    },
    "logsPolicy": {
        "destination": "CLOUD_LOGGING"
    }
}


Description of intent: An image processing job which requires medium amount of compute resources and proper machine type. The job is not mission critical so we can use "provisioningModel": "SPOT".

{
  "taskGroups": [
    {
      "taskSpec": {
        "runnables": [
          {
            "script": {
              "text": "bash /mnt/share/transcode.sh"
            }
          }
        ],
        "computeResource": {
          "cpuMilli": 2000,
          "memoryMib": 2048
        },
        "volumes": [
          {
            "gcs": {
              "remotePath": "BUCKET_NAME"
            },
            "mountPath": "/mnt/share"
          }
        ],
        "maxRetryCount": 2,
        "maxRunDuration": "600s"
      },
      "taskCount": 3,
      "parallelism": 3
    }
  ],
  "allocationPolicy": {
    "instances": [
      {
        "policy": {
          "machineType": "n2d-standard-4",
          "provisioningModel": "SPOT"
        }
      }
    ]
  },
  "logsPolicy": {
    "destination": "CLOUD_LOGGING"
  }
}
