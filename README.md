# ROG Tower network automation

One device = one main automation folder. This repository maintains the existing
lab and prepares Staff Internet filtering and Staff Hotspot authentication.
**The cleanup did not connect to devices or deploy configuration.** The new
features still require a controlled lab deployment and real client tests.

| Device | Management | Role |
| --- | --- | --- |
| CORE-SW | 192.168.71.155 | Inter-VLAN routing, Staff ACL, LACP Port-channel10 |
| FGT-ROG-TOWER | 192.168.71.158 | FortiOS 7.6.2 EVAL, NAT, dual WAN, SD-WAN |
| MT-HOTSPOT | 192.168.71.157 | Guest Hotspot, DHCP, prepared Staff Hotspot |
| WLC-ROG-TOWER | 192.168.71.156 | Wireless management 192.168.10.2, WLAN mappings |
| ZABBIX | 192.168.71.159 | Monitoring 192.168.60.10; existing external services |

| VLAN | Purpose | Network | Gateway |
| --- | --- | --- | --- |
| 71 | Management / out-of-band | 192.168.71.0/24 | Existing management routing preserved |
| 100 | Wireless / AP management | 192.168.10.0/24 | Core 192.168.10.1 |
| 200 | staff-vlan (Staff) | 192.168.20.0/24 | Core 192.168.20.1 before optional cutover |
| 500 | Guest | 192.168.50.0/24 | MikroTik 192.168.50.1 |
| 600 | Monitoring / security | 192.168.60.0/24 | Core 192.168.60.1 |
| 900 | Core–MikroTik transit | 192.168.99.0/30 | Core .1 / MikroTik .2 |

VLANs 300/400 are retired. Old provisioners are archived and never imported.

```text
inventory/                 one hosts.yml, group_vars and encrypted device Vaults
devices/
  core-switch/             configure.yml verify.yml backup.yml vars.yml README.md
  fortigate/               configure.yml verify.yml backup.yml vars.yml README.md
  mikrotik/                configure.yml verify.yml backup.yml vars.yml README.md
  wlc/                     configure.yml verify.yml backup.yml vars.yml README.md
  zabbix/                  configure.yml verify.yml backup.yml vars.yml README.md
shared/                    shared tasks, backup/verify entrypoints, offline validator
docs/                      architecture, deployment, tests and validation evidence
archive/legacy/            private historical source; do not execute
backups/                   private device backups and pre-cleanup source snapshot
```

Current Staff path is VLAN200 → Core .20.1 → FortiGate → Internet.
Guest path remains VLAN500 → MikroTik Guest Hotspot → transit/Core →
FortiGate → Internet. The Staff WLAN stays `ROG_STAFF_WIFI` on VLAN200;
`ROG-GUEST` stays on VLAN500.

The optional Staff design advertises MikroTik .20.2 as the client gateway, retains
the Core .20.1 address, adds symmetric return routes and blocks direct Core bypass.
Separate profiles, server-bound Vault accounts and an actual MikroTik login portal
provide authentication. This changes routing and needs an outage window.
Read [Staff architecture](docs/STAFF_HOTSPOT_ARCHITECTURE.md) before enabling it.
All architecture switches default to false and need a separate explicit tag.

FortiGate filtering changes existing Staff policy11 only. Default FQDN exclusion
covers maintained Facebook/TikTok domains; stronger static URL filtering is an
optional capability-gated method. Neither is claimed to provide perfect app
blocking. YouTube/Google domains are excluded from the block list, but real browser
testing is required. See [filter tests](docs/STAFF_INTERNET_POLICY_TEST.md).

Start with safe local checks:

```bash
ansible-inventory --graph
python3 shared/scripts/validate.py
```

The validator checks YAML, templates, references, inventory and Ansible syntax
against the actual source files. It never contacts devices or decrypts Vaults.
For a full credential-aware syntax check, use `--syntax-check --ask-vault-pass`.
Dependencies and deployment controls are in [automation](docs/AUTOMATION.md).

Existing encrypted device Vaults were moved intact under inventory. Create new
shared secrets with:

```bash
ansible-vault create inventory/group_vars/all/vault.yml
```

Use the schema in [inventory/vault.example.yml](inventory/vault.example.yml);
do not copy placeholder values into a deployment. Backup/evidence/archive output
is private and ignored. Historical commits can still contain old device secrets;
rotate exposed credentials before sharing the repository.

Back up every device before changes, then verify the current network. Apply and
test FortiGate filtering, prepare the disabled Staff portal, perform the guarded
routing cutover, and test Staff and Guest authentication. Verify WAN, monitoring
and alerts, then take final backups. Exact commands and rollback procedures are in
[the deployment runbook](docs/FINAL_DEPLOYMENT_RUNBOOK.md).

Device SNMP automation is preserved. The supplied source did not contain Zabbix
server installation, Telegram actions, central syslog receiver or NTP-server
configuration. Their existing deployment is left intact; verify it using
[final validation](docs/FINAL_VALIDATION.md). No Staff monitoring trigger is
invented without actual log examples.

The WLC currently has no joined physical APs or real wireless clients. Wired
VLAN200/500 clients can test routing and portals; final RF evidence requires a
compatible Cisco AP. No fake AP, client, browser or Windows Wi-Fi popup evidence
is included.

See [cleanup report](CLEANUP_REPORT.md), [project structure](docs/PROJECT_STRUCTURE.md),
[Staff authentication tests](docs/STAFF_HOTSPOT_TEST.md) and
[static validation evidence](docs/STATIC_VALIDATION.json).
