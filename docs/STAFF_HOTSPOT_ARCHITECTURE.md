# Staff Hotspot architecture

## Why a routing change is required

The validated Staff network currently uses VLAN 200 (`staff-vlan`, `192.168.20.0/24`) with
the Core SVI `192.168.20.1` as the client default gateway. MikroTik also has
`192.168.20.2`, but Staff Internet traffic currently routes through the Core to
FortiGate and therefore bypasses MikroTik. A MikroTik Hotspot cannot reliably
authenticate traffic it does not forward.

## Guarded target path

After an approved cutover, DHCP advertises MikroTik `192.168.20.2` as the Staff
default gateway and DNS server:

`Staff client -> VLAN 200 -> MikroTik Hotspot -> VLAN 900/Core -> FortiGate -> Internet`

The Core keeps `192.168.20.1/24` for VLAN 200. Two more-specific `/25` static
routes direct return traffic for the whole Staff `/24` through MikroTik
`192.168.99.2`, providing symmetric forwarding while the connected `/24` remains
present. The Core also receives Staff anti-bypass/transit ACLs. MikroTik preserves
the Staff source address toward FortiGate so policy 11 can still identify
`192.168.20.0/24`.

## Safety gates

The cutover is disabled by default. It requires all of the following:

- `rog_allow_live_changes=true`
- `enable_staff_hotspot_architecture_change=true`
- explicit `staff_hotspot_architecture_change` tag
- `staff_hotspot_core_cutover_confirmed=true`
- `staff_hotspot_preflight_confirmed=true`

The preparation playbook creates the Staff Hotspot, portal and Vault-backed users
but keeps the service disabled. Preparation and cutover are intentionally
separate.

## Recommended order

1. Back up Core and MikroTik.
2. Verify current Staff/Guest behavior and save outputs.
3. Prepare Staff Hotspot users/portal while still disabled.
4. Review MikroTik preflight output: Guest Hotspot, DNS, default route, FastTrack,
   bypass bindings, walled garden and wildcard users.
5. Apply the Core anti-bypass/transit rules and more-specific Staff return routes.
6. Activate the MikroTik Staff Hotspot and change only the Staff DHCP gateway/DNS
   to `192.168.20.2`.
7. Renew a Staff endpoint DHCP lease; confirm gateway/DNS are `.20.2`.
8. Run the real tests in `STAFF_HOTSPOT_TEST.md`.

## Rollback

If Staff access fails:

1. Run the MikroTik Staff rollback playbook to restore DHCP gateway
   `192.168.20.1`, public DNS values, disable Staff Hotspot and remove Staff-only
   enforcement/NAT rules.
2. Run the Core architecture playbook with
   `staff_hotspot_architecture_action=rollback` to restore the original Staff ACL,
   remove the two `/25` routes and detach the transit ACL.
3. Renew Staff DHCP leases and verify the original path works.

Guest VLAN 500, Guest vouchers, dual WAN and WLC mappings are not intentionally
changed by this Staff cutover.
