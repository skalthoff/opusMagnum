using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;

internal static class _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D
{
	[DefaultMember("Item")]
	internal sealed class _000E_2003_2000_200A_200A_2004_2002_2000_2007_2000_2003_2005_2000_2003_2004_2001_2003_2005_2001_2005
	{
		private struct _0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D
		{
			public int _0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D;

			public string _0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D;
		}

		private _0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[] _0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D;

		private int _0023_003Dqp2uVoJMAa1Ik0ibaohGMDjEIAd5DH_Tc2WuT_0024az2M6A_003D;

		public _000E_2003_2000_200A_200A_2004_2002_2000_2007_2000_2003_2005_2000_2003_2004_2001_2003_2005_2001_2005()
		{
			_0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D = new _0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[16];
		}

		public _000E_2003_2000_200A_200A_2004_2002_2000_2007_2000_2003_2005_2000_2003_2004_2001_2003_2005_2001_2005(int _0023_003DqexYnvfGyavXmrfTBhVR88Wd88zCNgyrFO49XkK16ec4_003D)
		{
			int num = 16;
			_0023_003DqexYnvfGyavXmrfTBhVR88Wd88zCNgyrFO49XkK16ec4_003D <<= 1;
			while (num < _0023_003DqexYnvfGyavXmrfTBhVR88Wd88zCNgyrFO49XkK16ec4_003D && num > 0)
			{
				num <<= 1;
			}
			if (num < 0)
			{
				num = 16;
			}
			_0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D = new _0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[num];
		}

		public int _0023_003DqKVLxjoaPakI0xp2BQVg8OkH1_SOtchUS_00249KUMW3Wrjg_003D()
		{
			return _0023_003Dqp2uVoJMAa1Ik0ibaohGMDjEIAd5DH_Tc2WuT_0024az2M6A_003D;
		}

		private void _0023_003Dqqqh8Gw0xJh6JRTbLQ3fbaSqh_RpU7JScqxWLvmupuCE_003D()
		{
			_0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[] array = _0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D;
			int num = array.Length;
			int num2 = num * 2;
			if (num2 <= 0)
			{
				return;
			}
			_0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[] array2 = new _0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[num2];
			int num3 = 0;
			for (int i = 0; i < num; i++)
			{
				string _0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D = array[i]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D;
				if (_0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D == null)
				{
					continue;
				}
				int _0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D = array[i]._0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D;
				int num4 = _0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D & (num2 - 1);
				while (array2[num4]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D != null)
				{
					num4++;
					if (num4 >= num2)
					{
						num4 = 0;
					}
				}
				array2[num4]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D = _0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D;
				array2[num4]._0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D = _0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D;
				num3++;
			}
			_0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D = array2;
			_0023_003Dqp2uVoJMAa1Ik0ibaohGMDjEIAd5DH_Tc2WuT_0024az2M6A_003D = num3;
		}

		public string _0023_003Dq1tBl6WakibWw7woHu7jiaw_003D_003D(int _0023_003DqMwt_hQoC52AqKuYw2gAcycugZ_DEiP7KuKVBvxWu1S4_003D)
		{
			_0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[] array = _0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D;
			int num = array.Length;
			int num2 = _0023_003DqMwt_hQoC52AqKuYw2gAcycugZ_DEiP7KuKVBvxWu1S4_003D & (num - 1);
			string result = null;
			while (true)
			{
				if (array[num2]._0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D == _0023_003DqMwt_hQoC52AqKuYw2gAcycugZ_DEiP7KuKVBvxWu1S4_003D)
				{
					result = array[num2]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D;
					break;
				}
				if (array[num2]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D == null)
				{
					break;
				}
				num2++;
				if (num2 >= num)
				{
					num2 = 0;
				}
			}
			return result;
		}

