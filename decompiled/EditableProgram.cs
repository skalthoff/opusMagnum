using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;

public sealed class EditableProgram
{
	private sealed class _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D : IEnumerator<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D>, IEnumerable<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D;

		private _0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D _0023_003DqSVIHpjjYH0ODtxOMTdsr9A_003D_003D;

		private int _0023_003DqSqgbXo05ZSfoe5L_0024bxCOxuVYa_0024EaNQyId6EvnsAJtHY_003D;

		public EditableProgram _0023_003Dqh2BkCHESSde4S1yyhyeDfw_003D_003D;

		private SortedDictionary<int, InstructionType>.Enumerator _0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D;

		[DebuggerHidden]
		public _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D(int _0023_003DqmNevFZVHecmJbgtxGqG_TA_003D_003D)
		{
			_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = _0023_003DqmNevFZVHecmJbgtxGqG_TA_003D_003D;
			_0023_003DqSqgbXo05ZSfoe5L_0024bxCOxuVYa_0024EaNQyId6EvnsAJtHY_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003Dqwg153M_0024lGtBRm9Se9_SQGILEsRh_D66Dc_0024YpyPOoHwk_003D()
		{
			int num = _0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D;
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
			//ILSpy generated this explicit interface implementation from .override directive in #=qwg153M$lGtBRm9Se9_SQGILEsRh_D66Dc$YpyPOoHwk=
			this._0023_003Dqwg153M_0024lGtBRm9Se9_SQGILEsRh_D66Dc_0024YpyPOoHwk_003D();
		}

		private bool MoveNext()
		{
			try
			{
				int num = _0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D;
				EditableProgram editableProgram = _0023_003Dqh2BkCHESSde4S1yyhyeDfw_003D_003D;
				switch (num)
				{
				default:
					return false;
				case 0:
					_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = -1;
					_0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D = editableProgram._0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.GetEnumerator();
					_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = -3;
					break;
				case 1:
					_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = -3;
					break;
				}
				if (_0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D.MoveNext())
				{
					KeyValuePair<int, InstructionType> current = _0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D.Current;
					_0023_003DqSVIHpjjYH0ODtxOMTdsr9A_003D_003D = new _0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D(current.Key, current.Value);
					_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = 1;
					return true;
				}
				_0023_003DqPoEAhpaZJMGhxTM3_b3LNA_003D_003D();
				_0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D = default(SortedDictionary<int, InstructionType>.Enumerator);
				return false;
			}
			catch
			{
				//try-fault
				_0023_003Dqwg153M_0024lGtBRm9Se9_SQGILEsRh_D66Dc_0024YpyPOoHwk_003D();
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
			_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = -1;
			((IDisposable)_0023_003DqQYC40EFcJ7QcpXEAi_htXQ_003D_003D/*cast due to .constrained prefix*/).Dispose();
		}

		[DebuggerHidden]
		private _0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D _0023_003Dq1RJgwfPliNoGaYsWQ2FUGmBGQDd1GwnZcpcDXRQ_enb16g2Y51qGK_HSXMf4hdS_2Ak8A5Yrd_0024zCFeC8VxovlgTLPNZkLnTlky315bpu1T0_003D()
		{
			return _0023_003DqSVIHpjjYH0ODtxOMTdsr9A_003D_003D;
		}

		_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D IEnumerator<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q1RJgwfPliNoGaYsWQ2FUGmBGQDd1GwnZcpcDXRQ_enb16g2Y51qGK_HSXMf4hdS_2Ak8A5Yrd$zCFeC8VxovlgTLPNZkLnTlky315bpu1T0=
			return this._0023_003Dq1RJgwfPliNoGaYsWQ2FUGmBGQDd1GwnZcpcDXRQ_enb16g2Y51qGK_HSXMf4hdS_2Ak8A5Yrd_0024zCFeC8VxovlgTLPNZkLnTlky315bpu1T0_003D();
		}

		[DebuggerHidden]
		private void _0023_003DqGsTLvns0XNzAeyR2Cnq5Z3cbb_0024s22jQx7PNBq5rVQzV6pVYlaMhkAEvIwIMlEKkK()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qGsTLvns0XNzAeyR2Cnq5Z3cbb$s22jQx7PNBq5rVQzV6pVYlaMhkAEvIwIMlEKkK
			this._0023_003DqGsTLvns0XNzAeyR2Cnq5Z3cbb_0024s22jQx7PNBq5rVQzV6pVYlaMhkAEvIwIMlEKkK();
		}

