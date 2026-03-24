from app import create_app
from app.models.database import init_db

app = create_app()

if __name__ == "__main__":
    # This creates the .db file the very first time you run the app
    init_db() 
    
    print("🚀 Server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)