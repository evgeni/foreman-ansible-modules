#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2019 Bernhard Hopfenmüller (ATIX AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: host
version_added: 1.0.0
short_description: Manage Hosts
description:
  - Create, update, and delete Hosts
author:
  - "Bernhard Hopfenmueller (@Fobhep) ATIX AG"
options:
  name:
    description:
      - Fully Qualified Domain Name of host
    required: true
    type: str
  hostgroup:
    description:
      - Name of related hostgroup.
    required: false
    type: str
  location:
    description:
      - Name of related location
    required: false
    type: str
  organization:
    description:
      - Name of related organization
    required: false
    type: str
  build:
    description:
      - Whether or not to setup build context for the host
    type: bool
    required: false
  enabled:
    description:
      - Include this host within reporting
    type: bool
    required: false
  managed:
    description:
      - Whether a host is managed or unmanaged.
      - Forced to true when I(build=true)
    type: bool
    required: false
  ip:
    description:
      - IP address of the primary interface of the host.
    type: str
    required: false
  mac:
    description:
      - MAC address of the primary interface of the host.
      - Please include leading zeros and separate nibbles by colons, otherwise the execution will not be idempotent.
      - Example EE:BB:01:02:03:04
    type: str
    required: false
  comment:
    description:
      - Comment about the host.
    type: str
    required: false
  owner:
    description:
      - Owner (user) of the host.
      - Mutually exclusive with I(owner_group).
    type: str
    required: false
  owner_group:
    description:
      - Owner (user group) of the host.
      - Mutually excluside with I(owner).
    type: str
    required: false
  provision_method:
    description:
      - The method used to provision the host.
      - I(provision_method=bootdisk) is only available if the bootdisk plugin is installed.
    choices:
      - 'build'
      - 'image'
      - 'bootdisk'
    type: str
    required: false
  image:
    description:
      - The image to use when I(provision_method=image).
      - The I(compute_resource) parameter is required to find the correct image.
    type: str
    required: false
  compute_attributes:
    description:
      - Additional compute resource specific attributes.
      - When this parameter is set, the module will not be idempotent.
    type: dict
    required: false
  interfaces_attributes:
    description:
      - Additional interfaces specific attributes.
      - When this parameter is set, the module will not be idempotent.
    required: false
    type: list
    elements: dict
    suboptions:
      mac:
        description:
          - MAC address of interface. Required for managed interfaces on bare metal.
        type: str
      ip:
        description:
          - IPv4 address of interface
        type: str
      ip6:
        description:
          - IPv6 address of interface
        type: str
      type:
        description:
          - Interface type.
        type: str
        choices:
          - 'interface'
          - 'bmc'
          - 'bond'
          - 'bridge'
      name:
        description:
          - Interface's DNS name
        type: str
      subnet_id:
        description:
          - Foreman subnet ID of IPv4 interface
        type: int
      subnet6_id:
        description:
          - Foreman subnet ID of IPv6 interface
        type: int
      domain_id:
        description:
          - Foreman domain ID of interface. Required for primary interfaces on managed hosts.
        type: int
      identifier:
        description:
          - Device identifier, e.g. eth0 or eth1.1
        type: str
      managed:
        description:
          - Should this interface be managed via DHCP and DNS smart proxy and should it be configured during provisioning?
        type: bool
      primary:
        description:
          - Should this interface be used for constructing the FQDN of the host?
          - Each managed hosts needs to have one primary interface.
        type: bool
      provision:
        description:
          - Should this interface be used for TFTP of PXELinux (or SSH for image-based hosts)?
          - Each managed hosts needs to have one provision interface.
        type: bool
      username:
        description:
          - Only for BMC interfaces.
        type: str
      password:
        description:
          - Only for BMC interfaces.
        type: str
      provider:
        description:
          - Interface provider, e.g. IPMI. Only for BMC interfaces.
        type: str
        choices:
          - 'IPMI'
          - 'SSH'
      virtual:
        description:
          - Alias or VLAN device
        type: bool
      tag:
        description:
          - VLAN tag, this attribute has precedence over the subnet VLAN ID. Only for virtual interfaces.
        type: str
      mtu:
        description:
          - MTU, this attribute has precedence over the subnet MTU.
        type: int
      attached_to:
        description:
          - Identifier of the interface to which this interface belongs, e.g. eth1. Only for virtual interfaces.
        type: str
      mode:
        description:
          - Bond mode of the interface, e.g. balance-rr. Only for bond interfaces.
        type: str
        choices:
          - 'balance-rr'
          - 'active-backup'
          - 'balance-xor'
          - 'broadcast'
          - '802.3ad'
          - 'balance-tlb'
          - 'balance-alb'
      attached_devices:
        description:
          - Identifiers of attached interfaces, e.g. ['eth1', 'eth2'].
          - For bond interfaces those are the slaves. Only for bond and bridges interfaces.
        type: list
        elements: str
      bond_options:
        description:
          - Space separated options, e.g. miimon=100. Only for bond interfaces.
        type: str
      compute_attributes:
        description:
          - Additional compute resource specific attributes for the interface.
        type: dict
extends_documentation_fragment:
  - theforeman.foreman.foreman
  - theforeman.foreman.foreman.entity_state
  - theforeman.foreman.foreman.host_options
  - theforeman.foreman.foreman.nested_parameters
  - theforeman.foreman.foreman.operatingsystem
'''

EXAMPLES = '''
- name: "Create a host"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    hostgroup: my_hostgroup
    state: present

