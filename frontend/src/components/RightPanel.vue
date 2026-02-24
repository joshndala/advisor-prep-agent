<script setup lang="ts">
import { computed } from 'vue'
import { useClientStore } from '../store/clientStore'
import VuePdfEmbed from 'vue-pdf-embed'

// Import pdf.js worker setting correctly
import * as pdfjsLib from 'pdfjs-dist'
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`

const store = useClientStore()

const sourceUrl = computed(() => {
  if (!store.activeSource || !store.selectedClient) return ''
  return `http://localhost:8000/api/documents/${store.selectedClient}/${store.activeSource.document_name}`
})

const isPdf = computed(() => {
  return store.activeSource?.document_name?.toLowerCase().endsWith('.pdf')
})

const pageNumber = computed(() => {
  return store.activeSource?.page || 1
})

</script>

<template>
  <div class="h-full flex flex-col relative w-full pointer-events-auto">
    <!-- Header -->
    <div class="bg-slate-800 border-b border-slate-700 p-6 shrink-0 shadow-md z-10 flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-slate-100 flex items-center gap-3">
          <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
          Source Viewer
        </h2>
        <div v-if="store.activeSource" class="text-sm mt-3 flex items-center gap-3 bg-slate-900/50 py-1.5 px-3 rounded-lg border border-slate-700/50 inline-flex">
          <span class="font-mono text-slate-300">{{ store.activeSource.document_name }}</span>
          <span class="w-px h-4 bg-slate-600"></span>
          <span class="bg-blue-600/20 text-blue-300 px-2.5 py-0.5 rounded-md font-bold text-xs border border-blue-500/30">PAGE {{ pageNumber }}</span>
        </div>
        <p v-else class="text-sm text-slate-400 mt-2">Select a source badge to trace the AI's insight here.</p>
      </div>
    </div>

    <!-- Viewer Area -->
    <div class="flex-1 overflow-auto bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0wIDEwaDQwTTEwIDB2NDAiIHN0cm9rZT0icmdiYSgyNTUsIDI1NSwgMjU1LCAwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiAvPgo8L3N2Zz4=')] bg-slate-900 pt-8 pb-32 px-8 flex justify-center relative">
      
      <div v-if="!store.activeSource" class="text-slate-500 h-full flex flex-col items-center justify-center gap-5 mt-[-10%]">
        <div class="w-24 h-24 rounded-full bg-slate-800/50 border border-slate-700 flex items-center justify-center shadow-inner">
          <svg class="w-10 h-10 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
        </div>
        <p class="font-medium text-lg">No active source</p>
      </div>
      
      <div v-else-if="isPdf" class="w-full max-w-4xl bg-white rounded-xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden ring-4 ring-slate-800/50 mx-auto transition-transform">
        <VuePdfEmbed
          :source="sourceUrl"
          :page="pageNumber"
          class="w-full min-h-[600px]"
        />
      </div>

      <div v-else class="w-full max-w-4xl bg-white rounded-xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] p-10 text-slate-800 ring-4 ring-slate-800/50 mx-auto min-h-[400px]">
        <h3 class="text-2xl font-bold mb-6 border-b-2 border-slate-200 pb-4">{{ store.activeSource.document_name }}</h3>
        <p class="whitespace-pre-wrap font-serif text-lg leading-relaxed text-slate-600">
          This file is not a PDF, but the quote can be found here:
          <br><br>
          <strong class="text-black bg-yellow-200/50 px-2 py-1 rounded">"{{ store.activeSource.extracted_quote }}"</strong>
        </p>
      </div>
    </div>
    
    <!-- Floating Exact Quote Overlay -->
    <div v-if="store.activeSource && store.activeSource.extracted_quote" class="absolute bottom-8 left-1/2 -translate-x-1/2 w-[90%] max-w-3xl z-20 pointer-events-none">
      <div class="bg-slate-800/90 backdrop-blur-md border border-slate-600 rounded-2xl p-6 shadow-2xl pointer-events-auto transform transition-all hover:-translate-y-1">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">
            <svg class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 24 24"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg>
          </div>
          <div class="text-sm text-blue-300 font-bold uppercase tracking-widest">Extracted Insight Note</div>
        </div>
        <p class="text-slate-100 text-base font-serif italic border-l-4 border-blue-500 pl-4 py-1.5 leading-relaxed shadow-sm">
          "{{ store.activeSource.extracted_quote }}"
        </p>
      </div>
    </div>
  </div>
</template>
