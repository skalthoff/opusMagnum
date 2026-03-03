using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.CompilerServices;

[DebuggerDisplay("Hex({Q}, {R})")]
public struct HexIndex : IEquatable<HexIndex>
{
	private sealed class _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D : IEnumerator<HexIndex>, IEnumerable<HexIndex>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D;

		private HexIndex _0023_003DqVn0q1JMd3Vb9GYJPr5uvrg_003D_003D;

		private int _0023_003DqwiksYZnZ_eDnlmFHytKchhJZ8U8MvHBqG2EKFt5j_0024_00240_003D;

		private HexIndex _0023_003DqezNShUQLh4Ol1gKKxw0jGw_003D_003D;

		public HexIndex _0023_003DqU2aBgpiJ0BQBeWil_rQ0hw_003D_003D;

		private int _0023_003DqCAOg3bo05DOlADCqTv7Irg_003D_003D;

		public int _0023_003DqHVuLz9eittazuFPJlxa0rQ_003D_003D;

		private int _0023_003Dqokv4yzg85kHP57_0024GWqbnGQ_003D_003D;

		private IEnumerator<HexIndex> _0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D;

		[DebuggerHidden]
		public _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D(int _0023_003DqTSC1hGEMi9Y_0024x8OFiwL_xg_003D_003D)
		{
			_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = _0023_003DqTSC1hGEMi9Y_0024x8OFiwL_xg_003D_003D;
			_0023_003DqwiksYZnZ_eDnlmFHytKchhJZ8U8MvHBqG2EKFt5j_0024_00240_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqlkpZa_G6Y11Ve9AJ2HYBQLmXAhsg2rKWmfqJcwbkB9k_003D()
		{
			int num = _0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D;
			if (num == -3 || num == 2)
			{
				try
				{
				}
				finally
				{
					_0023_003DqLCtfwKbEtmpzBYoYxS_0024soA_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qlkpZa_G6Y11Ve9AJ2HYBQLmXAhsg2rKWmfqJcwbkB9k=
			this._0023_003DqlkpZa_G6Y11Ve9AJ2HYBQLmXAhsg2rKWmfqJcwbkB9k_003D();
		}

		private bool MoveNext()
		{
			try
			{
				switch (_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D)
				{
				default:
					return false;
				case 0:
					_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = -1;
					_0023_003DqVn0q1JMd3Vb9GYJPr5uvrg_003D_003D = _0023_003DqezNShUQLh4Ol1gKKxw0jGw_003D_003D;
					_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = 1;
					return true;
				case 1:
					_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = -1;
					_0023_003Dqokv4yzg85kHP57_0024GWqbnGQ_003D_003D = 1;
					goto IL_00c7;
				case 2:
					{
						_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = -3;
						goto IL_009d;
					}
					IL_00c7:
					if (_0023_003Dqokv4yzg85kHP57_0024GWqbnGQ_003D_003D <= _0023_003DqCAOg3bo05DOlADCqTv7Irg_003D_003D)
					{
						_0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D = EnumerateRing(_0023_003DqezNShUQLh4Ol1gKKxw0jGw_003D_003D, _0023_003Dqokv4yzg85kHP57_0024GWqbnGQ_003D_003D).GetEnumerator();
						_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = -3;
						goto IL_009d;
					}
					return false;
					IL_009d:
					if (_0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D.MoveNext())
					{
						HexIndex current = _0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D.Current;
						_0023_003DqVn0q1JMd3Vb9GYJPr5uvrg_003D_003D = current;
						_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = 2;
						return true;
					}
					_0023_003DqLCtfwKbEtmpzBYoYxS_0024soA_003D_003D();
					_0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D = null;
					_0023_003Dqokv4yzg85kHP57_0024GWqbnGQ_003D_003D++;
					goto IL_00c7;
				}
			}
			catch
			{
				//try-fault
				_0023_003DqlkpZa_G6Y11Ve9AJ2HYBQLmXAhsg2rKWmfqJcwbkB9k_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqLCtfwKbEtmpzBYoYxS_0024soA_003D_003D()
		{
			_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = -1;
			if (_0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D != null)
			{
				_0023_003Dqz2CJqBJhZwp296qGRlROrw_003D_003D.Dispose();
			}
		}

		[DebuggerHidden]
		private HexIndex _0023_003DqiBB8w5Cmc6hpOn0N2SFCXPga7wgPLv2Jc8bw8UeNrUPIKwLTifMIQ0pBJCMNTFDSbsCRCu8R_ESQWXjGCajdsQ_003D_003D()
		{
			return _0023_003DqVn0q1JMd3Vb9GYJPr5uvrg_003D_003D;
		}

		HexIndex IEnumerator<HexIndex>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qiBB8w5Cmc6hpOn0N2SFCXPga7wgPLv2Jc8bw8UeNrUPIKwLTifMIQ0pBJCMNTFDSbsCRCu8R_ESQWXjGCajdsQ==
			return this._0023_003DqiBB8w5Cmc6hpOn0N2SFCXPga7wgPLv2Jc8bw8UeNrUPIKwLTifMIQ0pBJCMNTFDSbsCRCu8R_ESQWXjGCajdsQ_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003DqBbOOtL1i5_0024R4Fz4U52XO4RziHiPmFJA1raBfzhJbLmz5ArPNMxLY_0024Gxn1vTtSNpd()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qBbOOtL1i5$R4Fz4U52XO4RziHiPmFJA1raBfzhJbLmz5ArPNMxLY$Gxn1vTtSNpd
			this._0023_003DqBbOOtL1i5_0024R4Fz4U52XO4RziHiPmFJA1raBfzhJbLmz5ArPNMxLY_0024Gxn1vTtSNpd();
		}

		[DebuggerHidden]
		private object _0023_003DqZ5iz8F6eQVBbYkghTO9y9MLJvXj446TbvH7v3iKcY7YPElgCosYomH9Zi3BAeBnE()
		{
			return _0023_003DqVn0q1JMd3Vb9GYJPr5uvrg_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qZ5iz8F6eQVBbYkghTO9y9MLJvXj446TbvH7v3iKcY7YPElgCosYomH9Zi3BAeBnE
			return this._0023_003DqZ5iz8F6eQVBbYkghTO9y9MLJvXj446TbvH7v3iKcY7YPElgCosYomH9Zi3BAeBnE();
		}

		[DebuggerHidden]
		private IEnumerator<HexIndex> _0023_003Dqau0XVgLK0Tf3zVrXi_pYOFXvIL5QGmquvuLUBwhyS_vWpIeanVhysJxzbAPePH4SQwFtmZ4RFRoBylLaggggPw_003D_003D()
		{
			_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D;
			if (_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D == -2 && _0023_003DqwiksYZnZ_eDnlmFHytKchhJZ8U8MvHBqG2EKFt5j_0024_00240_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003Dq1bMQfsHvyt_0024oW0o9K24ukQ_003D_003D = 0;
				_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D = this;
			}
			else
			{
				_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D = new _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D(0);
			}
			_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D._0023_003DqezNShUQLh4Ol1gKKxw0jGw_003D_003D = _0023_003DqU2aBgpiJ0BQBeWil_rQ0hw_003D_003D;
			_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D._0023_003DqCAOg3bo05DOlADCqTv7Irg_003D_003D = _0023_003DqHVuLz9eittazuFPJlxa0rQ_003D_003D;
			return _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D;
		}

		IEnumerator<HexIndex> IEnumerable<HexIndex>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qau0XVgLK0Tf3zVrXi_pYOFXvIL5QGmquvuLUBwhyS_vWpIeanVhysJxzbAPePH4SQwFtmZ4RFRoBylLaggggPw==
			return this._0023_003Dqau0XVgLK0Tf3zVrXi_pYOFXvIL5QGmquvuLUBwhyS_vWpIeanVhysJxzbAPePH4SQwFtmZ4RFRoBylLaggggPw_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003DqSeZvkJ73QBSL7uKxUrJziFai6OBOCyrsA4HWbHHpw1xb0x3VQP5gtTDV1R4mm99G()
		{
			return _0023_003Dqau0XVgLK0Tf3zVrXi_pYOFXvIL5QGmquvuLUBwhyS_vWpIeanVhysJxzbAPePH4SQwFtmZ4RFRoBylLaggggPw_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qSeZvkJ73QBSL7uKxUrJziFai6OBOCyrsA4HWbHHpw1xb0x3VQP5gtTDV1R4mm99G
			return this._0023_003DqSeZvkJ73QBSL7uKxUrJziFai6OBOCyrsA4HWbHHpw1xb0x3VQP5gtTDV1R4mm99G();
		}
	}

	private sealed class _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D : IEnumerator<HexIndex>, IEnumerable<HexIndex>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D;

		private HexIndex _0023_003DqHBwk_PqRHNMlk83T0Fn3uA_003D_003D;

		private int _0023_003DqLMXpvRRA0YQfjX6rK7TpGlKIsUKUrazgmAXQGTpuNDI_003D;

		private int _0023_003DqOPT_yI1JfL_W8aeTetuBdQ_003D_003D;

		public int _0023_003Dqhcm2PbtJgeeFyy_weiHTsg_003D_003D;

		private HexIndex _0023_003Dqv7LWOB0VFHlpbFt8Vw_0024NvA_003D_003D;

		public HexIndex _0023_003DqA7S5ny2PPIHR7P7opSMOQQ_003D_003D;

		private HexIndex _0023_003DqiDL4tZBuqQJQ74aD72J7qA_003D_003D;

		private int _0023_003DqCJyhHAVc8Jsn_np_b49mVw_003D_003D;

		private int _0023_003DqhKVPKlIl57xsPUONeM9aBw_003D_003D;

		[DebuggerHidden]
		public _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D(int _0023_003Dqa4jd6P_gUUSveyXybSkLxw_003D_003D)
		{
			_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D = _0023_003Dqa4jd6P_gUUSveyXybSkLxw_003D_003D;
			_0023_003DqLMXpvRRA0YQfjX6rK7TpGlKIsUKUrazgmAXQGTpuNDI_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqKphtFxRLCmxbGj4xQhSkpYsiTG2bHH_0024qIQgt_0024rj3zu0_003D()
		{
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qKphtFxRLCmxbGj4xQhSkpYsiTG2bHH$qIQgt$rj3zu0=
			this._0023_003DqKphtFxRLCmxbGj4xQhSkpYsiTG2bHH_0024qIQgt_0024rj3zu0_003D();
		}

		private bool MoveNext()
		{
			int num = _0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D;
			if (num != 0)
			{
				if (num != 1)
				{
					return false;
				}
				_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D = -1;
				HexIndex hexIndex = AdjacentOffsets[(_0023_003DqCJyhHAVc8Jsn_np_b49mVw_003D_003D + 2) % 6];
				_0023_003DqiDL4tZBuqQJQ74aD72J7qA_003D_003D += hexIndex;
				_0023_003DqhKVPKlIl57xsPUONeM9aBw_003D_003D++;
				goto IL_00b2;
			}
			_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D = -1;
			if (_0023_003DqOPT_yI1JfL_W8aeTetuBdQ_003D_003D < 1)
			{
				throw new ArgumentException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842839));
			}
			_0023_003DqiDL4tZBuqQJQ74aD72J7qA_003D_003D = _0023_003Dqv7LWOB0VFHlpbFt8Vw_0024NvA_003D_003D + new HexIndex(_0023_003DqOPT_yI1JfL_W8aeTetuBdQ_003D_003D, 0);
			_0023_003DqCJyhHAVc8Jsn_np_b49mVw_003D_003D = 0;
			goto IL_00d0;
			IL_00b2:
			if (_0023_003DqhKVPKlIl57xsPUONeM9aBw_003D_003D < _0023_003DqOPT_yI1JfL_W8aeTetuBdQ_003D_003D)
			{
				_0023_003DqHBwk_PqRHNMlk83T0Fn3uA_003D_003D = _0023_003DqiDL4tZBuqQJQ74aD72J7qA_003D_003D;
				_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D = 1;
				return true;
			}
			_0023_003DqCJyhHAVc8Jsn_np_b49mVw_003D_003D++;
			goto IL_00d0;
			IL_00d0:
			if (_0023_003DqCJyhHAVc8Jsn_np_b49mVw_003D_003D < 6)
			{
				_0023_003DqhKVPKlIl57xsPUONeM9aBw_003D_003D = 0;
				goto IL_00b2;
			}
			return false;
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		[DebuggerHidden]
		private HexIndex _0023_003DqXKPCxn06tQ2TJCddp6shiGk_0024Vrr7baRgeRAbMGTfZ2yRH7vcutoPqe4KJJfboDSTT_257UKoN2wK9wthALwH2g_003D_003D()
		{
			return _0023_003DqHBwk_PqRHNMlk83T0Fn3uA_003D_003D;
		}

		HexIndex IEnumerator<HexIndex>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qXKPCxn06tQ2TJCddp6shiGk$Vrr7baRgeRAbMGTfZ2yRH7vcutoPqe4KJJfboDSTT_257UKoN2wK9wthALwH2g==
			return this._0023_003DqXKPCxn06tQ2TJCddp6shiGk_0024Vrr7baRgeRAbMGTfZ2yRH7vcutoPqe4KJJfboDSTT_257UKoN2wK9wthALwH2g_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003DqqxIsipCI3arv6qGCb_0024_0024AyXAR4SY5UalhIT5zOKurcaWUL5GtJ_0024DAOpEPjFgjUKAE()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qqxIsipCI3arv6qGCb$$AyXAR4SY5UalhIT5zOKurcaWUL5GtJ$DAOpEPjFgjUKAE
			this._0023_003DqqxIsipCI3arv6qGCb_0024_0024AyXAR4SY5UalhIT5zOKurcaWUL5GtJ_0024DAOpEPjFgjUKAE();
		}

		[DebuggerHidden]
		private object _0023_003Dq4c2Y_0024UKmxM6gDrVD1WhbMY_xh1KzUeS_0024Drz9jvYrPDQEV3FT089OzPl0V1gtDLE_()
		{
			return _0023_003DqHBwk_PqRHNMlk83T0Fn3uA_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q4c2Y$UKmxM6gDrVD1WhbMY_xh1KzUeS$Drz9jvYrPDQEV3FT089OzPl0V1gtDLE_
			return this._0023_003Dq4c2Y_0024UKmxM6gDrVD1WhbMY_xh1KzUeS_0024Drz9jvYrPDQEV3FT089OzPl0V1gtDLE_();
		}

		[DebuggerHidden]
		private IEnumerator<HexIndex> _0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNQGnNfDUHlVq4jHAtI7zxd4wgku_qOc0yxBgFVlL8m4JA_003D_003D()
		{
			_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D;
			if (_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D == -2 && _0023_003DqLMXpvRRA0YQfjX6rK7TpGlKIsUKUrazgmAXQGTpuNDI_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003Dqm7JLQlP46OGHrmLqA9nM9g_003D_003D = 0;
				_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D = this;
			}
			else
			{
				_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D = new _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D(0);
			}
			_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D._0023_003Dqv7LWOB0VFHlpbFt8Vw_0024NvA_003D_003D = _0023_003DqA7S5ny2PPIHR7P7opSMOQQ_003D_003D;
			_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D._0023_003DqOPT_yI1JfL_W8aeTetuBdQ_003D_003D = _0023_003Dqhcm2PbtJgeeFyy_weiHTsg_003D_003D;
			return _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D;
		}

		IEnumerator<HexIndex> IEnumerable<HexIndex>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNQGnNfDUHlVq4jHAtI7zxd4wgku_qOc0yxBgFVlL8m4JA==
			return this._0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNQGnNfDUHlVq4jHAtI7zxd4wgku_qOc0yxBgFVlL8m4JA_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003DqPUHhwhIfbXXx_0024DWM4kLJPICvWlWMAAGX_0024GOsZ29LTCoIBFnHX_xBQ7_0024Z5kN_00244wZo()
		{
			return _0023_003Dqx9emq7y3kz_JRwd90oGnvIFUmcWkk6CtkRPb1NKjXNQGnNfDUHlVq4jHAtI7zxd4wgku_qOc0yxBgFVlL8m4JA_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qPUHhwhIfbXXx$DWM4kLJPICvWlWMAAGX$GOsZ29LTCoIBFnHX_xBQ7$Z5kN$4wZo
			return this._0023_003DqPUHhwhIfbXXx_0024DWM4kLJPICvWlWMAAGX_0024GOsZ29LTCoIBFnHX_xBQ7_0024Z5kN_00244wZo();
		}
	}

	public readonly int Q;

	public readonly int R;

	public static readonly HexIndex[] AdjacentOffsets = new HexIndex[6]
	{
		new HexIndex(1, 0),
		new HexIndex(0, 1),
		new HexIndex(-1, 1),
		new HexIndex(-1, 0),
		new HexIndex(0, -1),
		new HexIndex(1, -1)
	};

	public static readonly HexIndex[] HereAndAdjacentOffsets = new HexIndex[7]
	{
		new HexIndex(0, 0),
		new HexIndex(1, 0),
		new HexIndex(0, 1),
		new HexIndex(-1, 1),
		new HexIndex(-1, 0),
		new HexIndex(0, -1),
		new HexIndex(1, -1)
	};

	public int ImpliedS => -Q - R;

	public HexIndex(int q, int r)
	{
		Q = q;
		R = r;
	}

	public override string ToString()
	{
		return string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842818), Q, R);
	}

	public override bool Equals(object obj)
	{
		HexIndex? hexIndex = obj as HexIndex?;
		if (!hexIndex.HasValue)
		{
			return false;
		}
		HexIndex value = this;
		HexIndex? hexIndex2 = hexIndex;
		return value == hexIndex2;
	}

	public bool Equals(HexIndex other)
	{
		return this == other;
	}

	public override int GetHashCode()
	{
		return (391 + Q.GetHashCode()) * 23 + R.GetHashCode();
	}

	public static bool operator ==(HexIndex a, HexIndex b)
	{
		if (a.Q == b.Q)
		{
			return a.R == b.R;
		}
		return false;
	}

	public static bool operator !=(HexIndex a, HexIndex b)
	{
		if (a.Q == b.Q)
		{
			return a.R != b.R;
		}
		return true;
	}

	public static HexIndex operator +(HexIndex a, HexIndex b)
	{
		return new HexIndex(a.Q + b.Q, a.R + b.R);
	}

	public static HexIndex operator -(HexIndex a, HexIndex b)
	{
		return new HexIndex(a.Q - b.Q, a.R - b.R);
	}

	public static HexIndex operator -(HexIndex a)
	{
		return new HexIndex(-a.Q, -a.R);
	}

	public static int Distance(HexIndex a, HexIndex b)
	{
		return (Math.Abs(a.Q - b.Q) + Math.Abs(a.R - b.R) + Math.Abs(a.ImpliedS - b.ImpliedS)) / 2;
	}

	public int Length()
	{
		return (Math.Abs(Q) + Math.Abs(R) + Math.Abs(ImpliedS)) / 2;
	}

	public HexIndex Rotated(HexRotation rotation)
	{
		return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003Dq1CtWmXBstAQSPGOsSYcVjA_003D_003D(rotation.GetNumberOfTurns(), 6) switch
		{
			0 => new HexIndex(Q, R), 
			1 => new HexIndex(-R, -ImpliedS), 
			2 => new HexIndex(ImpliedS, Q), 
			3 => new HexIndex(-Q, -R), 
			4 => new HexIndex(R, ImpliedS), 
			5 => new HexIndex(-ImpliedS, -Q), 
			_ => throw new ArgumentOutOfRangeException(), 
		};
	}

	public HexIndex RotatedAround(HexIndex pivot, HexRotation rotation)
	{
		return (this - pivot).Rotated(rotation) + pivot;
	}

	public HashSet<HexIndex> GetHexesAtDistance(int distance)
	{
		HashSet<HexIndex> hashSet = new HashSet<HexIndex>();
		HexIndex hexIndex = this + new HexIndex(distance, 0);
		while (hexIndex != this + new HexIndex(0, distance))
		{
			hexIndex += new HexIndex(-1, 1);
			hashSet.Add(hexIndex);
		}
		while (hexIndex != this + new HexIndex(-distance, distance))
		{
			hexIndex += new HexIndex(-1, 0);
			hashSet.Add(hexIndex);
		}
		while (hexIndex != this + new HexIndex(-distance, 0))
		{
			hexIndex += new HexIndex(0, -1);
			hashSet.Add(hexIndex);
		}
		while (hexIndex != this + new HexIndex(0, -distance))
		{
			hexIndex += new HexIndex(1, -1);
			hashSet.Add(hexIndex);
		}
		while (hexIndex != this + new HexIndex(distance, -distance))
		{
			hexIndex += new HexIndex(1, 0);
			hashSet.Add(hexIndex);
		}
		while (hexIndex != this + new HexIndex(distance, 0))
		{
			hexIndex += new HexIndex(0, 1);
			hashSet.Add(hexIndex);
		}
		return hashSet;
	}

	[IteratorStateMachine(typeof(_0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D))]
	public static IEnumerable<HexIndex> EnumerateRing(HexIndex center, int radius)
	{
		return new _0023_003DqtwNOM4oBeH4PRc5oJoUui9VEcFW87oMzOXrlYVmXOvM_003D(-2)
		{
			_0023_003DqA7S5ny2PPIHR7P7opSMOQQ_003D_003D = center,
			_0023_003Dqhcm2PbtJgeeFyy_weiHTsg_003D_003D = radius
		};
	}

	[IteratorStateMachine(typeof(_0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D))]
	public static IEnumerable<HexIndex> EnumerateSpiral(HexIndex center, int radius)
	{
		return new _0023_003DqDUGP_DfSQ2YUgFug3YxObUIO3i6XOUewsgjkUJKT1gw_003D(-2)
		{
			_0023_003DqU2aBgpiJ0BQBeWil_rQ0hw_003D_003D = center,
			_0023_003DqHVuLz9eittazuFPJlxa0rQ_003D_003D = radius
		};
	}
}
