from django.shortcuts import render
from django.http import Http404

from .dummy_data import HOSTELS, bed_counts, get_hostel, get_room, hostel_counts


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


def _with_hostel_display_data(hostel):
    return {
        **hostel,
        "counts": hostel_counts(hostel),
        "review_percent": round((hostel["review"] / 5) * 100),
    }


def home(request):
    hostels = [_with_hostel_display_data(hostel) for hostel in HOSTELS]
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
    hostel = get_hostel(hostel_slug)
    if hostel is None:
        raise Http404("Hostel not found")

    rooms = [{**room, "counts": bed_counts(room)} for room in hostel["rooms"]]
    return render(
        request,
        "hostels/hostel_detail.html",
        {
            "hostel": {**hostel, "counts": hostel_counts(hostel)},
            "rooms": rooms,
        },
    )


def room_detail(request, hostel_slug, room_slug):
    hostel = get_hostel(hostel_slug)
    if hostel is None:
        raise Http404("Hostel not found")

    room = get_room(hostel, room_slug)
    if room is None:
        raise Http404("Room not found")

    return render(
        request,
        "hostels/room_detail.html",
        {
            "hostel": hostel,
            "room": {**room, "counts": bed_counts(room)},
        },
    )
