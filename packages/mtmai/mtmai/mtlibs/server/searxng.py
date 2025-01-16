from pathlib import Path

from mtmlib.mtutils import bash

searxng_dir_base = "/app/searxng"
searxng_setting_file = Path(searxng_dir_base) / "settings.yml"



def install_searxng():
    script = f"""git clone https://github.com/searxng/searxng {searxng_dir_base} \
    && cd /app/searxng \
    && python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -U --no-cache-dir pip setuptools wheel pyyaml && pip install --no-cache-dir -e ."""
    bash(script)


def start_searxng():
    # settings 完整配置文档： https://github.com/searxng/searxng/blob/master/utils/templates/etc/searxng/settings.yml
    config = """use_default_settings: true

general:
  debug: true
  instance_name: "SearXNG"

search:
  # Filter results. 0: None, 1: Moderate, 2: Strict
  safe_search: 0
  autocomplete: 'duckduckgo'
  formats:
    - html
    - csv
    - json
    - rss

server:
  port: 18777
  bind_address: "0.0.0.0"
  secret_key: "feihuo321"
  limiter: false
  image_proxy: true
  # public URL of the instance, to ensure correct inbound links. Is overwritten
  # base_url: http://example.com/location

redis:
  # url: unix:///usr/local/searxng-redis/run/redis.sock?db=0
  url: false
ui:
  static_use_hash: true

# preferences:
#   lock:
#     - autocomplete
#     - method

enabled_plugins:
  - 'Hash plugin'
  - 'Self Informations'
  - 'Tracker URL remover'
  - 'Ahmia blacklist'
  # - 'Hostnames plugin'  # see 'hostnames' configuration below
  # - 'Open Access DOI rewrite'

# plugins:
#   - only_show_green_results"""
    Path(searxng_setting_file).write_text(config)
    bash(
        f'cd {searxng_dir_base}  && export SEARXNG_SETTINGS_PATH="{searxng_setting_file}" && source .venv/bin/activate && python searx/webapp.py'
    )


def run_searxng_server():
    bash(
        f'cd {searxng_dir_base}  && export SEARXNG_SETTINGS_PATH="{searxng_setting_file}" && . .venv/bin/activate && python searx/webapp.py &'
    )
