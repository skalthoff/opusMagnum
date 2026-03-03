using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using Ionic.Zlib;
using Steamworks;

public sealed class ScoreManager
{
	private sealed class _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D : IEnumerator<string>, IEnumerable<string>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D;

		private string _0023_003DquTCEnkPESxZNRJXJDvdQdA_003D_003D;

		private int _0023_003DqZ8Iivuy4CxgOYUi3h77xyZl7u7KJ9k3l1jWfxgRd_nA_003D;

		public ScoreManager _0023_003Dqslsj71XqdUWR7AMe8YeXlg_003D_003D;

		private IEnumerator<Puzzle> _0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D;

		private Puzzle _0023_003DqfPlZcj2PmSRGuArVOeAjmA_003D_003D;

		private _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D[] _0023_003Dq3mLzuKlAZzuts44D_sTbCw_003D_003D;

		private int _0023_003DqfDyry7lP7OkqOJ5VG_ZXlw_003D_003D;

		[DebuggerHidden]
		public _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D(int _0023_003Dqtx9WZZvUVPy6kyHj9_0024zl3Q_003D_003D)
		{
			_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = _0023_003Dqtx9WZZvUVPy6kyHj9_0024zl3Q_003D_003D;
			_0023_003DqZ8Iivuy4CxgOYUi3h77xyZl7u7KJ9k3l1jWfxgRd_nA_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqGIQEeCloS7uIc8b9VffPyd7ePKnw1Ikjh_0024enf4ciRZY_003D()
		{
			int num = _0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D;
			if (num == -3 || num == 1)
			{
				try
				{
				}
				finally
				{
					_0023_003DqPoEAhpaZJMGhxTM3_b3LNA_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qGIQEeCloS7uIc8b9VffPyd7ePKnw1Ikjh$enf4ciRZY=
			this._0023_003DqGIQEeCloS7uIc8b9VffPyd7ePKnw1Ikjh_0024enf4ciRZY_003D();
		}

		private bool MoveNext()
		{
			try
			{
				int num = _0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D;
				ScoreManager scoreManager = _0023_003Dqslsj71XqdUWR7AMe8YeXlg_003D_003D;
				if (num != 0)
				{
					if (num != 1)
					{
						return false;
					}
					_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = -3;
					_0023_003DqfDyry7lP7OkqOJ5VG_ZXlw_003D_003D++;
					goto IL_00c8;
				}
				_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = -1;
				_0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D = Puzzles._0023_003DqnhlEx_8lWRS84VIwPrCbUF2ga28YfdgxbatefiyJl6M_003D.Concat(Puzzles._0023_003DqUtDWTpW46YfqF6sPsbruM7SiXoxFsm3CTiWNHyTUWuI_003D()).Concat(GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqP8MMPsTtOF8ma0H7Sn4BhEw9g6VKOkm3X0u8frQK7KQ_003D._0023_003Dqlo28ETNuKLflhI_3L3MLcrdXsuenX54py9e3RdOH9v4_003D).GetEnumerator();
				_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = -3;
				goto IL_00e6;
				IL_00c8:
				if (_0023_003DqfDyry7lP7OkqOJ5VG_ZXlw_003D_003D < _0023_003Dq3mLzuKlAZzuts44D_sTbCw_003D_003D.Length)
				{
					_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqkV8BMtuJpJ20o4eQBV8taQ_003D_003D = _0023_003Dq3mLzuKlAZzuts44D_sTbCw_003D_003D[_0023_003DqfDyry7lP7OkqOJ5VG_ZXlw_003D_003D];
					_0023_003DquTCEnkPESxZNRJXJDvdQdA_003D_003D = scoreManager._0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(_0023_003DqfPlZcj2PmSRGuArVOeAjmA_003D_003D, _0023_003DqkV8BMtuJpJ20o4eQBV8taQ_003D_003D);
					_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = 1;
					return true;
				}
				_0023_003Dq3mLzuKlAZzuts44D_sTbCw_003D_003D = null;
				_0023_003DqfPlZcj2PmSRGuArVOeAjmA_003D_003D = null;
				goto IL_00e6;
				IL_00e6:
				if (_0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D.MoveNext())
				{
					_0023_003DqfPlZcj2PmSRGuArVOeAjmA_003D_003D = _0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D.Current;
					_0023_003Dq3mLzuKlAZzuts44D_sTbCw_003D_003D = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
					_0023_003DqfDyry7lP7OkqOJ5VG_ZXlw_003D_003D = 0;
					goto IL_00c8;
				}
				_0023_003DqPoEAhpaZJMGhxTM3_b3LNA_003D_003D();
				_0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D = null;
				return false;
			}
			catch
			{
				//try-fault
				_0023_003DqGIQEeCloS7uIc8b9VffPyd7ePKnw1Ikjh_0024enf4ciRZY_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqPoEAhpaZJMGhxTM3_b3LNA_003D_003D()
		{
			_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = -1;
			if (_0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D != null)
			{
				_0023_003Dqxz4_0024ezQ0ApZJbjM6IZ7vFw_003D_003D.Dispose();
			}
		}

		[DebuggerHidden]
		private string _0023_003DqTyGGaQdaLEPduEv1W0zsZQ0CtQaI2zbCcMVxsHHjXd8Bqjw_0024cB42q6nn9p3HRHe3um1Y13L_002414Ghh42TeVD4B14WPBKSHsMlUjdc8hvwgfE_003D()
		{
			return _0023_003DquTCEnkPESxZNRJXJDvdQdA_003D_003D;
		}

		string IEnumerator<string>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qTyGGaQdaLEPduEv1W0zsZQ0CtQaI2zbCcMVxsHHjXd8Bqjw$cB42q6nn9p3HRHe3um1Y13L$14Ghh42TeVD4B14WPBKSHsMlUjdc8hvwgfE=
			return this._0023_003DqTyGGaQdaLEPduEv1W0zsZQ0CtQaI2zbCcMVxsHHjXd8Bqjw_0024cB42q6nn9p3HRHe3um1Y13L_002414Ghh42TeVD4B14WPBKSHsMlUjdc8hvwgfE_003D();
		}

		[DebuggerHidden]
		private void _0023_003Dq6DxLtNlO6Sgg0XPBpgSDkztEB4HyWo_csQC0Fkc5AkAoT3Vc3gmaLJLFt_KQAsfq()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q6DxLtNlO6Sgg0XPBpgSDkztEB4HyWo_csQC0Fkc5AkAoT3Vc3gmaLJLFt_KQAsfq
			this._0023_003Dq6DxLtNlO6Sgg0XPBpgSDkztEB4HyWo_csQC0Fkc5AkAoT3Vc3gmaLJLFt_KQAsfq();
		}

		[DebuggerHidden]
		private object _0023_003DqsHCayAcSvVw_00243gsASMg4KZ5u9V1nWdiOt5N_yRaUOsuNko6xGfVQYdAFljYNbx4r()
		{
			return _0023_003DquTCEnkPESxZNRJXJDvdQdA_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qsHCayAcSvVw$3gsASMg4KZ5u9V1nWdiOt5N_yRaUOsuNko6xGfVQYdAFljYNbx4r
			return this._0023_003DqsHCayAcSvVw_00243gsASMg4KZ5u9V1nWdiOt5N_yRaUOsuNko6xGfVQYdAFljYNbx4r();
		}

		[DebuggerHidden]
		private IEnumerator<string> _0023_003Dq15kOCU2aYOmgqg5KJigPGMopWpypK9ZAaGMm0tvKWxVqXXLSfrWsR_t9dOLpPwSYMLIBO9QeT0CwUpRtdn6TI7zq97BNhxNo2scvbc75iFc_003D()
		{
			_0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D;
			if (_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D == -2 && _0023_003DqZ8Iivuy4CxgOYUi3h77xyZl7u7KJ9k3l1jWfxgRd_nA_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003Dq4sD7kF8wJgtl4ueOOwB_0024ug_003D_003D = 0;
				_0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D = this;
			}
			else
			{
				_0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D = new _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D(0);
				_0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D._0023_003Dqslsj71XqdUWR7AMe8YeXlg_003D_003D = _0023_003Dqslsj71XqdUWR7AMe8YeXlg_003D_003D;
			}
			return _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D;
		}

		IEnumerator<string> IEnumerable<string>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q15kOCU2aYOmgqg5KJigPGMopWpypK9ZAaGMm0tvKWxVqXXLSfrWsR_t9dOLpPwSYMLIBO9QeT0CwUpRtdn6TI7zq97BNhxNo2scvbc75iFc=
			return this._0023_003Dq15kOCU2aYOmgqg5KJigPGMopWpypK9ZAaGMm0tvKWxVqXXLSfrWsR_t9dOLpPwSYMLIBO9QeT0CwUpRtdn6TI7zq97BNhxNo2scvbc75iFc_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003Dq1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2()
		{
			return _0023_003Dq15kOCU2aYOmgqg5KJigPGMopWpypK9ZAaGMm0tvKWxVqXXLSfrWsR_t9dOLpPwSYMLIBO9QeT0CwUpRtdn6TI7zq97BNhxNo2scvbc75iFc_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2
			return this._0023_003Dq1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2();
		}
	}

	private sealed class _0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D
	{
		public _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D _0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D;

		internal void _0023_003Dq3UOz0Vrn1WlJUQAUpnUnFjfV8akJStT0gctPJFsTe3c_003D(_0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D _0023_003Dq_HroJDCHKLNwcLokELmqpQ_003D_003D)
		{
			for (int i = 0; i < _0023_003Dq_HroJDCHKLNwcLokELmqpQ_003D_003D._0023_003DqiURNUIjBFRouwT9K61_uHQ_003D_003D.Count; i++)
			{
				if (_0023_003Dq_HroJDCHKLNwcLokELmqpQ_003D_003D._0023_003DqiURNUIjBFRouwT9K61_uHQ_003D_003D[i]._0023_003Dqq_002477eBAxZNiQ8h_0024mqxcdqg_003D_003D)
				{
					_0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqVJT4PQdR3AHKUBZ574ry2A_003D_003D = _0023_003Dq_HroJDCHKLNwcLokELmqpQ_003D_003D._0023_003DqiURNUIjBFRouwT9K61_uHQ_003D_003D[i]._0023_003DqIA36te09zn6JAmwxwDP2pw_003D_003D;
					break;
				}
			}
		}
	}

	private sealed class _0023_003DqrNFo_0024KdH_TO6amZK247hnSufbg3tlYtAXxb3gq_0024rg64_003D
	{
		public Dictionary<string, string> _0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D;

		internal void _0023_003DqQP33rngDfLOvjqgOXG0RRjwduuWamm7Qc3X8XaNOkCPqMbrFLpII97_0024vwtcpEM8g(string _0023_003DqhvejelnYsUqsneDjzQuY5g_003D_003D)
		{
			_0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D.Add(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831679), Convert.ToBase64String(File.ReadAllBytes(_0023_003DqhvejelnYsUqsneDjzQuY5g_003D_003D)));
		}
	}

	private sealed class _0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D
	{
		public ScoreManager _0023_003Dq01_0024dhcQspEkXvR_vKxTb_Q_003D_003D;

		public string _0023_003DqpIbaaVxJXipxqsRAwB_0024VES6vw_5EQxx_0024l8yotR5I6Bw_003D;

		internal void _0023_003Dqp_TiPYwUMrXs8DmILDuKAr8eRi9YLbeZSQELUpCnMWs_003D(LeaderboardScoreUploaded_t _0023_003DqFvkajS2O1ECiQMaF6AoaOA_003D_003D, bool _0023_003Dq_0024cpaPwOf1uPbUxH6OiI8pA_003D_003D)
		{
			_0023_003Dq01_0024dhcQspEkXvR_vKxTb_Q_003D_003D._0023_003Dq8Q5XI7e1Aaw0pVrbQ5YstHaBqB6svzNRLOcUTQY_WOU_003D(_0023_003DqpIbaaVxJXipxqsRAwB_0024VES6vw_5EQxx_0024l8yotR5I6Bw_003D);
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Action<byte[]> _003C_003E9__13_0;

		public static Action _003C_003E9__13_1;

		public static Func<string, string> _003C_003E9__16_2;

		public static Action _003C_003E9__16_1;

		public static Func<LeaderboardEntry, bool> _003C_003E9__21_0;

		public static Func<LeaderboardEntry, int> _003C_003E9__21_1;

		public static Func<string, int> _003C_003E9__26_1;

		public static Func<int, float> _003C_003E9__26_2;

		public static Func<string, string> _003C_003E9__27_0;

		internal void _0023_003DqvMpY8jK8hdCYfzlJycbKq2tzOfi8sjuEvNICB8mcNQw_003D(byte[] _0023_003Dq6OiDIRgeiv4CqZfIaWXBGw_003D_003D)
		{
		}

		internal void _0023_003DqoB1cema47lPd5FD5rPFOms382hjG0qCb8cGz4E_0024Teyw_003D()
		{
		}

		internal string _0023_003Dq2pd5ydVHF1WPeo7hcKpAy6Qfb6fQSelQabb_lKrBeSM_003D(string _0023_003DqS6V3zQev5jGoDeYEOciuGA_003D_003D)
		{
			return _0023_003DqS6V3zQev5jGoDeYEOciuGA_003D_003D.Trim();
		}

		internal void _0023_003Dq_0024Bd2kKiicHru7ENCC7bHjodJsnHVVY3atA6p_0024TB7Y64_003D()
		{
		}

		internal bool _0023_003DqS8T6YQWGuF1OwPFotBqhOOttGbp9NA09v_SREfdv3D1XvV3H1wWz9yLU3exN0RF_(LeaderboardEntry _0023_003DqJ5XjMyiuryrFUzjvlbaNrQ_003D_003D)
		{
			return !_0023_003DqJ5XjMyiuryrFUzjvlbaNrQ_003D_003D._0023_003Dqq_002477eBAxZNiQ8h_0024mqxcdqg_003D_003D;
		}

		internal int _0023_003DqwUgZYggQi3gXlCRJpQyfCNKKCjAvXxqKkQCIIQH2rIoEQP7eYLjuYY5J21ltRWRK(LeaderboardEntry _0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D)
		{
			return _0023_003DqtKqYqMAZ0mmrwD_0WPOTzA_003D_003D._0023_003DqIA36te09zn6JAmwxwDP2pw_003D_003D;
		}

		internal int _0023_003Dq3im30lWa99NVe8XyDL9uInkQF7K5aPI8V4ivfcbTOEk_003D(string _0023_003DqZnz0ZUILeIjA3KJWRUtXKw_003D_003D)
		{
			return int.Parse(_0023_003DqZnz0ZUILeIjA3KJWRUtXKw_003D_003D);
		}

		internal float _0023_003Dq1WbXDlCsYfTwPWvdYVBorDF7VVhizS7HUkHsDZ3VjWQ_003D(int _0023_003DqE8aXYk6Ffa1t2_0024f1FVUwGg_003D_003D)
		{
			return _0023_003DqE8aXYk6Ffa1t2_0024f1FVUwGg_003D_003D;
		}

		internal string _0023_003DqexVAvyAJCZcpoGAw5_0024sGaKLHWov1me98JpT4qoEa_0024suzNxaaHI3J2q2WhEv_VHW6(string _0023_003Dq_0024X_0024unu4Qis_0024_0024y0gt_cG8Fw_003D_003D)
		{
			return _0023_003Dq_0024X_0024unu4Qis_0024_0024y0gt_cG8Fw_003D_003D.Trim();
		}
	}

	public static readonly _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D[] _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D = new _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D[4]
	{
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Cycles,
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Cost,
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Footprint,
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Instructions
	};

	public static readonly int _0023_003DqP0lBOAKv9yYVfnKdWuE5dP7RJq8lLk_00244MSCgplNnsuk_003D = 6;

	private Dictionary<string, string> _0023_003DqQw7z2hzRJbs9h8L5zM2W7A_003D_003D = new Dictionary<string, string>();

	private Dictionary<string, _0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D> _0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D = new Dictionary<string, _0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D>();

	private Dictionary<string, int> _0023_003DqtcZwbKsz_gg_GbJfk6wfuaUTD_00240BAzhJY4oterokgEk_003D = new Dictionary<string, int>();

	private int _0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D;

	public bool _0023_003DqG_00249vDwl_0024EF2GUxaOTE05YmPVxr5HVNj5_0024gJGLikmyccZ3Rk9abmW1LgevTpl_9e6()
	{
		return _0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D > 0;
	}

	private static string _0023_003Dq_0024OzXXbGJKVpCBl09nubrYb0TOXsac9UmYVupctBs908_003D(string _0023_003DqCPtQXshyE1rM3rBTjbcZbw_003D_003D)
	{
		return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831669), new object[3]
		{
			_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqBiBmwQjWXF_0024vo1i8YTmAu_ex0Q99CIfzEAed8GMpfYc_003D,
			_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D,
			_0023_003DqCPtQXshyE1rM3rBTjbcZbw_003D_003D
		});
	}

