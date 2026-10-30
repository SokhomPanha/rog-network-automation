# Final validation checklist

Use this only as a checklist; mark items complete from real device/client evidence.

## Core
- [ ] VLANs 71/100/200/500/600/900 are correct; VLAN 200 is named `staff-vlan`; no active VLAN 300/400 design.
- [ ] Inter-VLAN routing works as intended.
- [ ] Staff protected-network controls work.
- [ ] Port-Channel 10/LACP is healthy.
- [ ] NTP, syslog and SNMP remain healthy.

## FortiGate
- [ ] Dual WAN/SD-WAN health checks are healthy.
- [ ] Existing NAT and Guest/management policies are unchanged.
- [ ] Staff normal Internet works.
- [ ] YouTube works from Staff.
- [ ] Facebook is blocked from Staff.
- [ ] TikTok is blocked from Staff.
- [ ] Filtering limitation/method is documented accurately.

## MikroTik
- [ ] Guest Hotspot and vouchers still work.
- [ ] Staff receives VLAN 200 (`staff-vlan`) address with gateway/DNS `192.168.20.2` after cutover.
- [ ] Staff Internet is unavailable/redirected before login.
- [ ] Wrong Staff password is rejected.
- [ ] Correct Staff credentials authenticate successfully.
- [ ] Staff protected-network isolation remains effective.

## WLC / wireless
- [ ] `ROG_STAFF_WIFI` remains mapped to VLAN 200 (`staff-vlan`).
- [ ] `ROG-GUEST` remains mapped to VLAN 500.
- [ ] No fake AP/client evidence is used.
- [ ] Final RF test is performed with a compatible physical Cisco AP when available.

## Monitoring and automation
- [ ] Core, MikroTik, WLC and FortiGate appear healthy in Zabbix.
- [ ] Central syslog is receiving expected device/security messages.
- [ ] Telegram alert/recovery workflow still works.
- [ ] NTP synchronization is correct.
- [ ] Repository static validation is clean.
- [ ] New final device backups were taken and kept private.
