# Guide to use pyats.
Visit this website https://developer.cisco.com/docs/pyats-getting-started/
## OS of choice
The tutorial assume the Operating system using Linux especially ubuntu server 20.04 or higher
## Install python venv
python -m venv .venv
cd .venv 
source .venv/bin/activate
## Install pyats and ansible
Ansible: pip install ansible
Pyats: pip install "pyats[full]"
## Install Ansible Cisco IOS module
ansible-galaxy collection install -r collections/requirements.yml -p collections/
## Creating testbed inventory and test using cli
pyats create testbed file --path scripts/testbed.csv --output scripts/testbed.yml \
pyats validate testbed scripts/testbed.yml \
pyats parse "show version" --testbed-file scripts/testbed.yml --devices csr1
## Basic pyats usecase capture before after ospf change
1. pyats learn ospf routing --testbed-file testbed.yml --devices csr1 --output pre-change
2. pyats learn ospf routing --testbed-file testbed.yml --devices csr1 --output post-change
3. genie diff pre-change post-change
## Workflows for the lab are:
1. All configurations are in ansible playbook using jinja2 templating and host_vars and group_vars.
2. Pyats capture state before.
3. The ospf neighbour reconfigure using authentication using branch update_ospf_password branch.
4. After change and doing pull request, pyats validate ospf neighbourship after re-configure.