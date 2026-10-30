# Staff Internet policy — real test procedure

Status: **prepared, not deployed or browser-tested during cleanup**. Expected results below are acceptance criteria, not evidence of success. There are no joined physical APs or real wireless clients in the recorded WLC baseline; a wired VLAN 200 (`staff-vlan`) client can test routing/filtering now, and a compatible Cisco AP is needed for later RF tests.

## Scope and capability decision

Staff is `192.168.20.0/24`, address object `ROG-STAFF`, policy 11. Keep Guest policy 1, management/server policy 10 and both WAN members unchanged. Repository preflight verifies this exact policy count and source separation before writes. The saved route returns internal traffic through Core `192.168.71.155`.

Default `fqdn` filtering excludes a maintained Facebook/TikTok destination group from the existing Staff allow policy; excluded traffic reaches implicit deny. A fourth deny rule would exceed the known three-policy EVAL design. No Google/YouTube domain is deliberately blocked. The list includes apex and subdomains for Facebook, its dedicated CDNs and Messenger, plus TikTok's dedicated domains/CDNs. Shared providers such as all of Akamai or CloudFront are deliberately excluded to avoid unrelated outages.

Fortinet documents [unlicensed static URL filtering](https://community.fortinet.com/fortigate-3/technical-tip-use-static-url-filtering-without-fortiguard-web-filter-license-94525), but HTTPS requires inspection. [EVAL restrictions](https://docs.fortinet.com/document/fortigate/7.6.3/administration-guide/441460) and missing evidence of active signatures mean neither working application control nor TLS inspection is assumed. The optional `static_url` deployment requires a real appliance capability test, disables FortiGuard categories and blocks Staff QUIC to permit HTTPS/TCP fallback. Native apps and ECH must be tested separately.

## Baseline and read-only preflight

1. Back up all devices as described in the deployment runbook. Record the test client's IP, gateway, DNS servers, browser and time.
2. Before changing anything, record Google, YouTube, Facebook and TikTok behavior from Staff, Guest and management. Confirm Staff currently has working Internet and takes the intended path.
3. On FortiGate, inspect these read-only commands via the existing management console. Keep full output private; licensing output may contain identifiers.

```text
get system status
diagnose autoupdate versions
show firewall policy
show firewall address ROG-STAFF
show router static
show system sdwan
show system session-helper
diagnose sys sdwan health-check
```

Confirm policy 11 uses only `ROG-STAFF`, `port3`, `virtual-wan-link` and NAT. Confirm no other accept rule can match Staff. Policy count must remain three. Confirm UDP DNS session helper exists. The configuration-only verifier does not prove that WAN health probes pass.

For FQDN mode, from the Staff client use ordinary DNS through its configured resolver:

```bash
nslookup www.facebook.com
nslookup www.tiktok.com
nslookup www.youtube.com
```

Observe DNS forwarding through FortiGate, preferably using a short packet capture restricted to port 53. Press Ctrl-C when done:

```text
diagnose sniffer packet any 'port 53' 4 20 l
```

Do not substitute a resolver bypassing FortiGate. If MikroTik serves cached answers, a fresh lookup may produce no upstream traffic: wait for TTL expiry or use a controlled fresh lookup and document the result. Fortinet's [DNS helper explanation](https://docs.fortinet.com/document/fortigate/7.6.2/administration-guide/143041/dns-session-helpers) describes passive learning. Confirming this path is necessary before setting `fortigate_staff_dns_visibility_confirmed=true`; it does not guarantee complete future blocking.

After deployment repeat DNS lookups and inspect:

```text
diagnose firewall fqdn list
diagnose test application dnsproxy 6
```

Confirm the `ROG-STAFF-BLOCK-*` objects have appropriate learned/resolved addresses. An empty wildcard object cannot block its unknown destinations. [Fortinet FQDN guidance](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/217973) explains expiry and encrypted DNS limitations. Do not mark a block successful merely because an object exists.

## Client acceptance tests

Run these from a real Staff client, using fresh browser sessions. After Hotspot deployment, authenticate first for tests 1–4, then repeat the pre-login tests in `STAFF_HOTSPOT_TEST.md`. Close old app sessions; existing FortiGate sessions and cached content can survive configuration changes. Avoid a global session clear, which interrupts unrelated users.

| Test | Real action | Expected result | Actual result / evidence |
| --- | --- | --- | --- |
| 1: YouTube from Staff | Open YouTube, search, start multiple videos and seek within one | Allowed, including video playback | NOT RUN |
| 2: Facebook from Staff | Open Facebook in a fresh browser; test mobile site and app separately | Blocked; no feed/login use | NOT RUN |
| 3: TikTok from Staff | Open TikTok, attempt fresh video playback; test app separately | Blocked; no fresh feed/playback | NOT RUN |
| 4: Google/general web | Search Google and open unrelated HTTPS and HTTP sites | Allowed | NOT RUN |
| 5: Guest Internet | Use an existing Guest voucher/login, browse and play YouTube | Existing Guest behavior unchanged | NOT RUN |
| 6: Staff DNS | Resolve permitted sites with the normal configured resolver | DNS still works | NOT RUN |
| 7: Management Internet | Repeat the baseline browser tests from management | Existing behavior unchanged | NOT RUN |
| 8: Staff isolation | Try protected management/monitoring destinations | Existing security restrictions remain | NOT RUN |
| 9: Dual WAN | Inspect both existing SD-WAN member/health-check states | Existing healthy behavior preserved | NOT RUN |

A failed `ping` or a `curl -I` response is insufficient proof of application blocking. Capture the actual browser/app result, client source, time and relevant firewall session/log. For default FQDN exclusion, blocked packets fall to **implicit deny**, so do not expect a policy-11 web-filter event or branded block page. Implicit-deny logging may be disabled in the existing configuration; use a narrowly scoped diagnostic capture if necessary, and do not enable global verbose logging casually. Static URL mode can emit `webfilter` block events under policy 11; verify those actual events before adding monitoring triggers.

Record remaining bypasses honestly: secure DNS/DoH, IPv6, VPN/proxy, previously cached DNS, alternate CDN domains and shared IP collateral effects. Test ordinary browser defaults as well as any controlled DNS test. If Facebook/TikTok works under the intended client settings, record FAIL and do not declare the requirement complete. Domain coverage needs maintenance; this repository does not claim complete application-level enforcement.

## Return path after Staff Hotspot

Confirm FortiGate sees each authenticated Staff session with source `192.168.20.x` and policy ID 11. MikroTik must preserve this source. If MikroTik masquerades Staff to `.99.2` or `.71.157`, traffic could match management policy 10 and bypass the Staff filter. Check both outbound sessions and return traffic; a configuration-only assertion cannot establish the real packet path.

## Rollback

Use the captured policy snapshot, not a guessed `unset`:

```bash
ansible-playbook devices/fortigate/configure.yml --ask-vault-pass --tags staff_filter_rollback -e rog_allow_live_changes=true
```

This restores the first captured destination and profile attachment fields. Re-test Staff Internet, Guest Internet, management, both WANs and monitoring. Keep before/after evidence privately, redact credentials and avoid publishing full configuration exports.
