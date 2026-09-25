#!/usr/bin/env python3
"""Check the book's external source-reading anchors at default-branch HEADs.

These are existence guards, not build, execution or deployment evidence.
"""
from pathlib import Path
import argparse
import re
import subprocess
import tempfile

REPOSITORIES = {
    'mqttsuite': ('SNodeC/mqttsuite', 'master'),
    'OpenWRT': ('SNodeC/OpenWRT', 'main'),
}
ANCHORS = {
    'mqttsuite': {
        'CMakeLists.txt': [r'project\('],
        'lib/CMakeLists.txt': [r'mqtt-mapping'],
        **{f'{app}/CMakeLists.txt': [app] for app in
           ('mqttbroker', 'mqttintegrator', 'mqttbridge', 'mqttcli', 'mqttstore')},
        'mqttbridge/lib/Mqtt.cpp': [r'Mqtt::onPublish\(', r'broker\.getBridge\(\)\.publish\('],
        'mqttstore/lib/Mqtt.cpp': [r'Mqtt::onPublish\(', r'storage\.store\('],
        'mqttstore/lib/MariaDbStorage.cpp': [r'MariaDbStorage::store\(', r'MariaDbStorage::storeProjections\('],
        'mqttcli/lib/Mqtt.cpp': [r'sendConnect\(', r'sendSubscribe\(', r'sendPublish\(', r'sendDisconnect\('],
        'mqttcli/SocketContextFactory.cpp': [r'create\(', r'iot::mqtt::SocketContext'],
    },
    'OpenWRT': {
        'net/snode.c/Makefile': [r'(?m)^PKG_VERSION\s*:=\s*2\.', r'(?m)^PKG_SOURCE_VERSION\s*:=',
                               r'Download/spdlog', r'HASH\s*:=\s*[0-9a-f]{64}',
                               r'FETCHCONTENT_FULLY_DISCONNECTED=ON', r'BuildSNodeCModule,net-un-phy,'],
    },
}


def check(name, root):
    errors = []
    for path, patterns in ANCHORS[name].items():
        source = root / path
        if not source.is_file():
            errors.append(f'{path}: missing path')
            continue
        text = source.read_text()
        for pattern in patterns:
            if not re.search(pattern, text):
                errors.append(f'{path}: missing anchor {pattern}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, help='Parent for fresh clones (must not contain their directories)')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='snodec-external-') as temporary:
        parent = args.work_dir or Path(temporary)
        parent.mkdir(parents=True, exist_ok=True)
        errors = []
        for name, (repository, branch) in REPOSITORIES.items():
            root = parent / name
            subprocess.run(['git', 'clone', '--depth', '1', '--single-branch', '--branch', branch,
                            f'https://github.com/{repository}.git', str(root)], check=True)
            head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            print(f'Observed {repository} {branch} HEAD: {head}', flush=True)
            errors.extend(f'{repository} {branch} has drifted from the manuscript anchors: {e}'
                          for e in check(name, root))
        for error in errors:
            print('ERROR: '+error)
        if not errors:
            print('External anchors passed; source existence only, not execution.')
        return bool(errors)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f'External anchor check could not verify HEAD: {error}')