		public void _0023_003DqWkLahNSGMK2L_0024vbnEmTn_0024Q_003D_003D(int _0023_003DqbYFZyf3vm8gyb0IbXX_40AE_0024uDqRw9xP2niw_0024fneEsg_003D, string _0023_003Dq3aXwtvHsOHZcW0OCLwXFbX1c8FFn_0024mUtZNZSodZXAI4_003D)
		{
			_0023_003DqMD4THSMylde7y13CYMHy8AVhI4PGRqMxc1exomALCtM_003D[] array = _0023_003Dqg8ctmwVtBny_uzRixjJrnQFRk9ig0PCafpAJQVuWG30_003D;
			int num = array.Length;
			int num2 = num >> 1;
			int num3 = _0023_003DqbYFZyf3vm8gyb0IbXX_40AE_0024uDqRw9xP2niw_0024fneEsg_003D & (num - 1);
			bool flag;
			while (true)
			{
				int _0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D = array[num3]._0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D;
				flag = array[num3]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D == null;
				if (_0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D == _0023_003DqbYFZyf3vm8gyb0IbXX_40AE_0024uDqRw9xP2niw_0024fneEsg_003D || flag)
				{
					break;
				}
				num3++;
				if (num3 >= num)
				{
					num3 = 0;
				}
			}
			array[num3]._0023_003Dq0x4Qhp1yGQi8UAkRqdvWap6mdNeCyLgevKnuhlt2fjY_003D = _0023_003Dq3aXwtvHsOHZcW0OCLwXFbX1c8FFn_0024mUtZNZSodZXAI4_003D;
			if (flag)
			{
				array[num3]._0023_003Dq6Ptpdp2WGxGYfwpQBdp_0024HAKL0R3DOZvpT5WSflG4XXU_003D = _0023_003DqbYFZyf3vm8gyb0IbXX_40AE_0024uDqRw9xP2niw_0024fneEsg_003D;
				_0023_003Dqp2uVoJMAa1Ik0ibaohGMDjEIAd5DH_Tc2WuT_0024az2M6A_003D++;
				if (_0023_003Dqp2uVoJMAa1Ik0ibaohGMDjEIAd5DH_Tc2WuT_0024az2M6A_003D > num2)
				{
					_0023_003Dqqqh8Gw0xJh6JRTbLQ3fbaSqh_RpU7JScqxWLvmupuCE_003D();
				}
			}
		}
	}

	private enum _0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003
	{

	}

	private sealed class _0005_2008_2002_2008_2006_2004_2008_2006_2005_2002_2008_2002_2001_2005_200A_2001_2001_2009_2003_2003_2004_2007_2004_2007_2004_200B_2001_2006_2004_2009
	{
		private Stream _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D;

		private byte[] _0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D;

		public _0005_2008_2002_2008_2006_2004_2008_2006_2005_2002_2008_2002_2001_2005_200A_2001_2001_2009_2003_2003_2004_2007_2004_2007_2004_200B_2001_2006_2004_2009(Stream _0023_003DqcSybdzXJclgPXC3pmmjshlRkI7aRk3i2pnioIKJLvb0_003D)
		{
			_0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D = _0023_003DqcSybdzXJclgPXC3pmmjshlRkI7aRk3i2pnioIKJLvb0_003D;
			_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D = new byte[4];
		}

		public Stream _0023_003Dqb87xY_0024z_0024L9NF_6mmyv2CBMjXMbRGotFsi8xBw2CzJX0_003D()
		{
			return _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D;
		}

		public short _0023_003Dqw5_0024h5ZpOSEzY7IpQmoBg9ZZXfS9cYNuXjqKAtHlovKI_003D()
		{
			_0023_003DqTLA6h2KbyxySi0kbmtdvacSHG0tzV4s4TvTR8b11qWU_003D(2);
			return (short)(_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[0] | (_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[1] << 8));
		}

		public int _0023_003Dqy_0024Gzg9UCkFWmSBnb9d_0024T_d_BDyzvvBFzkcIZFTDNOEc_003D()
		{
			_0023_003DqTLA6h2KbyxySi0kbmtdvacSHG0tzV4s4TvTR8b11qWU_003D(4);
			return _0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[0] | (_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[1] << 8) | (_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[2] << 16) | (_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[3] << 24);
		}

