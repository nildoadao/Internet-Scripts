import json, subprocess

output = {}
instances = {}
services = {}
listener = {}

try:
    status_command = subprocess.check_output(["./status-bd-sh"])

    for line in status_command.splitlines():

        if "Instance" in line:
            instance_key = line.split(' ')[1]
            instance_value = line.split(' ')[3]

            if "not" in instance_value:
                instance_value = "not running"

            instances[instance_key] = instance_value

        if "Service" in line:
            service_key = line.split(' ')[1]
            service_value = line.split(' ')[3]

            if "not" in service_value:
                service_value = "not running"

            services[service_key] = service_value

        if "Listener" in line:

            if "node" in line:
                listener_state = line.split(' ')[3]
                if "not" in listener_state:
                    listener_state = "not running"
                listener["state"] = listener_state
            else:
                listener_enabled = line.split(' ')[3]
                if "not" in listener_enabled:
                    listener_enabled = "not enabled"
                listener["enabled"] = listener_enabled


    output["Instances"] = instances
    output["Services"] = services
    output["Listener"] = listener

except Exception as e:
    output["Instances"] = "erro"
    output["Services"] = "erro"
    output["Listener"] = "erro"

print(json.dumps(output, indent=4))
