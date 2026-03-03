using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.CompilerServices;

[DebuggerDisplay("[{Start}, {Size}]")]
public struct Range2
{
	private sealed class _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D : IEnumerator<Index2>, IEnumerable<Index2>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D;

		private Index2 _0023_003DqwnMsDRMK4ZMrwAjD7sUSAg_003D_003D;

		private int _0023_003DqHm1LorQPnthnGsc_0024svqaYbUs4_a9Tp7uKE1yqlzXwL4_003D;

		public Range2 _0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D;

		public Range2 _0023_003DqEQs4WXciviGhi4uRLOYGBA_003D_003D;

		private int _0023_003Dq0hW7GKKkKwXGLPoonbXfuA_003D_003D;

		private int _0023_003Dq9Qhoxzf0Up9pC2LHnhLv9g_003D_003D;

		[DebuggerHidden]
		public _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D(int _0023_003Dq_N4RBY3krqqJtyzkLjfY_w_003D_003D)
		{
			_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D = _0023_003Dq_N4RBY3krqqJtyzkLjfY_w_003D_003D;
			_0023_003DqHm1LorQPnthnGsc_0024svqaYbUs4_a9Tp7uKE1yqlzXwL4_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqHIY_0024pwKqxsio7iVrsjjs3SqtMjMoRmWIlstfNAomimU_003D()
		{
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qHIY$pwKqxsio7iVrsjjs3SqtMjMoRmWIlstfNAomimU=
			this._0023_003DqHIY_0024pwKqxsio7iVrsjjs3SqtMjMoRmWIlstfNAomimU_003D();
		}

		private bool MoveNext()
		{
			int num = _0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D;
			if (num != 0)
			{
				if (num != 1)
				{
					return false;
				}
				_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D = -1;
				_0023_003Dq9Qhoxzf0Up9pC2LHnhLv9g_003D_003D++;
				goto IL_007e;
			}
			_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D = -1;
			_0023_003Dq0hW7GKKkKwXGLPoonbXfuA_003D_003D = _0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D.Start.Y;
			goto IL_00a6;
			IL_007e:
			if (_0023_003Dq9Qhoxzf0Up9pC2LHnhLv9g_003D_003D < _0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D.End.X)
			{
				_0023_003DqwnMsDRMK4ZMrwAjD7sUSAg_003D_003D = new Index2(_0023_003Dq9Qhoxzf0Up9pC2LHnhLv9g_003D_003D, _0023_003Dq0hW7GKKkKwXGLPoonbXfuA_003D_003D);
				_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D = 1;
				return true;
			}
			_0023_003Dq0hW7GKKkKwXGLPoonbXfuA_003D_003D++;
			goto IL_00a6;
			IL_00a6:
			if (_0023_003Dq0hW7GKKkKwXGLPoonbXfuA_003D_003D < _0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D.End.Y)
			{
				_0023_003Dq9Qhoxzf0Up9pC2LHnhLv9g_003D_003D = _0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D.Start.X;
				goto IL_007e;
			}
			return false;
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		[DebuggerHidden]
		private Index2 _0023_003DqY4pspj7Ke89QSiXW6LDBBlJC0FgX9b9yh3pF8qwnWnQpcum_0024g3pyx2oXmVTTtRTxMRuuYB95_0024ht8GrKkxG6FUA_003D_003D()
		{
			return _0023_003DqwnMsDRMK4ZMrwAjD7sUSAg_003D_003D;
		}

		Index2 IEnumerator<Index2>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qY4pspj7Ke89QSiXW6LDBBlJC0FgX9b9yh3pF8qwnWnQpcum$g3pyx2oXmVTTtRTxMRuuYB95$ht8GrKkxG6FUA==
			return this._0023_003DqY4pspj7Ke89QSiXW6LDBBlJC0FgX9b9yh3pF8qwnWnQpcum_0024g3pyx2oXmVTTtRTxMRuuYB95_0024ht8GrKkxG6FUA_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003Dq91oDOODmWH2cD2Lr6Klw_mrvtxTup0I9z_0024W_0024o8p5W_9oAGH5Slecn1wfLRY_6PtB()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q91oDOODmWH2cD2Lr6Klw_mrvtxTup0I9z$W$o8p5W_9oAGH5Slecn1wfLRY_6PtB
			this._0023_003Dq91oDOODmWH2cD2Lr6Klw_mrvtxTup0I9z_0024W_0024o8p5W_9oAGH5Slecn1wfLRY_6PtB();
		}

		[DebuggerHidden]
		private object _0023_003DqNYJNQRqtIj_TW0XcnZ_2LHu3Jr0dv12GlPpr6fABaV_DSSv2JsYmeCrwT2xkpuY8()
		{
			return _0023_003DqwnMsDRMK4ZMrwAjD7sUSAg_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qNYJNQRqtIj_TW0XcnZ_2LHu3Jr0dv12GlPpr6fABaV_DSSv2JsYmeCrwT2xkpuY8
			return this._0023_003DqNYJNQRqtIj_TW0XcnZ_2LHu3Jr0dv12GlPpr6fABaV_DSSv2JsYmeCrwT2xkpuY8();
		}

		[DebuggerHidden]
		private IEnumerator<Index2> _0023_003Dq7Yhu7RA7UD9xL7GzlWqKJr_0024mum_f_cSJPRvcJp_0024n47Dvk5GH7sGGkP80Ftzg89xewmv35jsPAI94qG2J9ZazQA_003D_003D()
		{
			_0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D;
			if (_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D == -2 && _0023_003DqHm1LorQPnthnGsc_0024svqaYbUs4_a9Tp7uKE1yqlzXwL4_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003DqKezk_0024zutsO61HjnimQVdQw_003D_003D = 0;
				_0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D = this;
			}
			else
			{
				_0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D = new _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D(0);
			}
			_0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D._0023_003DqfCWbRcKv00_0024o_0024lGaq0cOwQ_003D_003D = _0023_003DqEQs4WXciviGhi4uRLOYGBA_003D_003D;
			return _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D;
		}

		IEnumerator<Index2> IEnumerable<Index2>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q7Yhu7RA7UD9xL7GzlWqKJr$mum_f_cSJPRvcJp$n47Dvk5GH7sGGkP80Ftzg89xewmv35jsPAI94qG2J9ZazQA==
			return this._0023_003Dq7Yhu7RA7UD9xL7GzlWqKJr_0024mum_f_cSJPRvcJp_0024n47Dvk5GH7sGGkP80Ftzg89xewmv35jsPAI94qG2J9ZazQA_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003Dq1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2()
		{
			return _0023_003Dq7Yhu7RA7UD9xL7GzlWqKJr_0024mum_f_cSJPRvcJp_0024n47Dvk5GH7sGGkP80Ftzg89xewmv35jsPAI94qG2J9ZazQA_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2
			return this._0023_003Dq1ktflj60IkSMcGpnElB1qOUaOMudbpYY949fOvzBdAoLRuyviu3eWQJc2zQjypk2();
		}
	}

