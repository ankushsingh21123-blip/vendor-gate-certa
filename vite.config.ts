import {defineConfig} from 'vite';
export default defineConfig({root:'web',server:{proxy:{'/api':'http://127.0.0.1:4178'}},test:{environment:'jsdom',include:['**/*.test.tsx']}});
