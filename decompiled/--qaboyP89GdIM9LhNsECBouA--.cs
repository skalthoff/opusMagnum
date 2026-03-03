using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using Ionic.Zip;

public sealed class _0023_003DqaboyP89GdIM9LhNsECBouA_003D_003D
{
	public static class _0023_003DqqIedhwSwW_QchkzWfGAhAQ_003D_003D
	{
		[DllImport("kernel32.dll", EntryPoint = "LoadLibrary")]
		public static extern IntPtr _0023_003DqUgqfOCp6wgYcG0g3Bwqo7g_003D_003D(string _0023_003Dq4a0U7TLQjeoMc_0024wI1HR3_g_003D_003D);

		[DllImport("kernel32.dll", EntryPoint = "FreeLibrary")]
		public static extern bool _0023_003Dqptp0dqets4PLTJsAoRVcRg_003D_003D(IntPtr _0023_003DqzWcjJKNO5Elsze47dqt3Pg_003D_003D);

		[DllImport("kernel32.dll", EntryPoint = "GetProcAddress")]
		public static extern IntPtr _0023_003DqTTAP5lssI0r2ByF_0024TfH6ww_003D_003D(IntPtr _0023_003DquVd9eNRTo2vUaMJJi8T1_0024Q_003D_003D, string _0023_003Dqi1saQTsZlCsJHaNHhPmUPQ_003D_003D);
	}

