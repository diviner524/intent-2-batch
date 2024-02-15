import subprocess
import json

# Construct the gcloud command
gcloud_command = [
    'gcloud', 'batch', 'jobs', 'submit', 'example-ai-job-2',
    '--location', 'us-central1',
    '--config', 'intense_config.json'
]

# Execute the gcloud command
subprocess.run(gcloud_command, check=True)