- name: "Create a host with build context"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    hostgroup: my_hostgroup
    build: true
    state: present

- name: "Create an unmanaged host"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    managed: false
    state: present

- name: "Create a VM with 2 CPUs and 4GB RAM"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    compute_attributes:
      cpus: 2
      memory_mb: 4096
    state: present

- name: "Create a VM and start it after creation"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    compute_attributes:
      start: "1"
    state: present

- name: "Create a VM on specific ovirt network"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    interfaces_attributes:
    - type: "interface"
      compute_attributes:
        name: "nic1"
        network: "969efbe6-f9e0-4383-a19a-a7ee65ad5007"
        interface: "virtio"
    state: present

- name: "Create a VM with 2 NICs on specific ovirt networks"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    interfaces_attributes:
    - type: "interface"
      primary: true
      compute_attributes:
        name: "nic1"
        network: "969efbe6-f9e0-4383-a19a-a7ee65ad5007"
        interface: "virtio"
    - type: "interface"
      name: "new_host_nic2"
      managed: true
      compute_attributes:
        name: "nic2"
        network: "969efbe6-f9e0-4383-a19a-a7ee65ad5008"
        interface: "e1000"
    state: present

- name: "Delete a host"
  theforeman.foreman.host:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "new_host"
    state: absent
'''

RETURN = '''
entity:
  description: Final state of the affected entities grouped by their type.
  returned: success
  type: dict
  contains:
    hosts:
      description: List of hosts.
      type: list
      elements: dict
'''

from ansible_collections.theforeman.foreman.plugins.module_utils.foreman_helper import (
    ensure_puppetclasses,
    ForemanEntityAnsibleModule,
    HostMixin,
)


class ForemanHostModule(HostMixin, ForemanEntityAnsibleModule):
    pass


def main():
    module = ForemanHostModule(
        foreman_spec=dict(
            name=dict(required=True),
            hostgroup=dict(type='entity'),
            location=dict(type='entity'),
            organization=dict(type='entity'),
            enabled=dict(type='bool'),
            managed=dict(type='bool'),
            build=dict(type='bool'),
            ip=dict(),
            mac=dict(),
            comment=dict(),
            owner=dict(type='entity', resource_type='users', flat_name='owner_id'),
            owner_group=dict(type='entity', resource_type='usergroups', flat_name='owner_id'),
            owner_type=dict(invisible=True),
            provision_method=dict(choices=['build', 'image', 'bootdisk']),
            image=dict(type='entity', scope=['compute_resource']),
            compute_attributes=dict(type='dict'),
            interfaces_attributes=dict(type='list', elements='dict', options=dict(
                mac=dict(),
                ip=dict(),
                ip6=dict(),
                type=dict(choices=['interface', 'bmc', 'bond', 'bridge']),
                name=dict(),
                subnet_id=dict(type='int'),
                subnet6_id=dict(type='int'),
                domain_id=dict(type='int'),
                identifier=dict(),
                managed=dict(type='bool'),
                primary=dict(type='bool'),
                provision=dict(type='bool'),
                username=dict(),
                password=dict(no_log=True),
                provider=dict(choices=['IPMI', 'SSH']),
                virtual=dict(type='bool'),
                tag=dict(),
                mtu=dict(type='int'),
                attached_to=dict(),
                mode=dict(choices=[
                    'balance-rr',
                    'active-backup',
                    'balance-xor',
                    'broadcast',
                    '802.3ad',
                    'balance-tlb',
                    'balance-alb',
                ]),
                attached_devices=dict(type='list', elements='str'),
                bond_options=dict(),
                compute_attributes=dict(type='dict'),
            )),
        ),
        mutually_exclusive=[
            ['owner', 'owner_group']
        ],
        required_by=dict(
            image=('compute_resource',),
        ),
    )

    # additional param validation
    if '.' not in module.foreman_params['name']:
        module.fail_json(msg="The hostname must be FQDN")

    if not module.desired_absent:
        if 'build' in module.foreman_params and module.foreman_params['build']:
            # When 'build'=True, 'managed' has to be True. Assuming that user's priority is to build.
            if 'managed' in module.foreman_params and not module.foreman_params['managed']:
                module.warn("when 'build'=True, 'managed' is ignored and forced to True")
            module.foreman_params['managed'] = True
        elif 'build' not in module.foreman_params and 'managed' in module.foreman_params and not module.foreman_params['managed']:
            # When 'build' is not given and 'managed'=False, have to clear 'build' context that might exist on the server.
            module.foreman_params['build'] = False

        if 'mac' in module.foreman_params:
            module.foreman_params['mac'] = module.foreman_params['mac'].lower()

        if 'owner' in module.foreman_params:
            module.foreman_params['owner_type'] = 'User'
        elif 'owner_group' in module.foreman_params:
            module.foreman_params['owner_type'] = 'Usergroup'

        if 'interfaces_attributes' in module.foreman_params:
            filtered = [nic for nic in ({k: v for k, v in obj.items() if v} for obj in module.foreman_params['interfaces_attributes']) if nic]
            module.foreman_params['interfaces_attributes'] = filtered

    with module.api_connection():
        if not module.desired_absent:
            module.auto_lookup_entities()
        expected_puppetclasses = module.foreman_params.pop('puppetclasses', None)
        entity = module.run()
        if not module.desired_absent and 'environment_id' in entity:
            ensure_puppetclasses(module, 'host', entity, expected_puppetclasses)


if __name__ == '__main__':
    main()
