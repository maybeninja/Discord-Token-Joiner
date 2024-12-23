import yaml

with open("config.yaml",'r') as f:
    config = yaml.safe_load(f)

# Proxy 
proxy_mode = config['ProxyMode']['Enable'] 
proxy = config['ProxyMode']['Proxy']

delay = config['Delay']
threads = config['Threads']
capsolving = config['CaptchaSolver']['Enable'] 
api_key =  config['CaptchaSolver']['API']
service = config['CaptchaSolver']['Service']
