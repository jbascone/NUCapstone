import re
import email
from bs4 import BeautifulSoup

class EmailParser:
    def __init__(self, message_body):
        self.message_body = message_body
        

    def extract_booking_info(self):
        msg = email.message_from_string(self.message_body)

        # Extract information using BeautifulSoup
        soup = BeautifulSoup(msg.get_payload(), 'html.parser')
        soup.prettify()
        
        # Use regular expression to find "Airbnb" or "Kayak" (case-insensitive)
        airbnb_match = re.search(r'(?i)\bAirbnb\b', self.message_body)
        kayak_match = re.search(r'(?i)\bKayak\b', self.message_body)

        reservation_origin = airbnb_match.group(0) if airbnb_match else (kayak_match.group(0) if kayak_match else None)
        if reservation_origin == None:
            return

        try:
            customer_name_element = soup.find(text=re.compile(r'Confirmed guests'))
            customer_name_unformatted = customer_name_element.find_next('div').text.strip() if customer_name_element else None
            customer_name_str = str(customer_name_unformatted)  # Convert to string
            customer_name_only = re.sub(r'\n.*$', '', customer_name_str)
            customer_name = str(customer_name_only).strip().replace('\n', '')
        except AttributeError:
            customer_name = None

        event_name_match = re.search(r'Booking confirmed for (.+?) on (.+?):', str(soup))
        event_name = event_name_match.group(1).strip() if event_name_match else None

        try:
            confirmation_code_element = soup.find(text=re.compile(r'Confirmation code'))
            confirmation_code = confirmation_code_element.find_next('p').text.strip() if confirmation_code_element else None
        except AttributeError:
            confirmation_code = None

        try:
            time_element = soup.select('p:-soup-contains("AM")') + soup.select('p:-soup-contains("PM")')

            time_text = time_element[0].text if time_element else None

            # Split the text into date and time segments
            date_segment, time_segment = time_text.split(',', 1)

            # Extract date
            date = date_segment.strip()

            # Extract start and end times
            times = time_segment.split('–')
            start_time = times[0].strip()
            end_time = times[1].strip().split(',')[1].strip()  # Take the second element after splitting by comma
        except AttributeError:
            date, start_time, end_time, = None, None, None

        try:
            seats_booked_element = soup.find(text=re.compile(r'Seats booked'))
            seats_booked = seats_booked_element.find_next('p').text.strip().split('/')[0].strip() if seats_booked_element else None
            total_seats = seats_booked_element.find_next('p').text.strip().split('/')[1].strip() if seats_booked_element else None
        except AttributeError:
            seats_booked, total_seats = None, None

        print("=" * 50)
        print(f"Reservation Origin: {reservation_origin}")
        print(f"Customer Name: {customer_name}")
        print(f"Event Name: {event_name}")
        print(f"Confirmation Code: {confirmation_code}")
        print(f"Date: {date}")
        print(f"Time: {start_time} – {end_time}")
        print(f"Seats Booked: {seats_booked} / {total_seats}")
        print("=" * 50 + "\n")

        return {            
            "ReservationOrigin": reservation_origin,
            "CustomerName": customer_name,
            "EventName": event_name,
            "ConfirmationCode": confirmation_code,
            "Date": date,
            "StartTime": start_time,
            "EndTime": end_time,
            "SeatsBooked": seats_booked,
            "TotalSeats": total_seats
            }

    def extract_booking_info_reg_table(self):
        msg = email.message_from_string(self.message_body)

        # Extract information using BeautifulSoup
        soup = BeautifulSoup(msg.get_payload(), 'html.parser')
        soup.prettify()
        
        # Use regular expression to find "Airbnb" or "Kayak" (case-insensitive)
        airbnb_match = re.search(r'(?i)\bAirbnb\b', self.message_body)
        kayak_match = re.search(r'(?i)\bKayak\b', self.message_body)

        reservation_origin = airbnb_match.group(0) if airbnb_match else (kayak_match.group(0) if kayak_match else None)
        if reservation_origin is None:
            return

        try:
            customer_name_element = soup.find(text=re.compile(r'Confirmed guests'))
            customer_name_unformatted = customer_name_element.find_next('div').text.strip() if customer_name_element else None
            customer_name_str = str(customer_name_unformatted)  # Convert to string
            customer_name_only = re.sub(r'\n.*$', '', customer_name_str)
            customer_name = str(customer_name_only).strip().replace('\n', '')
        except AttributeError:
            customer_name = None

        event_name_match = re.search(r'Booking confirmed for (.+?) on (.+?):', str(soup))
        event_name = event_name_match.group(1).strip() if event_name_match else None

        try:
            confirmation_code_element = soup.find(text=re.compile(r'Confirmation code'))
            confirmation_code = confirmation_code_element.find_next('p').text.strip() if confirmation_code_element else None
        except AttributeError:
            confirmation_code = None

        try:
            time_element = soup.select('p:-soup-contains("AM")') + soup.select('p:-soup-contains("PM")')

            time_text = time_element[0].text if time_element else None

            # Split the text into date and time segments
            date_segment, time_segment = time_text.split(',', 1)

            # Extract date
            date = date_segment.strip()

            # Extract start and end times
            times = time_segment.split('–')
            start_time = times[0].strip()
            end_time = times[1].strip().split(',')[1].strip()  # Take the second element after splitting by comma
        except AttributeError:
            date, start_time, end_time, = None, None, None

        try:
            seats_booked_element = soup.find(text=re.compile(r'Seats booked'))
            seats_booked = seats_booked_element.find_next('p').text.strip().split('/')[0].strip() if seats_booked_element else None
            total_seats = seats_booked_element.find_next('p').text.strip().split('/')[1].strip() if seats_booked_element else None
        except AttributeError:
            seats_booked, total_seats = None, None

        print("=" * 50)
        print(f"Reservation Origin: {reservation_origin}")
        print(f"Customer Name: {customer_name}")
        print(f"Event Name: {event_name}")
        print(f"Confirmation Code: {confirmation_code}")
        print(f"Date: {date}")
        print(f"Time: {start_time} – {end_time}")
        print(f"Seats Booked: {seats_booked} / {total_seats}")
        print("=" * 50 + "\n")

        username = "deltateam"
        username = str(username).strip().replace('\n', '')


        return {
            "confirmation": confirmation_code,
            "username": username,
            "name": customer_name,
            "date": "2024-06-01",
            "time": "08:00:00",
            "duration": 1,    
            "tracking": "booking.com",
            "rent": "table"
            }
