from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
import uvicorn
from datetime import datetime

from database import init_db, get_db, VehicleProfile, DiagnosticHistory, User, ChatHistory
from agent import run_diagnostic
from tools.rag_tool import ingest_all_manuals
from language_support import detect_language, enhance_prompt_for_malayalam, get_malayalam_greeting
from tools.parts_scraper import scrape_parts, format_parts_results
from tools.image_analyzer import analyze_vehicle_image, save_uploaded_image
from structured_diagnostic import (
    analyze_initial_symptom,
    generate_diagnosis_with_parts,
    format_structured_response
)
from auth import verify_password, get_password_hash, create_access_token, verify_token
from proactive_agent import ProactiveAgent, SeasonalAdvisor

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AutoMech AI",
    description="AI-powered automotive diagnostic assistant for Kerala, India",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# ── Schemas ──────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class VehicleCreate(BaseModel):
    name: str
    make: str
    model: str
    year: int
    mileage: Optional[float] = None
    fuel_type: Optional[str] = "Petrol"


class VehicleOut(BaseModel):
    id: int
    name: str
    make: str
    model: str
    year: int
    mileage: Optional[float]
    fuel_type: Optional[str]

    class Config:
        from_attributes = True


class DiagnosticRequest(BaseModel):
    symptoms: str
    vehicle_id: Optional[int] = None
    obd_code: Optional[str] = None
    session_id: Optional[str] = None  # For conversation continuity


class DiagnosticOut(BaseModel):
    diagnosis: str
    vehicle_context: str
    products: Optional[List[Dict]] = []


class StructuredDiagnosticStart(BaseModel):
    symptom: str
    vehicle_id: Optional[int] = None


class StructuredDiagnosticAnswer(BaseModel):
    symptom: str
    answers: Dict[str, str]
    vehicle_id: Optional[int] = None


class HistoryOut(BaseModel):
    id: int
    vehicle_id: int
    symptoms: str
    diagnosis: str

    class Config:
        from_attributes = True


# ── Lifecycle ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    await init_db()
    ingest_all_manuals()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "AutoMech AI is running 🔧", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"ok": True}


# ── Authentication ────────────────────────────────────────────────────────────

@app.post("/api/auth/register", response_model=Token, tags=["Authentication"])
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if username exists
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.username, "user_id": new_user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


