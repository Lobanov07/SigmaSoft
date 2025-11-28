import React, { useState } from 'react'
import Header from '../components/Header'
import ProductGrid from '../components/ProductGrid'


export default function Home() {
    const [query, setQuery] = useState('')


    return (
        <div className="flex-1">
            <Header onSearch={setQuery} />


            <main className="container mx-auto p-4">
                <h2 className="text-2xl font-semibold mb-4">Подборки — White Box</h2>
                <ProductGrid search={query} />
            </main>
        </div>
    )
}