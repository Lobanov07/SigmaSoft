import { http, HttpResponse } from "msw";
import whiteBoxProducts from "./whitebox_products.json";

// ===============================================================
//                          HANDLERS
// ===============================================================

export const handlers = [
    // ========= список всех товаров ==========
    http.get("/api/products", () => {
        return HttpResponse.json({
            items: whiteBoxProducts,
            total: whiteBoxProducts.length,
        });
    }),

    // ========= получить конкретный товар ==========
    http.get("/api/products/:id", ({ params }) => {
        const product = whiteBoxProducts.find(p => p.id === Number(params.id));

        if (!product) {
            return HttpResponse.json({ error: "Product not found" }, { status: 404 });
        }

        return HttpResponse.json(product);
    }),

    // ========= рекомендации ==========
    http.get("/api/recommendations/:productId", ({ params }) => {
        const { productId } = params;

        // Простая логика моков: отдаём 12 случайных похожих товаров
        const shuffled = [...whiteBoxProducts].sort(() => 0.5 - Math.random());

        const recommendations = shuffled.slice(0, 12).map(p => ({
            id: p.id,
            name: p.name,
            price: p.price,
            image: p.image,
            score: +(Math.random() * (0.95 - 0.6) + 0.6).toFixed(2),
        }));

        return HttpResponse.json({
            productId,
            recommendations,
        });
    }),

    // ========= лайк / дизлайк ==========
    http.post("/api/feedback", async ({ request }) => {
        const body = await request.json();
        console.log("Получено MOCK-фидбэк:", body);

        return HttpResponse.json({ status: "ok" });
    }),
];
