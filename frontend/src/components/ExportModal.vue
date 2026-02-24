<script setup lang="ts">
import { ref } from 'vue'
import { useClientStore } from '../store/clientStore'

const store = useClientStore()
const emit = defineEmits(['close'])

const copied = ref(false)

const handleCopy = async () => {
  let textToCopy = `Prep Brief: ${store.selectedClient}\n\n`
  
  store.approvedAgendaItems.forEach((item, index) => {
    textToCopy += `${index + 1}. [${item.topic}]\n`
    textToCopy += `Insight: ${item.insight}\n`

    textToCopy += '\n'
  })

  try {
    await navigator.clipboard.writeText(textToCopy)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch (err) {
    console.error('Failed to copy text', err)
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm p-4">
    <div class="bg-slate-800 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="p-6 border-b border-slate-700 flex justify-between items-center shrink-0">
        <h2 class="text-2xl font-bold text-slate-100 flex items-center gap-3">
          <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          Finalized Agenda
        </h2>
        <button @click="emit('close')" class="text-slate-400 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>

      <!-- Scrollable Preview Area -->
      <div class="p-6 overflow-y-auto flex-1 font-serif bg-slate-900/50 text-slate-300">
        <div class="mb-6">
          <h3 class="text-xl font-bold text-slate-100 uppercase tracking-widest mb-1">Client Brief</h3>
          <p class="text-blue-400 font-mono">{{ store.selectedClient }}</p>
        </div>
        
        <div class="space-y-6">
          <div v-for="(item, idx) in store.approvedAgendaItems" :key="item.id" class="border-l-2 border-blue-500/50 pl-4 py-1">
            <h4 class="font-bold text-lg text-slate-200 mb-2">{{ idx + 1 }}. {{ item.topic }}</h4>
            <p class="text-slate-400 leading-relaxed mb-3">{{ item.insight }}</p>

          </div>
        </div>

        <div v-if="store.approvedAgendaItems.length === 0" class="text-center py-10 text-slate-500 italic">
          No items were approved for the final agenda.
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="p-6 border-t border-slate-700 flex justify-end gap-3 shrink-0 bg-slate-800 rounded-b-2xl">
        <button @click="emit('close')" class="px-5 py-2.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-700 transition-colors font-medium">
          Close
        </button>
        <button 
          @click="handleCopy"
          :class="copied ? 'bg-green-600 hover:bg-green-500' : 'bg-blue-600 hover:bg-blue-500'"
          class="flex items-center gap-2 px-6 py-2.5 rounded-lg text-white font-medium shadow-lg transition-all"
        >
          <svg v-if="copied" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" /></svg>
          {{ copied ? 'Copied!' : 'Copy to Clipboard' }}
        </button>
      </div>

    </div>
  </div>
</template>