		[DebuggerHidden]
		private object _0023_003Dq67cxJz7JQ6kedYDL8_APCpqkKN34uFTJ5KVG9YbQhAUEAIlAwxuB0i3kQYdpobEZ()
		{
			return _0023_003DqSVIHpjjYH0ODtxOMTdsr9A_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q67cxJz7JQ6kedYDL8_APCpqkKN34uFTJ5KVG9YbQhAUEAIlAwxuB0i3kQYdpobEZ
			return this._0023_003Dq67cxJz7JQ6kedYDL8_APCpqkKN34uFTJ5KVG9YbQhAUEAIlAwxuB0i3kQYdpobEZ();
		}

		[DebuggerHidden]
		private IEnumerator<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D> _0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNRiFtrf_7L_0024_xoixPo4ji_Ki7uNdeSIdefIMOvtevuwsGrwAoHUlFsVy4gCVD9nvLI_003D()
		{
			_0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D;
			if (_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D == -2 && _0023_003DqSqgbXo05ZSfoe5L_0024bxCOxuVYa_0024EaNQyId6EvnsAJtHY_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003DqZtDYXKSXr_VlL4QJbzpvGg_003D_003D = 0;
				_0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D = this;
			}
			else
			{
				_0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D = new _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D(0);
				_0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D._0023_003Dqh2BkCHESSde4S1yyhyeDfw_003D_003D = _0023_003Dqh2BkCHESSde4S1yyhyeDfw_003D_003D;
			}
			return _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D;
		}

		IEnumerator<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D> IEnumerable<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNRiFtrf_7L$_xoixPo4ji_Ki7uNdeSIdefIMOvtevuwsGrwAoHUlFsVy4gCVD9nvLI=
			return this._0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNRiFtrf_7L_0024_xoixPo4ji_Ki7uNdeSIdefIMOvtevuwsGrwAoHUlFsVy4gCVD9nvLI_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003DqZzIY_0024Y7WmdHIvSOjDldXcpBUdpliNfs5VReye1KaVhm4SmJf6ZuzInEaeV3vAM8j()
		{
			return _0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNRiFtrf_7L_0024_xoixPo4ji_Ki7uNdeSIdefIMOvtevuwsGrwAoHUlFsVy4gCVD9nvLI_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qZzIY$Y7WmdHIvSOjDldXcpBUdpliNfs5VReye1KaVhm4SmJf6ZuzInEaeV3vAM8j
			return this._0023_003DqZzIY_0024Y7WmdHIvSOjDldXcpBUdpliNfs5VReye1KaVhm4SmJf6ZuzInEaeV3vAM8j();
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<InstructionType, InstructionType> _003C_003E9__17_0;

		internal InstructionType _0023_003DqFyOxWtUEtnO7hsVz4ytyoAHIz7eVjard57SKO0KO5_0024ANd3JCfcYk66jeRt4HaPgK(InstructionType _0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D)
		{
			if (_0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D != _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqVHpEyBrpSRvjFzqRqBCIvA_003D_003D._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D)
			{
				return _0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D;
			}
			return _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D;
		}
	}

	public bool _0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D;

	private SortedDictionary<int, InstructionType> _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D = new SortedDictionary<int, InstructionType>();

