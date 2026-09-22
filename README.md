# 📊 India Macroeconomic Indicators — Live Calendar Feed

[![Update India Macro Calendar](https://github.com/navanshi-parekh/india-calendar-sync/actions/workflows/update_calendar.yml/badge.svg)](https://github.com/navanshi-parekh/india-calendar-sync/actions/workflows/update_calendar.yml)
[![Calendar Format: iCal](https://img.shields.io/badge/Format-iCal%20%2F%20.ics-blue.svg)](https://en.wikipedia.org/wiki/ICalendar)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated, subscribe-and-forget calendar feed syncing key Indian macroeconomic release dates directly into your personal calendar (Google Calendar, Apple Calendar, Outlook).

### Tracked Indicators
* **RBI Monetary Policy Committee (MPC)** decisions & rate announcements
* **Consumer Price Index (CPI)** inflation releases
* **Wholesale Price Index (WPI)** data
* **Index of Industrial Production (IIP)** numbers
* **Gross Domestic Product (GDP)** quarterly releases
* **Trade Deficit & Forex Reserves** telemetry

---

## ⚡ 1-Click Subscribe

Choose your primary calendar platform below:

| Platform | Quick Action | Direct URL |
| :--- | :--- | :--- |
| **Google Calendar** | [![Subscribe to Google Calendar](https://img.shields.io/badge/Google_Calendar-Subscribe_with_1--Click-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://calendar.google.com/calendar/render?cid=https%3A%2F%2Fraw.githubusercontent.com%2Fnavanshi-parekh%2Findia-calendar-sync%2Fmain%2Findia_macro_calendar.ics) | Add via [Render Link](https://calendar.google.com/calendar/render?cid=https%3A%2F%2Fraw.githubusercontent.com%2Fnavanshi-parekh%2Findia-calendar-sync%2Fmain%2Findia_macro_calendar.ics) |
| **Apple Calendar** *(Mac / iOS)* | [![Subscribe to Apple Calendar](https://img.shields.io/badge/Apple_Calendar-Subscribe_with_1--Click-000000?style=for-the-badge&logo=apple&logoColor=white)](webcal://raw.githubusercontent.com/navanshi-parekh/india-calendar-sync/main/india_macro_calendar.ics) | Launch with `webcal://` |
| **Outlook / Office 365** | [![Subscribe to Outlook](https://img.shields.io/badge/Outlook-Subscribe_from_Web-0078D4?style=for-the-badge&logo=microsoftoutlook&logoColor=white)](https://outlook.live.com/calendar/0/addcalendar?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnavanshi-parekh%2Findia-calendar-sync%2Fmain%2Findia_macro_calendar.ics&name=India%20Macro%20Indicators) | Add via [Outlook Web](https://outlook.live.com/calendar/0/addcalendar?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnavanshi-parekh%2Findia-calendar-sync%2Fmain%2Findia_macro_calendar.ics&name=India%20Macro%20Indicators) |

---

## 📋 Manual Subscription Instructions

If the 1-click links don't open your client automatically, copy the raw feed URL:

```text
[https://raw.githubusercontent.com/navanshi-parekh/india-calendar-sync/main/india_macro_calendar.ics](https://raw.githubusercontent.com/navanshi-parekh/india-calendar-sync/main/india_macro_calendar.ics)

Google Calendar
Open Google Calendar.

On the left sidebar, click the + icon next to Other calendars.

Select From URL.

Paste the raw feed URL above and click Add calendar.

Apple Calendar (macOS & iOS)
macOS: Open Calendar > File > New Calendar Subscription... > paste the URL > select auto-refresh frequency (e.g., Every day).

iOS: Go to Settings > Calendar > Accounts > Add Account > Other > Add Subscribed Calendar > paste the URL.

Microsoft Outlook
Open Outlook Web or the desktop client.

Navigate to Calendar > Add calendar > Subscribe from web.

Paste the URL, set the calendar name to India Macro Indicators, and select Import.


⚙️ How It Works
┌───────────────────────────────┐
│  indiamacroindicators.co.in   │
└───────────────┬───────────────┘
                │  Headless Chromium (Playwright)
                ▼
┌───────────────────────────────┐
│     sync_calendar.py          │  Parses dynamic calendar DOM,
│                               │  formats to RFC 5545 iCalendar
└───────────────┬───────────────┘
                │  Runs on the 1st of every month
                ▼
┌───────────────────────────────┐
│     GitHub Actions Runner     │  Commits updated .ics feed
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│   Google / Apple / Outlook    │  Pulls latest events via Webcal
└───────────────────────────────┘
The scraper workflow (.github/workflows/update_calendar.yml) executes automatically on the 1st of every month at 00:00 UTC via GitHub Actions. Any changes or upcoming quarterly revisions are committed directly to india_macro_calendar.ics.

🛠️ Local Development
To run the scraper locally:

Bash
# Clone the repository
git clone [https://github.com/navanshi-parekh/india-calendar-sync.git](https://github.com/navanshi-parekh/india-calendar-sync.git)
cd india-calendar-sync

# Install Python requirements
pip install requests playwright icalendar pytz

# Install headless browser binaries
python -m playwright install chromium

# Run the parser
python sync_calendar.py
📄 License
This project is open-source under the MIT License.


---

### Key Features of This README:
* **True 1-Click URLs:** 
  * The Google Calendar button uses Google's `render?cid=` URL scheme with URL-encoded parameters to open Google Calendar with the URL preloaded.
  * The Apple Calendar button uses the `webcal://` URI protocol to trigger native macOS/iOS calendar subscription dialogs.
  * The Outlook button uses Microsoft's `addcalendar?url=` web interface schema.
* **Dynamic Action Badge:** Visual indicator showing visitors whether the monthly sync job is currently passing.
* **Architecture ASCII Flowchart:** Clear overview of how Playwright and GitHub Actions tie into Webcal.

<FollowUp label="Want to know how to add an MIT License file to your repository?" query="How do I add a standard MIT License file to my GitHub repository?"/>

<ElicitationsGroup message="Next actions for your repository:">
  <Elicitation label="Set up GitHub Pages for an even cleaner feed domain" query="How can I host the .ics file using GitHub Pages to have a custom personal domain URL?"/>
  <Elicitation label="Add a notification for workflow run failures" query="How do I configure GitHub Actions to send me an email or Telegram notification if the scraper fails?"/>
</ElicitationsGroup>