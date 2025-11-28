import MOCK_DATA from "./whitebox_products.json";


export async function sendFeedback(event) {
// event: { product_id, rec_id, feedback }
// For now just log and resolve. Later replace with POST to backend.
    console.log('Feedback event:', event)
    await new Promise(r => setTimeout(r, 150))
    return { status: 'ok' }
}
export async function fetchCatalog({ page = 1, pageSize = 12, q = '' } = {}) {
    await new Promise(r => setTimeout(r, 200))
    const filtered = MOCK_DATA.filter(it => it.title.toLowerCase().includes(q.toLowerCase()))
    const start = (page - 1) * pageSize
    const items = filtered.slice(start, start + pageSize)
    const nextPage = start + pageSize < filtered.length ? page + 1 : undefined

    return { items, nextPage }  // <- обязательно объект, не массив
}


export async function fetchProduct(id) {
    await new Promise(r => setTimeout(r, 150))
    return MOCK_DATA.find(p => Number(p.id) === Number(id))
}

export async function fetchSimilar(id) {
    await new Promise(r => setTimeout(r, 150))
    // просто возвращаем 12 случайных товаров из MOCK_DATA
    return MOCK_DATA.slice(0, 12)
}
