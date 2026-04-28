# Hybrid-AI
Uses a hybrid (Edge AI + Cloud AI) model that can switch between two AI models flawlessly. When the internet is unavailable (due to some catastrophic crisis or any such reason), it would use Edge AI (Y) for giving immediate solutions, and when the internet is back, it can switch to Gemini for answering complex, heavy queries.

# 🆘 Project Y: Hybrid Edge-First Emergency AI
Project Y is a resilient, dual-layered AI assistant built to bridge the "Connectivity Gap" during natural disasters and humanitarian crises.

# 📖 Overview
When disaster strikes, the internet is often the first thing to go. Project Y ensures that life-saving information is always accessible by intelligently switching between high-performance Cloud AI and local Edge AI.

The Problem: Standard AI assistants (Gemini, ChatGPT) require a stable internet connection. In a flood, earthquake, or conflict zone, this makes them useless.

The Solution: A hybrid system that uses Google Gemini 1.5 Flash for deep reasoning when online, and a quantized TinyLlama-1.1B model for instant, offline intelligence when the grid fails.

# 🛠️ Technical Architecture
Cloud Layer: Google Gemini 1.5 Flash (via google-generativeai SDK).

Edge Layer: TinyLlama-1.1B-Chat (via HuggingFace transformers).

Backend: Flask (Python) managing session memory and failover logic.

Frontend: Responsive HTML5/JavaScript with a real-time system status indicator.

# 🚀 Features
Offline Autonomy: Functions in 100% Airplane Mode.

Smart Failover: Automatically detects network drops and switches models in seconds.

System Memory: Maintains conversation context even after switching from Cloud to Edge.

Privacy Centric: Offline queries never leave the local hardware.

# 💻 Installation & Setup

```bash
  # Clone the repository
git clone https://github.com/sounak1410/Hybrid-AI.git

# Enter the directory
cd Hybrid-AI

# Install dependencies
pip install -r requirements.txt

# Configure Environmental Variables
Create a .env file in the root directory:
FLASK_SECRET_KEY=pick_a_very_long_random_string_here
APP_PASSWORD=676767
GOOGLE_API_KEY=your_gemini_api_key_here

# Run the application
python h2s.py
```

# 📊 Impact & UN SDGs
Our project targets the following United Nations Sustainable Development Goals:

Goal 9: Industry, Innovation, and Infrastructure (Resilient infrastructure).

Goal 11: Sustainable Cities and Communities (Disaster resilience).

Goal 3: Good Health and Well-being (Emergency first-aid access).

# 🔮 Future Roadmap
[ ] Multimodal Edge: Offline image processing for wound/injury assessment.

[ ] Mesh Sync: P2P emergency data sharing via Bluetooth.

[ ] Ultra-Lightweight: Implementation of Gemini Nano for mobile-native deployment.

# 📜 License
Distributed under the MIT License. See LICENSE for more information.

# Created by S(Sounak) Developed for the Google Solution Challenge 2026