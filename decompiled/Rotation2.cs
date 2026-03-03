using System;

public struct Rotation2
{
	private readonly int Turns;

	public static readonly Rotation2 R0 = new Rotation2(0);

	public static readonly Rotation2 R90 = new Rotation2(1);

	public static readonly Rotation2 R180 = new Rotation2(2);

	public static readonly Rotation2 R270 = new Rotation2(3);

	public static readonly Rotation2 Counterclockwise = new Rotation2(1);

	public static readonly Rotation2 Clockwise = new Rotation2(-1);

	public bool IsZero => Turns % 4 == 0;

	public Rotation2(int turns)
	{
		Turns = turns;
	}

	public int GetNumberOfTurns()
	{
		return Turns;
	}

	public float ToRadians()
	{
		return (float)(Turns * 90) * ((float)Math.PI / 180f);
	}

	public Rotation2 Opposite()
	{
		return new Rotation2((Turns + 2) % 4);
	}

	public Rotation2 Negative()
	{
		return new Rotation2(-Turns);
	}

	public Rotation2 RotatedCounterclockwise()
	{
		return new Rotation2(Turns + 1);
	}

	public Rotation2 RotatedClockwise()
	{
		return new Rotation2(Turns - 1);
	}

	public static Rotation2 operator +(Rotation2 a, Rotation2 b)
	{
		return new Rotation2(a.Turns + b.Turns);
	}

	public static Rotation2 operator -(Rotation2 a, Rotation2 b)
	{
		return new Rotation2(a.Turns - b.Turns);
	}

	public Rotation2 AsShortestAngle()
	{
		int i;
		for (i = Turns; i < -2; i += 4)
		{
		}
		while (i > 2)
		{
			i -= 4;
		}
		return new Rotation2(i);
	}

	public static Rotation2 Rounded(float radians)
	{
		float num = radians * (180f / (float)Math.PI);
		for (num += 45f; num < 0f; num += 360f)
		{
		}
		num %= 360f;
		return new Rotation2((int)Math.Floor(num / 90f));
	}
}
