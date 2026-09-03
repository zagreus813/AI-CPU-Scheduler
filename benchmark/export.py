import json
import csv
import os


def save_json(
    results,
    filename
):

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )


    with open(
        filename,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )



def save_csv(
    results,
    filename
):

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )


    if not results:
        return


    fields = [
        "scheduler",
        "waiting",
        "turnaround",
        "response",
        "cpu_utilization",
        "throughput",
        "context_switches",
        "context_switch_overhead",
        "context_switch_ratio"
    ]


    with open(
        filename,
        "w",
        newline=""
    ) as f:


        writer = csv.DictWriter(
            f,
            fieldnames=fields
        )


        writer.writeheader()


        for name, metrics in results.items():

            row = {
                "scheduler": name
            }

            row.update(metrics)


            writer.writerow(row)
