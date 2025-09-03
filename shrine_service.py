#!/usr/bin/env -S uv run --with fastapi --with uvicorn --with jinja2 python3

"""
🏛️ The Shrine - Calm and Steady Contemplative Service
A serene, stable service for quiet reflection and steady wisdom
Counterbalance to the dynamic randomness systems
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configuration for stability and calm
SHRINE_PORT = 44777  # Stable, memorable port
SHRINE_REFRESH_INTERVAL = 3600  # 1 hour - very stable
MAX_CONTEMPLATION_TIME = 7200  # 2 hours maximum session

class ContemplativeWisdom:
    """Stable wisdom and reflection management"""
    
    def __init__(self):
        self.wisdom_cache = {}
        self.contemplation_sessions = {}
        self.steady_metrics = {
            'total_sessions': 0,
            'average_session_time': 0,
            'wisdom_accessed': 0,
            'shrine_uptime': 0
        }
        self.startup_time = time.time()
        self.last_wisdom_refresh = 0
        
    def get_daily_wisdom(self) -> Dict[str, str]:
        """Provide stable daily wisdom that changes slowly"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.wisdom_cache:
            # Generate stable wisdom for the day
            day_seed = hash(today) % 1000
            
            wisdom_themes = [
                "On the nature of simplicity and its quiet power",
                "The steady accumulation of understanding over time", 
                "Finding clarity in the midst of complexity",
                "The value of patient observation and careful thought",
                "Balance between action and reflection",
                "The deeper patterns that emerge through contemplation",
                "Wisdom that grows slowly like ancient trees",
                "The peace found in accepting what cannot be changed",
                "Truth revealed through sustained attention",
                "The gentle strength of consistent practice"
            ]
            
            reflections = [
                "True understanding comes not from rushing but from patient observation.",
                "In stillness, we often find the answers that elude us in motion.",
                "Complexity reveals its secrets to those who approach with calm curiosity.",
                "The most profound insights arise when we stop trying to force them.",
                "Simplicity is not the absence of complexity, but its harmonious resolution.",
                "Wisdom accumulates slowly, like sediment forming precious stone.",
                "The deepest truths are often the quietest ones.",
                "In the space between thoughts, understanding dawns.",
                "Patience is not passive waiting, but active cultivation of clarity.",
                "The shrine of wisdom is built one contemplative moment at a time."
            ]
            
            self.wisdom_cache[today] = {
                "theme": wisdom_themes[day_seed % len(wisdom_themes)],
                "reflection": reflections[day_seed % len(reflections)],
                "date": today,
                "contemplation_focus": self._get_contemplation_focus(day_seed),
                "generated_at": time.time()
            }
            
        return self.wisdom_cache[today]
    
    def _get_contemplation_focus(self, seed: int) -> str:
        """Get a stable contemplation focus for the day"""
        focuses = [
            "mindful observation of complexity patterns",
            "patient consideration of multiple perspectives",
            "steady attention to underlying principles",
            "gentle awareness of interconnections",
            "calm exploration of fundamental questions",
            "quiet appreciation of elegant solutions",
            "sustained reflection on core values",
            "peaceful integration of diverse insights"
        ]
        return focuses[seed % len(focuses)]
    
    def start_contemplation_session(self, session_id: str) -> Dict[str, Any]:
        """Begin a contemplative session"""
        session = {
            "session_id": session_id,
            "start_time": time.time(),
            "wisdom_accessed": [],
            "status": "active",
            "contemplation_depth": 0
        }
        
        self.contemplation_sessions[session_id] = session
        self.steady_metrics['total_sessions'] += 1
        
        return {
            "message": "🏛️ Contemplative session begun",
            "session_id": session_id,
            "daily_wisdom": self.get_daily_wisdom(),
            "guidance": "Take your time. Wisdom emerges naturally through patient attention."
        }
    
    def get_shrine_status(self) -> Dict[str, Any]:
        """Get stable shrine status - changes slowly"""
        uptime = time.time() - self.startup_time
        
        # Calculate stable averages
        active_sessions = len([s for s in self.contemplation_sessions.values() 
                              if s.get('status') == 'active'])
        
        return {
            "shrine_status": "🏛️ Serene and Stable",
            "uptime_hours": round(uptime / 3600, 1),
            "active_contemplations": active_sessions,
            "total_sessions": self.steady_metrics['total_sessions'],
            "wisdom_stability": "High - refreshes daily",
            "contemplative_atmosphere": "Calm and Focused",
            "shrine_principle": "Stability through consistent presence"
        }
    
    def end_contemplation_session(self, session_id: str) -> Dict[str, Any]:
        """End contemplative session with gentle summary"""
        if session_id not in self.contemplation_sessions:
            return {"error": "Session not found"}
            
        session = self.contemplation_sessions[session_id]
        duration = time.time() - session['start_time']
        
        session['status'] = 'completed'
        session['duration'] = duration
        
        return {
            "message": "🏛️ Contemplation complete",
            "session_duration_minutes": round(duration / 60, 1),
            "wisdom_integration": "Allow insights to settle naturally",
            "parting_thought": "Carry this clarity with you into action",
            "return_invitation": "The shrine remains open for future reflection"
        }

