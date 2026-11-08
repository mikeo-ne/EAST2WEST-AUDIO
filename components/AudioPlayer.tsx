"use client";

import { Howl } from "howler";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";

export type PreviewTrack = {
  id: string;
  title: string;
  artist: string;
  previewUrl: string;
  artworkUrl?: string;
};

type PlayerContextValue = {
  currentTrack: PreviewTrack | null;
  isPlaying: boolean;
  volume: number;
  playTrack: (track: PreviewTrack) => void;
  toggle: () => void;
  seek: (fraction: number) => void;
  setVolume: (volume: number) => void;
};

const PlayerContext = createContext<PlayerContextValue | null>(null);

export function useAudioPlayer(): PlayerContextValue {
  const context = useContext(PlayerContext);
  if (!context) throw new Error("useAudioPlayer must be used inside AudioPlayerProvider.");
  return context;
}

function formatTime(value: number) {
  if (!Number.isFinite(value) || value < 0) return "0:00";
  const minutes = Math.floor(value / 60);
  const seconds = Math.floor(value % 60).toString().padStart(2, "0");
  return `${minutes}:${seconds}`;
}

/**
 * A root-layout provider, so its Howler instance survives client-side route changes.
 * `watermarkUrl` must point to a very short spoken "East Sound Exclusive" MP3 or OGG.
 * Watermarking deters casual ripping; storage/download authorization remains the protection
 * for full-resolution files.
 */
