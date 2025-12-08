import sys
import json
import traceback

status_msg = "Network: Ready"

async def submit_score_native(score):
    global status_msg, status_color
    
    if sys.platform != "emscripten":
        status_msg = "Skipped (Desktop Mode)"
        return

    url = "/api/submit-score"
    status_msg = f"Sending {score}..."
    status_color = (255, 255, 255)
    
    try:
        from platform import window
        
        score_payload = json.dumps({"game_id": "ghost_in_the_files", "score": score})
        
        fetch_config = {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": score_payload,
            "credentials": "include"
        }
        
        config_str = json.dumps(fetch_config)
        
        js_options = window.JSON.parse(config_str)
        
        response = await window.fetch(url, js_options)

        if response.status == 200:
            status_msg = "SUCCESS: Saved!"
            status_color = (50, 255, 50)
        else:
            status_msg = f"FAIL: {response.status}"
            status_color = (255, 50, 50)
            
    except Exception as e:
        # Print error to screen and console
        status_msg = f"Err: {str(e)[:20]}"
        status_color = (255, 50, 50)
        print(f"Full Error: {e}")
        traceback.print_exc()
