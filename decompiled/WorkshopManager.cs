using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using Steamworks;

public sealed class WorkshopManager
{
	private sealed class _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D : IEnumerator<Puzzle>, IEnumerable<Puzzle>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D;

		private Puzzle _0023_003DqvB2yVEkuuboSrqAYcWnJew_003D_003D;

		private int _0023_003Dqb6Q7nmCQJpHcGZZhVsPAgdCcHc2MyOfko09hvLfx_0024A0_003D;

		private string _0023_003Dq_0024IZjLgsJm2WiLocCWMnmBQ_003D_003D;

		public string _0023_003Dqxop_0024ycrmsLxoAfkvEN8dRqMf8qgWS_bYiDdTs762qVY_003D;

		public WorkshopManager _0023_003DqSHsvySg4sNibDc7ajXSNPw_003D_003D;

		private IEnumerator<string> _0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D;

		[DebuggerHidden]
		public _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D(int _0023_003DqhXEdUMqv2JeNZVAlXu0NIQ_003D_003D)
		{
			_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = _0023_003DqhXEdUMqv2JeNZVAlXu0NIQ_003D_003D;
			_0023_003Dqb6Q7nmCQJpHcGZZhVsPAgdCcHc2MyOfko09hvLfx_0024A0_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003Dq6pC6VwqU7A_0024ELSTrv1CG3VShYPu__0024dulzlEXbcDYz7Y_003D()
		{
			int num = _0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D;
			if (num == -3 || num == 1)
			{
				try
				{
				}
				finally
				{
					_0023_003DqnAihdMEtry3k2cKnM_UlHQ_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q6pC6VwqU7A$ELSTrv1CG3VShYPu_$dulzlEXbcDYz7Y=
			this._0023_003Dq6pC6VwqU7A_0024ELSTrv1CG3VShYPu__0024dulzlEXbcDYz7Y_003D();
		}

		private bool MoveNext()
		{
			try
			{
				int num = _0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D;
				WorkshopManager workshopManager = _0023_003DqSHsvySg4sNibDc7ajXSNPw_003D_003D;
				switch (num)
				{
				default:
					return false;
				case 0:
				{
					_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = -1;
					string path = Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003Dq_0024IZjLgsJm2WiLocCWMnmBQ_003D_003D);
					Directory.CreateDirectory(path);
					IEnumerable<string> enumerable = from _0023_003DqiQfgDdDfzj_0024bRt75sqtQHQ_003D_003D in Directory.EnumerateFiles(path, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681173))
						orderby File.GetCreationTimeUtc(_0023_003DqiQfgDdDfzj_0024bRt75sqtQHQ_003D_003D)
						select _0023_003DqiQfgDdDfzj_0024bRt75sqtQHQ_003D_003D;
					_0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D = enumerable.GetEnumerator();
					_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = -3;
					break;
				}
				case 1:
					_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = -3;
					break;
				}
				while (_0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D.MoveNext())
				{
					string current = _0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D.Current;
					Maybe<Puzzle> maybe = Puzzle._0023_003Dq9c_PshlBCwK_y71QcoZ1Eg_003D_003D(current);
					if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
					{
						maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqViRbgaU2sHVR4ckpVcNQAIj6LvNmJSXPB_0024Z4vX2tJ4s_003D = workshopManager._0023_003DqsgcBLsmpf_wnvYMB_wXNVs8h8UcY7QN6iXNMEDrElYM_003D(current);
						_0023_003DqvB2yVEkuuboSrqAYcWnJew_003D_003D = maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
						_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = 1;
						return true;
					}
				}
				_0023_003DqnAihdMEtry3k2cKnM_UlHQ_003D_003D();
				_0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D = null;
				return false;
			}
			catch
			{
				//try-fault
				_0023_003Dq6pC6VwqU7A_0024ELSTrv1CG3VShYPu__0024dulzlEXbcDYz7Y_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqnAihdMEtry3k2cKnM_UlHQ_003D_003D()
		{
			_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = -1;
			if (_0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D != null)
			{
				_0023_003DqHtR03gAdDtLtucQ_0024uXOkrQ_003D_003D.Dispose();
			}
		}

		[DebuggerHidden]
		private Puzzle _0023_003DqcKLozln9Te_kYtFwUMrx7q0qDcej5litJUNgOtBIH2CntJil0fNJuqThpyNpajxTB__0024dyJLg8HcrC3Z_0024KVJVNw_003D_003D()
		{
			return _0023_003DqvB2yVEkuuboSrqAYcWnJew_003D_003D;
		}

		Puzzle IEnumerator<Puzzle>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qcKLozln9Te_kYtFwUMrx7q0qDcej5litJUNgOtBIH2CntJil0fNJuqThpyNpajxTB_$dyJLg8HcrC3Z$KVJVNw==
			return this._0023_003DqcKLozln9Te_kYtFwUMrx7q0qDcej5litJUNgOtBIH2CntJil0fNJuqThpyNpajxTB__0024dyJLg8HcrC3Z_0024KVJVNw_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003DqQnyIKNYO5p0NQIWW22WPKQvoBjXKAyQydwqrzv18OjXxfwa5U0Sle9nUHOhoVPkd()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qQnyIKNYO5p0NQIWW22WPKQvoBjXKAyQydwqrzv18OjXxfwa5U0Sle9nUHOhoVPkd
			this._0023_003DqQnyIKNYO5p0NQIWW22WPKQvoBjXKAyQydwqrzv18OjXxfwa5U0Sle9nUHOhoVPkd();
		}

		[DebuggerHidden]
		private object _0023_003DqlptacT4fE3BKxicAvN_0024TwunYKuICq0IKDh3Ys9gCfCyMXo4ZLGPhkBOSlq05_0024mjf()
		{
			return _0023_003DqvB2yVEkuuboSrqAYcWnJew_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qlptacT4fE3BKxicAvN$TwunYKuICq0IKDh3Ys9gCfCyMXo4ZLGPhkBOSlq05$mjf
			return this._0023_003DqlptacT4fE3BKxicAvN_0024TwunYKuICq0IKDh3Ys9gCfCyMXo4ZLGPhkBOSlq05_0024mjf();
		}

		[DebuggerHidden]
		private IEnumerator<Puzzle> _0023_003DqK9Y9Chj2g2VyC2w_0024A8S8CMx4iIi8m_skmCVUnEvaE5qPxDcuh47KLpY_0024qEMFWKNLzge1bLCk2ExyxG15XoK_fA_003D_003D()
		{
			_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D;
			if (_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D == -2 && _0023_003Dqb6Q7nmCQJpHcGZZhVsPAgdCcHc2MyOfko09hvLfx_0024A0_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003DqZe6p0F9OB45ZQYZHhqP8hA_003D_003D = 0;
				_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D = this;
			}
			else
			{
				_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D = new _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D(0);
				_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D._0023_003DqSHsvySg4sNibDc7ajXSNPw_003D_003D = _0023_003DqSHsvySg4sNibDc7ajXSNPw_003D_003D;
			}
			_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D._0023_003Dq_0024IZjLgsJm2WiLocCWMnmBQ_003D_003D = _0023_003Dqxop_0024ycrmsLxoAfkvEN8dRqMf8qgWS_bYiDdTs762qVY_003D;
			return _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D;
		}

		IEnumerator<Puzzle> IEnumerable<Puzzle>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qK9Y9Chj2g2VyC2w$A8S8CMx4iIi8m_skmCVUnEvaE5qPxDcuh47KLpY$qEMFWKNLzge1bLCk2ExyxG15XoK_fA==
			return this._0023_003DqK9Y9Chj2g2VyC2w_0024A8S8CMx4iIi8m_skmCVUnEvaE5qPxDcuh47KLpY_0024qEMFWKNLzge1bLCk2ExyxG15XoK_fA_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003Dq_JJnOLx1Wq8c_0024ueuUsIwo8B08xUpSlOJJhKrUMuP7wBJuxDILau00O5CxhciXcli()
		{
			return _0023_003DqK9Y9Chj2g2VyC2w_0024A8S8CMx4iIi8m_skmCVUnEvaE5qPxDcuh47KLpY_0024qEMFWKNLzge1bLCk2ExyxG15XoK_fA_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q_JJnOLx1Wq8c$ueuUsIwo8B08xUpSlOJJhKrUMuP7wBJuxDILau00O5CxhciXcli
			return this._0023_003Dq_JJnOLx1Wq8c_0024ueuUsIwo8B08xUpSlOJJhKrUMuP7wBJuxDILau00O5CxhciXcli();
		}
	}

	private sealed class _0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D
	{
		public Puzzle _0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D;

		internal bool _0023_003DqMh9AKLfcLmrBHVRSXBef5P5bdMmtc2qfvOdyorTrU8M_003D(Puzzle _0023_003DqcAcUx9rt93lajSaujuXaUQ_003D_003D)
		{
			return _0023_003DqcAcUx9rt93lajSaujuXaUQ_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D == _0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D;
		}
	}

	private sealed class _0023_003Dq82H1lL67hheBUNlkV2RFBYfqWibLFz6G2COR47K11Xg_003D
	{
		public bool _0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D;

		public Vector2 _0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D;

		public float _0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D;

		internal RenderTargetHandle _0023_003DqKIDOOpidaLih6s9MpdY2m91_0024q49Ki1LEHzGaGDMSkBQ_003D(PuzzleInputOutput _0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D)
		{
			return Editor._0023_003Dq0qN0BYqxTQ16CED_0024eWcX9pRAuWvMrLTCVdu5U2FtG5g_003D(_0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D._0023_003DqtEJwWjfLoLTPDwDVzc5Cwg_003D_003D, _0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D, _0023_003DqDU6H4wGxojZBS5U5YN_002425w_003D_003D: false, _0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D, _0023_003Dqeajk3dEu_0024TA05vhtBudYzrlA0rD5G3MNPaAX0RDfZ04_003D: true, _0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D);
		}
	}

	private sealed class _0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D
	{
		public WorkshopManager _0023_003DqrAz8l1mH55Vg6mmgPGPtDw_003D_003D;

		public Puzzle _0023_003DqOmgxEI8nvUAcNehpmajMqg_003D_003D;

		internal void _0023_003DqwPZY8jonfHGPUP6yLc2yXbTqEljr4RmBmxwWplUXVRD6lnhdhK0qJ5FVF7BaENr0(CreateItemResult_t _0023_003DqWAAkWXsW5szWYoNsa3uenw_003D_003D, bool _0023_003DqOiqG4Ue7LFT_mt5fCy5V3A_003D_003D)
		{
			_0023_003DqrAz8l1mH55Vg6mmgPGPtDw_003D_003D._0023_003DqeNGzpjmEamdJMOfGfk4x3je5TYGBgTSR9_tQUQaH2gBjweifz20nTVel6lMkT94A(_0023_003DqWAAkWXsW5szWYoNsa3uenw_003D_003D, _0023_003DqOiqG4Ue7LFT_mt5fCy5V3A_003D_003D, _0023_003DqOmgxEI8nvUAcNehpmajMqg_003D_003D);
		}
	}

	private sealed class _0023_003DqPM5pKJy1UMWdiulvAbXi2b6AyDQYDKz9LMJzcqdlqWw_003D
	{
		public Maybe<Puzzle> _0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D;

		internal bool _0023_003Dq_JYkC8Zb4JVng4NNhpAs9_0024h0cONSuIclneOKd3Y6BVA_003D(Puzzle _0023_003Dq4JHZT0_YDrUnhgBVH2NvUw_003D_003D)
		{
			return _0023_003Dq4JHZT0_YDrUnhgBVH2NvUw_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D == _0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D;
		}
	}

	private sealed class _0023_003DqTrIZLc1X5ujgPesIDaQWQ_od2V9RFuQfBxm8B2PUZuY_003D
	{
		public WorkshopManager _0023_003Dqm59_2_0024ASy45UwNJ6mMpIRw_003D_003D;

		public Puzzle _0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D;

		public PublishedFileId_t _0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D;

		public string _0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D;

		public string _0023_003DqmusUFoIrQLvuOb_0024CWowF4Q_003D_003D;

		internal void _0023_003DqAsx914mFEDheC2PXpuX7Yhvk65czadyX0d763nOjI7QFGs_3QASfLL26BcsHC_0024KG(SubmitItemUpdateResult_t _0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D, bool _0023_003DqtiVEZIBURTm3ZKFW4heg_g_003D_003D)
		{
			_0023_003Dqm59_2_0024ASy45UwNJ6mMpIRw_003D_003D._0023_003DqAbx_0024JH8u9CstzrdqA7z7zrXKHIixtI3ENxQxf5su32gvzfNtb0oGjLnhPgMmvlmd(_0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D, _0023_003DqtiVEZIBURTm3ZKFW4heg_g_003D_003D, _0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D, _0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D, _0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D, _0023_003DqmusUFoIrQLvuOb_0024CWowF4Q_003D_003D);
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Action<Puzzle> _003C_003E9__15_0;

		public static Action<Puzzle> _003C_003E9__16_0;

		public static Func<string, DateTime> _003C_003E9__17_0;

		public static Func<PuzzleInputOutput[], bool, float, RenderTargetHandle[]> _003C_003E9__32_0;

		public static Func<RenderTargetHandle, int> _003C_003E9__32_3;

		public static Func<RenderTargetHandle, int> _003C_003E9__32_4;

		public static Func<RenderTargetHandle[], Vector2> _003C_003E9__32_1;

		public static Func<RenderTargetHandle, int> _003C_003E9__32_5;

		internal void _0023_003DqC8bYD3sd4seNY7SDsO4X_0024d1onetrHT6ps0a7CU8kIAY_003D(Puzzle _0023_003DqKtk9iuqc_0024ZUe9Gm1EZS14Q_003D_003D)
		{
			_0023_003DqKtk9iuqc_0024ZUe9Gm1EZS14Q_003D_003D._0023_003DqCxYBLxg2zRA4ckiRERT7Uw_003D_003D = true;
		}

		internal void _0023_003Dq_v8PZ8x345ZiDWVFDG2TkHW1l2UKsKG3cAMKKdvZHbA_003D(Puzzle _0023_003DqrMxt9_0024MFHfdizvOKiTZy5A_003D_003D)
		{
			_0023_003DqrMxt9_0024MFHfdizvOKiTZy5A_003D_003D._0023_003DqfFl7Xv8C4HNCe4mdPC_GIw_003D_003D = true;
		}

		internal DateTime _0023_003Dq0yzwFNF3bZJW7f9clpdwhsKedirhkDWgVVdYssYsR_0024shGc2aZvw4khq_0024qUKt1As3(string _0023_003DqiQfgDdDfzj_0024bRt75sqtQHQ_003D_003D)
		{
			return File.GetCreationTimeUtc(_0023_003DqiQfgDdDfzj_0024bRt75sqtQHQ_003D_003D);
		}

		internal RenderTargetHandle[] _0023_003Dqh8WxWghdTfQybTwvsyFjly_0024WzHMoaCNj4xrNvHTb6w9ChOWHVZ7b0mR8OfKilqZH(PuzzleInputOutput[] _0023_003DqP2k6nAjetuD0i0LTp5mNxA_003D_003D, bool _0023_003Dq9Lpgeb6xbIAHceGB613NDQ_003D_003D, float _0023_003DqJOa_0024Ta0m3gzI3rCazxOr2g_003D_003D)
		{
			_0023_003Dq82H1lL67hheBUNlkV2RFBYfqWibLFz6G2COR47K11Xg_003D CS_0024_003C_003E8__locals6 = new _0023_003Dq82H1lL67hheBUNlkV2RFBYfqWibLFz6G2COR47K11Xg_003D();
			CS_0024_003C_003E8__locals6._0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D = _0023_003Dq9Lpgeb6xbIAHceGB613NDQ_003D_003D;
			CS_0024_003C_003E8__locals6._0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D = _0023_003DqJOa_0024Ta0m3gzI3rCazxOr2g_003D_003D;
			CS_0024_003C_003E8__locals6._0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D = new Vector2(float.PositiveInfinity, float.PositiveInfinity);
			return _0023_003DqP2k6nAjetuD0i0LTp5mNxA_003D_003D.Select((PuzzleInputOutput _0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D) => Editor._0023_003Dq0qN0BYqxTQ16CED_0024eWcX9pRAuWvMrLTCVdu5U2FtG5g_003D(_0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D._0023_003DqtEJwWjfLoLTPDwDVzc5Cwg_003D_003D, CS_0024_003C_003E8__locals6._0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D, _0023_003DqDU6H4wGxojZBS5U5YN_002425w_003D_003D: false, CS_0024_003C_003E8__locals6._0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D, _0023_003Dqeajk3dEu_0024TA05vhtBudYzrlA0rD5G3MNPaAX0RDfZ04_003D: true, CS_0024_003C_003E8__locals6._0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D)).ToArray();
		}

		internal Vector2 _0023_003DqA7pELCb88TLtKIK_0024LutvNDuEBY7c2Duc2y1Xfota8ny2Vvn1dRls7pmh0l6btVkI(RenderTargetHandle[] _0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D)
		{
			return new Vector2(_0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Max((RenderTargetHandle _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D) => _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D._0023_003Dqbgi6PR5csucWEZb39Gq59A_003D_003D()), _0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Sum((RenderTargetHandle _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D) => _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D._0023_003DqRIZH7_0024MVKJkEqSc6NTmwIg_003D_003D()) + (_0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Length - 1) * -5);
		}

		internal int _0023_003DqY1CYGEfYc0XC_002421Y5dAQb_pAtnDHa7umx86jTpBCWe1amH2wOnTBj8WHtB_0024M8TnH(RenderTargetHandle _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D)
		{
			return _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D._0023_003Dqbgi6PR5csucWEZb39Gq59A_003D_003D();
		}

		internal int _0023_003DqS7GXoCEG9yIyXIZxqVvgygfsi3N9CLXZXeRHt4VSJuWzkkgW2uqY4AbG7z_0024KbLkc(RenderTargetHandle _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D)
		{
			return _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D._0023_003DqRIZH7_0024MVKJkEqSc6NTmwIg_003D_003D();
		}

		internal int _0023_003Dq2sf40reYkeHlKMjE40yUNKR87AMOEWBeBHGw7SR5fKF5MO1XThDSrN6l8nSweWqK(RenderTargetHandle _0023_003DqPZ0lGs_0024vIKrgCELlyfhvkA_003D_003D)
		{
			return _0023_003DqPZ0lGs_0024vIKrgCELlyfhvkA_003D_003D._0023_003DqRIZH7_0024MVKJkEqSc6NTmwIg_003D_003D();
		}
	}

	public List<Puzzle> _0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D = new List<Puzzle>();

	public List<Puzzle> _0023_003Dqlo28ETNuKLflhI_3L3MLcrdXsuenX54py9e3RdOH9v4_003D = new List<Puzzle>();

	private bool _0023_003DqM66us_XWZ0yi2jjvFgZ6NPmkUeJNjC9VPW_VNt__g41OPerODfWF55M7J7auOx3J;

	private Maybe<string> _0023_003DqjTRvrvnVAq0Msn91z3B1A6kgyeWVM2MUB7BXE9yLvaw_003D;

	public bool _0023_003DqhW2G1s4N6gZWEv4n2GMLhwCQ3oW19wd_0024PNeq656hAjA_003D()
	{
		return _0023_003DqM66us_XWZ0yi2jjvFgZ6NPmkUeJNjC9VPW_VNt__g41OPerODfWF55M7J7auOx3J;
	}

	private void _0023_003DqS7DUDwfwPP_0024d2siNo5XlTZc5yHBlr6JsmYYxY7OMQ4Y_003D(bool _0023_003Dqb32b5KQRJaJBL6Lv2vqx1A_003D_003D)
	{
		_0023_003DqM66us_XWZ0yi2jjvFgZ6NPmkUeJNjC9VPW_VNt__g41OPerODfWF55M7J7auOx3J = _0023_003Dqb32b5KQRJaJBL6Lv2vqx1A_003D_003D;
	}

	public Maybe<string> _0023_003DqT3nGhhoaadYOFnRu8JowUmmOTC5dZ33JALZvbHo0cCw_003D()
	{
		return _0023_003DqjTRvrvnVAq0Msn91z3B1A6kgyeWVM2MUB7BXE9yLvaw_003D;
	}

	private void _0023_003Dqqh9VZzA94MDzqXb9Pv5WBvh376V5q6dvNfcDknMlzBM_003D(Maybe<string> _0023_003DqcuINkA7dn86eUFin8_bTTA_003D_003D)
	{
		_0023_003DqjTRvrvnVAq0Msn91z3B1A6kgyeWVM2MUB7BXE9yLvaw_003D = _0023_003DqcuINkA7dn86eUFin8_bTTA_003D_003D;
	}

	public void _0023_003Dq2aEJi0F7tvc9NkkYsS0a4Q_003D_003D()
	{
		_0023_003DqH0l55RJpbqslJxi7FSR2WUCAPyNS_hDdKVuzdBLioZY_003D();
		_0023_003DqYUxqB94KBvzAfBoGtCIPq5tMZHyk7COovdkSiwxi1zg_003D();
		_0023_003Dq84kVXvKj3DHFQziVxkpyLjSKK6DQQKTBPC_0024Q1ewFSj8_003D();
	}

	public void _0023_003Dq0q_0024fidKj3nQZcCpbcF3SEA_003D_003D()
	{
		if (Steam._0023_003DqPvxGVUOvQO1LuvS4nX05xIIMrSrN6ENSc_0024_0024kiFneSP8_003D<ItemInstalled_t>().Any() || Steam._0023_003DqPvxGVUOvQO1LuvS4nX05xIIMrSrN6ENSc_0024_0024kiFneSP8_003D<DownloadItemResult_t>().Any() || Steam._0023_003DqPvxGVUOvQO1LuvS4nX05xIIMrSrN6ENSc_0024_0024kiFneSP8_003D<RemoteStoragePublishedFileSubscribed_t>().Any() || Steam._0023_003DqPvxGVUOvQO1LuvS4nX05xIIMrSrN6ENSc_0024_0024kiFneSP8_003D<RemoteStoragePublishedFileUnsubscribed_t>().Any())
		{
			_0023_003Dq84kVXvKj3DHFQziVxkpyLjSKK6DQQKTBPC_0024Q1ewFSj8_003D();
		}
	}

	private void _0023_003Dq84kVXvKj3DHFQziVxkpyLjSKK6DQQKTBPC_0024Q1ewFSj8_003D()
	{
		string text = Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681158));
		string[] array = Directory.EnumerateFiles(text).ToArray();
		for (int i = 0; i < array.Length; i++)
		{
			File.Delete(array[i]);
		}
		PublishedFileId_t[] array2 = new PublishedFileId_t[SteamUGC.GetNumSubscribedItems()];
		SteamUGC.GetSubscribedItems(array2, (uint)array2.Length);
		PublishedFileId_t[] array3 = array2;
		foreach (PublishedFileId_t nPublishedFileID in array3)
		{
			EItemState itemState = (EItemState)SteamUGC.GetItemState(nPublishedFileID);
			if ((itemState & EItemState.k_EItemStateInstalled) != EItemState.k_EItemStateInstalled || !SteamUGC.GetItemInstallInfo(nPublishedFileID, out var _, out var pchFolder, 4096u, out var _))
			{
				continue;
			}
			foreach (string item in Directory.EnumerateFiles(pchFolder))
			{
				string destFileName = Path.Combine(text, Path.GetFileName(item));
				File.Copy(item, destFileName);
			}
		}
		_0023_003DqH0l55RJpbqslJxi7FSR2WUCAPyNS_hDdKVuzdBLioZY_003D();
	}

