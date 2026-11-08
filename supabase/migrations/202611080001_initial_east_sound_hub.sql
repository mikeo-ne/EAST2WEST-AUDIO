-- East Sound Hub: marketplace, licensing, and Mobile Money escrow.
-- Apply with: supabase db push
-- The only client-readable audio object should be a lossy preview. Keep WAVs and stems
-- in a private bucket and issue short-lived signed URLs only after a license check.

create extension if not exists pgcrypto;

create type public.user_role as enum ('producer', 'engineer', 'artist');
create type public.momo_network as enum ('mtn', 'airtel');
create type public.service_category as enum ('mixing', 'mastering', 'vocal_tuning');
create type public.escrow_status as enum ('pending', 'held', 'released', 'disputed');
create type public.license_tier as enum ('basic_lease', 'premium_lease', 'exclusive');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  msisdn_phone text unique check (msisdn_phone is null or msisdn_phone ~ '^\\+[1-9][0-9]{7,14}$'),
  full_name text not null check (char_length(trim(full_name)) between 2 and 120),
  stage_name text check (stage_name is null or char_length(trim(stage_name)) between 2 and 80),
  role public.user_role not null default 'artist',
  momo_number text check (momo_number is null or momo_number ~ '^\\+[1-9][0-9]{7,14}$'),
  momo_network public.momo_network,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint momo_details_are_paired check (
    (momo_number is null and momo_network is null) or
    (momo_number is not null and momo_network is not null)
  )
);

