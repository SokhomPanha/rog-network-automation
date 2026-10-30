# MikroTik automation

**Device:** `MT-HOTSPOT`  
**Management:** `192.168.71.157`

The MikroTik keeps the existing Guest Hotspot on VLAN 500 and contains a guarded,
disabled-by-default Staff Hotspot design for VLAN 200 (`staff-vlan`). Its
operational interface name remains `vlan200-ground`. The Staff change is not a
simple portal toggle: current Staff clients use Core `192.168.20.1` as their
gateway, so the Hotspot requires a coordinated routing cutover that makes
MikroTik `192.168.20.2` the Staff client gateway while preserving the Core SVI.

Main files:

- `configure.yml` — existing MikroTik baseline maintenance.
- `verify.yml` — read-only verification.
- `backup.yml` — RouterOS export/backup workflow.
- `guest_portal.yml` / `guest_voucher.yml` — existing Guest service.
- `staff_hotspot.yml` — prepares the Staff profile, users, portal and service but
  keeps it disabled.
- `staff_hotspot_architecture.yml` — guarded live Staff gateway/routing cutover.
- `staff_hotspot_rollback.yml` — restores the original Staff DHCP gateway and
  removes Staff-only enforcement rules.
- `vars.yml` — non-secret design variables. Staff credentials come from Vault.

Do not run the Staff architecture playbook until the Core-side cutover has been
reviewed with `docs/STAFF_HOTSPOT_ARCHITECTURE.md`. All live changes require
explicit variables/tags and are disabled by default.

Safe checks from the repository root:

```bash
python3 shared/scripts/validate.py
ansible-playbook devices/mikrotik/verify.yml --syntax-check --ask-vault-pass
```

For a real Staff test, renew the client DHCP lease after cutover. Before login,
Internet should redirect/block; after valid login, normal Internet/YouTube should
work while FortiGate enforces the separate Facebook/TikTok Staff policy.

Portal presentation assets live in `files/staff_hotspot/` (uploaded to
`hotspot-staff`) and `files/guest_hotspot/` (uploaded to `hotspot`). Both use
matching, independent copies of `portal-style.css` for the login, connected,
status, logout and error pages. The pages use local assets only and no longer
reference logos; the existing image files are retained.

Staff still submits a username and password using the existing HTTP-CHAP
`doLogin()` / `hexMD5` flow. Guest still accepts one voucher/coupon code and uses
the existing `submitVoucher()` flow. Keep the existing RouterOS `md5.js`,
`redirect.html` and `rlogin.html` files in place; they are not supplied or replaced
by these source folders. The existing HTML-directory settings remain
`hotspot-staff` for Staff and `hotspot` for Guest.

For a presentation-only update, copy the five HTML pages and `portal-style.css`
from each source folder into its corresponding existing router directory.
Do not run the Staff preparation, architecture or baseline playbooks just to
refresh the UI: those entry points also manage network/service configuration.
The source changes alone do not deploy anything to a device.
