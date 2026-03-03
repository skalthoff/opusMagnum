using System;
using System.Collections.Generic;

internal sealed class _0023_003DqpRGyP_wVnwlrhvA8tocMlQ_003D_003D
{
	public static void _0023_003DqPcWaQNYohFBOnLryKUNUIQ_003D_003D()
	{
		_0023_003Dq8e8f93cid72ToF15Gqp1m4g6EdmTkE2Ib_7Ebvk7Nu8_003D();
		_0023_003DqD9xmGHu9ZygmOvO_0024I54Y76ZWVZcSCcDciHVsnl473rs_003D();
		_0023_003DqnUGLn8JKfUowz21Da00ZBKnOAu0R3rD7XLB2dOJd6fk_003D();
		_0023_003Dqz8OyPYcYNjqsHsoBk_0024EHB3tz3MIHRWSX5Cws5uF_00245v8_003D();
		_0023_003Dq1WGtP4yuoiMC5Gvn_0024oyE5U3f1aQ9_jgahZ_xXMn6jF4_003D();
	}

	private static void _0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(object _0023_003DqcN4rjej__j_AXZgUVCpD2g_003D_003D, object _0023_003DqUs2mhT76_0024NUOI6Gn1_00246HNQ_003D_003D)
	{
	}

	private static void _0023_003Dq8e8f93cid72ToF15Gqp1m4g6EdmTkE2Ib_7Ebvk7Nu8_003D()
	{
		HexIndex hexIndex = new HexIndex(1, 2);
		HexIndex[] array = new HexIndex[6]
		{
			new HexIndex(1, 2),
			new HexIndex(-2, 3),
			new HexIndex(-3, 1),
			new HexIndex(-1, -2),
			new HexIndex(2, -3),
			new HexIndex(3, -1)
		};
		for (int i = 0; i < 6; i++)
		{
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexIndex.Rotated(new HexRotation(i)), array[i]);
		}
	}

	private static void _0023_003DqD9xmGHu9ZygmOvO_0024I54Y76ZWVZcSCcDciHVsnl473rs_003D()
	{
		HexIndex hexIndex = new HexIndex(2, 0);
		HexIndex pivot = new HexIndex(1, 0);
		HexIndex[] array = new HexIndex[6]
		{
			new HexIndex(2, 0),
			new HexIndex(1, 1),
			new HexIndex(0, 1),
			new HexIndex(0, 0),
			new HexIndex(1, -1),
			new HexIndex(2, -1)
		};
		List<HexIndex> list = new List<HexIndex>();
		for (int i = 0; i < 6; i++)
		{
			HexIndex hexIndex2 = hexIndex.RotatedAround(pivot, new HexRotation(i));
			list.Add(hexIndex2);
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexIndex2, array[i]);
		}
	}

	private static void _0023_003DqnUGLn8JKfUowz21Da00ZBKnOAu0R3rD7XLB2dOJd6fk_003D()
	{
		_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(0, HexIndex.Distance(new HexIndex(2, 3), new HexIndex(2, 3)));
		_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(1, HexIndex.Distance(new HexIndex(2, 3), new HexIndex(1, 4)));
		_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(2, HexIndex.Distance(new HexIndex(1, 0), new HexIndex(2, 1)));
	}

	private static void _0023_003Dqz8OyPYcYNjqsHsoBk_0024EHB3tz3MIHRWSX5Cws5uF_00245v8_003D()
	{
		HexIndex a = new HexIndex(0, 0);
		HexIndex[] adjacentOffsets = HexIndex.AdjacentOffsets;
		foreach (HexIndex b in adjacentOffsets)
		{
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(HexIndex.Distance(a, b), 1);
		}
	}

	private static void _0023_003Dq1WGtP4yuoiMC5Gvn_0024oyE5U3f1aQ9_jgahZ_xXMn6jF4_003D()
	{
		for (int i = 0; i < 6; i++)
		{
			HexRotation hexRotation = new HexRotation(i);
			float num = (float)(i * 60) * ((float)Math.PI / 180f);
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num));
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num - (float)Math.PI * 18f));
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num + (float)Math.PI * 18f));
			float num2 = (float)Math.PI / 180f;
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num - num2));
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num + num2));
			float num3 = (float)Math.PI * 29f / 180f;
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num - num3));
			_0023_003DqzSLoVc_0024rxZVyOSnlGMYUrQ_003D_003D(hexRotation, HexRotation.Rounded(num + num3));
		}
	}
}
