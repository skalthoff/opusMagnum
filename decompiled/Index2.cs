using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential, Pack = 4)]
[DebuggerDisplay("[{X}, {Y}]")]
public struct Index2 : IEquatable<Index2>, IComparable<Index2>
{
	public int X;

	public int Y;

	public static readonly Index2 Zero = new Index2(0, 0);

	public static readonly Index2 MinValue = new Index2(int.MinValue, int.MinValue);

	public static readonly Index2 MaxValue = new Index2(int.MaxValue, int.MaxValue);

	public static readonly Index2[] AdjacentOffsets = new Index2[4]
	{
		new Index2(1, 0),
		new Index2(0, 1),
		new Index2(-1, 0),
		new Index2(0, -1)
	};

	public Index2(int x, int y)
	{
		X = x;
		Y = y;
	}

	public override string ToString()
	{
		return string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850840473), X, Y);
	}

	public Vector2 ToVector2()
	{
		return new Vector2(X, Y);
	}

	public Vector3 ToVector3(float z)
	{
		return new Vector3(X, Y, z);
	}

	public bool IsNoLargerThan(Index2 other)
	{
		if (X <= other.X)
		{
			return Y <= other.Y;
		}
		return false;
	}

	public override bool Equals(object obj)
	{
		Index2? index = obj as Index2?;
		if (!index.HasValue)
		{
			return false;
		}
		Index2 value = this;
		Index2? index2 = index;
		return value == index2;
	}

	public override int GetHashCode()
	{
		return (391 + X.GetHashCode()) * 23 + Y.GetHashCode();
	}

	public static bool operator ==(Index2 a, Index2 b)
	{
		if (a.X == b.X)
		{
			return a.Y == b.Y;
		}
		return false;
	}

	public static bool operator !=(Index2 a, Index2 b)
	{
		if (a.X == b.X)
		{
			return a.Y != b.Y;
		}
		return true;
	}

	public static Index2 operator +(Index2 a, Index2 b)
	{
		return new Index2(a.X + b.X, a.Y + b.Y);
	}

	public static Index2 operator -(Index2 a, Index2 b)
	{
		return new Index2(a.X - b.X, a.Y - b.Y);
	}

	public static Index2 operator *(int s, Index2 a)
	{
		return new Index2(s * a.X, s * a.Y);
	}

	public static Index2 operator *(Index2 a, int s)
	{
		return new Index2(s * a.X, s * a.Y);
	}

	public static Index2 operator /(Index2 a, int s)
	{
		return new Index2(a.X / s, a.Y / s);
	}

	public static int ManhattanDistance(Index2 a, Index2 b)
	{
		return Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y);
	}

	public int ManhattanLength()
	{
		return Math.Abs(X) + Math.Abs(Y);
	}

	public bool Equals(Index2 other)
	{
		return this == other;
	}

	public int CompareTo(Index2 other)
	{
		if (Y < other.Y)
		{
			return -1;
		}
		if (Y > other.Y)
		{
			return 1;
		}
		if (X < other.X)
		{
			return -1;
		}
		if (X > other.X)
		{
			return 1;
		}
		return 0;
	}

	public static Index2 Min(Index2 a, Index2 b)
	{
		return new Index2(Math.Min(a.X, b.X), Math.Min(a.Y, b.Y));
	}

	public static Index2 Max(Index2 a, Index2 b)
	{
		return new Index2(Math.Max(a.X, b.X), Math.Max(a.Y, b.Y));
	}

	public Index2 Rotated(Rotation2 rotation)
	{
		return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003Dq1CtWmXBstAQSPGOsSYcVjA_003D_003D(rotation.GetNumberOfTurns(), 4) switch
		{
			0 => new Index2(X, Y), 
			1 => new Index2(-Y, X), 
			2 => new Index2(-X, -Y), 
			3 => new Index2(Y, -X), 
			_ => throw new ArgumentOutOfRangeException(), 
		};
	}

	public Index2 RotatedAround(Index2 pivot, Rotation2 rotation)
	{
		return (this - pivot).Rotated(rotation) + pivot;
	}
}
