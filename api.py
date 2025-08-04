from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Create an instance of the FastAPI application.
app = FastAPI()

# Define a route for the root URL ("/") that handles GET requests.
# The 'response_class=HTMLResponse' tells FastAPI to return an HTML response.
@app.get("/", response_class=HTMLResponse)
async def serve_park_ride_app():
    # This multi-line f-string contains the entire HTML structure.
    # The f-string is used here for convenience, but no Python variables
    # are being dynamically injected in this version.
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Park & Ride Time Estimator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
        }}
        .form-container {{
            background-color: #ffffff;
            border-radius: 1.5rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            padding: 2.5rem;
            position: relative;
            width: 100%;
            max-width: 24rem;
        }}
        .submit-button {{
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        .submit-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}
        .input-field:focus {{
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
        }}
        .loading-spinner {{
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border-left-color: #3b82f6;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .results-panel {{
            position: absolute;
            top: 0;
            left: 100%;
            margin-left: 1rem;
            width: 20rem;
        }}
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">

    <div class="form-container">
        <h1 class="text-4xl font-extrabold text-center text-gray-900 mb-8">
            Park & Ride Estimator
        </h1>

        <form id="estimatorForm" class="space-y-6">
            <div>
                <label for="origin" class="block text-gray-700 text-sm font-bold mb-2">Origin</label>
                <input type="text" id="origin" name="origin" required placeholder="e.g., Downtown Ottawa"
                       class="input-field w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500">
            </div>
            <div>
                <label for="destination" class="block text-gray-700 text-sm font-bold mb-2">Destination</label>
                <input type="text" id="destination" name="destination" required placeholder="e.g., Greenboro Station"
                       class="input-field w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500">
            </div>
            <div>
                <label for="departureDate" class="block text-gray-700 text-sm font-bold mb-2">Departure Date</label>
                <input type="date" id="departureDate" name="departureDate" required
                       class="input-field w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500">
            </div>
            <div>
                <label for="departureTime" class="block text-gray-700 text-sm font-bold mb-2">Departure Time</label>
                <input type="time" id="departureTime" name="departureTime" required
                       class="input-field w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500">
            </div>
            <button type="submit"
                    class="submit-button w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-xl text-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Calculate Time
            </button>
        </form>

        <div id="results-container" class="results-panel hidden bg-white rounded-lg shadow p-4 space-y-4">
            <div id="loading-spinner" class="flex justify-center items-center">
                <div class="loading-spinner"></div>
            </div>
            <div id="results" class="space-y-4">
                <div class="flex flex-col p-2 border-b border-gray-200">
                    <div class="flex justify-between items-center mb-1">
                        <h3 class="text-lg font-semibold text-gray-800">Lot A</h3>
                    </div>
                    <p class="text-sm text-gray-600">Origin → Park: <span class="font-medium">12 min</span></p>
                    <p class="text-sm text-gray-600">Park → Destination: <span class="font-medium">25 min</span></p>
                    <p class="text-sm text-gray-600">Arrival Time: <span class="font-medium">08:37 AM</span></p>
                </div>
                <div class="flex flex-col p-2 border-b border-gray-200">
                    <div class="flex justify-between items-center mb-1">
                        <h3 class="text-lg font-semibold text-gray-800">Lot B</h3>
                    </div>
                    <p class="text-sm text-gray-600">Origin → Park: <span class="font-medium">8 min</span></p>
                    <p class="text-sm text-gray-600">Park → Destination: <span class="font-medium">22 min</span></p>
                    <p class="text-sm text-gray-600">Arrival Time: <span class="font-medium">08:30 AM</span></p>
                </div>
                <div class="flex flex-col p-2">
                    <div class="flex justify-between items-center mb-1">
                        <h3 class="text-lg font-semibold text-gray-800">Lot C</h3>
                    </div>
                    <p class="text-sm text-gray-600">Origin → Park: <span class="font-medium">15 min</span></p>
                    <p class="text-sm text-gray-600">Park → Destination: <span class="font-medium">18 min</span></p>
                    <p class="text-sm text-gray-600">Arrival Time: <span class="font-medium">08:33 AM</span></p>
                </div>
            </div>
            <div id="error-message" class="hidden text-red-600 text-sm"></div>
        </div>
    </div>

    <script>
        document.getElementById('estimatorForm').addEventListener('submit', function(event) {
            event.preventDefault();
            document.getElementById('loading-spinner').classList.add('hidden');
            document.getElementById('results').classList.remove('hidden');
            document.getElementById('results-container').classList.remove('hidden');
        });
        document.getElementById('departureDate').valueAsDate = new Date();
    </script>
</body>
</html>
"""
    
    # Return the HTML content using the HTMLResponse class.
    return HTMLResponse(content=html_content)