		private void _0023_003DqK2PwZ_0024m1yoPqlb4vp3mk2r6SroMenGcQAtlrwHaoa5Y_003D()
		{
			throw new EndOfStreamException();
		}

		private void _0023_003DqTLA6h2KbyxySi0kbmtdvacSHG0tzV4s4TvTR8b11qWU_003D(int _0023_003Dqt7iUqtGoHoZAwmw8vC3BpyeFdXITLcySvzs2fz8e1_0024A_003D)
		{
			int num = 0;
			int num2 = 0;
			if (_0023_003Dqt7iUqtGoHoZAwmw8vC3BpyeFdXITLcySvzs2fz8e1_0024A_003D == 1)
			{
				num2 = _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D.ReadByte();
				if (num2 == -1)
				{
					_0023_003DqK2PwZ_0024m1yoPqlb4vp3mk2r6SroMenGcQAtlrwHaoa5Y_003D();
				}
				_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D[0] = (byte)num2;
				return;
			}
			do
			{
				num2 = _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D.Read(_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D, num, _0023_003Dqt7iUqtGoHoZAwmw8vC3BpyeFdXITLcySvzs2fz8e1_0024A_003D - num);
				if (num2 == 0)
				{
					_0023_003DqK2PwZ_0024m1yoPqlb4vp3mk2r6SroMenGcQAtlrwHaoa5Y_003D();
				}
				num += num2;
			}
			while (num < _0023_003Dqt7iUqtGoHoZAwmw8vC3BpyeFdXITLcySvzs2fz8e1_0024A_003D);
		}

		public void _0023_003DqUGFXjjvTcWyD4ptke6p1hSqwzeRqksTaY2aUzFvMGLA_003D()
		{
			Stream stream = _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D;
			_0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D = null;
			stream?.Close();
			_0023_003DqHeMh3f1UlA4Psi_k9ZYTlv7GjOLCMD5v3Jkn3hyuesc_003D = null;
		}

		public byte[] _0023_003DqadBDd3PURGRXccGmLMoqHykdR_0024PHJ1IBCaBMkZWxzB4_003D(int _0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D)
		{
			if (_0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D < 0)
			{
				throw new ArgumentOutOfRangeException();
			}
			byte[] array = new byte[_0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D];
			int num = 0;
			do
			{
				int num2 = _0023_003Dq_0024cCPvvvxlIU678qhVGMu_UkOjbrrRs979RAzxvfqkBM_003D.Read(array, num, _0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D);
				if (num2 == 0)
				{
					break;
				}
				num += num2;
				_0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D -= num2;
			}
			while (_0023_003DqjGy11uUmf_WhrfBCE9M0TFI_0024M2TMpG3LuODMZL1NY_s_003D > 0);
			if (num != array.Length)
			{
				byte[] array2 = new byte[num];
				Buffer.BlockCopy(array, 0, array2, 0, num);
				array = array2;
			}
			return array;
		}
	}

	private static _000E_2003_2000_200A_200A_2004_2002_2000_2007_2000_2003_2005_2000_2003_2004_2001_2003_2005_2001_2005 _0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D;

	private static _0005_2008_2002_2008_2006_2004_2008_2006_2005_2002_2008_2002_2001_2005_200A_2001_2001_2009_2003_2003_2004_2007_2004_2007_2004_200B_2001_2006_2004_2009 _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D;

	private static byte[] _0023_003DqLMxHC6WxFCOfPuzXDLyo5hz6RpMHNpBUeCJWSysfBUE_003D;

	private static short _0023_003DqKNSWa_0024clUnQTwc2BZoZSPevjF0417QzUofpxsYe67Uw_003D;

	private static int _0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D;

	private static byte[] _0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D;

	private static int _0023_003DqMMDQHGs_0024c83YjwCJSmuB_0024GkgKzuEsYYZa3HXF6_dGsY_003D;

	private static int _0023_003Dq2p8Ph47Hmu6JPXLu1KXcJAYixtRgDVArq0PHy_p92N8_003D;

	private static _0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003 _0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D;

