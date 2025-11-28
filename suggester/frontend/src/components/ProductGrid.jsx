import React, { useState, useRef, useCallback, useEffect } from 'react'
import ProductCard from './ProductCard'
import { fetchCatalog } from '../services/api'

export default function ProductGrid({ search }) {
    const [items, setItems] = useState([])
    const [page, setPage] = useState(1)
    const [hasMore, setHasMore] = useState(true)
    const [loading, setLoading] = useState(false)

    const observerRef = useRef()

    const loadMore = useCallback(async () => {
        if (loading || !hasMore) return
        setLoading(true)
        const res = await fetchCatalog({ page, q: search })
        setItems(prev => [...prev, ...res.items])
        setHasMore(!!res.nextPage)
        setPage(prev => prev + 1)
        setLoading(false)
    }, [page, search, loading, hasMore])

    const loadMoreRef = useCallback(node => {
        if (observerRef.current) observerRef.current.disconnect()
        observerRef.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {
                loadMore()
            }
        })
        if (node) observerRef.current.observe(node)
    }, [loadMore])

    // обновляем при смене поиска
    useEffect(() => {
        setItems([])
        setPage(1)
        setHasMore(true)
    }, [search])

    return (
        <div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {items.map(item => (
                    <ProductCard key={item.id} product={item} />
                ))}
            </div>

            <div ref={loadMoreRef} className="mt-4 text-center">
                {loading ? 'Загрузка...' : hasMore ? 'Прокрутите вниз для загрузки' : 'Больше нет товаров'}
            </div>
        </div>
    )
}