	public readonly Index2 Start;

	public readonly Index2 End;

	public static readonly Range2 Empty = new Range2(Index2.Zero, Index2.Zero);

	public Index2 Size => End - Start;

	public IEnumerable<Index2> Indexes
	{
		[IteratorStateMachine(typeof(_0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D))]
		get
		{
			return new _0023_003DqOFG1wH151qhFFvuyTlYYQdBuBwCykzRgCJtllmabWso_003D(-2)
			{
				_0023_003DqEQs4WXciviGhi4uRLOYGBA_003D_003D = this
			};
		}
	}

	public Range2(Index2 start, Index2 end)
	{
		Start = start;
		End = end;
	}

	public static Range2 FromZero(Index2 size)
	{
		return new Range2(Index2.Zero, size);
	}

	public static Range2 WithSize(Index2 start, Index2 size)
	{
		return new Range2(start, start + size);
	}

	public static Range2 WithSize(int x, int y, int width, int height)
	{
		return WithSize(new Index2(x, y), new Index2(width, height));
	}

	public bool Contains(Index2 index)
	{
		if (index.X >= Start.X && index.X < End.X && index.Y >= Start.Y)
		{
			return index.Y < End.Y;
		}
		return false;
	}

	public bool Contains(Range2 range)
	{
		if (range.Start.X >= Start.X && range.End.X <= End.X && range.Start.Y >= Start.Y)
		{
			return range.End.Y <= End.Y;
		}
		return false;
	}

	public bool Overlaps(Range2 other)
	{
		return End.X > other.Start.X && other.End.X > Start.X && End.Y > other.Start.Y && other.End.Y > Start.Y;
	}

	public Range2 UnionedWith(Index2 point)
	{
		if (Size.X == 0)
		{
			return new Range2(point, point + new Index2(1, 1));
		}
		return new Range2(new Index2(Math.Min(Start.X, point.X), Math.Min(Start.Y, point.Y)), new Index2(Math.Max(End.X, point.X + 1), Math.Max(End.Y, point.Y + 1)));
	}

	public Range2 Translated(Index2 delta)
	{
		return new Range2(Start + delta, End + delta);
	}

	public Range2 Expanded(int w, int h)
	{
		Index2 index = new Index2(w, h);
		return new Range2(Start - index, End + 2 * index);
	}
}
