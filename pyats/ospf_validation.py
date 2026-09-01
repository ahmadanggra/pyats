#!/usr/bin/env python3
import json
from pathlib import Path
from pyats.topology import loader

try:
    testbed = loader.load('testbed.yml')
    learnt = {}
    for name, dev in testbed.devices.items():
        output_dir = Path('./pre-change/')
        output_dir.mkdir(parents=True, exist_ok=True)
        dev.connect(log_stdout=False)
        learnt[name] = {}
        learnt[name]['routing'] = dev.learn('routing')
        learnt[name]['ospf'] = dev.learn('ospf')
        # print(json.dumps(learnt[name]['routing'].to_dict(), indent=4))
        # print(json.dumps(learnt[name]['ospf'].to_dict(), indent=4))
        with open(f"{output_dir}/{name}_routing.json", "w") as f:
            json.dump(learnt[name]['routing'].to_dict(), f, indent=4)
        with open(f"{output_dir}/{name}_ospf.json", "w") as f:
            json.dump(learnt[name]['ospf'].to_dict(), f, indent=4)
        dev.disconnect()
except Exception as e:
    print(f"Error parsing command: {e}")