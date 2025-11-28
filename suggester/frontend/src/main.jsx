import React from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'


async function bootstrap() {
    const queryClient = new QueryClient();

    // Запуск MSW только если мы в development
    if (import.meta.env.DEV) {
        const { worker } = await import('./mocks/browser');
        await worker.start({
            onUnhandledRequest: 'bypass', // чтобы игнорировать неиспользуемые запросы
        });
    }

    createRoot(document.getElementById('root')).render(
        <React.StrictMode>
            <QueryClientProvider client={queryClient}>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
            </QueryClientProvider>
        </React.StrictMode>
    );
}

bootstrap();
