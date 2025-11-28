import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { fetchProduct, fetchSimilar } from '../services/api'
import ProductCard from '../components/ProductCard'
import FeedbackWidget from '../components/FeedbackWidget'

export default function ProductPage() {
    const { id } = useParams()

    const { data: product, isLoading } = useQuery({
        queryKey: ['product', id],
        queryFn: () => fetchProduct(id),
    })

    const { data: similar } = useQuery({
        queryKey: ['similar', id],
        queryFn: () => fetchSimilar(id),
        enabled: !!product,
    })

    if (isLoading) return <div className="p-4">Загрузка...</div>
    if (!product) return <div className="p-4">Товар не найден</div>

    return (
        <div className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2">
                <div className="bg-white rounded shadow p-4">
                    <img src={product.image} alt={product.title} className="w-full h-96 object-contain" />
                    <div className="mt-4 flex gap-2">
                        {product.images?.map((img, idx) => (
                            <img key={idx} src={img} className="w-20 h-20 object-cover rounded" />
                        ))}
                    </div>

                    <h1 className="text-2xl font-semibold mt-4">{product.title}</h1>
                    <div className="text-lg font-medium mt-2">{product.price} ₽</div>
                    <p className="mt-4 text-gray-700">{product.description}</p>
                </div>

                {similar?.length > 0 && (
                    <div className="mt-6">
                        <h3 className="text-xl font-semibold mb-2">Похожие товары</h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {similar.map((s) => (
                                <div key={s.id} className="bg-white p-2 rounded shadow">
                                    <ProductCard product={s} />
                                    <div className="mt-2">
                                        <FeedbackWidget productId={product.id} recId={s.id} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            <aside>
                <div className="bg-white rounded shadow p-4">
                    <h4 className="font-semibold">Визуализация признаков</h4>
                    <ul className="mt-2 text-sm text-gray-600">
                        {product.features?.map((f, i) => <li key={i}>• {f}</li>)}
                    </ul>
                </div>
            </aside>
        </div>
    )
}
