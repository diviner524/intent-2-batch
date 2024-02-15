# intent-2-batch
Convert user intent to a GCP batch job

In a common workflow, GCP batch users need to manually convert their intent into a configuration file which can be understood by Batch API before creating a Batch Job.

```mermaid
graph LR;
    UserIntent("User Intent") -->|Manually Crafting| BatchJobConfig("Batch Job Config");
    BatchJobConfig --> BatchAPI("Batch API");
    BatchAPI --> ComputeResources("Compute Resources");
```

