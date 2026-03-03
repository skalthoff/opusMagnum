using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

public sealed class _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D
{
	public sealed class _0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D
	{
		public IntPtr _0023_003Dq9ZXRmb5Vn2INRwhKhq_0024ejg_003D_003D;

		public Index2 _0023_003DqHVwh2KvnmT2N6b8bY9sHBg_003D_003D;

		public List<_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D> _0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D = new List<_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D>();

		public float _0023_003DqMx2kpt1GXORWiOMazZ3v4w_003D_003D;

		public float _0023_003DqM5aS1GFcb22BBrFkbeQwNQ_003D_003D;

		public byte[] _0023_003DqNndwolyDaVlr0PPX5NhgYQ_003D_003D;

		public int _0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D;

		public int _0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D;

		public int _0023_003Dqx_0024TwDnAzXYx8htRJi7tpHQ_003D_003D;

		public FontGlyphInfo _0023_003DqnFcSwTz0l9VytOypq4P_mg_003D_003D;
	}

	private static FontGlyphInfo _0023_003DqDTpknr5y5uyv1cxqTS8AE5qVlSZuf5zA9mYZ_0024qM693k_003D = new FontGlyphInfo
	{
		AdvanceX = 0f,
		Height = 0f,
		OffsetX = 0f,
		OffsetY = 0f,
		TextureIndex = 0,
		Width = 0f,
		X = 0f,
		Y = 0f
	};

	public float _0023_003DqZUMmCfMUOYG8j76BVAYxqw_003D_003D;

	public float _0023_003DqFXf_IbBZM_CM7oMbrcfwsQ_003D_003D;

	public float _0023_003DqFdipoIPvo1DrydaSj3J8_w_003D_003D;

	public List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D> _0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D;

	public List<FontGlyphInfo> _0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D;

	public Index2 _0023_003Dqrc9DL1AN4AiOgI4E6grI2g_003D_003D;

	public _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D[] _0023_003DquDu1ihpGepUwZOX2gYGonQ_003D_003D;

	private static readonly Index2 _0023_003Dq0jv5QF3AlMTyz69zpp_D3hiiJF2aKATXghaSxfs7TPr4qunHJ_0024u4jPhSYLT6QllQ = new Index2(512, 512);

	public string _0023_003Dq6EYobdWvsS6PJKshK7ALfrqbYGHB6W7rEhoIsesq6_00240_003D(string _0023_003DqmRzVbYvt12Rs4OlZZX9MCA_003D_003D)
	{
		StringBuilder stringBuilder = new StringBuilder();
		foreach (char c in _0023_003DqmRzVbYvt12Rs4OlZZX9MCA_003D_003D)
		{
			if (c == '\n')
			{
				stringBuilder.Append(c);
				continue;
			}
			char value = '?';
			foreach (_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D item in _0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D)
			{
				if (c >= item._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D && c <= item._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D)
				{
					value = c;
					break;
				}
			}
			stringBuilder.Append(value);
		}
		return stringBuilder.ToString();
	}

