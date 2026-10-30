# Cleanup report

Initial audit: 20260927T164639Z. No device connections or live changes performed.

104 original files inspected by inventory/content audits and device-specific review. Existing uncommitted edits are part of the baseline. All originals will be retained in the private snapshot before refactoring.

## Findings

- Multiple old provisioners can restore retired VLANs 300/400; staged migrations are historical, not safe default entry points.
- Two MikroTik main variable files are byte-for-byte duplicates; FortiGate variables and Vault are outside the authoritative inventory tree.
- Inventory targets FortiGate .153, while the requested architecture and latest saved configuration use .158.
- WLC ansible_become contains the invalid value `falsec`.
- Existing encrypted Vaults will be moved unchanged. Plaintext SNMP settings and sensitive saved configurations need private handling.
- No Zabbix server provisioning, Telegram integration, or backup scheduler exists in the supplied source; preserve external services and document the evidence gap.
- No abandoned Windows Wi-Fi popup experiment was found.
- Saved configurations are historical evidence, not proof of current device behavior.

## Original-file classification

KEEP, MERGE, MOVE, RENAME, ARCHIVE, DELETE-CANDIDATE and MANUAL-REVIEW describe disposition. No destructive source deletion is planned. Renames are represented by explicit destination mappings after consolidation.

| Original file | Classification | Reason |
| --- | --- | --- |
| `NETWORK_SERVICES_GUIDE.md` | ARCHIVE | Historical audit with obsolete paths; superseded by current docs. |
| `ansible.cfg` | KEEP | Preserve existing data or working automation. |
| `backups/CORE-SW-20260904T113808Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260904T113808Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260904T161633Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260904T161633Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260909T032156Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260909T032156Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260922T093602Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/CORE-SW-20260922T093602Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260825T083410Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260902T070423Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260903T025154Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260903T025412Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260909T033739Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/FGT-ROG-TOWER-20260922T093430Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260907T065049Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260907T065049Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260907T105504Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260907T105504Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260908T050741Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260908T050741Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260909T033517Z.conf` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/WLC-ROG-TOWER-20260909T033517Z.conf.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/mikrotik/MT-HOTSPOT-20260826T070748Z.rsc` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/mikrotik/MT-HOTSPOT-20260909T033254Z.rsc` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `backups/mikrotik/MT-HOTSPOT-20260909T033408Z.rsc` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/CORE-SW-20260904T114138Z-evidence.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/CORE-SW-20260904T114138Z-evidence.txt.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/CORE-SW-20260904T161749Z-evidence.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/CORE-SW-20260904T161749Z-evidence.txt.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/FGT-ROG-TOWER-sdwan-current.json` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/FGT-ROG-TOWER-sdwan-current.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260907T071700Z-evidence.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260907T071700Z-evidence.txt.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260908T050816Z-evidence.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260908T050816Z-evidence.txt.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260909T061248Z-evidence.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/WLC-ROG-TOWER-20260909T061248Z-evidence.txt.sha256` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/mikrotik/MT-HOTSPOT-current-20260826T071227Z.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `evidence/mikrotik/MT-HOTSPOT-current-20260903T073319Z.txt` | KEEP | Private rollback/evidence; retain locally and exclude from future Git tracking. |
| `files/mikrotik_hotspot/alogin.html` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/cover.png` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/error.html` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/img/rgc-logo.png` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/login.html` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/logo.png` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/logout.html` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/rgc-style-v2.css` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `files/mikrotik_hotspot/status.html` | MOVE | Keep Guest portal assets under devices/mikrotik/files/. |
| `group_vars/fortigate/main.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `group_vars/fortigate/vault.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `group_vars/mikrotik/main.yml` | DELETE-CANDIDATE | Exact duplicate of inventory/group_vars/mikrotik/main.yml; archive original instead of destroying it. |
| `group_vars/mikrotik/vault.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `inventory/group_vars/core_switch/main.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `inventory/group_vars/core_switch/vault.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `inventory/group_vars/mikrotik/main.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `inventory/group_vars/wireless_ac/main.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |
| `inventory/hosts.yml` | KEEP | Preserve existing data or working automation. |
| `inventory/hosts.yml.before-core` | ARCHIVE | Historical inventory; authoritative inventory is inventory/hosts.yml. |
| `inventory/hosts.yml.before-wlc` | ARCHIVE | Historical inventory; authoritative inventory is inventory/hosts.yml. |
| `playbooks/backup_core_switch.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/backup_fortigate.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/backup_mikrotik.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/backup_wireless_ac.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/cleanup_wlc_legacy_staff.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/collect_core_switch.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/collect_mikrotik.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/collect_sdwan.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/collect_wireless_ac.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_core_lacp_ground.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_core_snmp.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_core_switch.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_fortigate_policies.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_fortigate_policies_eval.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_fortigate_snmp.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_internet_sla.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_dhcp.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_hotspot.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_ip_addresses.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_pools.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_routing.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_security.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_snmp.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_vlans.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_mikrotik_voucher.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_monitoring_vlan600.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_wlc_security_stage3b.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_wlc_snmp.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_wlc_trunk_stage1.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_wlc_wlans_stage3a.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/configure_wlc_wmi_stage2.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/deploy_mikrotik_portal.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/migrate_unified_staff.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/prepare_unified_staff_core.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/test_core_vlans.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_core_switch.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_fortigate.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_fortigate_policies.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_fortigate_policies_eval.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_mikrotik.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_unified_mikrotik.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `playbooks/verify_wireless_ac.yml` | MERGE | Consolidate into the corresponding device folder; preserve original in legacy archive. |
| `vars/wlc_wlan_vault.yml` | MOVE | Consolidate under inventory; preserve encrypted Vault bytes and resolve duplicate variables. |

## Completion and validation

Pending refactor, static validation, and final documentation.

## Final completion update

The uploaded repository represented a partially completed Codex refactor. This
final pass completed the missing local-only pieces without contacting any network
device:

- Confirmed the authoritative inventory uses FortiGate `192.168.71.158` and final
  VLANs 71/100/200/500/600/900.
- Confirmed no active VLAN 300/400 references remain in current automation.
- Added the missing MikroTik device README and real Staff Hotspot portal pages.
- Added the missing Staff Hotspot architecture, test, deployment runbook and final
  validation documents referenced by the root README.
- Kept Staff Hotspot routing changes disabled by default and separated preparation
  from cutover/rollback.
- Preserved Guest Hotspot, WLC mappings, monitoring boundaries and existing device
  configuration logic.
- Improved the offline validator so YAML/Jinja checks still run on a workstation
  that does not have Ansible installed; Ansible inventory/syntax checks are marked
  `SKIP` there and must be run on the user's Ansible controller.
- Removed only empty superseded top-level directories from this working copy; no
  device backup/evidence/Vault content was deleted.

No live Staff Hotspot, FortiGate filter, AP, browser, RF, Zabbix, Telegram or
network-device result is claimed by this cleanup. Those remain real deployment
and validation tasks.