# Initialize the contemplative wisdom system
wisdom = ContemplativeWisdom()

# FastAPI app setup - configured for stability
app = FastAPI(
    title="🏛️ The Shrine - Contemplative Service",
    description="Calm and steady service for reflection and stable wisdom",
    version="1.0.0"
)

# CORS - open but stable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limited methods for stability
    allow_headers=["*"],
)

# Templates for serene UI
templates = Jinja2Templates(directory="/tmp")

@app.get("/", response_class=HTMLResponse)
async def shrine_home(request: Request):
    """Serene shrine homepage"""
    daily_wisdom = wisdom.get_daily_wisdom()
    status = wisdom.get_shrine_status()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏛️ The Shrine - Contemplative Service</title>
        <style>
            body {{
                font-family: 'Vollkorn', Georgia, serif;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #343a40;
                line-height: 1.8;
                margin: 0;
                padding: 2rem;
                min-height: 100vh;
            }}
            
            .shrine-container {{
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }}
            
            .shrine-title {{
                font-size: 2.5rem;
                color: #6c757d;
                margin-bottom: 1rem;
                font-weight: 300;
            }}
            
            .shrine-subtitle {{
                font-size: 1.2rem;
                color: #868e96;
                margin-bottom: 3rem;
                font-style: italic;
            }}
            
            .wisdom-card {{
                background: rgba(255,255,255,0.8);
                padding: 2rem;
                border-radius: 8px;
                margin: 2rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 4px solid #6c757d;
            }}
            
            .wisdom-theme {{
                font-size: 1.3rem;
                font-weight: 600;
                color: #495057;
                margin-bottom: 1rem;
            }}
            
            .wisdom-reflection {{
                font-size: 1.1rem;
                font-style: italic;
                color: #6c757d;
                line-height: 1.6;
            }}
            
            .contemplation-focus {{
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 4px;
                margin-top: 1rem;
                font-size: 0.95rem;
                color: #868e96;
            }}
            
            .shrine-status {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }}
            
            .status-item {{
                background: rgba(255,255,255,0.6);
                padding: 1rem;
                border-radius: 4px;
                text-align: center;
            }}
            
            .status-value {{
                font-size: 1.5rem;
                font-weight: 600;
                color: #495057;
            }}
            
            .status-label {{
                font-size: 0.9rem;
                color: #868e96;
                margin-top: 0.5rem;
            }}
            
            .shrine-actions {{
                margin: 2rem 0;
            }}
            
            .shrine-button {{
                background: #6c757d;
                color: white;
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 4px;
                font-size: 1rem;
                cursor: pointer;
                margin: 0.5rem;
                transition: background-color 0.3s ease;
            }}
            
            .shrine-button:hover {{
                background: #5a6268;
            }}
            
            .footer {{
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid #dee2e6;
                color: #adb5bd;
                font-size: 0.9rem;
            }}
        </style>
    </head>
    <body>
        <div class="shrine-container">
            <h1 class="shrine-title">🏛️ The Shrine</h1>
            <div class="shrine-subtitle">Calm and Steady Contemplative Service</div>
            
            <div class="wisdom-card">
                <div class="wisdom-theme">{daily_wisdom['theme']}</div>
                <div class="wisdom-reflection">"{daily_wisdom['reflection']}"</div>
                <div class="contemplation-focus">
                    Today's contemplative focus: {daily_wisdom['contemplation_focus']}
                </div>
            </div>
            
            <div class="shrine-status">
                <div class="status-item">
                    <div class="status-value">{status['uptime_hours']}h</div>
                    <div class="status-label">Stable Uptime</div>
                </div>
                <div class="status-item">
                    <div class="status-value">{status['active_contemplations']}</div>
                    <div class="status-label">Active Contemplations</div>
                </div>
                <div class="status-item">
                    <div class="status-value">{status['total_sessions']}</div>
                    <div class="status-label">Total Sessions</div>
                </div>
                <div class="status-item">
                    <div class="status-value">High</div>
                    <div class="status-label">Wisdom Stability</div>
                </div>
            </div>
            
            <div class="shrine-actions">
                <button class="shrine-button" onclick="beginContemplation()">Begin Contemplation</button>
                <button class="shrine-button" onclick="viewWisdom()">Daily Wisdom API</button>
                <button class="shrine-button" onclick="shrineStatus()">Shrine Status</button>
            </div>
            
            <div class="footer">
                <p>The Shrine provides stable, contemplative balance to dynamic systems</p>
                <p>Port {SHRINE_PORT} • Refreshes daily • Designed for sustained reflection</p>
            </div>
        </div>
        
        <script>
            function beginContemplation() {{
                const sessionId = 'session_' + Date.now();
                window.open('/contemplation/start/' + sessionId, '_blank');
            }}
            
            function viewWisdom() {{
                window.open('/api/wisdom', '_blank');
            }}
            
            function shrineStatus() {{
                window.open('/api/status', '_blank');
            }}
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(html_content)

