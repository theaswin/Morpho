from django.core.management.base import BaseCommand

from hostels.dummy_data import HOSTELS
from hostels.models import Hostel, Room, Bed


class Command(BaseCommand):
    help = "Import dummy hostels/rooms/beds into the database (idempotent)"

    def handle(self, *args, **options):
        created = 0
        for h in HOSTELS:
            hostel, _ = Hostel.objects.get_or_create(
                slug=h["slug"],
                defaults={
                    "name": h.get("name", h["slug"]),
                    "area": h.get("area", ""),
                    "gender": h.get("gender", "mixed"),
                    "warden": h.get("warden", ""),
                    "summary": h.get("summary", ""),
                    "status": h.get("status", ""),
                    "capacity": h.get("capacity"),
                    "occupied": h.get("occupied"),
                    "review": h.get("review", 0),
                    "price_min": h.get("price_min"),
                    "price_max": h.get("price_max"),
                    "photos": ",".join(h.get("photos", [])),
                },
            )
            # create/update rooms
            for r in h.get("rooms", []):
                room, _ = Room.objects.get_or_create(
                    hostel=hostel,
                    slug=r["slug"],
                    defaults={
                        "name": r.get("name", r["slug"]),
                        "floor": r.get("floor", ""),
                        "type": r.get("type", ""),
                        "price": r.get("price"),
                    },
                )
                # create/update beds
                for b in r.get("beds", []):
                    Bed.objects.get_or_create(
                        room=room,
                        code=b.get("code"),
                        defaults={
                            "status": b.get("status", "vacant"),
                            "price": b.get("price"),
                        },
                    )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Imported/updated {created} hostels from dummy data."))
