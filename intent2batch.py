import subprocess
import json
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
        content = content.strip('```')
        content = content.strip('json')

        # Show content to user
        print("--------------------------------------------------------------------------------")
        print("Generated job config:")
        print(content)

        happy = input("Are you happy with the job config: Y/N\n").strip()
        if happy == 'Y':
            pass
        else:
            # TODO: Add the iterative part
            break
        
        with open("./job_config.json", "w") as f:
            f.write(content)

        job_name = input("Please type in a job_name: ").strip()
        location = input("Please type in a location: ").strip()


        gcloud_command = [
            'gcloud', 'batch', 'jobs', 'submit', job_name,
            '--location', location,
            '--config', 'job_config.json'
        ]
        print(" ".join(gcloud_command))
        print("Submitting the batch job...")
        subprocess.run(gcloud_command, check=True)

def fix_batch_job():
    config = {
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    }
    model = GenerativeModel("gemini-pro")
    chat = model.start_chat()
    # Load prompt from file as a string
    prompt = load_file("./fix_my_batch_job_prompt.md")

    # Send prompt to chat for initial training and rules setting
    chat.send_message(prompt, generation_config=config, safety_settings={
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    })

    # Get input from command line on the intent description
    while True:
        print("--------------------------------------------------------------------------------")
        job_str = json.load(open('./job_to_fix.json'))
        job_description = "Batch job to fix is: " + json.dumps(job_str)

        error_description = input("What bothers you? (You can input errors or your intent): ").strip()
        if error_description == "exit":
            break
        error_description = "Errors or intent: " + error_description

        intent_description = job_description + error_description
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
        print(job_description)
        print(error_description)
        print("Generated content:")
        print(content)

        # Save content to file
        with open("./fixed_job.json", "w") as f:
            f.write(content)

        gcloud_command = [
            'gcloud', 'batch', 'jobs', 'submit', 'example-ai-job-2',
            '--location', 'us-central1',
            '--config', 'job_config.json'
        ]

        # Execute the gcloud command
        print("--------------------------------------------------------------------------------")
        print("Submitting batch job...")
        # TODO: we should run actual gcloud command. Batch gcloud command does not support --dry-run, so I cannot do a dry-run here.
        # subprocess.run(gcloud_command, check=True)
        print(" ".join(gcloud_command))


def main():
    intent = input("""Please choose 1. generate a Batch job spec based on my intent \n 2. help fix my batch job (please put the job to fix into ./job_to_fix.json first)\n""")
    if intent == "1":
        multiturn_generate_content()
    elif intent == "2":
        fix_batch_job()
    else:
        print("Thanks for trying intent2batch tool, please choose between 1 and 2.")

main()


