using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public static class SolutionManager
{
	private sealed class _0023_003DqG80vVKA4EykOkcUMj_0024Qm7CLxUat1vnhbzihNeJpoQhU_003D
	{
		public Puzzle _0023_003Dq1Umlmei3s1HY5twwXh2nBQ_003D_003D;

		internal bool _0023_003DqAJjDuh0TDUSieHfXNjcbXj6f_0024YFaR6wqZo2t2DAFMkk_003D(Solution _0023_003Dq1h1hzqIb9_bAT2l8pXzNqw_003D_003D)
		{
			return _0023_003Dq1h1hzqIb9_bAT2l8pXzNqw_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D == _0023_003Dq1Umlmei3s1HY5twwXh2nBQ_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D;
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<string, DateTime> _003C_003E9__0_0;

		internal DateTime _0023_003Dq1HhbwdQIrcZDc4fTZ7oe_0024hz263BgXGohh3GKhS1Y2C8_003D(string _0023_003DqLf5oHFN2JjlOWtF92ck6CQ_003D_003D)
		{
			return File.GetCreationTimeUtc(_0023_003DqLf5oHFN2JjlOWtF92ck6CQ_003D_003D);
		}
	}

	public static List<Solution> _0023_003DqxLdWfC0HIp4wr7qQLCOGiw_003D_003D()
	{
		IOrderedEnumerable<string> orderedEnumerable = from _0023_003DqLf5oHFN2JjlOWtF92ck6CQ_003D_003D in Directory.EnumerateFiles(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850804746) + Solution._0023_003Dq4crTKzX_s8G7lhQ_0024j9HVyA_003D_003D)
			orderby File.GetCreationTimeUtc(_0023_003DqLf5oHFN2JjlOWtF92ck6CQ_003D_003D)
			select _0023_003DqLf5oHFN2JjlOWtF92ck6CQ_003D_003D;
		List<Solution> list = new List<Solution>();
		foreach (string item in orderedEnumerable)
		{
			Maybe<Solution> maybe = Solution._0023_003Dq0WaBlOaOC95VoTXOqFIFAQ_003D_003D(item);
			if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
			{
				list.Add(maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
			}
		}
		return list;
	}

	public static Solution[] _0023_003Dqhiu3J9B_drNMHFdxxZ_002464I7PHCDgppPKaZ_002484AodycU_003D(Puzzle _0023_003DqltHC8_0024rYUpcLc1cLTERW0w_003D_003D)
	{
		_0023_003DqG80vVKA4EykOkcUMj_0024Qm7CLxUat1vnhbzihNeJpoQhU_003D CS_0024_003C_003E8__locals2 = new _0023_003DqG80vVKA4EykOkcUMj_0024Qm7CLxUat1vnhbzihNeJpoQhU_003D();
		CS_0024_003C_003E8__locals2._0023_003Dq1Umlmei3s1HY5twwXh2nBQ_003D_003D = _0023_003DqltHC8_0024rYUpcLc1cLTERW0w_003D_003D;
		return GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003Dq3XyF_0024m0mJ19HKM9j8Xh0Eg_003D_003D.Where((Solution _0023_003Dq1h1hzqIb9_bAT2l8pXzNqw_003D_003D) => _0023_003Dq1h1hzqIb9_bAT2l8pXzNqw_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D == CS_0024_003C_003E8__locals2._0023_003Dq1Umlmei3s1HY5twwXh2nBQ_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D).ToArray();
	}
}