@app.get("/api/wisdom")
async def get_daily_wisdom():
    """Stable daily wisdom API"""
    return wisdom.get_daily_wisdom()

@app.get("/api/status")
async def get_shrine_status():
    """Shrine status - changes slowly, emphasizes stability"""
    return wisdom.get_shrine_status()

@app.post("/contemplation/start/{session_id}")
async def start_contemplation(session_id: str):
    """Begin contemplative session"""
    return wisdom.start_contemplation_session(session_id)

@app.post("/contemplation/end/{session_id}")
async def end_contemplation(session_id: str):
    """End contemplative session"""
    return wisdom.end_contemplation_session(session_id)

@app.get("/contemplation/start/{session_id}", response_class=HTMLResponse)
async def contemplation_page(session_id: str):
    """Contemplative session page"""
    session_data = wisdom.start_contemplation_session(session_id)
    daily_wisdom = session_data['daily_wisdom']
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>🏛️ Contemplative Session</title>
        <style>
            body {{
                font-family: 'Vollkorn', Georgia, serif;
                background: #f8f9fa;
                color: #343a40;
                line-height: 1.8;
                padding: 2rem;
                text-align: center;
            }}
            
            .contemplation-space {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 3rem;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            
            .session-header {{
                color: #6c757d;
                margin-bottom: 2rem;
            }}
            
            .wisdom-display {{
                font-size: 1.2rem;
                font-style: italic;
                color: #495057;
                margin: 2rem 0;
                padding: 2rem;
                background: #f8f9fa;
                border-radius: 4px;
                border-left: 4px solid #6c757d;
            }}
            
            .contemplation-timer {{
                font-size: 1.1rem;
                color: #868e96;
                margin: 1rem 0;
            }}
            
            .end-session {{
                background: #6c757d;
                color: white;
                padding: 1rem 2rem;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 2rem;
            }}
        </style>
    </head>
    <body>
        <div class="contemplation-space">
            <h2 class="session-header">🏛️ Contemplative Session Active</h2>
            
            <div class="wisdom-display">
                <strong>{daily_wisdom['theme']}</strong><br><br>
                "{daily_wisdom['reflection']}"<br><br>
                <em>Focus: {daily_wisdom['contemplation_focus']}</em>
            </div>
            
            <div class="contemplation-timer">
                Session time: <span id="timer">0:00</span>
            </div>
            
            <p style="color: #868e96; margin: 2rem 0;">
                Take your time. Let insights emerge naturally through patient attention.
            </p>
            
            <button class="end-session" onclick="endSession()">Complete Contemplation</button>
        </div>
        
        <script>
            let startTime = Date.now();
            
            function updateTimer() {{
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsed / 60);
                const seconds = elapsed % 60;
                document.getElementById('timer').textContent = 
                    minutes + ':' + seconds.toString().padStart(2, '0');
            }}
            
            setInterval(updateTimer, 1000);
            
            async function endSession() {{
                const response = await fetch('/contemplation/end/{session_id}', {{
                    method: 'POST'
                }});
                const result = await response.json();
                
                alert(result.message + '\\n\\n' + 
                     'Session duration: ' + result.session_duration_minutes + ' minutes\\n\\n' +
                     result.wisdom_integration + '\\n\\n' +
                     result.parting_thought);
                
                window.close();
            }}
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(html_content)

@app.get("/health")
async def shrine_health():
    """Shrine health check - always stable"""
    return {
        "status": "🏛️ Serene and Stable",
        "service": "The Shrine",
        "stability": "High",
        "contemplative_readiness": "Always",
        "uptime": time.time() - wisdom.startup_time,
        "purpose": "Calm counterbalance to dynamic systems"
    }

@app.on_event("startup")
async def shrine_startup():
    """Initialize shrine with calm stability"""
    print("🏛️ The Shrine is opening...")
    print("   Contemplative service ready")
    print("   Wisdom stability: High")
    print("   Atmosphere: Calm and focused")
    print(f"   Serving on port {SHRINE_PORT}")
    print("✨ The Shrine is now open for contemplation")

def main():
    """Run the serene shrine service"""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SHRINE_PORT,
        log_level="warning"  # Quiet logging for serenity
    )

if __name__ == "__main__":
    main()