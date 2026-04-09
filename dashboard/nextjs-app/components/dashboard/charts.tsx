export function AreaChart({ points, color }: { points: number[]; color: string }) {
  const width = 420;
  const height = 160;
  const max = Math.max(...points, 1);
  const step = width / Math.max(points.length - 1, 1);
  const path = points
    .map((point, index) => `${index === 0 ? "M" : "L"}${index * step},${height - (point / max) * (height - 20)}`)
    .join(" ");

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="chart" role="img" aria-label="area chart">
      <path d={`${path} L ${width},${height} L 0,${height} Z`} fill={`${color}22`} />
      <path d={path} fill="none" stroke={color} strokeWidth="3" />
    </svg>
  );
}

export function ActivityBars({ points }: { points: number[] }) {
  const max = Math.max(...points, 1);
  return (
    <div className="bars">
      {points.map((point, index) => (
        <div
          key={`bar-${index}`}
          className="bar"
          style={{ height: `${Math.max(18, Math.round((point / max) * 100))}%` }}
          title={`${point}`}
        />
      ))}
    </div>
  );
}
