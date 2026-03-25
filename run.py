import os
from app import create_app
from app.models.database import init_db

# 1. Initialize the app globally so Gunicorn can see it
app = create_app()

# 2. Add a simple Home route directly here to stop the 404
@app.route('/')
def home():
    return "🌱 Smart-Pest-Detection is LIVE and listening!"

if __name__ == "__main__":
    # Create database on first run
    init_db() 
    
    # Get port from environment (Render) or use 5000 (Local)
    port = int(os.environ.get("PORT", 5000))
    
    # 0.0.0.0 is CRITICAL for Render
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)