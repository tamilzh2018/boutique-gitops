
# import subprocess


# def kubectl(command):
#     result = subprocess.run(
#         ["kubectl"] + command.split(),
#         capture_output=True,
#         text=True
#     )

#     if result.returncode != 0:
#         raise RuntimeError(result.stderr)

#     return result.stdout


# def get_pods():
#     return kubectl("get pods -A")


# def get_events():
#     return kubectl("get events -A --sort-by=.lastTimestamp")


# def get_nodes():
#     return kubectl("get nodes")


# if __name__ == "__main__":
#     print("=== PODS ===")
#     print(get_pods())

#     print("=== EVENTS ===")
#     print(get_events())

#     print("=== NODES ===")
#     print(get_nodes())

import subprocess


def kubectl(command):
    result = subprocess.run(
        ["kubectl"] + command.split(),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("kubectl error:")
        print(result.stderr)
        return ""

    return result.stdout


def get_pods():
    return kubectl("get pods -A")


# def get_events():
#     return kubectl("get events -A --sort-by=.lastTimestamp")
def get_pod_events(namespace, pod):
    return kubectl(
        f"get events -n {namespace} "
        f"--field-selector involvedObject.name={pod} "
        f"--sort-by=.lastTimestamp"
    )

def get_pod_details(namespace, pod):
    return kubectl(f"describe pod {pod} -n {namespace}")


# def get_pod_logs(namespace, pod):
#     return kubectl(f"logs {pod} -n {namespace}")
def get_pod_logs(namespace, pod):
    return kubectl(
        f"logs {pod} -n {namespace} --tail=100"
    )

def get_problem_pods():
    output = get_pods()

    problem_pods = []

    for line in output.splitlines():

        if "CrashLoopBackOff" in line:
            parts = line.split()

            if len(parts) >= 2:
                namespace = parts[0]
                pod = parts[1]

                problem_pods.append({
                    "namespace": namespace,
                    "pod": pod,
                    "status": "CrashLoopBackOff"
                })

    return problem_pods


