from loguru import logger
from argparse import ArgumentParser

from solaredge_influxdb import app

parser = ArgumentParser()
parser.add_argument(
    "--config-path",
    type=str,
    help="Path to configuration file",
)
parser.add_argument(
    "--latitude",
    type=float,
    help="Latitude of the solar panels",
)
parser.add_argument(
    "--longitude",
    type=float,
    help="Longitude of the solar panels",
)
parser.add_argument(
    "--api-key",
    type=str,
    help="API key for the SolarEdge API",
)

logger.info("Starting application; to get SolarEdge data into InfluxDB")

args = vars(parser.parse_args())
keys = list(args.keys())
for k in keys:
    if args[k] is None:
        args.pop(k)

app(**args)
logger.info("Application finished")
