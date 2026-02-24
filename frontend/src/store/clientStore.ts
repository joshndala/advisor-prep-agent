import { defineStore } from 'pinia';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const useClientStore = defineStore('client', {
    state: () => ({
        clients: [] as string[],
        selectedClient: '',
        agendaItems: [] as any[],
        activeSource: null as any,
        clientFiles: [] as string[],
        isLoading: false,
        error: ''
    }),
    getters: {
        approvedAgendaItems(state) {
            return state.agendaItems.filter(item => item.status === 'approved');
        },
        isReviewComplete(state) {
            return state.agendaItems.length > 0 &&
                state.agendaItems.every(item => item.status !== 'pending');
        }
    },
    actions: {
        async fetchClients() {
            try {
                const response = await axios.get(`${API_BASE}/clients`);
                this.clients = response.data.clients;
            } catch (err: any) {
                this.error = 'Failed to load clients';
            }
        },
        async fetchClientFiles() {
            if (!this.selectedClient) return;
            try {
                const response = await axios.get(`${API_BASE}/clients/${this.selectedClient}/files`);
                this.clientFiles = response.data.files;
            } catch (err: any) {
                console.error('Failed to load client files', err);
            }
        },
        async generatePrep() {
            if (!this.selectedClient) return;
            this.isLoading = true;
            this.error = '';
            try {
                const response = await axios.post(`${API_BASE}/generate_prep/${this.selectedClient}`);
                this.agendaItems = response.data.ai_generated_agenda.map((item: any) => ({
                    ...item,
                    status: 'pending' // track local human-in-the-loop status: 'pending', 'approved', 'discarded'
                }));
            } catch (err: any) {
                this.error = err.response?.data?.detail || 'Failed to generate prep';
            } finally {
                this.isLoading = false;
            }
        },
        async uploadFile(file: File) {
            if (!this.selectedClient) return;
            this.isLoading = true;
            try {
                const formData = new FormData();
                formData.append('file', file);
                await axios.post(`${API_BASE}/upload/${this.selectedClient}`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                await this.fetchClientFiles();
            } catch (err: any) {
                this.error = 'Upload failed';
            } finally {
                this.isLoading = false;
            }
        },
        setActiveSource(source: any) {
            this.activeSource = source;
        },
        approveItem(id: string) {
            const item = this.agendaItems.find(i => i.id === id);
            if (item) item.status = 'approved';
        },
        discardItem(id: string) {
            const item = this.agendaItems.find(i => i.id === id);
            if (item) item.status = 'discarded';
        }
    }
});
