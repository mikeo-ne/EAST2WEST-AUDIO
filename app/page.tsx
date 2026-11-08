"use client";

import { useAudioPlayer } from "@/components/AudioPlayer";

const demoBeat = {
  id: "kampala-after-dark",
  title: "Kampala After Dark",
  artist: "East Sound Demo",
  artworkUrl: "/artwork/kampala-after-dark.jpg",
  previewUrl: "/audio/kampala-after-dark-preview.mp3"
};

export default function HomePage() {
  const { playTrack } = useAudioPlayer();

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-5 pb-36 pt-20 sm:px-8">
      <p className="mb-4 text-sm font-semibold uppercase tracking-[0.28em] text-teal">Kampala · East Africa · Everywhere</p>
      <h1 className="max-w-4xl text-5xl font-black leading-[0.95] tracking-tight sm:text-7xl">
        Make the next sound <span className="text-gold">move.</span>
      </h1>
      <p className="mt-7 max-w-xl text-lg leading-8 text-slate-300">
        Beat licensing, protected studio collaboration, and Mobile Money escrow made for East African music.
      </p>
      <button
        className="mt-8 rounded-full bg-gold px-6 py-3 font-bold text-black transition hover:bg-amber-300 focus:outline-none focus:ring-2 focus:ring-teal"
        onClick={() => playTrack(demoBeat)}
      >
        Play protected preview
      </button>
    </main>
  );
}
