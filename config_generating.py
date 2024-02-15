import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview import generative_models


def multiturn_generate_content():
    config = {
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    }
    model = GenerativeModel("gemini-pro")
    chat = model.start_chat()
    print(chat.send_message("""You are going to take a user-provided intent which describes their batch job requirement, and convert it to JSON which can be used to create a GCP batch resource. JSON is a lightweight data-interchange format that is easy for humans to read and write and for machines to parse and generate.

You will be given a natural lauguage text input which describes the intent of user. Some examples are provided below but you can also use the GCP batch config json examples you already have.

Description of intent: a basic job which runs a very simple test script, it requires minimal compute resources
```
{
    \"taskGroups\": [
        {
            \"taskSpec\": {
                \"runnables\": [
                    {
                        \"script\": {
                            \"text\": \"echo Hello world! This is task ${BATCH_TASK_INDEX}. This job has a total of ${BATCH_TASK_COUNT} tasks.\"
                        }
                    }
                ],
                \"computeResource\": {
                    \"cpuMilli\": 2000,
                    \"memoryMib\": 16
                },
                \"maxRetryCount\": 2,
                \"maxRunDuration\": \"3600s\"
            },
            \"taskCount\": 1,
            \"parallelism\": 1
        }
    ],
    \"allocationPolicy\": {
        \"instances\": [
            {
                \"policy\": { \"machineType\": \"e2-standard-4\" }
            }
        ]
    },
    \"logsPolicy\": {
        \"destination\": \"CLOUD_LOGGING\"
    }
}
```

Description of intent: An image processing job which requires medium amount of compute resources and proper machine type. The job is not mission critical so we can use \"provisioningModel\": \"SPOT\".

```
{
  \"taskGroups\": [
    {
      \"taskSpec\": {
        \"runnables\": [
          {
            \"script\": {
              \"text\": \"bash /mnt/share/transcode.sh\"
            }
          }
        ],
        \"computeResource\": {
          \"cpuMilli\": 2000,
          \"memoryMib\": 2048
        },
        \"volumes\": [
          {
            \"gcs\": {
              \"remotePath\": \"BUCKET_NAME\"
            },
            \"mountPath\": \"/mnt/share\"
          }
        ],
        \"maxRetryCount\": 2,
        \"maxRunDuration\": \"600s\"
      },
      \"taskCount\": 3,
      \"parallelism\": 3
    }
  ],
  \"allocationPolicy\": {
    \"instances\": [
      {
        \"policy\": {
          \"machineType\": \"n2d-standard-4\",
          \"provisioningModel\": \"SPOT\"
        }
      }
    ]
  },
  \"logsPolicy\": {
    \"destination\": \"CLOUD_LOGGING\"
  }
}
```""", generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }))
    print(chat.send_message("""Description of intent: User
I want to create a test batch job which is not mission critical, but I want to create 5 different tasks to run the same test script, please generate the JSON""", generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }))
    print(chat.send_message("""Description of intent: User I want to create a test batch job which is not mission critical, so SPOT VMs are acceptable. But I want to create 5 different tasks to run the same test script, and allow at most 2 tasks to run at the same time. please generate the JSON""", generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }))
    print(chat.send_message("""Description of intent: A data processing job which requires a lot of compute resources and a specific machine type. The job is mission critical so we can use \"provisioningModel\": \"PREEMPTIBLE\".""", generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }))




multiturn_generate_content()
