using System;
using System.IO;
using System.Text;
using SDL2;
using Steamworks;

public static class _0023_003Dq2LWs2GS3YwVDvdCY7pAeqQ_003D_003D
{
	public static void _0023_003Dqg6tyIxLUCx_00243__G63OPM7NXadA_6m8IA9a5U6WogwhU_003D()
	{
		PlatformID platform = Environment.OSVersion.Platform;
		string versionString = Environment.OSVersion.VersionString;
		string arg = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828443);
		_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqhFzzZFf_00243kD8gPQl9_O2Ag_003D_003D = Type.GetType(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828433)) != null;
		if (platform == PlatformID.Win32NT || platform == PlatformID.Win32Windows)
		{
			_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D = _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Windows;
		}
		else
		{
			string text = SDL.SDL_GetPlatform();
			if (text.Equals(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828478)))
			{
				_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D = _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Linux;
			}
			else if (text.Equals(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828466)))
			{
				_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D = _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Mac;
			}
		}
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828451), platform, (int)platform));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828359), versionString));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828399), arg));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828303), Environment.Is64BitOperatingSystem));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850828341), _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826204), Environment.Version));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826234), _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqhFzzZFf_00243kD8gPQl9_O2Ag_003D_003D));
		stringBuilder.Append(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826141), Environment.Is64BitProcess));
		_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqYXvzZX6xs76BY_P35r3oc05OtbjtsmCDQ5b2hNGlsbs_003D = stringBuilder.ToString();
	}

	public static bool _0023_003DqI3WtKyt_00244n3CARgysPaQnV0WaH6pVqdn5o2jAFScaKo_003D()
	{
		if (_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D == _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Windows)
		{
			StringBuilder stringBuilder = new StringBuilder(9);
			Win32.GetKeyboardLayoutName(stringBuilder);
			string text = stringBuilder.ToString().ToLowerInvariant();
			if (!(text == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826174)))
			{
				return text == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826159);
			}
			return true;
		}
		return false;
	}

	public static string _0023_003Dq6G5epLv2Us3yzgzdAzjsfg_003D_003D()
	{
		string text = ((!_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqQopT4GnkGZVw6kE2V4K7WqGgFOiegM4WY6jnDR04ROI_003D) ? _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826144) : SteamUser.GetSteamID().m_SteamID._0023_003DqJ48CPrMhBNnF2kaBaRm3RNPbduqs65u9_W3Mky02XoM_003D());
		string text2;
		if (File.Exists(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826061)))
		{
			text2 = File.ReadAllText(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826061)).Trim();
		}
		else if (_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D == _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Mac)
		{
			text2 = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826101), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826087), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqV4fpEarKb5hVAhDt9DwfYg_003D_003D, text);
		}
		else if (_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D == _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Windows)
		{
			text2 = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825997), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqV4fpEarKb5hVAhDt9DwfYg_003D_003D, text);
		}
		else if (_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D == _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Linux)
		{
			string environmentVariable = Environment.GetEnvironmentVariable(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826046));
			string path = ((environmentVariable == null || environmentVariable.Length <= 0 || !Path.IsPathRooted(environmentVariable)) ? Path.Combine(Environment.GetEnvironmentVariable(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850826026)), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825951), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825938)) : environmentVariable);
			text2 = Path.Combine(path, _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqV4fpEarKb5hVAhDt9DwfYg_003D_003D, text);
		}
		else
		{
			text2 = SDL.SDL_GetPrefPath(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825926), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqV4fpEarKb5hVAhDt9DwfYg_003D_003D);
		}
		Directory.CreateDirectory(text2);
		return text2;
	}
}
