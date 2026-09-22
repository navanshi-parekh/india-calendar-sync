import datetime
import re
import uuid
import pytz
from icalendar import Calendar, Event
from playwright.sync_api import sync_playwright

IST = pytz.timezone("Asia/Kolkata")

def scrape_calendar_events():
    url = "https://indiamacroindicators.co.in/india-economic-calendar"
    scraped_events = []

    print("Launching browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # Abort heavy analytics/tracking requests so the page loads instantly
        page = context.new_page()
        page.route("**/*clarity*", lambda route: route.abort())
        page.route("**/*psimg*", lambda route: route.abort())
        page.route("**/*google-analytics*", lambda route: route.abort())

        print("Navigating to calendar page...")
        # Use 'domcontentloaded' instead of 'networkidle' to avoid timeouts
        page.goto(url, wait_until="domcontentloaded", timeout=45000)

        # Wait for the main content container to mount
        print("Waiting for page elements to render...")
        page.wait_for_timeout(5000)

        # Find all text blocks across the calendar grid
        elements = page.locator("div, tr, li, [class*='calendar'], [class*='day']").all()

        seen_entries = set()
        now = datetime.datetime.now(IST)
        current_year = now.year

        keywords = [
            "CPI", "WPI", "GDP", "IIP", "Monetary Policy", "MPC",
            "Trade Deficit", "Forex", "Inflation", "PMI"
        ]

        for el in elements:
            try:
                text = el.inner_text().strip()
                if not text or len(text) > 300:
                    continue

                if any(kw.lower() in text.lower() for kw in keywords):
                    lines = [line.strip() for line in text.split("\n") if line.strip()]
                    if not lines:
                        continue

                    signature = " | ".join(lines[:2])
                    if signature in seen_entries:
                        continue
                    seen_entries.add(signature)

                    # Extract day number
                    day_match = re.search(r"\b([1-9]|[12][0-9]|3[01])\b", text)
                    month_match = re.search(
                        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", text, re.I
                    )

                    day = int(day_match.group(1)) if day_match else now.day
                    month_str = month_match.group(1) if month_match else now.strftime("%b")

                    # Indicator name is usually the prominent text line
                    title = [l for l in lines if any(kw.lower() in l.lower() for kw in keywords)]
                    event_title = title[0] if title else lines[0]

                    scraped_events.append({
                        "title": event_title,
                        "day": day,
                        "month": month_str,
                        "description": " \n".join(lines)
                    })
            except Exception:
                continue

        browser.close()

    return scraped_events

def build_ics_file(events, output_filename="india_macro_calendar.ics"):
    cal = Calendar()
    cal.add("prodid", "-//India Macro Indicators Feed//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "India Macro Indicators")
    cal.add("x-wr-timezone", "Asia/Kolkata")

    now = datetime.datetime.now(IST)
    current_year = now.year

    month_lookup = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    added_count = 0
    for item in events:
        try:
            m_num = month_lookup.get(item["month"][:3].capitalize(), now.month)
            event_date = datetime.date(current_year, m_num, item["day"])
        except ValueError:
            continue

        evt = Event()
        evt.add("summary", f"📊 {item['title']}")
        evt.add("description", item["description"])
        evt.add("dtstart", event_date)
        evt.add("dtend", event_date + datetime.timedelta(days=1))
        evt.add("dtstamp", now)
        evt.add("uid", f"{uuid.uuid4()}@indiamacroindicators")

        cal.add_component(evt)
        added_count += 1

    with open(output_filename, "wb") as f:
        f.write(cal.to_ical())

    print(f"\nSuccess! Exported {added_count} events to '{output_filename}'.")

if __name__ == "__main__":
    extracted = scrape_calendar_events()
    print(f"Captured {len(extracted)} event entries.")
    build_ics_file(extracted)