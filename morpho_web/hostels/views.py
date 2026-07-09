import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .dummy_data import HOSTELS, bed_counts, hostel_counts
from .models import Hostel, Room, Bed


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _slugify(value):
    value = str(value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9\-\s]", "", value).strip().lower()
    return re.sub(r"[\s]+", "-", value)


def _parse_remote_gender(tags):
    normalized = [tag.strip().lower() for tag in tags or []]
    if any("gents" in tag for tag in normalized):
        return "gents"
    if any("ladies" in tag for tag in normalized):
        return "ladies"
    return "mixed"


def _parse_remote_area(tags):
    for tag in tags or []:
        normalized = tag.strip()
        if normalized.lower() not in {"gents", "ladies"} and "review" not in normalized.lower():
            return normalized
    return "Unknown"


def _normalize_remote_logo(logo):
    if not logo:
        return None
    if isinstance(logo, str):
        if logo.startswith("data:") or logo.startswith("http://") or logo.startswith("https://"):
            return logo
        return f"data:image/png;base64,{logo}"
    return None


def _build_remote_rooms(rooms_value, vacant, occupied):
    bed_statuses = ["vacant"] * int(vacant) + ["occupied"] * int(occupied)
    total_beds = len(bed_statuses)

    if isinstance(rooms_value, int):
        room_count = max(1, rooms_value)
    elif isinstance(rooms_value, list):
        room_count = max(1, len(rooms_value))
    else:
        room_count = 1

    if total_beds == 0:
        return [{"slug": "room-1", "beds": []} for _ in range(room_count)]

    rooms = []
    for index in range(room_count):
        start = (total_beds * index) // room_count
        end = (total_beds * (index + 1)) // room_count
        beds = [
            {"code": f"bed-{i + 1}", "status": status}
            for i, status in enumerate(bed_statuses[start:end], start=start)
        ]
        rooms.append({"slug": f"room-{index + 1}", "beds": beds})

    return rooms


def _map_remote_hostel(hostel):
    rooms_value = hostel.get("rooms", [])
    vacant = hostel.get("vacant", 0)
    occupied = hostel.get("occupied", 0)
    rooms = _build_remote_rooms(rooms_value, vacant, occupied)

    rent_range = hostel.get("rent_range") or []
    price_min = rent_range[0] if len(rent_range) > 0 else 0
    price_max = rent_range[1] if len(rent_range) > 1 else price_min

    return {
        "id": hostel.get("id"),
        "slug": _slugify(hostel.get("name", "hostel")),
        "name": hostel.get("name", "Unnamed Hostel"),
        "area": _parse_remote_area(hostel.get("tags", [])),
        "gender": _parse_remote_gender(hostel.get("tags", [])),
        "warden": "Morpho Team",
        "summary": hostel.get("desc", ""),
        "status": hostel.get("status", "Open"),
        "capacity": int(vacant) + int(occupied),
        "occupied": int(occupied),
        "review": float(hostel.get("ratings", 0)) if hostel.get("ratings") is not None else 0,
        "price_min": price_min,
        "price_max": price_max,
        "logo": _normalize_remote_logo(hostel.get("logo")),
        "photos": [
            "https://images.unsplash.com/photo-1549187774-b4e9b0445b85?auto=format&fit=crop&w=1400&q=80"
        ],
        "rooms": rooms,
        "tags": hostel.get("tags", []),
    }