	private static string _0023_003DqwvOU_T271beTEz_0024VMMsIWBIxVFn_0024j2Xyj9B1eJrvRIo_003D()
	{
		return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831580), new object[2]
		{
			_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqBiBmwQjWXF_0024vo1i8YTmAu_ex0Q99CIfzEAed8GMpfYc_003D,
			_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003Dq3GKXjjAfRRyMy790aR9YSA_003D_003D
		});
	}

	public void _0023_003DqM1KeEC5Bc27fwLfS5DEH2g_003D_003D()
	{
		_0023_003DqjGRLpY90B6aEAI0dcpughIke2FjCzQEwNhf2DdtezVPy8kPZP0XrKqrXSpiO7pC_();
	}

	public void _0023_003DqjGRLpY90B6aEAI0dcpughIke2FjCzQEwNhf2DdtezVPy8kPZP0XrKqrXSpiO7pC_()
	{
		_0023_003Dq7i7T_0024TnCCYtsGsjYUQMRiiKn6kWlVTyAEfhSW5gZZuY_003D();
		if (!_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqQopT4GnkGZVw6kE2V4K7WqGgFOiegM4WY6jnDR04ROI_003D)
		{
			return;
		}
		foreach (string item in _0023_003DqpI4d1_qKEZT2PovOLoDhe7u5rV4ZUg9Yx1Kq6WaQc3Y_003D())
		{
			_0023_003Dq8Q5XI7e1Aaw0pVrbQ5YstHaBqB6svzNRLOcUTQY_WOU_003D(item);
		}
	}

	public void _0023_003Dq7NNQmSSMZT0ep4pZA5jF5g_003D_003D(Solution _0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D, Dictionary<_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D, int> _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D, bool _0023_003DqgTQE6QJTPnIlWMNTCUqsRg_003D_003D)
	{
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D[] array = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
		foreach (_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2 in array)
		{
			if (_0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D.TryGetValue(_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2, out var value))
			{
				_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003DqWU34Z_6OK_0024X4Fx6r4Bs8pQ_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2] = value;
			}
			else
			{
				_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(_0023_003DqEAUzl2SAuL7SL8Q6djdntQ_003D_003D: false, string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831559), _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2));
			}
		}
		_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003DqLNHMQqWWb4weIWLao078gg_003D_003D();
		array = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
		foreach (_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D3 in array)
		{
			int _0023_003Dqoox52AzgsKtIHnj5_aL6Ng_003D_003D = Math.Min(_0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D3], GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqaSd0oiaoKLIPayaSsqe7Mg_003D_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D(), _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D3)._0023_003Dq3e1PtR_0024cLyGIxVVzJO8pbQ_003D_003D(int.MaxValue));
			GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003Dq4_0024_Bm_00243D5HyKZDj6ncOyJg_003D_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D(), _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D3, _0023_003Dqoox52AzgsKtIHnj5_aL6Ng_003D_003D);
		}
		if (_0023_003DqgTQE6QJTPnIlWMNTCUqsRg_003D_003D && !_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqfFl7Xv8C4HNCe4mdPC_GIw_003D_003D)
		{
			string _0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D = _0023_003Dq_0024OzXXbGJKVpCBl09nubrYb0TOXsac9UmYVupctBs908_003D(GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqfnmQQt3zoSvedPCGamLDZUurwc32sk5rZyIXFn7qauA_003D());
			Dictionary<string, string> dictionary = new Dictionary<string, string>();
			array = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
			foreach (_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D4 in array)
			{
				dictionary[_0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D(), _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D4)] = _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D4]._0023_003DqrOGVGXoZHE5Vju847DGT7xDvONJWW9J5MzlnON_0024ApXQ_003D();
			}
			GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqeXqtb1z02sln1SmzjUzp1g_003D_003D._0023_003DqSwSn_0024phqr8T4YqiCQYUFvA_003D_003D(_0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D, dictionary, _003C_003Ec._003C_003E9._0023_003DqvMpY8jK8hdCYfzlJycbKq2tzOfi8sjuEvNICB8mcNQw_003D, delegate
			{
			});
			array = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
			foreach (_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D5 in array)
			{
				_0023_003DqL7yjz1shnpGbUZ2WgttfU7DLeUKTfE9uWHDKn7KC3Rs_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D(), _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D5, _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D5]);
			}
			_0023_003Dq4UlPwJnDMhulKLZr33iVm49CMnJC_pgkY5tpHOLTB3o_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D, _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D);
			GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003Dqo_HUpZPHtmpEeCo_002413MMoQ_003D_003D._0023_003DqV5gJ3b6k1NLkOCphA3HKmg_003D_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D, _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Cycles], _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Cost], _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Footprint], _0023_003DqQhvn9YoCvuM9R_d2vLMfhA_003D_003D[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D.Instructions]);
		}
		if (_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqfFl7Xv8C4HNCe4mdPC_GIw_003D_003D)
		{
			GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqY_ELfN3IBj01IpOjj_HI3h_0024dA_XU9FjngHGyDpfj9kE_003D(_0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D(), _0023_003DquU8Mz0OVQfSQArEWJW7kYg_003D_003D._0023_003Dq9rTMVE4SxEcT30dZu1NK3w_003D_003D()._0023_003DqViRbgaU2sHVR4ckpVcNQAIj6LvNmJSXPB_0024Z4vX2tJ4s_003D);
		}
	}

	private string _0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(Puzzle _0023_003Dq9V8W4cIiFuBLJKba_0024341Tg_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqkV8BMtuJpJ20o4eQBV8taQ_003D_003D)
	{
		return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831590), new object[2]
		{
			_0023_003Dq9V8W4cIiFuBLJKba_0024341Tg_003D_003D._0023_003DqLO4yOtgYUaMxQYXi12r7Wg_003D_003D,
			(int)_0023_003DqkV8BMtuJpJ20o4eQBV8taQ_003D_003D
		});
	}

	[IteratorStateMachine(typeof(_0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D))]
	private IEnumerable<string> _0023_003DqpI4d1_qKEZT2PovOLoDhe7u5rV4ZUg9Yx1Kq6WaQc3Y_003D()
	{
		return new _0023_003DqERH9_WNDKRhVctCwa2BEAPvwGHdjGs2BIfcjxddRUlQ_003D(-2)
		{
			_0023_003Dqslsj71XqdUWR7AMe8YeXlg_003D_003D = this
		};
	}

	private void _0023_003Dq7i7T_0024TnCCYtsGsjYUQMRiiKn6kWlVTyAEfhSW5gZZuY_003D()
	{
		string _0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D = _0023_003DqwvOU_T271beTEz_0024VMMsIWBIxVFn_0024j2Xyj9B1eJrvRIo_003D();
		Dictionary<string, string> dictionary = new Dictionary<string, string>();
		foreach (string item in _0023_003DqpI4d1_qKEZT2PovOLoDhe7u5rV4ZUg9Yx1Kq6WaQc3Y_003D())
		{
			dictionary[item] = string.Empty;
		}
		GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqeXqtb1z02sln1SmzjUzp1g_003D_003D._0023_003DqSwSn_0024phqr8T4YqiCQYUFvA_003D_003D(_0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D, dictionary, delegate(byte[] _0023_003DqHTc63rAy0NH4S_0024E8g3D5Nw_003D_003D)
		{
			foreach (string item2 in ZlibStream.UncompressString(_0023_003DqHTc63rAy0NH4S_0024E8g3D5Nw_003D_003D).Split('\n').Select(_003C_003Ec._003C_003E9._0023_003Dq2pd5ydVHF1WPeo7hcKpAy6Qfb6fQSelQabb_lKrBeSM_003D))
			{
				string[] array = item2.Split(':');
				if (array.Length == 2)
				{
					_0023_003DqQw7z2hzRJbs9h8L5zM2W7A_003D_003D[array[0]] = array[1];
				}
			}
		}, delegate
		{
		});
	}

	private void _0023_003DqL7yjz1shnpGbUZ2WgttfU7DLeUKTfE9uWHDKn7KC3Rs_003D(Puzzle _0023_003DqXTgjRz7d4o8KPsmjjZqGDA_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqPGbJnNEJz1EVAXx0SmY7cw_003D_003D, int _0023_003DqMcrD8VF6BF0sHJ2sNrL4Xg_003D_003D)
	{
		_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D _0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D = new _0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D();
		_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D._0023_003Dq01_0024dhcQspEkXvR_vKxTb_Q_003D_003D = this;
		if (!GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqVNJd026yklBP0Fbn0JH3xw_003D_003D._0023_003DqdwjtHgk3PmTzvTQ90pJdwD590qQONNwtHBgpAFj_0024WtE_003D._0023_003DqlOhyUD18rP9og1gRBQY3eQ_003D_003D() && !_0023_003DqXTgjRz7d4o8KPsmjjZqGDA_003D_003D._0023_003DqfFl7Xv8C4HNCe4mdPC_GIw_003D_003D)
		{
			_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D._0023_003DqpIbaaVxJXipxqsRAwB_0024VES6vw_5EQxx_0024l8yotR5I6Bw_003D = _0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(_0023_003DqXTgjRz7d4o8KPsmjjZqGDA_003D_003D, _0023_003DqPGbJnNEJz1EVAXx0SmY7cw_003D_003D);
			if (_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D.ContainsKey(_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D._0023_003DqpIbaaVxJXipxqsRAwB_0024VES6vw_5EQxx_0024l8yotR5I6Bw_003D))
			{
				SteamUserStats.UploadLeaderboardScore(new SteamLeaderboard_t(_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D[_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D._0023_003DqpIbaaVxJXipxqsRAwB_0024VES6vw_5EQxx_0024l8yotR5I6Bw_003D]._0023_003DqyQG3QduK5FX1k4T6gWONug_003D_003D), ELeaderboardUploadScoreMethod.k_ELeaderboardUploadScoreMethodKeepBest, _0023_003DqMcrD8VF6BF0sHJ2sNrL4Xg_003D_003D, null, 0)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D<LeaderboardScoreUploaded_t>(_0023_003DqSMUjxk6S1Mfk6MRNZWnlewAleXhgwWcSMG6vqonJNR0_003D._0023_003Dqp_TiPYwUMrXs8DmILDuKAr8eRi9YLbeZSQELUpCnMWs_003D);
			}
		}
	}

	private void _0023_003Dq8Q5XI7e1Aaw0pVrbQ5YstHaBqB6svzNRLOcUTQY_WOU_003D(string _0023_003DqIHRjkrUYhuqowV4uckF8XMZefZqfGfvAtG6q4NZfX0I_003D)
	{
		SteamUserStats.FindOrCreateLeaderboard(_0023_003DqIHRjkrUYhuqowV4uckF8XMZefZqfGfvAtG6q4NZfX0I_003D, ELeaderboardSortMethod.k_ELeaderboardSortMethodAscending, ELeaderboardDisplayType.k_ELeaderboardDisplayTypeNumeric)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D(delegate(LeaderboardFindResult_t _0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D, bool _0023_003DqYmQnpKygtINgjF5eOVnxSA_003D_003D)
		{
			if (_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_bLeaderboardFound != 0 && !_0023_003DqYmQnpKygtINgjF5eOVnxSA_003D_003D)
			{
				string leaderboardName = SteamUserStats.GetLeaderboardName(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard);
				if (!_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D.ContainsKey(leaderboardName))
				{
					_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D[leaderboardName] = new _0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard.m_SteamLeaderboard);
				}
				int num = SteamUserStats.GetLeaderboardEntryCount(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard) / 100 + 1;
				SteamUserStats.DownloadLeaderboardEntries(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard, ELeaderboardDataRequest.k_ELeaderboardDataRequestGlobal, num, num)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D(delegate(LeaderboardScoresDownloaded_t _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D, bool _0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D)
				{
					if (!_0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D && _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_cEntryCount == 1)
					{
						SteamUserStats.GetDownloadedLeaderboardEntry(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboardEntries, 0, out var pLeaderboardEntry, null, 0);
						string leaderboardName2 = SteamUserStats.GetLeaderboardName(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboard);
						_0023_003DqtcZwbKsz_gg_GbJfk6wfuaUTD_00240BAzhJY4oterokgEk_003D[leaderboardName2] = pLeaderboardEntry.m_nScore;
					}
				});
				SteamUserStats.DownloadLeaderboardEntries(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard, ELeaderboardDataRequest.k_ELeaderboardDataRequestFriends, 0, 0)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D<LeaderboardScoresDownloaded_t>(_0023_003DqLHhnkW3tJNPKxuhw6LviXtXU6Pu9T2I2y_zKYQaDHOyksHyBOfb9vvq71kR8EZoR);
			}
		});
	}

	private void _0023_003DqkEq2EfV2iNVzq_0024GjJoD5h6XnHQvAl3_cczVqloyWAjA_003D(LeaderboardFindResult_t _0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D, bool _0023_003DqYmQnpKygtINgjF5eOVnxSA_003D_003D)
	{
		if (_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_bLeaderboardFound == 0 || _0023_003DqYmQnpKygtINgjF5eOVnxSA_003D_003D)
		{
			return;
		}
		string leaderboardName = SteamUserStats.GetLeaderboardName(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard);
		if (!_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D.ContainsKey(leaderboardName))
		{
			_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D[leaderboardName] = new _0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard.m_SteamLeaderboard);
		}
		int num = SteamUserStats.GetLeaderboardEntryCount(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard) / 100 + 1;
		SteamUserStats.DownloadLeaderboardEntries(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard, ELeaderboardDataRequest.k_ELeaderboardDataRequestGlobal, num, num)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D(delegate(LeaderboardScoresDownloaded_t _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D, bool _0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D)
		{
			if (!_0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D && _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_cEntryCount == 1)
			{
				SteamUserStats.GetDownloadedLeaderboardEntry(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboardEntries, 0, out var pLeaderboardEntry, null, 0);
				string leaderboardName2 = SteamUserStats.GetLeaderboardName(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboard);
				_0023_003DqtcZwbKsz_gg_GbJfk6wfuaUTD_00240BAzhJY4oterokgEk_003D[leaderboardName2] = pLeaderboardEntry.m_nScore;
			}
		});
		SteamUserStats.DownloadLeaderboardEntries(_0023_003Dqk3F9xJOUOa93_0024lyh5N1TsA_003D_003D.m_hSteamLeaderboard, ELeaderboardDataRequest.k_ELeaderboardDataRequestFriends, 0, 0)._0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D<LeaderboardScoresDownloaded_t>(_0023_003DqLHhnkW3tJNPKxuhw6LviXtXU6Pu9T2I2y_zKYQaDHOyksHyBOfb9vvq71kR8EZoR);
	}

	private void _0023_003Dq1oAiVXALaGYd3rR8meven_0024Ot_gpyzkbUi4ncEOf9Cipb_Mlear6icq_0024q3ceFHggQ(LeaderboardScoresDownloaded_t _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D, bool _0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D)
	{
		if (!_0023_003Dq0ndNucChlkDp81x65yYvQQ_003D_003D && _0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_cEntryCount == 1)
		{
			SteamUserStats.GetDownloadedLeaderboardEntry(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboardEntries, 0, out var pLeaderboardEntry, null, 0);
			string leaderboardName = SteamUserStats.GetLeaderboardName(_0023_003Dq01PeZat02jHsGL_ILdNP9g_003D_003D.m_hSteamLeaderboard);
			_0023_003DqtcZwbKsz_gg_GbJfk6wfuaUTD_00240BAzhJY4oterokgEk_003D[leaderboardName] = pLeaderboardEntry.m_nScore;
		}
	}

	private void _0023_003DqLHhnkW3tJNPKxuhw6LviXtXU6Pu9T2I2y_zKYQaDHOyksHyBOfb9vvq71kR8EZoR(LeaderboardScoresDownloaded_t _0023_003Dqnydu4ZZHw3VY04gQg_00243aPA_003D_003D, bool _0023_003DqgVZV9X07MrxvHtnNz4r_0024Nw_003D_003D)
	{
		if (!_0023_003DqgVZV9X07MrxvHtnNz4r_0024Nw_003D_003D)
		{
			List<LeaderboardEntry> list = new List<LeaderboardEntry>();
			for (int i = 0; i < _0023_003Dqnydu4ZZHw3VY04gQg_00243aPA_003D_003D.m_cEntryCount; i++)
			{
				SteamUserStats.GetDownloadedLeaderboardEntry(_0023_003Dqnydu4ZZHw3VY04gQg_00243aPA_003D_003D.m_hSteamLeaderboardEntries, i, out var pLeaderboardEntry, null, 0);
				list.Add(new LeaderboardEntry(SteamFriends.GetFriendPersonaName(pLeaderboardEntry.m_steamIDUser), pLeaderboardEntry.m_nScore, pLeaderboardEntry.m_steamIDUser == SteamUser.GetSteamID(), _0023_003DqSWVkY9dnC7BKENE95y625g_003D_003D: false));
			}
			list = list.OrderBy(_003C_003Ec._003C_003E9._0023_003DqS8T6YQWGuF1OwPFotBqhOOttGbp9NA09v_SREfdv3D1XvV3H1wWz9yLU3exN0RF_).OrderBy(_003C_003Ec._003C_003E9._0023_003DqwUgZYggQi3gXlCRJpQyfCNKKCjAvXxqKkQCIIQH2rIoEQP7eYLjuYY5J21ltRWRK).ToList();
			while (list.Count > _0023_003DqP0lBOAKv9yYVfnKdWuE5dP7RJq8lLk_00244MSCgplNnsuk_003D && !list[list.Count - 1]._0023_003Dqq_002477eBAxZNiQ8h_0024mqxcdqg_003D_003D)
			{
				list.RemoveAt(list.Count - 1);
			}
			while (list.Count > _0023_003DqP0lBOAKv9yYVfnKdWuE5dP7RJq8lLk_00244MSCgplNnsuk_003D)
			{
				list.RemoveAt(list.Count - 2);
			}
			string leaderboardName = SteamUserStats.GetLeaderboardName(_0023_003Dqnydu4ZZHw3VY04gQg_00243aPA_003D_003D.m_hSteamLeaderboard);
			_0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D[leaderboardName]._0023_003DqiURNUIjBFRouwT9K61_uHQ_003D_003D = list;
		}
	}

	public void _0023_003Dq7GYqB6kbP1_0024rsIML_yAfmXFRxkHHBEHdvwWCjjWheO4_003D(Puzzle _0023_003DqrJ6CwJNNVX_b72Sm5OtdFw_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqFAsEeZZzJ1l_XTyfxLJ4zw_003D_003D)
	{
		if (!_0023_003DqrJ6CwJNNVX_b72Sm5OtdFw_003D_003D._0023_003DqfFl7Xv8C4HNCe4mdPC_GIw_003D_003D)
		{
			_0023_003Dq8Q5XI7e1Aaw0pVrbQ5YstHaBqB6svzNRLOcUTQY_WOU_003D(_0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(_0023_003DqrJ6CwJNNVX_b72Sm5OtdFw_003D_003D, _0023_003DqFAsEeZZzJ1l_XTyfxLJ4zw_003D_003D));
		}
	}

	public Maybe<_0023_003DqlcxfSDwfgI9jiplez8BSOA_003D_003D> _0023_003DqnzHemgwhhYxJ2_zA9db4sEkbaWO5TP1Ql4cxRG7uiT0_003D(string _0023_003DqlwpsfJd1SNjzvCGyfq_POg_003D_003D)
	{
		return _0023_003Dq87UI_0024ln1Z13sEceCb4thwD40VSc_Kxwa4Ns1rljQTCI_003D._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(_0023_003DqlwpsfJd1SNjzvCGyfq_POg_003D_003D);
	}

	public Maybe<int> _0023_003DqgJznB1HL4QgxiEMyEYwrmCSbwbFclKh2sr3GZav_vmg_003D(string _0023_003DqhYcl2FIoZnlncxf9e5JsTQ_003D_003D)
	{
		return _0023_003DqtcZwbKsz_gg_GbJfk6wfuaUTD_00240BAzhJY4oterokgEk_003D._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(_0023_003DqhYcl2FIoZnlncxf9e5JsTQ_003D_003D);
	}

	public Dictionary<_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D, _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D> _0023_003Dqd_lK6nUBxrFUgQ7NCBCGOxj10WghhB1_SNR1SRELddk4NlOysmnA_0024yrfsvm29Ig0(Puzzle _0023_003DqvqdAegI5P_0024DP0DQe_00247qMjA_003D_003D, Maybe<Solution> _0023_003DqYAT_0024SV2d5CoghI9aE7DNKQ_003D_003D)
	{
		Dictionary<_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D, _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D> dictionary = new Dictionary<_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D, _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D>();
		_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D[] array = _0023_003DqdLZvqyDQMx22MRno2jhtWg_003D_003D;
		foreach (_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2 in array)
		{
			dictionary[_0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2] = _0023_003DqZfZn92QOJsO49U9Fe7d5sFODj64fK8_19WwMft3o4Wk_003D(_0023_003DqvqdAegI5P_0024DP0DQe_00247qMjA_003D_003D, _0023_003DqYAT_0024SV2d5CoghI9aE7DNKQ_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2);
			_0023_003Dq7GYqB6kbP1_0024rsIML_yAfmXFRxkHHBEHdvwWCjjWheO4_003D(_0023_003DqvqdAegI5P_0024DP0DQe_00247qMjA_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D2);
		}
		return dictionary;
	}

	private _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D _0023_003DqZfZn92QOJsO49U9Fe7d5sFODj64fK8_19WwMft3o4Wk_003D(Puzzle _0023_003DqqTzZszE1PcCe1ikx4ant0A_003D_003D, Maybe<Solution> _0023_003DqH1VXoYJ2xqIrz0H6drz31g_003D_003D, _0023_003DqnEvXdvc8ap3SryZEJXz2rg_003D_003D _0023_003DqFwUijQAnkL3_0024n8TDV1iP5Q_003D_003D)
	{
		_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D _0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D = new _0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D();
		_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D = new _0023_003DqZmQGV7NQgWz8hudSE3pGEw_003D_003D();
		_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqeKgFb9JSxLuKTvAq3UmCwQ_003D_003D = _0023_003DqFwUijQAnkL3_0024n8TDV1iP5Q_003D_003D;
		_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqrreEu9hrQzW7rf07xxxwWg_003D_003D = _0023_003DqPdoCJyuu4wVXLgS1XFNxyw_003D_003D(_0023_003DqqTzZszE1PcCe1ikx4ant0A_003D_003D, _0023_003DqFwUijQAnkL3_0024n8TDV1iP5Q_003D_003D);
		_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqHDw0YMr_0024_0024hItqf5LnvzG9Q_003D_003D = _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
		if (_0023_003DqH1VXoYJ2xqIrz0H6drz31g_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqnwpVAFx62BFkTVtfMQ3bOg_003D_003D = _0023_003DqH1VXoYJ2xqIrz0H6drz31g_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqWU34Z_6OK_0024X4Fx6r4Bs8pQ_003D_003D._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(_0023_003DqFwUijQAnkL3_0024n8TDV1iP5Q_003D_003D);
		}
		if (_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DqQopT4GnkGZVw6kE2V4K7WqGgFOiegM4WY6jnDR04ROI_003D)
		{
			_0023_003DqnzHemgwhhYxJ2_zA9db4sEkbaWO5TP1Ql4cxRG7uiT0_003D(_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqrreEu9hrQzW7rf07xxxwWg_003D_003D)._0023_003DqC9C214FH5q3i9m0bAC59zQ_003D_003D(_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dq3UOz0Vrn1WlJUQAUpnUnFjfV8akJStT0gctPJFsTe3c_003D);
		}
		else
		{
			_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqVJT4PQdR3AHKUBZ574ry2A_003D_003D = GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqSLfkENk39EmkqHxEzWjRSQ_003D_003D._0023_003DqaSd0oiaoKLIPayaSsqe7Mg_003D_003D(_0023_003DqqTzZszE1PcCe1ikx4ant0A_003D_003D, _0023_003DqFwUijQAnkL3_0024n8TDV1iP5Q_003D_003D);
		}
		try
		{
			if (_0023_003DqQw7z2hzRJbs9h8L5zM2W7A_003D_003D.TryGetValue(_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqrreEu9hrQzW7rf07xxxwWg_003D_003D, out var value))
			{
				int[] array = value.Split(',').Select(_003C_003Ec._003C_003E9._0023_003Dq3im30lWa99NVe8XyDL9uInkQF7K5aPI8V4ivfcbTOEk_003D).ToArray();
				if (array.Length >= 2)
				{
					List<float> list = array.Skip(1).Select(_003C_003Ec._003C_003E9._0023_003Dq1WbXDlCsYfTwPWvdYVBorDF7VVhizS7HUkHsDZ3VjWQ_003D).ToList();
					float num = list.Max();
					for (int i = 0; i < list.Count; i++)
					{
						list[i] /= num;
					}
					_0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D._0023_003DqHDw0YMr_0024_0024hItqf5LnvzG9Q_003D_003D = new _0023_003Dq0Usu4la6abcTcLsjVJiQhQ_003D_003D
					{
						_0023_003DqWyzGtdanvbnWShzt_0024R6XHg_003D_003D = array[0],
						_0023_003Dqt4_0024YuZvqaBqzWhdbxBicG8_5ZmqepUZYnG9l5qUx0Is_003D = list.ToArray()
					};
				}
			}
		}
		catch
		{
		}
		return _0023_003DqgQTHaHknJ7SPgLo_KXotNqIcv7txcUbAXmGviO6JpcI_003D._0023_003Dqf1iom8cVnoJLd21gs432Nw_003D_003D;
	}

	public void _0023_003Dq4UlPwJnDMhulKLZr33iVm49CMnJC_pgkY5tpHOLTB3o_003D(Solution _0023_003Dq45yDJHJDqCdYouOb0QT4Ew_003D_003D, Maybe<string> _0023_003Dqv9qYI9g631ZJ9JuhFTFRog_003D_003D)
	{
		if (GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqVNJd026yklBP0Fbn0JH3xw_003D_003D._0023_003DqdwjtHgk3PmTzvTQ90pJdwD590qQONNwtHBgpAFj_0024WtE_003D._0023_003DqlOhyUD18rP9og1gRBQY3eQ_003D_003D())
		{
			return;
		}
		foreach (string item in from _0023_003Dq_0024X_0024unu4Qis_0024_0024y0gt_cG8Fw_003D_003D in GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqVNJd026yklBP0Fbn0JH3xw_003D_003D._0023_003DqoxYlVGZG0Hcwc0g2kQVTq23y8xtpsnPnSnoW3CwDa34_003D._0023_003DqlOhyUD18rP9og1gRBQY3eQ_003D_003D().Split(',')
			select _0023_003Dq_0024X_0024unu4Qis_0024_0024y0gt_cG8Fw_003D_003D.Trim())
		{
			_0023_003DqrNFo_0024KdH_TO6amZK247hnSufbg3tlYtAXxb3gq_0024rg64_003D CS_0024_003C_003E8__locals4 = new _0023_003DqrNFo_0024KdH_TO6amZK247hnSufbg3tlYtAXxb3gq_0024rg64_003D();
			if (item.Length != 0)
			{
				string _0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D = item.TrimEnd('/') + (_0023_003Dqv9qYI9g631ZJ9JuhFTFRog_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D() ? _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831496) : _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831510));
				CS_0024_003C_003E8__locals4._0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D = new Dictionary<string, string>();
				CS_0024_003C_003E8__locals4._0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D.Add(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831544), Convert.ToBase64String(_0023_003Dq45yDJHJDqCdYouOb0QT4Ew_003D_003D._0023_003Dq67Lirx05LaE02PKnyY21XA_003D_003D()));
				_0023_003Dqv9qYI9g631ZJ9JuhFTFRog_003D_003D._0023_003DqC9C214FH5q3i9m0bAC59zQ_003D_003D(delegate(string _0023_003DqhvejelnYsUqsneDjzQuY5g_003D_003D)
				{
					CS_0024_003C_003E8__locals4._0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D.Add(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850831679), Convert.ToBase64String(File.ReadAllBytes(_0023_003DqhvejelnYsUqsneDjzQuY5g_003D_003D)));
				});
				_0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D++;
				GameLogic._0023_003DqL1tiTz9_0024QrhT_W7WpLrF4g_003D_003D._0023_003DqeXqtb1z02sln1SmzjUzp1g_003D_003D._0023_003DqSwSn_0024phqr8T4YqiCQYUFvA_003D_003D(_0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D, CS_0024_003C_003E8__locals4._0023_003Dqng4sMGPE_OG6CN6ICFIXNQ_003D_003D, delegate
				{
					_0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D--;
				}, delegate
				{
					_0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D--;
				});
			}
		}
	}

	private void _0023_003DqODZz_0024YvD1dh59_PIck5eG6SbcLGkP3J4WKgTe8rtoso_003D(byte[] _0023_003DqHTc63rAy0NH4S_0024E8g3D5Nw_003D_003D)
	{
		foreach (string item in ZlibStream.UncompressString(_0023_003DqHTc63rAy0NH4S_0024E8g3D5Nw_003D_003D).Split('\n').Select(_003C_003Ec._003C_003E9._0023_003Dq2pd5ydVHF1WPeo7hcKpAy6Qfb6fQSelQabb_lKrBeSM_003D))
		{
			string[] array = item.Split(':');
			if (array.Length == 2)
			{
				_0023_003DqQw7z2hzRJbs9h8L5zM2W7A_003D_003D[array[0]] = array[1];
			}
		}
	}

	private void _0023_003DqNHgo6oeQUfpfWemqBYwuXq7Slac_0024W3ElAviiL0P97qae8Axm1__6UzsQDG0Kfb_0024Z(byte[] _0023_003DqQbxNKWU5_0024yY_UIerDk09CQ_003D_003D)
	{
		_0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D--;
	}

	private void _0023_003DqOs5kmxs08EnkAGYxt1eMi9cStCZWPFZG9P_00248JCS_0024b5AsbEE4B_OMRHHXPGk4OXfr()
	{
		_0023_003DqQHoGj6E1pirCdAtBqYAWfMD_8VoyVY_XfUHaz7SAR9c_003D--;
	}
}
