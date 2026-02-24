<script setup lang="ts">
import { onMounted } from 'vue'
import { useClientStore } from './store/clientStore'
import LeftPanel from './components/LeftPanel.vue'
import RightPanel from './components/RightPanel.vue'

const store = useClientStore()

onMounted(() => {
  store.fetchClients()
})
</script>

<template>
  <div class="flex h-screen w-full bg-slate-900 text-slate-100 overflow-hidden font-sans">
    <div class="w-1/2 h-full border-r border-slate-700 overflow-y-auto">
      <LeftPanel />
    </div>
    <div class="w-1/2 h-full bg-slate-800 flex flex-col relative overflow-hidden">
      <RightPanel />
    </div>
  </div>
</template>
