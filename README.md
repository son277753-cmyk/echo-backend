# Echo / PCOS Backend — Deploy Guide

This folder is your real EchoCore engine (all 11 layers, unmodified except
two harmless duplicate lines removed in `echo_core.py`) plus one new file:
**`app.py`** — the web entrypoint. It:

- Runs Sentinel's passive scan + the Asimov gate on every request, exactly
  like `EchoCore.process()` already did.
- Detects **every** layer that applies to a request, not just the top one
  (this is the "new entity" — e.g. "create an educational website" now
  correctly activates both CREATOR and SCHOLAR together).
- Runs each activated layer for real and treats their combined structured
  output as the deliberation input.
- Sends that to a free model to write the actual final answer, grounded in
  what the layers decided.
- Caches the result by (layers + question), so a repeat/similar ask skips
  straight to the cached answer — this is "Echo gets faster the more Orho
  is used."

I tested all of this locally before handing it to you — combination
detection, caching, and the safety gates all confirmed working.

## 1. Get the code onto GitHub (no Termux needed for this part)
1. Go to github.com → **New repository** → name it something like `echo-backend` → Create.
2. On the empty repo page, click **uploading an existing file**.
3. Drag in every file from this folder (all the `.py` files, `requirements.txt`, this README).
4. Commit.

(If you'd rather do this from Termux with real `git` commands for the practice, that works too — ask me and I'll walk you through it.)

## 2. Deploy on Render
1. Go to render.com → sign up (no card needed) → **New** → **Web Service**.
2. Connect the GitHub repo you just made.
3. Settings:
   - **Language**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
4. Under **Environment Variables**, add:
   - `OPENROUTER_API_KEY` = your key from openrouter.ai
5. Click **Create Web Service**. First build takes a couple minutes.
6. You'll get a URL like `https://echo-backend-xxxx.onrender.com`.

Send me that URL and I'll point the frontend at it and redeploy.

## Reminder on the free tier
Render's free web services sleep after 15 minutes of no traffic — the
first request after that takes 30-60 seconds to wake up, then it's normal
speed. Fine for people testing a prototype, just don't be surprised by one
slow first message.

## Endpoints
- `POST /api/echo` — body: `{"message": "..."}` → returns `{"reply", "layers", "cached"}`
- `GET /api/status` — quick health check, shows cache size and whether the LLM key is configured
