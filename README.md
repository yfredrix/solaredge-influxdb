# solaredge-influxdb
Uploading data from Solar Edge API towards Influxdb on a regular interval of 5 minutes to prevent rate limiting

## Usage

Run the application with:

```bash
python -m solaredge_influxdb
```

Available CLI options:

- `--config-path`: Path to the configuration file.
- `--latitude`: Latitude of the solar panels.
- `--longitude`: Longitude of the solar panels.
- `--api-key`: API key for the SolarEdge API.
- `--timewindow`: Optional time window in minutes used for the technical-data lookback window.
- `--force`: Collect data even outside the daylight window.

Examples:

```bash
python -m solaredge_influxdb --config-path ./solaredge_influxdb/config.toml --timewindow 15
python -m solaredge_influxdb --force
```

By default, the application skips data collection outside the configured daylight window. Use `--force` to collect data even after sundown.
