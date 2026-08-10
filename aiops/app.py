
# from k8s_observer import (
#     get_pods,
#     get_events,
#     get_pod_details,
#     get_pod_logs
# )


# def detect_incidents(pods, events):
#     incidents = []

#     problem_states = [
#         "CrashLoopBackOff",
#         "ImagePullBackOff",
#         "ErrImagePull",
#         "Pending",
#         "OOMKilled",
#         "Error"
#     ]

#     for state in problem_states:
#         if state in pods or state in events:
#             incidents.append(state)

#     return incidents


# def main():

#     print("Collecting Kubernetes information...")

#     pods = get_pods()
#     events = get_events()

#     incidents = detect_incidents(pods, events)

#     if not incidents:
#         print("✅ No obvious incidents detected.")
#         return

#     print("\n🚨 INCIDENT DETECTED")

#     for incident in incidents:
#         print(f" - {incident}")

#     print("\n=== POD INFORMATION ===")
#     print(pods)

#     print("\n=== KUBERNETES EVENTS ===")
#     print(events)


# if __name__ == "__main__":
#     main()

from k8s_observer import (
    get_pod_details,
    get_pod_logs,
    get_pod_events,
    get_problem_pods
)

from ai_analyzer import analyze_incident


def main():

    print("🔍 Checking Kubernetes for incidents...")

    incidents = get_problem_pods()

    if not incidents:
        print("✅ No incidents detected.")
        return

    print("\n🚨 INCIDENT(S) DETECTED")

    for incident in incidents:

        namespace = incident["namespace"]
        pod = incident["pod"]
        status = incident["status"]

        print(f"\nNamespace : {namespace}")
        print(f"Pod       : {pod}")
        print(f"Status    : {status}")

        print("\n📋 Collecting pod details...")
        pod_info = get_pod_details(namespace, pod)

        print("📜 Collecting pod logs...")
        logs = get_pod_logs(namespace, pod)

        print("📅 Collecting pod events...")
        events = get_pod_events(namespace, pod)

        # Keep only useful recent evidence
        pod_info = pod_info[-2000:]
        logs = logs[-1500:]
        events = events[-2000:]

        evidence = f"""
POD: {pod}
NAMESPACE: {namespace}
STATUS: {status}

POD DETAILS:
{pod_info}

CONTAINER LOGS:
{logs}

POD EVENTS:
{events}
"""

        print("\n📦 Evidence size:", len(evidence), "characters")

        analysis = analyze_incident(evidence)

        print("\n==============================")
        print("       AI INCIDENT REPORT")
        print("==============================")

        print(analysis)


if __name__ == "__main__":
    main()