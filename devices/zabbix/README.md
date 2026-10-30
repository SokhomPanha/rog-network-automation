# Zabbix / monitoring server

Management/web: `192.168.71.159`; monitoring: `192.168.60.10`.
The original repository contained device SNMP provisioning but no Zabbix server,
database, syslog receiver, Telegram, NTP server or scheduler implementation.
Their live state is unknown; existing external services are preserved.

- `configure.yml` reports this boundary and makes no server changes.
- `verify.yml` queries API version and checks selected SSH service states.
  Set the real `zabbix_web_url`, SSH username in Vault, and service names first.
- `backup.yml` retrieves confirmed configuration paths plus an existing
  consistent database dump. Supply `zabbix_backup_paths` and
  `zabbix_database_dump_path`; it never guesses a database engine.
- `vars.yml` contains public settings only.

Live read/backup commands require `-e allow_device_connections=true`.
The default API URL is an unverified deployment assumption.
[Zabbix API documentation](https://www.zabbix.com/documentation/7.0/en/manual/api)
describes the unauthenticated `apiinfo.version` call. A responding API is not
proof that devices, triggers or notification actions work.

Retain existing SNMP, syslog, Telegram problem/recovery actions and NTP.
Verify recent values on all four network devices, an actual syslog arrival,
time offset and a real problem followed by recovery notification.
Do not put tokens, message payloads with credentials, or raw logs in Git.

Only build Staff log triggers after sanitized real logs identify stable event
fields. Proposed checks: repeated Staff login failures and FortiGate policy11
denies; a deny alone does not identify a Facebook/TikTok application. New
triggers are deliberately not invented from unavailable logs.
