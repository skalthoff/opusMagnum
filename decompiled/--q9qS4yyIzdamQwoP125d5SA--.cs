using System.Collections.Generic;
using System.IO;

public sealed class _0023_003Dq9qS4yyIzdamQwoP125d5SA_003D_003D
{
	public string _0023_003Dq9abEtJxUOJo60H8iMszY4w_003D_003D;

	public Dictionary<Language, Vignette> _0023_003DqqtoUdquGtE453TJNJZ3qGA_003D_003D = new Dictionary<Language, Vignette>();

	public _0023_003Dq9qS4yyIzdamQwoP125d5SA_003D_003D(string _0023_003DqjaZhIfN_0024fRrziEamWRhLcw_003D_003D)
	{
		_0023_003Dq9abEtJxUOJo60H8iMszY4w_003D_003D = _0023_003DqjaZhIfN_0024fRrziEamWRhLcw_003D_003D;
		Language[] array = new Language[13]
		{
			Language.English,
			Language.German,
			Language.French,
			Language.Russian,
			Language.Chinese,
			Language.Japanese,
			Language.Spanish,
			Language.Korean,
			Language.Turkish,
			Language.Ukrainian,
			Language.Portuguese,
			Language.Czech,
			Language.Polish
		};
		foreach (Language language in array)
		{
			string path = Path.Combine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805785), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848451), string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848499), _0023_003DqjaZhIfN_0024fRrziEamWRhLcw_003D_003D, _0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003Dq32C9wiQedZk_0024_MB2Amu2PQ_003D_003D[language]));
			if (!File.Exists(path))
			{
				string path2 = Path.Combine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805785), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848451), string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848499), _0023_003DqjaZhIfN_0024fRrziEamWRhLcw_003D_003D, _0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003Dq32C9wiQedZk_0024_MB2Amu2PQ_003D_003D[Language.English]));
				if (language == Language.English || !File.Exists(path2))
				{
					File.WriteAllText(path, string.Empty);
				}
				else
				{
					File.WriteAllText(path, File.ReadAllText(path2));
				}
			}
			_0023_003DqqtoUdquGtE453TJNJZ3qGA_003D_003D[language] = new Vignette(File.ReadAllText(path), Path.GetFileNameWithoutExtension(path), language);
			if (language != Language.English)
			{
				continue;
			}
			Vignette vignette = new Vignette(File.ReadAllText(path), Path.GetFileNameWithoutExtension(path), Language.Pseudo);
			_0023_003DqqtoUdquGtE453TJNJZ3qGA_003D_003D[Language.Pseudo] = vignette;
			vignette._0023_003DqSc8XLhgG_0024hUKDq_0024yeKuqyA_003D_003D = _0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqDlXc_0024u8aV4XgIfkN7vQinQ_003D_003D(vignette._0023_003DqSc8XLhgG_0024hUKDq_0024yeKuqyA_003D_003D);
			foreach (List<VignetteEvent> item in vignette._0023_003DqN_0024vkLOZfHUFNuHFpCNrFuQ_003D_003D)
			{
				for (int j = 0; j < item.Count; j++)
				{
					if (item[j]._0023_003DqRke4UC1WeTITs0dYzBmaaA_003D_003D())
					{
						VignetteEvent.LineFields lineFields = item[j]._0023_003DqRLKkU1hMPk_00244acc8_egb3g_003D_003D();
						item[j] = VignetteEvent._0023_003DqDdYZMC7iayu_0024aP9sAURUBQ_003D_003D(lineFields._0023_003DqVPfzvfCKFP32sBwhRzftHg_003D_003D, _0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqDlXc_0024u8aV4XgIfkN7vQinQ_003D_003D(lineFields._0023_003DqZFMGcQJN0lhN6PYwfr2kEg_003D_003D));
					}
				}
			}
		}
	}

	public Vignette _0023_003Dq920NaJWIRLlLu6X6J_0024KeVw_003D_003D()
	{
		return _0023_003DqqtoUdquGtE453TJNJZ3qGA_003D_003D[_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqXlg23IO9hk2TzaPnoEfeL5OmxgBaqr2F9ZTrnO27pKg_003D];
	}
}
