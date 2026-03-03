using System.Collections;
using System.Collections.Generic;
using System.Reflection;

[DefaultMember("Item")]
public struct _0023_003DqCeAEwhNataLenIe8TD123Q_003D_003D<_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D> : IEnumerable<_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D>, IEnumerable
{
	private readonly IList<_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D> _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D;

	public _0023_003DqCeAEwhNataLenIe8TD123Q_003D_003D(IList<_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D> _0023_003DqtUSO6AQogno5fRIwZea_0024qQ_003D_003D)
	{
		_0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D = _0023_003DqtUSO6AQogno5fRIwZea_0024qQ_003D_003D;
	}

	public int _0023_003DqnrASNNWYjMlBAnTu1tdnQA_003D_003D()
	{
		return _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D.Count;
	}

	public _0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D _0023_003DqsBrCCezD6gT1qnb7loJ12w_003D_003D(int _0023_003DqCpxeJyXrYxeN2okK33aOaQ_003D_003D)
	{
		return _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D[_0023_003DqCpxeJyXrYxeN2okK33aOaQ_003D_003D];
	}

	public IEnumerator<_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D> GetEnumerator()
	{
		return _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D.GetEnumerator();
	}

	private IEnumerator _0023_003DqMdfccKIq_W7fcMO6p7J8ID4XuFms4iqmDrOwZ8iYRTYw8LRoLMiAqFOxvvry6mCr()
	{
		return _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D.GetEnumerator();
	}

	IEnumerator IEnumerable.GetEnumerator()
	{
		//ILSpy generated this explicit interface implementation from .override directive in #=qMdfccKIq_W7fcMO6p7J8ID4XuFms4iqmDrOwZ8iYRTYw8LRoLMiAqFOxvvry6mCr
		return this._0023_003DqMdfccKIq_W7fcMO6p7J8ID4XuFms4iqmDrOwZ8iYRTYw8LRoLMiAqFOxvvry6mCr();
	}

	public int _0023_003DqLve9xlvx_0024djaBlSAgguHjw_003D_003D(_0023_003Dqk6gw_kzSLsqxjKiBg9ioUQ_003D_003D _0023_003DqTS8RnZ0zkWVAclVwOCzNjw_003D_003D)
	{
		return _0023_003DqbM_0024iVjWaFfF_GCJKICWTPg_003D_003D.IndexOf(_0023_003DqTS8RnZ0zkWVAclVwOCzNjw_003D_003D);
	}
}