	public EditableProgram _0023_003DqiYL0qGAgh8uWbHm3DEGvGg_003D_003D()
	{
		return new EditableProgram
		{
			_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true,
			_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D = new SortedDictionary<int, InstructionType>(_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D)
		};
	}

	public void _0023_003DqoSzfD9mzW6a0Rg3GAZarzQ_003D_003D(EditableProgram _0023_003DqWLCIcEcRhpQ18Gss2JSMQw_003D_003D)
	{
		foreach (KeyValuePair<int, InstructionType> item in _0023_003DqWLCIcEcRhpQ18Gss2JSMQw_003D_003D._0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D)
		{
			if (!_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.ContainsKey(item.Key))
			{
				_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D[item.Key] = item.Value;
				_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true;
			}
		}
	}

	public int _0023_003DqV5u8Dyc3S1uTZiKdZmxvrQ_003D_003D()
	{
		if (_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Count > 0)
		{
			return _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Keys.Min();
		}
		return 0;
	}

	public int _0023_003DqB1W89_0024VwEprO5V08F3PcDQ_003D_003D()
	{
		if (_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Count > 0)
		{
			return _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Keys.Max();
		}
		return 0;
	}

	public Maybe<InstructionType> _0023_003DqtYWIMlfA_PYQxSqmDtqy_0024Q_003D_003D(int _0023_003DqqFCaBS4IC1PNHmmpiEsaNA_003D_003D)
	{
		return _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(_0023_003DqqFCaBS4IC1PNHmmpiEsaNA_003D_003D);
	}

	[IteratorStateMachine(typeof(_0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D))]
	public IEnumerable<_0023_003DqHkuRsQ65LwPyKq9G70OWjKlvIF2w9t3qOvm821O1okg_003D> _0023_003Dq1wgMGEmS0ZZ8eWdswpLhu1SNHyq8ESZTruAjGr0_W9M_003D()
	{
		return new _0023_003DqrFEKODvQcUwIuVAQ_qlqlJU6J5NV5wL5QEN4yHNZHeI_003D(-2)
		{
			_0023_003Dqh2BkCHESSde4S1yyhyeDfw_003D_003D = this
		};
	}

	public bool _0023_003DqUsL9uZ_0024c1rnjAqoybxPXqKTweMfDQeCIm_TvcDg_0024Z84_003D(InstructionType _0023_003DqUlVfzKWvI2aBRECAIDlZUg_003D_003D)
	{
		return _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Values.Contains(_0023_003DqUlVfzKWvI2aBRECAIDlZUg_003D_003D);
	}

	public int _0023_003DqNNXXW5dXGIvsryYL_0024m_0024RyjciEzQqpnmA6UHwqB6Yebk_003D()
	{
		return _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Count;
	}

	public void _0023_003Dqj5h_FH6X3_00249s1NonSRh_0024VA_003D_003D(int _0023_003DqRgYmRmboKxuEWjQb2P3RDg_003D_003D, InstructionType _0023_003DqfaD0diy64GixFESEcJCIjw_003D_003D)
	{
		_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D[_0023_003DqRgYmRmboKxuEWjQb2P3RDg_003D_003D] = _0023_003DqfaD0diy64GixFESEcJCIjw_003D_003D;
		_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true;
	}

