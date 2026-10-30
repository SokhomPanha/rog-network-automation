# Automation

Run from the repository root. The tested controller has Ansible core 2.21.3,
Python 3.12 and the collection versions pinned in `requirements.yml`.
Install those collections on another controller with
`ansible-galaxy collection install -r requirements.yml`.
Use existing SSH keys and host trust; do not commit private keys.

| Device | Preserved connection |
| --- | --- |
| Core | ansible.netcommon.network_cli, cisco.ios, Paramiko, existing privilege15 account |
| FortiGate | fortinet.fortios HTTPAPI, HTTPS port8443, root VDOM, existing API Vault token |
| MikroTik | community.routeros network_cli, libssh, existing SSH key |
| WLC | cisco.ios network_cli, libssh, existing SSH key |
| Zabbix | SSH for selected server checks/backups; HTTP API version from controller |

The old lab settings disable SSH host-key checking and FortiGate certificate
validation; they were retained to preserve connection behavior. Portal SCP uses
known-host verification. Establish trust before a deployment.

## Offline checks

```bash
ansible-inventory --graph
python3 shared/scripts/validate.py
ansible-playbook devices/core-switch/configure.yml --syntax-check --ask-vault-pass
ansible-playbook devices/fortigate/configure.yml --syntax-check --ask-vault-pass
ansible-playbook devices/mikrotik/configure.yml --syntax-check --ask-vault-pass
ansible-playbook devices/wlc/configure.yml --syntax-check --ask-vault-pass
ansible-playbook devices/zabbix/verify.yml --syntax-check --ask-vault-pass
```

The Python validator also checks every additional deployment entrypoint and shared
orchestrator. It preserves Vaults in place and checks the actual source files
without decrypting credentials. It cannot validate decrypted
credential names/values or hardware command acceptance. Check mode is not a
substitute for offline validation and can still contact devices.

## Controls

| Variable/tag | Meaning |
| --- | --- |
| allow_device_connections=true | Allow deliberate verify or backup access |
| rog_allow_live_changes=true | Allow selected configuration operations |
| staff_filter | FortiGate Staff-only filtering |
| staff_filter_rollback | Restore captured original policy fields |
| staff_hotspot | Prepare disabled Staff Hotspot, users and portal |
| staff_hotspot_architecture_change | Deliberate Core/MikroTik cutover |
| enable_staff_hotspot_architecture_change=true | Second required cutover gate |
| guest_hotspot | Existing Guest maintenance; consult MikroTik README |
| verify / backup / monitoring / ntp | Device-specific tasks; see --list-tags |

Use `ansible-playbook <file> --list-tasks --list-tags --ask-vault-pass` to review
selection. Do not use `--tags all,never` or skip guard tasks. Baseline Core/MikroTik
configuration refuses to undo an already activated Staff architecture.

## Secrets and output

Existing encrypted Vaults were retained byte for byte and moved under inventory.
Create `inventory/group_vars/all/vault.yml` using Ansible Vault and the public
schema. Reuse the actual installed SNMP community until a coordinated rotation;
setting a different community on only one device breaks monitoring. Passwords
and sensitive module results use `no_log`.

Do not use `--diff`, inventory `--list/--vars`, or verbose debug output in a public
report: these can expose decrypted values. Raw backups, evidence, migration source
and temporary outputs are private/ignored. Ignoring files does not erase old Git
history. Raw backup/evidence files previously tracked were removed from the index
while their local copies were retained.

## Backups and automation schedule

`shared/backup.yml` invokes all five device backup entrypoints. Network-device
backups are restricted local files. Zabbix requires actual configuration paths
and a pre-created consistent database dump; it never guesses the database engine.
Use fresh backups before and after each maintenance window and verify restoration
in the lab. The pre-cleanup tarball is a source rollback, not a replacement for
device backups.

No installed scheduler was supplied. If scheduling later, use an external Vault
password helper with restricted permissions, absolute repository paths and
`ansible-playbook shared/backup.yml -e allow_device_connections=true`; confirm
interactive backups first. Never put a Vault password or API token on a cron
command line or overwrite an existing external schedule.
