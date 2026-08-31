import json
from pyats.topology import loader

testbed = loader.load('testbed.yml')

device = testbed.devices['csr1']

device.connect(log_stdout=False)

output = device.parse('show version')

json_output = json.dumps(output, indent=4)

print(json_output)