@app.post("/api/auth/login", response_model=Token, tags=["Authentication"])
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with username and password"""
    # Find user
    result = await db.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/api/auth/me", response_model=UserOut, tags=["Authentication"])
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get current user from token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# Vehicles CRUD
@app.post("/vehicles/", response_model=VehicleOut, tags=["Vehicles"])
async def create_vehicle(data: VehicleCreate, db: AsyncSession = Depends(get_db)):
    vehicle = VehicleProfile(**data.model_dump())
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@app.get("/vehicles/", response_model=List[VehicleOut], tags=["Vehicles"])
async def list_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VehicleProfile).order_by(VehicleProfile.created_at.desc()))
    return result.scalars().all()


@app.get("/vehicles/{vehicle_id}", response_model=VehicleOut, tags=["Vehicles"])
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VehicleProfile).where(VehicleProfile.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.delete("/vehicles/{vehicle_id}", tags=["Vehicles"])
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VehicleProfile).where(VehicleProfile.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    await db.delete(vehicle)
    await db.commit()
    return {"message": f"Vehicle {vehicle_id} deleted"}


# Diagnostics
@app.post("/diagnose/", tags=["Diagnostics"])
async def diagnose(req: DiagnosticRequest, db: AsyncSession = Depends(get_db)):
    # Generate session_id if not provided
    import uuid
    session_id = req.session_id or str(uuid.uuid4())
    
    vehicle_context = ""
    vehicle_make = ""
    vehicle_model = ""

    if req.vehicle_id:
        result = await db.execute(
            select(VehicleProfile).where(VehicleProfile.id == req.vehicle_id)
        )
        v = result.scalar_one_or_none()
        if v:
            vehicle_context = (
                f"{v.year} {v.make} {v.model}, "
                f"{int(v.mileage or 0):,} km, {v.fuel_type}"
            )
            vehicle_make = v.make
            vehicle_model = v.model

    symptoms = req.symptoms
    if req.obd_code:
        symptoms = f"OBD Code: {req.obd_code.strip().upper()}. Additional symptoms: {symptoms}"

    # Detect language (Malayalam or English)
    detected_lang = detect_language(symptoms)
    if detected_lang == 'ml':
        print(f"🇮🇳 Malayalam language detected")
    
    # Retrieve chat history for this session (last 10 messages)
    chat_history_result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(10)
    )
    chat_history_records = chat_history_result.scalars().all()
    chat_history_records.reverse()  # Oldest first
    
    # Format chat history for the agent
    chat_history = []
    for record in chat_history_records:
        chat_history.append({
            "role": record.role,
            "content": record.content
        })
    
    print(f"💬 Retrieved {len(chat_history)} previous messages for session {session_id[:8]}...")

    # Use agentic AI system
    try:
        from agentic_agent import create_agentic_automech
        agent = create_agentic_automech(user_id=str(req.vehicle_id) if req.vehicle_id else None)
        
        context = {
            "vehicle_context": vehicle_context,
            "vehicle_make": vehicle_make,
            "vehicle_model": vehicle_model,
            "chat_history": chat_history,
            "language": detected_lang  # Pass detected language to agent
        }
        
        result = agent.diagnose(symptoms, context)
        diagnosis = result["diagnosis"]
        
        # Add agentic info to response
        print(f"🤖 Agentic AI used {result['tools_used']} in {result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"⚠️ Agentic AI failed, using fallback: {e}")
        # Fallback to simple diagnostic
        from agent import run_diagnostic
        diagnosis = run_diagnostic(symptoms, vehicle_context)
    
    # Extract parts from diagnosis and scrape products
    products = []
    try:
        # Try to identify parts mentioned in diagnosis
        import re
        
        # Common auto parts keywords (more flexible matching)
        parts_keywords = {
            'spark plug': ['spark plug', 'sparkplug', 'ignition plug'],
            'brake pad': ['brake pad', 'brake pads', 'brakepad'],
            'brake disc': ['brake disc', 'brake rotor', 'rotor'],
            'oil filter': ['oil filter'],
            'air filter': ['air filter'],
            'battery': ['battery', 'car battery'],
            'alternator': ['alternator'],
            'starter': ['starter motor', 'starter'],
            'radiator': ['radiator'],
            'thermostat': ['thermostat'],
            'coolant': ['coolant', 'antifreeze'],
            'brake fluid': ['brake fluid'],
            'engine oil': ['engine oil', 'motor oil'],
            'clutch': ['clutch plate', 'clutch'],
            'timing belt': ['timing belt'],
            'fuel pump': ['fuel pump'],
            'oxygen sensor': ['oxygen sensor', 'o2 sensor'],
            'shock absorber': ['shock absorber', 'shock'],
            'headlight': ['headlight', 'head light'],
            'wiper blade': ['wiper blade', 'wiper'],
            'tyre': ['tyre', 'tire', 'tyres', 'tires'],
            'bulb': ['bulb', 'light bulb', 'headlight bulb'],
        }
        
        diagnosis_lower = diagnosis.lower()
        found_parts = []
        
        print(f"🔍 Searching for parts in diagnosis...")
        
        for part_name, variations in parts_keywords.items():
            for variation in variations:
                if variation in diagnosis_lower:
                    found_parts.append(part_name)
                    print(f"✅ Found part: {part_name} (matched: {variation})")
                    break
        
        if not found_parts:
            print("⚠️ No parts detected in diagnosis")
        
        # Scrape products for found parts (max 2 parts)
        for part in found_parts[:2]:
            print(f"🛒 Scraping products for: {part}")
            try:
                scraped = scrape_parts(part, vehicle_make, vehicle_model)
                print(f"   Found {len(scraped)} products")
                products.extend(scraped[:3])  # Top 3 per part
            except Exception as e:
                print(f"   Failed to scrape {part}: {e}")
                
    except Exception as e:
        print(f"❌ Product scraping error: {e}")

    # Save to history
    if req.vehicle_id:
        history = DiagnosticHistory(
            vehicle_id=req.vehicle_id,
            symptoms=symptoms,
            diagnosis=diagnosis,
        )
        db.add(history)
        await db.commit()

    # Save chat messages to history
    user_message = ChatHistory(
        session_id=session_id,
        vehicle_id=req.vehicle_id,
        role="user",
        content=symptoms
    )
    assistant_message = ChatHistory(
        session_id=session_id,
        vehicle_id=req.vehicle_id,
        role="assistant",
        content=diagnosis
    )
    db.add(user_message)
    db.add(assistant_message)
    await db.commit()
    
    print(f"💾 Saved chat messages to session {session_id[:8]}...")

    return {
        "diagnosis": diagnosis,
        "vehicle_context": vehicle_context,
        "products": products,
        "session_id": session_id  # Return session_id to frontend
    }


# Structured Diagnostic Flow
@app.post("/diagnose/structured/start", tags=["Diagnostics"])
async def start_structured_diagnostic(req: StructuredDiagnosticStart, db: AsyncSession = Depends(get_db)):
    """
    Start structured diagnostic - analyze symptom and return follow-up questions
    """
    vehicle_context = ""
    if req.vehicle_id:
        result = await db.execute(
            select(VehicleProfile).where(VehicleProfile.id == req.vehicle_id)
        )
        v = result.scalar_one_or_none()
        if v:
            vehicle_context = f"{v.year} {v.make} {v.model}"
    
    analysis = analyze_initial_symptom(req.symptom)
    
    return {
        "symptom": req.symptom,
        "category": analysis['category'],
        "severity": analysis['severity'],
        "initial_assessment": analysis['initial_assessment'],
        "questions": analysis['questions'],
        "vehicle_context": vehicle_context
    }


@app.post("/diagnose/structured/complete", tags=["Diagnostics"])
async def complete_structured_diagnostic(req: StructuredDiagnosticAnswer, db: AsyncSession = Depends(get_db)):
    """
    Complete structured diagnostic - generate diagnosis with parts recommendations
    """
    vehicle_context = ""
    if req.vehicle_id:
        result = await db.execute(
            select(VehicleProfile).where(VehicleProfile.id == req.vehicle_id)
        )
        v = result.scalar_one_or_none()
        if v:
            vehicle_context = f"{v.year} {v.make} {v.model}, {int(v.mileage or 0):,} km, {v.fuel_type}"
    
    diagnosis_data = generate_diagnosis_with_parts(req.symptom, req.answers, vehicle_context)
    formatted_text = format_structured_response(diagnosis_data)
    
    # Save to history
    if req.vehicle_id:
        history = DiagnosticHistory(
            vehicle_id=req.vehicle_id,
            symptoms=req.symptom,
            diagnosis=formatted_text,
        )
        db.add(history)
        await db.commit()
    
    return {
        "diagnosis_text": formatted_text,
        "diagnosis_data": diagnosis_data,
        "vehicle_context": vehicle_context
    }


@app.get("/history/{vehicle_id}", response_model=List[HistoryOut], tags=["Diagnostics"])
async def get_history(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DiagnosticHistory)
        .where(DiagnosticHistory.vehicle_id == vehicle_id)
        .order_by(DiagnosticHistory.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


# Parts Search
@app.get("/parts/search", tags=["Parts"])
async def search_parts(part_name: str, make: str = "", model: str = ""):
    """Search for automotive parts online"""
    parts = scrape_parts(part_name, make, model)
    formatted = format_parts_results(parts)
    return {"results": parts, "formatted": formatted}


# Image Upload & Analysis
@app.post("/analyze/image", tags=["Analysis"])
async def analyze_image(file: UploadFile = File(...)):
    """Upload and analyze vehicle damage image"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save image
    file_data = await file.read()
    file_path = save_uploaded_image(file_data, file.filename)
    
    # Analyze
    analysis = analyze_vehicle_image(file_path)
    
    return {"analysis": analysis, "file_path": file_path}


