# 💬 Conversation Memory System

## Overview
AutoMech AI now maintains conversation history across messages, providing a natural chat experience where the AI remembers previous context.

## How It Works

### Backend Implementation
1. **ChatHistory Database Table**: Stores all conversation messages with session tracking
   - `session_id`: Unique identifier linking messages in the same conversation
   - `role`: Either 'user' or 'assistant'
   - `content`: The message text
   - `vehicle_id`: Optional link to vehicle profile
   - `created_at`: Timestamp

2. **Session Management**: 
   - Each conversation gets a unique session_id (UUID)
   - Session persists across multiple messages
   - Last 10 messages are retrieved for context

3. **Agent Integration**:
   - Chat history is passed to the agentic AI system
   - Agent uses previous context to provide better responses
   - Maintains continuity in multi-turn conversations

### Frontend Implementation
- Stores `session_id` in component state
- Automatically sends session_id with each request
- Receives and updates session_id from backend responses

## Features

✅ **Context Awareness**: AI remembers what you discussed earlier
✅ **Follow-up Questions**: Ask clarifying questions without repeating context
✅ **Natural Conversations**: Chat flows naturally like talking to a mechanic
✅ **Session Persistence**: Conversation history stored in database
✅ **Vehicle Context**: Links conversations to specific vehicles

## Example Usage

```
User: My car is making a grinding noise when I brake
AI: That grinding noise typically indicates worn brake pads...

User: How much would it cost to replace them?
AI: [Remembers we're talking about brake pads] For your vehicle, brake pad replacement typically costs...

User: What about the rotors?
AI: [Remembers brake context] If the rotors are damaged from worn pads, you'll need...
```

## Technical Details

### Database Schema
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    vehicle_id INTEGER,
    role VARCHAR NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### API Changes
- **Request**: Added `session_id` field to DiagnosticRequest
- **Response**: Returns `session_id` for frontend to store

### Memory Retrieval
- Retrieves last 10 messages per session
- Orders chronologically (oldest first)
- Formats as conversation history for agent

## Benefits

1. **Better Diagnostics**: AI can ask follow-up questions and refine diagnosis
2. **User Experience**: Natural conversation flow without repetition
3. **Context Retention**: Remembers vehicle details, symptoms, and previous suggestions
4. **Learning**: System can track conversation patterns for improvement

## Future Enhancements

- [ ] Conversation summarization for long sessions
- [ ] Cross-session learning (similar issues across users)
- [ ] Conversation export/sharing
- [ ] Voice conversation support with memory
- [ ] Multi-vehicle conversation tracking
