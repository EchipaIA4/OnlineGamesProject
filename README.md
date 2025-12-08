# Online Game Project

This project is a small web-based game hub where users can play games directly in their browser.
It aims to provide a simple platform with user accounts, login functionality, and a persistent leaderboard for storing scores.

The current hub includes a puzzle-style game inspired by titles such as *Rusty Lake*. The architecture supports adding additional games in the future, ranging from small classics (e.g., Snake or Pong) to more complex puzzles.

Source code is available at this 
[GitHub page](https://github.com/EchipaIA4/OnlineGamesProject)

The project is full-stack. A Flask backend handles authentication, data storage, and routing; the frontend is built with HTML, CSS, and Jinja2 templates; and the games are implemented in Pygame and compiled for the web using Pygbag, enabling Python to run in the browser via WebAssembly.


## Technologies Overview

The platform is built using a hybrid architecture that combines a Python web server (Flask) with browser-based game execution through WebAssembly (WASM).

## 1. Backend (Flask)

The backend handles routing, authentication, and API operations.

**Architecture**

* Uses an Application Factory Pattern (`main_app.py`) for initialization of configurations, extensions, and database integration.

**Routing**

* Organized via Blueprints for separation of concerns:

  * `auth_bp`: Handles registration, login, and logout.
  * `main_bp`: Serves core pages (`/`, `/leaderboard`) and the authenticated score submission endpoint (`/api/submit-score`).

**Extensions and Security**

* Initialized in `extensions.py`:

  * Flask-Login: session management and access control.
  * Flask-Bcrypt: password hashing.
  * Flask-CORS: enables cross-origin requests from the WASM game client.

## 2. Database Layer

Data persistence is implemented using SQLite via SQLAlchemy.

**Models (`user_model.py`):**

* `User`: stores usernames and password hashes.
* `Score`: stores score values and game identifiers, linked to `User` through a foreign key.

**Functionality:**

* Secure storage of users and scores.
* Aggregation of results for the leaderboard.


## 3. Game Client (Pygame / WASM)

Games run client-side and communicate with the Flask backend.

**Implementation**

* Built as standard Pygame projects (example: `game_source/pong/main.py`).

**Web Execution**

* Packaged using Pygbag into WebAssembly, allowing execution in modern browsers.

**Score Submission**

* After a game session, results are sent to the server via asynchronous POST requests to `/api/submit-score`.



## 4. Frontend

The presentation layer renders pages and displays game-related data.

**Technologies**

* Templates stored in `templates/`
* Jinja2 for dynamic rendering
* CSS styling in `static/css/style.css`

Functionality includes:

* Displaying available games
* Rendering user-specific content
* Displaying live leaderboards based on database queries


## 5. Games
### Ghost in the Files

**Ghost in the Files** is a narrative-driven puzzle game set within a simulated, decaying computer system. Players must navigate between two distinct operating system environments, manage system resources, and solve logic puzzles to repair corrupted hardware and uncover hidden secrets.

### Features

  * **Dual-Boot System:** Access two different desktop environments (**CipherShell** and **KernelGate**) via the Boot Menu to interact with different system layers.
  * **Simulated Desktop Interface:** Navigate a retro GUI complete with a file system, program windows, and an inventory system.
  * **Logic Puzzles:**
      * **CPU Balance:** Manage core loads to stabilize the processor thermal activity.
      * **RAM Restoration:** Solve grid-based logic puzzles to clear volatile memory blocks.
      * **Network Repair:** Reconnect nodes to restore data pathways.
  * **File Decryption:** Use the built-in **Convertor** tool to decode hidden messages using Base64 and XOR ciphers.
  * **Inventory System:** Collect and use hardware items (Entropy Flasks, Memory Chips, Null Pointers) to interact with system components.

### Controls

  * **Mouse:** Point and click to interact with files, buttons, and puzzle elements.
  * **ESC:** Pause game / Close current program window.
  * **Arrow Keys & Enter:** Navigate the Boot Menu.


## Pong

This game is purely for the purpose of showing how this project is scalable with any game.

## Usage

### 1. Create and Activate a Virtual Environment

Consult [this Python documentation](https://docs.python.org/3/library/venv.html) for details:

Activate the environment:

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Start the Server

```bash
python3 run.py
```

Upon startup, two URLs are displayed:

* One for use on the hosting machine
* One for use by other devices on the same local network

#### Stop the server at any time with: **CTRL + C**

#### Gameplay and Leaderboard :

An account is required to play games.
Scores are automatically submitted to the server and displayed on the leaderboard.


## Screenshot

![Screenshot](/github.jpg)

---