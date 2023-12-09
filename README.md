# 👩‍✈️ Elizabeth Flight Tracker 
<p>This Python script, named "ElizabethFlightTracker.py," is designed to help you track and monitor flight details based on a provided Google Flight URL. It scrapes relevant information from the webpage and sends an email with the flight details to a specified email address.</p>

## Features

- Web scraping of flight details from a Google Flight URL.
- HTML email generation with flight information.
- Sends the email with flight details to a specified email address.

## Usage

### Prerequisites

- Python 3.x installed
- Required Python packages installed (`requests`, `beautifulsoup4`, `yagmail`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/judcodeofficial/ElizabethFlightTrackerModule.git
   cd ElizabethFlightTrackerModule

2. Install requirements
   ```bash
   pip install -r requirements.txt
   
3. Running the script
   ```bash
   python ElizabethFlightTracker.py "https://www.google.com/flights?..." "your_email@gmail.com" "your_gmail_password" "recipient@example.com"

### Options
    Google_Flight_URL: The URL of the Google Flight page with applied filters.
    Gmail_Username: Your Gmail username.
    Gmail_Password: Your Gmail password.
    Recipient_Email: The email address that will receive the flight details.
