# Park & Ride Time Estimator

This web application helps users find the fastest Park & Ride lots in Ottawa. Enter your origin, destination, and departure time to get the fastest Park & Ride options.

## Features

- FastAPI backend with Jinja2 templating
- Uses Google Maps APIs for directions and transit times
- Displays top 3 Park & Ride options with breakdowns
- Responsive UI styled with Tailwind CSS

## Setup

1. **Clone the repository**  
   ```
   git clone <your-repo-url>
   cd ParknSlide
   ```

2. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

3. **Configure Google API Key**  
   - Add your Google Maps API key to the `.env` file:
     ```
     GOOGLE_API_KEY = '<your-api-key>'
     ```

4. **Run the application**  
   ```
   python main.py
   ```
   - The app will be available at [http://localhost:8000](http://localhost:8000).

## File Structure

- `main.py` — FastAPI app and core logic
- `templates/index.html` — Main HTML template
- `.env` — API keys and secrets (not tracked by git)
- `requirements.txt` — Python dependencies

## Notes

- Requires a valid Google Maps API key with Directions and Geocoding enabled.
- For development, use the provided `.env` and `.gitignore` to keep secrets safe.

## License

MIT License