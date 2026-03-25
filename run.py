import os
from app import create_app
from app.models.database import init_db

# Initialize the app factory
app = create_app()

if __name__ == "__main__":
    # Create the database on the first run
    init_db() 
    
    # Use the port Render gives you, or 10000 by default
    port = int(os.environ.get("PORT", 10000))
    
    # '0.0.0.0' is mandatory to allow Africa's Talking to reach your app
    print(f"🚀 Smart-Pest-Detection starting on port {port}")
    app.run(host='0.0.0.0', port=port)