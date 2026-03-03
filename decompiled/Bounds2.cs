using System;
using System.Diagnostics;

[DebuggerDisplay("[Bounds2: X={Min.X}, Y={Min.Y}, W={Width}, H={Height}]")]
public struct Bounds2
{
	public Vector2 Min;

	public Vector2 Max;

	public static readonly Bounds2 Empty = WithCorners(Vector2.Zero, Vector2.Zero);

	public static readonly Bounds2 Undefined = WithCorners(float.PositiveInfinity, float.PositiveInfinity, float.NegativeInfinity, float.NegativeInfinity);

	public Vector2 Size => Max - Min;

	public float Width => Max.X - Min.X;

	public float Height => Max.Y - Min.Y;

	public Vector2 Center => Min + 0.5f * (Max - Min);

	public Vector2 BottomLeft => Min;

	public Vector2 BottomRight => new Vector2(Max.X, Min.Y);

	public Vector2 TopLeft => new Vector2(Min.X, Max.Y);

	public Vector2 TopRight => Max;

	public bool IsEmpty
	{
		get
		{
			if (Min.X != Max.X)
			{
				return Min.Y == Max.Y;
			}
			return true;
		}
	}

	public static Bounds2 WithCorners(Vector2 a, Vector2 b)
	{
		return new Bounds2
		{
			Min = new Vector2(Math.Min(a.X, b.X), Math.Min(a.Y, b.Y)),
			Max = new Vector2(Math.Max(a.X, b.X), Math.Max(a.Y, b.Y))
		};
	}

	public static Bounds2 WithCorners(float minX, float minY, float maxX, float maxY)
	{
		return new Bounds2
		{
			Min = new Vector2(minX, minY),
			Max = new Vector2(maxX, maxY)
		};
	}

	public static Bounds2 WithSize(float x, float y, float width, float height)
	{
		return new Bounds2
		{
			Min = new Vector2(x, y),
			Max = new Vector2(x + width, y + height)
		};
	}

	public static Bounds2 WithSize(Vector2 position, Vector2 size)
	{
		return WithSize(position.X, position.Y, size.X, size.Y);
	}

	public static Bounds2 CenteredOn(Vector2 point, float width, float height)
	{
		return WithSize(point.X - width / 2f, point.Y - height / 2f, width, height);
	}

	public Bounds2 Expanded(Vector2 amount)
	{
		return new Bounds2
		{
			Min = Min - amount,
			Max = Max + amount
		};
	}

	public Bounds2 Expanded(float dx, float dy)
	{
		return Expanded(new Vector2(dx, dy));
	}

	public Bounds2 Expanded(float left, float right, float bottom, float top)
	{
		return new Bounds2
		{
			Min = new Vector2(Min.X - left, Min.Y - bottom),
			Max = new Vector2(Max.X + right, Max.Y + top)
		};
	}

	public Bounds2 UnionedWith(Vector2 point)
	{
		return new Bounds2
		{
			Min = new Vector2(Math.Min(Min.X, point.X), Math.Min(Min.Y, point.Y)),
			Max = new Vector2(Math.Max(Max.X, point.X), Math.Max(Max.Y, point.Y))
		};
	}

	public Bounds2 UnionedWith(float x, float y)
	{
		return UnionedWith(new Vector2(x, y));
	}

	public Bounds2 UnionedWith(Vector2 position, Vector2 size)
	{
		return UnionedWith(position).UnionedWith(position + size);
	}

	public Bounds2 UnionedWith(Bounds2 bounds)
	{
		return UnionedWith(bounds.Min).UnionedWith(bounds.Max);
	}

	public Bounds2 IntersectedWith(Bounds2 other)
	{
		float num = Math.Max(Min.X, other.Min.X);
		float num2 = Math.Max(Min.Y, other.Min.Y);
		float num3 = Math.Min(Max.X, other.Max.X);
		float num4 = Math.Min(Max.Y, other.Max.Y);
		if (num >= num3 || num2 >= num4)
		{
			return Empty;
		}
		return new Bounds2
		{
			Min = new Vector2(num, num2),
			Max = new Vector2(num3, num4)
		};
	}

	public bool Contains(Vector2 point)
	{
		if (Min.X <= point.X && point.X <= Max.X && Min.Y <= point.Y)
		{
			return point.Y <= Max.Y;
		}
		return false;
	}

	public bool Overlaps(Bounds2 bounds)
	{
		if (!(bounds.Max.X < Min.X) && !(bounds.Min.X > Max.X) && !(bounds.Max.Y < Min.Y))
		{
			return !(bounds.Min.Y > Max.Y);
		}
		return false;
	}

	public Bounds2 Translated(Vector2 offset)
	{
		return new Bounds2
		{
			Min = Min + offset,
			Max = Max + offset
		};
	}

	public Vector2 GetEdgePosition(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D edge)
	{
		return edge switch
		{
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)0 => new Vector2(Min.X, Max.Y), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)1 => new Vector2((Min.X + Max.X) / 2f, Max.Y), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)2 => new Vector2(Max.X, Max.Y), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)3 => new Vector2(Min.X, (Min.Y + Max.Y) / 2f), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)4 => new Vector2((Min.X + Max.X) / 2f, (Min.Y + Max.Y) / 2f), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)5 => new Vector2(Max.X, (Min.Y + Max.Y) / 2f), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)6 => new Vector2(Min.X, Min.Y), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)7 => new Vector2((Min.X + Max.X) / 2f, Min.Y), 
			(_0023_003DqYCaqglgk8eBUCLwO_Kqu_w_003D_003D)8 => new Vector2(Max.X, Min.Y), 
			_ => throw new _0023_003DqRaaOoTBvHvWK2vyz8S665Q_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850811127)), 
		};
	}
}
