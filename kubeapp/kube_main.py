from kubernetes import client, config
import subprocess

config.load_kube_config()

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
                
    print(running_pods)
    print(issue_pods)
    
    return running_pods,issue_pods
    

def get_all_deployments():
    print("Listing Deployments:")
    
    ret=client.AppsV1Api().list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.metadata.namespace, i.metadata.name, i.status.available_replicas))
        
    return ret.items

def get_logs(pod_name):
    # print("Getting logs for pod %s" % pod_name)
    # ret=v1.read_namespaced_pod_log(name=pod_name,namespace="default")
    # print(ret)
    rest=subprocess.check_output(["kubectl","describe","pod",pod_name,"-n","default"])
    print(rest)

def issue_pod_logs(arr):
    
    for pod in arr:
        print("Getting logs for pod %s" % pod)
        get_logs(pod)
    
    return "Logs fetched for all issue pods"
    

if __name__=="__main__":
    running_pods,issue_pods=get_pods()
    issue_pod_logs(issue_pods)
    
    totalpods=len(running_pods)+len(issue_pods)
    
    
    print("Total pods: %d" % totalpods)
    
    