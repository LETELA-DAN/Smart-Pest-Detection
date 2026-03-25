import os
from app import create_app
from app.models.database import init_db

# 1. Create the app instance at the TOP LEVEL
# Render needs to see this 'app' variable to start your service.
app = create_app()

# 2. Initialize the Database
# We use 'app.app_context()' to ensure the database 
# is ready before the first farmer sends a message.
with app.app_context():
    try:
        init_db()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

if __name__ == "__main__":
    # 3. Local Development (VS Code)
    # This only runs if you manually type 'python run.py'
    port = int(os.environ.get("PORT", 10000))
    
    print(f"🚀 Starting locally on port {port}")
    # '0.0.0.0' allows external services like AT to find your app
    app.run(host='0.0.0.0', port=port, debug=True)