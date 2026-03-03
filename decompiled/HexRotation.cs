using System;

public struct HexRotation
{
	private readonly int Turns;

	public static readonly HexRotation R0 = new HexRotation(0);

	public static readonly HexRotation R60 = new HexRotation(1);

	public static readonly HexRotation R120 = new HexRotation(2);

	public static readonly HexRotation R180 = new HexRotation(3);

	public static readonly HexRotation R240 = new HexRotation(4);

	public static readonly HexRotation R300 = new HexRotation(5);

	public static readonly HexRotation Counterclockwise = new HexRotation(1);

	public static readonly HexRotation Clockwise = new HexRotation(-1);

	public bool IsZero => Turns % 6 == 0;

	public HexRotation(int turns)
	{
		Turns = turns;
	}

	public int GetNumberOfTurns()
	{
		return Turns;
	}

	public float ToRadians()
	{
		return (float)(Turns * 60) * ((float)Math.PI / 180f);
	}

	public HexRotation Opposite()
	{
		return new HexRotation((Turns + 3) % 6);
	}

	public HexRotation Negative()
	{
		return new HexRotation(-Turns);
	}

	public HexRotation RotatedCounterclockwise()
	{
		return new HexRotation(Turns + 1);
	}

	public HexRotation RotatedClockwise()
	{
		return new HexRotation(Turns - 1);
	}

	public static HexRotation operator +(HexRotation a, HexRotation b)
	{
		return new HexRotation(a.Turns + b.Turns);
	}

	public static HexRotation operator -(HexRotation a, HexRotation b)
	{
		return new HexRotation(a.Turns - b.Turns);
	}

	public HexRotation AsShortestAngle()
	{
		int i;
		for (i = Turns; i < -3; i += 6)
		{
		}
		while (i > 3)
		{
			i -= 6;
		}
		return new HexRotation(i);
	}

	public static HexRotation Rounded(float radians)
	{
		float num = radians * (180f / (float)Math.PI);
		for (num += 30f; num < 0f; num += 360f)
		{
		}
		num %= 360f;
		return new HexRotation((int)Math.Floor(num / 60f));
	}
}
