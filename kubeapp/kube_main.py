from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
import subprocess

# config.load_kube_config()

# config.load_incluster_config()

try:
    # If running inside Kubernetes
    config.load_incluster_config()
    print("Loaded in-cluster config")
except ConfigException:
    # If running locally
    config.load_kube_config()
    print("Loaded local kube config")

v1=client.CoreV1Api()


def get_pods():
    print("Listing pods with their IPs:")
    ret=v1.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
        # print("%s\t%s\t%s\t%s" % (i.status.phase,i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    running_pods=[]
    issue_pods=[]
    
    for a in ret.items:
        if a.metadata.namespace=="default":
            if a.status.phase=="Running":
                running_pods.append(a.metadata.name)
            else:
                issue_pods.append(a.metadata.name)
    
    return running_pods,issue_pods
    

def get_all_deployments():
    print("Listing Deployments:")
    
    ret=client.AppsV1Api().list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.metadata.namespace, i.metadata.name, i.status.available_replicas))
        
    services=[]
    
    for i in ret.items:
        services.append(i.metadata.name)
    print("Services: %s" % services)
    return services

def get_all_services():
    print("Listing Services:")
    
    ret=v1.list_service_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.metadata.namespace, i.metadata.name, i.spec.type))
        
    return ret.items

def get_logs(pod_name):
    # print("Getting logs for pod %s" % pod_name)
    # ret=v1.read_namespaced_pod_log(name=pod_name,namespace="default")
    # # print(ret)
    # rest=subprocess.check_output(["kubectl","describe","pod",pod_name,"-n","default"])
    # return rest
    
    try:
        ret=subprocess.check_output(["kubectl","describe","pod",pod_name,"-n","default"])
        return ret.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return "Error fetching logs for pod %s: %s" % (pod_name, e)
def issue_pod_logs(arr):
    
    for pod in arr:
        get_logs(pod)
    
    return "Logs fetched for all issue pods"

def overall_dashboard():
    running_pods,issue_pods=get_pods()
    issue_pod_logs(issue_pods)
    
    totalpods=len(running_pods)+len(issue_pods)
    
    print("Total pods: %d" % totalpods)
    get_all_services()
    return running_pods,issue_pods,totalpods,issue_pod_logs(issue_pods),get_all_services()


if __name__=="__main__":
    running_pods,issue_pods=get_pods()
    issue_pod_logs(issue_pods)
    
    totalpods=len(running_pods)+len(issue_pods)
    
    
    
