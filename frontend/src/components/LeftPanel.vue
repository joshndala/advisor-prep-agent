<script setup lang="ts">
import { ref } from 'vue'
import { useClientStore } from '../store/clientStore'
import ExportModal from './ExportModal.vue'

const store = useClientStore()
const fileInput = ref<HTMLInputElement | null>(null)
const isInputCollapsed = ref(false)
const isExportModalOpen = ref(false)

const handleClientChange = (e: Event) => {
  store.selectedClient = (e.target as HTMLSelectElement).value
  store.agendaItems = []
  store.activeSource = null
  store.fetchClientFiles()
  isInputCollapsed.value = false
}

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (e: Event) => {
  const target = e.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    const file = files[0]
    if (file) store.uploadFile(file)
    target.value = ''
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    const file = files[0]
    if (file) store.uploadFile(file)
  }
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const handleGeneratePrep = async () => {
  await store.generatePrep()
  if (store.agendaItems.length > 0) {
    isInputCollapsed.value = true
  }
}
</script>

<template>
  <div class="p-6 flex flex-col gap-6 h-full relative">
    <!-- Header & Client Selector -->
    <div class="shrink-0">
      <h1 class="text-3xl font-extrabold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent mb-4 tracking-tight">
        AI Advisor Prep
      </h1>
      <div class="flex items-center gap-4">
        <label class="text-sm font-medium text-slate-400">Select Client:</label>
        <select 
          :value="store.selectedClient" 
          @change="handleClientChange"
          class="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 transition-all flex-1 shadow-sm font-medium"
        >
          <option value="" disabled>Choose a client...</option>
          <option v-for="c in store.clients" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
    </div>

    <!-- Collapsible Input Area -->
    <div v-if="store.selectedClient" class="shrink-0 flex flex-col gap-4">
      
      <!-- Collapsed State -->
      <div v-if="isInputCollapsed" class="bg-slate-800/50 rounded-xl p-4 border border-slate-700 flex justify-between items-center shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          </div>
          <span class="font-medium text-slate-200">{{ store.clientFiles.length }} Documents Loaded</span>
        </div>
        <button @click="isInputCollapsed = false" class="text-sm font-semibold text-blue-400 hover:text-blue-300 bg-blue-400/10 hover:bg-blue-400/20 px-4 py-2 rounded-lg transition-colors border border-blue-400/20">
          Edit / Add
        </button>
      </div>
      
      <!-- Expanded State -->
      <div v-else class="flex flex-col gap-4">
        <!-- Upload Zone -->
        <div 
          @drop="handleDrop"
          @dragover="handleDragOver"
          @click="triggerUpload"
          class="border-2 border-dashed border-slate-600 rounded-2xl p-8 flex flex-col items-center justify-center text-slate-400 cursor-pointer hover:border-blue-500 hover:bg-slate-800/50 transition-all group shadow-sm"
        >
          <input type="file" ref="fileInput" class="hidden" @change="handleFileUpload" />
          <div class="w-14 h-14 mb-4 rounded-full bg-slate-800 flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform">
            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p class="font-medium text-slate-300">Click or drag document to upload</p>
          <p class="text-sm mt-1 opacity-70">Supports PDF, TXT, CSV, XLSX, DOCX, PNG, JPG</p>
        </div>

        <!-- Available Files -->
        <div v-if="store.clientFiles.length > 0" class="bg-slate-800/40 rounded-xl p-4 border border-slate-700/50">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 ml-1">Available Documents</h3>
          <div class="flex flex-wrap gap-2">
            <div 
              v-for="file in store.clientFiles" 
              :key="file"
              class="flex items-center gap-2 bg-slate-700/50 px-3 py-1.5 rounded-lg border border-slate-600/50 text-sm text-slate-300"
            >
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              {{ file }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Button -->
    <div v-if="store.selectedClient && !isInputCollapsed" class="shrink-0">
      <button 
        @click="handleGeneratePrep" 
        :disabled="store.isLoading"
        class="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 text-white font-medium py-3.5 rounded-xl shadow-[0_0_15px_rgba(37,99,235,0.3)] transition-all flex justify-center items-center gap-2 group"
      >
        <svg v-if="store.isLoading" class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" stroke-width="4" stroke="currentColor" stroke-opacity="0.3"></circle>
          <path d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" fill="currentColor"></path>
        </svg>
        <span v-else class="flex items-center gap-2">
          Generate Prep Brief
          <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>
        </span>
      </button>
      <p v-if="store.error" class="text-red-400 text-sm mt-3 text-center bg-red-900/20 p-2 rounded">{{ store.error }}</p>
    </div>

    <!-- Agenda List -->
    <div v-if="store.agendaItems.length > 0" class="flex-1 overflow-y-auto pr-2 pb-12 space-y-5">
      <h2 class="text-xl font-bold text-slate-200 sticky top-0 bg-slate-900 py-3 z-10 border-b border-slate-700/50 shadow-[0_4px_10px_-4px_rgba(0,0,0,0.5)]">AI Generated Agenda</h2>
      
      <div 
        v-for="item in store.agendaItems" 
        :key="item.id"
        class="bg-slate-800 rounded-2xl p-5 border shadow-lg transition-all"
        :class="{
          'border-slate-700': item.status === 'pending',
          'border-green-500/50 bg-green-900/10 shadow-green-900/20': item.status === 'approved',
          'border-red-500/50 bg-red-900/10 opacity-75 grayscale-[0.2]': item.status === 'discarded'
        }"
      >
        <div class="flex flex-wrap justify-between items-start gap-y-3 gap-x-4 mb-3">
          <h3 
            class="flex-1 min-w-[200px] font-semibold text-lg text-blue-300 leading-tight pr-4 break-words whitespace-normal transition-all"
            :class="{'line-through text-slate-500': item.status === 'discarded'}"
          >
            {{ item.topic }}
          </h3>
          <span 
            v-if="item.action_required && item.status !== 'discarded'" 
            class="text-[10px] max-w-full font-bold uppercase tracking-widest px-2.5 py-1.5 rounded-lg text-amber-200 bg-amber-900/30 border border-amber-800/50 whitespace-normal break-words text-left sm:text-right self-start"
          >
            {{ item.action_required.replace(/_/g, ' ') }}
          </span>
        </div>
        <p class="text-slate-300 text-sm mb-5 leading-relaxed">{{ item.insight }}</p>
        
        <!-- Sources -->
        <div class="flex flex-wrap gap-2 mb-5">
          <button 
            v-for="(source, idx) in item.sources" 
            :key="idx"
            @click="store.setActiveSource(source)"
            class="text-xs font-mono font-medium px-3.5 py-1.5 rounded-lg bg-slate-700/50 hover:bg-blue-600 hover:text-white text-blue-300 transition-colors border border-slate-600/50 flex items-center gap-2 group/btn"
          >
            <svg class="w-3.5 h-3.5 text-blue-400 group-hover/btn:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
            {{ source.document_name }} <span class="text-slate-500 group-hover/btn:text-blue-200">—</span> Pg {{ source.page }}
          </button>
        </div>
        
        <!-- Action Buttons / Status Badges -->
        <div v-if="item.status === 'pending'" class="flex gap-3 mt-5">
          <button 
            @click="store.approveItem(item.id)"
            class="flex-1 py-2.5 text-sm font-semibold rounded-lg transition-all focus:ring-2 focus:ring-green-500/50 bg-slate-700/50 text-green-400 hover:bg-green-600/20 border border-green-900/30 hover:border-green-500/50"
          >
            Approve
          </button>
          <button 
            @click="store.discardItem(item.id)"
            class="flex-1 py-2.5 text-sm font-semibold rounded-lg transition-all focus:ring-2 focus:ring-red-500/50 bg-slate-700/50 text-red-400 hover:bg-red-600/20 border border-red-900/30 hover:border-red-500/50"
          >
            Discard
          </button>
        </div>
        
        <!-- Approved Badge -->
        <div v-else-if="item.status === 'approved'" class="mt-5 flex items-center gap-2 text-green-400 bg-green-900/20 w-max px-3 py-1.5 rounded-lg border border-green-500/30">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          <span class="text-xs font-bold uppercase tracking-wider">Added to Agenda</span>
        </div>

        <!-- Discarded Badge -->
        <div v-else-if="item.status === 'discarded'" class="mt-5 flex items-center gap-2 text-red-400 bg-red-900/20 w-max px-3 py-1.5 rounded-lg border border-red-500/30">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          <span class="text-xs font-bold uppercase tracking-wider">Discarded</span>
        </div>
      </div>
    </div>
    
    <!-- Footer Export Button -->
    <div v-if="store.agendaItems.length > 0" class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-slate-900 via-slate-900 to-transparent pt-12">
      <button 
        @click="isExportModalOpen = true"
        :disabled="!store.isReviewComplete"
        class="w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg text-white"
        :class="store.isReviewComplete ? 'bg-indigo-600 hover:bg-indigo-500 shadow-indigo-600/30 translate-y-0' : 'bg-slate-700 text-slate-500 cursor-not-allowed border border-slate-600'"
      >
        <template v-if="store.isReviewComplete">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
          Export Final Agenda
        </template>
        <template v-else>
          <span class="text-sm">Review all pending items to export</span>
        </template>
      </button>
    </div>

    <!-- Teleport Modal -->
    <ExportModal v-if="isExportModalOpen" @close="isExportModalOpen = false" />
  </div>
</template>
