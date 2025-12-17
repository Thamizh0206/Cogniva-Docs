# Cogniva Docs - Project Renaming Summary

## Changes Made

### 1. Frontend Updates
- Updated `frontend/package.json` to change project name from "vite_react_shadcn_ts" to "cogniva-docs"
- Updated `frontend/index.html` to change page title from "PDF AI Assistant" to "Cogniva Docs"
- Updated `frontend/src/pages/Index.tsx` to change application name from "PDF AI Assistant" to "Cogniva Docs"
- Updated placeholder text in the chat input from "Ask a question about your PDFs..." to "Ask a question about your documents..."

### 2. Backend/API Updates
- Updated `api.py` to change API title from "Multi-PDF Chat API" to "Cogniva Docs API"
- Updated root endpoint message from "Multi-PDF Chat API is running!" to "Cogniva Docs API is running!"

### 3. Documentation Updates
- Updated `README.md` to change project name from "Multi-PDF-s ChatApp AI Agent" to "Cogniva Docs"
- Updated `Backend_README.md` to change title from "Multi-PDF Chat App - FastAPI Backend" to "Cogniva Docs - FastAPI Backend"

## Manual Steps Required

### Directory Renaming
Due to active processes using the directories, you'll need to manually rename the directories when the servers are not running:

1. Stop all running servers (FastAPI backend and React frontend)
2. Rename the main project directory:
   - From: `multi_pdf\Multi-PDFs_ChatApp_AI-Agent`
   - To: `multi_pdf\Cogniva_Docs`

### Verification
After renaming the directories, verify that the application still works correctly by:
1. Starting the backend server: `python api.py`
2. Starting the frontend server: `npm run dev`
3. Accessing the application in your browser