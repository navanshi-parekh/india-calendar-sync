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

        page = context.new_page()
        page.route("**/*clarity*", lambda route: route.abort())
        page.route("**/*psimg*", lambda route: route.abort())
        page.route("**/*google-analytics*", lambda route: route.abort())

        print("Navigating to calendar...")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(4000)

        # Evaluate directly in the browser DOM to bind each event pill to its exact cell day
        # Evaluate directly in the browser DOM to bind each event pill strictly to its own calendar cell
        events_data = page.evaluate("""() => {
            const results = [];
            const keywords = [
                'PMI', 'GST', 'Reserves', 'WPI', 'CPI', 'Inflation', 'Unemployment',
                'Trade', 'Money Supply', 'Bank Credit', 'Industries', 'IIP',
                'Expenditure', 'Monetary Policy', 'MPC', 'GDP'
            ];

            for (const el of document.querySelectorAll('div, span, p, a')) {
                const t = (el.innerText || '').trim();
                const matched = keywords.some(k => t.toLowerCase() === k.toLowerCase() || (t.toLowerCase().includes(k.toLowerCase()) && t.length < 50));
                
                // Only consider leaf nodes (the text inside the colored pill badge)
                if (matched && el.children.length === 0) {
                    let parent = el.parentElement;
                    let foundDay = null;
                    
                    // Traverse up strictly within the individual day cell
                    for (let depth = 0; depth < 5 && parent; depth++) {
                        const pText = parent.innerText || '';
                        
                        // Guard: A single calendar day cell will never have thousands of characters of text
                        if (pText.length > 250) {
                            parent = parent.parentElement;
                            continue;
                        }

                        // Match the standalone day number at the start of the cell
                        const m = pText.match(/(?:^|\\n)\\s*([1-9]|[12][0-9]|3[01])\\s*(?:\\n|$)/);
                        if (m) {
                            foundDay = parseInt(m[1], 10);
                            break;
                        }
                        parent = parent.parentElement;
                    }

                    // Exclude outer page headers (like the top nav 'Consumer Inflation Index')
                    if (foundDay && t !== "Consumer Inflation Index") {
                        results.push({
                            title: t,
                            day: foundDay
                        });
                    }
                }
            }
            return results;
        }""")

        browser.close()

    # Deduplicate entries: (title, day)
    unique_events = []
    seen = set()
    for ev in events_data:
        key = (ev["title"].strip(), ev["day"])
        if key not in seen and len(ev["title"]) > 2:
            seen.add(key)
            unique_events.append(ev)

    return unique_events

def build_ics_file(events, output_filename="india_macro_calendar.ics"):
    cal = Calendar()
    cal.add("prodid", "-//India Macro Indicators Feed//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "India Macro Indicators")
    cal.add("x-wr-timezone", "Asia/Kolkata")

    now = datetime.datetime.now(IST)
    year = now.year
    month = now.month  # September

    added_count = 0
    for item in events:
        day = item["day"]
        # Handle calendar padding days (e.g. days 30, 31 from previous month or 1, 2, 3 of next)
        event_month = month
        event_year = year

        # If day is 30 or 31 and appears before day 1, or 1, 2, 3 at the bottom
        # Default straightforward matching for the active month:
        try:
            event_date = datetime.date(event_year, event_month, day)
        except ValueError:
            continue

        evt = Event()
        evt.add("summary", f"📊 {item['title']}")
        evt.add("description", f"{item['title']} - Scheduled Indian Macroeconomic Release")
        evt.add("dtstart", event_date)
        evt.add("dtend", event_date + datetime.timedelta(days=1))
        evt.add("dtstamp", now)
        # Deterministic UID so updates don't create duplicates
        evt.add("uid", f"{event_year}{event_month:02d}{day:02d}-{re.sub(r'[^a-zA-Z0-9]', '', item['title'])}@indiamacro")

        cal.add_component(evt)
        added_count += 1

    with open(output_filename, "wb") as f:
        f.write(cal.to_ical())

    print(f"\nDone! Exported {added_count} correctly mapped events to '{output_filename}'.")

if __name__ == "__main__":
    extracted = scrape_calendar_events()
    print(f"Captured {len(extracted)} accurately mapped events:")
    for e in extracted:
        print(f"  Day {e['day']:02d}: {e['title']}")
    build_ics_file(extracted)