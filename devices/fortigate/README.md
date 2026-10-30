# FortiGate — ROG Tower Internet gateway

The saved 22 September configuration is the baseline: management/internal `192.168.71.158` on `port3`, HTTPAPI HTTPS port `8443`, WAN `port1` and `port2` in `virtual-wan-link`, and three EVAL firewall policies. The old inventory's `.153` address was stale. Inventory correction changes the controller target only.

| Policy | Source | Existing behavior |
| --- | --- | --- |
| 1 ROG-GUEST-INTERNET | 192.168.50.0/24 | Guest Internet, NAT and traffic logging |
| 10 ROG-MANAGEMENT-SERVERS-INTERNET | AP, management, monitoring and transit subnets | Existing Internet, NAT and logging |
| 11 ROG-STAFF-INTERNET | ROG-STAFF = 192.168.20.0/24 | Staff Internet, NAT and logging |

`configure.yml` changes only selected Staff filtering or existing SNMP settings. It does not rewrite interfaces, routes, SD-WAN, health checks, NTP or Guest/management policy rules. Old network objects can remain on the appliance for historical reference; active automation does not recreate obsolete VLANs.

## Files and safe defaults

- `vars.yml`: expected baseline and maintained blocked-domain list.
- `configure.yml`: requires `rog_allow_live_changes=true` and an explicit feature tag.
- `verify.yml`: read-only baseline checks; requires `allow_device_connections=true`.
- `backup.yml`: protected full configuration backup; requires `allow_device_connections=true`.
- `tasks/` and `templates/`: implementation shared by the entrypoints.

The existing encrypted FortiGate Vault still provides `fortigate_api_token`. All FortiOS modules now consistently use that name, including SNMP (the old SNMP playbook used a different token variable). SNMP community is `vault_snmp_community` in the shared encrypted Vault. No token value is copied into source or documentation. Existing certificate-validation behavior remains in inventory; changing that behavior is a separate reviewed task.

## Why the default is domain filtering

Application Control is preferred when a valid appliance signature set can be demonstrated. The repository has no evidence of current Facebook/TikTok signatures or FortiGuard entitlement. Fortinet documents trial restrictions including three policies, low-encryption operation and no FortiGuard support; this is not evidence that every Application Control function is unavailable. Verify the actual appliance before choosing signature-based filtering. See [Fortinet trial limitations](https://docs.fortinet.com/document/fortigate/7.6.3/administration-guide/441460).

Static URL filtering itself works without a subscription, with FortiGuard categories disabled. HTTPS hostname matching needs SSL inspection. EVAL TLS capability cannot be established from a saved profile definition, so `static_url` requires an explicit successful lab capability test. See [Fortinet's unlicensed static URL guidance](https://community.fortinet.com/fortigate-3/technical-tip-use-static-url-filtering-without-fortiguard-web-filter-license-94525).

The default `fqdn` method creates apex and wildcard address objects for dedicated Facebook, Messenger and TikTok service/CDN domains. Existing policy 11 accepts destinations **outside** their group using `dstaddr-negate`. Blocked destinations fall through to implicit deny. No fourth policy is added. Preflight stops if the current three-policy layout, exact source networks or NAT/interfaces have drifted; another broad accept policy would defeat the exclusion. [Fortinet policy semantics](https://docs.fortinet.com/document/fortigate/7.6.6/cli-reference/333889629/config-firewall-policy) document destination negation.

This is partial domain/IP coverage, not perfect application blocking. Wildcard objects learn from visible DNS responses and expire with TTL; DoH, cached answers, unseen CDN names, alternate IPs, VPNs/proxies and IPv6 require separate testing. Shared IPs may cause collateral blocking. Google/YouTube domains and whole shared CDN providers are excluded from the block list, but real video playback must still be tested. [Fortinet's wildcard FQDN guidance](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/217973) explains DNS learning and DoH limitations.

`static_url` instead attaches `ROG-STAFF-WEB-FILTER` with FortiGuard scanning disabled and a dedicated certificate-inspection profile. Only Staff QUIC is blocked, allowing ordinary browsers to retry HTTPS over TCP. SNI/ECH, native applications, unknown domains and HTTPS inspection limitations still apply. It does not enable deep inspection or install a client CA.

## Commands from the repository root

Offline checks do not connect to the firewall:

```bash
python3 shared/scripts/validate.py
ansible-playbook devices/fortigate/configure.yml --syntax-check --ask-vault-pass
```

Only during the reviewed deployment window:

```bash
ansible-playbook devices/fortigate/backup.yml --ask-vault-pass -e allow_device_connections=true
ansible-playbook devices/fortigate/verify.yml --ask-vault-pass --tags verify -e allow_device_connections=true
# First prove the DNS forwarding path with the checks in the test document.
ansible-playbook devices/fortigate/configure.yml --ask-vault-pass --tags staff_filter -e rog_allow_live_changes=true -e fortigate_staff_dns_visibility_confirmed=true
ansible-playbook devices/fortigate/verify.yml --ask-vault-pass --tags verify,staff_filter -e allow_device_connections=true
```

To deliberately choose URL inspection after testing its TLS/QUIC support:

```bash
ansible-playbook devices/fortigate/configure.yml --ask-vault-pass --tags staff_filter -e rog_allow_live_changes=true -e fortigate_staff_filter_method=static_url -e fortigate_staff_tls_inspection_confirmed=true
ansible-playbook devices/fortigate/verify.yml --ask-vault-pass --tags verify,staff_filter -e allow_device_connections=true -e fortigate_staff_filter_method=static_url
```

The `monitoring` tag preserves SNMPv2c community ID 10 restricted to Zabbix `192.168.60.10`. It uses the shared Vault community; it does not change the token or monitoring server.

## Rollback and evidence

The first filter deployment saves `backups/FGT-ROG-TOWER-staff-filter-before.json` with destination matching and exact existing UTM/profile attachment fields. It is never overwritten automatically. Take a complete device backup first. To undo filtering:

```bash
ansible-playbook devices/fortigate/configure.yml --ask-vault-pass --tags staff_filter_rollback -e rog_allow_live_changes=true
```

This restores captured Staff fields only. Dedicated filter objects remain unused for review. Keep the original snapshot; if a later intentional baseline needs a new one, archive the old snapshot and override `fortigate_staff_rollback_file` with a new private filename. If current topology fails preflight, review the full backup and restore the Staff fields through the management console instead of forcing unrelated policy changes.

No live results were generated during repository cleanup. Follow [Staff Internet tests](../../docs/STAFF_INTERNET_POLICY_TEST.md), including YouTube playback and Guest/management regression checks. After MikroTik Hotspot deployment, repeat them: FortiGate must still see the original Staff source `192.168.20.x`, not a masqueraded transit/management address.
