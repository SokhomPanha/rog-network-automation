# Final deployment runbook

This runbook intentionally separates safe repository validation from live network
changes. Run commands from the repository root and use the existing encrypted
Vaults. Never paste Vault passwords or API tokens into shell history.

## 1. Static validation

```bash
python3 shared/scripts/validate.py
ansible-inventory -i inventory/hosts.yml --graph
```

Resolve every real validation error before touching devices.

## 2. Back up and verify current state

Run each device backup/verify workflow with device connections explicitly enabled.
Keep the resulting raw backups private. Confirm Staff Internet, Guest Hotspot,
FortiGate WANs, monitoring/syslog/Telegram and WLC logical WLAN mappings still
match the validated baseline.

## 3. Staff FortiGate filtering

The default repository method is the conservative FQDN destination exclusion.
Before enabling it, confirm the actual Staff DNS path is visible to FortiGate and
set `fortigate_staff_dns_visibility_confirmed=true`. If the lab cannot provide
reliable FQDN resolution/visibility, do not claim complete application blocking.
The optional static URL method requires a separate verified TLS/QUIC capability
check on this exact EVAL appliance.

Deploy only the `staff_filter` tag, then use a real Staff client to test:
YouTube/general web allowed, Facebook/TikTok blocked. Guest and management must
remain unchanged. Keep the captured Staff policy rollback file.

## 4. Prepare Staff Hotspot (still disabled)

Create Staff accounts inside encrypted Vault data. Enable only the Staff Hotspot
preparation flag/tag. This uploads the real portal pages and creates the dedicated
Staff profile/users/service while keeping the service disabled.

## 5. Staff routing cutover

Read `STAFF_HOTSPOT_ARCHITECTURE.md`. This requires a maintenance window because
new DHCP leases will use MikroTik `192.168.20.2` instead of Core `.20.1`.

Apply the Core side first, then activate the guarded MikroTik cutover. Renew a
Staff client DHCP lease immediately and verify the gateway/DNS and symmetric path.
If anything is wrong, use the documented MikroTik rollback followed by Core
rollback.

## 6. End-to-end validation

Run all cases in `STAFF_HOTSPOT_TEST.md` and `STAFF_INTERNET_POLICY_TEST.md`.
Also verify Guest Hotspot, dual WAN, SNMP/Zabbix, syslog, Telegram and NTP.

## 7. Final backups and evidence

After successful real tests, take new configuration backups, save read-only CLI
outputs, and capture screenshots needed for the report. Do not place credentials,
raw Vault contents or sensitive device backups in the public report/repository.
