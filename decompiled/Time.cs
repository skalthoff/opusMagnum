using SDL2;

public struct Time
{
	public readonly ulong Ticks;

	public static readonly Time MinValue = new Time(0uL);

	public Time(ulong ticks)
	{
		Ticks = ticks;
	}

	public static Time Now()
	{
		return new Time(SDL.SDL_GetPerformanceCounter());
	}

	public static float NowInSeconds()
	{
		return (float)SDL.SDL_GetPerformanceCounter() / (float)SDL.SDL_GetPerformanceFrequency();
	}

	public static Time operator +(Time time, _0023_003DqeCtUSavZEi2zYuJ88A68jQ_003D_003D delta)
	{
		return new Time(time.Ticks + delta._0023_003Dq1nzB10CipsAEuOPOSx1crA_003D_003D);
	}

	public static Time operator -(Time time, _0023_003DqeCtUSavZEi2zYuJ88A68jQ_003D_003D delta)
	{
		return new Time(time.Ticks - delta._0023_003Dq1nzB10CipsAEuOPOSx1crA_003D_003D);
	}

	public static _0023_003DqeCtUSavZEi2zYuJ88A68jQ_003D_003D operator -(Time a, Time b)
	{
		return new _0023_003DqeCtUSavZEi2zYuJ88A68jQ_003D_003D(a.Ticks - b.Ticks);
	}

	public static bool operator <(Time a, Time b)
	{
		return a.Ticks < b.Ticks;
	}

	public static bool operator >(Time a, Time b)
	{
		return a.Ticks > b.Ticks;
	}
}
