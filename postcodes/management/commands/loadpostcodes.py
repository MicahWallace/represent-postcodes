import csv
import logging
import sys

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from postcodes.models import Postcode

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports a CSV file without headers and columns for code,latitude,longitude,locality,region from the given filename or standard input.'

    def handle(self, *args, **options):
        if len(args) == 1:
            f = open(args[0])
        else:
            f = sys.stdin

        reader = csv.DictReader(f, fieldnames=['code', 'latitude', 'longitude', 'locality', 'region'])
        for row in reader:
            try:
                Postcode(
                    code=row['code'].upper(),
                    centroid=Point(float(row['longitude']), float(row['latitude'])),
                    city=row['locality'].decode('iso-8859-1'),
                    province=row['region'],
                ).save()
            except ValidationError as e:
                log.error("%s: %r" % (row['code'], e))
