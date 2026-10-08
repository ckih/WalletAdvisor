## 2025-02-14 - Optimize Sequential API Calls in Dashboard
**Learning:** Found a network waterfall in `frontend/src/app/dashboard/page.tsx` where `/goals/` and `/risk/profile` were being fetched sequentially instead of concurrently.
**Action:** Always batch independent data fetching using `Promise.all` in React components to optimize load times and prevent network waterfalls.