export function AudioPlayerProvider({
  children,
  watermarkUrl
}: {
  children: React.ReactNode;
  watermarkUrl: string;
}) {
  const soundRef = useRef<Howl | null>(null);
  const watermarkRef = useRef<Howl | null>(null);
  const trackIdRef = useRef<string | null>(null);
  const watermarkAtRef = useRef(35);
  const volumeRef = useRef(0.82);

  const [currentTrack, setCurrentTrack] = useState<PreviewTrack | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [volume, setVolumeState] = useState(volumeRef.current);

  useEffect(() => {
    const watermark = new Howl({
      src: [watermarkUrl],
      html5: true,
      preload: false,
      volume: volumeRef.current * 0.9
    });
    watermarkRef.current = watermark;

    return () => {
      watermark.unload();
      watermarkRef.current = null;
    };
  }, [watermarkUrl]);

  useEffect(() => {
    return () => {
      soundRef.current?.unload();
      soundRef.current = null;
    };
  }, []);

  const setVolume = useCallback((nextVolume: number) => {
    const bounded = Math.max(0, Math.min(1, nextVolume));
    volumeRef.current = bounded;
    setVolumeState(bounded);
    soundRef.current?.volume(bounded);
    watermarkRef.current?.volume(bounded * 0.9);
  }, []);

  const playTrack = useCallback((track: PreviewTrack) => {
    const existing = soundRef.current;
    if (trackIdRef.current === track.id && existing) {
      if (!existing.playing()) existing.play();
      return;
    }

    existing?.stop();
    existing?.unload();

    const sound = new Howl({
      src: [track.previewUrl],
      html5: true,
      preload: "metadata",
      volume: volumeRef.current,
      onload: () => setDuration(sound.duration()),
      onplay: () => setIsPlaying(true),
      onpause: () => setIsPlaying(false),
      onstop: () => setIsPlaying(false),
      onend: () => {
        setIsPlaying(false);
        setElapsed(0);
      },
      onloaderror: (_id, error) => {
        console.error("Preview audio could not be loaded", error);
        setIsPlaying(false);
      },
      onplayerror: (_id, error) => {
        console.error("Preview audio could not be played", error);
        setIsPlaying(false);
      }
    });

    soundRef.current = sound;
    trackIdRef.current = track.id;
    watermarkAtRef.current = 32 + Math.floor(Math.random() * 14);
    setCurrentTrack(track);
    setElapsed(0);
    setDuration(0);
    sound.play();
  }, []);

  const toggle = useCallback(() => {
    const sound = soundRef.current;
    if (!sound) return;
    if (sound.playing()) sound.pause();
    else sound.play();
  }, []);

  const seek = useCallback((fraction: number) => {
    const sound = soundRef.current;
    const safeFraction = Math.max(0, Math.min(1, fraction));
    if (!sound || !duration) return;
    const position = safeFraction * duration;
    sound.seek(position);
    setElapsed(position);
  }, [duration]);

  // Polling is intentionally light: mobile devices only update this while audio is playing.
  useEffect(() => {
    if (!isPlaying) return;
    const timer = window.setInterval(() => {
      const sound = soundRef.current;
      if (!sound || !sound.playing()) return;
      const position = Number(sound.seek()) || 0;
      setElapsed(position);

      if (position >= watermarkAtRef.current) {
        const watermark = watermarkRef.current;
        if (watermark && !watermark.playing()) watermark.play();
        watermarkAtRef.current = position + 34 + Math.floor(Math.random() * 22);
      }
    }, 300);

    return () => window.clearInterval(timer);
  }, [isPlaying]);

  const contextValue = useMemo<PlayerContextValue>(() => ({
    currentTrack,
    isPlaying,
    volume,
    playTrack,
    toggle,
    seek,
    setVolume
  }), [currentTrack, isPlaying, volume, playTrack, toggle, seek, setVolume]);

  const progress = duration ? Math.min(1, elapsed / duration) : 0;

  return (
    <PlayerContext.Provider value={contextValue}>
      {children}
      <aside className="fixed inset-x-0 bottom-0 z-50 border-t border-white/10 bg-[#11161c]/95 px-3 py-3 shadow-2xl backdrop-blur md:px-6">
        <div className="mx-auto grid max-w-7xl grid-cols-[auto_1fr_auto] items-center gap-3 md:grid-cols-[minmax(210px,1fr)_minmax(230px,2fr)_minmax(160px,1fr)]">
          <div className="flex min-w-0 items-center gap-3">
            <button
              aria-label={isPlaying ? "Pause preview" : "Play preview"}
              className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-gold text-lg font-bold text-black transition hover:bg-amber-300 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
              disabled={!currentTrack}
              onClick={toggle}
            >
              {isPlaying ? "Ⅱ" : "▶"}
            </button>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-white">{currentTrack?.title ?? "Select a protected preview"}</p>
              <p className="truncate text-xs text-slate-400">{currentTrack?.artist ?? "East Sound Hub"}</p>
            </div>
          </div>

          <div className="hidden min-w-0 md:block">
            <div className="mb-1 flex h-6 items-end gap-[3px]" aria-hidden="true">
              {Array.from({ length: 34 }, (_, index) => {
                const barProgress = (index + 1) / 34;
                const height = 20 + ((index * 37) % 70);
                return (
                  <span
                    className={barProgress <= progress ? "bg-teal" : "bg-slate-700"}
                    key={index}
                    style={{ height: `${height}%`, width: "100%", borderRadius: 99 }}
                  />
                );
              })}
            </div>
            <input
              aria-label="Preview position"
              className="h-1 w-full cursor-pointer accent-gold"
              disabled={!currentTrack || !duration}
              max="1"
              min="0"
              onChange={(event) => seek(Number(event.target.value))}
              step="0.001"
              type="range"
              value={progress}
            />
            <div className="mt-1 flex justify-between text-[10px] tabular-nums text-slate-500">
              <span>{formatTime(elapsed)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>

          <label className="flex items-center justify-end gap-2 text-xs text-slate-400">
            <span className="hidden sm:inline">Volume</span>
            <input
              aria-label="Volume"
              className="w-16 accent-teal sm:w-24"
              max="1"
              min="0"
              onChange={(event) => setVolume(Number(event.target.value))}
              step="0.01"
              type="range"
              value={volume}
            />
          </label>
        </div>
      </aside>
    </PlayerContext.Provider>
  );
}
