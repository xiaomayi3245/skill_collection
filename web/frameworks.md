# Framework Patterns and Traps

## React

- **State updates are async** — `setState(x)` doesn't immediately change state; use callback form for derived state
- **Keys must be stable** — Don't use array index as key if list reorders; causes bugs with forms/animations
- **useEffect dependencies** — Missing deps cause stale closures; ESLint exhaustive-deps catches these
- **useEffect cleanup** — Return cleanup function for subscriptions/timers; prevents memory leaks
- **Conditional hooks** — Hooks can't be in conditions/loops; breaks React's hook order tracking
- **Context rerenders** — Every consumer rerenders when context value changes; memoize or split contexts

## Vue 3 (Composition API)

- **`ref` vs `reactive`** — 基礎型別 (字串、數字) 必須用 `ref`（讀取需 `.value`）；物件或陣列可用 `reactive`，但解構 `reactive` 會遺失響應性（需用 `toRefs`）。
- **生命週期不可非同步呼叫** — `onMounted` 等生命週期 Hook 必須同步註冊在 `setup` 頂層，若放在 `setTimeout` 或 `await` 之後會導致註冊失敗。
- **Props 是單向資料流** — 不要在子元件直接修改 `props` 的值。請發送 `emit('update:modelValue', newValue)` 讓父元件更新，或使用 `v-model` 語法糖。
- **`watch` vs `watchEffect`** — `watch` 需要明確指定依賴來源並提供前後值比較；`watchEffect` 會自動追蹤其內部使用到的響應式變數，適合用在需要立即執行的副作用。
- **避免直接使用陣列索引作為 `:key`** — 與 React 相同，當陣列順序會變動時，使用 `index` 作為 `key` 會導致渲染與狀態對應錯亂。

## Nuxt 3

- **自動引入 (Auto-imports)** — `components/`、`composables/` 與 Vue 的 API (`ref`, `computed`) 都是自動引入的，不需要手動寫 `import`。
- **`useFetch` vs `$fetch`** — 在元件初始化抓取資料時使用 `useFetch` (避免 Hydration mismatch)；若是在點擊事件或方法中發送請求，請使用 `$fetch`。
- **伺服器端渲染 (SSR) 變數洩漏** — 全域狀態 (如 Pinia) 如果沒有正確封裝在 Request 範圍內，可能會導致不同使用者的資料在 SSR 階段互相污染（跨請求狀態污染）。
- **僅限客戶端執行的程式碼** — 凡是會存取 `window` 或 `document` 的套件，必須包在 `<ClientOnly>` 元件內，或是將其檔案命名為 `.client.vue` / `.client.js`。

## Next.js (App Router)

- **Server vs Client Components** — Default is server; add `"use client"` for hooks, browser APIs, events
- **`fetch` in Server Components** — Automatically deduped and cached; use `{cache: 'no-store'}` for fresh
- **Middleware runs on edge** — No Node APIs; limited to Web APIs and edge-compatible packages
- **Route handlers** — Export `GET`, `POST` functions from `route.ts`; not `page.tsx`
- **`revalidatePath`/`revalidateTag`** — Call after mutations to bust cache; ISR invalidation
- **Parallel routes** — Use `@folder` convention for loading multiple routes in same layout
- **`NEXT_PUBLIC_` prefix** — Required for env vars in client code; others are server-only

## General SPA

- **Hydration mismatch** — Server and client must render identically on first pass; use `useEffect` for client-only
- **Bundle size** — Tree-shaking needs ES modules; named imports from lodash don't tree-shake without lodash-es
- **Code splitting** — Use `lazy()` or `next/dynamic` for below-fold components; improves LCP
- **SSR data fetching** — Fetch on server to avoid waterfalls; don't fetch in useEffect for initial data