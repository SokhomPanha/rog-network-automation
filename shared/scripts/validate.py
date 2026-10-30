#!/usr/bin/env python3
"""Offline source checks. Never connects to network devices or decrypts Vaults."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import shutil
import yaml
from jinja2 import Environment

ROOT = Path(__file__).resolve().parents[2]
ACTIVE = ("devices", "shared", "inventory")
class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError("duplicate YAML key: " + str(key))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)

def main():
    errors, checked, vaults = [], [], []
    files = [p for folder in ACTIVE for p in (ROOT / folder).rglob("*") if p.is_file()]
    files += [ROOT / "requirements.yml"]
    playbooks = []
    for p in sorted(files):
        if p.suffix not in (".yml", ".yaml", ".j2"):
            continue
        rel = str(p.relative_to(ROOT))
        source = p.read_text()
        if source.startswith("$ANSIBLE_VAULT;"):
            vaults.append(rel)
            continue
        try:
            if p.suffix == ".j2":
                Environment(extensions=["jinja2.ext.do"]).parse(source)
            else:
                data = yaml.load(source, Loader=UniqueLoader)
                if isinstance(data, list) and any(isinstance(x, dict) and ("hosts" in x or "import_playbook" in x) for x in data):
                    playbooks.append(p)
                def inspect(value):
                    if isinstance(value, dict):
                        for key, val in value.items():
                            if key in ("import_playbook", "import_tasks", "include_tasks", "ansible.builtin.import_tasks", "ansible.builtin.include_tasks") and isinstance(val, str) and "{{" not in val:
                                if not (p.parent / val).is_file():
                                    raise ValueError("missing include " + val)
                            if key == "vars_files":
                                for name in val:
                                    if isinstance(name, str) and "{{" not in name and not (p.parent / name).is_file():
                                        raise ValueError("missing vars file " + name)
                            if key == "no_log" and not isinstance(val, bool) and not (isinstance(val, str) and "{{" in val):
                                raise ValueError("no_log must be boolean or templated")
                            inspect(val)
                    elif isinstance(value, list):
                        for child in value:
                            inspect(child)
                inspect(data)
            checked.append(rel)
        except Exception as exc:
            errors.append(rel + ": " + str(exc))
    records = []
    def run(label, argv, cwd, env):
        if shutil.which(argv[0]) is None:
            records.append({"check": label, "status": "SKIP", "returncode": None, "output": f"{argv[0]} is not installed on this controller"})
            print("SKIP " + label + f" ({argv[0]} not installed)")
            return
        proc = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        records.append({"check": label, "status": "PASS" if proc.returncode == 0 else "FAIL", "returncode": proc.returncode, "output": proc.stdout.strip()})
        print(("PASS " if proc.returncode == 0 else "FAIL ") + label)
        if proc.returncode:
            errors.append(label)
            print(proc.stdout)
    env = dict(os.environ)
    env["ANSIBLE_NOCOLOR"] = "1"
    env["ANSIBLE_LOCAL_TEMP"] = "/tmp/rog-ansible-static"
    env.pop("ANSIBLE_VAULT_PASSWORD_FILE", None)
    run("authoritative inventory graph", ["ansible-inventory", "-i", str(ROOT / "inventory/hosts.yml"), "--graph"], ROOT, env)
    # Syntax checking imports source but does not evaluate device credentials.
    env["ANSIBLE_CONFIG"] = str(ROOT / "ansible.cfg")
    for p in sorted(playbooks):
        relative = p.relative_to(ROOT)
        run("syntax " + str(relative), ["ansible-playbook", "-i", str(ROOT / "inventory/hosts.yml"), "--syntax-check", str(p)], ROOT, env)
    report = {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Offline only; authoritative inventory graph and syntax on actual source files. Encrypted Vault values are not evaluated. No device/browser/RF verification.",
        "yaml_and_jinja_files": checked,
        "encrypted_vaults_preserved_not_decrypted": vaults,
        "checks": records,
        "errors": errors,
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files) if p.suffix in (".yml", ".yaml", ".j2") and not p.read_bytes().startswith(b"$ANSIBLE_VAULT;")},
    }
    out = ROOT / "docs/STATIC_VALIDATION.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Checked {len(checked)} YAML/Jinja sources and {len(playbooks)} playbooks; {len(errors)} errors.")
    for error in errors:
        print("ERROR " + error)
    return bool(errors)

if __name__ == "__main__":
    sys.exit(main())
