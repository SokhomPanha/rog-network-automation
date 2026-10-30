# Cisco C9800-CL wireless controller

`WLC-ROG-TOWER` uses management `192.168.71.156` and wireless management Vlan100 `192.168.10.2`. The existing network CLI/libssh connection and SSH key authentication remain in inventory. On the saved device, OOB management is on **Vlan1**, despite the management subnet being called VLAN71 elsewhere; the baseline preserves that detail and the existing default route via `192.168.71.1`.

The newer `20260909T061248Z` operational evidence supersedes the older full WLC backup for WLAN state: `ROG_STAFF_WIFI`, WLAN ID5, maps to `ROG-STAFF-POLICY`/VLAN200; `ROG-GUEST`, ID4, maps to `ROG-GUEST-POLICY`/VLAN500. Guest Layer 2 remains open for its MikroTik captive portal; Staff retains its vaulted WPA2 PSK. The new Staff Hotspot provides an additional login in the data path, without inventing a WLAN web-auth configuration.

VLAN 200 has the display name `staff-vlan`. The Staff SSID and policy names remain
`ROG_STAFF_WIFI` and `ROG-STAFF-POLICY`.

- `configure.yml`: final VLAN100/200/500 trunk, WMI and two WLAN/policy mappings. Requires `rog_allow_live_changes=true`.
- `verify.yml`: actual WLAN, policy, country, AP and client counts plus network/monitoring checks. Requires `allow_device_connections=true`.
- `backup.yml`: private running-config backup and SHA256. Requires `allow_device_connections=true`.
- `vars.yml` and `templates/`: nonsecret settings. The existing `vault_staff_wlan_psk` and `wlc_snmp_community` come from encrypted Vault storage.

From the repository root, use the configured Vault password source or `--ask-vault-pass`:

```sh
ansible-playbook devices/wlc/configure.yml --syntax-check
ansible-playbook devices/wlc/verify.yml -e allow_device_connections=true
ansible-playbook devices/wlc/backup.yml -e allow_device_connections=true
ansible-playbook devices/wlc/configure.yml -e rog_allow_live_changes=true
```

NTP/syslog provisioning additionally requires `wlc_enable_monitoring_services=true` because the old backup does not establish their final configuration. Existing settings are otherwise left in place. An empty `wlc_country_code` preserves the current radio country; inspect `show wireless country configured` before intentionally supplying a country. No country is guessed.

The latest saved evidence still contains unused old floor policy profiles/VLANs. Archived migration scripts document their history; active baseline code never creates those objects and does not delete unknown device state. The final trunk excludes the retired floor VLANs. Verify actual device cleanup separately before claiming they are absent live.

There are no verified joined physical APs or real wireless clients. Automated output is configuration evidence only. A compatible physical Cisco AP and client tests are still required; do not present zero-client output as successful RF testing. Roll back only from a fresh predeployment backup: older backups contain obsolete per-floor WLANs and should not be blindly restored.