	public bool _0023_003Dq_0024AmynykjjN0nx1SB0WVEngiqxXUJv6yo7OM4rBUeUp8_003D(int _0023_003DqA9HQ8ws5Xjkz451knPOBIQ_003D_003D, out FontGlyphInfo _0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D)
	{
		if (_0023_003DqA9HQ8ws5Xjkz451knPOBIQ_003D_003D == 9679)
		{
			_0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D = _0023_003DqDTpknr5y5uyv1cxqTS8AE5qVlSZuf5zA9mYZ_0024qM693k_003D;
			return true;
		}
		int num = 0;
		for (int i = 0; i < _0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D.Count; i++)
		{
			_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2 = _0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D[i];
			if (_0023_003DqA9HQ8ws5Xjkz451knPOBIQ_003D_003D >= _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D && _0023_003DqA9HQ8ws5Xjkz451knPOBIQ_003D_003D <= _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D)
			{
				int num2 = num + (_0023_003DqA9HQ8ws5Xjkz451knPOBIQ_003D_003D - _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D);
				if (num2 < _0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D.Count)
				{
					_0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D = _0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D[num2];
					return true;
				}
				_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(_0023_003DqEAUzl2SAuL7SL8Q6djdntQ_003D_003D: false, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803263));
			}
			num += _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D - _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D2._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D + 1;
		}
		_0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D = _0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D[0];
		return false;
	}

	public FontGlyphInfo _0023_003DqASxD03x0nWYRnuBTXL86T49GK2verLz7POU3PXdD_0024A4_003D(int _0023_003Dq1o6sSNQ9GK6N8ItFbXl_iA_003D_003D)
	{
		_0023_003Dq_0024AmynykjjN0nx1SB0WVEngiqxXUJv6yo7OM4rBUeUp8_003D(_0023_003Dq1o6sSNQ9GK6N8ItFbXl_iA_003D_003D, out var _0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D);
		return _0023_003DqbZQtDpVvZqylK4vvCgdNoQ_003D_003D;
	}

	public static List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D> _0023_003DqZ3sh9Luj52_TDrMDwtli9l8NiL8f0jBGxcZlp_0024oh_V0_003D()
	{
		return new List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D>
		{
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(32, 255),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(256, 591),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(1024, 1279),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(8192, 8303)
		};
	}

	public static List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D> _0023_003DqtFsEL3RiWZT5wDbMO3w_DsF8hgV5Lmk8u9kH7b59_00246Y_003D()
	{
		return new List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D>
		{
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(32, 255),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(256, 591),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(1024, 1279),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(8192, 8303),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(12352, 12543),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(19968, 40959),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(12288, 12336),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(65280, 65520),
			new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(44032, 55215)
		};
	}

	public static _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D _0023_003DqcEVS856p0hJq03800JP3xBtuW38OSdhPCaQEdTapihE_003D(string _0023_003Dqmfbb1r_TevrH9sHOxVic0w_003D_003D, float _0023_003DqY_0024TPIC_0024hY9kJPMn20GDLvw_003D_003D, float _0023_003Dq_0024wotX9DMlqHzHZvJ_0024T68hA_003D_003D, int _0023_003DqcK2oZXYhn0U3z5CbSP1ByC3zko37lP06CkVdK91da2g_003D, List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D> _0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D)
	{
		Directory.CreateDirectory(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803148));
		string path = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803186), new object[5]
		{
			Path.GetFileNameWithoutExtension(_0023_003Dqmfbb1r_TevrH9sHOxVic0w_003D_003D),
			_0023_003DqY_0024TPIC_0024hY9kJPMn20GDLvw_003D_003D,
			_0023_003Dq_0024wotX9DMlqHzHZvJ_0024T68hA_003D_003D,
			_0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D.Count,
			5
		});
		Time time;
		if (_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqLqalDA38XbLiV7HV5I6LKg_003D_003D && !File.Exists(path))
		{
			time = Time.Now();
			_0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D.Insert(0, new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(0, 0));
			float ascent;
			float descent;
			float lineAdvance;
			IntPtr intPtr = FontRenderer.CreateFontRenderer(_0023_003Dqmfbb1r_TevrH9sHOxVic0w_003D_003D, _0023_003DqY_0024TPIC_0024hY9kJPMn20GDLvw_003D_003D, out ascent, out descent, out lineAdvance);
			if (intPtr == IntPtr.Zero)
			{
				throw new _0023_003DqRaaOoTBvHvWK2vyz8S665Q_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803120) + _0023_003Dqmfbb1r_TevrH9sHOxVic0w_003D_003D);
			}
			_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D _0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D = new _0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D
			{
				_0023_003Dq9ZXRmb5Vn2INRwhKhq_0024ejg_003D_003D = intPtr,
				_0023_003DqMx2kpt1GXORWiOMazZ3v4w_003D_003D = _0023_003DqY_0024TPIC_0024hY9kJPMn20GDLvw_003D_003D,
				_0023_003DqM5aS1GFcb22BBrFkbeQwNQ_003D_003D = _0023_003Dq_0024wotX9DMlqHzHZvJ_0024T68hA_003D_003D,
				_0023_003DqNndwolyDaVlr0PPX5NhgYQ_003D_003D = new byte[1048576],
				_0023_003DqHVwh2KvnmT2N6b8bY9sHBg_003D_003D = _0023_003Dq0jv5QF3AlMTyz69zpp_D3hiiJF2aKATXghaSxfs7TPr4qunHJ_0024u4jPhSYLT6QllQ
			};
			_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D._0023_003DqnFcSwTz0l9VytOypq4P_mg_003D_003D = _0023_003DqEULRv92Ckp1eNp8ZXnwuLg_003D_003D(_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D, 0);
			List<FontGlyphInfo> list = new List<FontGlyphInfo>();
			foreach (_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D item3 in _0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D)
			{
				for (int i = item3._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D; i <= item3._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D; i++)
				{
					FontGlyphInfo item = _0023_003DqEULRv92Ckp1eNp8ZXnwuLg_003D_003D(_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D, i);
					list.Add(item);
				}
			}
			FontRenderer.DestroyFontRenderer(intPtr);
			FileStream fileStream = new FileStream(path, FileMode.Create);
			try
			{
				BinaryWriter binaryWriter = new BinaryWriter(fileStream);
				try
				{
					binaryWriter.Write(ascent);
					binaryWriter.Write(descent);
					binaryWriter.Write(lineAdvance);
					binaryWriter.Write(_0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D.Count);
					foreach (_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D item4 in _0023_003DqZwhzLX6Qf3rbfQ5CwP2Leg_003D_003D)
					{
						binaryWriter.Write(item4._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D);
						binaryWriter.Write(item4._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D);
					}
					binaryWriter.Write(list.Count);
					foreach (FontGlyphInfo item5 in list)
					{
						binaryWriter.Write(item5.TextureIndex);
						binaryWriter.Write(item5.X);
						binaryWriter.Write(item5.Y);
						binaryWriter.Write(item5.Width);
						binaryWriter.Write(item5.Height);
						binaryWriter.Write(item5.OffsetX);
						binaryWriter.Write(item5.OffsetY);
						binaryWriter.Write(item5.AdvanceX);
					}
					binaryWriter.Write(_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Count);
					foreach (_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D item6 in _0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D)
					{
						binaryWriter.Write(item6._0023_003DqjQx9OlgxJ46PnSu9kMIoZw_003D_003D());
						binaryWriter.Write(item6._0023_003Dqch1uXvz3Kaa1pWNzLr5Leg_003D_003D());
						binaryWriter.Write(item6._0023_003Dq1Nt8EYFcWgybJaf5zup3Qg_003D_003D);
					}
				}
				finally
				{
					((IDisposable)binaryWriter).Dispose();
				}
			}
			finally
			{
				((IDisposable)fileStream).Dispose();
			}
			(Time.Now() - time)._0023_003DqPg_0024xIQ6YpDjW4KgiFGFHLQ_003D_003D();
		}
		time = Time.Now();
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2 = new _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D();
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003Dqrc9DL1AN4AiOgI4E6grI2g_003D_003D = _0023_003Dq0jv5QF3AlMTyz69zpp_D3hiiJF2aKATXghaSxfs7TPr4qunHJ_0024u4jPhSYLT6QllQ;
		FileStream fileStream2 = new FileStream(path, FileMode.Open, FileAccess.Read);
		try
		{
			BinaryReader binaryReader = new BinaryReader(fileStream2);
			try
			{
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqZUMmCfMUOYG8j76BVAYxqw_003D_003D = binaryReader.ReadSingle();
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqFXf_IbBZM_CM7oMbrcfwsQ_003D_003D = binaryReader.ReadSingle();
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqFdipoIPvo1DrydaSj3J8_w_003D_003D = binaryReader.ReadSingle();
				int num = binaryReader.ReadInt32();
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D = new List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D>();
				for (int j = 0; j < num; j++)
				{
					int _0023_003Dq1fTmGJNBkfRRatW5AB0ssA_003D_003D = binaryReader.ReadInt32();
					int _0023_003DqXhyhX9OrP1Q3XlXkXc4t8A_003D_003D = binaryReader.ReadInt32();
					_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D.Add(new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(_0023_003Dq1fTmGJNBkfRRatW5AB0ssA_003D_003D, _0023_003DqXhyhX9OrP1Q3XlXkXc4t8A_003D_003D));
				}
				int num2 = binaryReader.ReadInt32();
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D = new List<FontGlyphInfo>();
				FontGlyphInfo item2 = default(FontGlyphInfo);
				for (int k = 0; k < num2; k++)
				{
					item2.TextureIndex = binaryReader.ReadInt32();
					item2.X = binaryReader.ReadSingle();
					item2.Y = binaryReader.ReadSingle();
					item2.Width = binaryReader.ReadSingle();
					item2.Height = binaryReader.ReadSingle();
					item2.OffsetX = binaryReader.ReadSingle();
					item2.OffsetY = binaryReader.ReadSingle();
					item2.AdvanceX = binaryReader.ReadSingle();
					_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D.Add(item2);
				}
				int num3 = binaryReader.ReadInt32();
				_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DquDu1ihpGepUwZOX2gYGonQ_003D_003D = new _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D[num3];
				for (int l = 0; l < num3; l++)
				{
					_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D _0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D2 = (_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D)1;
					int num4 = binaryReader.ReadInt32();
					int num5 = binaryReader.ReadInt32();
					byte[] _0023_003DqRHCjLWOwwEy9edyI_0024RCvhQ_003D_003D = binaryReader.ReadBytes(num4 * num5 * _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqZy1vd8HJ1YCon9sIZ6wOAQ_003D_003D(_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D2));
					_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D _0023_003DqpcR4IfIud_FIlxZXUodV0g_003D_003D = new _0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D(_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D2, num4, num5, _0023_003DqRHCjLWOwwEy9edyI_0024RCvhQ_003D_003D);
					_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DquDu1ihpGepUwZOX2gYGonQ_003D_003D[l] = Renderer._0023_003Dqrc3BdFat04yLy9aaEx9COw_003D_003D(_0023_003DqpcR4IfIud_FIlxZXUodV0g_003D_003D);
				}
			}
			finally
			{
				((IDisposable)binaryReader).Dispose();
			}
		}
		finally
		{
			((IDisposable)fileStream2).Dispose();
		}
		(Time.Now() - time)._0023_003DqPg_0024xIQ6YpDjW4KgiFGFHLQ_003D_003D();
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqFdipoIPvo1DrydaSj3J8_w_003D_003D += _0023_003DqcK2oZXYhn0U3z5CbSP1ByC3zko37lP06CkVdK91da2g_003D;
		return _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2;
	}

	private static FontGlyphInfo _0023_003DqEULRv92Ckp1eNp8ZXnwuLg_003D_003D(_0023_003DqOMwEDtMn6xMbVRwrKfsVGGHVbYOZqKgYfr1sw1lfz9Y_003D _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D, int _0023_003DqZOs8M3ZiK77dTZ9WUv8crw_003D_003D)
	{
		int x = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqHVwh2KvnmT2N6b8bY9sHBg_003D_003D.X;
		int y = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqHVwh2KvnmT2N6b8bY9sHBg_003D_003D.Y;
		int glyphIndex = FontRenderer.GetGlyphIndex(_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dq9ZXRmb5Vn2INRwhKhq_0024ejg_003D_003D, _0023_003DqZOs8M3ZiK77dTZ9WUv8crw_003D_003D);
		if (glyphIndex == 0)
		{
			return _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqnFcSwTz0l9VytOypq4P_mg_003D_003D;
		}
		FontRenderer.GetGlyphBitmap(_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dq9ZXRmb5Vn2INRwhKhq_0024ejg_003D_003D, glyphIndex, _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqNndwolyDaVlr0PPX5NhgYQ_003D_003D, out var bitmapWidth, out var bitmapHeight, out var offsetX, out var offsetY, out var advanceX);
		_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(bitmapWidth * bitmapHeight <= _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqNndwolyDaVlr0PPX5NhgYQ_003D_003D.Length, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803018));
		if (_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D + bitmapWidth > x)
		{
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqx_0024TwDnAzXYx8htRJi7tpHQ_003D_003D + 4;
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D = 0;
		}
		if (_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Count == 0 || _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D + bitmapHeight > y)
		{
			if (_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Count >= 200)
			{
				throw new _0023_003DqRaaOoTBvHvWK2vyz8S665Q_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803053));
			}
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Add(new _0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D((_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D)1, x, y, new byte[x * y]));
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D = 0;
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D = 0;
			_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqx_0024TwDnAzXYx8htRJi7tpHQ_003D_003D = 0;
		}
		FontGlyphInfo result = default(FontGlyphInfo);
		result.TextureIndex = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Count - 1;
		result.X = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D;
		result.Y = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D;
		result.Width = bitmapWidth;
		result.Height = bitmapHeight;
		result.OffsetX = offsetX;
		result.OffsetY = offsetY - bitmapHeight;
		result.AdvanceX = advanceX;
		_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D _0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D2 = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqaV3CV4cBHqBf2o9pGdlikw_003D_003D.Last();
		for (int i = 0; i < bitmapHeight; i++)
		{
			for (int j = 0; j < bitmapWidth; j++)
			{
				int num = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D + j;
				int num2 = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D + i;
				if (num < x && num2 < y)
				{
					byte b = _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqNndwolyDaVlr0PPX5NhgYQ_003D_003D[(bitmapHeight - i - 1) * bitmapWidth + j];
					b = (byte)((float)Math.Pow((float)(int)b / 255f, 1f / _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqM5aS1GFcb22BBrFkbeQwNQ_003D_003D) * 255f);
					_0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D2._0023_003Dq1Nt8EYFcWgybJaf5zup3Qg_003D_003D[num2 * x + num] = b;
				}
			}
		}
		_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqx_0024TwDnAzXYx8htRJi7tpHQ_003D_003D = Math.Max(_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqx_0024TwDnAzXYx8htRJi7tpHQ_003D_003D, _0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003Dqtd2hSAV5Ia7_X1xj2iTQvg_003D_003D + bitmapHeight);
		_0023_003Dq3w31X7AyABUSxZpWv_0024GQXA_003D_003D._0023_003DqeExJh0e_0024GGS9UON5kqGs8Q_003D_003D += bitmapWidth + 4;
		return result;
	}

	public static _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D _0023_003DqHjpGlmJWC5tgSqUwW293xySeGT1HulQtlvTOCFHn_0024CY_003D(string _0023_003DqkQx0YGFsWgaS0Kh7HHKBWA_003D_003D)
	{
		_0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2 = Renderer._0023_003DqEFo6Mlcr5P0xmyyJUPhMQ6EPiXfNtvHl66quophpNBk_003D(_0023_003DqkQx0YGFsWgaS0Kh7HHKBWA_003D_003D, (_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D)1);
		float num = _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2._0023_003DqCvFw_qmLCUyv_0024pJeA_00242fuQ_003D_003D() / 16;
		float num2 = _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2._0023_003DqpKfEOOa42zjzqerT2f9obA_003D_003D() / 16;
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2 = new _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D();
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003Dqrc9DL1AN4AiOgI4E6grI2g_003D_003D = _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2._0023_003DqS1FXM7vc4G9JN8xWcZ9Tsw_003D_003D;
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DquDu1ihpGepUwZOX2gYGonQ_003D_003D = new _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D[1];
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DquDu1ihpGepUwZOX2gYGonQ_003D_003D[0] = _0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2;
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqZUMmCfMUOYG8j76BVAYxqw_003D_003D = num2;
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqFXf_IbBZM_CM7oMbrcfwsQ_003D_003D = 0f;
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqFdipoIPvo1DrydaSj3J8_w_003D_003D = 0f;
		_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D item = new _0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D(0, 255);
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqAClZ3N8z42k4ii29noya8g_003D_003D = new List<_0023_003Dq1iT88wpzjnqerUhdPeA32w_003D_003D> { item };
		_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D = new List<FontGlyphInfo>();
		for (int i = item._0023_003DqLoHsqo0ckDhgvABBq_0024eHog_003D_003D; i <= item._0023_003Dq_vZiZl98k1Hanso_0024bym9Qw_003D_003D; i++)
		{
			_0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2._0023_003DqVQ4As4C_0024BQsbdjIYJfdrhw_003D_003D.Add(new FontGlyphInfo
			{
				TextureIndex = 0,
				X = (float)(i % 16) * num,
				Y = (float)_0023_003DqkSodVkNJRQnSJWtiOMu4kg_003D_003D2._0023_003DqpKfEOOa42zjzqerT2f9obA_003D_003D() - (float)(i / 16) * num2,
				Width = num,
				Height = 0f - num2,
				OffsetX = 0f,
				OffsetY = 0f,
				AdvanceX = num
			});
		}
		return _0023_003DqmiwB2kbfH7l6DwGyB4KKZA_003D_003D2;
	}
}
