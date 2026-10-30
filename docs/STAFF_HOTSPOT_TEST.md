# Staff Hotspot test plan

Record screenshots/CLI evidence only from real tests. Do not mark a test passed
because a playbook completed.

| Test | Action | Expected result |
| --- | --- | --- |
| 1 | Connect Staff endpoint and renew DHCP | VLAN 200 (`staff-vlan`) address, gateway/DNS `192.168.20.2` |
| 2 | Browse before login | Redirect to ROG Tower Staff Wi-Fi login or Internet blocked |
| 3 | Enter wrong password | Authentication rejected |
| 4 | Enter valid Staff Vault-backed account | Authentication succeeds and Internet becomes available |
| 5 | Open YouTube | Allowed normally |
| 6 | Open Facebook | Blocked by the Staff FortiGate policy |
| 7 | Open TikTok | Blocked by the Staff FortiGate policy |
| 8 | Access management/protected subnets | Blocked by existing/Staff isolation controls |
| 9 | Test Guest VLAN 500 | Existing Guest Hotspot still works |
| 10 | Check logs | MikroTik Hotspot and FortiGate events correspond to the real test |

Useful endpoint checks:

```text
Windows: ipconfig /all
Linux:   ip route; resolvectl status
```

Useful MikroTik read-only checks include `/ip hotspot active print`, `/ip dhcp-server
lease print`, `/ip firewall filter print stats where comment~"ROG-STAFF"`, and
`/log print where topics~"hotspot"`.
