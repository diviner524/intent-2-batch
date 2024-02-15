import subprocess
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview import generative_models

def load_file(filepath):
  with open(filepath, "r") as f:
    content = f.read()
  return content

def multiturn_generate_content():
    config = {
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    }
    model = GenerativeModel("gemini-pro")
    chat = model.start_chat()
    # Load prompt from file ./prompt.md as a string
    prompt = load_file("./prompt.md")

    # Send prompt to chat for initial training and rules setting
    chat.send_message(prompt, generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    })

    # Get input from command line on the intent description
    # sample intent descriptions
    # 1. I want to create a test batch job which is not mission critical, but I want to create 5 different tasks to run the same test script, please generate the JSON.
    # 2. I want to create a test batch job which is not mission critical, so SPOT VMs are acceptable. But I want to create 5 different tasks to run the same test script, and allow at most 2 tasks to run at the same time. please generate the JSON.
    # 3. A data processing job which requires a lot of compute resources and a specific machine type. The job is mission critical so we can use "provisioningModel": "PREEMPTIBLE".
    while True:
        print("--------------------------------------------------------------------------------")
        intent_description = input("Describe your desired batch job: ").strip()
        if intent_description == "exit":
            break
        intent_description = "Description of intent: " + intent_description
        response = chat.send_message(intent_description, generation_config=config, safety_settings={
              generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
              generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
              generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
              generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        })

        # Get content from the GenerationResponse
        content = response.candidates[0].content.text

        # Show content to user
        print("--------------------------------------------------------------------------------")
        print("Generated content:")
        print(content)

        # Save content to file
        with open("./job_config.json", "w") as f:
            f.write(content)
        
        # Creating a batch job using gcloud and the saved job config 

        # Construct the gcloud command
        # TODO: let user specify the job name, or generate a random name
        gcloud_command = [
            'gcloud', 'batch', 'jobs', 'submit', 'example-ai-job-2',
            '--location', 'us-central1',
            '--config', 'job_config.json'
            '--dry-run'
        ]

        # Execute the gcloud command
        print("--------------------------------------------------------------------------------")
        print("Submitting batch job...")
        # TODO: we should run actual gcloud command. Batch gcloud command does not support --dry-run, so I cannot do a dry-run here.
        # subprocess.run(gcloud_command, check=True)
        print(" ".join(gcloud_command))

multiturn_generate_content()
