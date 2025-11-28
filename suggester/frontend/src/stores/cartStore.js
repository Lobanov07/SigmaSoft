import { create } from "zustand"


export const useCartStore = create((set) => ({
    items: [],
    add: (product) => set(state => ({ items: [...state.items, product] })),
    remove: (id) => set(state => ({ items: state.items.filter(i => i.id !== id) })),
    clear: () => set({ items: [] })
}))