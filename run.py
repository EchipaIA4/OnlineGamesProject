from app.main_app import app

if __name__ == '__main__':
    # In production, debug should be False
    app.run(debug=True, host="0.0.0.0", port=5000)