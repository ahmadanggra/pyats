#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pyats.topology import loader


def validate_ospf(output_dir):
    output_path = Path('./' + output_dir + '/')
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        testbed = loader.load('testbed.yml')
        learnt = {}

        for name, dev in testbed.devices.items():
            dev.connect(log_stdout=False)
            learnt[name] = {}
            learnt[name]['routing'] = dev.learn('routing')
            learnt[name]['ospf'] = dev.learn('ospf')

            with open(output_path / f'{name}_routing.json', 'w') as f:
                json.dump(learnt[name]['routing'].to_dict(), f, indent=4)

            with open(output_path / f'{name}_ospf.json', 'w') as f:
                json.dump(learnt[name]['ospf'].to_dict(), f, indent=4)

            dev.disconnect()

    except Exception as e:
        print(f"Error parsing command: {e}")


def main():
    validate_ospf(sys.argv[1])


if __name__ == '__main__':
    main()