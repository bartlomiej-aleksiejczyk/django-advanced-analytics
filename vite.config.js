import {dirname, resolve} from "node:path";
import {fileURLToPath} from "node:url";
import {defineConfig} from "vite";
import {svelte} from "@sveltejs/vite-plugin-svelte";
import tailwindcss from '@tailwindcss/vite'

const __dirname = dirname(fileURLToPath(import.meta.url));

// https://vite.dev/config/
export default defineConfig({
    plugins: [svelte(), tailwindcss()],
    build: {
        manifest: true,
        outDir: resolve(__dirname, "client_components__dist"),
        server: {
            open: "client_components/main.js",  // Change default file
        },
        lib: {
            entry: resolve(__dirname, "client_components/main.js"),
            name: "OfflineNotesClientComponents",
            fileName: "offline_notes_client_components",
            formats: ["es"],
        },
    },
});
