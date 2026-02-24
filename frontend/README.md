# Advisor Prep Agent - Frontend

This directory contains the Vue 3 frontend application for the Advisor Prep Agent, built with Vite and Tailwind CSS.

## Features

- **Split-Screen Dashboard**: A rich, modern UI that divides the workspace into the AI Agent view and the Source Viewer.
- **State Management**: Utilizes Pinia (`clientStore.ts`) to manage client selection, uploaded files, and the human-in-the-loop review state.
- **Explainable RAG UI**: Displays AI-generated agendas with clickable source badges.
- **Programmatic PDF Viewing**: Integrates `vue-pdf-embed` to dynamically load and scroll to the exact page of a financial PDF referenced by the AI.
- **Collapsible Dropzone**: Drag-and-drop file upload zone that intelligently collapses once the AI generation is complete to maximize vertical space for reading the agenda.
- **Export Workflow**: A clean modal overlay that extracts only "Approved" items and copies a formatted brief to the system clipboard.

## Tech Stack
- **Framework**: Vue 3 (Composition API)
- **Tooling**: Vite, TypeScript
- **Styling**: Tailwind CSS v4
- **State**: Pinia
- **HTTP Client**: Axios
- **PDF Rendering**: vue-pdf-embed & pdfjs-dist

## Setup Instructions

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run Development Server**
   ```bash
   npm run dev
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

The frontend expects the FastAPI backend to be running concurrently on `http://localhost:8000`.
