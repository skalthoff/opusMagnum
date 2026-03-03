using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.CompilerServices;
using Steamworks;

public static class Steam
{
	private sealed class _0023_003DqTSgpA89o5Wa2nT1tT_0024Qbws5Rho_w1YFCMFAD2XvYm3Y_003D<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D> : IEnumerator<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D>, IEnumerable<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D>, IEnumerable, IEnumerator, IDisposable where _0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D : struct
	{
		private int _0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D;

		private _0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D _0023_003Dq6HhSmnOCSWITcStHoAw1GA_003D_003D;

		private int _0023_003DqAI7JZJN88ga9dEpco5f0vReIXmF0aS8bKRnaCc_rBwY_003D;

		private List<object>.Enumerator _0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D;

		[DebuggerHidden]
		public _0023_003DqTSgpA89o5Wa2nT1tT_0024Qbws5Rho_w1YFCMFAD2XvYm3Y_003D(int _0023_003DqGuHcYCpDQozs3TQ6eEKimQ_003D_003D)
		{
			_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = _0023_003DqGuHcYCpDQozs3TQ6eEKimQ_003D_003D;
			_0023_003DqAI7JZJN88ga9dEpco5f0vReIXmF0aS8bKRnaCc_rBwY_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqfdOl0S41luck2IpbTsY_0024Akj3zrmcZ92O3RWE_0024ZYLreQ_003D()
		{
			int num = _0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D;
			if (num == -3 || num == 1)
			{
				try
				{
				}
				finally
				{
					_0023_003DqCgU_BKlPy38bnZquKIT_jg_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qfdOl0S41luck2IpbTsY$Akj3zrmcZ92O3RWE$ZYLreQ=
			this._0023_003DqfdOl0S41luck2IpbTsY_0024Akj3zrmcZ92O3RWE_0024ZYLreQ_003D();
		}

		private bool MoveNext()
		{
			try
			{
				switch (_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D)
				{
				default:
					return false;
				case 0:
					_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = -1;
					_0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D = _0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.GetEnumerator();
					_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = -3;
					break;
				case 1:
					_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = -3;
					break;
				}
				while (_0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D.MoveNext())
				{
					_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D? val = _0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D.Current as _0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D?;
					if (val.HasValue)
					{
						_0023_003Dq6HhSmnOCSWITcStHoAw1GA_003D_003D = val.Value;
						_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = 1;
						return true;
					}
				}
				_0023_003DqCgU_BKlPy38bnZquKIT_jg_003D_003D();
				_0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D = default(List<object>.Enumerator);
				return false;
			}
			catch
			{
				//try-fault
				_0023_003DqfdOl0S41luck2IpbTsY_0024Akj3zrmcZ92O3RWE_0024ZYLreQ_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqCgU_BKlPy38bnZquKIT_jg_003D_003D()
		{
			_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = -1;
			((IDisposable)_0023_003Dq41aYOe9Sw_34xZRXGz0fWA_003D_003D/*cast due to .constrained prefix*/).Dispose();
		}

		[DebuggerHidden]
		private _0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D _0023_003DqsQZ447XlmHrZWkhPuwPx5_0024jSC6EaHGxDG9ShYF1IXeosFQqOV7_L0qs3_tK8VAz6M95n1xGA3DmUTiaMO3ZicQ_003D_003D()
		{
			return _0023_003Dq6HhSmnOCSWITcStHoAw1GA_003D_003D;
		}

		_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D IEnumerator<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qsQZ447XlmHrZWkhPuwPx5$jSC6EaHGxDG9ShYF1IXeosFQqOV7_L0qs3_tK8VAz6M95n1xGA3DmUTiaMO3ZicQ==
			return this._0023_003DqsQZ447XlmHrZWkhPuwPx5_0024jSC6EaHGxDG9ShYF1IXeosFQqOV7_L0qs3_tK8VAz6M95n1xGA3DmUTiaMO3ZicQ_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003Dqu7kl79B8inoYUAksqPk10cfyujCASnlPa2nyP0G3X2TMlhpRZLXMqS_v1cWsHZ8N()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qu7kl79B8inoYUAksqPk10cfyujCASnlPa2nyP0G3X2TMlhpRZLXMqS_v1cWsHZ8N
			this._0023_003Dqu7kl79B8inoYUAksqPk10cfyujCASnlPa2nyP0G3X2TMlhpRZLXMqS_v1cWsHZ8N();
		}

		[DebuggerHidden]
		private object _0023_003DqvtSrN7RlT3D7Mvb4Mu6EOojA9EScaSI_0024Ulu6CP4gFSilpBKC68oSI0WEyo7__0024ZL1()
		{
			return _0023_003Dq6HhSmnOCSWITcStHoAw1GA_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qvtSrN7RlT3D7Mvb4Mu6EOojA9EScaSI$Ulu6CP4gFSilpBKC68oSI0WEyo7_$ZL1
			return this._0023_003DqvtSrN7RlT3D7Mvb4Mu6EOojA9EScaSI_0024Ulu6CP4gFSilpBKC68oSI0WEyo7__0024ZL1();
		}

		[DebuggerHidden]
		private IEnumerator<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D> _0023_003DqnKuu_zLNO2Ry1E_wwu7Q25IPWKiDiqXD7GxIIEBOKqKsRXOL9_Cysr5maeQKRKTScO0eXhjNXz0S5iqzuztxAg_003D_003D()
		{
			if (_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D == -2 && _0023_003DqAI7JZJN88ga9dEpco5f0vReIXmF0aS8bKRnaCc_rBwY_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003DqwN4vyBcpZ_0024SKQ7mH_ICCsw_003D_003D = 0;
				return this;
			}
			return new _0023_003DqTSgpA89o5Wa2nT1tT_0024Qbws5Rho_w1YFCMFAD2XvYm3Y_003D<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D>(0);
		}

		IEnumerator<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D> IEnumerable<_0023_003DqdNDu_0024gkLq1zbw4qP_aoGNw_003D_003D>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qnKuu_zLNO2Ry1E_wwu7Q25IPWKiDiqXD7GxIIEBOKqKsRXOL9_Cysr5maeQKRKTScO0eXhjNXz0S5iqzuztxAg==
			return this._0023_003DqnKuu_zLNO2Ry1E_wwu7Q25IPWKiDiqXD7GxIIEBOKqKsRXOL9_Cysr5maeQKRKTScO0eXhjNXz0S5iqzuztxAg_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003DqJivF3icGtCBWqPcIfOsj6qa7n7sHzcVBQw1plBvuE8qiDSM7RkFyyKDkEhXpS1p3()
		{
			return _0023_003DqnKuu_zLNO2Ry1E_wwu7Q25IPWKiDiqXD7GxIIEBOKqKsRXOL9_Cysr5maeQKRKTScO0eXhjNXz0S5iqzuztxAg_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qJivF3icGtCBWqPcIfOsj6qa7n7sHzcVBQw1plBvuE8qiDSM7RkFyyKDkEhXpS1p3
			return this._0023_003DqJivF3icGtCBWqPcIfOsj6qa7n7sHzcVBQw1plBvuE8qiDSM7RkFyyKDkEhXpS1p3();
		}
	}

	private sealed class _0023_003DqUT5TW7IxQT3UREPtdDH3QcB_0024A8sQo0Kwa4zA364wmgU_003D<_0023_003DqDlP4YH462uBARVxCn5bKAQ_003D_003D>
	{
		public CallResult<_0023_003DqDlP4YH462uBARVxCn5bKAQ_003D_003D> _0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D;

		public CallResult<_0023_003DqDlP4YH462uBARVxCn5bKAQ_003D_003D>.APIDispatchDelegate _0023_003DqxioqV_0024m1FV0oBISsroGQbA_003D_003D;

		internal void _0023_003DqA0YDSzB25uqVrvD4aQvXIDkwvxNR_0024tGBZL7Q28ZJT9A_003D(_0023_003DqDlP4YH462uBARVxCn5bKAQ_003D_003D _0023_003Dq66_2k5llSka_Ap_rZ8P2Xw_003D_003D, bool _0023_003Dqh6SIhRFZ4vwmmvCHuBeRzw_003D_003D)
		{
			_0023_003DqxHFi5vQ5Sj0AzjZwaM10VQ_003D_003D.Remove(_0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D);
			_0023_003DqxioqV_0024m1FV0oBISsroGQbA_003D_003D(_0023_003Dq66_2k5llSka_Ap_rZ8P2Xw_003D_003D, _0023_003Dqh6SIhRFZ4vwmmvCHuBeRzw_003D_003D);
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Callback<LobbyDataUpdate_t>.DispatchDelegate _003C_003E9__11_0;

		public static Callback<LobbyChatUpdate_t>.DispatchDelegate _003C_003E9__11_1;

		public static Callback<GameLobbyJoinRequested_t>.DispatchDelegate _003C_003E9__11_2;

		public static Callback<GameOverlayActivated_t>.DispatchDelegate _003C_003E9__11_3;

		public static Callback<P2PSessionRequest_t>.DispatchDelegate _003C_003E9__11_4;

		public static Callback<ItemInstalled_t>.DispatchDelegate _003C_003E9__11_5;

		public static Callback<DownloadItemResult_t>.DispatchDelegate _003C_003E9__11_6;

		public static Callback<RemoteStoragePublishedFileSubscribed_t>.DispatchDelegate _003C_003E9__11_7;

		public static Callback<RemoteStoragePublishedFileUnsubscribed_t>.DispatchDelegate _003C_003E9__11_8;

		internal void _0023_003Dq_bVf4B7yyWnCf0_00245q_A8bIJwjbuAbYOSfVBrZX_0024ILvI_003D(LobbyDataUpdate_t _0023_003DqyBqhkXGPqCLKDou_0024KmReaA_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqyBqhkXGPqCLKDou_0024KmReaA_003D_003D);
		}

		internal void _0023_003DqWV1muz4KQS4_0024AspJkMQhffsUooGCIpFbMl2mW2nLE9o_003D(LobbyChatUpdate_t _0023_003DqjvNr_v6Ve1BspeLuJrDQ1Q_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqjvNr_v6Ve1BspeLuJrDQ1Q_003D_003D);
		}

		internal void _0023_003DqBullC1dARiGdxMrseb_oEYy2FXsGVOnoXmkeE1HDJJ8_003D(GameLobbyJoinRequested_t _0023_003DqCmk_00241bQkEqIEfoOO1MLGfw_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqCmk_00241bQkEqIEfoOO1MLGfw_003D_003D);
		}

		internal void _0023_003DqMvyR5NqF3R54kyvNZNJCvkH5SlxSXDQDk2Jmii2IrhM_003D(GameOverlayActivated_t _0023_003DqZJjTSQ6HrYYq4UvEfxk0zQ_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqZJjTSQ6HrYYq4UvEfxk0zQ_003D_003D);
		}

		internal void _0023_003DqzeInG0OeNBNLoWZXHKt3zjZVdL_fNLppE4sAYIVudhg_003D(P2PSessionRequest_t _0023_003DqZJjTSQ6HrYYq4UvEfxk0zQ_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqZJjTSQ6HrYYq4UvEfxk0zQ_003D_003D);
		}