def _fetch_hostels_from_odoo():
    api_url = getattr(settings, "ODOO_HOSTELS_API_URL", None)
    if not api_url:
        return []

    payload = json.dumps({"params": {}}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    request_obj = urllib.request.Request(api_url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request_obj, timeout=getattr(settings, "ODOO_HOSTELS_API_TIMEOUT", 10)) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
            if isinstance(data, dict) and "result" in data and isinstance(data["result"], list):
                return [_map_remote_hostel(hostel) for hostel in data["result"]]
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return []

    return []


def _fetch_rooms_from_odoo(hostel_id):
    api_base = getattr(settings, "ODOO_HOSTELS_API_URL", None)
    if not api_base or not hostel_id:
        return []

    # derive rooms endpoint from base URL if possible
    rooms_url = api_base.replace('/fetch_hostels', '/fetch_rooms')
    payload = json.dumps({"params": {"hostel_id": hostel_id}}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(rooms_url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=getattr(settings, "ODOO_HOSTELS_API_TIMEOUT", 10)) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            if isinstance(data, dict) and "result" in data and isinstance(data["result"], list):
                out = []
                for r in data["result"]:
                    room_id = r.get("id")
                    room_num = r.get("room_number") or str(room_id)
                    beds = []
                    for b in r.get("beds", []):
                        beds.append({"code": b.get("id") or b.get("bed_number") or str(b.get("id")), "status": b.get("status"), "price": b.get("price")})
                    room_price = None
                    bed_prices = [b.get("price") for b in beds if b.get("price") is not None]
                    if bed_prices:
                        room_price = min(bed_prices)
                    out.append({"id": room_id, "slug": _slugify(room_num), "name": room_num, "beds": beds, "price": room_price})
                return out
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return []

    return []


def _fetch_beds_from_odoo(hostel_id, room_id):
    api_base = getattr(settings, "ODOO_HOSTELS_API_URL", None)
    if not api_base or not hostel_id or not room_id:
        return []

    beds_url = api_base.replace('/fetch_hostels', '/fetch_beds')
    payload = json.dumps({"params": {"hostel_id": hostel_id, "room_id": room_id}}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(beds_url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=getattr(settings, "ODOO_HOSTELS_API_TIMEOUT", 10)) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            if isinstance(data, dict) and "result" in data and isinstance(data["result"], list):
                out = []
                for b in data["result"]:
                    out.append({
                        "id": b.get("id"),
                        "code": b.get("bed_number") or str(b.get("id")),
                        "status": b.get("status"),
                        "price": b.get("price"),
                        "enquiry_mobile": b.get("enquiry_mobile"),
                        "enquiry_message": b.get("enquiry_message"),
                    })
                return out
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return []

    return []


def _with_hostel_display_data(hostel):
    return {
        **hostel,
        "counts": hostel_counts(hostel),
        "review_percent": round((hostel["review"] / 5) * 100),
    }


def _get_hostels():
    # Prefer database hostels when available
    qs = Hostel.objects.all()
    if qs.exists():
        out = []
        for h in qs:
            rooms = []
            for r in h.room_set.all():
                beds = [
                    {"code": b.code, "status": b.status, "price": b.price}
                    for b in r.bed_set.all()
                ]
                rooms.append({"id": r.pk, "slug": r.slug, "name": r.name, "beds": beds, "price": r.price})

            out.append(
                {
                    "id": h.pk,
                    "slug": h.slug,
                    "name": h.name,
                    "area": h.area or "Unknown",
                    "gender": h.gender or "mixed",
                    "warden": h.warden or "",
                    "summary": h.summary or "",
                    "status": h.status or "",
                    "capacity": h.capacity or sum(len(r["beds"]) for r in rooms),
                    "occupied": h.occupied or 0,
                    "review": float(h.review or 0),
                    "price_min": h.price_min or 0,
                    "price_max": h.price_max or (h.price_min or 0),
                    "logo": (h.logo.url if getattr(h, "logo") else None),
                    "photos": [p for p in (h.photos or "").split(",") if p],
                    "rooms": rooms,
                    "source": "db",
                    "tags": [],
                }
            )
        return out

    hostels = _fetch_hostels_from_odoo()
    return hostels if hostels else HOSTELS


def _get_hostel(hostel_slug):
    # Try DB first
    try:
        h = Hostel.objects.get(slug=hostel_slug)
        rooms = []
        for r in h.room_set.all():
            beds = [
                {
                    "code": b.code,
                    "status": b.status,
                    "price": b.price,
                    "enquiry_mobile": b.enquiry_mobile,
                    "enquiry_message": b.enquiry_message,
                }
                for b in r.bed_set.all()
            ]
            rooms.append({"id": r.pk, "slug": r.slug, "name": r.name, "beds": beds, "price": r.price})

        return {
            "id": h.pk,
            "slug": h.slug,
            "name": h.name,
            "area": h.area or "Unknown",
            "gender": h.gender or "mixed",
            "warden": h.warden or "",
            "summary": h.summary or "",
            "status": h.status or "",
            "capacity": h.capacity or sum(len(r["beds"]) for r in rooms),
            "occupied": h.occupied or 0,
            "review": float(h.review or 0),
            "price_min": h.price_min or 0,
            "price_max": h.price_max or (h.price_min or 0),
            "logo": (h.logo.url if getattr(h, "logo") else None),
            "photos": [p for p in (h.photos or "").split(",") if p],
            "rooms": rooms,
            "source": "db",
            "tags": [],
        }
    except Hostel.DoesNotExist:
        for hostel in _get_hostels():
            if hostel.get("slug") == hostel_slug:
                return hostel
    return None


def _find_room(hostel, room_slug):
    if not hostel or "rooms" not in hostel:
        return None
    room = next((room for room in hostel["rooms"] if room.get("slug") == room_slug), None)
    if room is not None:
        return room

    # If hostel is remote, try fetching fresh rooms from the API and search again
    if hostel.get("id"):
        fresh_rooms = _fetch_rooms_from_odoo(hostel.get("id"))
        for r in fresh_rooms:
            if r.get("slug") == room_slug:
                return r

    return None


def home(request):
    hostels = _get_hostels()
    hostels = [_with_hostel_display_data(hostel) for hostel in hostels]
    total_hostels = len(hostels)
    total_beds = sum(hostel["counts"]["total"] for hostel in hostels)
    vacant_beds = sum(hostel["counts"]["vacant"] for hostel in hostels)
    verified_hostels = sum(1 for hostel in hostels if hostel["status"] == "Open")
    average_review = round(
        sum(hostel["review"] for hostel in hostels) / total_hostels,
        1,
    )

    gender = request.GET.get("gender", "")
    location = request.GET.get("location", "").strip().lower()
    min_price = _to_int(request.GET.get("min_price"))
    max_price = _to_int(request.GET.get("max_price"))
    min_review = _to_float(request.GET.get("min_review"))
    sort = request.GET.get("sort", "vacancy_desc")

    if gender in {"ladies", "gents"}:
        hostels = [hostel for hostel in hostels if hostel["gender"] == gender]

    if location:
        hostels = [
            hostel
            for hostel in hostels
            if location in hostel["area"].lower() or location in hostel["name"].lower()
        ]

    if min_price is not None:
        hostels = [hostel for hostel in hostels if hostel["price_max"] >= min_price]

    if max_price is not None:
        hostels = [hostel for hostel in hostels if hostel["price_min"] <= max_price]

    if min_review is not None:
        hostels = [hostel for hostel in hostels if hostel["review"] >= min_review]

    sorters = {
        "vacancy_desc": lambda hostel: (-hostel["counts"]["vacant"], hostel["price_min"]),
        "price_asc": lambda hostel: (hostel["price_min"], -hostel["counts"]["vacant"]),
        "price_desc": lambda hostel: (-hostel["price_max"], -hostel["counts"]["vacant"]),
        "review_desc": lambda hostel: (-hostel["review"], -hostel["counts"]["vacant"]),
        "location_asc": lambda hostel: (hostel["area"], hostel["name"]),
    }
    sort = sort if sort in sorters else "vacancy_desc"
    hostels = sorted(hostels, key=sorters[sort])

    return render(
        request,
        "hostels/home.html",
        {
            "hostels": hostels,
            "stats": {
                "hostels": total_hostels,
                "satisfied_customers": 1250,
                "verified_hostels": verified_hostels,
                "vacant_beds": vacant_beds,
                "total_beds": total_beds,
                "average_review": average_review,
            },
            "filters": {
                "gender": gender,
                "location": request.GET.get("location", "").strip(),
                "min_price": request.GET.get("min_price", ""),
                "max_price": request.GET.get("max_price", ""),
                "min_review": request.GET.get("min_review", ""),
                "sort": sort,
            },
        },
    )


def hostel_detail(request, hostel_slug):
    hostel = _get_hostel(hostel_slug)
    if hostel is None:
        raise Http404("Hostel not found")
    # If this is a remote hostel (has an id and not from our DB), fetch rooms from the API
    if hostel.get("id") and hostel.get("source") != "db":
        rooms_raw = _fetch_rooms_from_odoo(hostel.get("id"))
    else:
        rooms_raw = hostel.get("rooms", [])

    rooms = [{**room, "counts": bed_counts(room)} for room in rooms_raw]
    return render(
        request,
        "hostels/hostel_detail.html",
        {
            "hostel": {**hostel, "counts": hostel_counts(hostel)},
            "rooms": rooms,
        },
    )


def room_detail(request, hostel_slug, room_slug):
    hostel = _get_hostel(hostel_slug)
    if hostel is None:
        raise Http404("Hostel not found")

    room = _find_room(hostel, room_slug)
    if room is None:
        raise Http404("Room not found")

    # If remote (not db source), refresh bed list from API (uses hostel id and room id when available)
    if hostel.get("id") and room.get("id") and hostel.get("source") != "db":
        beds = _fetch_beds_from_odoo(hostel.get("id"), room.get("id"))
        # normalize beds into expected structure and preserve bed price and enquiry details
        room = {
            **room,
            "beds": [
                {
                    "code": b.get("code"),
                    "status": b.get("status"),
                    "price": b.get("price"),
                    "enquiry_mobile": b.get("enquiry_mobile"),
                    "enquiry_message": b.get("enquiry_message"),
                }
                for b in beds
            ],
        }

    return render(
        request,
        "hostels/room_detail.html",
        {
            "hostel": hostel,
            "room": {**room, "counts": bed_counts(room)},
        },
    )