	public void _0023_003DqJQw4tF8rZ_Z76wIT6m6B0TSm_0024dvfIpV_0024_0024G64JcfPKrw_003D(int _0023_003Dqdi_ZTNRtjRKvdYzZw6IP7g_003D_003D, InstructionType _0023_003Dq11PzfnR_002448JozOun39W4mQ_003D_003D)
	{
		Maybe<InstructionType> maybe = _0023_003Dq11PzfnR_002448JozOun39W4mQ_003D_003D;
		while (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			Maybe<InstructionType> maybe2 = _0023_003DqtYWIMlfA_PYQxSqmDtqy_0024Q_003D_003D(_0023_003Dqdi_ZTNRtjRKvdYzZw6IP7g_003D_003D);
			_0023_003Dqj5h_FH6X3_00249s1NonSRh_0024VA_003D_003D(_0023_003Dqdi_ZTNRtjRKvdYzZw6IP7g_003D_003D, maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
			maybe = maybe2;
			_0023_003Dqdi_ZTNRtjRKvdYzZw6IP7g_003D_003D++;
		}
		_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true;
	}

	public void _0023_003DqLcMNL3wJLqDGejIizZv2z693sktNZ5mVq_qq6tuNSiA_003D(int _0023_003Dq3Piux4Y3PmWS_fsivm_002473A_003D_003D, bool _0023_003Dqh8HzoSAnO2LMDDRG4Obp2A_003D_003D)
	{
		_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Remove(_0023_003Dq3Piux4Y3PmWS_fsivm_002473A_003D_003D);
		if (_0023_003Dqh8HzoSAnO2LMDDRG4Obp2A_003D_003D)
		{
			_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true;
		}
	}

	public void _0023_003DqvdEQq__EW1gLz9d8e7deUO7LySgEMHV72famjPJs2F0_003D()
	{
		_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Clear();
		_0023_003DqM6yhXxC9T6Uvp5u2QF9BjQ_003D_003D = true;
	}

	public void _0023_003DqitxY_0024_002464YZqRIqAiKWKFL5apy0mc0dYNp5CRxdQhETXrTAGyTHCkQnpD3w5NAlla()
	{
		int[] array = _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Keys.ToArray();
		foreach (int key in array)
		{
			if (_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D[key]._0023_003Dqzfm2QxZbEyekaDnvDEVofw_003D_003D)
			{
				_0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D.Remove(key);
			}
		}
	}

	public _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D _0023_003DqyBQSjTHnDEGcyfMCR8oAJw_003D_003D(Part _0023_003Dqy_0024DWtTg_2SfiKSCcZkq6WQ_003D_003D, Maybe<Part> _0023_003DqBjWmuS_nKigKqPLbleT9hA_003D_003D)
	{
		_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2 = new _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D();
		foreach (KeyValuePair<int, InstructionType> item in _0023_003Dq9FGGQuAHAXyFIbH3tvT_Aw_003D_003D)
		{
			_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D[item.Key] = new _0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D
			{
				_0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D = item.Value,
				_0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D = new InstructionType[1] { item.Value }
			};
		}
		foreach (KeyValuePair<int, _0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D> item2 in _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D)
		{
			if (item2.Value._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D == (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)6)
			{
				_0023_003DqFJJxc3CWaWd3XzAelSuRpaYlAFnyE3ex0EsyL7hKY_M_003D(_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2, item2.Key, _0023_003Dqy_0024DWtTg_2SfiKSCcZkq6WQ_003D_003D, _0023_003DqBjWmuS_nKigKqPLbleT9hA_003D_003D);
			}
		}
		foreach (KeyValuePair<int, _0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D> item3 in _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D)
		{
			if (item3.Value._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D == (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)7)
			{
				_0023_003Dqg95MIuFHxWbNLQLt2Aq9S857LzrOC1Pl1dP5mTrDf9Y_003D(_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2, item3.Key);
			}
		}
		return _0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D2;
	}

	private static void _0023_003DqFJJxc3CWaWd3XzAelSuRpaYlAFnyE3ex0EsyL7hKY_M_003D(_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D _0023_003DqgN3P7or6df3v_0024sZJEozlR7bh_0024o9DIfwlS78gR3257sw_003D, int _0023_003DqSLa2k0QJzxBQ6BSwvnNjDA_003D_003D, Part _0023_003DqxwgJfnZvjU50Ybpra0CJKA_003D_003D, Maybe<Part> _0023_003DqHQ5tH7lzBuB3FkZZTk_0024MmA_003D_003D)
	{
		_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(_0023_003DqgN3P7or6df3v_0024sZJEozlR7bh_0024o9DIfwlS78gR3257sw_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D[_0023_003DqSLa2k0QJzxBQ6BSwvnNjDA_003D_003D]._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D == (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)6, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803375));
		int num = _0023_003DqxwgJfnZvjU50Ybpra0CJKA_003D_003D._0023_003Dq6jyjbEzWFIOgvl_0024ykKNlncly5gcFQHb3jy1wGDdvGiI_003D();
		int num2 = 0;
		int num3 = 1;
		bool flag = false;
		if (_0023_003DqHQ5tH7lzBuB3FkZZTk_0024MmA_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			IReadOnlyList<HexIndex> readOnlyList = _0023_003DqHQ5tH7lzBuB3FkZZTk_0024MmA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqrUsz82io4zz4MfRsRqj4RbvWOQJPVO9ZfkmfSDBBVWM_003D();
			num2 = readOnlyList._0023_003Dqe8o5c_0024UPQ5y2E7uO15FqdQ_003D_003D(_0023_003DqxwgJfnZvjU50Ybpra0CJKA_003D_003D._0023_003DqmDkefz3wch3y4rXSbGlJBLDbPzzw_00249jand5557fYsDg_003D() - _0023_003DqHQ5tH7lzBuB3FkZZTk_0024MmA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqmDkefz3wch3y4rXSbGlJBLDbPzzw_00249jand5557fYsDg_003D())._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
			num3 = readOnlyList.Count;
			flag = _0023_003DqHQ5tH7lzBuB3FkZZTk_0024MmA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()._0023_003DqtknXkI3c7CiPOc1oXZoQsuzJWKQsPG4x_YQILu6TwUw_003D();
		}
		int num4 = 0;
		int num5 = num;
		int num6 = num2;
		bool flag2 = false;
		foreach (KeyValuePair<int, _0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D> item in _0023_003DqgN3P7or6df3v_0024sZJEozlR7bh_0024o9DIfwlS78gR3257sw_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D)
		{
			if (item.Key == _0023_003DqSLa2k0QJzxBQ6BSwvnNjDA_003D_003D)
			{
				break;
			}
			InstructionType _0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D = item.Value._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D;
			switch (_0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D)
			{
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)6:
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)7:
				num4 = 0;
				num5 = num;
				num6 = num2;
				flag2 = false;
				break;
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)1:
				num5 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqURBbaL72HtfW40SuvLCq7A_003D_003D(num5 + (_0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqbQczAEEOrzd85SToU7jtMg_003D_003D ? 1 : (-1)), Part._0023_003Dq0zrtZ2qjf8jw5qfwxr9V2Q_003D_003D, Part._0023_003Dq1ZjWOW9t_0024SFhmEC7Ct8qJQ_003D_003D);
				break;
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)2:
				num4 += (_0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqbQczAEEOrzd85SToU7jtMg_003D_003D ? 1 : (-1));
				break;
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)4:
				num6 += (_0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqbQczAEEOrzd85SToU7jtMg_003D_003D ? 1 : (-1));
				if (!flag)
				{
					num6 = _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqURBbaL72HtfW40SuvLCq7A_003D_003D(num6, 0, num3 - 1);
				}
				break;
			case (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)5:
				flag2 = _0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqbQczAEEOrzd85SToU7jtMg_003D_003D;
				break;
			}
		}
		int i = num5 - num;
		num4 %= 6;
		if (num4 > 3)
		{
			num4 -= 6;
		}
		else if (num4 < -3)
		{
			num4 += 6;
		}
		int j = num6 - num2;
		if (flag)
		{
			j %= num3;
			if (j > num3 / 2)
			{
				j -= num3;
			}
			else if (j < -num3 / 2)
			{
				j += num3;
			}
		}
		List<InstructionType> list = new List<InstructionType>();
		if (flag2)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqKnYdOtJJj0JxaKLZOshAoA_003D_003D);
			flag2 = false;
		}
		while (i > 0)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqAvGnTUAqHoG0hslorQaQGg_003D_003D);
			i--;
		}
		while (num4 > 0)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqIJUZrx8veRnH7neJYNCsoQ_003D_003D);
			num4--;
		}
		for (; num4 < 0; num4++)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqZS8HTMWqOky641Z_0024vEW2eg_003D_003D);
		}
		while (j > 0)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqANmXBF2eVvdcEh4beYXX8A_003D_003D);
			j--;
		}
		for (; j < 0; j++)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqyLRZUJDe_Lo9eNZZ7yvBjQ_003D_003D);
		}
		for (; i < 0; i++)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqRac1qSZYh2xnm6jclfLYSA_003D_003D);
		}
		if (list.Count == 0)
		{
			list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D);
		}
		_0023_003DqgN3P7or6df3v_0024sZJEozlR7bh_0024o9DIfwlS78gR3257sw_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D[_0023_003DqSLa2k0QJzxBQ6BSwvnNjDA_003D_003D]._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D = list.ToArray();
	}

	private static void _0023_003Dqg95MIuFHxWbNLQLt2Aq9S857LzrOC1Pl1dP5mTrDf9Y_003D(_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D _0023_003DqB6mS_jDvISggSBzm6_znVwLu0jycsPhEpd_rnZDN9m0_003D, int _0023_003DqnQYKuZindUnYxCfqiyeruQ_003D_003D)
	{
		_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(_0023_003DqB6mS_jDvISggSBzm6_znVwLu0jycsPhEpd_rnZDN9m0_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D[_0023_003DqnQYKuZindUnYxCfqiyeruQ_003D_003D]._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D == (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)7, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850803276));
		List<InstructionType> list = new List<InstructionType>();
		Maybe<InstructionType[]> maybe = _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
		int num = 0;
		for (int i = 0; i < _0023_003DqnQYKuZindUnYxCfqiyeruQ_003D_003D; i++)
		{
			if (_0023_003DqB6mS_jDvISggSBzm6_znVwLu0jycsPhEpd_rnZDN9m0_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D.TryGetValue(i, out var value))
			{
				if (value._0023_003DqksJWu_Qkg7tvayeA4h18oQ_003D_003D._0023_003DqtJtOuuNKZkwRFOD8j4hBMA_003D_003D == (_0023_003DqT8u4fWiLjx9fsaCFXx9xwYwMhVRpAvv_O1tarFxMkeQ_003D)7)
				{
					list.Clear();
					maybe = value._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D;
					continue;
				}
				list.AddRange(value._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D.Select((InstructionType _0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D) => (_0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D != _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqVHpEyBrpSRvjFzqRqBCIvA_003D_003D._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D) ? _0023_003DqWNhMJeQ2egzNldSwVLVD7g_003D_003D : _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D));
				num = value._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D.Length - 1;
			}
			else if (list.Count > 0)
			{
				if (num > 0)
				{
					num--;
				}
				else
				{
					list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqGwPv_K9AuSuXO4P5ODf_0024nQ_003D_003D);
				}
			}
		}
		int num2 = list.Count - 1;
		while (num2 >= 0 && list[num2]._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D == _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqGwPv_K9AuSuXO4P5ODf_0024nQ_003D_003D._0023_003DqK_0024lKZsuUBE5md5evfwbS_Q_003D_003D)
		{
			list.RemoveAt(num2);
			num2--;
		}
		if (list.Count == 0)
		{
			if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
			{
				list.AddRange(maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
			}
			else
			{
				list.Add(_0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D);
			}
		}
		_0023_003DqB6mS_jDvISggSBzm6_znVwLu0jycsPhEpd_rnZDN9m0_003D._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D[_0023_003DqnQYKuZindUnYxCfqiyeruQ_003D_003D]._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D = list.ToArray();
	}
}
