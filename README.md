# East Sound Hub

Dark-mode, mobile-first Next.js foundation for an East African beat marketplace, studio service directory, and Mobile Money escrow flow.

## App Router layout

```text
app/
  api/checkout/momo/route.ts     # signed Flutterwave payment + transfer callbacks
  globals.css                    # charcoal / gold / teal design tokens
  layout.tsx                     # persistent player mount point
  page.tsx                       # landing route example
components/
  AudioPlayer.tsx                # Howler provider, global player bar, watermark scheduler
lib/
  supabase/admin.ts              # server-only Supabase service client
supabase/migrations/
  202611080001_initial_east_sound_hub.sql
                                 # schema, RLS, idempotent financial RPCs
```

The intended expansion is to add route groups without remounting `app/layout.tsx`:

```text
app/
  (marketing)/beats/page.tsx
  (marketing)/services/page.tsx
  (auth)/sign-in/page.tsx
  (dashboard)/producer/page.tsx
  (dashboard)/artist/licenses/page.tsx
  (dashboard)/vault/page.tsx
  api/contracts/[licenseId]/route.ts
  api/checkout/momo/route.ts
```

## Important setup

1. Copy `.env.example` to `.env.local` and fill it with production secrets. Keep the service-role and Flutterwave secret keys server-only.
2. Run `supabase db push` to apply the migration.
3. Configure Flutterwave to send webhooks to `/api/checkout/momo`, set the same `FLUTTERWAVE_WEBHOOK_HASH` in both places, and subscribe to `charge.completed` and `transfer.completed`.
4. Add a short spoken `public/audio/east-sound-exclusive.mp3` watermark. Preview tracks should be lossy public files; protect WAV/stems in a private Storage bucket and issue signed URLs after the license lookup.
5. The artist-approval action must calculate `floor(amount_ugx * 0.12)`, create the provider transfer for the balance, then store its reference in `payout_transaction_ref`. The supplied transfer webhook performs the final `held → released` transition only after provider verification.

## Security model

- RLS exposes active beats and service listings, while profiles expose only a minimal public view. Private phone and MoMo fields are readable only by their owner.
- Checkout callbacks verify the `verif-hash`, re-query Flutterwave's API, and use database-level idempotency records plus row locking. A webhook alone can never credit funds.
- License creation, payment-order creation, split-sheet PDF generation, escrow dispute handling, and private asset signing belong in server actions/routes using the authenticated user or service role—not direct browser writes.

Audio watermarking adds friction for casual copying, but cannot secure an audio stream against a determined recorder. Licensing/RLS/private storage are the access controls.
