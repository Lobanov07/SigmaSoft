import React from 'react'
import { useCartStore } from '../stores/cartStore'


export default function CartPage() {
    const items = useCartStore(state => state.items)
    const remove = useCartStore(state => state.remove)


    return (
        <div className="container mx-auto p-4">
            <h2 className="text-2xl font-semibold mb-4">Корзина</h2>
            {items.length === 0 ? <div>Корзина пуста</div> : (
                <div className="grid grid-cols-1 gap-4">
                    {items.map(it => (
                        <div key={it.id} className="flex items-center gap-4 bg-white p-3 rounded shadow">
                            <img src={it.image} className="w-20 h-20 object-cover" />
                            <div className="flex-1">
                                <div className="font-semibold">{it.title}</div>
                                <div className="text-gray-600">{it.price} ₽</div>
                            </div>
                            <button onClick={() => remove(it.id)} className="text-red-500">Удалить</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}