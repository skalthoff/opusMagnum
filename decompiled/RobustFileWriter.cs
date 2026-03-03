using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

public sealed class RobustFileWriter
{
	private sealed class _0023_003DqQ0confmu_0024onuFTr7ey_HCA_0024qOPBaE4a3a_2ad6fzuNE_003D
	{
		public string _0023_003DqUS7pDMnUcsEeYOrNQicgug_003D_003D;

		internal bool _0023_003DqwwdNpGxw0CxKJRRRaoqIyOnT4WLu_0024n6bGB3oaDjcLYE_003D(PendingFileWrite _0023_003Dq8mk9P7ZyIdXNfGLXqgehwA_003D_003D)
		{
			return _0023_003Dq8mk9P7ZyIdXNfGLXqgehwA_003D_003D._0023_003DqLy8nRpTAQBntybGu1I1f6A_003D_003D == _0023_003DqUS7pDMnUcsEeYOrNQicgug_003D_003D;
		}
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Predicate<PendingFileWrite> _003C_003E9__6_0;

		internal bool _0023_003DqEqBCLlLJgLmF6cnogXcVvb4wN4_4WOFgTeBu6P5Wq6E_003D(PendingFileWrite _0023_003Dqb2ooEllzHEUDl3xA7l06TA_003D_003D)
		{
			return _0023_003Dqb2ooEllzHEUDl3xA7l06TA_003D_003D._0023_003Dq4tNqhmMngw04p9VbrTzzaQ_003D_003D;
		}
	}

	private sealed class PendingFileWrite
	{
		public readonly string _0023_003DqLy8nRpTAQBntybGu1I1f6A_003D_003D;

		public readonly byte[] _0023_003Dqhp_00242Jtj7HgZdOQcp_GpR5w_003D_003D;

		public bool _0023_003Dq4tNqhmMngw04p9VbrTzzaQ_003D_003D;

		public int _0023_003DqGUPJ2hSxN0gREc4BprtESg_003D_003D;

		public PendingFileWrite(string _0023_003DqZHrM3eJQIa4MLnMZZ3jcPg_003D_003D, byte[] _0023_003DqfZ65nKX0dwpgbbd6HJjSFg_003D_003D)
		{
			_0023_003DqLy8nRpTAQBntybGu1I1f6A_003D_003D = _0023_003DqZHrM3eJQIa4MLnMZZ3jcPg_003D_003D;
			_0023_003Dqhp_00242Jtj7HgZdOQcp_GpR5w_003D_003D = _0023_003DqfZ65nKX0dwpgbbd6HJjSFg_003D_003D;
		}
	}

	private static readonly int _0023_003Dq4zBTh4uvFRfIWpQCJ0Ximg_003D_003D = 20;

	private static readonly TimeSpan _0023_003DqaXwaNvOyL6jmISCFxYHKvC43FobuCfm0RWX3Jai0KLk_003D = TimeSpan.FromSeconds(1.0);

	private DateTime _0023_003DqN0tmQfzPUqwZVFGyNAuqtQ_003D_003D = DateTime.MinValue;

	private List<PendingFileWrite> _0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D = new List<PendingFileWrite>();

	public void _0023_003DqLEillCIrRAUbDwKHmCp1AQ_003D_003D(string _0023_003Dqw8hGopxSvWYRj8TbzlkFeA_003D_003D, byte[] _0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D)
	{
		_0023_003DqQ0confmu_0024onuFTr7ey_HCA_0024qOPBaE4a3a_2ad6fzuNE_003D CS_0024_003C_003E8__locals3 = new _0023_003DqQ0confmu_0024onuFTr7ey_HCA_0024qOPBaE4a3a_2ad6fzuNE_003D();
		CS_0024_003C_003E8__locals3._0023_003DqUS7pDMnUcsEeYOrNQicgug_003D_003D = _0023_003Dqw8hGopxSvWYRj8TbzlkFeA_003D_003D;
		_0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D.RemoveAll((PendingFileWrite _0023_003Dq8mk9P7ZyIdXNfGLXqgehwA_003D_003D) => _0023_003Dq8mk9P7ZyIdXNfGLXqgehwA_003D_003D._0023_003DqLy8nRpTAQBntybGu1I1f6A_003D_003D == CS_0024_003C_003E8__locals3._0023_003DqUS7pDMnUcsEeYOrNQicgug_003D_003D);
		_0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D.Add(new PendingFileWrite(CS_0024_003C_003E8__locals3._0023_003DqUS7pDMnUcsEeYOrNQicgug_003D_003D, _0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D));
		_0023_003DqMONZKwXfLxwUJ9op9t2w9g_003D_003D();
	}

	public void _0023_003Dq8538ntTv9vI9I_0024SEEUBkWg_003D_003D(string _0023_003DqKTzC44407FJmaTI1onNEfg_003D_003D, string _0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D)
	{
		_0023_003DqLEillCIrRAUbDwKHmCp1AQ_003D_003D(_0023_003DqKTzC44407FJmaTI1onNEfg_003D_003D, Encoding.ASCII.GetBytes(_0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D));
	}

	public void _0023_003DqMONZKwXfLxwUJ9op9t2w9g_003D_003D()
	{
		TimeSpan timeSpan = DateTime.Now - _0023_003DqN0tmQfzPUqwZVFGyNAuqtQ_003D_003D;
		if (_0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D.Count == 0 || timeSpan < _0023_003DqaXwaNvOyL6jmISCFxYHKvC43FobuCfm0RWX3Jai0KLk_003D)
		{
			return;
		}
		foreach (PendingFileWrite item in _0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D)
		{
			try
			{
				File.WriteAllBytes(item._0023_003DqLy8nRpTAQBntybGu1I1f6A_003D_003D, item._0023_003Dqhp_00242Jtj7HgZdOQcp_GpR5w_003D_003D);
				item._0023_003Dq4tNqhmMngw04p9VbrTzzaQ_003D_003D = true;
			}
			catch (Exception _0023_003DqTpi4EGBhCwe8zIPg8_0024pl9Q_003D_003D)
			{
				item._0023_003DqGUPJ2hSxN0gREc4BprtESg_003D_003D++;
				if (!_0023_003DqrdMSrn2dcGXkc0mBwD65vaGLITnU3RARs5_00241ivL11Kc_003D(_0023_003DqTpi4EGBhCwe8zIPg8_0024pl9Q_003D_003D) || item._0023_003DqGUPJ2hSxN0gREc4BprtESg_003D_003D >= _0023_003Dq4zBTh4uvFRfIWpQCJ0Ximg_003D_003D)
				{
					throw;
				}
			}
		}
		_0023_003DqCdiBokguvwYTHnM_0024_7CRlA_003D_003D.RemoveAll(_003C_003Ec._003C_003E9._0023_003DqEqBCLlLJgLmF6cnogXcVvb4wN4_4WOFgTeBu6P5Wq6E_003D);
		_0023_003DqN0tmQfzPUqwZVFGyNAuqtQ_003D_003D = DateTime.Now;
	}

	private bool _0023_003DqrdMSrn2dcGXkc0mBwD65vaGLITnU3RARs5_00241ivL11Kc_003D(Exception _0023_003DqTpi4EGBhCwe8zIPg8_0024pl9Q_003D_003D)
	{
		if (!(_0023_003DqTpi4EGBhCwe8zIPg8_0024pl9Q_003D_003D is IOException))
		{
			return _0023_003DqTpi4EGBhCwe8zIPg8_0024pl9Q_003D_003D is UnauthorizedAccessException;
		}
		return true;
	}
}
