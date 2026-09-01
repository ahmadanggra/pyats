#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pyats.topology import loader

# Directory this script lives in, regardless of where it's invoked from
SCRIPT_DIR = Path(__file__).resolve().parent


def state_ospf(output_dir):
    output_path = Path('/tmp/semaphore/pyats/' + output_dir + '/')
    output_path.mkdir(parents=True, exist_ok=True)

    testbed_path = SCRIPT_DIR / 'testbed.yml'

    if not testbed_path.exists():
        print(f"Error: testbed file not found at {testbed_path}")
        return

    try:
        testbed = loader.load(str(testbed_path))
        learnt = {}

        for name, dev in testbed.devices.items():
            dev.connect(log_stdout=False)
            learnt[name] = {}
            learnt[name]['routing'] = dev.learn('routing')
            learnt[name]['ospf'] = dev.learn('ospf')

            with open(output_path / f'routing_{dev.os}_{dev.name}_ops.txt', 'w') as f:
                json.dump(learnt[name]['routing'].info, f, indent=2)

            with open(output_path / f'ospf_{dev.os}_{dev.name}_ops.txt', 'w') as f:
                json.dump(learnt[name]['ospf'].info, f, indent=2)

            dev.disconnect()

        print(f"✅ Capture state had been done successfully.")
        return 0

    except Exception as e:
        print(f"Error parsing command: {e}")
        return 1


def main():
    result = state_ospf(sys.argv[1])
    sys.exit(result)


if __name__ == '__main__':
    main()