FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
WORKDIR /app

# ========================
# 1️⃣ DEPENDENCIES INSTALL
# ========================
FROM base AS deps
WORKDIR /app

# COPY ONLY WEB PACKAGE FILES
COPY apps/web/package.json apps/web/package-lock.json* ./apps/web/

RUN cd apps/web && \
    if [ -f package-lock.json ]; then npm ci; else npm install; fi


# ========================
# 2️⃣ BUILDER
# ========================
FROM base AS builder
WORKDIR /app

# Copy full repo for build
COPY . .

# Copy dependencies installed earlier
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules

ENV NEXT_TELEMETRY_DISABLED=1
RUN cd apps/web && npm run build


# ========================
# 3️⃣ RUNNER (PRODUCTION)
# ========================
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy standalone build
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static

# Copy public folder SAFELY (no error if missing)
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
