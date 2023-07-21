import asyncio
from bs4 import BeautifulSoup
import requests
import telegram

# Define the URL to scrape
url = "https://reliefweb.int/jobs"

# Define the Telegram bot token and chat ID
bot_token = "6307722427:AAEDDTmdCZnnVTTt6u5CtuPr5Kw6mXvpmFQ"
chat_id = "@ezeganews"

# Define an async function to send messages
async def send_job_messages():
    # Create a Telegram bot object
    bot = telegram.Bot(token=bot_token)

    while True:
        # Send a GET request to the URL and get the HTML content
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the job article cards using the class name
        job_cards = soup.find_all('article', class_='rw-river-article--card')

        # Loop through each job article card and extract the URL and text of the job title
        for job_card in job_cards:
            job_title = job_card.find('h3', class_='rw-river-article__title')
            job_url = job_title.find('a')['href']
            job_text = job_title.text.strip()

            # Send the job title and URL to the Telegram chat asynchronously
            message = f"{job_text}\n{job_url}"
            await bot.send_message(chat_id=chat_id, text=message)

        # Pause for 30 seconds before sending the next job message
        await asyncio.sleep(600)

# Create an event loop object
loop = asyncio.get_event_loop()

# Run the async function to send job messages in the event loop
loop.create_task(send_job_messages())

# Run the event loop until it's stopped manually or by an exception
loop.run_forever()