		internal void _0023_003DqKpuKgFW_0024rmnj_FPQqmY0AG5FkFa8bJHOI4hck04YNb4_003D(ItemInstalled_t _0023_003Dq9Qv_qzE4pEz0oMmzxWOJ1g_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003Dq9Qv_qzE4pEz0oMmzxWOJ1g_003D_003D);
		}

		internal void _0023_003Dq1cfjZHITZcQFWcc8pa1_lcXnNGfw87ObwIIB2j_0024FpdE_003D(DownloadItemResult_t _0023_003DqMZXsSRMTEP_04B6NHikTew_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqMZXsSRMTEP_04B6NHikTew_003D_003D);
		}

		internal void _0023_003Dqr87dXNzE7pZaIDxmGgtbxQzQF226hjIyVQFwqdSuBg4_003D(RemoteStoragePublishedFileSubscribed_t _0023_003DqztWhYpg6i6KoV0B09zrR4A_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqztWhYpg6i6KoV0B09zrR4A_003D_003D);
		}

		internal void _0023_003DqhzzQLet7M_Tj4punkybbCZrCi8tWL64Uv_00246dnjNRHa8_003D(RemoteStoragePublishedFileUnsubscribed_t _0023_003Dq2vxtXP1D5xH9JJm_cPC4Nw_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003Dq2vxtXP1D5xH9JJm_cPC4Nw_003D_003D);
		}
	}

	private static Callback<LobbyDataUpdate_t> _0023_003DqqEdJ726XyI1_0024B8B2QA_00246oQC1o7x_7o9mTQA5h8QS_0024Uw_003D;

	private static Callback<LobbyChatUpdate_t> _0023_003Dqu0WCW6EDbkmefB2Izknn7ivE16ZrLgUS9x1dh3Vmw2Y_003D;

	private static Callback<GameLobbyJoinRequested_t> _0023_003DqS1UOcRTBGS0l_0024WpKrXetaMIk0lCEWVx_00243MPG4x1d_yQ_003D;

	private static Callback<GameOverlayActivated_t> _0023_003DqAu4Nm1ZFNvX0iwrIRdm6yqNRYnhJ77zoo2C0WlKrss0_003D;

	private static Callback<P2PSessionRequest_t> _0023_003DqoD3LueY0_0024isltLiBK_YFXrtPdF7ZHiI8lNr6XsSbq_0024w_003D;

	private static Callback<ItemInstalled_t> _0023_003DqJTA0hYZ0tpyAXVU_D7Ig9MTSKxwmpEv9k4q9aeGC1jw_003D;

	private static Callback<DownloadItemResult_t> _0023_003DqK17I1kgHTPZZzHjMiDNAlbfZFgrTIFM6lCB_00249QMP_0024K8_003D;

	private static Callback<RemoteStoragePublishedFileSubscribed_t> _0023_003Dq2lUsA132_PKQ_mSh_ketIML9imSix55HMgxE0j8Hhe0_003D;

	private static Callback<RemoteStoragePublishedFileUnsubscribed_t> _0023_003DqiryUSgft7CIYxdhq_JDHSvKAEsFIsB7mHQholNSAUio_003D;

	private static List<object> _0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D = new List<object>();

	private static List<object> _0023_003DqxHFi5vQ5Sj0AzjZwaM10VQ_003D_003D = new List<object>();

	public static void _0023_003DqN_zwltLfAjemzK7tNl2ZRA_003D_003D()
	{
		_0023_003DqqEdJ726XyI1_0024B8B2QA_00246oQC1o7x_7o9mTQA5h8QS_0024Uw_003D = Callback<LobbyDataUpdate_t>.Create(delegate(LobbyDataUpdate_t _0023_003DqyBqhkXGPqCLKDou_0024KmReaA_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqyBqhkXGPqCLKDou_0024KmReaA_003D_003D);
		});
		_0023_003Dqu0WCW6EDbkmefB2Izknn7ivE16ZrLgUS9x1dh3Vmw2Y_003D = Callback<LobbyChatUpdate_t>.Create(delegate(LobbyChatUpdate_t _0023_003DqjvNr_v6Ve1BspeLuJrDQ1Q_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqjvNr_v6Ve1BspeLuJrDQ1Q_003D_003D);
		});
		_0023_003DqS1UOcRTBGS0l_0024WpKrXetaMIk0lCEWVx_00243MPG4x1d_yQ_003D = Callback<GameLobbyJoinRequested_t>.Create(_003C_003Ec._003C_003E9._0023_003DqBullC1dARiGdxMrseb_oEYy2FXsGVOnoXmkeE1HDJJ8_003D);
		_0023_003DqAu4Nm1ZFNvX0iwrIRdm6yqNRYnhJ77zoo2C0WlKrss0_003D = Callback<GameOverlayActivated_t>.Create(_003C_003Ec._003C_003E9._0023_003DqMvyR5NqF3R54kyvNZNJCvkH5SlxSXDQDk2Jmii2IrhM_003D);
		_0023_003DqoD3LueY0_0024isltLiBK_YFXrtPdF7ZHiI8lNr6XsSbq_0024w_003D = Callback<P2PSessionRequest_t>.Create(_003C_003Ec._003C_003E9._0023_003DqzeInG0OeNBNLoWZXHKt3zjZVdL_fNLppE4sAYIVudhg_003D);
		_0023_003DqJTA0hYZ0tpyAXVU_D7Ig9MTSKxwmpEv9k4q9aeGC1jw_003D = Callback<ItemInstalled_t>.Create(delegate(ItemInstalled_t _0023_003Dq9Qv_qzE4pEz0oMmzxWOJ1g_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003Dq9Qv_qzE4pEz0oMmzxWOJ1g_003D_003D);
		});
		_0023_003DqK17I1kgHTPZZzHjMiDNAlbfZFgrTIFM6lCB_00249QMP_0024K8_003D = Callback<DownloadItemResult_t>.Create(delegate(DownloadItemResult_t _0023_003DqMZXsSRMTEP_04B6NHikTew_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003DqMZXsSRMTEP_04B6NHikTew_003D_003D);
		});
		_0023_003Dq2lUsA132_PKQ_mSh_ketIML9imSix55HMgxE0j8Hhe0_003D = Callback<RemoteStoragePublishedFileSubscribed_t>.Create(_003C_003Ec._003C_003E9._0023_003Dqr87dXNzE7pZaIDxmGgtbxQzQF226hjIyVQFwqdSuBg4_003D);
		_0023_003DqiryUSgft7CIYxdhq_JDHSvKAEsFIsB7mHQholNSAUio_003D = Callback<RemoteStoragePublishedFileUnsubscribed_t>.Create(delegate(RemoteStoragePublishedFileUnsubscribed_t _0023_003Dq2vxtXP1D5xH9JJm_cPC4Nw_003D_003D)
		{
			_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Add(_0023_003Dq2vxtXP1D5xH9JJm_cPC4Nw_003D_003D);
		});
	}

	public static void _0023_003DquhSeGo4SMDlaHhvfbVoAtg_003D_003D()
	{
		_0023_003DqnwXm5_uSO4V7kLV0ZLAAwQ_003D_003D.Clear();
		SteamAPI.RunCallbacks();
	}

	[IteratorStateMachine(typeof(_0023_003DqTSgpA89o5Wa2nT1tT_0024Qbws5Rho_w1YFCMFAD2XvYm3Y_003D))]
	public static IEnumerable<T> _0023_003DqPvxGVUOvQO1LuvS4nX05xIIMrSrN6ENSc_0024_0024kiFneSP8_003D<T>() where T : struct
	{
		return new _0023_003DqTSgpA89o5Wa2nT1tT_0024Qbws5Rho_w1YFCMFAD2XvYm3Y_003D<T>(-2);
	}

	public static void _0023_003Dqu6TaiTmOlPX6srrNiaO3zA_003D_003D<T>(this SteamAPICall_t _0023_003DqHsOLfQiBLlPJNi6L0pnQiw_003D_003D, CallResult<T>.APIDispatchDelegate _0023_003DqHI0ArwO8H8Yfl0QGCcYtxA_003D_003D)
	{
		_0023_003DqUT5TW7IxQT3UREPtdDH3QcB_0024A8sQo0Kwa4zA364wmgU_003D<T> CS_0024_003C_003E8__locals6 = new _0023_003DqUT5TW7IxQT3UREPtdDH3QcB_0024A8sQo0Kwa4zA364wmgU_003D<T>();
		CS_0024_003C_003E8__locals6._0023_003DqxioqV_0024m1FV0oBISsroGQbA_003D_003D = _0023_003DqHI0ArwO8H8Yfl0QGCcYtxA_003D_003D;
		CS_0024_003C_003E8__locals6._0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D = CallResult<T>.Create();
		_0023_003DqxHFi5vQ5Sj0AzjZwaM10VQ_003D_003D.Add(CS_0024_003C_003E8__locals6._0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D);
		CS_0024_003C_003E8__locals6._0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D.Set(_0023_003DqHsOLfQiBLlPJNi6L0pnQiw_003D_003D, delegate(T _0023_003Dq66_2k5llSka_Ap_rZ8P2Xw_003D_003D, bool _0023_003Dqh6SIhRFZ4vwmmvCHuBeRzw_003D_003D)
		{
			_0023_003DqxHFi5vQ5Sj0AzjZwaM10VQ_003D_003D.Remove(CS_0024_003C_003E8__locals6._0023_003DqRm51EGLBGRH7NikHEsBnYw_003D_003D);
			CS_0024_003C_003E8__locals6._0023_003DqxioqV_0024m1FV0oBISsroGQbA_003D_003D(_0023_003Dq66_2k5llSka_Ap_rZ8P2Xw_003D_003D, _0023_003Dqh6SIhRFZ4vwmmvCHuBeRzw_003D_003D);
		});
	}
}
