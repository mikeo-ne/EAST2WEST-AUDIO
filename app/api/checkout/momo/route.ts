import { timingSafeEqual } from "node:crypto";
import { NextResponse } from "next/server";
import { createSupabaseAdmin } from "@/lib/supabase/admin";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type FlutterwaveData = {
  id?: string | number;
  tx_ref?: string;
  reference?: string;
  amount?: string | number;
  currency?: string;
  status?: string;
};

type FlutterwaveEvent = {
  event?: string;
  data?: FlutterwaveData;
};

function matchesWebhookHash(received: string | null, expected: string | undefined) {
  if (!received || !expected) return false;
  const receivedBuffer = Buffer.from(received);
  const expectedBuffer = Buffer.from(expected);
  return receivedBuffer.length === expectedBuffer.length && timingSafeEqual(receivedBuffer, expectedBuffer);
}

function asUgandanShillings(value: unknown) {
  const parsed = typeof value === "number" ? value : Number(value);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) throw new Error("Provider returned an invalid UGX amount.");
  return parsed;
}

function isSuccessful(status: unknown) {
  return String(status).toLowerCase() === "successful";
}

/**
 * A webhook is a notification, not proof of payment. Re-query the provider before
 * recording an escrow transition, because a client can forge a payload shape.
 */
async function verifyFlutterwaveResource(path: string): Promise<FlutterwaveData> {
  const secretKey = process.env.FLUTTERWAVE_SECRET_KEY;
  if (!secretKey) throw new Error("FLUTTERWAVE_SECRET_KEY is not configured.");

  const response = await fetch(`https://api.flutterwave.com/v3/${path}`, {
    headers: { Authorization: `Bearer ${secretKey}` },
    cache: "no-store"
  });

  if (!response.ok) throw new Error(`Flutterwave verification failed (${response.status}).`);

  const body = (await response.json()) as { status?: string; data?: FlutterwaveData };
  if (body.status !== "success" || !body.data) throw new Error("Flutterwave did not return a verified record.");
  return body.data;
}

export async function POST(request: Request) {
  // Flutterwave sends its dashboard-configured secret in `verif-hash`.
  if (!matchesWebhookHash(request.headers.get("verif-hash"), process.env.FLUTTERWAVE_WEBHOOK_HASH)) {
    return NextResponse.json({ error: "Invalid webhook signature." }, { status: 401 });
  }

  let event: FlutterwaveEvent;
  try {
    event = JSON.parse(await request.text()) as FlutterwaveEvent;
  } catch {
    return NextResponse.json({ error: "Invalid JSON payload." }, { status: 400 });
  }

  const data = event.data;
  const providerId = data?.id == null ? null : String(data.id);
  if (!event.event || !data || !providerId) {
    return NextResponse.json({ error: "Malformed Flutterwave event." }, { status: 400 });
  }

  try {
    const supabase = createSupabaseAdmin();

    if (event.event === "charge.completed") {
      const verified = await verifyFlutterwaveResource(`transactions/${encodeURIComponent(providerId)}/verify`);
      const paymentReference = verified.tx_ref;

      if (!isSuccessful(verified.status) || verified.currency !== "UGX" || !paymentReference) {
        // A failed/cancelled prompt must never mutate an escrow order.
        return NextResponse.json({ received: true, processed: false });
      }

      const { error } = await supabase.rpc("hold_escrow_for_verified_payment", {
        p_provider_event_id: `charge:${providerId}`,
        p_transaction_ref: paymentReference,
        p_amount_ugx: asUgandanShillings(verified.amount),
        p_payload: event
      });
      if (error) throw new Error(`Could not hold escrow: ${error.message}`);

      return NextResponse.json({ received: true, processed: true });
    }

    if (event.event === "transfer.completed") {
      // Release occurs only after the provider confirms the 88% MoMo payout succeeded.
      const verified = await verifyFlutterwaveResource(`transfers/${encodeURIComponent(providerId)}`);
      const payoutReference = verified.reference ?? verified.tx_ref;

      if (!isSuccessful(verified.status) || verified.currency !== "UGX" || !payoutReference) {
        return NextResponse.json({ received: true, processed: false });
      }

      const { error } = await supabase.rpc("release_escrow_after_verified_payout", {
        p_provider_event_id: `transfer:${providerId}`,
        p_payout_transaction_ref: payoutReference,
        p_amount_ugx: asUgandanShillings(verified.amount),
        p_payload: event
      });
      if (error) throw new Error(`Could not release escrow: ${error.message}`);

      return NextResponse.json({ received: true, processed: true });
    }

    // Acknowledge unrelated, correctly signed events so Flutterwave does not retry them.
    return NextResponse.json({ received: true, processed: false });
  } catch (error) {
    // A non-2xx response lets Flutterwave retry a transient database/provider failure.
    console.error("Mobile Money webhook processing failed", {
      event: event.event,
      providerId,
      message: error instanceof Error ? error.message : "Unknown error"
    });
    return NextResponse.json({ error: "Webhook processing failed." }, { status: 500 });
  }
}
