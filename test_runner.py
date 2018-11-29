import os
from kubernetes import client, config

DEPLOYMENT_NAME = "lalaa"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret.json"

def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(name="lala", image="gcr.io/spacemesh-198810/node:46f1ad099cdfefc65dda5f726d26ecea7b1f35fb", ports=[client.V1ContainerPort(container_port=9091)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app": "nginx"}), spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(replicas=1, template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(api_version="extensions/v1beta1", kind="Deployment",metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),spec=spec)
    return deployment

def create_deployment(api_instance, deployment):
# Create deployement
    api_response = api_instance.create_namespaced_deployment(body=deployment,namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))

def update_deployment(api_instance, deployment):
    # Update container image
    deployment.spec.template.spec.containers[0].image = "nginx:1.9.1"
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))

def delete_deployment(api_instance):
# Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
    name=DEPLOYMENT_NAME,
    namespace="default",
    body=client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def list_all():
    config_file = os.path.join(os.path.expanduser('~'), '.kube', 'config')
    contexts, active_context = config.list_kube_config_contexts(config_file)
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return    
    contextsNames = [context['name'] for context in contexts]    
    for ctx in contextsNames:
        v1 = client.CoreV1Api(config.new_client_from_config(config_file, ctx))
        print("cluster: " + ctx + " Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default")
    for item in ret.items:
        print("%s\t%s\t%s" % (item.status.pod_ip, item.metadata.namespace, item.metadata.name))
           
if __name__ == '__main__':
   list_all()    
   config.load_kube_config()
   extensions_v1beta1 = client.ExtensionsV1beta1Api()
   deployment = create_deployment_object()    
   create_deployment(extensions_v1beta1, deployment)
   list_all()
   update_deployment(extensions_v1beta1, deployment)
   #delete_deployment(extensions_v1beta1)