	private static readonly string _0023_003Dq7WAeDxApLektd__S6C_00243FQ_003D_003D = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850819124);

	public static void _0023_003Dq4_DkR3jQySNADuVTan4YOQ_003D_003D()
	{
		AppDomain.CurrentDomain.UnhandledException += delegate(object _0023_003DqfKpKggO64L_0024kbHS1m3v6dg_003D_003D, UnhandledExceptionEventArgs _0023_003Dq4CUwdy1SiuqiwlPegcQF5Q_003D_003D)
		{
			Exception ex = (Exception)_0023_003Dq4CUwdy1SiuqiwlPegcQF5Q_003D_003D.ExceptionObject;
			string text = _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqYXvzZX6xs76BY_P35r3oc05OtbjtsmCDQ5b2hNGlsbs_003D.Trim() + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790083) + _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqWJ8JlmqWH6_WsDkbdfhtA9JonjkufbY7JlaXdJOayzg_003D.Trim() + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790083) + _0023_003DqoR7TJnUeEqZuS6tBW1EG0g_003D_003D().Trim();
			string text2 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790136), new object[1] { DateTime.Now });
			string path = Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790037), text2 + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790025));
			Directory.CreateDirectory(Path.GetDirectoryName(path));
			string text3 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790074), new object[4]
			{
				_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dqwn4hYQ_0024xzN2mdS8cLb5WLg_003D_003D,
				ex.Message,
				ex.StackTrace,
				text
			});
			File.WriteAllText(path, text3);
			string text4 = Path.Combine(Path.GetTempPath(), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790005));
			ZipFile zipFile = new ZipFile();
			try
			{
				zipFile.AddDirectory(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D);
				using FileStream outputStream = File.Create(text4);
				zipFile.Save(outputStream);
			}
			finally
			{
				((IDisposable)zipFile).Dispose();
			}
			string newValue = Convert.ToBase64String(File.ReadAllBytes(text4));
			string newValue2 = ((GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D == null) ? _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqWeeZ4lOiYOc_0024hd_B9oJJEs06lFNSEvtSt_qRYDhwYho_003D(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D, 18) : GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqfnmQQt3zoSvedPCGamLDZUurwc32sk5rZyIXFn7qauA_003D());
			string text5 = Path.Combine(Path.GetTempPath(), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789915));
			string contents = _0023_003Dq7WAeDxApLektd__S6C_00243FQ_003D_003D.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789890), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dqwn4hYQ_0024xzN2mdS8cLb5WLg_003D_003D).Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789929), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D).Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789835), newValue2)
				.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789875), text3)
				.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789785), text4)
				.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789762), newValue);
			File.WriteAllText(text5, contents);
			Process.Start(text5);
			Environment.Exit(1);
		};
	}

	private static void _0023_003DqXdnXcKxVi4_0024nQGaesYKR5g_003D_003D(object _0023_003DqfKpKggO64L_0024kbHS1m3v6dg_003D_003D, UnhandledExceptionEventArgs _0023_003Dq4CUwdy1SiuqiwlPegcQF5Q_003D_003D)
	{
		Exception ex = (Exception)_0023_003Dq4CUwdy1SiuqiwlPegcQF5Q_003D_003D.ExceptionObject;
		string text = _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqYXvzZX6xs76BY_P35r3oc05OtbjtsmCDQ5b2hNGlsbs_003D.Trim() + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790083) + _0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqWJ8JlmqWH6_WsDkbdfhtA9JonjkufbY7JlaXdJOayzg_003D.Trim() + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790083) + _0023_003DqoR7TJnUeEqZuS6tBW1EG0g_003D_003D().Trim();
		string text2 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790136), new object[1] { DateTime.Now });
		string path = Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790037), text2 + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790025));
		Directory.CreateDirectory(Path.GetDirectoryName(path));
		string text3 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790074), new object[4]
		{
			_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dqwn4hYQ_0024xzN2mdS8cLb5WLg_003D_003D,
			ex.Message,
			ex.StackTrace,
			text
		});
		File.WriteAllText(path, text3);
		string text4 = Path.Combine(Path.GetTempPath(), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850790005));
		ZipFile zipFile = new ZipFile();
		try
		{
			zipFile.AddDirectory(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D);
			using FileStream outputStream = File.Create(text4);
			zipFile.Save(outputStream);
		}
		finally
		{
			((IDisposable)zipFile).Dispose();
		}
		string newValue = Convert.ToBase64String(File.ReadAllBytes(text4));
		string newValue2 = ((GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D == null) ? _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqWeeZ4lOiYOc_0024hd_B9oJJEs06lFNSEvtSt_qRYDhwYho_003D(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D, 18) : GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqfnmQQt3zoSvedPCGamLDZUurwc32sk5rZyIXFn7qauA_003D());
		string text5 = Path.Combine(Path.GetTempPath(), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789915));
		string contents = _0023_003Dq7WAeDxApLektd__S6C_00243FQ_003D_003D.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789890), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dqwn4hYQ_0024xzN2mdS8cLb5WLg_003D_003D).Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789929), _0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D).Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789835), newValue2)
			.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789875), text3)
			.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789785), text4)
			.Replace(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789762), newValue);
		File.WriteAllText(text5, contents);
		Process.Start(text5);
		Environment.Exit(1);
	}

	private static string _0023_003DqoR7TJnUeEqZuS6tBW1EG0g_003D_003D()
	{
		StringBuilder stringBuilder = new StringBuilder(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789803));
		if (_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqVzZm0N_0024qll6yak949SnX_w_003D_003D == _0023_003DqGDf0dWN49qXN54qWfQi73JnNDfSmnxiZzNc5NQyhHxI_003D.Windows)
		{
			string[] array = new string[5]
			{
				_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789715),
				_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789699),
				_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789748),
				_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789731),
				_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789648)
			};
			foreach (string text in array)
			{
				string text2 = ((_0023_003DqqIedhwSwW_QchkzWfGAhAQ_003D_003D._0023_003DqUgqfOCp6wgYcG0g3Bwqo7g_003D_003D(text) != IntPtr.Zero) ? _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789680) : _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789689));
				stringBuilder.Append(_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789670), new object[2] { text, text2 }));
			}
		}
		else
		{
			stringBuilder.Append(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850789587));
		}
		return stringBuilder.ToString();
	}
}
