import React, { useState } from 'react'
import { sendFeedback } from '../services/api'


export default function FeedbackWidget({ productId, recId, onSubmitted }) {
    const [value, setValue] = useState(null)
    const [loading, setLoading] = useState(false)
    const [done, setDone] = useState(false)


    async function submit() {
        if (!value) return
        setLoading(true)
        setDone(true)
        try {
            await sendFeedback({ product_id: productId, rec_id: recId, feedback: value })
            if (onSubmitted) onSubmitted(value)
        } catch (e) {
            setDone(false)
            console.error(e)
        } finally {
            setLoading(false)
        }
    }


    if (done) return <div className="text-green-700 text-sm">Спасибо!</div>


    return (
        <div className="flex items-center gap-3">
            <button onClick={() => setValue('like')} className={`px-2 py-1 border rounded ${value==='like' ? 'bg-sber text-white':''}`}>👍</button>
            <button onClick={() => setValue('dislike')} className={`px-2 py-1 border rounded ${value==='dislike' ? 'bg-red-200':''}`}>👎</button>
            <button onClick={submit} disabled={!value || loading} className="ml-auto px-3 py-1 rounded bg-sber text-white disabled:opacity-50">Оценить</button>
        </div>
    )
}