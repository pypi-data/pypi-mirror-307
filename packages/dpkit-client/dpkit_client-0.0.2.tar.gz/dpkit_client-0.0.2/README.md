# dpkit

> Python Client of the Module API for Pathology

# Install

Make sure you create a virtual environment, activate it, and then install the `dpkit` client:

```bash
python3 -m pip install dpkit-client
```

# Usage

```python
from time import sleep

from dpkit import AnalysisRequest, Client
from requests_toolbelt import sessions


with sessions.BaseUrlSession(base_url="http://localhost:5000/") as s:
    c = Client(s)

    # let's create a fileset by uploading the content of "input_dir"
    fileset = c.upload(input_dir)

    # then, request an analysis
    analysis = c.new_analysis(AnalysisRequest(
        module="hello_world_v1",
        inputs={
            "wsi": f"@{fileset.id}",
        },
    ))

    # this may take time so wait for the analysis to end
    while True:
        analysis = c.get_analysis(analysis.id)
        if analysis.state == State.FAILED:
            raise RuntimeError(f"last update: {analysis.changes[-1]}")
        if analysis.state == State.COMPLETE:
            break
        sleep(5)

    # analysis is complete so let's download the results
    c.download(analysis, result_dir)

    # and display the analysis itself
    print(analysis.model_dump_json(indent=2))
```
