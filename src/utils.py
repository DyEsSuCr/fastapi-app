from typing import Any


def parse_to_list(origins_or_hosts: Any) -> list[str]:
    if isinstance(origins_or_hosts, str) and not origins_or_hosts.startswith('['):
        return [v.strip() for v in origins_or_hosts.split(',')]
    elif isinstance(origins_or_hosts, list):
        return origins_or_hosts
    raise ValueError(f'Invalid value for CORS or Trusted Hosts: {origins_or_hosts}')
