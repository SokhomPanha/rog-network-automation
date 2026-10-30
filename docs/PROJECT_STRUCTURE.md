# Project structure

`inventory/hosts.yml` is the only active inventory. Group names remain
`core_switch`, `fortigate`, `mikrotik`, `wireless_ac`, and `monitoring`
to preserve working connection settings. A new monitoring host represents the
existing server; its SSH user and installation details must be supplied.

Each device has one main folder with configure, verify, backup, public variables
and a README. Device-specific task files, templates, portal assets and controlled
migration entrypoints stay inside that folder. Shared Cisco backup/evidence
mechanics live under `shared/tasks/`; the two shared orchestration playbooks only
import device entrypoints.

| Location | Ownership |
| --- | --- |
| devices/core-switch | Final VLANs, original routing/ACL, LACP, guarded Staff routing |
| devices/fortigate | Staff policy, preserved WAN/NAT, readback and rollback capture |
| devices/mikrotik | Guest services and real portal, Staff preparation/cutover/rollback |
| devices/wlc | Unified Staff/Guest WLANs, management, evidence; no fabricated APs |
| devices/zabbix | Existing-service boundary, API/service checks and confirmed-path backup |
| inventory/group_vars/all/main.yml | Safe defaults and repository-relative output paths |
| inventory/group_vars/*/vault.yml | Original encrypted device credentials |
| inventory/vault.example.yml | Public schema, outside automatic group variable loading |
| shared/scripts/validate.py | Offline validation, no network-device access |
| docs | Deployment instructions, test cases and honest evidence status |
| archive/legacy | Local historical automation, excluded from active imports and Git |
| backups/repository | Permission-restricted original source snapshot and hash manifest |
| backups, evidence | Local sensitive outputs, ignored by Git |

Original `playbooks/`, root `group_vars/`, `files/`, and `vars/` are
superseded. Exact original-file classifications are in the root cleanup report.
Archived files are reference material, not runnable compatibility wrappers.
