# Community Help Board — Starter (MERN)

## 1) Prereqs
- Node.js 18+
- MongoDB (local or Atlas)

## 2) Setup
```bash
# server
cd server
cp .env.example .env
npm install
npm run dev

# client
cd ../client
cp .env.example .env
npm install
npm run dev
```

Open client at http://localhost:5173. API at http://localhost:5000.

## 3) Workflow
1. Register → Login (copy token is automatic in client via localStorage).
2. Post a help request.
3. From another account, offer help.
4. Requester accepts offer → status becomes **in_progress**.
5. Requester sets status to **fulfilled** (via API for now: PATCH `/requests/:id/status`).
6. Requester posts rating to `/ratings/:volunteerId` with `{ requestId, score, comment }`.

## 4) Notes
- Media upload is URL-based placeholder. Integrate Cloudinary later.
- Notifications are in-app (list endpoint). Socket room `user:{userId}` can be joined from client if needed.
