import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import ProductPage from './pages/ProductPage'
import CartPage from './pages/CartPage'

export default function App() {
    return (
        <div className="min-h-screen flex flex-col">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/product/:id" element={<ProductPage />} /> {/* <-- путь /product/:id */}
                <Route path="/cart" element={<CartPage />} />
            </Routes>
        </div>
    )
}