using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential, Pack = 4)]
public struct Vector3
{
	public float X;

	public float Y;

	public float Z;

	public static Vector3 Zero = new Vector3(0f, 0f, 0f);

	public Vector2 XY => new Vector2(X, Y);

	public Vector3(float x, float y, float z)
	{
		X = x;
		Y = y;
		Z = z;
	}

	public override string ToString()
	{
		return string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680329), X, Y, Z);
	}

	public float Length()
	{
		return (float)Math.Sqrt(X * X + Y * Y + Z * Z);
	}

	public float LengthSquared()
	{
		return X * X + Y * Y + Z * Z;
	}

	public Vector3 ScaledToLength(float newLength)
	{
		float num = Length();
		return newLength / num * this;
	}

	public Vector3 ClampedToLength(float limit)
	{
		Vector3 result = this;
		if (Length() > limit)
		{
			result = ScaledToLength(limit);
		}
		return result;
	}

	public Vector3 Rounded()
	{
		return new Vector3((float)Math.Round(X), (float)Math.Round(Y), (float)Math.Round(Z));
	}

	public Vector3 RotatedZ(float radians)
	{
		float num = (float)Math.Sin(radians);
		float num2 = (float)Math.Cos(radians);
		return new Vector3(X * num2 - Y * num, X * num + Y * num2, Z);
	}

	public static float Distance(Vector3 a, Vector3 b)
	{
		return (a - b).Length();
	}

	public static float Dot(Vector3 a, Vector3 b)
	{
		return a.X * b.X + a.Y * b.Y;
	}

	public static Vector3 Cross(Vector3 a, Vector3 b)
	{
		return new Vector3(a.Y * b.Z - a.Z * b.Y, a.Z * b.X - a.X * b.Z, a.X * b.Y - a.Y * b.X);
	}

	public static Vector3 operator -(Vector3 a)
	{
		return new Vector3(0f - a.X, 0f - a.Y, 0f - a.Z);
	}

	public static Vector3 operator +(Vector3 a, Vector3 b)
	{
		return new Vector3(a.X + b.X, a.Y + b.Y, a.Z + b.Z);
	}

	public static Vector3 operator -(Vector3 a, Vector3 b)
	{
		return new Vector3(a.X - b.X, a.Y - b.Y, a.Z - b.Z);
	}

	public static Vector3 operator *(float s, Vector3 v)
	{
		return new Vector3(s * v.X, s * v.Y, s * v.Z);
	}

	public static Vector3 operator *(Vector3 v, float s)
	{
		return new Vector3(s * v.X, s * v.Y, s * v.Z);
	}
}
