import React from 'react'
import { Link } from 'react-router-dom'
import { useCartStore } from '../stores/cartStore'


export default function ProductCard({ product }) {
    const add = useCartStore(state => state.add)


    return (
        <div className="bg-white rounded-lg shadow overflow-hidden flex flex-col">
            <Link to={`/product/${product.id}`} className="block flex-1">
                <div className="h-40 bg-gray-100 flex items-center justify-center overflow-hidden">
                    <img src={product.image} alt={product.title} className="object-cover h-full w-full" />
                </div>
                <div className="p-3">
                    <h3 className="font-semibold text-sm mb-1">{product.title}</h3>
                    <div className="text-lg font-medium">{product.price} ₽</div>
                </div>
            </Link>


            <div className="p-3 border-t flex items-center gap-2">
                <button onClick={() => add(product)} className="flex-1 bg-sber text-white py-2 rounded">Добавить в корзину</button>
            </div>
        </div>
    )
}