# ── Proactive Features ────────────────────────────────────────────────────────

@app.get("/proactive/maintenance/{vehicle_id}", tags=["Proactive"])
async def get_proactive_maintenance(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    """Get proactive maintenance predictions for a vehicle"""
    result = await db.execute(select(VehicleProfile).where(VehicleProfile.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    proactive = ProactiveAgent()
    
    vehicle_info = {
        "mileage": vehicle.mileage or 0,
        "year": vehicle.year,
        "last_service_mileage": vehicle.mileage or 0,  # Can be enhanced with service history
    }
    
    predictions = proactive.predict_maintenance(vehicle_info)
    message = proactive.generate_proactive_message(vehicle_info)
    
    return {
        "vehicle_id": vehicle_id,
        "predictions": predictions,
        "message": message
    }


@app.get("/proactive/seasonal", tags=["Proactive"])
async def get_seasonal_advice():
    """Get seasonal maintenance advice for Kerala climate"""
    advisor = SeasonalAdvisor()
    advice = advisor.get_seasonal_advice()
    message = advisor.format_seasonal_message()
    
    return {
        "season": advice["season"],
        "advice": advice["advice"],
        "common_issues": advice["common_issues"],
        "message": message
    }


@app.post("/proactive/predict-issues", tags=["Proactive"])
async def predict_future_issues(symptoms: str, vehicle_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    """Predict potential future issues based on current symptoms"""
    vehicle_info = {}
    
    if vehicle_id:
        result = await db.execute(select(VehicleProfile).where(VehicleProfile.id == vehicle_id))
        vehicle = result.scalar_one_or_none()
        if vehicle:
            vehicle_info = {
                "mileage": vehicle.mileage or 0,
                "year": vehicle.year,
                "make": vehicle.make,
                "model": vehicle.model
            }
    
    proactive = ProactiveAgent()
    predictions = proactive.predict_issues_from_symptoms(symptoms, vehicle_info)
    
    if not predictions:
        return {
            "predictions": [],
            "message": "No specific future issues predicted. Continue monitoring symptoms."
        }
    
    message = "⚠️ **Potential Future Issues:**\n\n"
    for pred in predictions:
        message += f"**Current: {pred['current_symptom'].title()}**\n"
        message += f"  • May lead to: {', '.join(pred['future_issues'])}\n"
        message += f"  • Timeframe: {pred['timeframe']}\n"
        message += f"  • Prevention: {pred['prevention']}\n\n"
    
    return {
        "predictions": predictions,
        "message": message
    }


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
