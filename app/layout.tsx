import type { Metadata } from "next";
import "./globals.css";
import { AudioPlayerProvider } from "@/components/AudioPlayer";

export const metadata: Metadata = {
  title: "East Sound Hub",
  description: "East Africa's studio collaboration and beat marketplace."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        {/* Mounting here keeps one Howler instance alive across App Router navigation. */}
        <AudioPlayerProvider watermarkUrl="/audio/east-sound-exclusive.mp3">
          {children}
        </AudioPlayerProvider>
      </body>
    </html>
  );
}
