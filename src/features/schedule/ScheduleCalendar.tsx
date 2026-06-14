import { useMemo } from 'react';
import type { Schedule } from './types';

interface Props {
  year: number;
  month: number;
  schedules: Schedule[];
  onSelectDay?: (date: string) => void;
}

function daysInMonth(year: number, month: number) {
  return new Date(year, month + 1, 0).getDate();
}

function firstDayOfMonth(year: number, month: number) {
  return new Date(year, month, 1).getDay();
}

function toDateKey(year: number, month: number, day: number) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

export default function ScheduleCalendar({ year, month, schedules, onSelectDay }: Props) {
  const scheduleMap = useMemo(() => {
    const map: Record<string, Schedule[]> = {};
    for (const s of schedules) {
      const key = s.scheduled_at.slice(0, 10);
      if (!map[key]) map[key] = [];
      map[key].push(s);
    }
    return map;
  }, [schedules]);

  const totalDays = daysInMonth(year, month);
  const startDow = firstDayOfMonth(year, month);

  const cells: (number | null)[] = [
    ...Array(startDow).fill(null),
    ...Array.from({ length: totalDays }, (_, i) => i + 1),
  ];

  const today = new Date();
  const todayKey = toDateKey(today.getFullYear(), today.getMonth(), today.getDate());

  const DOW = ['일', '월', '화', '수', '목', '금', '토'];

  return (
    <div className="calendar">
      <div className="calendar-grid calendar-grid--header">
        {DOW.map((d) => (
          <div key={d} className="calendar-dow">{d}</div>
        ))}
      </div>
      <div className="calendar-grid">
        {cells.map((day, idx) => {
          if (day === null) return <div key={`e-${idx}`} className="calendar-cell calendar-cell--empty" />;
          const key = toDateKey(year, month, day);
          const daySchedules = scheduleMap[key] ?? [];
          const isToday = key === todayKey;
          return (
            <div
              key={key}
              className={`calendar-cell${isToday ? ' calendar-cell--today' : ''}${onSelectDay ? ' calendar-cell--clickable' : ''}`}
              onClick={() => onSelectDay?.(key)}
            >
              <span className="calendar-day-num">{day}</span>
              <div className="calendar-events">
                {daySchedules.slice(0, 3).map((s) => (
                  <div key={s.id} className={`calendar-event${s.is_recurring ? ' calendar-event--recurring' : ''}`}>
                    {s.scheduled_at.slice(11, 16)} {s.title}
                  </div>
                ))}
                {daySchedules.length > 3 && (
                  <div className="calendar-event calendar-event--more">+{daySchedules.length - 3}개</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