	[MethodImpl(MethodImplOptions.NoInlining)]
	static _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D()
	{
		int num = -453529636;
		int num2 = num ^ -66437784;
		_0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D = new _000E_2003_2000_200A_200A_2004_2002_2000_2007_2000_2003_2005_2000_2003_2004_2001_2003_2005_2001_2005(872804192 + num - num2);
		int num3 = 1;
		StackTrace stackTrace = new StackTrace(num3, fNeedFileInfo: false);
		num3--;
		StackFrame frame = stackTrace.GetFrame(num3);
		int num4 = -(~(-(~(~(-(-(~(~(num ^ -18837508 ^ num2))))))))) ^ ~(-(-(~(~(-(~(-(~(-348461911 - num - num2)))))))));
		MethodBase methodBase = frame?.GetMethod();
		if (frame != null)
		{
			num4 ^= -(~(~(-(-(~(-(~(~(-(~(num ^ 0x114C3D68 ^ num2)))))))))));
		}
		Type type = methodBase?.DeclaringType;
		if ((object)type == typeof(RuntimeMethodHandle))
		{
			_0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D = (_0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003)4 | _0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D;
			num4 ^= -872800177 - num + num2 + num3;
		}
		else if ((object)type == null)
		{
			_0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D = (_0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003)1 | _0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D;
			num4 ^= -(~(-(~(-(~(~(-(~(872763939 + num - num2)))))))));
		}
		else if ((object)type.Assembly != typeof(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D).Assembly)
		{
			num4 ^= -148598767 - num + num2;
			_0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D = (_0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003)2 | _0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D;
		}
		else
		{
			num4 ^= -(~(~(-(-(~(-(~(~(-(~((34242764 + num) ^ num2))))))))))) - num3;
			_0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D = (_0002_2003_2008_2002_2000_200B_2005_2005_2000_2005_2008_2003)16 | _0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D;
		}
		_0023_003Dq2p8Ph47Hmu6JPXLu1KXcJAYixtRgDVArq0PHy_p92N8_003D = num4 + _0023_003Dq2p8Ph47Hmu6JPXLu1KXcJAYixtRgDVArq0PHy_p92N8_003D;
	}

	private static void _0023_003DqXLCM_0024cOoIa9GlIJieVnSak_0024sMWO1I7gCiMf9Xf0Yc5s_003D(byte[] _0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D, int _0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D, byte[] _0023_003DqYVB0D6BTwwmg_0024DTnnJCUPfsyxXGrHFgRQska8VKymtc_003D)
	{
		int num = 0;
		int num2 = 0;
		int num3 = 128;
		int num4 = _0023_003DqYVB0D6BTwwmg_0024DTnnJCUPfsyxXGrHFgRQska8VKymtc_003D.Length;
		while (num < num4)
		{
			if ((num3 <<= 1) == 256)
			{
				num3 = 1;
				num2 = _0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D[_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D++];
			}
			if ((num2 & num3) != 0)
			{
				int num5 = (_0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D[_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D] >> 2) + 3;
				int num6 = ((_0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D[_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D] << 8) | _0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D[_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D + 1]) & 0x3FF;
				_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D += 2;
				int num7 = num - num6;
				if (num7 < 0)
				{
					break;
				}
				while (--num5 >= 0 && num < num4)
				{
					_0023_003DqYVB0D6BTwwmg_0024DTnnJCUPfsyxXGrHFgRQska8VKymtc_003D[num++] = _0023_003DqYVB0D6BTwwmg_0024DTnnJCUPfsyxXGrHFgRQska8VKymtc_003D[num7++];
				}
			}
			else
			{
				_0023_003DqYVB0D6BTwwmg_0024DTnnJCUPfsyxXGrHFgRQska8VKymtc_003D[num++] = _0023_003DqbC7OxBrOSCPqSaLWRZOQ65JbH_SrpnQMn8qhbcXywwA_003D[_0023_003DqQRWywJchAMr1Hw67DPSTHiNfF_3rp1wUYTbrhDakH_00240_003D++];
			}
		}
	}