	public void _0023_003Dqmvd4uR4udoya9Ia3s7ubFQ_003D_003D()
	{
		SteamFriends.ActivateGameOverlayToWebPage(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681207));
	}

	public void _0023_003DqH0l55RJpbqslJxi7FSR2WUCAPyNS_hDdKVuzdBLioZY_003D()
	{
		_0023_003Dqlo28ETNuKLflhI_3L3MLcrdXsuenX54py9e3RdOH9v4_003D.Clear();
		_0023_003Dqlo28ETNuKLflhI_3L3MLcrdXsuenX54py9e3RdOH9v4_003D.AddRange(_0023_003DqHVQqww82LY8EXR4uRKW5IpH2fu7eJMo24c_Kcjtozls_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681158)));
		_0023_003Dqlo28ETNuKLflhI_3L3MLcrdXsuenX54py9e3RdOH9v4_003D.ForEach(delegate(Puzzle _0023_003DqKtk9iuqc_0024ZUe9Gm1EZS14Q_003D_003D)
		{
			_0023_003DqKtk9iuqc_0024ZUe9Gm1EZS14Q_003D_003D._0023_003DqCxYBLxg2zRA4ckiRERT7Uw_003D_003D = true;
		});
		GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003Dq7CTjEDd77SFNH_jY5jn7Hw_003D_003D._0023_003DqjGRLpY90B6aEAI0dcpughIke2FjCzQEwNhf2DdtezVPy8kPZP0XrKqrXSpiO7pC_();
	}

	public void _0023_003DqYUxqB94KBvzAfBoGtCIPq5tMZHyk7COovdkSiwxi1zg_003D()
	{
		_0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D.Clear();
		_0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D.AddRange(_0023_003DqHVQqww82LY8EXR4uRKW5IpH2fu7eJMo24c_Kcjtozls_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681090)));
		_0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D.ForEach(_003C_003Ec._003C_003E9._0023_003Dq_v8PZ8x345ZiDWVFDG2TkHW1l2UKsKG3cAMKKdvZHbA_003D);
	}

	[IteratorStateMachine(typeof(_0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D))]
	private IEnumerable<Puzzle> _0023_003DqHVQqww82LY8EXR4uRKW5IpH2fu7eJMo24c_Kcjtozls_003D(string _0023_003DqB97tCJ_090FBBklbUwVPMA_003D_003D)
	{
		return new _0023_003Dq_9La6ulcS1FtTuDhb42h9fgiC64hwFZWOas8iVJld_0024g_003D(-2)
		{
			_0023_003DqSHsvySg4sNibDc7ajXSNPw_003D_003D = this,
			_0023_003Dqxop_0024ycrmsLxoAfkvEN8dRqMf8qgWS_bYiDdTs762qVY_003D = _0023_003DqB97tCJ_090FBBklbUwVPMA_003D_003D
		};
	}

	private string _0023_003Dqx7uuKJn5oHshpDZcEQhBbXooT9T_Cg_0024MO3aoq3aXjI8_003D(Puzzle _0023_003Dq13jOMLitJgisaBb66c1ozg_003D_003D)
	{
		return Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681090), _0023_003Dq13jOMLitJgisaBb66c1ozg_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681141));
	}

	private uint _0023_003DqsgcBLsmpf_wnvYMB_wXNVs8h8UcY7QN6iXNMEDrElYM_003D(string _0023_003DqssragScrqmYahv8iOxAZeg_003D_003D)
	{
		uint num = 17u;
		byte[] array = File.ReadAllBytes(_0023_003DqssragScrqmYahv8iOxAZeg_003D_003D);
		foreach (byte b in array)
		{
			num = num * 23 + b;
		}
		return num;
	}

	public Puzzle _0023_003DqS0zZrhNjfiogdLnOw4zi5gdq6xH5jSLLeSiP1ufNLrQ_003D()
	{
		_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D _0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D = new _0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D();
		_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D = new Puzzle();
		_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681127) + _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqWeeZ4lOiYOc_0024hd_B9oJJEs06lFNSEvtSt_qRYDhwYho_003D(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D, 15);
		_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D._0023_003Dq_0024n1PGWu2UmOjkvoCuI2uIg_003D_003D = _0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003Dq3y3ZI0jRezykg4Vq6zHxcg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681055), string.Empty)._0023_003DqUdODFoA79EG_0024o_0024um1qpWuQ_003D_003D());
		_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D._0023_003DqJ78SySKpfB4ScMkoo_0024Snxw_003D_003D = _0023_003Dq2SJ7nDnwdpwNXk9f3XmpdA_003D_003D.CoreTools;
		_0023_003DqL914h19lN2UMHqCI92hIZ_mYlopfLIn1ShD0s6IDMbY_003D(_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003Dq83yRDDj50KKnAOKBB15u9g_003D_003D);
		_0023_003DqYUxqB94KBvzAfBoGtCIPq5tMZHyk7COovdkSiwxi1zg_003D();
		return _0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D.Where(_0023_003Dq54P09diLi1AaY_NqGuBfjlmHcv_y2wg81g3EkBpwWt0_003D._0023_003DqMh9AKLfcLmrBHVRSXBef5P5bdMmtc2qfvOdyorTrU8M_003D).First();
	}

	public Maybe<Puzzle> _0023_003DqyjJUjjC5c9RCobuMuGX0icrl15dT5Ua_Xjop58A6BJc_003D(Puzzle _0023_003Dqme8I7XDS7jFOtDPZTg2WyQ_003D_003D)
	{
		_0023_003DqPM5pKJy1UMWdiulvAbXi2b6AyDQYDKz9LMJzcqdlqWw_003D CS_0024_003C_003E8__locals5 = new _0023_003DqPM5pKJy1UMWdiulvAbXi2b6AyDQYDKz9LMJzcqdlqWw_003D();
		CS_0024_003C_003E8__locals5._0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D = Puzzle._0023_003Dq9c_PshlBCwK_y71QcoZ1Eg_003D_003D(_0023_003Dqx7uuKJn5oHshpDZcEQhBbXooT9T_Cg_0024MO3aoq3aXjI8_003D(_0023_003Dqme8I7XDS7jFOtDPZTg2WyQ_003D_003D));
		if (CS_0024_003C_003E8__locals5._0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			CS_0024_003C_003E8__locals5._0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681127) + _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqWeeZ4lOiYOc_0024hd_B9oJJEs06lFNSEvtSt_qRYDhwYho_003D(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D, 15);
			_0023_003DqL914h19lN2UMHqCI92hIZ_mYlopfLIn1ShD0s6IDMbY_003D(CS_0024_003C_003E8__locals5._0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
			_0023_003DqYUxqB94KBvzAfBoGtCIPq5tMZHyk7COovdkSiwxi1zg_003D();
			return _0023_003DqtSb49UR2So5_0024yT3kZee0IQ_003D_003D.Where((Puzzle _0023_003Dq4JHZT0_YDrUnhgBVH2NvUw_003D_003D) => _0023_003Dq4JHZT0_YDrUnhgBVH2NvUw_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D == CS_0024_003C_003E8__locals5._0023_003DqVrg_9bt_00247jbb7eCojgMZKA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D).First();
		}
		return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
	}

	public void _0023_003DqL914h19lN2UMHqCI92hIZ_mYlopfLIn1ShD0s6IDMbY_003D(Puzzle _0023_003DqSlXcXae10PTZthKSE5U8PA_003D_003D)
	{
		string text = _0023_003Dqx7uuKJn5oHshpDZcEQhBbXooT9T_Cg_0024MO3aoq3aXjI8_003D(_0023_003DqSlXcXae10PTZthKSE5U8PA_003D_003D);
		_0023_003DqSlXcXae10PTZthKSE5U8PA_003D_003D._0023_003DqfFRymBe_0024enpn6gZtXeTjyg_003D_003D(text);
		_0023_003DqSlXcXae10PTZthKSE5U8PA_003D_003D._0023_003DqViRbgaU2sHVR4ckpVcNQAIj6LvNmJSXPB_0024Z4vX2tJ4s_003D = _0023_003DqsgcBLsmpf_wnvYMB_wXNVs8h8UcY7QN6iXNMEDrElYM_003D(text);
	}

	public void _0023_003DqKuM4pL_00249vthaHjOF6IuiwcsglLr8Kigv_RL9vw2UiYE_003D(Puzzle _0023_003DqR6nMqPMoo0dZaOniYe1kzA_003D_003D)
	{
		string text = _0023_003Dqx7uuKJn5oHshpDZcEQhBbXooT9T_Cg_0024MO3aoq3aXjI8_003D(_0023_003DqR6nMqPMoo0dZaOniYe1kzA_003D_003D);
		string text2 = Path.Combine(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqwAtfWCgAfC_2DxdxRCfZqQ_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681090), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831101), Path.GetFileName(text));
		Directory.CreateDirectory(Path.GetDirectoryName(text2));
		if (File.Exists(text2))
		{
			File.Delete(text2);
		}
		File.Move(text, text2);
		_0023_003DqYUxqB94KBvzAfBoGtCIPq5tMZHyk7COovdkSiwxi1zg_003D();
	}

	public bool _0023_003DqtEgYOsvYg5LJcglLj35K8_0024vsjB5W4ivgnQxeNO7FzwxaAjea_0024nhgUC9SvTdsGSSr(Puzzle _0023_003DqKHk90wcVvrcsCt5sP38UZg_003D_003D)
	{
		Maybe<uint> maybe = GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqkUkpgp6rFx59ZDh3JOFye1WnBb3BmbMPbv3ijnvXaYY_003D(_0023_003DqKHk90wcVvrcsCt5sP38UZg_003D_003D);
		if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D() == _0023_003DqKHk90wcVvrcsCt5sP38UZg_003D_003D._0023_003DqViRbgaU2sHVR4ckpVcNQAIj6LvNmJSXPB_0024Z4vX2tJ4s_003D;
		}
		return false;
	}

	public void _0023_003Dq0XVactwJ1Teu1Mj92W1Sd04ngB4R_wiFlBzogzF07w0_003D(Puzzle _0023_003DqLkae64el57uOkc85EAbgKA_003D_003D)
	{
		_0023_003DqS7DUDwfwPP_0024d2siNo5XlTZc5yHBlr6JsmYYxY7OMQ4Y_003D(_0023_003Dqb32b5KQRJaJBL6Lv2vqx1A_003D_003D: true);
		_0023_003Dqqh9VZzA94MDzqXb9Pv5WBvh376V5q6dvNfcDknMlzBM_003D(_0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D);
		_0023_003DqwBKWV_0024yK3Ff5Eau8BV0awwNTWrKNEgQSTU5DrehNpjs_003D(_0023_003DqLkae64el57uOkc85EAbgKA_003D_003D);
	}

	private void _0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(string _0023_003DqUwrFLrBEikQlaz_u0xKBpQ_003D_003D)
	{
		_0023_003Dqqh9VZzA94MDzqXb9Pv5WBvh376V5q6dvNfcDknMlzBM_003D(_0023_003DqUwrFLrBEikQlaz_u0xKBpQ_003D_003D);
		_0023_003DqS7DUDwfwPP_0024d2siNo5XlTZc5yHBlr6JsmYYxY7OMQ4Y_003D(_0023_003Dqb32b5KQRJaJBL6Lv2vqx1A_003D_003D: false);
	}

	public void _0023_003DqPRprj7DzsuORbcnv8zgNCDwKXqzaP4vb_0024FmgE_MEqC8_003D()
	{
		_0023_003Dqqh9VZzA94MDzqXb9Pv5WBvh376V5q6dvNfcDknMlzBM_003D(_0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D);
	}

	private void _0023_003DqwBKWV_0024yK3Ff5Eau8BV0awwNTWrKNEgQSTU5DrehNpjs_003D(Puzzle _0023_003Dq4QH_00248lMmwGt1eh2iDrHs8Q_003D_003D)
	{
		_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D _0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D = new _0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D();
		_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D._0023_003DqrAz8l1mH55Vg6mmgPGPtDw_003D_003D = this;
		_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D._0023_003DqOmgxEI8nvUAcNehpmajMqg_003D_003D = _0023_003Dq4QH_00248lMmwGt1eh2iDrHs8Q_003D_003D;
		Maybe<ulong> maybe = GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003Dq4nND6C2eLujmhFq_xCUunjB_0024z7fmjeHvYgZEJ63z1kQ_003D(_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D._0023_003DqOmgxEI8nvUAcNehpmajMqg_003D_003D);
		if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			_0023_003DqtMIdA_0024mizHiZGW0vcXSGqrddVguKhto1pMImbltb8mmwxuk6nW9GLlq454pS98Cz(_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D._0023_003DqOmgxEI8nvUAcNehpmajMqg_003D_003D, new PublishedFileId_t(maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()));
		}
		else
		{
			SteamUGC.CreateItem(_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqOAIznDa37FKt8d4vKREtaA_003D_003D, EWorkshopFileType.k_EWorkshopFileTypeFirst)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D<CreateItemResult_t>(_0023_003DqeinlLsh9L8hpM8TCLkatFvneMnqVfQ063MhFKVwxgWI_003D._0023_003DqwPZY8jonfHGPUP6yLc2yXbTqEljr4RmBmxwWplUXVRD6lnhdhK0qJ5FVF7BaENr0);
		}
	}

	private void _0023_003DqeNGzpjmEamdJMOfGfk4x3je5TYGBgTSR9_tQUQaH2gBjweifz20nTVel6lMkT94A(CreateItemResult_t _0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D, bool _0023_003DqDEwkX6qXKC5R2yIpmEbyNA_003D_003D, Puzzle _0023_003Dq_0024yFRJigyGdlk4KT08EGZow_003D_003D)
	{
		if (!_0023_003DqDEwkX6qXKC5R2yIpmEbyNA_003D_003D)
		{
			if (_0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_eResult == EResult.k_EResultOK)
			{
				GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003Dq_XJv6WjP7IAwwStpmnikkyONbnXEqO_0024WWOwdEsnVS9U_003D(_0023_003Dq_0024yFRJigyGdlk4KT08EGZow_003D_003D, _0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_nPublishedFileId.m_PublishedFileId);
				_0023_003DqtMIdA_0024mizHiZGW0vcXSGqrddVguKhto1pMImbltb8mmwxuk6nW9GLlq454pS98Cz(_0023_003Dq_0024yFRJigyGdlk4KT08EGZow_003D_003D, _0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_nPublishedFileId);
				return;
			}
			if (_0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_eResult == EResult.k_EResultInsufficientPrivilege)
			{
				_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850681027), string.Empty));
				return;
			}
			if (_0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_eResult == EResult.k_EResultTimeout)
			{
				_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680967), string.Empty));
				return;
			}
			if (_0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_eResult == EResult.k_EResultNotLoggedOn)
			{
				_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680921), string.Empty));
				return;
			}
			_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D((string)_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680938), string.Empty) + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680837) + (int)_0023_003DqDWt3LEdHiYoUNclN0JenCw_003D_003D.m_eResult + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680892));
		}
		else
		{
			_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680938), string.Empty));
		}
	}

	private void _0023_003DqtMIdA_0024mizHiZGW0vcXSGqrddVguKhto1pMImbltb8mmwxuk6nW9GLlq454pS98Cz(Puzzle _0023_003DqNIWglELsTHygCMwr5_HEFw_003D_003D, PublishedFileId_t _0023_003DqSff61xZda046wywWWoVyVQ_003D_003D)
	{
		_0023_003DqTrIZLc1X5ujgPesIDaQWQ_od2V9RFuQfBxm8B2PUZuY_003D CS_0024_003C_003E8__locals20 = new _0023_003DqTrIZLc1X5ujgPesIDaQWQ_od2V9RFuQfBxm8B2PUZuY_003D();
		CS_0024_003C_003E8__locals20._0023_003Dqm59_2_0024ASy45UwNJ6mMpIRw_003D_003D = this;
		CS_0024_003C_003E8__locals20._0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D = _0023_003DqNIWglELsTHygCMwr5_HEFw_003D_003D;
		CS_0024_003C_003E8__locals20._0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D = _0023_003DqSff61xZda046wywWWoVyVQ_003D_003D;
		UGCUpdateHandle_t handle = SteamUGC.StartItemUpdate(_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqOAIznDa37FKt8d4vKREtaA_003D_003D, CS_0024_003C_003E8__locals20._0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D);
		CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D = Path.GetTempFileName();
		File.Delete(CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D);
		Directory.CreateDirectory(CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D);
		string sourceFileName = _0023_003Dqx7uuKJn5oHshpDZcEQhBbXooT9T_Cg_0024MO3aoq3aXjI8_003D(CS_0024_003C_003E8__locals20._0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D);
		string destFileName = Path.Combine(CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D, string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680884), CS_0024_003C_003E8__locals20._0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D.m_PublishedFileId._0023_003DqJ48CPrMhBNnF2kaBaRm3RNPbduqs65u9_W3Mky02XoM_003D()));
		File.Copy(sourceFileName, destFileName);
		CS_0024_003C_003E8__locals20._0023_003DqmusUFoIrQLvuOb_0024CWowF4Q_003D_003D = _0023_003DqiGUR3ZSM5pOM0FAd7YI8vREGAf2rC_0024sWvCGfRTwM_uE_003D(CS_0024_003C_003E8__locals20._0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D);
		SteamUGC.SetItemTitle(handle, CS_0024_003C_003E8__locals20._0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D._0023_003Dq_0024n1PGWu2UmOjkvoCuI2uIg_003D_003D);
		SteamUGC.SetItemContent(handle, CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D);
		SteamUGC.SetItemPreview(handle, CS_0024_003C_003E8__locals20._0023_003DqmusUFoIrQLvuOb_0024CWowF4Q_003D_003D);
		SteamUGC.SubmitItemUpdate(handle, string.Empty)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D(delegate(SubmitItemUpdateResult_t _0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D, bool _0023_003DqtiVEZIBURTm3ZKFW4heg_g_003D_003D)
		{
			CS_0024_003C_003E8__locals20._0023_003Dqm59_2_0024ASy45UwNJ6mMpIRw_003D_003D._0023_003DqAbx_0024JH8u9CstzrdqA7z7zrXKHIixtI3ENxQxf5su32gvzfNtb0oGjLnhPgMmvlmd(_0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D, _0023_003DqtiVEZIBURTm3ZKFW4heg_g_003D_003D, CS_0024_003C_003E8__locals20._0023_003DqFaciibvQ9ceEBV1YAQGkWQ_003D_003D, CS_0024_003C_003E8__locals20._0023_003DqKgK1yq6omKGnorWKJfOSxA_003D_003D, CS_0024_003C_003E8__locals20._0023_003DqBwgM_0024hMYbyD8dLwWL9fCXA_003D_003D, CS_0024_003C_003E8__locals20._0023_003DqmusUFoIrQLvuOb_0024CWowF4Q_003D_003D);
		});
	}

	private void _0023_003DqAbx_0024JH8u9CstzrdqA7z7zrXKHIixtI3ENxQxf5su32gvzfNtb0oGjLnhPgMmvlmd(SubmitItemUpdateResult_t _0023_003DqPaDACYRmtKSXMMtnlnOjVA_003D_003D, bool _0023_003Dqus1BKIXG53M2StMJ01Vq0g_003D_003D, Puzzle _0023_003DqGDln7_0024rpkqs_0024EjF4fXgATQ_003D_003D, PublishedFileId_t _0023_003Dq1pfn_LWVph_0024OeUaaS1qv1A_003D_003D, string _0023_003Dq_0024oU1jJ_0024JZHvQvGK6zvx1wQ_003D_003D, string _0023_003Dql1I0Vpyudl2HuSZCeu0yMg_003D_003D)
	{
		if (!_0023_003Dqus1BKIXG53M2StMJ01Vq0g_003D_003D)
		{
			if (_0023_003DqPaDACYRmtKSXMMtnlnOjVA_003D_003D.m_eResult == EResult.k_EResultOK)
			{
				_0023_003DqS7DUDwfwPP_0024d2siNo5XlTZc5yHBlr6JsmYYxY7OMQ4Y_003D(_0023_003Dqb32b5KQRJaJBL6Lv2vqx1A_003D_003D: false);
				SteamFriends.ActivateGameOverlayToWebPage(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680866), _0023_003Dq1pfn_LWVph_0024OeUaaS1qv1A_003D_003D.m_PublishedFileId._0023_003DqJ48CPrMhBNnF2kaBaRm3RNPbduqs65u9_W3Mky02XoM_003D()));
			}
			else if (_0023_003DqPaDACYRmtKSXMMtnlnOjVA_003D_003D.m_eResult == EResult.k_EResultFileNotFound && GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003Dq4nND6C2eLujmhFq_xCUunjB_0024z7fmjeHvYgZEJ63z1kQ_003D(_0023_003DqGDln7_0024rpkqs_0024EjF4fXgATQ_003D_003D)._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
			{
				GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqFVPQl9XuVnuNyfYAUUpiThC5WCwEjx4f6GrbKBK_0024zhg_003D(_0023_003DqGDln7_0024rpkqs_0024EjF4fXgATQ_003D_003D);
				_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850678778), string.Empty));
			}
			else
			{
				GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqFVPQl9XuVnuNyfYAUUpiThC5WCwEjx4f6GrbKBK_0024zhg_003D(_0023_003DqGDln7_0024rpkqs_0024EjF4fXgATQ_003D_003D);
				_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D((string)_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680938), string.Empty) + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680837) + (int)_0023_003DqPaDACYRmtKSXMMtnlnOjVA_003D_003D.m_eResult + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680892));
			}
		}
		else
		{
			_0023_003DqtZBnavaY_0024ayYUWhA3sgdJg_003D_003D(_0023_003DqlfEvrNJFRsktTV9VbTbyJw_003D_003D._0023_003DqF_xxEpZJ6Y4Ql_0024DpzfJbpw_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850680938), string.Empty));
		}
		Directory.Delete(_0023_003Dq_0024oU1jJ_0024JZHvQvGK6zvx1wQ_003D_003D, recursive: true);
		File.Delete(_0023_003Dql1I0Vpyudl2HuSZCeu0yMg_003D_003D);
	}

	public static string _0023_003DqiGUR3ZSM5pOM0FAd7YI8vREGAf2rC_0024sWvCGfRTwM_uE_003D(Puzzle _0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D)
	{
		Vector2 vector = new Vector2(606f, 608f);
		Func<PuzzleInputOutput[], bool, float, RenderTargetHandle[]> func = delegate(PuzzleInputOutput[] _0023_003DqP2k6nAjetuD0i0LTp5mNxA_003D_003D, bool _0023_003Dq9Lpgeb6xbIAHceGB613NDQ_003D_003D, float _0023_003DqJOa_0024Ta0m3gzI3rCazxOr2g_003D_003D)
		{
			_0023_003Dq82H1lL67hheBUNlkV2RFBYfqWibLFz6G2COR47K11Xg_003D CS_0024_003C_003E8__locals6 = new _0023_003Dq82H1lL67hheBUNlkV2RFBYfqWibLFz6G2COR47K11Xg_003D();
			CS_0024_003C_003E8__locals6._0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D = _0023_003Dq9Lpgeb6xbIAHceGB613NDQ_003D_003D;
			CS_0024_003C_003E8__locals6._0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D = _0023_003DqJOa_0024Ta0m3gzI3rCazxOr2g_003D_003D;
			CS_0024_003C_003E8__locals6._0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D = new Vector2(float.PositiveInfinity, float.PositiveInfinity);
			return _0023_003DqP2k6nAjetuD0i0LTp5mNxA_003D_003D.Select((PuzzleInputOutput _0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D) => Editor._0023_003Dq0qN0BYqxTQ16CED_0024eWcX9pRAuWvMrLTCVdu5U2FtG5g_003D(_0023_003DqCEEftO3hFMduCqYbRPWj6A_003D_003D._0023_003DqtEJwWjfLoLTPDwDVzc5Cwg_003D_003D, CS_0024_003C_003E8__locals6._0023_003DquSbh8Hh5_PVF6rJMlGRwxQ_003D_003D, _0023_003DqDU6H4wGxojZBS5U5YN_002425w_003D_003D: false, CS_0024_003C_003E8__locals6._0023_003Dq2KDx2ldw9fRCcsVU6siTdw_003D_003D, _0023_003Dqeajk3dEu_0024TA05vhtBudYzrlA0rD5G3MNPaAX0RDfZ04_003D: true, CS_0024_003C_003E8__locals6._0023_003DqWg_0024QKVzoWIMDVyMiwxaOlQ_003D_003D)).ToArray();
		};
		Func<RenderTargetHandle[], Vector2> func2 = (RenderTargetHandle[] _0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D) => new Vector2(_0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Max((RenderTargetHandle _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D) => _0023_003DqAeDzNd4QT2_v37PfXcvj1Q_003D_003D._0023_003Dqbgi6PR5csucWEZb39Gq59A_003D_003D()), _0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Sum((RenderTargetHandle _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D) => _0023_003DqLl1FC2eHbu6hw6BAXUiYrw_003D_003D._0023_003DqRIZH7_0024MVKJkEqSc6NTmwIg_003D_003D()) + (_0023_003DqpS6Z1JZyGsnu_NRUzxX6rg_003D_003D.Length - 1) * -5);
		float num = 1f;
		string text;
		while (true)
		{
			text = Path.ChangeExtension(Path.GetTempFileName(), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850800837));
			RenderTargetHandle[] arg = func(_0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D._0023_003DqPRcMa9fT2PqyhM_oa9uBLQ_003D_003D, arg2: true, 1f);
			RenderTargetHandle[] arg2 = func(_0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D._0023_003DqL8YtTRKDYeskNKv78P2cKQ_003D_003D, arg2: false, 1f);
			Vector2 vector2 = func2(arg);
			Vector2 vector3 = func2(arg2);
			float num2 = Math.Min(1f, Math.Min(vector.X / vector2.X, vector.Y / vector2.Y));
			float num3 = Math.Min(1f, Math.Min(vector.X / vector3.X, vector.Y / vector3.Y));
			arg = func(_0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D._0023_003DqPRcMa9fT2PqyhM_oa9uBLQ_003D_003D, arg2: true, num2 * num);
			arg2 = func(_0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D._0023_003DqL8YtTRKDYeskNKv78P2cKQ_003D_003D, arg2: false, num3 * num);
			vector2 = func2(arg);
			vector3 = func2(arg2);
			Index2 index = new Index2(1366, 768);
			Matrix4 _0023_003DqZPrIqa6TssWrfgXjVGafpRpktIsdZmUW75_Oxg1R858_003D = Matrix4._0023_003Dq8gsJJucWPLnwqdS84Gdr3bsynrn3Jxx9djvZ67765xI_003D(index, !Renderer._0023_003DqbfIJeO_eHvK7Baklb986vcZbHcGvtARn9bP6J4ocF65AjMaHGYfihiZWpXBCEN2d());
			Matrix4 _0023_003Dqyqxo0JpWrJZeB4RZZI1KVg_003D_003D = Matrix4._0023_003DqOKFWpaX_3qACu_R1gqBsKg_003D_003D();
			RenderTargetHandle renderTargetHandle = new RenderTargetHandle(index);
			using (_0023_003Dq3Dio0w_DPg9nBxgbzTfa1XQlI_00245T3laoefco0OmT61I_003D._0023_003DqCSiKkE6THhc7vSD4rCeJ9w_003D_003D(renderTargetHandle._0023_003DqYiUxMaAEp74lMmzQ6EZr9g_003D_003D(), index, _0023_003DqZPrIqa6TssWrfgXjVGafpRpktIsdZmUW75_Oxg1R858_003D, _0023_003Dqyqxo0JpWrJZeB4RZZI1KVg_003D_003D))
			{
				_0023_003DqrFMJa74ctCqlhe_0024648yJNA_003D_003D._0023_003Dq89CIqqQys5ANdJd_GTRPHw_003D_003D(_0023_003Dq2UqcJSe2_00245N1HhpOyAz1Mg_003D_003D._0023_003Dqc50Z5wZTflISAZxdug3Jow_003D_003D._0023_003DqAbCNSNbdXhqZ1WyFV2thHQ_003D_003D._0023_003DqqBqp0B__00248fDKM07uuPyf6A_003D_003D, Vector2.Zero);
				for (int num4 = 0; num4 < 2; num4++)
				{
					RenderTargetHandle[] source = ((num4 == 0) ? arg : arg2);
					Vector2 vector4 = new Vector2((num4 == 0) ? 358 : 1010, 377f - ((num4 == 0) ? vector2.Y : vector3.Y) / 2f);
					foreach (RenderTargetHandle item in source.Reverse().OrderBy(_003C_003Ec._003C_003E9._0023_003Dq2sf40reYkeHlKMjE40yUNKR87AMOEWBeBHGw7SR5fKF5MO1XThDSrN6l8nSweWqK))
					{
						Vector2 vector5 = vector4 + new Vector2(-item._0023_003Dqbgi6PR5csucWEZb39Gq59A_003D_003D() / 2, 0f);
						_0023_003DqrFMJa74ctCqlhe_0024648yJNA_003D_003D._0023_003Dq89CIqqQys5ANdJd_GTRPHw_003D_003D(item._0023_003DqYiUxMaAEp74lMmzQ6EZr9g_003D_003D()._0023_003Dq3YtYdk9iB6CQgvN2ArCeEw_003D_003D, vector5.Rounded());
						vector4.Y += item._0023_003DqRIZH7_0024MVKJkEqSc6NTmwIg_003D_003D() + -5;
					}
				}
				_0023_003DqrFMJa74ctCqlhe_0024648yJNA_003D_003D._0023_003DqTchLnW87O9oWXu_cq9p4Rw_003D_003D(_0023_003DqsYDkoYKV6vKoLZW_0024D3ZJ2Q_003D_003D._0023_003Dq_0024n1PGWu2UmOjkvoCuI2uIg_003D_003D._0023_003DqUtYg_J_SnAPijAkdK6v5kA_003D_003D()._0023_003DqWNzk6lS_0024FsPV0TRkS0je0w_003D_003D(), new Vector2(683f, 720f), _0023_003Dq2UqcJSe2_00245N1HhpOyAz1Mg_003D_003D._0023_003DqFGK5IVGlLH2ZLT0aRvOJzA_003D_003D._0023_003Dq8qh4J3C62Ry58dQ9RH8zmA_003D_003D, Color.White, (_0023_003DqhzrWBSSw5Z2O6UlV3lLKaA_003D_003D)1, 1f, 0.6f, float.MaxValue, 1200f, -2, Color.Black, _0023_003Dq2UqcJSe2_00245N1HhpOyAz1Mg_003D_003D._0023_003Dqc50Z5wZTflISAZxdug3Jow_003D_003D._0023_003Dq0odZ2iOpjsN5zSLrKBmtDg_003D_003D._0023_003DqsEGNDKrvVYNpaqMRxNG9pA_003D_003D._0023_003Dq0Z6goeSE1IN0nxJX_aISrg_003D_003D, int.MaxValue, _0023_003Dq_0024CYGhHWRFyn5bVJfnVeESQ_003D_003D: false, _0023_003DqOnGZVoidYi6U0T8x5fRUfA_003D_003D: true);
			}
			Renderer._0023_003Dqm_0024iuH1nRiDrNq8kteZa3gw_003D_003D(renderTargetHandle._0023_003DqYiUxMaAEp74lMmzQ6EZr9g_003D_003D()._0023_003Dq3YtYdk9iB6CQgvN2ArCeEw_003D_003D)._0023_003DqCAiUDw5AlbkjxvWtxR4h8w_003D_003D(text);
			if (new FileInfo(text).Length < 1000000)
			{
				break;
			}
			num -= 0.1f;
		}
		return text;
	}
}
