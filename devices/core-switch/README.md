# Core switch

`CORE-SW` remains at `192.168.71.155`, using the existing IOS network CLI connection with Paramiko. The baseline follows the saved 22 September configuration: Staff gateway `192.168.20.1`, wireless management gateway `192.168.10.1`, monitoring gateway `192.168.60.1`, transit `192.168.99.1`, Staff ACL, default route to FortiGate `192.168.71.158`, Guest route through MikroTik, and LACP Port-channel10 on Gi1/0 and Gi1/3. Member ports are never reset to defaults.

VLAN 200 has the display name `staff-vlan`; its SVI remains `Vlan200`.

- `configure.yml`: merge the final baseline; requires `rog_allow_live_changes=true`.
- `verify.yml`: collect actual VLAN, route, ACL, LACP and monitoring output; requires `allow_device_connections=true`.
- `backup.yml`: save the running configuration locally with SHA256 and private permissions; requires `allow_device_connections=true`.
- `vars.yml` and `templates/`: reviewed nonsecret settings.
- `staff_hotspot_architecture.yml`: separate, disabled Staff path change and rollback.

Run commands from the repository root. Supply the existing Vault password through the configured protected password file or `--ask-vault-pass` when needed. Never paste passwords into command arguments.

```sh
ansible-playbook devices/core-switch/configure.yml --syntax-check
ansible-playbook devices/core-switch/verify.yml -e allow_device_connections=true
ansible-playbook devices/core-switch/backup.yml -e allow_device_connections=true
ansible-playbook devices/core-switch/configure.yml -e rog_allow_live_changes=true
```

Ordinary configuration does not move the Staff gateway. It refuses to reset an active Staff Hotspot ingress ACL. Archived old VLAN automation, the unused/shutdown Vlan254, and the shutdown Vlan1 in the backup are not recreated or removed. Existing unknown device configuration is preserved. Review current device drift before applying the baseline.

## Staff Hotspot cutover

The optional change retains `.20.1` on the Core. MikroTik becomes the Staff DHCP default gateway at `.20.2`. Two more-specific `/25` routes via `.99.2` make Staff replies traverse MikroTik. An ingress ACL denies all routed IPv4 traffic entering Core Vlan200 so manually selecting `.20.1` cannot bypass authentication. Local Layer 2 traffic to `.20.2` still works. A separate transit ingress ACL keeps the existing four protected destinations blocked for Staff while permitting Guest and other transit traffic.

The entrypoint requires its explicit tag, refuses check mode, and rejects Core IPv6 routing or Staff IPv6 addresses/enablement before cutover because RouterOS Hotspot authenticates IPv4. It does not silently disable IPv6.

This is a planned maintenance interruption: the ingress gate blocks current Staff Internet access until the MikroTik cutover and client DHCP renewal are complete. Stage the MikroTik portal, users, no-NAT rule, isolation and Hotspot first. Preserve console/OOB access and review [the architecture](../../docs/STAFF_HOTSPOT_ARCHITECTURE.md) and [deployment runbook](../../docs/FINAL_DEPLOYMENT_RUNBOOK.md).

```sh
ansible-playbook devices/core-switch/staff_hotspot_architecture.yml \
  --tags staff_hotspot_architecture_change \
  -e rog_allow_live_changes=true \
  -e enable_staff_hotspot_architecture_change=true
```

Rollback requires the same deliberate gates:

```sh
ansible-playbook devices/core-switch/staff_hotspot_architecture.yml \
  --tags staff_hotspot_architecture_change \
  -e rog_allow_live_changes=true \
  -e enable_staff_hotspot_architecture_change=true \
  -e staff_hotspot_architecture_action=rollback
```

Restore the MikroTik Staff DHCP gateway to `.20.1`, disable only the new Staff Hotspot and its dedicated rules, then renew Staff leases as described in the runbook. The Core rollback restores the original ingress ACL, removes the two specific routes and detaches the new transit ACL; it leaves all VLAN addresses and Guest settings intact. This design has only static validation until actual maintenance and client tests are recorded.
