import asyncio
import openpyxl
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.lead import Lead


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(
                Lead.id,
                Lead.address,
                Lead.published_offer_at,
                Lead.created_offer_at
            )
            .where(Lead.published_offer_at.isnot(None))
            .where(Lead.created_offer_at.isnot(None))
        )
        rows = result.all()
        print(f"Всего записей: {len(rows)}")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Скорость парсера"
        ws.append(["ID", "Адрес", "Опубликовано на ЦИАН", "Добавлено в систему", "Задержка (сек)", "Задержка"])

        for row in rows:
            diff = row.published_offer_at - row.created_offer_at
            seconds = diff.total_seconds()
            real_seconds = abs(seconds) - 7200
            if real_seconds < 0:
                real_seconds = 0
            minutes = int(real_seconds // 60)
            secs = int(real_seconds % 60)
            ws.append([
                row.id,
                row.address,
                str(row.published_offer_at),
                str(row.created_offer_at),
                int(real_seconds),
                f"{minutes}м {secs}с"
            ])

        wb.save("parser_speed.xlsx")
        print("Сохранено в parser_speed.xlsx")


asyncio.run(main())
