import json
from pyats.topology import loader

testbed = loader.load('testbed.yml')
device = testbed.devices['csr1']
device.connect(log_stdout=False)

try:
    output = device.learn('ospf')
    print(json.dumps(output.to_dict(), indent=4))
except Exception as e:
    print(f"Error parsing command: {e}")
finally:
    device.disconnect()