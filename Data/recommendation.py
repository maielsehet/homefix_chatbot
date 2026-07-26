from Data.technician import TECHNICIANS


def recommend_technician(history: str):

    history = history.lower()

    if "سخان" in history:
        device = "سخان"

    elif "غسالة" in history:
        device = "غسالة"

    elif "ثلاجة" in history:
        device = "ثلاجة"

    elif "تكييف" in history:
        device = "تكييف"

    else:
        return None

    technicians = TECHNICIANS.get(device)

    if not technicians:
        return None

    technicians = sorted(
        technicians,
        key=lambda x: x["rating"],
        reverse=True
    )

    return technicians[0]