	[MethodImpl(MethodImplOptions.NoInlining)]
	internal static string _0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(int _0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D)
	{
		int num = 1733199245;
		int num2 = 507738754 - num;
		lock (_0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D)
		{
			byte[] array;
			int num10;
			string text;
			while (true)
			{
				text = _0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D._0023_003Dq1tBl6WakibWw7woHu7jiaw_003D_003D(_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D);
				if (text != null)
				{
					return text;
				}
				int num6;
				if (_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D == null)
				{
					Assembly executingAssembly = Assembly.GetExecutingAssembly();
					Assembly callingAssembly = Assembly.GetCallingAssembly();
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D |= 1337917930 + num - num2;
					StringBuilder stringBuilder = new StringBuilder();
					int num3 = num ^ -239447693 ^ num2;
					stringBuilder.Append((char)num3).Append((char)(num3 >> 16));
					num3 = 1873186664 + num - num2;
					stringBuilder.Append((char)(num3 >> 16)).Append((char)num3);
					num3 = -799297381 - num + num2;
					stringBuilder.Append((char)num3).Append((char)(num3 >> 16));
					num3 = (799625074 + num) ^ num2;
					stringBuilder.Append((char)(num3 >> 16)).Append((char)num3);
					num3 = -1336299361 - num + num2;
					stringBuilder.Append((char)num3);
					Stream manifestResourceStream = executingAssembly.GetManifestResourceStream(stringBuilder.ToString());
					int num4 = 1;
					StackTrace stackTrace = new StackTrace(num4, fNeedFileInfo: false);
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= (num + 1336314030 - num2) | num4;
					num4--;
					StackFrame frame = stackTrace.GetFrame(num4);
					MethodBase methodBase = frame?.GetMethod();
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= num4 + ((num ^ 0x2E458E06) + num2);
					Type type = methodBase?.DeclaringType;
					if (frame == null)
					{
						_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= num + 1336526875 - num2;
					}
					bool flag = (object)type == typeof(RuntimeMethodHandle);
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= -1336307400 - num + num2;
					if (!flag)
					{
						flag = (object)type == null;
						if (flag)
						{
							_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= (1336485593 + num) ^ num2;
						}
					}
					if (flag == (stackTrace != null))
					{
						_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D = 0x20 ^ _0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D;
					}
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D ^= (507745256 - num - num2) | (1 + num4);
					_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D = new _0005_2008_2002_2008_2006_2004_2008_2006_2005_2002_2008_2002_2001_2005_200A_2001_2001_2009_2003_2003_2004_2007_2004_2007_2004_200B_2001_2006_2004_2009(manifestResourceStream);
					short num5 = (short)(_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003Dqw5_0024h5ZpOSEzY7IpQmoBg9ZZXfS9cYNuXjqKAtHlovKI_003D() ^ (short)(-(~(~(-(-(~(-(~(~((num + 1336288730) ^ num2)))))))))));
					if (num5 == 0)
					{
						_0023_003DqKNSWa_0024clUnQTwc2BZoZSPevjF0417QzUofpxsYe67Uw_003D = (short)(_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003Dqw5_0024h5ZpOSEzY7IpQmoBg9ZZXfS9cYNuXjqKAtHlovKI_003D() ^ (short)(~(-(-(~(~(-(~(-(~(-1336279045 - num + num2)))))))))));
					}
					else
					{
						_0023_003DqLMxHC6WxFCOfPuzXDLyo5hz6RpMHNpBUeCJWSysfBUE_003D = _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003DqadBDd3PURGRXccGmLMoqHykdR_0024PHJ1IBCaBMkZWxzB4_003D(num5);
					}
					callingAssembly = executingAssembly;
					AssemblyName assemblyName;
					try
					{
						assemblyName = callingAssembly.GetName();
					}
					catch
					{
						assemblyName = new AssemblyName(callingAssembly.FullName);
					}
					_0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D = assemblyName.GetPublicKeyToken();
					if (_0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D != null && _0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D.Length == 0)
					{
						_0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D = null;
					}
					num6 = _0023_003Dq2p8Ph47Hmu6JPXLu1KXcJAYixtRgDVArq0PHy_p92N8_003D;
					_0023_003Dq2p8Ph47Hmu6JPXLu1KXcJAYixtRgDVArq0PHy_p92N8_003D = 0;
					long num7 = _0023_003Dqewxqtvf1xuhfD1ZxsyKiAKYQL7oX4ptDwPz0zyL0uBY_003D._0023_003DqdLpxDZlk7UBJfxXFF9Izvg_003D_003D();
					num6 ^= (int)num7;
					num6 ^= 1816917281 + num - num2;
					num6 ^= (num ^ -776955830 ^ num2) + -(~(~(-(~(-(-(~(~(-(~(507738446 - num - num2)))))))))));
					num6 ^= -(~(-(~(-(~(~(-(~((0x647F4956 ^ num) + num2)))))))));
					_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D = (_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D & (num + 1604742874 - num2)) ^ ((507737086 - num) ^ num2);
					_0023_003DqMMDQHGs_0024c83YjwCJSmuB_0024GkgKzuEsYYZa3HXF6_dGsY_003D = num6;
					if (((uint)_0023_003DqBqQ3G0fj1hf2s7xuOf5uVyoO8ZC88IRIBYoNUULDvgg_003D & (uint)(-(~(~(-(-(~(-(~(-(~(~(-507738768 + num + num2))))))))))))) == 0)
					{
						_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D = (507700444 - num) ^ num2;
					}
				}
				else
				{
					num6 = _0023_003DqMMDQHGs_0024c83YjwCJSmuB_0024GkgKzuEsYYZa3HXF6_dGsY_003D;
				}
				if (_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D == num + 1336351522 - num2)
				{
					return new string(new char[3]
					{
						(char)((507738682 - num) ^ num2),
						'0',
						(char)((-776310592 ^ num) - num2)
					});
				}
				int num8 = _0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D ^ (755638932 + num + num2) ^ num6;
				num8 ^= (529785011 - num) ^ num2;
				_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003Dqb87xY_0024z_0024L9NF_6mmyv2CBMjXMbRGotFsi8xBw2CzJX0_003D().Position = num8;
				if (_0023_003DqLMxHC6WxFCOfPuzXDLyo5hz6RpMHNpBUeCJWSysfBUE_003D != null)
				{
					array = _0023_003DqLMxHC6WxFCOfPuzXDLyo5hz6RpMHNpBUeCJWSysfBUE_003D;
				}
				else
				{
					short num9 = ((_0023_003DqKNSWa_0024clUnQTwc2BZoZSPevjF0417QzUofpxsYe67Uw_003D != -1) ? _0023_003DqKNSWa_0024clUnQTwc2BZoZSPevjF0417QzUofpxsYe67Uw_003D : ((short)(_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003Dqw5_0024h5ZpOSEzY7IpQmoBg9ZZXfS9cYNuXjqKAtHlovKI_003D() ^ ((-776322064 ^ num) - num2) ^ num8)));
					if (num9 == 0)
					{
						array = null;
					}
					else
					{
						array = _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003DqadBDd3PURGRXccGmLMoqHykdR_0024PHJ1IBCaBMkZWxzB4_003D(num9);
						for (int i = 0; i != array.Length; i++)
						{
							array[i] ^= (byte)(_0023_003DqMMDQHGs_0024c83YjwCJSmuB_0024GkgKzuEsYYZa3HXF6_dGsY_003D >> ((i & 3) << 3));
						}
					}
				}
				num10 = _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003Dqy_0024Gzg9UCkFWmSBnb9d_0024T_d_BDyzvvBFzkcIZFTDNOEc_003D() ^ num8 ^ -(~(-(~(~(-(-(~(~(-1860131875 - num + num2))))))))) ^ num6;
				if (num10 != (num ^ 0x2E458E86 ^ num2))
				{
					break;
				}
				byte[] array2 = _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003DqadBDd3PURGRXccGmLMoqHykdR_0024PHJ1IBCaBMkZWxzB4_003D(4);
				_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D = (1860131876 + num - num2) ^ num6;
				_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D = (array2[2] | (array2[3] << 16) | (array2[0] << 8) | (array2[1] << 24)) ^ -_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D;
			}
			bool flag2 = (num10 & (num + 566003070 + num2)) != 0;
			bool flag3 = (num10 & (num ^ -239439496 ^ num2)) != 0;
			bool flag4 = (num10 & (-1639744894 - num - num2)) != 0;
			num10 &= num ^ -565866873 ^ num2;
			byte[] array3 = _0023_003DqUVRKpJOdrDmWYOn_00240RZOGaxHIrgGQkHlI_a3NXXHMwOVYjt_n_AbEjryifcaqIG2._0023_003DqHphNwXOj6tfRhNZoZMAImQ_003D_003D(array, _0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003DqadBDd3PURGRXccGmLMoqHykdR_0024PHJ1IBCaBMkZWxzB4_003D(num10));
			if (_0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D != null != (_0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D != 1337915374 + num - num2))
			{
				for (int num11 = 0; num11 < num10; num11 = 1 + num11)
				{
					byte b = _0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D[num11 & 7];
					b = (byte)((b << 3) | (b >> 5));
					array3[num11] ^= b;
				}
			}
			int num12 = _0023_003DqzIinjIZzKEngxlPQo6dTp20OeTY09YWHNz6L95xaZdw_003D - 12;
			int num13;
			byte[] array4;
			if (!flag2)
			{
				num13 = num10;
				array4 = array3;
			}
			else
			{
				num13 = array3[2] | (array3[0] << 16) | (array3[3] << 8) | (array3[1] << 24);
				array4 = new byte[num13];
				_0023_003DqXLCM_0024cOoIa9GlIJieVnSak_0024sMWO1I7gCiMf9Xf0Yc5s_003D(array3, 4, array4);
			}
			if (flag3 && num12 == (-777848574 ^ num ^ num2))
			{
				char[] array5 = new char[num13];
				for (int num14 = 0; num14 < num13; num14 = 1 + num14)
				{
					array5[num14] = (char)array4[num14];
				}
				text = new string(array5);
			}
			else
			{
				text = Encoding.Unicode.GetString(array4, 0, array4.Length);
			}
			num12 += -1336307433 - num + num2 + (3 & num12) << 5;
			if (num12 != (num ^ -800913406) - num2)
			{
				int num15 = (_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D + num10) ^ (-1335370992 - num + num2) ^ (num12 & (num ^ -776309643 ^ num2));
				StringBuilder stringBuilder = new StringBuilder();
				int num3 = -1336307472 - num + num2;
				stringBuilder.Append((char)(byte)num3);
				text = num15.ToString(stringBuilder.ToString());
			}
			if (!flag4)
			{
				text = string.Intern(text);
				_0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D._0023_003DqWkLahNSGMK2L_0024vbnEmTn_0024Q_003D_003D(_0023_003DqaKecWaCG0ay03zI11oU4_sYKVql7BsFzu9PrnsV9Utw_003D, text);
				if (_0023_003Dq2peh3pzS9xJgQtgpIrRhDjXouxzO3ZKvO6_5EgxUc0w_003D._0023_003DqKVLxjoaPakI0xp2BQVg8OkH1_SOtchUS_00249KUMW3Wrjg_003D() == (num ^ -776239888) - num2)
				{
					_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D._0023_003DqUGFXjjvTcWyD4ptke6p1hSqwzeRqksTaY2aUzFvMGLA_003D();
					_0023_003DqA1DewHopsyLqT1DLmePNt2Z7eqT8YPHNOAwa7ilt3Lo_003D = null;
					_0023_003DqLMxHC6WxFCOfPuzXDLyo5hz6RpMHNpBUeCJWSysfBUE_003D = (_0023_003Dqs4X9YptzEBRw_0024ybc8KDW3D9hDpsDC6S3hIOyC_0024LYaV0_003D = null);
				}
			}
			return text;
		}
	}
}