create table public.tracks (
  id uuid primary key default gen_random_uuid(),
  producer_id uuid not null references public.profiles(id) on delete restrict,
  title text not null check (char_length(trim(title)) between 1 and 160),
  bpm smallint not null check (bpm between 40 and 260),
  key text not null check (char_length(trim(key)) between 1 and 20),
  genre text not null check (genre in ('7 Hills Riddim', 'Amapiano', 'Afro-fusion', 'Lugaflow', 'Trap')),
  preview_url text not null,
  stems_url text not null,
  price_ugx_lease bigint not null check (price_ugx_lease >= 0),
  price_ugx_premium bigint check (price_ugx_premium is null or price_ugx_premium >= price_ugx_lease),
  price_ugx_exclusive bigint not null check (price_ugx_exclusive >= price_ugx_lease),
  price_usd_lease numeric(10,2) not null check (price_usd_lease >= 0),
  price_usd_premium numeric(10,2) check (price_usd_premium is null or price_usd_premium >= price_usd_lease),
  price_usd_exclusive numeric(10,2) not null check (price_usd_exclusive >= price_usd_lease),
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.service_listings (
  id uuid primary key default gen_random_uuid(),
  provider_id uuid not null references public.profiles(id) on delete restrict,
  title text not null check (char_length(trim(title)) between 1 and 140),
  description text not null check (char_length(trim(description)) between 20 and 5000),
  category public.service_category not null,
  price_ugx bigint not null check (price_ugx > 0),
  turnaround_days smallint not null check (turnaround_days between 1 and 90),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.escrow_orders (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references public.profiles(id) on delete restrict,
  provider_id uuid not null references public.profiles(id) on delete restrict,
  service_id uuid not null references public.service_listings(id) on delete restrict,
  amount_ugx bigint not null check (amount_ugx > 0),
  status public.escrow_status not null default 'pending',
  transaction_ref text not null unique check (char_length(transaction_ref) between 8 and 128),
  payout_transaction_ref text unique,
  platform_fee_ugx bigint not null default 0 check (platform_fee_ugx >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint distinct_escrow_parties check (client_id <> provider_id)
);

create table public.licenses (
  id uuid primary key default gen_random_uuid(),
  track_id uuid not null references public.tracks(id) on delete restrict,
  buyer_id uuid not null references public.profiles(id) on delete restrict,
  license_type public.license_tier not null,
  pdf_contract_url text,
  split_percentage_producer numeric(5,2) not null default 50 check (split_percentage_producer >= 0 and split_percentage_producer <= 100),
  split_percentage_artist numeric(5,2) not null default 50 check (split_percentage_artist >= 0 and split_percentage_artist <= 100),
  created_at timestamptz not null default now(),
  constraint split_percentages_total_100 check (split_percentage_producer + split_percentage_artist = 100)
);

-- Audit records are server-only and make provider retries harmless.
create table public.momo_webhook_events (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  provider_event_id text not null,
  event_type text not null,
  payload jsonb not null,
  received_at timestamptz not null default now(),
  unique (provider, provider_event_id)
);

create table public.escrow_order_events (
  id uuid primary key default gen_random_uuid(),
  escrow_order_id uuid not null references public.escrow_orders(id) on delete cascade,
  status public.escrow_status not null,
  event_type text not null,
  actor_id uuid references public.profiles(id) on delete set null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index tracks_discovery_idx on public.tracks (is_active, genre, bpm);
create index tracks_producer_idx on public.tracks (producer_id, created_at desc);
create index service_listings_provider_idx on public.service_listings (provider_id, category);
create index escrow_orders_client_idx on public.escrow_orders (client_id, status, created_at desc);
create index escrow_orders_provider_idx on public.escrow_orders (provider_id, status, created_at desc);
create index licenses_buyer_idx on public.licenses (buyer_id, created_at desc);
create unique index one_exclusive_license_per_track on public.licenses (track_id) where license_type = 'exclusive';

create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at before update on public.profiles for each row execute function public.set_updated_at();
create trigger tracks_set_updated_at before update on public.tracks for each row execute function public.set_updated_at();
create trigger service_listings_set_updated_at before update on public.service_listings for each row execute function public.set_updated_at();
create trigger escrow_orders_set_updated_at before update on public.escrow_orders for each row execute function public.set_updated_at();

-- All new accounts start as artists. Role upgrades should go through an admin-only server action.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, msisdn_phone, full_name, stage_name)
  values (
    new.id,
    nullif(new.phone, ''),
    coalesce(nullif(trim(new.raw_user_meta_data ->> 'full_name'), ''), 'New member'),
    nullif(trim(new.raw_user_meta_data ->> 'stage_name'), '')
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- A public, deliberately minimal producer card. Phone and MoMo details stay private.
create or replace view public.public_profiles
with (security_invoker = false) as
select id, coalesce(stage_name, full_name) as display_name, role
from public.profiles;

alter table public.profiles enable row level security;
alter table public.tracks enable row level security;
alter table public.service_listings enable row level security;
alter table public.escrow_orders enable row level security;
alter table public.licenses enable row level security;
alter table public.momo_webhook_events enable row level security;
alter table public.escrow_order_events enable row level security;

create policy "members can read their private profile" on public.profiles
  for select to authenticated using (id = auth.uid());
create policy "members can update their private profile" on public.profiles
  for update to authenticated using (id = auth.uid()) with check (id = auth.uid());

create policy "anyone can browse active tracks" on public.tracks
  for select using (is_active or producer_id = auth.uid());
create policy "producers create their own tracks" on public.tracks
  for insert to authenticated with check (producer_id = auth.uid());
create policy "producers update their own tracks" on public.tracks
  for update to authenticated using (producer_id = auth.uid()) with check (producer_id = auth.uid());
create policy "producers delete their own tracks" on public.tracks
  for delete to authenticated using (producer_id = auth.uid());

create policy "anyone can browse services" on public.service_listings
  for select using (true);
create policy "providers create their services" on public.service_listings
  for insert to authenticated with check (provider_id = auth.uid());
create policy "providers update their services" on public.service_listings
  for update to authenticated using (provider_id = auth.uid()) with check (provider_id = auth.uid());
create policy "providers delete their services" on public.service_listings
  for delete to authenticated using (provider_id = auth.uid());

create policy "parties can read an escrow order" on public.escrow_orders
  for select to authenticated using (client_id = auth.uid() or provider_id = auth.uid());
create policy "parties can read their order history" on public.escrow_order_events
  for select to authenticated using (
    exists (
      select 1 from public.escrow_orders o
      where o.id = escrow_order_id and (o.client_id = auth.uid() or o.provider_id = auth.uid())
    )
  );

create policy "buyers and track owners can read a license" on public.licenses
  for select to authenticated using (
    buyer_id = auth.uid() or exists (
      select 1 from public.tracks t where t.id = track_id and t.producer_id = auth.uid()
    )
  );

-- Only the server-side webhook handler may execute these financial transitions.
-- The insert into momo_webhook_events and the state transition are one transaction.
create or replace function public.hold_escrow_for_verified_payment(
  p_provider_event_id text,
  p_transaction_ref text,
  p_amount_ugx bigint,
  p_payload jsonb
)
returns uuid
language plpgsql
security definer set search_path = public
as $$
declare
  v_event_id uuid;
  v_order public.escrow_orders%rowtype;
begin
  insert into public.momo_webhook_events (provider, provider_event_id, event_type, payload)
  values ('flutterwave', p_provider_event_id, 'charge.completed', p_payload)
  on conflict (provider, provider_event_id) do nothing
  returning id into v_event_id;

  select * into v_order
  from public.escrow_orders
  where transaction_ref = p_transaction_ref
  for update;

  if not found then
    raise exception 'Unknown escrow payment reference';
  end if;

  -- A duplicate may arrive after a successful transaction; it has no further effect.
  if v_event_id is null then
    return v_order.id;
  end if;

  if v_order.amount_ugx <> p_amount_ugx then
    raise exception 'Payment amount does not match escrow order';
  end if;

  if v_order.status = 'pending' then
    update public.escrow_orders set status = 'held' where id = v_order.id;
    insert into public.escrow_order_events (escrow_order_id, status, event_type, metadata)
    values (v_order.id, 'held', 'payment.held', jsonb_build_object('provider_event_id', p_provider_event_id));
  elsif v_order.status not in ('held', 'released') then
    raise exception 'Escrow order cannot accept a payment in state %', v_order.status;
  end if;

  return v_order.id;
end;
$$;

-- Call this only after a verified provider transfer callback. The payout initiation server
-- action sets payout_transaction_ref and platform_fee_ugx = floor(amount_ugx * 0.12).
create or replace function public.release_escrow_after_verified_payout(
  p_provider_event_id text,
  p_payout_transaction_ref text,
  p_amount_ugx bigint,
  p_payload jsonb
)
returns uuid
language plpgsql
security definer set search_path = public
as $$
declare
  v_event_id uuid;
  v_order public.escrow_orders%rowtype;
begin
  insert into public.momo_webhook_events (provider, provider_event_id, event_type, payload)
  values ('flutterwave', p_provider_event_id, 'transfer.completed', p_payload)
  on conflict (provider, provider_event_id) do nothing
  returning id into v_event_id;

  select * into v_order
  from public.escrow_orders
  where payout_transaction_ref = p_payout_transaction_ref
  for update;

  if not found then
    raise exception 'Unknown escrow payout reference';
  end if;

  if v_event_id is null then
    return v_order.id;
  end if;

  if v_order.amount_ugx - v_order.platform_fee_ugx <> p_amount_ugx then
    raise exception 'Payout amount does not match escrow order';
  end if;

  if v_order.status = 'held' then
    update public.escrow_orders set status = 'released' where id = v_order.id;
    insert into public.escrow_order_events (escrow_order_id, status, event_type, metadata)
    values (v_order.id, 'released', 'payout.released', jsonb_build_object('provider_event_id', p_provider_event_id));
  elsif v_order.status <> 'released' then
    raise exception 'Escrow order cannot be released in state %', v_order.status;
  end if;

  return v_order.id;
end;
$$;

revoke all on function public.hold_escrow_for_verified_payment(text, text, bigint, jsonb) from public;
revoke all on function public.release_escrow_after_verified_payout(text, text, bigint, jsonb) from public;
grant execute on function public.hold_escrow_for_verified_payment(text, text, bigint, jsonb) to service_role;
grant execute on function public.release_escrow_after_verified_payout(text, text, bigint, jsonb) to service_role;
grant select on public.public_profiles to anon, authenticated;
