# solaredge-influxdb

A Python application that fetches solar energy data from the [SolarEdge API](https://www.solaredge.com/) and stores it in [InfluxDB](https://www.influxdata.com/).

## Features

- Retrieves real-time and historical energy data from SolarEdge inverters
- Automatically calculates sunrise/sunset times to optimize API calls during daylight hours
- Stores data in InfluxDB for time-series analysis and visualization
- Supports multiple data types: inverters, meters, and equipment
- Timezone-aware data collection
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- InfluxDB instance (local or cloud)
- SolarEdge API key
- Latitude and longitude of your solar installation

## Installation

### Using Poetry

```bash
git clone https://github.com/yfredrix/solaredge-influxdb.git
cd solaredge-influxdb
poetry install
```

### Using pip

```bash
pip install solaredge-influxdb
```

### Using Docker

```bash
docker build -t solaredge-influxdb .
docker run -e API_KEY=<your_api_key> -e LATITUDE=<latitude> -e LONGITUDE=<longitude> solaredge-influxdb
```

## Configuration

Configuration is managed through environment variables and/or a `config.toml` file.

### Environment Variables

- `API_KEY` - Your SolarEdge API key (required)
- `LATITUDE` - Latitude of your solar installation (default: 52.3676)
- `LONGITUDE` - Longitude of your solar installation (default: 4.9041)
- `INFLUXDB_URL` - InfluxDB connection URL (configured in config.toml)
- `INFLUXDB_TOKEN` - InfluxDB authentication token (configured in config.toml)

### Configuration File

Create a `solaredge_influxdb/config.toml` file:

```toml
[influxdb]
url = "http://localhost:8086"
token = "your-influxdb-token"
org = "your-org"
bucket = "solaredge"
```

## Usage

### Running the Application

```bash
python -m solaredge_influxdb
```

### Running with Custom Parameters

```python
from solaredge_influxdb.app import app

app(
    api_key="your-api-key",
    latitude=52.3676,
    longitude=4.9041,
    timezone_str="Europe/Amsterdam",
    timewindow=15,  # Data collection interval in minutes
    force=False  # Force collection regardless of daylight
)
```

### Force Mode

Use `force=True` to collect data regardless of sunrise/sunset times:

```bash
API_KEY=<key> python -m solaredge_influxdb --force
```

## Data Collection

The application automatically:
1. Calculates local sunrise and sunset times
2. Only collects data during daylight hours (with configurable buffer time)
3. Fetches equipment data, meters, and energy metrics from SolarEdge
4. Stores the data in InfluxDB with timestamps

## Testing

Run the test suite:

```bash
poetry run pytest
```

With coverage:

```bash
poetry run pytest --cov=solaredge_influxdb
```

## Project Structure

```
solaredge_influxdb/
├── __init__.py
├── __main__.py
├── app.py              # Main application logic
├── config.toml         # Configuration file
├── influxdb/           # InfluxDB client and utilities
│   ├── __init__.py
│   └── client.py
└── solaredge/          # SolarEdge API client and data models
    ├── __init__.py
    ├── client.py
    ├── equipment.py
    ├── meters.py
    ├── models.py
    └── site.py
```

## Requirements

- Python 3.11+
- requests >= 2.31.0
- influxdb-client >= 1.40.0
- pydantic >= 2.6.1
- loguru >= 0.7.2
- pytz >= 2024.1
- astral >= 3.2

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/yfredrix/solaredge-influxdb).
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
