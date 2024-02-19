from django.core.management.base import BaseCommand, CommandError

from join_in.utils.image_generator import text_to_image


class Command(BaseCommand):
    help = "Test command to test some code"

    def add_arguments(self, parser):
        # parser.add_argument("poll_ids", nargs="+", type=int)
        pass

    def handle(self, *args, **options):
        text_to_image("Cees van Wieringen")
