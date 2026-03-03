using System;

public sealed class _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D
{
	public static _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D _0023_003DqIWs0XvTMOZ5_HFGjfV84rQ_003D_003D = new _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D(_0023_003Dq2UqcJSe2_00245N1HhpOyAz1Mg_003D_003D._0023_003Dqc50Z5wZTflISAZxdug3Jow_003D_003D._0023_003DqYvNHu6Ns440FlAwGZxzTZw_003D_003D._0023_003Dqrdkl6b8sd6NKWX0cwJittw_003D_003D._0023_003DqWPp4vQh_94zqNmICZBmbZw_003D_003D());

	public static _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D _0023_003DqT_00240_0024saJJct8UFUvatRPDdw_003D_003D = new _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D(new Index2(66, 57));

	public readonly Vector2 _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D;

	public _0023_003DqfERfV0GY_xmGXWefYmmI5Q_003D_003D(Index2 _0023_003DqHKpEVYn_00249IPU7ZaEBLkC8g_003D_003D)
	{
		_0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D = _0023_003DqHKpEVYn_00249IPU7ZaEBLkC8g_003D_003D.ToVector2();
	}

	public float _0023_003DqEgPiNDGLWfz55X4HlF0HTvRIxo686B5dEpKGB1PkPO8_003D()
	{
		return _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.X;
	}

	public Vector2 _0023_003DqsDGoLxMgBUwcuTKFzRlSlse_caYsO1EQJcBI7aZnjvQ_003D(HexIndex _0023_003DqSTgF9BIyOMhsc8EePgU6pg_003D_003D, Vector2 _0023_003Dqx0T0gz24xKhYgNIv3IA9hg_003D_003D)
	{
		return _0023_003Dqx0T0gz24xKhYgNIv3IA9hg_003D_003D + _0023_003DqyirDZ8dcW1VaWYDudYDwxhSch7V3lu5nHp4FegIV_0024FU_003D(_0023_003DqSTgF9BIyOMhsc8EePgU6pg_003D_003D);
	}

	public Vector2 _0023_003DqyirDZ8dcW1VaWYDudYDwxhSch7V3lu5nHp4FegIV_0024FU_003D(HexIndex _0023_003DqgRw6lKEgdPaWDAQH8eWViQ_003D_003D)
	{
		float x = _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.X * ((float)_0023_003DqgRw6lKEgdPaWDAQH8eWViQ_003D_003D.Q + 0.5f * (float)_0023_003DqgRw6lKEgdPaWDAQH8eWViQ_003D_003D.R);
		float y = _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.Y * (float)_0023_003DqgRw6lKEgdPaWDAQH8eWViQ_003D_003D.R;
		return new Vector2(x, y);
	}

	public HexIndex _0023_003DqteIDCIqmsN3Bk_00242MpqldcVcxL3vgzLMSTOEMQY6P6mA_003D(Vector2 _0023_003DqPm39gut18mr_0024hSp0CmoctQ_003D_003D, Vector2 _0023_003Dqg6j5WwPUohzp08Xa1wrdCg_003D_003D)
	{
		Vector2 vector = _0023_003DqPm39gut18mr_0024hSp0CmoctQ_003D_003D - _0023_003Dqg6j5WwPUohzp08Xa1wrdCg_003D_003D;
		float num = vector.X / _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.X - 0.5f * vector.Y / _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.Y;
		float num2 = vector.Y / _0023_003Dq2gszGIREUvKmKaORgA_RYA_003D_003D.Y;
		float num3 = 0f - num - num2;
		int num4 = (int)Math.Round(num);
		int num5 = (int)Math.Round(num2);
		int num6 = (int)Math.Round(num3);
		float num7 = Math.Abs(num - (float)num4);
		float num8 = Math.Abs(num2 - (float)num5);
		float num9 = Math.Abs(num3 - (float)num6);
		if (num7 > num8 && num7 > num9)
		{
			num4 = -num5 - num6;
		}
		else if (num8 > num9)
		{
			num5 = -num4 - num6;
		}
		else
		{
			num6 = -num4 - num5;
		}
		return new HexIndex(num4, num5);
	}
}
