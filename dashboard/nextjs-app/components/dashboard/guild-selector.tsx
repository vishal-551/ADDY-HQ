"use client";

import { useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { GuildSummary } from "@/lib/api";

export function GuildSelector({ guilds, selectedGuildId }: { guilds: GuildSummary[]; selectedGuildId?: number }) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const value = useMemo(() => {
    if (selectedGuildId) {
      return String(selectedGuildId);
    }
    return guilds.length ? String(guilds[0].id) : "";
  }, [guilds, selectedGuildId]);

  return (
    <select
      className="input guild-select"
      value={value}
      onChange={(event) => {
        const next = new URLSearchParams(searchParams.toString());
        next.set("guild", event.target.value);
        router.push(`${pathname}?${next.toString()}`);
      }}
    >
      {guilds.map((guild) => (
        <option key={guild.id} value={guild.id}>
          {guild.name}
        </option>
      ))}
    </select>
  );
}
