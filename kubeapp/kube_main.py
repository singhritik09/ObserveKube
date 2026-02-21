from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def load_kubernetes_config():
    """
    Load Kubernetes config safely.
    Works for:
    - In-cluster
    - Local kubeconfig
    - CI (gracefully skips)
    """
    try:
        config.load_incluster_config()
        print("Using in-cluster config")
        return True
    except ConfigException:
        try:
            config.load_kube_config()
            print("Using local kubeconfig")
            return True
        except Exception:
            print("No Kubernetes config found (CI or Docker without kubeconfig)")
            return False


def get_core_v1():
    if not load_kubernetes_config():
        return None
    return client.CoreV1Api()


def get_pods():
    v1 = get_core_v1()
    if not v1:
        return [], []

    running_pods = []
    issue_pods = []

    ret = v1.list_pod_for_all_namespaces(watch=False)

    for pod in ret.items:
        if pod.metadata.namespace == "default":
            if pod.status.phase == "Running":
                running_pods.append(pod.metadata.name)
            else:
                issue_pods.append(pod.metadata.name)

    return running_pods, issue_pods


def get_all_deployments():
    if not load_kubernetes_config():
        return []

    apps_v1 = client.AppsV1Api()
    ret = apps_v1.list_deployment_for_all_namespaces(watch=False)

    return ret.items


def get_logs(pod_name):
    """
    Use Kubernetes API instead of subprocess kubectl
    """
    v1 = get_core_v1()
    if not v1:
        return "No cluster access"

    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace="default"
        )
        return logs
    except Exception as e:
        return str(e)


def issue_pod_logs(pod_list):
    logs_data = {}

    for pod in pod_list:
        logs_data[pod] = get_logs(pod)

    return logs_data


def overall_dashboard():
    running_pods, issue_pods = get_pods()

    totalpods = len(running_pods) + len(issue_pods)

    logs = issue_pod_logs(issue_pods)

    return {
        "running_pods": running_pods,
        "issue_pods": issue_pods,
        "total_pods": totalpods,
        "issue_logs": logs
    }