using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential, Pack = 4)]
public struct Vector2
{
	public float X;

	public float Y;

	public static Vector2 Zero = new Vector2(0f, 0f);

	public bool IsZero
	{
		get
		{
			if (X == 0f)
			{
				return Y == 0f;
			}
			return false;
		}
	}

	public Vector2(float x, float y)
	{
		X = x;
		Y = y;
	}

	public override string ToString()
	{
		return string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850840473), X, Y);
	}

	public Vector3 ToVector3(float z)
	{
		return new Vector3(X, Y, z);
	}

	public float Length()
	{
		return (float)Math.Sqrt(X * X + Y * Y);
	}

	public float LengthSquared()
	{
		return X * X + Y * Y;
	}

	public Vector2 ScaledToLength(float newLength)
	{
		float num = Length();
		return newLength / num * this;
	}

	public Vector2 ClampedToLength(float limit)
	{
		Vector2 result = this;
		if (Length() > limit)
		{
			result = ScaledToLength(limit);
		}
		return result;
	}

	public Vector2 Rounded()
	{
		return new Vector2((float)Math.Round(X), (float)Math.Round(Y));
	}

	public Vector2 Rotated(float radians)
	{
		float num = (float)Math.Sin(radians);
		float num2 = (float)Math.Cos(radians);
		return new Vector2(X * num2 - Y * num, X * num + Y * num2);
	}

	public Vector2 Normalized()
	{
		float num = Length();
		if (num == 0f)
		{
			return Zero;
		}
		return this / num;
	}

	public static float Distance(Vector2 a, Vector2 b)
	{
		return (a - b).Length();
	}

	public static float DistanceSquared(Vector2 a, Vector2 b)
	{
		return (a - b).LengthSquared();
	}

	public static float Dot(Vector2 a, Vector2 b)
	{
		return a.X * b.X + a.Y * b.Y;
	}

	public Vector2 Floored()
	{
		return new Vector2((float)Math.Floor(X), (float)Math.Floor(Y));
	}

	public Index2 FlooredToInt()
	{
		return new Index2((int)Math.Floor(X), (int)Math.Floor(Y));
	}

	public Index2 CeilingToInt()
	{
		return new Index2((int)Math.Ceiling(X), (int)Math.Ceiling(Y));
	}

	public float Angle()
	{
		return (float)Math.Atan2(Y, X);
	}

	public static Vector2 operator -(Vector2 a)
	{
		return new Vector2(0f - a.X, 0f - a.Y);
	}

	public static Vector2 operator +(Vector2 a, Vector2 b)
	{
		return new Vector2(a.X + b.X, a.Y + b.Y);
	}

	public static Vector2 operator -(Vector2 a, Vector2 b)
	{
		return new Vector2(a.X - b.X, a.Y - b.Y);
	}

	public static Vector2 operator *(float s, Vector2 v)
	{
		return new Vector2(s * v.X, s * v.Y);
	}

	public static Vector2 operator *(Vector2 v, float s)
	{
		return new Vector2(s * v.X, s * v.Y);
	}

	public static Vector2 operator *(int s, Vector2 v)
	{
		return new Vector2((float)s * v.X, (float)s * v.Y);
	}

	public static Vector2 operator *(Vector2 v, int s)
	{
		return new Vector2((float)s * v.X, (float)s * v.Y);
	}

	public static Vector2 operator /(Vector2 v, float s)
	{
		return new Vector2(v.X / s, v.Y / s);
	}

	public static Vector2 operator /(Vector2 v, int s)
	{
		return new Vector2(v.X / (float)s, v.Y / (float)s);
	}

	public static Vector2 operator *(Vector2 a, Vector2 b)
	{
		return new Vector2(a.X * b.X, a.Y * b.Y);
	}

	public static Vector2 operator /(Vector2 a, Vector2 b)
	{
		return new Vector2(a.X / b.X, a.Y / b.Y);
	}
}
