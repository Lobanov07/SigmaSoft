import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useCartStore } from '../stores/cartStore'


export default function Header({ onSearch }) {
    const cart = useCartStore(state => state.items)
    const navigate = useNavigate()


    return (
        <header className="bg-white shadow">
            <div className="container mx-auto p-4 flex items-center gap-4">
                <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/') }>
                    <div className="w-10 h-10 rounded-full bg-sber flex items-center justify-center text-white font-bold">S</div>
                    <div className="text-lg font-semibold">Suggester</div>
                </div>


                <div className="flex-1">
                    <input
                        type="search"
                        placeholder="Поиск товаров"
                        className="w-full border rounded px-3 py-2"
                        onChange={(e) => onSearch(e.target.value)}
                    />
                </div>


                <nav className="flex items-center gap-4">
                    <Link to="/cart" className="relative">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-sber" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4" />
                        </svg>
                        {cart.length > 0 && (
                            <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full text-xs px-1">{cart.length}</span>
                        )}
                    </Link>
                </nav>
            </div>
        </header>
    )
}