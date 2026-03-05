def format_lead_card(lead) -> str:
    return (
        f"🏠 <b>Новая квартира!</b>\n"
        f"💰 <b>Цена:</b> {lead.price:,} ₽/мес\n"
        f"📍 <b>Адрес:</b> {lead.address}\n"
        f"🚇 <b>Метро:</b> {lead.metro_station or 'Не указано'}\n"
        f"📐 <b>Параметры:</b> {lead.area} м², {lead.rooms_count}-к, {lead.floor}/{lead.floors_count} эт.\n"
        f"📍 <b>Номер:</b> {lead.phone_number}\n"
        f"🔗 <a href='{lead.external_url}'>Открыть на Циан</a>"
    )