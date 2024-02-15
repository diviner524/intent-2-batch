# intent-2-batch
Convert user intent to a GCP batch job

In a common workflow, GCP batch users need to manually convert their intent into a configuration file which can be understood by Batch API before creating a Batch Job.

```mermaid
graph TD;
    UserIntent("User Intent") -->|Manually Crafting| BatchJobConfig("Batch Job Config");
    BatchJobConfig --> BatchAPI("Batch API");
    BatchAPI --> ComputeResources("Compute Resources");
```

We can leverage Gemini API to help us convert user intent to a job configuration and then directly feed the configuration to Batch API.

```mermaid
graph TD;
    Prompt("Prompt") -.->|Examples & Rules| GeminiAPI("Gemini API");
    UserIntent("User Intent") --> GeminiAPI;
    GeminiAPI --> BatchJobConfig("Batch Job Config");
    BatchJobConfig --> BatchAPI("Batch API");
    BatchAPI --> ComputeResources("Compute Resources");
```

