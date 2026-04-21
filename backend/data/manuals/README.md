# Vehicle Service Manuals

## Purpose
Place PDF service manuals here for RAG-powered diagnostic assistance.

## Supported Vehicles (Kerala Market)

### Cars
- Maruti Suzuki: Swift, Alto, Baleno, Dzire, WagonR, Ertiga
- Hyundai: i20, Creta, Grand i10, Venue, Verna
- Tata: Nexon, Altroz, Tiago, Harrier, Safari
- Honda: City, Amaze, Jazz
- Toyota: Innova, Fortuner, Glanza
- Mahindra: Scorpio, XUV700, Thar, Bolero
- Kia: Seltos, Sonet, Carens
- MG: Hector, Astor

### Two-Wheelers
- Hero: Splendor, Passion, Glamour, Xtreme
- Honda: Activa, Shine, Unicorn, Hornet
- Bajaj: Pulsar, Platina, Avenger, Dominar
- TVS: Apache, Jupiter, Ntorq, Raider
- Royal Enfield: Classic, Bullet, Himalayan, Meteor

## How to Add Manuals

1. **Download** official service manuals (PDF format)
2. **Name** descriptively: `Make_Model_Year.pdf`
   - Example: `Maruti_Swift_2019.pdf`
   - Example: `Hero_Splendor_Plus_2020.pdf`
3. **Place** in this directory
4. **Restart** backend server

The system will automatically:
- Extract text from PDFs
- Chunk into 500-character segments
- Generate embeddings (all-MiniLM-L6-v2)
- Store in ChromaDB vector database
- Enable semantic search during diagnostics

## Manual Sources

### Official Dealerships
- Request service manuals from authorized dealers
- Often available for purchase or free with vehicle

### Online Resources
- Manufacturer websites (owner's section)
- Automotive forums (Kerala Auto Forum, Team-BHP)
- Service manual repositories (with proper licensing)

### Workshop Manuals
- Haynes manuals
- Chilton manuals
- Factory service manuals (FSM)

## File Format Requirements

- **Format**: PDF only
- **Size**: No limit (chunked automatically)
- **Quality**: Text-based PDFs preferred (not scanned images)
- **Language**: English or Malayalam

## What Gets Indexed

The RAG system extracts:
- Diagnostic procedures
- Torque specifications
- Fluid capacities
- Wiring diagrams (text descriptions)
- Maintenance schedules
- Troubleshooting flowcharts
- Part numbers and specifications

## Privacy & Licensing

⚠️ **Important**: Only use manuals you have legal rights to use.
- Personal use: OK for your own workshop
- Commercial use: Ensure proper licensing
- Distribution: Do not redistribute copyrighted materials

## Current Status

📁 No manuals indexed yet.

Add PDFs here and restart the backend to enable RAG-powered diagnostics.

---

Need help finding manuals? Check Kerala automotive forums or contact vehicle dealerships.
